"""
Mock utilities for FastAPI-Authlib-Keycloak development and testing.

This module provides tools for mocking Keycloak authentication
without requiring a real Keycloak server, useful for development
and testing environments.
"""

import os
import json
import time
import logging
import uuid
import jwt
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

# Default mock user data
DEFAULT_MOCK_USER = {
    "sub": "mock-user-id",
    "preferred_username": "mock-user",
    "email": "mock-user@example.com",
    "name": "Mock User",
    "given_name": "Mock",
    "family_name": "User",
    "realm_access": {
        "roles": ["user"]
    },
    "resource_access": {
        "account": {
            "roles": ["manage-account"]
        }
    }
}

DEFAULT_MOCK_ADMIN = {
    "sub": "mock-admin-id",
    "preferred_username": "mock-admin",
    "email": "mock-admin@example.com",
    "name": "Mock Admin",
    "given_name": "Mock",
    "family_name": "Admin",
    "realm_access": {
        "roles": ["user", "admin"]
    },
    "resource_access": {
        "account": {
            "roles": ["manage-account"]
        }
    }
}

# Secret key for mock token signing
DEFAULT_SECRET = "mock-secret-key-do-not-use-in-production"


class MockKeycloakService:
    """
    Mock Keycloak service for development and testing.
    
    This class provides mock implementations of Keycloak's authentication
    and authorization features without requiring a real Keycloak server.
    """
    
    def __init__(
        self, 
        keycloak_url: str,
        keycloak_realm: str,
        client_id: str,
        client_secret: str,
        mock_users: Optional[Dict[str, Any]] = None,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize the mock Keycloak service.
        
        Args:
            keycloak_url: URL of the Keycloak server (for mock issuer)
            keycloak_realm: Keycloak realm name (for mock issuer)
            client_id: Client ID (for token audience)
            client_secret: Client secret (unused, but stored for consistency)
            mock_users: Dictionary of mock users indexed by username
            logger: Logger instance
        """
        self.keycloak_url = keycloak_url
        self.keycloak_realm = keycloak_realm
        self.client_id = client_id
        self.client_secret = client_secret
        self.issuer = f"{keycloak_url}/realms/{keycloak_realm}"
        self.logger = logger or logging.getLogger("fastapi-keycloak.mock")
        
        # Initialize the mock users
        self.mock_users = {
            "mock-user": DEFAULT_MOCK_USER,
            "mock-admin": DEFAULT_MOCK_ADMIN
        }
        
        # Add custom mock users if provided
        if mock_users:
            if isinstance(mock_users, dict):
                # If it's a simple dictionary, add as a single user
                if "sub" in mock_users and "preferred_username" in mock_users:
                    username = mock_users["preferred_username"]
                    self.mock_users[username] = mock_users
                # If it's a dictionary of users indexed by username
                else:
                    for username, user_data in mock_users.items():
                        self.mock_users[username] = user_data
            elif isinstance(mock_users, list):
                # If it's a list of user dictionaries
                for user_data in mock_users:
                    if "preferred_username" in user_data:
                        username = user_data["preferred_username"]
                        self.mock_users[username] = user_data
        
        # Generate signing keys
        self.secret = os.environ.get("MOCK_JWT_SECRET", DEFAULT_SECRET)
        
        self.logger.info(f"Mock Keycloak service initialized with {len(self.mock_users)} users")
        
    def create_token(
        self, 
        username: str, 
        expires_in: int = 3600,
        include_refresh: bool = True
    ) -> Dict[str, Any]:
        """
        Create a mock JWT token for a user.
        
        Args:
            username: Username of the mock user
            expires_in: Token expiration time in seconds
            include_refresh: Whether to include a refresh token
            
        Returns:
            Dict[str, Any]: Token response data
        """
        # Check if the user exists
        if username not in self.mock_users:
            self.logger.warning(f"User {username} not found in mock users")
            raise ValueError(f"User {username} not found")
        
        # Get user data
        user_data = self.mock_users[username]
        
        # Set token metadata
        now = int(time.time())
        expires_at = now + expires_in
        
        # Create token payload
        token_data = {
            "iss": self.issuer,
            "aud": self.client_id,
            "exp": expires_at,
            "iat": now,
            "jti": str(uuid.uuid4()),
            "sub": user_data["sub"],
            "typ": "Bearer",
            "azp": self.client_id,
            "session_state": str(uuid.uuid4()),
            "acr": "1",
            "scope": "openid profile email",
            "sid": str(uuid.uuid4()),
            "email_verified": True,
            "preferred_username": user_data["preferred_username"],
            "name": user_data.get("name", f"{user_data.get('given_name', '')} {user_data.get('family_name', '')}").strip(),
            "given_name": user_data.get("given_name", ""),
            "family_name": user_data.get("family_name", ""),
            "email": user_data.get("email", f"{user_data['preferred_username']}@example.com"),
        }
        
        # Add role data if available
        if "realm_access" in user_data:
            token_data["realm_access"] = user_data["realm_access"]
        
        if "resource_access" in user_data:
            token_data["resource_access"] = user_data["resource_access"]
        
        # Add any other custom fields from user_data
        for key, value in user_data.items():
            if key not in token_data and key not in ["sub", "preferred_username"]:
                token_data[key] = value
        
        # Sign the token
        access_token = jwt.encode(token_data, self.secret, algorithm="HS256")
        
        # Create response
        response = {
            "access_token": access_token,
            "expires_in": expires_in,
            "token_type": "bearer",
            "scope": "openid profile email",
            "session_state": token_data["session_state"],
            "id_token": access_token  # For simplicity, use the same token
        }
        
        # Add refresh token if requested
        if include_refresh:
            refresh_token_data = {
                "iss": self.issuer,
                "aud": self.client_id,
                "exp": now + expires_in * 2,  # Refresh token lasts twice as long
                "iat": now,
                "jti": str(uuid.uuid4()),
                "sub": user_data["sub"],
                "typ": "Refresh",
                "azp": self.client_id,
                "session_state": token_data["session_state"],
                "scope": "openid profile email"
            }
            refresh_token = jwt.encode(refresh_token_data, self.secret, algorithm="HS256")
            response["refresh_token"] = refresh_token
            response["refresh_expires_in"] = expires_in * 2
        
        return response
    
    def validate_token(self, token: str) -> Dict[str, Any]:
        """
        Validate a mock JWT token.
        
        Args:
            token: JWT token to validate
            
        Returns:
            Dict[str, Any]: Validated token data
        
        Raises:
            ValueError: If token validation fails
        """
        try:
            # Decode the token
            token_data = jwt.decode(
                token,
                self.secret,
                algorithms=["HS256"],
                audience=self.client_id,
                issuer=self.issuer
            )
            
            # Check expiration
            now = int(time.time())
            if token_data["exp"] < now:
                raise ValueError("Token has expired")
            
            # Add validation metadata
            token_data["active"] = True
            token_data["client_id"] = self.client_id
            
            return token_data
        except jwt.ExpiredSignatureError:
            return {"active": False, "error": "token_expired"}
        except jwt.InvalidTokenError as e:
            return {"active": False, "error": f"invalid_token: {str(e)}"}
        except Exception as e:
            return {"active": False, "error": f"validation_error: {str(e)}"}
    
    def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Refresh a mock JWT token.
        
        Args:
            refresh_token: Refresh token
            
        Returns:
            Dict[str, Any]: New token response data
        
        Raises:
            ValueError: If token refresh fails
        """
        try:
            # Decode the refresh token
            token_data = jwt.decode(
                refresh_token,
                self.secret,
                algorithms=["HS256"],
                audience=self.client_id,
                issuer=self.issuer
            )
            
            # Check if it's a refresh token
            if token_data.get("typ") != "Refresh":
                raise ValueError("Not a refresh token")
            
            # Check expiration
            now = int(time.time())
            if token_data["exp"] < now:
                raise ValueError("Refresh token has expired")
            
            # Get the username
            sub = token_data["sub"]
            username = None
            for uname, user_data in self.mock_users.items():
                if user_data["sub"] == sub:
                    username = uname
                    break
            
            if not username:
                raise ValueError(f"User with sub {sub} not found")
            
            # Create a new token
            return self.create_token(username)
        except jwt.ExpiredSignatureError:
            raise ValueError("Refresh token has expired")
        except jwt.InvalidTokenError as e:
            raise ValueError(f"Invalid refresh token: {str(e)}")
        except Exception as e:
            raise ValueError(f"Token refresh failed: {str(e)}")
    
    def generate_jwks(self) -> Dict[str, Any]:
        """
        Generate a mock JWKS (JSON Web Key Set) for token validation.
        
        Returns:
            Dict[str, Any]: JWKS data
        """
        # For the mock service, we use a simple symmetric key
        # In a real implementation, this would be an asymmetric key pair
        
        # Generate a key ID
        kid = str(uuid.uuid4())
        
        return {
            "keys": [
                {
                    "kid": kid,
                    "kty": "oct",
                    "alg": "HS256",
                    "use": "sig",
                    "k": self.secret
                }
            ]
        }
    
    def get_user_info(self, token: str) -> Dict[str, Any]:
        """
        Get user info from a mock JWT token.
        
        Args:
            token: JWT token
            
        Returns:
            Dict[str, Any]: User info data
        
        Raises:
            ValueError: If token validation fails
        """
        # Validate the token
        token_data = self.validate_token(token)
        
        if not token_data.get("active", False):
            raise ValueError(f"Invalid token: {token_data.get('error', 'unknown error')}")
        
        # Extract user info fields
        user_info = {
            "sub": token_data["sub"],
            "preferred_username": token_data.get("preferred_username", ""),
            "name": token_data.get("name", ""),
            "given_name": token_data.get("given_name", ""),
            "family_name": token_data.get("family_name", ""),
            "email": token_data.get("email", ""),
            "email_verified": token_data.get("email_verified", False)
        }
        
        return user_info
    
    def introspect_token(self, token: str) -> Dict[str, Any]:
        """
        Introspect a mock JWT token.
        
        Args:
            token: JWT token to introspect
            
        Returns:
            Dict[str, Any]: Token introspection data
        """
        try:
            # Validate the token
            token_data = self.validate_token(token)
            
            # For introspection, only return a subset of token data
            return {
                "active": token_data.get("active", False),
                "exp": token_data.get("exp", 0),
                "iat": token_data.get("iat", 0),
                "aud": token_data.get("aud", self.client_id),
                "iss": token_data.get("iss", self.issuer),
                "sub": token_data.get("sub", ""),
                "username": token_data.get("preferred_username", ""),
                "client_id": self.client_id,
                "token_type": token_data.get("typ", "Bearer")
            }
        except Exception as e:
            return {"active": False, "error": str(e)}


def setup_mock_mode(
    keycloak_url: str,
    keycloak_realm: str,
    client_id: str,
    client_secret: str,
    mock_users: Optional[Dict[str, Any]] = None,
    logger: Optional[logging.Logger] = None
) -> MockKeycloakService:
    """
    Set up mock mode for development and testing.
    
    Args:
        keycloak_url: URL of the Keycloak server (for mock issuer)
        keycloak_realm: Keycloak realm name (for mock issuer)
        client_id: Client ID (for token audience)
        client_secret: Client secret (unused, but stored for consistency)
        mock_users: Dictionary of mock users indexed by username
        logger: Logger instance
        
    Returns:
        MockKeycloakService: Mock Keycloak service instance
    """
    # Create the mock service
    mock_service = MockKeycloakService(
        keycloak_url=keycloak_url,
        keycloak_realm=keycloak_realm,
        client_id=client_id,
        client_secret=client_secret,
        mock_users=mock_users,
        logger=logger
    )
    
    # Log that mock mode is enabled
    if logger:
        logger.warning(
            "Mock mode enabled. Using mock Keycloak service for development and testing. "
            "Do not use in production!"
        )
    
    return mock_service
