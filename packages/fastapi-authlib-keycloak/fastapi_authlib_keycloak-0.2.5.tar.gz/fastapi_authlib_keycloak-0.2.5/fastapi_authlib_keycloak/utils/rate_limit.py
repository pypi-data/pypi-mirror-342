#!/usr/bin/env python3
"""
Rate limiting utilities for FastAPI-Authlib-Keycloak.

This module provides comprehensive rate limiting capabilities to protect
authentication endpoints from abuse, with support for multiple strategies,
storage backends, and configuration options.

Features:
- Multiple rate limiting strategies (fixed window, sliding window, token bucket)
- Various scope options (IP-based, client-based, user-based)
- Flexible storage backends (in-memory, Redis)
- Integration with metrics for monitoring
- FastAPI middleware for easy application
"""

import time
import math
import uuid
import logging
import threading
import asyncio
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Set, Tuple, Optional, Any, Union, Callable, Type

from fastapi import FastAPI, Request, Response, HTTPException, status, Depends
from fastapi.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint

# Try to import Redis if available
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

# Try to import metrics if available
try:
    from fastapi_authlib_keycloak.utils.metrics import (
        increment_counter,
        set_gauge,
        observe_histogram,
        record_rate_limit_hit
    )
    METRICS_AVAILABLE = True
except ImportError:
    METRICS_AVAILABLE = False
    # Create stub functions if metrics not available
    def increment_counter(*args, **kwargs):
        pass
    
    def set_gauge(*args, **kwargs):
        pass
    
    def observe_histogram(*args, **kwargs):
        pass
    
    def record_rate_limit_hit(*args, **kwargs):
        pass


# Create logger
logger = logging.getLogger("fastapi-keycloak.rate-limit")


class RateLimitStrategy(str, Enum):
    """Enumeration of rate limiting strategies."""
    FIXED_WINDOW = "fixed"
    SLIDING_WINDOW = "sliding"
    TOKEN_BUCKET = "token_bucket"


class RateLimitScope(str, Enum):
    """Enumeration of rate limiting scopes."""
    IP = "ip"
    CLIENT = "client"
    USER = "user"
    COMBINED = "combined"


class RateLimitExceeded(Exception):
    """Exception raised when a rate limit is exceeded."""
    
    def __init__(
        self,
        message: str = "Rate limit exceeded",
        limit: int = 0,
        remaining: int = 0,
        reset: int = 0,
        retry_after: int = 0,
        scope: str = ""
    ):
        """
        Initialize rate limit exceeded exception.
        
        Args:
            message: Error message
            limit: The request limit
            remaining: Remaining requests in window
            reset: Seconds until the limit resets
            retry_after: Seconds to wait before retrying
            scope: Scope that was limited (ip, client, user)
        """
        self.message = message
        self.limit = limit
        self.remaining = remaining
        self.reset = reset
        self.retry_after = retry_after
        self.scope = scope
        super().__init__(self.message)


class BaseRateLimitStrategy(ABC):
    """
    Abstract base class for rate limiting strategies.
    
    This defines the interface that all rate limiting strategies must implement.
    """
    
    @abstractmethod
    async def check_and_update(
        self,
        key: str,
        storage: 'BaseRateLimitStorage',
        increment: bool = True
    ) -> Tuple[bool, int, int]:
        """
        Check if a request exceeds the rate limit and update the counter.
        
        Args:
            key: Identifier for the rate limit (e.g., IP address, client ID)
            storage: Storage backend to use
            increment: Whether to increment the counter or just check
            
        Returns:
            Tuple[bool, int, int]: (is_allowed, remaining, reset_seconds)
        """
        pass


