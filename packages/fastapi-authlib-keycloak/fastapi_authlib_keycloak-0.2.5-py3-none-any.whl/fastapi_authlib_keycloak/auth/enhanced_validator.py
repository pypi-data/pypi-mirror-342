#!/usr/bin/env python3
"""
Enhanced JWT Token Validator for Keycloak Integration.

This module provides robust JWT token validation using Authlib and Keycloak,
with support for JWKS caching, rotation, introspection, and detailed error handling.
"""

import asyncio
import base64
import json
import logging
import os
import ssl
import time
import uuid
import warnings
from datetime import datetime
from enum import Enum
from functools import lru_cache
from typing import Dict, Optional, List, Any, Union, Tuple, Callable, Set

import httpx
from authlib.integrations.httpx_client import OAuth2Client
from authlib.jose import JsonWebToken, JsonWebKey
from authlib.jose.errors import JoseError, ExpiredTokenError, InvalidClaimError, MissingClaimError
from fastapi import HTTPException, status, Request

# Import the metrics module if it exists
try:
    from fastapi_authlib_keycloak.utils.metrics import record_token_validation, record_jwks_fetch
    METRICS_AVAILABLE = True
except ImportError:
    METRICS_AVAILABLE = False
    
    # Create stub functions for metrics
    def record_token_validation(*args, **kwargs):
        pass
        
    def record_jwks_fetch(*args, **kwargs):
        pass


class TokenValidationMethod(str, Enum):
    """Enumeration of token validation methods."""
    JWT = "jwt"
    INTROSPECTION = "introspection"
    BOTH = "both"


class KeyType(str, Enum):
    """Enumeration of key types in JWKS."""
    RSA = "RSA"
    EC = "EC"
    OCT = "oct"


