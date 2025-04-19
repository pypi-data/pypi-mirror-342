#!/usr/bin/env python3
"""
Test KeycloakAuth class initialization and methods.
"""

import pytest
from unittest.mock import MagicMock, patch
from fastapi import FastAPI
from fastapi_authlib_keycloak import KeycloakAuth


@pytest.fixture
def mock_app():
    """Create a mock FastAPI application."""
    app = FastAPI()
    app.mount = MagicMock()
    app.get = MagicMock()
    app.include_router = MagicMock()
    app.add_middleware = MagicMock()
    return app


@patch("fastapi_authlib_keycloak.keycloak_auth.setup_oauth")
@patch("fastapi_authlib_keycloak.keycloak_auth.create_validator")
@patch("fastapi_authlib_keycloak.keycloak_auth.create_auth_router")
@patch("fastapi_authlib_keycloak.keycloak_auth.setup_swagger_ui")
@patch("fastapi_authlib_keycloak.keycloak_auth.setup_ssl")
def test_keycloak_auth_init(
    mock_setup_ssl,
    mock_setup_swagger_ui,
    mock_create_auth_router,
    mock_create_validator,
    mock_setup_oauth,
    mock_app
):
    """Test KeycloakAuth initialization."""
    # Mock return values
    mock_setup_oauth.return_value = MagicMock()
    mock_create_validator.return_value = MagicMock()
    mock_create_auth_router.return_value = MagicMock()
    
    # Initialize KeycloakAuth
    auth = KeycloakAuth(
        app=mock_app,
        keycloak_url="https://example.com/auth",
        keycloak_realm="test-realm",
        client_id="test-client",
        client_secret="test-secret",
        api_base_url="https://api.example.com",
        ssl_enabled=True,
        ssl_cert_file="/path/to/cert.pem"
    )
    
    # Assert configurations were loaded correctly
    assert auth.config.keycloak_url == "https://example.com/auth"
    assert auth.config.keycloak_realm == "test-realm"
    assert auth.config.client_id == "test-client"
    assert auth.config.client_secret == "test-secret"
    assert auth.config.api_base_url == "https://api.example.com"
    assert auth.config.ssl_enabled is True
    assert auth.config.ssl_cert_file == "/path/to/cert.pem"
    
    # Assert methods were called
    mock_setup_ssl.assert_called_once()
    mock_app.add_middleware.assert_called()
    mock_setup_oauth.assert_called_once()
    mock_create_validator.assert_called_once()
    mock_create_auth_router.assert_called_once()
    mock_app.include_router.assert_called_once()
    mock_setup_swagger_ui.assert_called_once()


@patch("fastapi_authlib_keycloak.keycloak_auth.setup_oauth")
@patch("fastapi_authlib_keycloak.keycloak_auth.create_validator")
@patch("fastapi_authlib_keycloak.keycloak_auth.create_auth_router")
@patch("fastapi_authlib_keycloak.keycloak_auth.setup_swagger_ui")
def test_keycloak_auth_without_ssl(
    mock_setup_swagger_ui,
    mock_create_auth_router,
    mock_create_validator,
    mock_setup_oauth,
    mock_app
):
    """Test KeycloakAuth initialization without SSL."""
    # Mock return values
    mock_setup_oauth.return_value = MagicMock()
    mock_create_validator.return_value = MagicMock()
    mock_create_auth_router.return_value = MagicMock()
    
    # Initialize KeycloakAuth without SSL
    auth = KeycloakAuth(
        app=mock_app,
        keycloak_url="https://example.com/auth",
        keycloak_realm="test-realm",
        client_id="test-client",
        client_secret="test-secret",
        ssl_enabled=False
    )
    
    # Assert SSL setup was not called (would need to use a different approach with patch)
    assert auth.config.ssl_enabled is False


@patch("fastapi_authlib_keycloak.keycloak_auth.load_config_from_env")
@patch("fastapi_authlib_keycloak.keycloak_auth.setup_oauth")
@patch("fastapi_authlib_keycloak.keycloak_auth.create_validator")
@patch("fastapi_authlib_keycloak.keycloak_auth.create_auth_router")
@patch("fastapi_authlib_keycloak.keycloak_auth.setup_swagger_ui")
def test_keycloak_auth_from_env(
    mock_setup_swagger_ui,
    mock_create_auth_router,
    mock_create_validator,
    mock_setup_oauth,
    mock_load_config,
    mock_app
):
    """Test KeycloakAuth initialization with environment variables."""
    # Mock return values
    mock_setup_oauth.return_value = MagicMock()
    mock_create_validator.return_value = MagicMock()
    mock_create_auth_router.return_value = MagicMock()
    mock_load_config.return_value = {
        "keycloak_url": "https://env.example.com/auth",
        "keycloak_realm": "env-realm",
        "client_id": "env-client",
        "client_secret": "env-secret"
    }
    
    # Initialize KeycloakAuth with environment variables
    auth = KeycloakAuth(
        app=mock_app,
        load_from_env=True
    )
    
    # Assert environment configurations were loaded
    assert auth.config.keycloak_url == "https://env.example.com/auth"
    assert auth.config.keycloak_realm == "env-realm"
    assert auth.config.client_id == "env-client"
    assert auth.config.client_secret == "env-secret"
    
    # Assert methods were called
    mock_load_config.assert_called_once()