class FixedWindowStrategy(BaseRateLimitStrategy):
    """
    Fixed window rate limiting strategy.
    
    This strategy uses fixed time windows (e.g., 1 minute, 1 hour) and resets
    the counter at the beginning of each window.
    """
    
    def __init__(self, max_requests: int, window_seconds: int):
        """
        Initialize fixed window strategy.
        
        Args:
            max_requests: Maximum number of requests allowed in the window
            window_seconds: Time window in seconds
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
    
    async def check_and_update(
        self,
        key: str,
        storage: 'BaseRateLimitStorage',
        increment: bool = True
    ) -> Tuple[bool, int, int]:
        """
        Check if a request exceeds the rate limit and update the counter.
        
        Args:
            key: Identifier for the rate limit (e.g., IP address, client ID)
            storage: Storage backend to use
            increment: Whether to increment the counter or just check
            
        Returns:
            Tuple[bool, int, int]: (is_allowed, remaining, reset_seconds)
        """
        # Calculate the current window timestamp
        current_time = int(time.time())
        window_start = current_time - (current_time % self.window_seconds)
        window_key = f"{key}:{window_start}"
        
        # Calculate reset time
        reset_seconds = self.window_seconds - (current_time % self.window_seconds)
        
        # Get current count
        count = await storage.get(window_key)
        if count is None:
            count = 0
            
        # Check if limit would be exceeded
        is_allowed = count < self.max_requests
        
        # Increment counter if allowed and increment is requested
        if is_allowed and increment:
            # Use storage increment to handle race conditions
            count = await storage.increment(window_key, 1, self.window_seconds)
            is_allowed = count <= self.max_requests
            
        # Calculate remaining requests
        remaining = max(0, self.max_requests - count)
        
        return is_allowed, remaining, reset_seconds


class SlidingWindowStrategy(BaseRateLimitStrategy):
    """
    Sliding window rate limiting strategy.
    
    This strategy uses a sliding time window, which is more accurate but
    more complex than fixed window. It combines the current and previous
    windows with appropriate weights.
    """
    
    def __init__(self, max_requests: int, window_seconds: int):
        """
        Initialize sliding window strategy.
        
        Args:
            max_requests: Maximum number of requests allowed in the window
            window_seconds: Time window in seconds
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
    
    async def check_and_update(
        self,
        key: str,
        storage: 'BaseRateLimitStorage',
        increment: bool = True
    ) -> Tuple[bool, int, int]:
        """
        Check if a request exceeds the rate limit and update the counter.
        
        Args:
            key: Identifier for the rate limit (e.g., IP address, client ID)
            storage: Storage backend to use
            increment: Whether to increment the counter or just check
            
        Returns:
            Tuple[bool, int, int]: (is_allowed, remaining, reset_seconds)
        """
        # Calculate current and previous window timestamps
        current_time = int(time.time())
        current_window = current_time - (current_time % self.window_seconds)
        previous_window = current_window - self.window_seconds
        
        # Calculate the position in the current window (0.0 to 1.0)
        position = (current_time - current_window) / self.window_seconds
        
        # Generate keys for current and previous windows
        current_key = f"{key}:{current_window}"
        previous_key = f"{key}:{previous_window}"
        
        # Get counts from both windows
        current_count = await storage.get(current_key) or 0
        previous_count = await storage.get(previous_key) or 0
        
        # Calculate weighted count using the sliding window formula
        # This weights the previous window's count by how much it overlaps
        # with our sliding window of interest
        weighted_count = current_count + previous_count * (1 - position)
        
        # Check if limit would be exceeded
        is_allowed = weighted_count < self.max_requests
        
        # Increment counter if allowed and increment is requested
        if is_allowed and increment:
            # Use storage increment to handle race conditions
            current_count = await storage.increment(current_key, 1, self.window_seconds)
            
            # Recalculate weighted count
            weighted_count = current_count + previous_count * (1 - position)
            is_allowed = weighted_count <= self.max_requests
            
        # Calculate remaining requests (this is approximate for sliding window)
        remaining = max(0, math.floor(self.max_requests - weighted_count))
        
        # Calculate reset time (approximate for sliding window)
        # This is the time until the current request "slides out" of the window
        reset_seconds = self.window_seconds
        
        return is_allowed, remaining, reset_seconds