class ValidationError(Exception):
    """Base class for token validation errors."""
    def __init__(self, message: str, status_code: int = status.HTTP_401_UNAUTHORIZED):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class JWKSCache:
    """
    Cache for JSON Web Key Sets with automatic rotation handling.
    
    This class provides thread-safe caching of JWKS with support for:
    - Time-based expiration
    - Key rotation detection
    - Automatic refresh on key ID mismatch
    - Multiple backup keys
    """
    
    def __init__(
        self,
        ttl: int = 3600,
        max_keys: int = 10,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize the JWKS cache.
        
        Args:
            ttl: Cache time-to-live in seconds
            max_keys: Maximum number of keys to store
            logger: Logger instance
        """
        self.ttl = ttl
        self.max_keys = max_keys
        self.logger = logger or logging.getLogger("fastapi-keycloak.jwks_cache")
        self._cache = {}
        self._last_fetched = 0
        self._cached_key_ids = set()
        self._lock = asyncio.Lock()
        
    async def get(self, force_refresh: bool = False) -> Optional[Dict]:
        """
        Get the cached JWKS or None if not available or expired.
        
        Args:
            force_refresh: Force a refresh regardless of TTL
            
        Returns:
            Optional[Dict]: The cached JWKS or None
        """
        current_time = time.time()
        
        async with self._lock:
            # Check if cache is valid
            if not force_refresh and self._cache and (current_time - self._last_fetched) < self.ttl:
                self.logger.debug(f"Using cached JWKS (age: {current_time - self._last_fetched:.1f}s)")
                return self._cache
                
            # Cache is invalid or forced refresh
            return None
            
    async def update(self, jwks: Dict) -> None:
        """
        Update the cache with a new JWKS.
        
        This method also handles key rotation by identifying new keys
        and removing old ones that exceed the maximum count.
        
        Args:
            jwks: The new JWKS to cache
        """
        if not jwks or "keys" not in jwks:
            self.logger.warning("Attempted to cache invalid JWKS: missing 'keys' property")
            return
            
        async with self._lock:
            # Update the cache
            self._cache = jwks
            self._last_fetched = time.time()
            
            # Track key IDs for rotation detection
            old_key_ids = self._cached_key_ids.copy()
            new_key_ids = {key.get("kid") for key in jwks.get("keys", []) if key.get("kid")}
            
            # Check for key rotation
            if old_key_ids and new_key_ids:
                added_keys = new_key_ids - old_key_ids
                removed_keys = old_key_ids - new_key_ids
                
                if added_keys:
                    self.logger.info(f"Key rotation detected: {len(added_keys)} new keys added")
                    
                if removed_keys:
                    self.logger.info(f"Key rotation detected: {len(removed_keys)} keys removed")
            
            # Store current key IDs
            self._cached_key_ids = new_key_ids
            
    def contains_key_id(self, kid: str) -> bool:
        """
        Check if the cache contains a specific key ID.
        
        Args:
            kid: Key ID to check
            
        Returns:
            bool: True if the key ID exists in the cache
        """
        if not self._cache or "keys" not in self._cache:
            return False
            
        return any(key.get("kid") == kid for key in self._cache.get("keys", []))
        
    async def invalidate(self) -> None:
        """Invalidate the cache, forcing the next get() to fetch fresh data."""
        async with self._lock:
            self._last_fetched = 0
            
    def is_valid(self) -> bool:
        """
        Check if the cache is valid.
        
        Returns:
            bool: True if the cache is valid and not expired
        """
        return (
            bool(self._cache) and
            "keys" in self._cache and
            (time.time() - self._last_fetched) < self.ttl
        )
        
    @property
    def age(self) -> float:
        """
        Get the age of the cached data in seconds.
        
        Returns:
            float: Age in seconds, or -1 if not cached
        """
        if not self._last_fetched:
            return -1
            
        return time.time() - self._last_fetched


class TokenIntrospector:
    """
    Client for Keycloak token introspection endpoint.
    
    This class provides a way to validate tokens by introspecting them
    with the Keycloak server, which is useful when JWT validation is not
    sufficient or when more detailed token information is needed.
    """
    
    def __init__(
        self,
        introspection_url: str,
        client_id: str,
        client_secret: str,
        ssl_verify: Union[bool, str] = True,
        cache_ttl: int = 300,  # Short cache TTL for introspection
        max_cache_size: int = 1000,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize the token introspector.
        
        Args:
            introspection_url: URL of the Keycloak introspection endpoint
            client_id: Client ID for authentication
            client_secret: Client secret for authentication
            ssl_verify: SSL verification mode
            cache_ttl: Cache time-to-live in seconds
            max_cache_size: Maximum number of results to cache
            logger: Logger instance
        """
        self.introspection_url = introspection_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.ssl_verify = ssl_verify
        self.cache_ttl = cache_ttl
        self.logger = logger or logging.getLogger("fastapi-keycloak.introspector")
        
        # Initialize cache with LRU policy
        self._create_cache(max_cache_size)
        
    def _create_cache(self, max_size: int) -> None:
        """
        Create an LRU cache for introspection results.
        
        Args:
            max_size: Maximum number of results to cache
        """
        @lru_cache(maxsize=max_size)
        def _introspection_cache(token: str, timestamp_bucket: int) -> Tuple[Dict, float]:
            """Inner function that will be cached with the actual results."""
            # This function is never actually called directly,
            # but serves as the cached function for introspection results
            return {}, 0
            
        self._cache_fn = _introspection_cache
        self._cache_data = {}  # Stores actual results by token
        
    def _get_time_bucket(self) -> int:
        """
        Get the current time bucket for cache expiration.
        
        Time is divided into buckets of size cache_ttl to allow
        automatic expiration of cached results.
        
        Returns:
            int: Current time bucket
        """
        return int(time.time() / self.cache_ttl)
        
    def _get_cached_result(self, token: str) -> Optional[Dict]:
        """
        Get a cached introspection result if available and not expired.
        
        Args:
            token: Token to lookup
            
        Returns:
            Optional[Dict]: Cached result or None
        """
        # Get the current time bucket
        current_bucket = self._get_time_bucket()
        
        # Check if we have a cache hit
        cache_key = (token, current_bucket)
        if token in self._cache_data:
            result, timestamp = self._cache_data[token]
            if time.time() - timestamp < self.cache_ttl:
                # Touch the cache to update LRU order
                self._cache_fn(*cache_key)
                return result
                
            # Result is too old, remove it
            del self._cache_data[token]
            
        return None
        
    def _store_cache_result(self, token: str, result: Dict) -> None:
        """
        Store an introspection result in the cache.
        
        Args:
            token: Token used for introspection
            result: Introspection result
        """
        current_bucket = self._get_time_bucket()
        
        # Touch the cache to get LRU tracking
        self._cache_fn(token, current_bucket)
        
        # Store the actual result and timestamp
        self._cache_data[token] = (result, time.time())
        
    async def introspect(self, token: str, force_refresh: bool = False) -> Dict:
        """
        Introspect a token to validate it with Keycloak.
        
        Args:
            token: Token to introspect (access_token or refresh_token)
            force_refresh: Force a fresh introspection regardless of cache
            
        Returns:
            Dict: Introspection result with token information
            
        Raises:
            HTTPException: If introspection fails or token is invalid
        """
        # Remove Bearer prefix if present
        if token.startswith("Bearer "):
            token = token[7:]
            
        # Check cache first (unless forced refresh)
        if not force_refresh:
            cached_result = self._get_cached_result(token)
            if cached_result is not None:
                if cached_result.get("active", False):
                    self.logger.debug("Using cached introspection result")
                    return cached_result
                else:
                    # If cached result shows token is inactive, fail immediately
                    self.logger.warning("Cached introspection shows token is inactive")
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Token is not active"
                    )
        
        # Prepare request parameters
        data = {
            "token": token,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        
        try:
            # Make introspection request
            start_time = time.time()
            async with httpx.AsyncClient(verify=self.ssl_verify) as client:
                response = await client.post(self.introspection_url, data=data)
                response_time = time.time() - start_time
                
                # Log performance metrics
                self.logger.debug(f"Introspection request completed in {response_time:.3f}s")
                if METRICS_AVAILABLE:
                    record_token_validation(
                        method="introspection",
                        success=response.status_code == 200,
                        duration_seconds=response_time
                    )
                
                # Handle errors
                if response.status_code != 200:
                    self.logger.error(f"Introspection failed with status {response.status_code}: {response.text}")
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=f"Token introspection failed: {response.text}"
                    )
                    
                # Parse result
                result = response.json()
                
                # Verify activation status
                if not result.get("active", False):
                    self.logger.warning("Token is not active according to introspection")
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Token is not active"
                    )
                
                # Cache result for future use
                self._store_cache_result(token, result)
                return result
                
        except httpx.RequestError as e:
            self.logger.error(f"Error during introspection request: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Could not connect to introspection endpoint: {str(e)}"
            )


