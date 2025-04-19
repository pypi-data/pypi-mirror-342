#!/usr/bin/env python3
"""
Integration tests for KeycloakAuth rate limiting features.
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock

from fastapi import FastAPI, Depends, HTTPException
from fastapi.testclient import TestClient

from fastapi_authlib_keycloak import KeycloakAuth


@pytest.fixture
def mock_validator():
    """Fixture providing a mock token validator."""
    mock = AsyncMock()
    # Mock validate_token method to return a valid token
    mock.validate_token.return_value = {
        "sub": "user-123",
        "preferred_username": "testuser",
        "email": "test@example.com",
        "name": "Test User",
        "realm_access": {"roles": ["user"]},
        "resource_access": {
            "test-client": {"roles": ["api-user"]}
        }
    }
    return mock


@pytest.fixture
def mock_oauth():
    """Fixture providing a mock OAuth client."""
    return MagicMock()


@pytest.fixture
def app_with_rate_limiting():
    """Fixture providing a FastAPI app with rate limiting enabled."""
    app = FastAPI()
    
    # Use patches to avoid actual Keycloak connection
    with patch("fastapi_authlib_keycloak.keycloak_auth.setup_oauth"), \
         patch("fastapi_authlib_keycloak.keycloak_auth.create_enhanced_validator"), \
         patch("fastapi_authlib_keycloak.keycloak_auth.create_auth_router"), \
         patch("fastapi_authlib_keycloak.keycloak_auth.setup_swagger_ui"), \
         patch("fastapi_authlib_keycloak.keycloak_auth.setup_ssl"), \
         patch("fastapi_authlib_keycloak.utils.rate_limit.InMemoryStorage"), \
         patch("fastapi_authlib_keycloak.keycloak_auth.RATE_LIMIT_AVAILABLE", True):
        
        # Create KeycloakAuth instance with rate limiting enabled
        auth = KeycloakAuth(
            app=app,
            keycloak_url="http://localhost:8080/auth",
            keycloak_realm="test",
            client_id="test-client",
            client_secret="test-secret",
            development_mode=True,
            rate_limit_enabled=True,
            rate_limit_max_requests=3,  # Low limit for testing
            rate_limit_window_seconds=60,
            rate_limit_strategy="fixed"
        )
        
        # Mock the validator and OAuth client
        auth.validator = mock_validator()
        auth.oauth = mock_oauth()
        
        # Add test endpoints
        @app.get("/api/public")
        def public_endpoint():
            return {"message": "Public endpoint"}
        
        @app.get("/api/protected")
        def protected_endpoint(user = Depends(auth.get_current_user)):
            return {"message": f"Hello, {user.preferred_username}!"}
        
        @app.get("/api/rate-limited")
        def rate_limited_endpoint(
            user = Depends(auth.get_current_user),
            _rate_limit = Depends(auth.rate_limit)
        ):
            return {"message": f"Rate-limited endpoint for {user.preferred_username}"}
            
        yield app


@pytest.fixture
def test_client(app_with_rate_limiting):
    """Fixture providing a test client."""
    with TestClient(app_with_rate_limiting) as client:
        yield client


def test_rate_limiting_decorator(test_client):
    """Test that the rate_limit dependency works when applied to routes."""
    # First set of requests should succeed (up to the limit)
    for _ in range(3):
        response = test_client.get(
            "/api/rate-limited",
            headers={"Authorization": "Bearer test-token"}
        )
        assert response.status_code == 200
        assert "Rate-limited endpoint" in response.json()["message"]
        assert "X-RateLimit-Remaining" in response.headers
    
    # Request exceeding the limit should be rejected
    response = test_client.get(
        "/api/rate-limited",
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 429
    assert "Retry-After" in response.headers


def test_non_rate_limited_endpoints(test_client):
    """Test that endpoints without rate limiting don't have limits applied."""
    # We should be able to call this endpoint many times without hitting limits
    for _ in range(10):
        response = test_client.get(
            "/api/protected",
            headers={"Authorization": "Bearer test-token"}
        )
        assert response.status_code == 200
        assert "X-RateLimit-Remaining" not in response.headers


