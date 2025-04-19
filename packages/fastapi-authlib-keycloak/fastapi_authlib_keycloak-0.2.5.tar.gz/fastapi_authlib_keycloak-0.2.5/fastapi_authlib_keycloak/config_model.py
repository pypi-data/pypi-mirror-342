"""
Enhanced configuration model for FastAPI-Authlib-Keycloak.

This module provides a robust Pydantic model for validating and processing
configuration options with comprehensive error messages, sensible defaults,
and extensive validation.

Features:
- Comprehensive validation with detailed error messages
- Automatic type conversion from environment variables
- Support for both Pydantic v1 and v2
- Smart parsing of complex values (lists, objects, etc.)
- Development mode with sensible defaults
- Mock mode for testing without a real Keycloak server
- Configuration diagnostics and validation
"""

import os
import sys
import json
import logging
import platform
import secrets
import re
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Union, Any, Set, Tuple, Callable

# Import the appropriate Pydantic module based on the version
try:
    from pydantic import BaseModel, Field, validator, root_validator
    PYDANTIC_V1 = True
except ImportError:
    from pydantic import BaseModel, Field, field_validator, model_validator
    PYDANTIC_V1 = False

# Import cert_utils for certificate verification
try:
    from fastapi_authlib_keycloak.utils.cert_utils import (
        fix_certificate_issues,
        check_keycloak_certificate,
        auto_configure_ssl
    )
    CERT_UTILS_AVAILABLE = True
except ImportError:
    CERT_UTILS_AVAILABLE = False

# Set up logger
logger = logging.getLogger("fastapi-keycloak.config")


# Enums for configuration options
class TokenValidationMethod(str, Enum):
    """Method for validating tokens."""
    JWT = "jwt"
    INTROSPECTION = "introspection"
    BOTH = "both"


class RateLimitStrategy(str, Enum):
    """Strategy for rate limiting."""
    FIXED = "fixed"
    SLIDING = "sliding"
    TOKEN_BUCKET = "token_bucket"


class RateLimitScope(str, Enum):
    """Scope for rate limiting."""
    IP = "ip"
    CLIENT = "client"
    USER = "user"


class OnSSLError(str, Enum):
    """Action to take on SSL error."""
    RAISE = "raise"
    WARN = "warn"
    IGNORE = "ignore"


