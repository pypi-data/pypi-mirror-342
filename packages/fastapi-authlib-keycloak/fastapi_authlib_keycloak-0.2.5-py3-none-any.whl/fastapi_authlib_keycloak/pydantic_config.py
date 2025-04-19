#!/usr/bin/env python3
"""
Enhanced Pydantic-based configuration module for FastAPI-Authlib-Keycloak.

This module provides a robust configuration system using Pydantic for validation,
with support for loading from environment variables, configuration files, and
programmatic settings.
"""

import os
import json
import logging
import warnings
from enum import Enum
from pathlib import Path
from typing import List, Optional, Union, Dict, Any, Literal, Set

from pydantic import (
    BaseModel, 
    Field, 
    validator, 
    root_validator, 
    AnyHttpUrl,
    SecretStr,
    DirectoryPath,
    FilePath,
    ValidationError,
    parse_obj_as
)

# Check Pydantic version without using pkg_resources
import pydantic
pydantic_v2 = hasattr(pydantic, "__version__") and pydantic.__version__.startswith("2")


class SSLErrorHandling(str, Enum):
    """Enumeration for SSL error handling options."""
    RAISE = "raise"
    WARN = "warn"
    IGNORE = "ignore"


class SameSitePolicy(str, Enum):
    """Enumeration for cookie same-site policy options."""
    LAX = "lax"
    STRICT = "strict"
    NONE = "none"


class KeycloakSettings(BaseModel):
    """Keycloak server connection settings."""
    url: str = Field(
        default="",
        description="URL of the Keycloak server (e.g., https://keycloak.example.com/auth)"
    )
    realm: str = Field(
        default="",
        description="Keycloak realm name"
    )

    @validator("url")
    def validate_url(cls, v, values):
        """Validate that the URL is properly formatted."""
        if not v:
            return v
            
        # Add protocol if missing
        if not v.startswith(("http://", "https://")):
            v = f"https://{v}"
            
        # Remove trailing slash if present
        if v.endswith("/"):
            v = v[:-1]
            
        return v


class ClientSettings(BaseModel):
    """OAuth client settings."""
    client_id: str = Field(
        default="",
        description="Client ID for the UI client"
    )
    client_secret: SecretStr = Field(
        default="",
        description="Client secret for the UI client"
    )
    api_client_id: str = Field(
        default="",
        description="Client ID for the API client (if different from UI client)"
    )
    api_client_secret: SecretStr = Field(
        default="",
        description="Client secret for the API client"
    )
    api_base_url: str = Field(
        default="",
        description="Base URL for the API (defaults to request base URL if not provided)"
    )

    @validator("api_client_id", "api_client_secret")
    def set_api_defaults(cls, v, values, **kwargs):
        """Set API client defaults from UI client if not provided."""
        field_name = kwargs.get("field")
        
        if not v and field_name == "api_client_id" and "client_id" in values:
            return values["client_id"]
            
        if not v and field_name == "api_client_secret" and "client_secret" in values:
            return values["client_secret"]
            
        return v


class SessionSettings(BaseModel):
    """Session configuration settings."""
    secret: SecretStr = Field(
        default="",
        description="Secret key for session encryption"
    )
    max_age: int = Field(
        default=3600,
        description="Maximum session age in seconds",
        gt=0
    )
    https_only: bool = Field(
        default=False,
        description="Whether session cookies should be HTTPS only"
    )
    same_site: SameSitePolicy = Field(
        default=SameSitePolicy.LAX,
        description="Same-site policy for cookies (lax, strict, none)"
    )


class CORSSettings(BaseModel):
    """CORS configuration settings."""
    origins: List[str] = Field(
        default=["*"],
        description="List of allowed CORS origins"
    )
    credentials: bool = Field(
        default=True,
        description="Whether to allow credentials in CORS"
    )


class SecuritySettings(BaseModel):
    """Security-related configuration."""
    token_algorithm: str = Field(
        default="RS256",
        description="Algorithm used for JWT token signing"
    )
    strict_client_check: bool = Field(
        default=False,
        description="Whether to strictly enforce client ID matching"
    )