class TokenBucketStrategy(BaseRateLimitStrategy):
    """
    Token bucket rate limiting strategy.
    
    This strategy uses a token bucket algorithm, which allows for bursts of
    traffic while still maintaining a long-term rate limit. Tokens are added
    to the bucket at a fixed rate, and each request consumes a token.
    """
    
    def __init__(
        self,
        max_tokens: int,
        refill_rate: float,
        refill_interval: int = 1
    ):
        """
        Initialize token bucket strategy.
        
        Args:
            max_tokens: Maximum number of tokens in the bucket
            refill_rate: Tokens to add per interval
            refill_interval: Interval in seconds for token refill
        """
        self.max_tokens = max_tokens
        self.refill_rate = refill_rate
        self.refill_interval = refill_interval
    
    async def check_and_update(
        self,
        key: str,
        storage: 'BaseRateLimitStorage',
        increment: bool = True
    ) -> Tuple[bool, int, int]:
        """
        Check if a request exceeds the rate limit and update the counter.
        
        Args:
            key: Identifier for the rate limit (e.g., IP address, client ID)
            storage: Storage backend to use
            increment: Whether to increment the counter or just check
            
        Returns:
            Tuple[bool, int, int]: (is_allowed, remaining, reset_seconds)
        """
        # Token bucket requires two values: tokens and last update time
        tokens_key = f"{key}:tokens"
        timestamp_key = f"{key}:timestamp"
        
        # Get current tokens and last update time
        tokens = await storage.get(tokens_key)
        last_update = await storage.get(timestamp_key)
        
        # Initialize if not exists
        current_time = time.time()
        if tokens is None:
            tokens = self.max_tokens
            last_update = current_time
        else:
            if last_update is None:
                last_update = current_time
            else:
                last_update = float(last_update)
        
        # Calculate token refill based on time elapsed
        elapsed = current_time - last_update
        refill = elapsed * (self.refill_rate / self.refill_interval)
        tokens = min(self.max_tokens, tokens + refill)
        
        # Check if a token is available
        is_allowed = tokens >= 1
        
        # Consume token if allowed and increment is requested
        if is_allowed and increment:
            tokens -= 1
            # Update storage
            await storage.set(tokens_key, tokens, self.max_tokens / self.refill_rate * self.refill_interval * 2)
            await storage.set(timestamp_key, current_time, self.max_tokens / self.refill_rate * self.refill_interval * 2)
        
        # Calculate remaining tokens
        remaining = math.floor(tokens)
        
        # Calculate reset time (time until one token is refilled)
        if tokens < self.max_tokens:
            reset_seconds = (1 / self.refill_rate) * self.refill_interval
        else:
            reset_seconds = 0
            
        return is_allowed, remaining, math.ceil(reset_seconds)


class BaseRateLimitStorage(ABC):
    """
    Abstract base class for rate limit storage backends.
    
    This defines the interface that all storage backends must implement.
    """
    
    @abstractmethod
    async def get(self, key: str) -> Optional[float]:
        """
        Get a value from storage.
        
        Args:
            key: Storage key
            
        Returns:
            Optional[float]: Value if found, None otherwise
        """
        pass
    
    @abstractmethod
    async def set(self, key: str, value: float, expires: int) -> None:
        """
        Set a value in storage.
        
        Args:
            key: Storage key
            value: Value to store
            expires: Expiration time in seconds
        """
        pass
    
    @abstractmethod
    async def increment(self, key: str, amount: float, expires: int) -> float:
        """
        Increment a value in storage.
        
        Args:
            key: Storage key
            amount: Amount to increment by
            expires: Expiration time in seconds
            
        Returns:
            float: New value after increment
        """
        pass
    
    @abstractmethod
    async def delete(self, key: str) -> None:
        """
        Delete a value from storage.
        
        Args:
            key: Storage key
        """
        pass
    
    @abstractmethod
    async def clear(self, pattern: str = "*") -> None:
        """
        Clear all values matching pattern from storage.
        
        Args:
            pattern: Pattern to match keys
        """
        pass