class LogLevel(str, Enum):
    """Logging levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class SameSitePolicy(str, Enum):
    """Same-site cookie policy."""
    LAX = "lax"
    STRICT = "strict"
    NONE = "none"


class CertVerifyMode(str, Enum):
    """Certificate verification modes."""
    DEFAULT = "default"
    PLATFORM = "platform"
    DISABLED = "disabled"
    AUTO = "auto"


# Helper functions for parsing configuration values
def parse_cors_origins(v) -> List[str]:
    """
    Parse CORS origins from various formats into a list.
    
    Handles:
    - String lists: "http://localhost:3000,http://localhost:8000"
    - JSON arrays: '["http://localhost:3000","http://localhost:8000"]'
    - Single values: "*" or "http://localhost:3000"
    - Empty values: "" (returns ["*"])
    - Already parsed lists: ["http://localhost:3000", "http://localhost:8000"]
    
    Returns:
        List[str]: List of CORS origins
    """
    # If already a list, return as is
    if isinstance(v, list):
        return v
        
    # If not a string or None, return default
    if not isinstance(v, str) or v is None:
        logger.debug("CORS origins not a string or None, using default ['*']")
        return ["*"]
        
    # If empty string or whitespace, return default
    if not v.strip():
        logger.debug("CORS origins empty, using default ['*']")
        return ["*"]
        
    # If it's the wildcard character, return as list
    if v.strip() == "*":
        logger.debug("CORS origins is wildcard '*'")
        return ["*"]
    
    # Try parsing as JSON if it looks like a JSON array
    if v.strip().startswith("[") and v.strip().endswith("]"):
        try:
            parsed = json.loads(v)
            if isinstance(parsed, list):
                logger.debug(f"CORS origins parsed as JSON array: {parsed}")
                return parsed
        except Exception as e:
            logger.debug(f"Failed to parse CORS origins as JSON: {str(e)}")
            # Continue to comma-separated parsing
    
    # Parse as comma-separated string (default fallback)
    origins = [origin.strip() for origin in v.split(",") if origin.strip()]
    logger.debug(f"CORS origins parsed as comma-separated string: {origins}")
    return origins


def parse_string_list(v, default=None) -> List[str]:
    """
    Parse a generic string list from various formats.
    
    Similar to parse_cors_origins but with a custom default.
    
    Args:
        v: Value to parse
        default: Default value to return for empty/invalid inputs
        
    Returns:
        List[str]: Parsed list of strings
    """
    if default is None:
        default = []
        
    # If already a list, return as is
    if isinstance(v, list):
        return v
        
    # If not a string or None, return default
    if not isinstance(v, str) or v is None:
        return default
        
    # If empty string or whitespace, return default
    if not v.strip():
        return default
    
    # Try parsing as JSON if it looks like a JSON array
    if v.strip().startswith("[") and v.strip().endswith("]"):
        try:
            parsed = json.loads(v)
            if isinstance(parsed, list):
                return parsed
        except Exception:
            # Continue to comma-separated parsing
            pass
    
    # Parse as comma-separated string (default fallback)
    return [item.strip() for item in v.split(",") if item.strip()]


def parse_boolean(v) -> bool:
    """
    Parse boolean value from various formats.
    
    Handles:
    - Boolean: True/False
    - String: "true"/"false" (case insensitive)
    - Integer: 1/0
    
    Returns:
        bool: Parsed boolean value
    """
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        return v.lower() in ("yes", "true", "t", "1", "on", "y")
    if isinstance(v, int):
        return v != 0
    return False


def validate_ssl_verify(v) -> Union[bool, str]:
    """
    Validate SSL verification mode.
    
    Args:
        v: SSL verification mode (True, False, or path to CA bundle)
        
    Returns:
        Union[bool, str]: Validated SSL verification mode
    """
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        if v.lower() in ("true", "t", "1", "yes", "on"):
            return True
        if v.lower() in ("false", "f", "0", "no", "off"):
            return False
        # Check if it's a path to a CA bundle
        if Path(v).exists():
            return v
    return True  # Default to safe mode


def generate_secret() -> str:
    """
    Generate a secure random secret for sessions.
    
    Returns:
        str: Random 32-byte secret encoded as hex
    """
    return secrets.token_hex(32)


def parse_dict(v, default=None) -> Dict:
    """
    Parse a dictionary from various formats.
    
    Handles:
    - Dictionary: {key: value, ...}
    - JSON string: '{"key": "value", ...}'
    
    Args:
        v: Value to parse
        default: Default value to return for empty/invalid inputs
        
    Returns:
        Dict: Parsed dictionary
    """
    if default is None:
        default = {}
        
    # If already a dict, return as is
    if isinstance(v, dict):
        return v
        
    # If not a string or None, return default
    if not isinstance(v, str) or v is None:
        return default
        
    # If empty string or whitespace, return default
    if not v.strip():
        return default
    
    # Try parsing as JSON
    try:
        parsed = json.loads(v)
        if isinstance(parsed, dict):
            return parsed
    except Exception as e:
        logger.debug(f"Failed to parse dictionary from JSON: {str(e)}")
        
    # Return default if parsing failed
    return default


# Configuration model with comprehensive validation and documentation
class KeycloakConfig(BaseModel):
    """
    Comprehensive configuration for FastAPI-Authlib-Keycloak.
    
    This model validates all configuration options and provides
    sensible defaults with detailed error messages.
    """
    # Required Keycloak settings
    keycloak_url: str = Field(
        ..., 
        title="Keycloak URL",
        description="URL of the Keycloak server (e.g., https://keycloak.example.com/auth)"
    )
    keycloak_realm: str = Field(
        ..., 
        title="Keycloak Realm",
        description="Name of the Keycloak realm"
    )
    client_id: str = Field(
        ..., 
        title="Client ID",
        description="Client ID for the UI client"
    )
    client_secret: str = Field(
        ..., 
        title="Client Secret",
        description="Client secret for the UI client"
    )
    
    # Optional API client settings
    api_client_id: Optional[str] = Field(
        None, 
        title="API Client ID",
        description="Client ID for the API client (defaults to client_id if not provided)"
    )
    api_client_secret: Optional[str] = Field(
        None, 
        title="API Client Secret",
        description="Client secret for the API client (defaults to client_secret if not provided)"
    )
    api_base_url: Optional[str] = Field(
        None, 
        title="API Base URL",
        description="Base URL for the API (defaults to request base URL if not provided)"
    )
    
    # Session settings
    session_secret: Optional[str] = Field(
        None, 
        title="Session Secret",
        description="Secret key for session encryption (auto-generated if not provided)"
    )
    session_max_age: int = Field(
        3600, 
        title="Session Max Age",
        description="Maximum session age in seconds",
        ge=0
    )
    session_https_only: bool = Field(
        False, 
        title="Session HTTPS Only",
        description="Whether session cookies should be HTTPS only"
    )
    session_same_site: SameSitePolicy = Field(
        SameSitePolicy.LAX, 
        title="Session Same Site",
        description="Same-site policy for cookies (lax, strict, none)"
    )
    
    # CORS settings
    cors_origins: List[str] = Field(
        ["*"], 
        title="CORS Origins",
        description="List of allowed CORS origins (accepts comma-separated string, JSON array, or list)"
    )
    cors_credentials: bool = Field(
        True, 
        title="CORS Credentials",
        description="Whether to allow credentials in CORS"
    )
    cors_methods: List[str] = Field(
        ["*"],
        title="CORS Methods",
        description="HTTP methods to allow in CORS (accepts comma-separated string, JSON array, or list)"
    )
    cors_headers: List[str] = Field(
        ["*"],
        title="CORS Headers",
        description="HTTP headers to allow in CORS (accepts comma-separated string, JSON array, or list)"
    )
    cors_max_age: int = Field(
        1800,
        title="CORS Max Age",
        description="Maximum age for CORS preflight requests in seconds",
        ge=0
    )
    
    # Security settings
    token_algorithm: str = Field(
        "RS256", 
        title="Token Algorithm",
        description="Algorithm for token validation"
    )
    strict_client_check: bool = Field(
        False, 
        title="Strict Client Check",
        description="Whether to strictly enforce client ID matching in tokens"
    )
    
    # SSL settings
    ssl_enabled: bool = Field(
        False, 
        title="SSL Enabled",
        description="Whether to enable SSL certificate verification"
    )
    ssl_cert_file: Optional[str] = Field(
        None, 
        title="SSL Certificate File",
        description="Path to SSL certificate file"
    )
    ssl_key_file: Optional[str] = Field(
        None, 
        title="SSL Key File",
        description="Path to SSL key file"
    )
    ssl_verify: Union[bool, str] = Field(
        True, 
        title="SSL Verify",
        description="SSL verification mode (True for standard verification, "
                   "False to disable verification, or string path to a CA bundle)"
    )
    
    # Development settings
    development_mode: bool = Field(
        False, 
        title="Development Mode",
        description="Whether to enable development-friendly defaults"
    )
    allow_http: bool = Field(
        False, 
        title="Allow HTTP",
        description="Allow HTTP for Keycloak URL (insecure, for development only)"
    )
    jwks_cache_ttl: int = Field(
        3600, 
        title="JWKS Cache TTL",
        description="Cache time for JWKS in seconds",
        ge=0
    )
    jwks_file: Optional[str] = Field(
        None, 
        title="JWKS File",
        description="Path to a local JWKS file (for offline verification)"
    )
    on_ssl_error: OnSSLError = Field(
        OnSSLError.RAISE, 
        title="On SSL Error",
        description="How to handle SSL errors ('raise', 'warn', or 'ignore')"
    )
    
    # Swagger UI settings
    custom_swagger_title: Optional[str] = Field(
        None, 
        title="Custom Swagger Title",
        description="Custom title for Swagger UI"
    )
    custom_swagger_css: Optional[str] = Field(
        None, 
        title="Custom Swagger CSS",
        description="Path to custom CSS file for Swagger UI"
    )
    
    # Debug settings
    debug_endpoints_enabled: bool = Field(
        False, 
        title="Debug Endpoints Enabled",
        description="Whether to enable debug endpoints"
    )

    # Token validation settings
    validation_method: TokenValidationMethod = Field(
        TokenValidationMethod.JWT, 
        title="Validation Method",
        description="Method for token validation (jwt, introspection, both)"
    )
    introspection_cache_ttl: int = Field(
        300, 
        title="Introspection Cache TTL",
        description="Cache time for introspection results in seconds",
        ge=0
    )
    
    # Rate limiting settings
    rate_limit_enabled: bool = Field(
        False, 
        title="Rate Limit Enabled",
        description="Whether to enable rate limiting"
    )
    rate_limit_max_requests: int = Field(
        100, 
        title="Rate Limit Max Requests",
        description="Maximum number of requests per window",
        gt=0
    )
    rate_limit_window_seconds: int = Field(
        60, 
        title="Rate Limit Window Seconds",
        description="Time window for rate limiting in seconds",
        gt=0
    )
    rate_limit_strategy: RateLimitStrategy = Field(
        RateLimitStrategy.SLIDING, 
        title="Rate Limit Strategy",
        description="Rate limiting strategy (fixed, sliding, token_bucket)"
    )
    rate_limit_scope: RateLimitScope = Field(
        RateLimitScope.IP, 
        title="Rate Limit Scope",
        description="Scope for rate limiting (ip, client, user)"
    )
    rate_limit_use_redis: bool = Field(
        False, 
        title="Rate Limit Use Redis",
        description="Whether to use Redis for rate limiting storage"
    )
    rate_limit_redis_url: str = Field(
        "redis://localhost:6379/0", 
        title="Rate Limit Redis URL",
        description="Redis URL for rate limiting storage"
    )
    
    # Logging settings
    log_level: LogLevel = Field(
        LogLevel.INFO, 
        title="Log Level",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)"
    )
    
    # Mock mode for development
    mock_mode: bool = Field(
        False, 
        title="Mock Mode",
        description="Enable mock mode for development without a real Keycloak server"
    )
    mock_user_data: Optional[Dict[str, Any]] = Field(
        None, 
        title="Mock User Data",
        description="Mock user data for development"
    )
    mock_jwks_enabled: bool = Field(
        False,
        title="Mock JWKS Enabled",
        description="Whether to enable a mock JWKS endpoint in mock mode"
    )
    mock_user_roles: List[str] = Field(
        ["user"],
        title="Mock User Roles",
        description="Default roles for mock users"
    )
    
    # Certificate verification options
    cert_verify_mode: Optional[CertVerifyMode] = Field(
        None,
        title="Certificate Verification Mode",
        description="Custom certificate verification mode (default, platform, disabled, or auto)"
    )
    
    # Additional configuration
    use_secure_cookies: bool = Field(
        None,
        title="Use Secure Cookies",
        description="Whether to use secure cookies (defaults to True for HTTPS, False for HTTP)"
    )
    auto_redirect_login: bool = Field(
        True,
        title="Auto Redirect Login",
        description="Whether to automatically redirect to login when token is missing/invalid"
    )
    logout_redirect_url: Optional[str] = Field(
        None,
        title="Logout Redirect URL",
        description="URL to redirect to after logout (defaults to '/')"
    )
    login_redirect_url: Optional[str] = Field(
        None,
        title="Login Redirect URL",
        description="URL to redirect to after login (defaults to referrer or '/')"
    )
    error_template: Optional[str] = Field(
        None,
        title="Error Template",
        description="Custom HTML template for error pages"
    )
    
    # Connection settings
    connection_timeout: float = Field(
        10.0,
        title="Connection Timeout",
        description="Timeout for HTTP connections in seconds",
        gt=0
    )
    connection_retries: int = Field(
        3,
        title="Connection Retries",
        description="Maximum number of connection retry attempts",
        ge=0
    )
    connection_pool_maxsize: int = Field(
        10,
        title="Connection Pool Maxsize",
        description="Maximum number of connections in the connection pool",
        gt=0
    )
    
    # OAuth settings
    oauth_scopes: List[str] = Field(
        ["openid", "email", "profile"],
        title="OAuth Scopes",
        description="Scopes to request during OAuth flow"
    )
    oauth_pkce_enabled: bool = Field(
        True,
        title="OAuth PKCE Enabled",
        description="Whether to use PKCE for the OAuth flow (recommended)"
    )

    # Define validators using either Pydantic v1 or v2 style
    if PYDANTIC_V1:
        # Pydantic v1 validators
        @validator('keycloak_url')
        def validate_keycloak_url(cls, v, values):
            """Validate Keycloak URL and handle trailing slash."""
            if not v:
                raise ValueError("Keycloak URL is required")
            
            # Remove trailing slash
            if v.endswith('/'):
                v = v[:-1]
            
            # Check for HTTP when allow_http is False
            allow_http = values.get('allow_http', False)
            development_mode = values.get('development_mode', False)
            
            if not allow_http and not development_mode and v.startswith('http://'):
                raise ValueError(
                    "Using HTTP for Keycloak URL is insecure. "
                    "Set allow_http=True or development_mode=True to use HTTP (not recommended for production)."
                )
            
            return v
            
        @validator('cors_origins', pre=True)
        def validate_cors_origins(cls, v):
            """Validate CORS origins and parse from various formats."""
            return parse_cors_origins(v)
        
        @validator('cors_methods', 'cors_headers', pre=True)
        def validate_cors_lists(cls, v):
            """Validate CORS methods and headers."""
            return parse_string_list(v, default=["*"])
            
        @validator('ssl_verify', pre=True)
        def validate_ssl_verify_mode(cls, v):
            """Validate SSL verification mode."""
            return validate_ssl_verify(v)
            
        @validator('session_same_site')
        def validate_same_site(cls, v):
            """Validate same-site cookie policy."""
            if isinstance(v, SameSitePolicy):
                return v
                
            if isinstance(v, str):
                try:
                    return SameSitePolicy(v.lower())
                except ValueError:
                    raise ValueError(f"Same-site policy must be one of: {', '.join([e.value for e in SameSitePolicy])}")
            
            raise ValueError(f"Invalid type for same-site policy: {type(v)}")
            
        @validator('log_level')
        def validate_log_level(cls, v):
            """Validate log level."""
            if isinstance(v, LogLevel):
                return v
                
            if isinstance(v, str):
                try:
                    return LogLevel(v.upper())
                except ValueError:
                    raise ValueError(f"Log level must be one of: {', '.join([e.value for e in LogLevel])}")
            
            raise ValueError(f"Invalid type for log level: {type(v)}")
            
        @validator('api_client_id', 'api_client_secret')
        def set_api_defaults(cls, v, values, **kwargs):
            """Set API client defaults if not provided."""
            if v is None:
                field = kwargs.get('field')
                if field == 'api_client_id' and 'client_id' in values:
                    return values['client_id']
                elif field == 'api_client_secret' and 'client_secret' in values:
                    return values['client_secret']
            return v
            
        @validator('session_https_only', 'ssl_enabled', 'cors_credentials', 
                   'strict_client_check', 'development_mode', 'allow_http',
                   'debug_endpoints_enabled', 'rate_limit_enabled', 
                   'rate_limit_use_redis', 'mock_mode', 'mock_jwks_enabled',
                   'auto_redirect_login', 'oauth_pkce_enabled', pre=True)
        def validate_boolean(cls, v):
            """Validate boolean fields from various formats."""
            return parse_boolean(v)
            
        @validator('session_secret')
        def ensure_session_secret(cls, v):
            """Ensure session secret is set or generate a secure one."""
            if not v:
                logger.info("Generating secure random session secret")
                return generate_secret()
            return v
            
        @validator('use_secure_cookies')
        def set_secure_cookies_default(cls, v, values):
            """Determine if secure cookies should be used based on URL protocol."""
            if v is not None:
                return v
                
            # Default to secure cookies for HTTPS, non-secure for HTTP
            keycloak_url = values.get('keycloak_url', '')
            if keycloak_url.startswith('https://'):
                return True
            return False
            
        @validator('mock_user_data', pre=True)
        def parse_mock_user_data(cls, v):
            """Parse mock user data from various formats."""
            return parse_dict(v)

        @validator('oauth_scopes', pre=True)
        def parse_oauth_scopes(cls, v):
            """Parse OAuth scopes from various formats."""
            return parse_string_list(v, default=["openid", "email", "profile"])
            
        @validator('mock_user_roles', pre=True)
        def parse_mock_user_roles(cls, v):
            """Parse mock user roles from various formats."""
            return parse_string_list(v, default=["user"])
            
        @validator('cert_verify_mode')
        def validate_cert_verify_mode(cls, v):
            """Validate certificate verification mode."""
            if v is None:
                return None
                
            if isinstance(v, CertVerifyMode):
                return v
                
            if isinstance(v, str):
                try:
                    return CertVerifyMode(v.lower())
                except ValueError:
                    # Check if it's a path to a certificate file
                    if Path(v).exists():
                        logger.info(f"Using custom certificate file: {v}")
                        return v
                    raise ValueError(f"Certificate verification mode must be one of: {', '.join([e.value for e in CertVerifyMode])}")
            
            raise ValueError(f"Invalid type for certificate verification mode: {type(v)}")
            
        @root_validator
        def development_mode_defaults(cls, values):
            """Apply development mode defaults if enabled."""
            if values.get('development_mode'):
                # Only set values that haven't been explicitly provided
                if values.get('allow_http') is None:
                    values['allow_http'] = True
                if values.get('ssl_verify') is None:
                    values['ssl_verify'] = False
                if values.get('on_ssl_error') is None:
                    values['on_ssl_error'] = OnSSLError.WARN
                if values.get('debug_endpoints_enabled') is None:
                    values['debug_endpoints_enabled'] = True
                if values.get('log_level') is None:
                    values['log_level'] = LogLevel.DEBUG
            return values
            
        @root_validator
        def mock_mode_validation(cls, values):
            """Validate mock mode settings."""
            if values.get('mock_mode'):
                # In mock mode, generate default mock user data if not provided
                if not values.get('mock_user_data'):
                    roles = values.get('mock_user_roles', ["user"])
                    values['mock_user_data'] = {
                        "sub": "mock-user-id",
                        "preferred_username": "mock-user",
                        "email": "mock-user@example.com",
                        "name": "Mock User",
                        "realm_access": {
                            "roles": roles
                        }
                    }
                    
                # Enable mock JWKS by default in mock mode
                if values.get('mock_jwks_enabled') is None:
                    values['mock_jwks_enabled'] = True
            return values
            
        @root_validator
        def ssl_verification_settings(cls, values):
            """Configure SSL verification settings."""
            if CERT_UTILS_AVAILABLE and values.get('cert_verify_mode'):
                mode = values.get('cert_verify_mode')
                if isinstance(mode, CertVerifyMode):
                    mode = mode.value
                    
                # Apply certificate verification mode
                logger.info(f"Applying certificate verification mode: {mode}")
                
                # Don't actually fix issues here, just log the intent
                # The actual fixing will happen in the KeycloakAuth class
                if mode in [CertVerifyMode.PLATFORM.value, CertVerifyMode.DISABLED.value, 
                            CertVerifyMode.AUTO.value, CertVerifyMode.DEFAULT.value]:
                    logger.info(f"Will configure certificate verification mode: {mode}")
                else:
                    # Custom certificate file
                    logger.info(f"Will use custom certificate file: {mode}")
            return values
            
    else:
        # Pydantic v2 validators
        @field_validator('keycloak_url')
        def validate_keycloak_url(cls, v, info):
            """Validate Keycloak URL and handle trailing slash."""
            if not v:
                raise ValueError("Keycloak URL is required")
            
            # Remove trailing slash
            if v.endswith('/'):
                v = v[:-1]
            
            # Check for HTTP when allow_http is False
            data = info.data
            allow_http = data.get('allow_http', False)
            development_mode = data.get('development_mode', False)
            
            if not allow_http and not development_mode and v.startswith('http://'):
                raise ValueError(
                    "Using HTTP for Keycloak URL is insecure. "
                    "Set allow_http=True or development_mode=True to use HTTP (not recommended for production)."
                )
            
            return v
            
        @field_validator('cors_origins', mode='before')
        def validate_cors_origins(cls, v):
            """Validate CORS origins and parse from various formats."""
            return parse_cors_origins(v)
            
        @field_validator('cors_methods', 'cors_headers', mode='before')
        def validate_cors_lists(cls, v):
            """Validate CORS methods and headers."""
            return parse_string_list(v, default=["*"])
            
        @field_validator('ssl_verify', mode='before')
        def validate_ssl_verify_mode(cls, v):
            """Validate SSL verification mode."""
            return validate_ssl_verify(v)
            
        @field_validator('session_same_site')
        def validate_same_site(cls, v):
            """Validate same-site cookie policy."""
            if isinstance(v, SameSitePolicy):
                return v
                
            if isinstance(v, str):
                try:
                    return SameSitePolicy(v.lower())
                except ValueError:
                    raise ValueError(f"Same-site policy must be one of: {', '.join([e.value for e in SameSitePolicy])}")
            
            raise ValueError(f"Invalid type for same-site policy: {type(v)}")
            
        @field_validator('log_level')
        def validate_log_level(cls, v):
            """Validate log level."""
            if isinstance(v, LogLevel):
                return v
                
            if isinstance(v, str):
                try:
                    return LogLevel(v.upper())
                except ValueError:
                    raise ValueError(f"Log level must be one of: {', '.join([e.value for e in LogLevel])}")
            
            raise ValueError(f"Invalid type for log level: {type(v)}")
            
        @field_validator('api_client_id', 'api_client_secret')
        def set_api_defaults(cls, v, info):
            """Set API client defaults if not provided."""
            if v is None:
                data = info.data
                if info.field_name == 'api_client_id' and 'client_id' in data:
                    return data['client_id']
                elif info.field_name == 'api_client_secret' and 'client_secret' in data:
                    return data['client_secret']
            return v
            
        @field_validator('session_https_only', 'ssl_enabled', 'cors_credentials', 
                        'strict_client_check', 'development_mode', 'allow_http',
                        'debug_endpoints_enabled', 'rate_limit_enabled', 
                        'rate_limit_use_redis', 'mock_mode', 'mock_jwks_enabled',
                        'auto_redirect_login', 'oauth_pkce_enabled', mode='before')
        def validate_boolean(cls, v):
            """Validate boolean fields from various formats."""
            return parse_boolean(v)
            
        @field_validator('session_secret')
        def ensure_session_secret(cls, v):
            """Ensure session secret is set or generate a secure one."""
            if not v:
                logger.info("Generating secure random session secret")
                return generate_secret()
            return v
            
        @field_validator('use_secure_cookies')
        def set_secure_cookies_default(cls, v, info):
            """Determine if secure cookies should be used based on URL protocol."""
            if v is not None:
                return v
                
            # Default to secure cookies for HTTPS, non-secure for HTTP
            data = info.data
            keycloak_url = data.get('keycloak_url', '')
            if keycloak_url.startswith('https://'):
                return True
            return False
            
        @field_validator('mock_user_data', mode='before')
        def parse_mock_user_data(cls, v):
            """Parse mock user data from various formats."""
            return parse_dict(v)

        @field_validator('oauth_scopes', mode='before')
        def parse_oauth_scopes(cls, v):
            """Parse OAuth scopes from various formats."""
            return parse_string_list(v, default=["openid", "email", "profile"])
            
        @field_validator('mock_user_roles', mode='before')
        def parse_mock_user_roles(cls, v):
            """Parse mock user roles from various formats."""
            return parse_string_list(v, default=["user"])
            
        @field_validator('cert_verify_mode')
        def validate_cert_verify_mode(cls, v):
            """Validate certificate verification mode."""
            if v is None:
                return None
                
            if isinstance(v, CertVerifyMode):
                return v
                
            if isinstance(v, str):
                try:
                    return CertVerifyMode(v.lower())
                except ValueError:
                    # Check if it's a path to a certificate file
                    if Path(v).exists():
                        logger.info(f"Using custom certificate file: {v}")
                        return v
                    raise ValueError(f"Certificate verification mode must be one of: {', '.join([e.value for e in CertVerifyMode])}")
            
            raise ValueError(f"Invalid type for certificate verification mode: {type(v)}")
            
        @model_validator(mode='after')
        def development_mode_defaults(self):
            """Apply development mode defaults if enabled."""
            if self.development_mode:
                # Only set values that haven't been explicitly provided
                if getattr(self, 'allow_http', None) is None:
                    self.allow_http = True
                if getattr(self, 'ssl_verify', None) is None:
                    self.ssl_verify = False
                if getattr(self, 'on_ssl_error', None) is None:
                    self.on_ssl_error = OnSSLError.WARN
                if getattr(self, 'debug_endpoints_enabled', None) is None:
                    self.debug_endpoints_enabled = True
                if getattr(self, 'log_level', None) is None:
                    self.log_level = LogLevel.DEBUG
            return self
            
        @model_validator(mode='after')
        def mock_mode_validation(self):
            """Validate mock mode settings."""
            if self.mock_mode:
                # In mock mode, generate default mock user data if not provided
                if not self.mock_user_data:
                    roles = getattr(self, 'mock_user_roles', ["user"])
                    self.mock_user_data = {
                        "sub": "mock-user-id",
                        "preferred_username": "mock-user",
                        "email": "mock-user@example.com",
                        "name": "Mock User",
                        "realm_access": {
                            "roles": roles
                        }
                    }
                    
                # Enable mock JWKS by default in mock mode
                if getattr(self, 'mock_jwks_enabled', None) is None:
                    self.mock_jwks_enabled = True
            return self
            
        @model_validator(mode='after')
        def ssl_verification_settings(self):
            """Configure SSL verification settings."""
            if CERT_UTILS_AVAILABLE and self.cert_verify_mode:
                mode = self.cert_verify_mode
                if isinstance(mode, CertVerifyMode):
                    mode = mode.value
                    
                # Apply certificate verification mode
                logger.info(f"Applying certificate verification mode: {mode}")
                
                # Don't actually fix issues here, just log the intent
                # The actual fixing will happen in the KeycloakAuth class
                if mode in [CertVerifyMode.PLATFORM.value, CertVerifyMode.DISABLED.value, 
                            CertVerifyMode.AUTO.value, CertVerifyMode.DEFAULT.value]:
                    logger.info(f"Will configure certificate verification mode: {mode}")
                else:
                    # Custom certificate file
                    logger.info(f"Will use custom certificate file: {mode}")
            return self
    
    class Config:
        """Pydantic model configuration."""
        extra = "ignore"  # Allow extra fields for forward compatibility
        str_strip_whitespace = True


def get_default_config_for_mode(mode: str = "development") -> Dict[str, Any]:
    """
    Get default configuration values for a specific mode.
    
    Args:
        mode: Configuration mode:
            - "development": Local development configuration
            - "testing": Configuration for automated tests
            - "production": Recommended production settings
            - "mock": Configuration with mock mode enabled
            
    Returns:
        Dict[str, Any]: Default configuration values
    """
    base_config = {
        "keycloak_url": "placeholder",
        "keycloak_realm": "placeholder",
        "client_id": "placeholder",
        "client_secret": "placeholder",
    }
    
    if mode == "development":
        return {
            **base_config,
            "development_mode": True,
            "allow_http": True,
            "ssl_verify": False,
            "on_ssl_error": "warn",
            "debug_endpoints_enabled": True,
            "log_level": "DEBUG",
            "cert_verify_mode": "platform",
        }
    
    elif mode == "testing":
        return {
            **base_config,
            "development_mode": True,
            "mock_mode": True,
            "mock_jwks_enabled": True,
            "allow_http": True,
            "ssl_verify": False,
            "log_level": "DEBUG",
        }
    
    elif mode == "production":
        return {
            **base_config,
            "development_mode": False,
            "allow_http": False,
            "ssl_verify": True,
            "on_ssl_error": "raise",
            "debug_endpoints_enabled": False,
            "strict_client_check": True,
            "session_https_only": True,
            "session_same_site": "lax",
            "log_level": "INFO",
            "cert_verify_mode": "platform",
        }
    
    elif mode == "mock":
        return {
            **base_config,
            "development_mode": True,
            "mock_mode": True,
            "mock_jwks_enabled": True,
            "allow_http": True,
            "ssl_verify": False,
            "debug_endpoints_enabled": True,
            "log_level": "DEBUG",
        }
    
    else:
        raise ValueError(f"Unknown configuration mode: {mode}")


# Function to create a configuration from multiple sources
def create_config(
    env_prefix: str = "",
    dotenv_path: Optional[str] = None,
    config_file: Optional[str] = None,
    mode: Optional[str] = None,
    validate: bool = True,
    **explicit_values
) -> KeycloakConfig:
    """
    Create a KeycloakConfig from multiple sources with hierarchical precedence.
    
    Sources are checked in the following order of precedence:
    1. Explicit values passed as keyword arguments
    2. Environment variables (with optional prefix)
    3. Variables from .env file
    4. Configuration from JSON/YAML file
    5. Default values based on mode
    6. Default values from the model
    
    Args:
        env_prefix: Prefix for environment variables (e.g., "MYAPP_")
        dotenv_path: Path to .env file
        config_file: Path to JSON or YAML configuration file
        mode: Configuration mode to use for defaults
        validate: Whether to validate the configuration
        **explicit_values: Explicit configuration values
        
    Returns:
        KeycloakConfig: Configuration instance
    """
    # Initialize logger
    logger = logging.getLogger("fastapi-keycloak.config")
    
    # Setup dictionary to collect values
    config_values = {}
    
    # If mode is specified, get default values for that mode
    if mode:
        logger.info(f"Using '{mode}' mode for default configuration values")
        mode_defaults = get_default_config_for_mode(mode)
        config_values.update(mode_defaults)
    
    # Load from config file if specified
    if config_file:
        config_path = Path(config_file)
        if config_path.exists():
            logger.info(f"Loading configuration from file: {config_path}")
            try:
                extension = config_path.suffix.lower()
                
                if extension == '.json':
                    # JSON file
                    import json
                    with open(config_path, 'r') as f:
                        file_config = json.load(f)
                        
                elif extension in ('.yaml', '.yml'):
                    # YAML file
                    try:
                        import yaml
                        with open(config_path, 'r') as f:
                            file_config = yaml.safe_load(f)
                    except ImportError:
                        logger.warning("PyYAML not installed, skipping YAML config file loading")
                        file_config = {}
                else:
                    logger.warning(f"Unsupported config file format: {extension}")
                    file_config = {}
                
                # Update config values
                config_values.update(file_config)
                
            except Exception as e:
                logger.error(f"Error loading config file: {str(e)}")
    
    # Load from .env file if specified
    if dotenv_path:
        env_path = Path(dotenv_path)
        if env_path.exists():
            logger.info(f"Loading environment from {env_path}")
            try:
                from dotenv import load_dotenv
                load_dotenv(dotenv_path=env_path)
            except ImportError:
                logger.warning("python-dotenv not installed, skipping .env file loading")
    
    # Define mapping of environment variables to config keys
    env_mappings = {
        "KEYCLOAK_URL": "keycloak_url",
        "KEYCLOAK_REALM": "keycloak_realm",
        "CLIENT_ID": "client_id",
        "CLIENT_SECRET": "client_secret",
        "API_CLIENT_ID": "api_client_id",
        "API_CLIENT_SECRET": "api_client_secret",
        "API_BASE_URL": "api_base_url",
        "SESSION_SECRET": "session_secret",
        "SESSION_MAX_AGE": "session_max_age",
        "SESSION_HTTPS_ONLY": "session_https_only",
        "SESSION_SAME_SITE": "session_same_site",
        "CORS_ORIGINS": "cors_origins",
        "CORS_CREDENTIALS": "cors_credentials",
        "CORS_METHODS": "cors_methods",
        "CORS_HEADERS": "cors_headers",
        "CORS_MAX_AGE": "cors_max_age",
        "TOKEN_ALGORITHM": "token_algorithm",
        "STRICT_CLIENT_CHECK": "strict_client_check",
        "SSL_ENABLED": "ssl_enabled",
        "SSL_CERT_FILE": "ssl_cert_file",
        "SSL_KEY_FILE": "ssl_key_file",
        "SSL_VERIFY": "ssl_verify",
        "DEVELOPMENT_MODE": "development_mode",
        "ALLOW_HTTP": "allow_http",
        "JWKS_CACHE_TTL": "jwks_cache_ttl",
        "JWKS_FILE": "jwks_file",
        "ON_SSL_ERROR": "on_ssl_error",
        "CUSTOM_SWAGGER_TITLE": "custom_swagger_title",
        "CUSTOM_SWAGGER_CSS": "custom_swagger_css",
        "DEBUG_ENDPOINTS_ENABLED": "debug_endpoints_enabled",
        "VALIDATION_METHOD": "validation_method",
        "INTROSPECTION_CACHE_TTL": "introspection_cache_ttl",
        "RATE_LIMIT_ENABLED": "rate_limit_enabled",
        "RATE_LIMIT_MAX_REQUESTS": "rate_limit_max_requests",
        "RATE_LIMIT_WINDOW_SECONDS": "rate_limit_window_seconds",
        "RATE_LIMIT_STRATEGY": "rate_limit_strategy",
        "RATE_LIMIT_SCOPE": "rate_limit_scope",
        "RATE_LIMIT_USE_REDIS": "rate_limit_use_redis",
        "RATE_LIMIT_REDIS_URL": "rate_limit_redis_url",
        "LOG_LEVEL": "log_level",
        "MOCK_MODE": "mock_mode",
        "MOCK_USER_DATA": "mock_user_data",
        "MOCK_JWKS_ENABLED": "mock_jwks_enabled",
        "MOCK_USER_ROLES": "mock_user_roles",
        "CERT_VERIFY_MODE": "cert_verify_mode",
        "USE_SECURE_COOKIES": "use_secure_cookies",
        "AUTO_REDIRECT_LOGIN": "auto_redirect_login",
        "LOGOUT_REDIRECT_URL": "logout_redirect_url",
        "LOGIN_REDIRECT_URL": "login_redirect_url",
        "ERROR_TEMPLATE": "error_template",
        "CONNECTION_TIMEOUT": "connection_timeout",
        "CONNECTION_RETRIES": "connection_retries",
        "CONNECTION_POOL_MAXSIZE": "connection_pool_maxsize",
        "OAUTH_SCOPES": "oauth_scopes",
        "OAUTH_PKCE_ENABLED": "oauth_pkce_enabled",
    }
    
    # Load values from environment variables
    for env_name, config_name in env_mappings.items():
        prefixed_env_name = f"{env_prefix}{env_name}"
        env_value = os.environ.get(prefixed_env_name)
        
        if env_value is not None:
            config_values[config_name] = env_value
    
    # Override with explicit values
    for key, value in explicit_values.items():
        if value is not None:
            config_values[key] = value
    
    # Create and validate the configuration
    try:
        config = KeycloakConfig(**config_values)
        
        # Perform additional validation if requested
        if validate:
            validation_result = validate_config(config)
            if not validation_result["valid"]:
                logger.warning(
                    f"Configuration validation failed with {len(validation_result['issues'])} issues"
                )
                for issue in validation_result["issues"]:
                    logger.warning(f"- {issue}")
        
        return config
    
    except Exception as e:
        logger.error(f"Failed to create configuration: {str(e)}")
        
        # Log additional helpful information for specific errors
        if "keycloak_url" in str(e):
            logger.error("Keycloak URL is missing or invalid")
            logger.info(
                "- Ensure KEYCLOAK_URL environment variable is set"
                " (e.g., https://keycloak.example.com/auth)"
            )
            
        if "keycloak_realm" in str(e):
            logger.error("Keycloak realm is missing or invalid")
            logger.info("- Ensure KEYCLOAK_REALM environment variable is set")
            
        if "client_id" in str(e):
            logger.error("Client ID is missing or invalid")
            logger.info("- Ensure CLIENT_ID environment variable is set")
            
        if "client_secret" in str(e):
            logger.error("Client secret is missing or invalid")
            logger.info("- Ensure CLIENT_SECRET environment variable is set")
        
        if "development_mode" in config_values and config_values["development_mode"]:
            logger.info(
                "Development mode is enabled, but configuration is still invalid. "
                "For testing without a real Keycloak server, try setting mock_mode=True."
            )
        
        # Provide general guidance
        logger.info(
            "\nTo resolve this issue, ensure you provide the required configuration either:\n"
            "1. As parameters to KeycloakAuth constructor\n"
            "2. As environment variables (KEYCLOAK_URL, KEYCLOAK_REALM, CLIENT_ID, CLIENT_SECRET)\n"
            "3. In a .env file and specify the path with dotenv_path parameter\n"
            "4. In a configuration file and specify the path with config_file parameter\n\n"
            "For testing without a real Keycloak server, try using the mock mode:\n"
            "create_config(mode=\"mock\", ...)"
        )
        
        raise ValueError(f"Invalid configuration: {str(e)}")


def validate_config(config: KeycloakConfig) -> Dict[str, Any]:
    """
    Validate a configuration and check for potential issues.
    
    Args:
        config: Configuration to validate
        
    Returns:
        Dict[str, Any]: Validation results with issues and warnings
    """
    validation = {
        "valid": True,
        "issues": [],
        "warnings": [],
        "security_concerns": [],
    }
    
    # Check required fields
    required_fields = ["keycloak_url", "keycloak_realm", "client_id", "client_secret"]
    for field in required_fields:
        value = getattr(config, field, None)
        if not value:
            validation["valid"] = False
            validation["issues"].append(f"{field} is required but not provided")
    
    # If basic validation fails, no need to check further
    if not validation["valid"]:
        return validation
    
    # Check URL format
    if config.keycloak_url:
        if not config.keycloak_url.startswith(("http://", "https://")):
            validation["valid"] = False
            validation["issues"].append(
                f"keycloak_url must start with http:// or https://: {config.keycloak_url}"
            )
    
    # Check HTTP usage
    if config.keycloak_url and config.keycloak_url.startswith("http://"):
        if not config.allow_http and not config.development_mode:
            validation["valid"] = False
            validation["issues"].append(
                "Using HTTP for Keycloak URL requires allow_http=True or development_mode=True"
            )
        else:
            validation["security_concerns"].append(
                "Using HTTP for Keycloak URL is insecure and should only be used for development"
            )
    
    # Check SSL settings
    if config.ssl_enabled:
        if config.ssl_cert_file and not Path(config.ssl_cert_file).exists():
            validation["valid"] = False
            validation["issues"].append(f"SSL certificate file not found: {config.ssl_cert_file}")
        
        if config.ssl_key_file and not Path(config.ssl_key_file).exists():
            validation["valid"] = False
            validation["issues"].append(f"SSL key file not found: {config.ssl_key_file}")
    
    # Check JWKS file
    if config.jwks_file and not Path(config.jwks_file).exists():
        validation["warnings"].append(f"JWKS file not found: {config.jwks_file}")
    
    # Check for insecure settings
    if config.ssl_verify is False:
        validation["security_concerns"].append(
            "SSL verification is disabled (ssl_verify=False) which is insecure"
        )
    
    # Development mode warnings
    if config.development_mode and not config.mock_mode:
        validation["warnings"].append(
            "Development mode is enabled, which may use insecure defaults"
        )
    
    # Mock mode warnings
    if config.mock_mode:
        validation["warnings"].append(
            "Mock mode is enabled, which simulates Keycloak without a real server"
        )
    
    # If there are security concerns but we're in development/mock mode, convert to warnings
    if config.development_mode or config.mock_mode:
        validation["warnings"].extend(validation["security_concerns"])
        validation["security_concerns"] = []
    else:
        # In production mode, security concerns are issues
        validation["valid"] = validation["valid"] and not validation["security_concerns"]
        if validation["security_concerns"]:
            validation["issues"].extend(validation["security_concerns"])
            validation["security_concerns"] = []
    
    return validation


def check_ssl_certificate(url: str) -> Dict[str, Any]:
    """
    Check the SSL certificate of a URL.
    
    Args:
        url: URL to check
        
    Returns:
        Dict[str, Any]: Information about the certificate
    """
    if not url.startswith("https://"):
        return {"valid": False, "reason": "URL is not HTTPS"}
    
    try:
        import ssl
        import socket
        from datetime import datetime
        
        # Parse the hostname from the URL
        hostname = url.split("//")[1].split("/")[0].split(":")[0]
        
        # Create SSL context
        context = ssl.create_default_context()
        
        # Connect to the host
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssl_sock:
                # Get certificate
                cert = ssl_sock.getpeercert()
                
                # Check certificate validity
                valid_to = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
                valid_from = datetime.strptime(cert["notBefore"], "%b %d %H:%M:%S %Y %Z")
                now = datetime.now()
                
                # Get certificate issuer
                issuer = {item[0][0]: item[0][1] for item in cert["issuer"]}
                
                # Get certificate subject
                subject = {item[0][0]: item[0][1] for item in cert["subject"]}
                
                return {
                    "valid": True,
                    "issuer": issuer,
                    "subject": subject,
                    "valid_from": valid_from.isoformat(),
                    "valid_to": valid_to.isoformat(),
                    "expired": now > valid_to,
                    "not_yet_valid": now < valid_from,
                    "hostname_matches": ssl.match_hostname(cert, hostname),
                }
    except ssl.SSLError as e:
        return {"valid": False, "reason": f"SSL error: {str(e)}"}
    except socket.gaierror as e:
        return {"valid": False, "reason": f"DNS error: {str(e)}"}
    except Exception as e:
        return {"valid": False, "reason": f"Error: {str(e)}"}


def diagnose_configuration(config: KeycloakConfig) -> Dict[str, Any]:
    """
    Perform a comprehensive diagnosis of a configuration.
    
    This function checks all aspects of the configuration and
    provides detailed information about potential issues.
    
    Args:
        config: Configuration to diagnose
        
    Returns:
        Dict[str, Any]: Diagnostic information
    """
    diagnostics = {
        "valid": True,
        "issues": [],
        "warnings": [],
        "info": [],
        "environment": {},
        "checks": {},
    }
    
    # Add environment information
    diagnostics["environment"] = {
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
    }
    
    try:
        import ssl
        diagnostics["environment"]["ssl_version"] = ssl.OPENSSL_VERSION
    except ImportError:
        pass
    
    # Add configuration summary
    diagnostics["config_summary"] = {
        "keycloak_url": config.keycloak_url,
        "keycloak_realm": config.keycloak_realm,
        "client_id": config.client_id,
        "development_mode": config.development_mode,
        "mock_mode": config.mock_mode,
        "ssl_verify": config.ssl_verify,
    }
    
    # Perform validation
    validation = validate_config(config)
    diagnostics["valid"] = validation["valid"]
    diagnostics["issues"].extend(validation["issues"])
    diagnostics["warnings"].extend(validation["warnings"])
    
    # Check Keycloak URL
    if config.keycloak_url.startswith("http://") and not config.allow_http:
        diagnostics["valid"] = False
        diagnostics["issues"].append(
            "Keycloak URL uses HTTP without allow_http=True. This is insecure."
        )
    
    # Check SSL settings
    if config.ssl_enabled:
        if config.ssl_cert_file and not Path(config.ssl_cert_file).exists():
            diagnostics["valid"] = False
            diagnostics["issues"].append(
                f"SSL certificate file not found: {config.ssl_cert_file}"
            )
        
        if config.ssl_key_file and not Path(config.ssl_key_file).exists():
            diagnostics["valid"] = False
            diagnostics["issues"].append(
                f"SSL key file not found: {config.ssl_key_file}"
            )
    
    # Check JWKS file
    if config.jwks_file and not Path(config.jwks_file).exists():
        diagnostics["warnings"].append(
            f"JWKS file not found: {config.jwks_file}"
        )
    
    # Check for development mode in production
    if config.development_mode:
        diagnostics["warnings"].append(
            "Development mode is enabled. This is not recommended for production."
        )
    
    # Check for mock mode in production
    if config.mock_mode:
        diagnostics["warnings"].append(
            "Mock mode is enabled. This is not recommended for production."
        )
    
    # Check SSL verification
    if config.ssl_verify is False:
        diagnostics["warnings"].append(
            "SSL verification is disabled. This is insecure."
        )
    
    # Check SSL certificate if URL is HTTPS
    if config.keycloak_url.startswith("https://"):
        try:
            cert_info = check_ssl_certificate(config.keycloak_url)
            diagnostics["checks"]["ssl_certificate"] = cert_info
            
            if not cert_info["valid"]:
                if config.on_ssl_error == OnSSLError.RAISE:
                    diagnostics["valid"] = False
                    diagnostics["issues"].append(
                        f"SSL certificate check failed: {cert_info['reason']}"
                    )
                elif config.on_ssl_error == OnSSLError.WARN:
                    diagnostics["warnings"].append(
                        f"SSL certificate check failed: {cert_info['reason']}"
                    )
            
            if cert_info.get("expired", False):
                diagnostics["warnings"].append(
                    "SSL certificate is expired."
                )
            
            if cert_info.get("not_yet_valid", False):
                diagnostics["warnings"].append(
                    "SSL certificate is not yet valid."
                )
        except Exception as e:
            diagnostics["warnings"].append(
                f"Failed to check SSL certificate: {str(e)}"
            )
    
    # Check for advanced certificate utilities
    if not CERT_UTILS_AVAILABLE:
        diagnostics["info"].append(
            "Advanced certificate utilities are not available. "
            "This may limit the ability to diagnose SSL issues."
        )
    
    # Add recommendations based on issues
    diagnostics["recommendations"] = []
    
    if diagnostics["issues"]:
        # Provide recommendations for each issue
        for issue in diagnostics["issues"]:
            if "SSL certificate" in issue:
                diagnostics["recommendations"].append(
                    "Try setting cert_verify_mode='platform' to use certifi's CA bundle"
                )
                diagnostics["recommendations"].append(
                    "For development environments, you can use cert_verify_mode='disabled' (insecure)"
                )
                
            elif "SSL certificate file not found" in issue:
                diagnostics["recommendations"].append(
                    "Make sure the SSL certificate file exists and is accessible"
                )
                
            elif "HTTP" in issue:
                diagnostics["recommendations"].append(
                    "Use HTTPS instead of HTTP for production environments"
                )
                diagnostics["recommendations"].append(
                    "If using HTTP for development, set allow_http=True"
                )
    
    # Add general recommendations
    if config.development_mode and not diagnostics["issues"]:
        diagnostics["recommendations"].append(
            "Configuration looks good for development mode"
        )
        
    elif not config.development_mode and not diagnostics["issues"]:
        diagnostics["recommendations"].append(
            "Configuration looks good for production mode"
        )
    
    # Done with checks
    return diagnostics
