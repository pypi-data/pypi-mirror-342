#!/usr/bin/env python3
"""
FastAPI-Authlib-Keycloak
------------------------

A comprehensive integration between FastAPI, Authlib, and Keycloak
for seamless authentication and authorization with enhanced features
including metrics collection, debugging utilities, and rate limiting.

This module provides a simple interface for adding Keycloak authentication
to FastAPI applications with enhanced Swagger UI integration.

Basic Usage:
```python
from fastapi import FastAPI, Depends
from fastapi_authlib_keycloak import KeycloakAuth

app = FastAPI()

# Initialize Keycloak Auth
auth = KeycloakAuth(
    app,
    keycloak_url="https://keycloak.example.com/auth",
    keycloak_realm="your-realm",
    client_id="your-client-id",
    client_secret="your-client-secret"
)

# Use auth dependencies in your routes
@app.get("/protected")
async def protected_route(user = Depends(auth.get_current_user)):
    return {"message": f"Hello, {user.username}!"}

# For role-based access control
@app.get("/admin-only")
async def admin_route(user = Depends(auth.require_roles(["admin"]))):
    return {"message": "Admin access granted"}
```

Enhanced Features:
- Enhanced JWT validation with JWKS caching and rotation
- Metrics collection for monitoring and observability
- Debugging utilities for development
- Rate limiting for authentication endpoints
- Robust configuration with sensible defaults
- Certificate verification utilities

:copyright: (c) 2025 Harsha
:license: MIT
"""

import os

__version__ = "0.2.5"  # Updated with certificate verification fix

# Export main classes
from fastapi_authlib_keycloak.keycloak_auth import KeycloakAuth
from fastapi_authlib_keycloak.models import User

# Export configuration model
from fastapi_authlib_keycloak.config_model import KeycloakConfig, create_config

# Export certificate utilities
from fastapi_authlib_keycloak.patch import fix_ssl_certificate_issue, apply_all_patches

# Export diagnostic utilities
try:
    from fastapi_authlib_keycloak.utils.diagnostic import run_diagnostic_wizard as run_diagnostics, print_diagnostic_report as diagnose_and_fix
except ImportError:
    pass

# Export optional enhanced validator
try:
    from fastapi_authlib_keycloak.auth.enhanced_validator import (
        create_enhanced_validator,
        TokenValidationMethod
    )
except ImportError:
    pass

# Export optional metrics module
try:
    from fastapi_authlib_keycloak.utils.metrics import (
        configure_metrics,
        MetricsBackend
    )
except ImportError:
    pass

# Export optional rate limiting
try:
    from fastapi_authlib_keycloak.utils.rate_limit import (
        create_rate_limiter,
        RateLimitStrategy,
        RateLimitScope
    )
except ImportError:
    pass

__all__ = [
    # Main classes
    "KeycloakAuth", 
    "User",
    # Configuration and diagnostics
    "KeycloakConfig",
    "create_config",
    # Certificate utilities
    "fix_ssl_certificate_issue",
    "apply_all_patches"
]

# Add optional components to __all__ if available
try:
    __all__.extend(["run_diagnostics", "diagnose_and_fix"])
except NameError:
    pass

try:
    __all__.extend(["create_enhanced_validator", "TokenValidationMethod"])
except NameError:
    pass

try:
    __all__.extend(["configure_metrics", "MetricsBackend"])
except NameError:
    pass

try:
    __all__.extend(["create_rate_limiter", "RateLimitStrategy", "RateLimitScope"])
except NameError:
    pass

# Auto-apply patches if environment variable is set
if "KEYCLOAK_AUTO_PATCH" in os.environ:
    from fastapi_authlib_keycloak.patch import auto_patch
    auto_patch()