class SSLSettings(BaseModel):
    """SSL verification configuration."""
    enabled: bool = Field(
        default=False,
        description="Whether SSL verification is enabled"
    )
    cert_file: Optional[str] = Field(
        default=None,
        description="Path to SSL certificate file"
    )
    key_file: Optional[str] = Field(
        default=None,
        description="Path to SSL key file"
    )
    verify: Union[bool, str] = Field(
        default=True,
        description="SSL verification mode (True for standard verification, "
                   "False to disable verification, or path to certificate)"
    )
    on_error: SSLErrorHandling = Field(
        default=SSLErrorHandling.RAISE,
        description="How to handle SSL errors ('raise', 'warn', or 'ignore')"
    )
    
    @validator("cert_file", "key_file")
    def check_file_exists(cls, v):
        """Check if specified files exist."""
        if v and not os.path.isfile(v):
            warnings.warn(f"File not found: {v}")
        return v

    @root_validator(skip_on_failure=True)
    def check_ssl_settings(cls, values):
        """Validate SSL settings combinations."""
        enabled = values.get("enabled", False)
        verify = values.get("verify", True)
        cert_file = values.get("cert_file")
        
        # If SSL is enabled but verification is disabled, warn about security implications
        if enabled and verify is False:
            warnings.warn(
                "SSL verification is DISABLED. This is insecure and should only be used "
                "in development environments."
            )
            
        # If SSL is enabled but no certificate file is provided, warn about potential issues
        if enabled and not cert_file and isinstance(verify, bool) and verify:
            warnings.warn(
                "SSL verification is enabled but no certificate file was provided. "
                "This may cause issues if the Keycloak server uses a self-signed certificate."
            )
        
        return values


class JWKSSettings(BaseModel):
    """JSON Web Key Set (JWKS) configuration."""
    cache_ttl: int = Field(
        default=3600,
        description="Cache time for JWKS in seconds",
        gt=0
    )
    file: Optional[str] = Field(
        default=None,
        description="Path to a local JWKS file for offline verification"
    )
    retry_max: int = Field(
        default=3,
        description="Maximum number of retry attempts for JWKS fetching",
        ge=0
    )
    retry_backoff: float = Field(
        default=1.5,
        description="Backoff factor for retry attempts",
        ge=1.0
    )
    max_keys: int = Field(
        default=10,
        description="Maximum number of keys to store in the cache",
        gt=0
    )
    
    @validator("file")
    def check_jwks_file(cls, v):
        """Check if the JWKS file exists."""
        if v and not os.path.isfile(v):
            warnings.warn(f"JWKS file not found: {v}")
        return v


class DevelopmentSettings(BaseModel):
    """Development environment configuration."""
    mode: bool = Field(
        default=False,
        description="Enable development-friendly defaults"
    )
    allow_http: bool = Field(
        default=False,
        description="Allow HTTP for Keycloak URL (insecure, for development only)"
    )
    debug_endpoints: bool = Field(
        default=False,
        description="Enable debug endpoints"
    )
    mock_auth: bool = Field(
        default=False,
        description="Enable mock authentication (for testing only)"
    )
    log_level: str = Field(
        default="INFO",
        description="Logging level for development mode"
    )
    
    @root_validator(skip_on_failure=True)
    def check_development_settings(cls, values):
        """Validate development settings combinations."""
        dev_mode = values.get("mode", False)
        allow_http = values.get("allow_http", False)
        debug_endpoints = values.get("debug_endpoints", False)
        mock_auth = values.get("mock_auth", False)
        
        # If HTTP is allowed but not in development mode, warn about security implications
        if allow_http and not dev_mode:
            warnings.warn(
                "HTTP is allowed for Keycloak URL but development_mode is False. "
                "Using HTTP in production is highly insecure. "
                "Please enable development_mode if this is a development environment, "
                "or disable allow_http for production."
            )
        
        # If mock auth is enabled, warn about security implications
        if mock_auth:
            warnings.warn(
                "Mock authentication is enabled. This should NEVER be used in production "
                "as it bypasses actual authentication."
            )
            
        # If debug endpoints are enabled, warn about security implications
        if debug_endpoints and not dev_mode:
            warnings.warn(
                "Debug endpoints are enabled but development_mode is False. "
                "Debug endpoints may expose sensitive information and should not "
                "be enabled in production."
            )
        
        return values