class EnhancedJWTValidator:
    """
    Enhanced validator for Keycloak JWT tokens with advanced features.
    
    This class provides robust JWT token validation with:
    - JWKS caching and automatic rotation
    - Token introspection support
    - Detailed error messages
    - Performance metrics
    - Connection pooling
    - Offline validation support
    """

    def __init__(
        self,
        issuer: str,
        jwks_uri: str,
        client_id: str,
        client_secret: str,
        introspection_uri: Optional[str] = None,
        api_client_id: Optional[str] = None,
        api_client_secret: Optional[str] = None,
        validation_method: TokenValidationMethod = TokenValidationMethod.JWT,
        strict_client_check: bool = False,
        ssl_verify: Union[bool, str] = True,
        ssl_cert_file: Optional[str] = None,
        jwks_cache_ttl: int = 3600,
        jwks_file: Optional[str] = None,
        on_ssl_error: str = "raise",
        development_mode: bool = False,
        http_timeout: float = 10.0,
        max_retries: int = 3,
        introspection_cache_ttl: int = 300,
        max_jwks_keys: int = 10,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize the validator with enhanced parameters.

        Args:
            issuer: The issuer URL (usually the Keycloak server URL)
            jwks_uri: The URL to the JWK Set
            client_id: The primary client ID to verify in the token
            client_secret: Client secret for token introspection
            introspection_uri: URL for token introspection endpoint
            api_client_id: Secondary client ID that is also acceptable
            api_client_secret: Secondary client secret for API client
            validation_method: Method for token validation (jwt, introspection, or both)
            strict_client_check: Whether to strictly enforce client ID matching
            ssl_verify: SSL verification mode
            ssl_cert_file: Path to SSL certificate file
            jwks_cache_ttl: Cache time for JWKS in seconds
            jwks_file: Path to a local JWKS file for offline validation
            on_ssl_error: How to handle SSL errors
            development_mode: Whether development mode is enabled
            http_timeout: Timeout for HTTP requests in seconds
            max_retries: Maximum number of retry attempts
            introspection_cache_ttl: Cache time for introspection results
            max_jwks_keys: Maximum number of keys to store in JWKS cache
            logger: Logger instance
        """
        # Basic configuration
        self.issuer = issuer
        self.jwks_uri = jwks_uri
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_client_id = api_client_id
        self.api_client_secret = api_client_secret or client_secret
        
        # Validation settings
        self.validation_method = validation_method
        self.strict_client_check = strict_client_check
        
        # SSL settings
        self.ssl_verify = ssl_verify
        self.ssl_cert_file = ssl_cert_file
        self.on_ssl_error = on_ssl_error
        
        # Development settings
        self.development_mode = development_mode
        
        # HTTP settings
        self.http_timeout = http_timeout
        self.max_retries = max_retries
        
        # Cache settings
        self.jwks_cache_ttl = jwks_cache_ttl
        self.jwks_file = jwks_file
        self.max_jwks_keys = max_jwks_keys
        
        # Logging
        self.logger = logger or logging.getLogger("fastapi-keycloak.validator")
        
        # Initialize JWKS cache
        self.jwks_cache = JWKSCache(
            ttl=jwks_cache_ttl,
            max_keys=max_jwks_keys,
            logger=self.logger
        )
        
        # Initialize introspector if needed
        self.introspector = None
        if validation_method in (TokenValidationMethod.INTROSPECTION, TokenValidationMethod.BOTH):
            if not introspection_uri:
                # Construct introspection URI from issuer if not provided
                introspection_uri = f"{issuer}/protocol/openid-connect/token/introspect"
                
            self.introspector = TokenIntrospector(
                introspection_url=introspection_uri,
                client_id=client_id,
                client_secret=self.client_secret,
                ssl_verify=ssl_verify,
                cache_ttl=introspection_cache_ttl,
                logger=self.logger
            )
        
        # Initialize HTTP client limit pool (to be created on demand)
        self._http_client = None
        
        # In development mode, try to load local JWKS file if provided
        if self.development_mode and self.jwks_file:
            asyncio.create_task(self._try_load_local_jwks())
        
        # If development mode is enabled with insecure settings, log a warning
        if self.development_mode:
            if self.ssl_verify is False:
                self.logger.warning(
                    "Development mode: SSL verification is DISABLED. "
                    "This is insecure and should only be used in development environments."
                )
                
            if isinstance(self.ssl_verify, str) and "localhost" in issuer:
                self.logger.warning(
                    "Development mode: Using custom SSL certificate with localhost. "
                    "This may cause issues if the certificate doesn't match."
                )
                
            if "http://" in issuer:
                self.logger.warning(
                    "Development mode: Using HTTP for Keycloak connection. "
                    "This is insecure and should only be used in development environments."
                )

    async def _get_http_client(self) -> httpx.AsyncClient:
        """
        Get or create a shared HTTP client with connection pooling.
        
        Returns:
            httpx.AsyncClient: Configured HTTP client
        """
        if self._http_client is None or self._http_client.is_closed:
            # Configure limits for connection pooling
            limits = httpx.Limits(
                max_keepalive_connections=10,
                max_connections=20,
                keepalive_expiry=30.0
            )
            
            # Configure timeout
            timeout = httpx.Timeout(timeout=self.http_timeout)
            
            # Configure SSL verification
            verify = self.ssl_verify
            if isinstance(verify, str) and os.path.isfile(verify):
                # Use specific certificate file
                pass
            elif verify is False:
                # Disable verification (insecure)
                warnings.warn(
                    "SSL verification is disabled. This is insecure and should "
                    "only be used in development environments."
                )
            elif self.ssl_cert_file and os.path.isfile(self.ssl_cert_file):
                # Use configured certificate file
                verify = self.ssl_cert_file
                
            # Create client with connection pooling
            self._http_client = httpx.AsyncClient(
                verify=verify,
                timeout=timeout,
                limits=limits,
                follow_redirects=True
            )
            
        return self._http_client

    async def _try_load_local_jwks(self) -> bool:
        """
        Try to load JWKS from a local file for offline validation.
        
        Returns:
            bool: True if successfully loaded, False otherwise
        """
        try:
            if not self.jwks_file or not os.path.isfile(self.jwks_file):
                self.logger.warning(f"JWKS file not found: {self.jwks_file}")
                return False
                
            with open(self.jwks_file, 'r') as f:
                jwks_data = json.load(f)
                
            if not jwks_data or "keys" not in jwks_data:
                self.logger.warning(f"Invalid JWKS file format: {self.jwks_file}")
                return False
                
            # Update the cache with the loaded data
            await self.jwks_cache.update(jwks_data)
            self.logger.info(f"Successfully loaded JWKS from local file: {self.jwks_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading local JWKS file: {str(e)}")
            return False

    async def fetch_jwks(self, force_refresh: bool = False) -> Dict:
        """
        Fetch the JWK Set from the JWKS URI with caching and error handling.
        
        Args:
            force_refresh: Force a refresh regardless of cache state
            
        Returns:
            Dict: The JWKS as a dictionary
            
        Raises:
            HTTPException: If the JWKS cannot be fetched
        """
        # Check cache first (unless forced refresh)
        if not force_refresh:
            cached_jwks = await self.jwks_cache.get()
            if cached_jwks:
                return cached_jwks
                
        # Cache miss or forced refresh - fetch from server
        try:
            start_time = time.time()
            client = await self._get_http_client()
            
            # Attempt to fetch JWKS
            self.logger.info(f"Fetching JWKS from {self.jwks_uri}")
            response = await client.get(self.jwks_uri)
            response_time = time.time() - start_time
            
            # Record metrics
            if METRICS_AVAILABLE:
                record_jwks_fetch(
                    success=response.status_code == 200,
                    duration_seconds=response_time
                )
                
            # Handle HTTP errors
            response.raise_for_status()
            
            # Parse JWKS data
            jwks_data = response.json()
            
            # Validate JWKS format
            if "keys" not in jwks_data or not jwks_data["keys"]:
                self.logger.warning(f"Invalid JWKS format: missing or empty 'keys' property")
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Invalid JWKS format from server"
                )
                
            # Update cache
            await self.jwks_cache.update(jwks_data)
            self.logger.info(f"JWKS successfully fetched in {response_time:.3f}s")
            
            # Save to file in development mode if configured
            if self.development_mode and self.jwks_file:
                try:
                    with open(self.jwks_file, 'w') as f:
                        json.dump(jwks_data, f, indent=2)
                    self.logger.info(f"Saved JWKS to local file: {self.jwks_file}")
                except Exception as save_error:
                    self.logger.warning(f"Failed to save JWKS to file: {str(save_error)}")
            
            return jwks_data
            
        except httpx.HTTPStatusError as e:
            self.logger.error(f"HTTP error fetching JWKS: {e.response.status_code} - {e.response.text}")
            
            # Try local file in development mode
            if self.development_mode and self.jwks_file:
                self.logger.info(f"Attempting to load JWKS from local file after HTTP error")
                if await self._try_load_local_jwks():
                    return await self.jwks_cache.get() or {}
                    
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Could not fetch JWKS: HTTP {e.response.status_code}"
            )
            
        except httpx.RequestError as e:
            self.logger.error(f"Request error fetching JWKS: {str(e)}")
            
            # Handle SSL errors according to configuration
            if "SSL" in str(e) or "certificate" in str(e).lower():
                if self.on_ssl_error == "warn":
                    self.logger.warning(
                        f"SSL error when fetching JWKS: {str(e)}. "
                        f"Consider enabling development_mode if this is a development environment."
                    )
                    
                    # Try local file in development mode
                    if self.development_mode and self.jwks_file:
                        if await self._try_load_local_jwks():
                            return await self.jwks_cache.get() or {}
                            
                elif self.on_ssl_error == "ignore":
                    self.logger.info(f"Ignoring SSL error: {str(e)}")
                    return {}
                    
            # Try local file in development mode
            if self.development_mode and self.jwks_file:
                self.logger.info(f"Attempting to load JWKS from local file after request error")
                if await self._try_load_local_jwks():
                    return await self.jwks_cache.get() or {}
                    
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Could not fetch JWKS: {str(e)}"
            )
            
        except Exception as e:
            self.logger.error(f"Unexpected error fetching JWKS: {str(e)}")
            
            # Try local file in development mode
            if self.development_mode and self.jwks_file:
                self.logger.info(f"Attempting to load JWKS from local file after unexpected error")
                if await self._try_load_local_jwks():
                    return await self.jwks_cache.get() or {}
                    
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Could not fetch JWKS: {str(e)}"
            )

    async def extract_token_from_request(self, request: Request) -> str:
        """
        Extract an OAuth token from the request.
        
        This method supports multiple token extraction methods:
        - Authorization header (Bearer token)
        - Cookie-based tokens
        - Query parameter tokens
        
        Args:
            request: FastAPI Request object
            
        Returns:
            str: Extracted token
            
        Raises:
            HTTPException: If no token is found or it's invalid
        """
        # Try Authorization header first (preferred method)
        authorization = request.headers.get("Authorization")
        if authorization:
            scheme, _, token = authorization.partition(" ")
            if scheme.lower() == "bearer" and token:
                return token
                
        # Try cookie-based token
        token_cookie = request.cookies.get("auth_token")
        if token_cookie:
            return token_cookie
            
        # Try query parameter as a last resort (less secure)
        token_param = request.query_params.get("access_token")
        if token_param:
            self.logger.warning("Token extracted from query parameter - this is less secure")
            return token_param
            
        # No token found
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No authentication token found",
            headers={"WWW-Authenticate": "Bearer"}
        )

    async def validate_token_jwt(self, token: str, force_jwks_refresh: bool = False) -> Dict:
        """
        Validate a JWT token using JWKS.
        
        Args:
            token: The JWT token to validate
            force_jwks_refresh: Force a refresh of JWKS cache
            
        Returns:
            Dict: The decoded token claims if valid
            
        Raises:
            HTTPException: If token validation fails
        """
        start_time = time.time()
        success = False
        error_msg = None
        
        try:
            # Ensure token format - remove Bearer prefix if present
            if token.startswith("Bearer "):
                token = token[7:]
                
            # Extract token header to get key ID (kid)
            try:
                # Split token and decode header
                parts = token.split('.')
                if len(parts) != 3:
                    raise ValueError("Invalid JWT format: token must have three parts")
                    
                # Decode header
                header_data = parts[0]
                # Fix padding for base64url decode
                header_data += '=' * (4 - len(header_data) % 4)
                decoded_header = base64.urlsafe_b64decode(header_data)
                header = json.loads(decoded_header)
                
                # Get key ID
                kid = header.get("kid")
                if not kid:
                    self.logger.warning("JWT header missing 'kid' (key ID)")
                    
            except Exception as e:
                self.logger.error(f"Error decoding JWT header: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"Invalid token format: {str(e)}"
                )
                
            # Fetch JWKS if needed
            jwks = await self.fetch_jwks(force_refresh=force_jwks_refresh)
            
            # If we have a key ID but it's not in our JWKS, it might be a key rotation
            # Forcefully refresh the JWKS cache and try again
            if kid and not self.jwks_cache.contains_key_id(kid) and not force_jwks_refresh:
                self.logger.info(f"Key ID {kid} not found in JWKS, refreshing cache")
                jwks = await self.fetch_jwks(force_refresh=True)
                
                # If still not found, this is likely an invalid token
                if not self.jwks_cache.contains_key_id(kid):
                    self.logger.warning(f"Key ID {kid} not found in refreshed JWKS")
                
            # Create JsonWebKey instance from JWKS
            json_web_key = JsonWebKey.import_key_set(jwks)
            
            # Setup the JWT instance
            jwt = JsonWebToken(['RS256'])
            
            # Decode and validate the token
            claims = jwt.decode(
                token,
                json_web_key,
                claims_options={
                    'iss': {'essential': True, 'value': self.issuer},
                    'exp': {'essential': True},
                    # Allow any audience (Keycloak might use the realm as audience)
                    'aud': {'essential': False}
                }
            )
            
            # Perform additional verifications
            claims.validate()
            
            # Extract AZP (authorized party) from token - this is usually the client ID
            token_client_id = claims.get('azp')
            # Fallback to 'client_id' claim if 'azp' is not present
            if not token_client_id:
                token_client_id = claims.get('client_id')
            
            # Check client ID only if strict checking is enabled and a client ID exists in the token
            if self.strict_client_check and token_client_id:
                # Allow either the primary client ID or the API client ID
                valid_client_ids = [self.client_id]
                if self.api_client_id:
                    valid_client_ids.append(self.api_client_id)
                
                if token_client_id not in valid_client_ids:
                    self.logger.warning(
                        f"Client ID mismatch: Token has '{token_client_id}' but "
                        f"validator expects one of {valid_client_ids}"
                    )
                    
                    if self.development_mode:
                        # Be more lenient in development mode
                        self.logger.info(
                            "Development mode: Allowing token with mismatched client ID"
                        )
                    else:
                        # In production, enforce strict client ID checking
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Client ID mismatch: Token has '{token_client_id}' but validator expects one of {valid_client_ids}"
                        )
            
            success = True
            duration = time.time() - start_time
            self.logger.info(
                f"Token successfully validated for user: {claims.get('preferred_username')} "
                f"(took {duration:.3f}s)"
            )
            
            if METRICS_AVAILABLE:
                record_token_validation(
                    method="jwt",
                    success=True,
                    duration_seconds=duration
                )
                
            return claims
            
        except (JoseError, ValueError) as e:
            success = False
            error_msg = str(e)
            
            # Provide a more specific error message for common issues
            if isinstance(e, ExpiredTokenError):
                error_msg = "Token has expired"
            elif isinstance(e, InvalidClaimError):
                if "iss" in str(e):
                    error_msg = f"Invalid issuer in token. Expected: {self.issuer}"
                else:
                    error_msg = f"Invalid claim in token: {str(e)}"
            elif isinstance(e, MissingClaimError):
                error_msg = f"Missing required claim in token: {str(e)}"
                
            self.logger.error(f"Token validation error: {error_msg}")
            
            # Record metrics for failed validation
            duration = time.time() - start_time
            if METRICS_AVAILABLE:
                record_token_validation(
                    method="jwt",
                    success=False,
                    duration_seconds=duration,
                    error=error_msg
                )
                
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token validation failed: {error_msg}"
            )
            
        except Exception as e:
            success = False
            error_msg = str(e)
            self.logger.error(f"Unexpected error during token validation: {error_msg}")
            
            # Record metrics for failed validation
            duration = time.time() - start_time
            if METRICS_AVAILABLE:
                record_token_validation(
                    method="jwt",
                    success=False,
                    duration_seconds=duration,
                    error=error_msg
                )
                
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token validation failed: {error_msg}"
            )

    async def validate_token(self, token: str) -> Dict:
        """
        Validate a token using the configured validation method.
        
        This method orchestrates the validation process based on the
        chosen validation method (JWT, introspection, or both).
        
        Args:
            token: The token to validate
            
        Returns:
            Dict: The decoded token claims if valid
            
        Raises:
            HTTPException: If token validation fails
        """
        # Remove Bearer prefix if present
        if token.startswith("Bearer "):
            token = token[7:]
            
        # Choose validation method
        if self.validation_method == TokenValidationMethod.JWT:
            # Use JWT validation only
            return await self.validate_token_jwt(token)
            
        elif self.validation_method == TokenValidationMethod.INTROSPECTION:
            # Use introspection only
            if not self.introspector:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Token introspection requested but introspector not configured"
                )
                
            return await self.introspector.introspect(token)
            
        elif self.validation_method == TokenValidationMethod.BOTH:
            # Use both methods
            if not self.introspector:
                self.logger.warning(
                    "Both validation methods requested but introspector not configured. "
                    "Falling back to JWT validation only."
                )
                return await self.validate_token_jwt(token)
                
            # Try JWT validation first (faster and doesn't require backend call)
            try:
                jwt_result = await self.validate_token_jwt(token)
                
                # If JWT validation succeeded, also check with introspection
                try:
                    introspection_result = await self.introspector.introspect(token)
                    
                    # Combine results (introspection result takes precedence)
                    combined_result = {**jwt_result, **introspection_result}
                    return combined_result
                    
                except Exception as e:
                    # If introspection fails but JWT validation succeeded,
                    # log a warning and return the JWT result
                    self.logger.warning(
                        f"Token passed JWT validation but introspection failed: {str(e)}. "
                        f"Using JWT validation result."
                    )
                    return jwt_result
                    
            except Exception as jwt_error:
                # If JWT validation fails, try introspection
                self.logger.warning(
                    f"JWT validation failed: {str(jwt_error)}. "
                    f"Falling back to introspection."
                )
                
                try:
                    return await self.introspector.introspect(token)
                except Exception as introspect_error:
                    # If both methods fail, raise the JWT error (usually more informative)
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=f"Token validation failed: {str(jwt_error)}"
                    )
                    
        # This should never happen due to enum constraints
        raise ValueError(f"Invalid validation method: {self.validation_method}")

    async def close(self):
        """
        Close the validator and free resources.
        
        This method should be called when the validator is no longer needed
        to ensure proper cleanup of resources like HTTP connections.
        """
        if self._http_client is not None and not self._http_client.is_closed:
            await self._http_client.aclose()
            self._http_client = None
            
    async def health_check(self) -> Dict:
        """
        Check the health of the validator and its connections.
        
        This method performs checks on the validator's components:
        - JWKS endpoint connectivity
        - Introspection endpoint connectivity (if configured)
        - Cache status
        
        Returns:
            Dict: Health check status information
            
        Raises:
            HTTPException: If health check fails
        """
        result = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "components": {}
        }
        
        # Check JWKS connectivity
        jwks_status = "healthy"
        jwks_message = None
        
        try:
            start_time = time.time()
            jwks = await self.fetch_jwks(force_refresh=True)
            jwks_request_time = time.time() - start_time
            
            if "keys" not in jwks or not jwks["keys"]:
                jwks_status = "degraded"
                jwks_message = "JWKS endpoint returned empty keys array"
            else:
                jwks_message = f"JWKS fetch succeeded in {jwks_request_time:.3f}s with {len(jwks['keys'])} keys"
                
        except Exception as e:
            jwks_status = "unhealthy"
            jwks_message = f"JWKS fetch failed: {str(e)}"
            
            # Check for local JWKS file as backup
            if self.development_mode and self.jwks_file and os.path.isfile(self.jwks_file):
                jwks_status = "degraded"
                jwks_message += f" (using local file: {self.jwks_file})"
                
        result["components"]["jwks"] = {
            "status": jwks_status,
            "message": jwks_message,
            "cache_age": self.jwks_cache.age
        }
        
        # Check introspection if configured
        if self.introspector:
            introspection_status = "healthy"
            introspection_message = None
            
            try:
                # We can't actually test introspection without a valid token,
                # so we just check if the endpoint is reachable
                start_time = time.time()
                client = await self._get_http_client()
                response = await client.head(
                    self.introspector.introspection_url,
                    timeout=5.0
                )
                request_time = time.time() - start_time
                
                if response.status_code in (200, 204, 401, 403):
                    # These status codes indicate the endpoint exists
                    introspection_message = f"Introspection endpoint is reachable ({request_time:.3f}s)"
                else:
                    introspection_status = "degraded"
                    introspection_message = f"Unexpected status from introspection endpoint: {response.status_code}"
                    
            except Exception as e:
                introspection_status = "unhealthy"
                introspection_message = f"Introspection endpoint is unreachable: {str(e)}"
                
            result["components"]["introspection"] = {
                "status": introspection_status,
                "message": introspection_message
            }
            
        # Determine overall status
        component_statuses = [comp["status"] for comp in result["components"].values()]
        if "unhealthy" in component_statuses:
            result["status"] = "unhealthy"
        elif "degraded" in component_statuses:
            result["status"] = "degraded"
            
        return result


def create_enhanced_validator(
    keycloak_url: str,
    keycloak_realm: str,
    client_id: str,
    client_secret: str,
    api_client_id: Optional[str] = None,
    api_client_secret: Optional[str] = None,
    validation_method: Union[str, TokenValidationMethod] = TokenValidationMethod.JWT,
    strict_client_check: bool = False,
    ssl_verify: Union[bool, str] = True,
    ssl_cert_file: Optional[str] = None,
    jwks_cache_ttl: int = 3600,
    jwks_file: Optional[str] = None,
    on_ssl_error: str = "raise",
    development_mode: bool = False,
    http_timeout: float = 10.0,
    max_retries: int = 3,
    introspection_cache_ttl: int = 300,
    max_jwks_keys: int = 10,
    logger: Optional[logging.Logger] = None
) -> EnhancedJWTValidator:
    """
    Create an enhanced Keycloak JWT validator.
    
    This factory function creates a fully configured EnhancedJWTValidator
    instance with all the necessary settings.
    
    Args:
        keycloak_url: URL of the Keycloak server
        keycloak_realm: Keycloak realm name
        client_id: Client ID for authentication
        client_secret: Client secret for authentication 
        api_client_id: API client ID (if different from client_id)
        api_client_secret: API client secret (if different from client_secret)
        validation_method: Method for token validation
        strict_client_check: Whether to strictly enforce client ID matching
        ssl_verify: SSL verification mode
        ssl_cert_file: Path to SSL certificate file
        jwks_cache_ttl: Cache time for JWKS in seconds
        jwks_file: Path to a local JWKS file for offline validation
        on_ssl_error: How to handle SSL errors
        development_mode: Whether development mode is enabled
        http_timeout: Timeout for HTTP requests in seconds
        max_retries: Maximum number of retry attempts
        introspection_cache_ttl: Cache time for introspection results
        max_jwks_keys: Maximum number of keys to store in JWKS cache
        logger: Logger instance
        
    Returns:
        EnhancedJWTValidator: Configured validator instance
    """
    # Initialize logger if not provided
    logger = logger or logging.getLogger("fastapi-keycloak.validator")
    
    # Normalize validation method
    if isinstance(validation_method, str):
        validation_method = TokenValidationMethod(validation_method.lower())
        
    # Construct issuer URL
    issuer = f"{keycloak_url}/realms/{keycloak_realm}"
    
    # Construct JWKS URI
    jwks_uri = f"{keycloak_url}/realms/{keycloak_realm}/protocol/openid-connect/certs"
    
    # Construct introspection URI
    introspection_uri = f"{keycloak_url}/realms/{keycloak_realm}/protocol/openid-connect/token/introspect"
    
    # Create the validator
    validator = EnhancedJWTValidator(
        issuer=issuer,
        jwks_uri=jwks_uri,
        client_id=client_id,
        client_secret=client_secret,
        introspection_uri=introspection_uri,
        api_client_id=api_client_id,
        api_client_secret=api_client_secret,
        validation_method=validation_method,
        strict_client_check=strict_client_check,
        ssl_verify=ssl_verify,
        ssl_cert_file=ssl_cert_file,
        jwks_cache_ttl=jwks_cache_ttl,
        jwks_file=jwks_file,
        on_ssl_error=on_ssl_error,
        development_mode=development_mode,
        http_timeout=http_timeout,
        max_retries=max_retries,
        introspection_cache_ttl=introspection_cache_ttl,
        max_jwks_keys=max_jwks_keys,
        logger=logger
    )
    
    return validator