class InMemoryStorage(BaseRateLimitStorage):
    """
    In-memory storage backend for rate limiting.
    
    This storage uses local memory and is suitable for single-server deployments.
    It is thread-safe and handles automatic cleanup of expired entries.
    """
    
    def __init__(self, cleanup_interval: int = 60):
        """
        Initialize in-memory storage.
        
        Args:
            cleanup_interval: Interval in seconds for cleanup of expired entries
        """
        self._data = {}  # Key -> (value, expiration timestamp)
        self._lock = threading.RLock()
        self._cleanup_interval = cleanup_interval
        
        # Start cleanup task
        self._start_cleanup()
    
    def _start_cleanup(self):
        """Start periodic cleanup task."""
        def cleanup():
            while True:
                time.sleep(self._cleanup_interval)
                self._cleanup_expired()
        
        cleanup_thread = threading.Thread(target=cleanup, daemon=True)
        cleanup_thread.start()
    
    def _cleanup_expired(self):
        """Remove expired entries from storage."""
        now = time.time()
        with self._lock:
            # Find expired keys
            expired_keys = []
            for key, (_, expires) in self._data.items():
                if expires < now:
                    expired_keys.append(key)
            
            # Remove expired keys
            for key in expired_keys:
                del self._data[key]
                
            # Log cleanup if keys were removed
            if expired_keys:
                logger.debug(f"Cleaned up {len(expired_keys)} expired rate limit entries")
    
    async def get(self, key: str) -> Optional[float]:
        """
        Get a value from storage.
        
        Args:
            key: Storage key
            
        Returns:
            Optional[float]: Value if found and not expired, None otherwise
        """
        with self._lock:
            if key in self._data:
                value, expires = self._data[key]
                if expires > time.time():
                    return value
                else:
                    # Expired, remove it
                    del self._data[key]
            return None
    
    async def set(self, key: str, value: float, expires: int) -> None:
        """
        Set a value in storage.
        
        Args:
            key: Storage key
            value: Value to store
            expires: Expiration time in seconds
        """
        expires_at = time.time() + expires
        with self._lock:
            self._data[key] = (value, expires_at)
    
    async def increment(self, key: str, amount: float, expires: int) -> float:
        """
        Increment a value in storage.
        
        Args:
            key: Storage key
            amount: Amount to increment by
            expires: Expiration time in seconds
            
        Returns:
            float: New value after increment
        """
        with self._lock:
            # Get current value
            current_value = 0
            if key in self._data:
                current_value, old_expires = self._data[key]
                if old_expires < time.time():
                    # Expired, reset to 0
                    current_value = 0
            
            # Increment value
            new_value = current_value + amount
            
            # Set with new expiration
            expires_at = time.time() + expires
            self._data[key] = (new_value, expires_at)
            
            return new_value
    
    async def delete(self, key: str) -> None:
        """
        Delete a value from storage.
        
        Args:
            key: Storage key
        """
        with self._lock:
            if key in self._data:
                del self._data[key]
    
    async def clear(self, pattern: str = "*") -> None:
        """
        Clear all values matching pattern from storage.
        
        Args:
            pattern: Pattern to match keys
        """
        import fnmatch
        with self._lock:
            # Find matching keys
            matching_keys = []
            for key in self._data.keys():
                if fnmatch.fnmatch(key, pattern):
                    matching_keys.append(key)
            
            # Remove matching keys
            for key in matching_keys:
                del self._data[key]
                
            # Log cleanup if keys were removed
            if matching_keys:
                logger.debug(f"Cleared {len(matching_keys)} rate limit entries matching '{pattern}'")


class RedisStorage(BaseRateLimitStorage):
    """
    Redis storage backend for rate limiting.
    
    This storage uses Redis and is suitable for distributed deployments.
    It handles automatic expiration of keys using Redis's built-in expiry.
    """
    
    def __init__(
        self,
        redis_url: str = "redis://localhost:6379/0",
        prefix: str = "rate_limit:",
        redis_client: Optional[Any] = None
    ):
        """
        Initialize Redis storage.
        
        Args:
            redis_url: Redis connection URL
            prefix: Key prefix for rate limit keys
            redis_client: Existing Redis client to use
        """
        if not REDIS_AVAILABLE:
            raise ImportError("Redis is not available. Please install redis-py.")
            
        self.prefix = prefix
        
        # Use provided client or create a new one
        if redis_client:
            self.redis = redis_client
        else:
            self.redis = redis.from_url(redis_url)
    
    def _prefixed_key(self, key: str) -> str:
        """Add prefix to key."""
        return f"{self.prefix}{key}"
    
    async def get(self, key: str) -> Optional[float]:
        """
        Get a value from storage.
        
        Args:
            key: Storage key
            
        Returns:
            Optional[float]: Value if found, None otherwise
        """
        prefixed_key = self._prefixed_key(key)
        value = self.redis.get(prefixed_key)
        if value is None:
            return None
        return float(value)
    
    async def set(self, key: str, value: float, expires: int) -> None:
        """
        Set a value in storage.
        
        Args:
            key: Storage key
            value: Value to store
            expires: Expiration time in seconds
        """
        prefixed_key = self._prefixed_key(key)
        self.redis.setex(prefixed_key, expires, value)
    
    async def increment(self, key: str, amount: float, expires: int) -> float:
        """
        Increment a value in storage.
        
        Args:
            key: Storage key
            amount: Amount to increment by
            expires: Expiration time in seconds
            
        Returns:
            float: New value after increment
        """
        prefixed_key = self._prefixed_key(key)
        
        # Use pipeline to make operations atomic
        pipe = self.redis.pipeline()
        pipe.incrbyfloat(prefixed_key, amount)
        pipe.expire(prefixed_key, expires)
        results = pipe.execute()
        
        return float(results[0])
    
    async def delete(self, key: str) -> None:
        """
        Delete a value from storage.
        
        Args:
            key: Storage key
        """
        prefixed_key = self._prefixed_key(key)
        self.redis.delete(prefixed_key)
    
    async def clear(self, pattern: str = "*") -> None:
        """
        Clear all values matching pattern from storage.
        
        Args:
            pattern: Pattern to match keys
        """
        prefixed_pattern = self._prefixed_key(pattern)
        keys = self.redis.keys(prefixed_pattern)
        
        if keys:
            self.redis.delete(*keys)
            logger.debug(f"Cleared {len(keys)} rate limit entries matching '{pattern}'")