class ObservabilitySettings(BaseModel):
    """Observability and monitoring configuration."""
    metrics_enabled: bool = Field(
        default=False,
        description="Enable metrics collection"
    )
    metrics_route: str = Field(
        default="/metrics",
        description="Route for metrics endpoint"
    )
    health_route: str = Field(
        default="/health/keycloak",
        description="Route for health check endpoint"
    )
    log_level: str = Field(
        default="INFO",
        description="Default logging level"
    )
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format string"
    )
    tracing_enabled: bool = Field(
        default=False,
        description="Enable distributed tracing"
    )


class RateLimitSettings(BaseModel):
    """Rate limiting configuration to prevent abuse."""
    enabled: bool = Field(
        default=False,
        description="Enable rate limiting"
    )
    max_requests: int = Field(
        default=100,
        description="Maximum number of requests per window",
        gt=0
    )
    window_seconds: int = Field(
        default=60,
        description="Time window for rate limiting in seconds",
        gt=0
    )
    strategy: Literal["fixed", "sliding", "token_bucket"] = Field(
        default="sliding",
        description="Rate limiting strategy"
    )


class SwaggerSettings(BaseModel):
    """Swagger UI customization settings."""
    title: Optional[str] = Field(
        default=None,
        description="Custom title for Swagger UI"
    )
    css_path: Optional[str] = Field(
        default=None,
        description="Path to custom CSS file for Swagger UI"
    )
    oauth_realm: Optional[str] = Field(
        default=None,
        description="OAuth realm name to use in Swagger UI (defaults to config realm)"
    )