def test_public_endpoint_not_affected(test_client):
    """Test that public endpoints are not affected by rate limiting."""
    for _ in range(10):
        response = test_client.get("/api/public")
        assert response.status_code == 200
        assert "X-RateLimit-Remaining" not in response.headers


@patch("fastapi_authlib_keycloak.keycloak_auth.RATE_LIMIT_AVAILABLE", False)
def test_rate_limiting_unavailable():
    """Test rate limiting configuration when module is not available."""
    app = FastAPI()
    
    # Mock the required dependencies
    with patch("fastapi_authlib_keycloak.keycloak_auth.setup_oauth"), \
         patch("fastapi_authlib_keycloak.keycloak_auth.create_enhanced_validator"), \
         patch("fastapi_authlib_keycloak.keycloak_auth.create_auth_router"), \
         patch("fastapi_authlib_keycloak.keycloak_auth.setup_swagger_ui"), \
         patch("fastapi_authlib_keycloak.keycloak_auth.setup_ssl"):
        
        # Create KeycloakAuth instance with rate limiting enabled but module unavailable
        auth = KeycloakAuth(
            app=app,
            keycloak_url="http://localhost:8080/auth",
            keycloak_realm="test",
            client_id="test-client",
            client_secret="test-secret",
            development_mode=True,
            rate_limit_enabled=True
        )
        
        # Rate limit dependency should not be available
        assert auth.rate_limit is None


def test_different_rate_limit_strategies():
    """Test that different rate limit strategies can be configured."""
    app = FastAPI()
    
    # Mock the required dependencies
    with patch("fastapi_authlib_keycloak.keycloak_auth.setup_oauth"), \
         patch("fastapi_authlib_keycloak.keycloak_auth.create_enhanced_validator"), \
         patch("fastapi_authlib_keycloak.keycloak_auth.create_auth_router"), \
         patch("fastapi_authlib_keycloak.keycloak_auth.setup_swagger_ui"), \
         patch("fastapi_authlib_keycloak.keycloak_auth.setup_ssl"), \
         patch("fastapi_authlib_keycloak.utils.rate_limit.InMemoryStorage"), \
         patch("fastapi_authlib_keycloak.keycloak_auth.RATE_LIMIT_AVAILABLE", True) as mock_available, \
         patch("fastapi_authlib_keycloak.utils.rate_limit.FixedWindowStrategy") as fixed_strategy, \
         patch("fastapi_authlib_keycloak.utils.rate_limit.SlidingWindowStrategy") as sliding_strategy, \
         patch("fastapi_authlib_keycloak.utils.rate_limit.TokenBucketStrategy") as token_strategy:
        
        # Test fixed window strategy
        auth_fixed = KeycloakAuth(
            app=app,
            keycloak_url="http://localhost:8080/auth",
            keycloak_realm="test",
            client_id="test-client",
            client_secret="test-secret",
            rate_limit_enabled=True,
            rate_limit_strategy="fixed"
        )
        
        # Test sliding window strategy
        auth_sliding = KeycloakAuth(
            app=app,
            keycloak_url="http://localhost:8080/auth",
            keycloak_realm="test",
            client_id="test-client",
            client_secret="test-secret",
            rate_limit_enabled=True,
            rate_limit_strategy="sliding"
        )
        
        # Test token bucket strategy
        auth_token = KeycloakAuth(
            app=app,
            keycloak_url="http://localhost:8080/auth",
            keycloak_realm="test",
            client_id="test-client",
            client_secret="test-secret",
            rate_limit_enabled=True,
            rate_limit_strategy="token_bucket"
        )
        
        # Verify that the correct strategies were selected
        assert fixed_strategy.called
        assert sliding_strategy.called
        assert token_strategy.called