class RateLimiter:
    """
    Main rate limiter class that applies rate limiting strategies to requests.
    
    This class handles checking if a request is allowed, updating counters,
    and generating appropriate response headers.
    """
    
    def __init__(
        self,
        strategy: Union[str, BaseRateLimitStrategy],
        max_requests: int = 100,
        window_seconds: int = 60,
        scope: str = RateLimitScope.IP,
        storage: Optional[BaseRateLimitStorage] = None,
        storage_args: Dict[str, Any] = None,
        enabled: bool = True,
        key_prefix: str = "",
        header_prefix: str = "X-RateLimit-",
        strict_mode: bool = True,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize rate limiter.
        
        Args:
            strategy: Rate limiting strategy to use
            max_requests: Maximum number of requests per window
            window_seconds: Time window in seconds
            scope: Scope for rate limiting (ip, client, user)
            storage: Storage backend to use
            storage_args: Arguments for storage backend
            enabled: Whether rate limiting is enabled
            key_prefix: Prefix for storage keys
            header_prefix: Prefix for HTTP headers
            strict_mode: Whether to strictly enforce limits
            logger: Logger to use
        """
        self.enabled = enabled
        self.key_prefix = key_prefix
        self.header_prefix = header_prefix
        self.strict_mode = strict_mode
        self.logger = logger or logging.getLogger("fastapi-keycloak.rate-limit")
        self.scope = scope if isinstance(scope, RateLimitScope) else RateLimitScope(scope)
        
        # Create strategy
        if isinstance(strategy, BaseRateLimitStrategy):
            self.strategy = strategy
        else:
            strategy_type = strategy if isinstance(strategy, RateLimitStrategy) else RateLimitStrategy(strategy)
            
            if strategy_type == RateLimitStrategy.FIXED_WINDOW:
                self.strategy = FixedWindowStrategy(max_requests, window_seconds)
            elif strategy_type == RateLimitStrategy.SLIDING_WINDOW:
                self.strategy = SlidingWindowStrategy(max_requests, window_seconds)
            elif strategy_type == RateLimitStrategy.TOKEN_BUCKET:
                # For token bucket, max_requests is the bucket size and window_seconds
                # is used to calculate the refill rate
                refill_rate = max_requests / window_seconds
                self.strategy = TokenBucketStrategy(max_requests, refill_rate)
            else:
                raise ValueError(f"Unknown rate limiting strategy: {strategy}")
                
        # Create storage
        storage_args = storage_args or {}
        if storage:
            self.storage = storage
        else:
            try:
                if REDIS_AVAILABLE and storage_args.get("use_redis", False):
                    redis_url = storage_args.get("redis_url", "redis://localhost:6379/0")
                    self.storage = RedisStorage(redis_url=redis_url, prefix=key_prefix)
                else:
                    self.storage = InMemoryStorage()
            except Exception as e:
                self.logger.warning(f"Failed to initialize redis storage: {e}. Falling back to in-memory storage.")
                self.storage = InMemoryStorage()
        
        self.logger.info(
            f"Rate limiter initialized: strategy={self.strategy.__class__.__name__}, "
            f"scope={self.scope.value}, enabled={self.enabled}, strict_mode={self.strict_mode}"
        )
    
    async def get_identifier(self, request: Request) -> str:
        """
        Extract identifier from request based on scope.
        
        Args:
            request: FastAPI request
            
        Returns:
            str: Identifier for rate limiting
        """
        if self.scope == RateLimitScope.IP:
            # Get client IP
            forwarded = request.headers.get("X-Forwarded-For")
            if forwarded:
                # Get the first IP in the chain
                return forwarded.split(",")[0].strip()
            else:
                return request.client.host if request.client else "unknown"
                
        elif self.scope == RateLimitScope.CLIENT:
            # Try to get client ID from various sources
            auth_header = request.headers.get("Authorization", "")
            if auth_header.startswith("Bearer "):
                # TODO: Extract client ID from token if possible
                return "client_" + auth_header[7:10]  # First few chars of token as proxy
                
            # Fall back to a cookie or query param if available
            client_id = (
                request.cookies.get("client_id") or
                request.query_params.get("client_id") or
                "unknown_client"
            )
            return f"client_{client_id}"
            
        elif self.scope == RateLimitScope.USER:
            # Try to extract user ID from token or session
            # TODO: Implement proper user ID extraction
            return "user_unknown"
            
        elif self.scope == RateLimitScope.COMBINED:
            # Combine IP and client for more precise limiting
            ip = await self.get_identifier(RateLimitScope.IP)
            client = await self.get_identifier(RateLimitScope.CLIENT)
            return f"{ip}:{client}"
            
        else:
            # Default to IP
            return request.client.host if request.client else "unknown"
    
    async def is_allowed(
        self,
        request: Request,
        increment: bool = True
    ) -> Tuple[bool, Dict[str, str]]:
        """
        Check if a request is allowed based on rate limits.
        
        Args:
            request: FastAPI request
            increment: Whether to increment the counter or just check
            
        Returns:
            Tuple[bool, Dict[str, str]]: (is_allowed, headers)
        """
        if not self.enabled:
            return True, {}
            
        try:
            # Get identifier based on scope
            identifier = await self.get_identifier(request)
            
            # Add endpoint path to make it endpoint-specific
            path_key = request.url.path.replace("/", "_")
            key = f"{self.key_prefix}{path_key}:{identifier}"
            
            # Check rate limit
            is_allowed, remaining, reset = await self.strategy.check_and_update(
                key, self.storage, increment
            )
            
            # Generate headers
            headers = self._get_headers(is_allowed, remaining, reset)
            
            # Record metrics if available
            if METRICS_AVAILABLE and not is_allowed:
                record_rate_limit_hit(
                    endpoint=request.url.path,
                    remaining=remaining,
                    reset_seconds=reset
                )
                
            # Log if limit exceeded
            if not is_allowed:
                self.logger.warning(
                    f"Rate limit exceeded for {self.scope.value}={identifier} "
                    f"on {request.url.path} (remaining={remaining}, reset={reset}s)"
                )
                
            return is_allowed, headers
            
        except Exception as e:
            self.logger.error(f"Error checking rate limit: {str(e)}")
            # In case of error, allow the request to proceed if not in strict mode
            return not self.strict_mode, {}
    
    def _get_headers(
        self,
        is_allowed: bool,
        remaining: int,
        reset: int
    ) -> Dict[str, str]:
        """
        Generate rate limit headers.
        
        Args:
            is_allowed: Whether request is allowed
            remaining: Remaining requests in window
            reset: Seconds until the limit resets
            
        Returns:
            Dict[str, str]: HTTP headers
        """
        # Calculate actual limit based on strategy type
        if isinstance(self.strategy, FixedWindowStrategy):
            limit = self.strategy.max_requests
        elif isinstance(self.strategy, SlidingWindowStrategy):
            limit = self.strategy.max_requests
        elif isinstance(self.strategy, TokenBucketStrategy):
            limit = self.strategy.max_tokens
        else:
            limit = 0
            
        headers = {
            f"{self.header_prefix}Limit": str(limit),
            f"{self.header_prefix}Remaining": str(remaining),
            f"{self.header_prefix}Reset": str(reset)
        }
        
        # Add retry-after header if limit is exceeded
        if not is_allowed:
            headers["Retry-After"] = str(reset)
            
        return headers
    
    async def reset(self, identifier: str = "*") -> None:
        """
        Reset rate limits for an identifier or pattern.
        
        Args:
            identifier: Identifier to reset, or pattern to match (default: all)
        """
        pattern = f"{self.key_prefix}{identifier}"
        await self.storage.clear(pattern)
        self.logger.info(f"Reset rate limits for pattern: {pattern}")
        
    def get_dependency(self) -> Callable:
        """
        Get a FastAPI dependency function for this rate limiter.
        
        Returns:
            Callable: FastAPI dependency function
        """
        async def rate_limit_dependency(request: Request):
            # Check rate limit
            is_allowed, headers = await self.is_allowed(request)
            
            # Add headers to response
            # This requires the response to be initialized before adding headers
            # so we'll use a background task to add them later
            async def add_headers(response: Response):
                for key, value in headers.items():
                    response.headers[key] = value
            
            request.state.add_rate_limit_headers = add_headers
            
            # Raise exception if not allowed
            if not is_allowed:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Rate limit exceeded",
                    headers=headers
                )
                
        return Depends(rate_limit_dependency)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    FastAPI middleware for rate limiting.
    
    This middleware applies rate limiting to all requests or specific endpoints.
    """
    
    def __init__(
        self,
        app: FastAPI,
        rate_limiter: RateLimiter,
        include_paths: List[str] = None,
        exclude_paths: List[str] = None
    ):
        """
        Initialize rate limit middleware.
        
        Args:
            app: FastAPI application
            rate_limiter: Rate limiter to use
            include_paths: List of paths to include (None for all)
            exclude_paths: List of paths to exclude
        """
        super().__init__(app)
        self.rate_limiter = rate_limiter
        self.include_paths = include_paths
        self.exclude_paths = exclude_paths or []
    
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint
    ) -> Response:
        """
        Process a request and apply rate limiting if needed.
        
        Args:
            request: FastAPI request
            call_next: Next middleware or route handler
            
        Returns:
            Response: FastAPI response
        """
        # Check if path should be rate limited
        path = request.url.path
        
        # Skip rate limiting if path is excluded or not included
        if path in self.exclude_paths:
            return await call_next(request)
            
        if self.include_paths is not None and path not in self.include_paths:
            return await call_next(request)
            
        # Check rate limit
        is_allowed, headers = await self.rate_limiter.is_allowed(request)
        
        # If not allowed, return 429 Too Many Requests
        if not is_allowed:
            return Response(
                content='{"detail": "Rate limit exceeded"}',
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                headers=headers,
                media_type="application/json"
            )
            
        # Call next middleware/endpoint
        response = await call_next(request)
        
        # Add rate limit headers to response
        for key, value in headers.items():
            response.headers[key] = value
            
        return response


