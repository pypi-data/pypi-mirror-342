#!/usr/bin/env python3
"""
Utilities module for FastAPI-Authlib-Keycloak.

This module provides utility functions used throughout the package, including:
- SSL utilities for certificate handling
- Metrics collection for monitoring
- Debugging tools for development
- Rate limiting for API protection
"""

# Version
__version__ = "0.2.0"

# Base SSL utilities
from fastapi_authlib_keycloak.utils.ssl_utils import setup_ssl

# Import optional utilities based on availability
try:
    from fastapi_authlib_keycloak.utils.metrics import (
        configure_metrics,
        MetricsBackend,
        MetricsMiddleware,
        create_fastapi_metrics_endpoint,
        get_metrics_status,
        MetricsTimer,
        AsyncMetricsTimer,
        time_function,
        time_async_function
    )
except ImportError:
    pass

try:
    from fastapi_authlib_keycloak.utils.debug import (
        DebugLogger,
        create_debug_router,
        init_debug_environment,
        decode_token,
        validate_token_debug,
        inspect_jwks
    )
except ImportError:
    pass

try:
    from fastapi_authlib_keycloak.utils.rate_limit import (
        create_rate_limiter,
        RateLimitStrategy,
        RateLimitScope,
        RateLimitMiddleware,
        RateLimiter
    )
except ImportError:
    pass

__all__ = [
    # SSL utilities
    "setup_ssl",
    
    # Metrics (optional)
    "configure_metrics",
    "MetricsBackend",
    "MetricsMiddleware",
    "create_fastapi_metrics_endpoint",
    "get_metrics_status",
    "MetricsTimer",
    "AsyncMetricsTimer",
    "time_function",
    "time_async_function",
    
    # Debug (optional)
    "DebugLogger",
    "create_debug_router",
    "init_debug_environment",
    "decode_token",
    "validate_token_debug",
    "inspect_jwks",
    
    # Rate limiting (optional)
    "create_rate_limiter",
    "RateLimitStrategy",
    "RateLimitScope",
    "RateLimitMiddleware",
    "RateLimiter"
]