class KeycloakAuthConfig(BaseModel):
    """
    Complete configuration model for FastAPI-Authlib-Keycloak integration.
    
    This model provides comprehensive validation for all configuration settings
    and ensures type safety throughout the application.
    """
    keycloak: KeycloakSettings = Field(default_factory=KeycloakSettings)
    client: ClientSettings = Field(default_factory=ClientSettings)
    session: SessionSettings = Field(default_factory=SessionSettings)
    cors: CORSSettings = Field(default_factory=CORSSettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    ssl: SSLSettings = Field(default_factory=SSLSettings)
    jwks: JWKSSettings = Field(default_factory=JWKSSettings)
    development: DevelopmentSettings = Field(default_factory=DevelopmentSettings)
    observability: ObservabilitySettings = Field(default_factory=ObservabilitySettings)
    rate_limit: RateLimitSettings = Field(default_factory=RateLimitSettings)
    swagger: SwaggerSettings = Field(default_factory=SwaggerSettings)
    
    class Config:
        """Pydantic configuration."""
        validate_assignment = True
        extra = "ignore"
        json_encoders = {
            SecretStr: lambda v: v.get_secret_value() if v else ""
        }
    
    @root_validator(skip_on_failure=True)
    def check_production_security(cls, values):
        """Validate security settings for production environments."""
        # Extract nested settings
        dev_settings = values.get("development", DevelopmentSettings())
        ssl_settings = values.get("ssl", SSLSettings())
        keycloak_settings = values.get("keycloak", KeycloakSettings())
        
        # Skip validation in development mode
        if dev_settings.mode:
            return values
            
        # In production mode, perform strict security checks
        if keycloak_settings.url and keycloak_settings.url.startswith("http://"):
            warnings.warn(
                "Using HTTP for Keycloak URL in production is highly insecure. "
                "Please use HTTPS instead or enable development mode if this is "
                "a development environment."
            )
        
        # Check SSL settings in production
        if ssl_settings.enabled and ssl_settings.verify is False:
            warnings.warn(
                "SSL verification is disabled in production. This is highly insecure. "
                "Please enable SSL verification for production use."
            )
            
        return values

    @classmethod
    def from_environment(cls) -> "KeycloakAuthConfig":
        """
        Create a configuration instance from environment variables.
        
        Environment variables should be prefixed with 'KEYCLOAK_' and use uppercase
        with underscores, e.g., KEYCLOAK_SSL_ENABLED for ssl.enabled.
        
        Returns:
            KeycloakAuthConfig: Configuration instance
        """
        # Define mapping of environment prefixes to config sections
        section_prefixes = {
            "": "keycloak",  # Default section for unprefixed vars
            "CLIENT_": "client",
            "SESSION_": "session",
            "CORS_": "cors",
            "SECURITY_": "security",
            "SSL_": "ssl",
            "JWKS_": "jwks",
            "DEV_": "development",
            "OBS_": "observability",
            "RATE_": "rate_limit",
            "SWAGGER_": "swagger"
        }
        
        # Special case environment variables that don't follow the pattern
        special_case_mappings = {
            "KEYCLOAK_URL": ("keycloak", "url"),
            "KEYCLOAK_REALM": ("keycloak", "realm"),
            "CLIENT_ID": ("client", "client_id"),
            "CLIENT_SECRET": ("client", "client_secret"),
            "API_CLIENT_ID": ("client", "api_client_id"),
            "API_CLIENT_SECRET": ("client", "api_client_secret"),
            "API_BASE_URL": ("client", "api_base_url"),
            "SESSION_SECRET": ("session", "secret"),
            "DEVELOPMENT_MODE": ("development", "mode"),
            "DEBUG_ENDPOINTS": ("development", "debug_endpoints"),
            "ALLOW_HTTP": ("development", "allow_http"),
        }
        
        # Initialize config data by section
        config_data = {
            "keycloak": {},
            "client": {},
            "session": {},
            "cors": {},
            "security": {},
            "ssl": {},
            "jwks": {},
            "development": {},
            "observability": {},
            "rate_limit": {},
            "swagger": {}
        }
        
        # Process all environment variables
        for env_name, env_value in os.environ.items():
            if env_name.startswith("KEYCLOAK_") or env_name in special_case_mappings:
                # Handle special case mappings first
                if env_name in special_case_mappings:
                    section, key = special_case_mappings[env_name]
                    config_data[section][key] = cls._convert_env_value(env_value, key)
                    continue
                
                # Remove KEYCLOAK_ prefix
                name_without_prefix = env_name[9:]
                
                # Determine which section this belongs to
                section = None
                key = None
                
                for prefix, section_name in section_prefixes.items():
                    if name_without_prefix.startswith(prefix):
                        section = section_name
                        # Convert remaining part to snake_case
                        key = name_without_prefix[len(prefix):].lower()
                        break
                
                if section and key:
                    config_data[section][key] = cls._convert_env_value(env_value, key)
        
        # Create a config instance
        try:
            return cls(**config_data)
        except ValidationError as e:
            # Log validation errors but return a default config
            logging.error(f"Configuration validation error: {e}")
            return cls()
    
    @classmethod
    def _convert_env_value(cls, value: str, key: str) -> Any:
        """
        Convert environment variable string value to appropriate type.
        
        Args:
            value: String value from environment variable
            key: Configuration key name (used to infer type)
            
        Returns:
            Any: Converted value
        """
        # Boolean values
        if key.endswith(("enabled", "mode", "https_only", "credentials", 
                       "strict_client_check", "allow_http", "debug_endpoints",
                       "mock_auth", "tracing_enabled")):
            return value.lower() in ("true", "1", "yes", "y", "on")
            
        # Integer values
        if key.endswith(("max_age", "cache_ttl", "retry_max", "max_keys", 
                       "max_requests", "window_seconds", "port")):
            try:
                return int(value)
            except ValueError:
                return 0
                
        # Float values
        if key.endswith(("retry_backoff",)):
            try:
                return float(value)
            except ValueError:
                return 0.0
                
        # List values
        if key == "origins":
            return [s.strip() for s in value.split(",")]
            
        # Special handling for SSL verify which can be bool or string
        if key == "verify":
            if value.lower() in ("true", "1", "yes", "y", "on"):
                return True
            if value.lower() in ("false", "0", "no", "n", "off"):
                return False
            return value  # Assume it's a path if not a boolean
            
        # Default to string
        return value
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "KeycloakAuthConfig":
        """
        Create a configuration instance from a dictionary.
        
        Args:
            config_dict: Dictionary of configuration values
            
        Returns:
            KeycloakAuthConfig: Configuration instance
        """
        try:
            return cls(**config_dict)
        except ValidationError as e:
            # Log validation errors but return a default config
            logging.error(f"Configuration validation error: {e}")
            return cls()
    
    @classmethod
    def from_json(cls, json_path: Union[str, Path]) -> "KeycloakAuthConfig":
        """
        Load configuration from a JSON file.
        
        Args:
            json_path: Path to JSON configuration file
            
        Returns:
            KeycloakAuthConfig: Configuration instance
        """
        try:
            with open(json_path, "r") as f:
                config_data = json.load(f)
                return cls.from_dict(config_data)
        except Exception as e:
            logging.error(f"Error loading configuration from {json_path}: {e}")
            return cls()
    
    @classmethod
    def from_yaml(cls, yaml_path: Union[str, Path]) -> "KeycloakAuthConfig":
        """
        Load configuration from a YAML file.
        
        Args:
            yaml_path: Path to YAML configuration file
            
        Returns:
            KeycloakAuthConfig: Configuration instance
        """
        try:
            import yaml
            with open(yaml_path, "r") as f:
                config_data = yaml.safe_load(f)
                return cls.from_dict(config_data)
        except ImportError:
            logging.error("PyYAML is not installed. Install it with 'pip install pyyaml'")
            return cls()
        except Exception as e:
            logging.error(f"Error loading configuration from {yaml_path}: {e}")
            return cls()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to a dictionary.
        
        Returns:
            Dict[str, Any]: Dictionary representation of configuration
        """
        return json.loads(self.json(by_alias=True))
    
    def to_json(self, json_path: Union[str, Path]) -> bool:
        """
        Save configuration to a JSON file.
        
        Args:
            json_path: Path to JSON configuration file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(json_path, "w") as f:
                f.write(self.json(indent=2, by_alias=True))
            return True
        except Exception as e:
            logging.error(f"Error saving configuration to {json_path}: {e}")
            return False
    
    def to_yaml(self, yaml_path: Union[str, Path]) -> bool:
        """
        Save configuration to a YAML file.
        
        Args:
            yaml_path: Path to YAML configuration file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            import yaml
            with open(yaml_path, "w") as f:
                yaml.dump(self.to_dict(), f, default_flow_style=False)
            return True
        except ImportError:
            logging.error("PyYAML is not installed. Install it with 'pip install pyyaml'")
            return False
        except Exception as e:
            logging.error(f"Error saving configuration to {yaml_path}: {e}")
            return False
    
    def get_legacy_config(self) -> "Config":
        """
        Convert to legacy Config object for backward compatibility.
        
        Returns:
            Config: Legacy configuration object
        """
        from fastapi_authlib_keycloak.config import Config
        
        legacy_config = Config()
        
        # Map fields from this config to legacy config
        legacy_config.keycloak_url = self.keycloak.url
        legacy_config.keycloak_realm = self.keycloak.realm
        
        legacy_config.client_id = self.client.client_id
        legacy_config.client_secret = self.client.client_secret.get_secret_value() if self.client.client_secret else ""
        legacy_config.api_client_id = self.client.api_client_id
        legacy_config.api_client_secret = self.client.api_client_secret.get_secret_value() if self.client.api_client_secret else ""
        legacy_config.api_base_url = self.client.api_base_url
        
        legacy_config.session_secret = self.session.secret.get_secret_value() if self.session.secret else ""
        legacy_config.session_max_age = self.session.max_age
        legacy_config.session_https_only = self.session.https_only
        legacy_config.session_same_site = self.session.same_site.value
        
        legacy_config.cors_origins = self.cors.origins
        legacy_config.cors_credentials = self.cors.credentials
        
        legacy_config.token_algorithm = self.security.token_algorithm
        legacy_config.strict_client_check = self.security.strict_client_check
        
        legacy_config.ssl_enabled = self.ssl.enabled
        legacy_config.ssl_cert_file = self.ssl.cert_file or ""
        legacy_config.ssl_key_file = self.ssl.key_file or ""
        legacy_config.ssl_verify = self.ssl.verify
        
        legacy_config.development_mode = self.development.mode
        legacy_config.allow_http = self.development.allow_http
        legacy_config.jwks_cache_ttl = self.jwks.cache_ttl
        legacy_config.jwks_file = self.jwks.file
        legacy_config.on_ssl_error = self.ssl.on_error.value
        
        legacy_config.custom_swagger_title = self.swagger.title
        legacy_config.custom_swagger_css = self.swagger.css_path
        
        legacy_config.debug_endpoints_enabled = self.development.debug_endpoints
        
        return legacy_config
