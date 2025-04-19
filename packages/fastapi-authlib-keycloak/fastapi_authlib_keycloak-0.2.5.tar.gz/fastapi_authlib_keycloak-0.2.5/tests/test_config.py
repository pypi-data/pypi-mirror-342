#!/usr/bin/env python3
"""
Test configuration loading and validation.
"""

import os
import pytest
from fastapi_authlib_keycloak.config import Config, load_config_from_env


def test_config_defaults():
    """Test default configuration values."""
    config = Config()
    
    # Check default values
    assert config.keycloak_url == ""
    assert config.keycloak_realm == ""
    assert config.client_id == ""
    assert config.client_secret == ""
    assert config.session_max_age == 3600
    assert config.session_https_only is False
    assert config.session_same_site == "lax"
    assert config.cors_origins == ["*"]
    assert config.cors_credentials is True
    assert config.ssl_enabled is False


def test_config_update():
    """Test updating configuration values."""
    config = Config()
    
    # Update with dictionary
    config.update({
        "keycloak_url": "https://example.com/auth",
        "keycloak_realm": "test-realm",
        "client_id": "test-client",
        "client_secret": "test-secret",
        "session_max_age": 7200,
        "ssl_enabled": True
    })
    
    # Check updated values
    assert config.keycloak_url == "https://example.com/auth"
    assert config.keycloak_realm == "test-realm"
    assert config.client_id == "test-client"
    assert config.client_secret == "test-secret"
    assert config.session_max_age == 7200
    assert config.ssl_enabled is True
    
    # Check that non-updated values retain defaults
    assert config.session_https_only is False
    assert config.session_same_site == "lax"
    assert config.cors_origins == ["*"]
    assert config.cors_credentials is True


def test_load_config_from_env(monkeypatch):
    """Test loading configuration from environment variables."""
    # Set environment variables
    monkeypatch.setenv("KEYCLOAK_URL", "https://env.example.com/auth")
    monkeypatch.setenv("KEYCLOAK_REALM", "env-realm")
    monkeypatch.setenv("CLIENT_ID", "env-client")
    monkeypatch.setenv("CLIENT_SECRET", "env-secret")
    monkeypatch.setenv("SESSION_MAX_AGE", "1800")
    monkeypatch.setenv("SSL_ENABLED", "true")
    monkeypatch.setenv("CORS_ORIGINS", "https://example.com,https://app.example.com")
    
    # Load from environment
    config_values = load_config_from_env()
    
    # Check loaded values
    assert config_values["keycloak_url"] == "https://env.example.com/auth"
    assert config_values["keycloak_realm"] == "env-realm"
    assert config_values["client_id"] == "env-client"
    assert config_values["client_secret"] == "env-secret"
    assert config_values["session_max_age"] == 1800
    assert config_values["ssl_enabled"] is True
    assert config_values["cors_origins"] == ["https://example.com", "https://app.example.com"]
    
    # Create Config and update with values
    config = Config()
    config.update(config_values)
    
    # Check final config
    assert config.keycloak_url == "https://env.example.com/auth"
    assert config.keycloak_realm == "env-realm"
    assert config.client_id == "env-client"
    assert config.client_secret == "env-secret"
    assert config.session_max_age == 1800
    assert config.ssl_enabled is True
    assert config.cors_origins == ["https://example.com", "https://app.example.com"]