# Factory function to create rate limiter
def create_rate_limiter(
    strategy: str = "sliding",
    max_requests: int = 100,
    window_seconds: int = 60,
    scope: str = "ip",
    enabled: bool = True,
    use_redis: bool = False,
    redis_url: str = "redis://localhost:6379/0",
    key_prefix: str = "keycloak_auth_rate_limit:",
    strict_mode: bool = True,
    logger: Optional[logging.Logger] = None
) -> RateLimiter:
    """
    Create a rate limiter with the specified configuration.
    
    Args:
        strategy: Rate limiting strategy to use
        max_requests: Maximum number of requests per window
        window_seconds: Time window in seconds
        scope: Scope for rate limiting (ip, client, user)
        enabled: Whether rate limiting is enabled
        use_redis: Whether to use Redis for storage
        redis_url: Redis connection URL
        key_prefix: Prefix for storage keys
        strict_mode: Whether to strictly enforce limits
        logger: Logger to use
        
    Returns:
        RateLimiter: Configured rate limiter
    """
    storage_args = {
        "use_redis": use_redis,
        "redis_url": redis_url
    }
    
    return RateLimiter(
        strategy=strategy,
        max_requests=max_requests,
        window_seconds=window_seconds,
        scope=scope,
        storage=None,
        storage_args=storage_args,
        enabled=enabled,
        key_prefix=key_prefix,
        strict_mode=strict_mode,
        logger=logger
    )
