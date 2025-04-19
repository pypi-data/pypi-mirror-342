"""
Mock mode for FastAPI-Authlib-Keycloak.

This module provides a comprehensive mock implementation of Keycloak
for development and testing without requiring a real Keycloak server.
"""

import os
import json
import logging
import secrets
import time
from typing import Dict, List, Optional, Any, Union, Callable
from datetime import datetime, timedelta
from pathlib import Path

from fastapi import FastAPI, Request, Response, HTTPException, Depends, status
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.routing import APIRouter

# Configure logger
logger = logging.getLogger("fastapi-keycloak.mock")


class MockKeycloakService:
    """
    Mock Keycloak service for development and testing.
    
    This class provides mock implementations of Keycloak endpoints
    for OAuth flows, token validation, and user information.
    """
    
    def __init__(
        self,
        keycloak_url: str,
        keycloak_realm: str,
        client_id: str,
        client_secret: str,
        mock_users: Optional[List[Dict[str, Any]]] = None,
        token_expiration: int = 300,
        refresh_token_expiration: int = 1800,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize the mock Keycloak service.
        
        Args:
            keycloak_url: Keycloak server URL
            keycloak_realm: Keycloak realm name
            client_id: Client ID
            client_secret: Client secret
            mock_users: List of mock users (will create a default user if None)
            token_expiration: Token expiration time in seconds
            refresh_token_expiration: Refresh token expiration time in seconds
            logger: Logger instance
        """
        self.keycloak_url = keycloak_url
        self.keycloak_realm = keycloak_realm
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_expiration = token_expiration
        self.refresh_token_expiration = refresh_token_expiration
        self.logger = logger or logging.getLogger("fastapi-keycloak.mock")
        
        # Generate signing keys
        self.private_key, self.public_key, self.jwks = self._generate_keys()
        
        # Store mock tokens
        self.active_tokens = {}
        
        # Create mock users
        self.mock_users = {}
        if mock_users:
            for user in mock_users:
                user_id = user.get("sub") or secrets.token_hex(8)
                self.mock_users[user_id] = user
        
        # Create a default user if none provided
        if not self.mock_users:
            default_user_id = "mock-user-id"
            self.mock_users[default_user_id] = {
                "sub": default_user_id,
                "preferred_username": "mock-user",
                "email": "mock-user@example.com",
                "name": "Mock User",
                "realm_access": {
                    "roles": ["user"]
                }
            }
            
        self.logger.info(f"Mock Keycloak service initialized with {len(self.mock_users)} users")
    
    def _generate_keys(self) -> tuple:
        """
        Generate RSA keys for token signing.
        
        Returns:
            tuple: (private_key, public_key, jwks)
        """
        try:
            from cryptography.hazmat.primitives import serialization
            from cryptography.hazmat.primitives.asymmetric import rsa
            from cryptography.hazmat.backends import default_backend
            
            # Generate RSA key pair
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )
            
            # Get public key
            public_key = private_key.public_key()
            
            # Serialize private key
            private_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            
            # Serialize public key
            public_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            
            # Create a key ID
            kid = secrets.token_hex(8)
            
            # Create JWKS
            from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
            public_numbers = public_key.public_numbers()
            
            jwks = {
                "keys": [
                    {
                        "kid": kid,
                        "kty": "RSA",
                        "alg": "RS256",
                        "use": "sig",
                        "n": self._int_to_base64(public_numbers.n),
                        "e": self._int_to_base64(public_numbers.e),
                    }
                ]
            }
            
            # Set up JWK for PyJWT
            private_jwk = {
                "kid": kid,
                "kty": "RSA",
                "alg": "RS256",
                "use": "sig",
                "d": None  # This would be the private key parameter, but PyJWT doesn't need it
            }
            
            self.logger.info("Generated RSA key pair for token signing")
            return (private_pem, public_pem, jwks)
            
        except ImportError:
            # If cryptography is not available, use PyJWT's built-in key generation
            self.logger.warning("cryptography not installed, using PyJWT's key generation")
            
            # Generate a dummy key for PyJWT
            secret = secrets.token_hex(32)
            jwks = {
                "keys": [
                    {
                        "kid": secrets.token_hex(8),
                        "kty": "oct",
                        "alg": "HS256",
                        "use": "sig",
                        "k": secret
                    }
                ]
            }
            
            return (secret, secret, jwks)
    
    def _int_to_base64(self, value: int) -> str:
        """
        Convert an integer to base64url encoding.
        
        Args:
            value: Integer to convert
            
        Returns:
            str: Base64url encoded string
        """
        import base64
        import struct
        
        # Convert to bytes
        value_bytes = value.to_bytes((value.bit_length() + 7) // 8, byteorder='big')
        
        # Encode as base64url
        encoded = base64.urlsafe_b64encode(value_bytes).rstrip(b'=').decode('ascii')
        
        return encoded
    
    def create_token(self, user_id: str) -> Dict[str, str]:
        """
        Create a mock token for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            Dict[str, str]: Token response
        """
        if user_id not in self.mock_users:
            self.logger.warning(f"User {user_id} not found in mock users")
            raise ValueError(f"User {user_id} not found")
        
        # Get user data
        user_data = self.mock_users[user_id]
        
        # Current time
        now = int(time.time())
        
        # Create token payload
        payload = {
            "exp": now + self.token_expiration,
            "iat": now,
            "jti": secrets.token_hex(16),
            "iss": f"{self.keycloak_url}/realms/{self.keycloak_realm}",
            "aud": self.client_id,
            "sub": user_id,
            "typ": "Bearer",
            "azp": self.client_id,
            "session_state": secrets.token_hex(16),
            "acr": "1",
            "realm_access": user_data.get("realm_access", {"roles": ["user"]}),
            "resource_access": {
                self.client_id: {
                    "roles": user_data.get("realm_access", {"roles": ["user"]}).get("roles", ["user"])
                }
            },
            "scope": "openid profile email",
            "sid": secrets.token_hex(16),
            "email_verified": True,
            "preferred_username": user_data.get("preferred_username", f"user-{user_id}"),
            "email": user_data.get("email", f"user-{user_id}@example.com"),
            "name": user_data.get("name", f"User {user_id}")
        }
        
        # Add any additional user data
        for key, value in user_data.items():
            if key not in payload and key not in ["sub", "realm_access"]:
                payload[key] = value
        
        # Create refresh token with longer expiration
        refresh_payload = {
            "exp": now + self.refresh_token_expiration,
            "iat": now,
            "jti": secrets.token_hex(16),
            "iss": f"{self.keycloak_url}/realms/{self.keycloak_realm}",
            "aud": self.client_id,
            "sub": user_id,
            "typ": "Refresh",
            "azp": self.client_id,
            "session_state": payload["session_state"],
            "scope": "openid profile email"
        }
        
        # Sign tokens
        try:
            # Use PyJWT to sign tokens
            import jwt
            
            # Get the key ID
            if isinstance(self.jwks["keys"][0]["kty"], str) and self.jwks["keys"][0]["kty"] == "RSA":
                # RSA key
                algorithm = "RS256"
                kid = self.jwks["keys"][0]["kid"]
                
                # Add key ID to header
                headers = {"kid": kid}
                
                # Sign with private key
                access_token = jwt.encode(payload, self.private_key, algorithm=algorithm, headers=headers)
                refresh_token = jwt.encode(refresh_payload, self.private_key, algorithm=algorithm, headers=headers)
            else:
                # HS256 key
                algorithm = "HS256"
                access_token = jwt.encode(payload, self.private_key, algorithm=algorithm)
                refresh_token = jwt.encode(refresh_payload, self.private_key, algorithm=algorithm)
                
        except Exception as e:
            self.logger.error(f"Error signing tokens: {str(e)}")
            # Fallback to JSON representation if signing fails
            access_token = json.dumps(payload)
            refresh_token = json.dumps(refresh_payload)
        
        # Store token in active tokens
        self.active_tokens[access_token] = {
            "user_id": user_id,
            "expires_at": now + self.token_expiration,
            "payload": payload
        }
        
        self.active_tokens[refresh_token] = {
            "user_id": user_id,
            "expires_at": now + self.refresh_token_expiration,
            "payload": refresh_payload,
            "is_refresh": True
        }
        
        # Create token response
        token_response = {
            "access_token": access_token,
            "expires_in": self.token_expiration,
            "refresh_expires_in": self.refresh_token_expiration,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "id_token": access_token,  # Use same token for ID token in mock mode
            "not-before-policy": 0,
            "session_state": payload["session_state"],
            "scope": "openid profile email"
        }
        
        self.logger.info(f"Created mock token for user {user_id}")
        return token_response
    
    def validate_token(self, token: str) -> Dict[str, Any]:
        """
        Validate a mock token.
        
        Args:
            token: Token to validate
            
        Returns:
            Dict[str, Any]: Token payload if valid
            
        Raises:
            HTTPException: If token is invalid
        """
        # Remove Bearer prefix if present
        if token.startswith("Bearer "):
            token = token[7:]
        
        # Check if token is in active tokens
        if token in self.active_tokens:
            token_info = self.active_tokens[token]
            
            # Check if token is expired
            if token_info["expires_at"] < time.time():
                del self.active_tokens[token]
                self.logger.warning("Token expired")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token expired"
                )
            
            # Return token payload
            return token_info["payload"]
        
        # Try to decode the token
        try:
            # Use PyJWT to decode token
            import jwt
            
            # Get the key ID from the token header
            unverified_header = jwt.get_unverified_header(token)
            kid = unverified_header.get("kid")
            
            # Find the key
            key = None
            algorithm = None
            
            for jwk in self.jwks["keys"]:
                if jwk.get("kid") == kid:
                    # Use the key
                    if jwk["kty"] == "RSA":
                        key = self.public_key
                        algorithm = "RS256"
                    else:
                        key = self.private_key  # For HS256
                        algorithm = "HS256"
                    break
            
            # If key not found, use default
            if not key:
                key = self.private_key
                algorithm = "HS256"
            
            # Decode the token
            payload = jwt.decode(
                token,
                key,
                algorithms=[algorithm],
                audience=self.client_id,
                options={"verify_signature": True}
            )
            
            # If token is valid, add to active tokens
            self.active_tokens[token] = {
                "user_id": payload.get("sub"),
                "expires_at": payload.get("exp", 0),
                "payload": payload
            }
            
            return payload
            
        except jwt.ExpiredSignatureError:
            self.logger.warning("Token expired")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired"
            )
        except jwt.InvalidTokenError as e:
            self.logger.warning(f"Invalid token: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token: {str(e)}"
            )
        except Exception as e:
            self.logger.error(f"Token validation error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token validation error: {str(e)}"
            )
    
    def refresh_token(self, refresh_token: str) -> Dict[str, str]:
        """
        Refresh a token.
        
        Args:
            refresh_token: Refresh token
            
        Returns:
            Dict[str, str]: New token response
            
        Raises:
            HTTPException: If refresh token is invalid
        """
        # Validate refresh token
        try:
            payload = self.validate_token(refresh_token)
            
            # Check if token is a refresh token
            if payload.get("typ") != "Refresh":
                self.logger.warning("Not a refresh token")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not a refresh token"
                )
            
            # Get user ID
            user_id = payload.get("sub")
            
            # Create new token
            return self.create_token(user_id)
            
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Refresh token error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Refresh token error: {str(e)}"
            )
    
    def introspect_token(self, token: str) -> Dict[str, Any]:
        """
        Introspect a token.
        
        Args:
            token: Token to introspect
            
        Returns:
            Dict[str, Any]: Token introspection response
        """
        try:
            # Validate token
            payload = self.validate_token(token)
            
            # Create introspection response
            response = {
                "active": True,
                "exp": payload.get("exp"),
                "iat": payload.get("iat"),
                "jti": payload.get("jti"),
                "iss": payload.get("iss"),
                "aud": payload.get("aud"),
                "sub": payload.get("sub"),
                "typ": payload.get("typ"),
                "azp": payload.get("azp"),
                "session_state": payload.get("session_state"),
                "acr": payload.get("acr"),
                "realm_access": payload.get("realm_access"),
                "resource_access": payload.get("resource_access"),
                "scope": payload.get("scope"),
                "sid": payload.get("sid"),
                "email_verified": payload.get("email_verified"),
                "preferred_username": payload.get("preferred_username"),
                "email": payload.get("email"),
                "name": payload.get("name")
            }
            
            return response
            
        except HTTPException:
            # Token is invalid
            return {
                "active": False
            }
        except Exception as e:
            self.logger.error(f"Introspection error: {str(e)}")
            return {
                "active": False,
                "error": str(e)
            }
    
    def get_user_info(self, token: str) -> Dict[str, Any]:
        """
        Get user information from a token.
        
        Args:
            token: Token to get user info from
            
        Returns:
            Dict[str, Any]: User information
            
        Raises:
            HTTPException: If token is invalid
        """
        # Validate token
        payload = self.validate_token(token)
        
        # Extract user info
        user_info = {
            "sub": payload.get("sub"),
            "preferred_username": payload.get("preferred_username"),
            "email": payload.get("email"),
            "email_verified": payload.get("email_verified", True),
            "name": payload.get("name")
        }
        
        # Add any additional user data
        user_id = payload.get("sub")
        if user_id in self.mock_users:
            user_data = self.mock_users[user_id]
            for key, value in user_data.items():
                if key not in user_info and key not in ["sub", "realm_access"]:
                    user_info[key] = value
        
        return user_info
    
    def get_openid_configuration(self) -> Dict[str, Any]:
        """
        Get OpenID Connect provider configuration.
        
        Returns:
            Dict[str, Any]: OpenID configuration
        """
        base_url = f"{self.keycloak_url}/realms/{self.keycloak_realm}"
        
        return {
            "issuer": base_url,
            "authorization_endpoint": f"{base_url}/protocol/openid-connect/auth",
            "token_endpoint": f"{base_url}/protocol/openid-connect/token",
            "token_introspection_endpoint": f"{base_url}/protocol/openid-connect/token/introspect",
            "userinfo_endpoint": f"{base_url}/protocol/openid-connect/userinfo",
            "end_session_endpoint": f"{base_url}/protocol/openid-connect/logout",
            "jwks_uri": f"{base_url}/protocol/openid-connect/certs",
            "check_session_iframe": f"{base_url}/protocol/openid-connect/login-status-iframe.html",
            "grant_types_supported": [
                "authorization_code",
                "implicit",
                "refresh_token",
                "password",
                "client_credentials"
            ],
            "response_types_supported": [
                "code",
                "none",
                "id_token",
                "token",
                "id_token token",
                "code id_token",
                "code token",
                "code id_token token"
            ],
            "subject_types_supported": ["public", "pairwise"],
            "id_token_signing_alg_values_supported": ["RS256"],
            "userinfo_signing_alg_values_supported": ["RS256"],
            "request_object_signing_alg_values_supported": ["none", "RS256"],
            "response_modes_supported": ["query", "fragment", "form_post"],
            "registration_endpoint": f"{base_url}/clients-registrations/openid-connect",
            "token_endpoint_auth_methods_supported": [
                "private_key_jwt",
                "client_secret_basic",
                "client_secret_post",
                "client_secret_jwt"
            ],
            "token_endpoint_auth_signing_alg_values_supported": ["RS256"],
            "claims_supported": [
                "aud",
                "sub",
                "iss",
                "auth_time",
                "name",
                "given_name",
                "family_name",
                "preferred_username",
                "email",
                "acr"
            ],
            "claim_types_supported": ["normal"],
            "claims_parameter_supported": False,
            "scopes_supported": ["openid", "offline_access", "profile", "email", "roles", "web-origins"],
            "request_parameter_supported": True,
            "request_uri_parameter_supported": True,
            "code_challenge_methods_supported": ["plain", "S256"],
            "tls_client_certificate_bound_access_tokens": True,
            "revocation_endpoint": f"{base_url}/protocol/openid-connect/revoke"
        }
    
    def get_jwks(self) -> Dict[str, Any]:
        """
        Get JSON Web Key Set.
        
        Returns:
            Dict[str, Any]: JWKS
        """
        return self.jwks
    
    def revoke_token(self, token: str) -> None:
        """
        Revoke a token.
        
        Args:
            token: Token to revoke
        """
        # Remove token from active tokens
        if token in self.active_tokens:
            del self.active_tokens[token]
            self.logger.info("Token revoked")


def create_mock_router(service: MockKeycloakService) -> APIRouter:
    """
    Create a FastAPI router with mock Keycloak endpoints.
    
    Args:
        service: Mock Keycloak service
        
    Returns:
        APIRouter: Router with mock endpoints
    """
    # Create router
    router = APIRouter()
    
    # OpenID Configuration endpoint
    @router.get("/realms/{realm}/.well-known/openid-configuration")
    async def openid_configuration(realm: str):
        """OpenID Connect provider configuration."""
        # Validate realm
        if realm != service.keycloak_realm:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Realm {realm} not found"
            )
        
        return service.get_openid_configuration()
    
    # JWKS endpoint
    @router.get("/realms/{realm}/protocol/openid-connect/certs")
    async def jwks(realm: str):
        """JSON Web Key Set."""
        # Validate realm
        if realm != service.keycloak_realm:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Realm {realm} not found"
            )
        
        return service.get_jwks()
    
    # Token endpoint
    @router.post("/realms/{realm}/protocol/openid-connect/token")
    async def token(realm: str, request: Request):
        """Token endpoint."""
        # Validate realm
        if realm != service.keycloak_realm:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Realm {realm} not found"
            )
        
        # Get form data
        form_data = await request.form()
        grant_type = form_data.get("grant_type")
        
        # Handle different grant types
        if grant_type == "password":
            # Password grant
            username = form_data.get("username")
            password = form_data.get("password")
            
            # In mock mode, any password is valid
            # Find user by username
            user_id = None
            for uid, user in service.mock_users.items():
                if user.get("preferred_username") == username:
                    user_id = uid
                    break
            
            if not user_id:
                # Create a new mock user
                user_id = secrets.token_hex(8)
                service.mock_users[user_id] = {
                    "sub": user_id,
                    "preferred_username": username,
                    "email": f"{username}@example.com",
                    "name": username.title(),
                    "realm_access": {
                        "roles": ["user"]
                    }
                }
            
            # Create token
            return service.create_token(user_id)
            
        elif grant_type == "refresh_token":
            # Refresh token grant
            refresh_token = form_data.get("refresh_token")
            
            if not refresh_token:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Missing refresh_token"
                )
            
            # Refresh token
            return service.refresh_token(refresh_token)
            
        elif grant_type == "client_credentials":
            # Client credentials grant
            client_id = form_data.get("client_id")
            client_secret = form_data.get("client_secret")
            
            # Validate client credentials
            if client_id != service.client_id or client_secret != service.client_secret:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid client credentials"
                )
            
            # Create a service account token
            service_account_id = f"service-account-{client_id}"
            
            # Create or get service account user
            if service_account_id not in service.mock_users:
                service.mock_users[service_account_id] = {
                    "sub": service_account_id,
                    "preferred_username": f"service-account-{client_id}",
                    "email": f"service-account-{client_id}@example.com",
                    "name": f"Service Account {client_id}",
                    "realm_access": {
                        "roles": ["service-account"]
                    }
                }
            
            # Create token
            return service.create_token(service_account_id)
            
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported grant_type: {grant_type}"
            )
    
    # Token introspection endpoint
    @router.post("/realms/{realm}/protocol/openid-connect/token/introspect")
    async def introspect(realm: str, request: Request):
        """Token introspection endpoint."""
        # Validate realm
        if realm != service.keycloak_realm:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Realm {realm} not found"
            )
        
        # Get form data
        form_data = await request.form()
        token = form_data.get("token")
        
        if not token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing token"
            )
        
        # Validate client credentials
        client_id = form_data.get("client_id")
        client_secret = form_data.get("client_secret")
        
        if client_id != service.client_id or client_secret != service.client_secret:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid client credentials"
            )
        
        # Introspect token
        return service.introspect_token(token)
    
    # Userinfo endpoint
    @router.get("/realms/{realm}/protocol/openid-connect/userinfo")
    async def userinfo(realm: str, request: Request):
        """Userinfo endpoint."""
        # Validate realm
        if realm != service.keycloak_realm:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Realm {realm} not found"
            )
        
        # Get authorization header
        authorization = request.headers.get("Authorization")
        
        if not authorization:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing authorization header"
            )
        
        # Get token
        if authorization.startswith("Bearer "):
            token = authorization[7:]
        else:
            token = authorization
        
        # Get user info
        return service.get_user_info(token)
    
    # Revocation endpoint
    @router.post("/realms/{realm}/protocol/openid-connect/revoke")
    async def revoke(realm: str, request: Request):
        """Token revocation endpoint."""
        # Validate realm
        if realm != service.keycloak_realm:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Realm {realm} not found"
            )
        
        # Get form data
        form_data = await request.form()
        token = form_data.get("token")
        
        if not token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing token"
            )
        
        # Validate client credentials
        client_id = form_data.get("client_id")
        client_secret = form_data.get("client_secret")
        
        if client_id != service.client_id or client_secret != service.client_secret:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid client credentials"
            )
        
        # Revoke token
        service.revoke_token(token)
        
        # Return success
        return {"status": "ok"}
    
    # Add OAuth endpoints
    @router.get("/realms/{realm}/protocol/openid-connect/auth")
    async def oauth_authorize(
        realm: str,
        client_id: str,
        redirect_uri: str,
        response_type: str,
        scope: Optional[str] = None,
        state: Optional[str] = None,
        request: Request = None
    ):
        """OAuth authorization endpoint."""
        # Validate realm
        if realm != service.keycloak_realm:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Realm {realm} not found"
            )
        
        # Validate client
        if client_id != service.client_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Client {client_id} not found"
            )
        
        # In mock mode, we'll automatically authorize the user
        # with a default mock user
        user_id = list(service.mock_users.keys())[0]
        
        # Create token
        token_response = service.create_token(user_id)
        
        # Handle different response types
        if response_type == "code":
            # Authorization code flow
            # In mock mode, we'll use the access token as the code
            code = token_response["access_token"]
            
            # Store token for later use
            service.active_tokens[code] = {
                "user_id": user_id,
                "redirect_uri": redirect_uri,
                "token_response": token_response,
                "is_code": True
            }
            
            # Redirect to redirect_uri with code
            redirect_url = f"{redirect_uri}?code={code}"
            if state:
                redirect_url += f"&state={state}"
            
            return RedirectResponse(url=redirect_url)
            
        elif response_type == "token":
            # Implicit flow
            # Redirect to redirect_uri with token
            redirect_url = f"{redirect_uri}#access_token={token_response['access_token']}&token_type=bearer&expires_in={token_response['expires_in']}"
            if state:
                redirect_url += f"&state={state}"
            
            return RedirectResponse(url=redirect_url)
            
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported response_type: {response_type}"
            )
    
    # Login page for testing
    @router.get("/realms/{realm}/protocol/openid-connect/login")
    async def login_page(realm: str):
        """Login page for testing."""
        # Validate realm
        if realm != service.keycloak_realm:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Realm {realm} not found"
            )
        
        # Return a simple login form
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Mock Keycloak Login</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    background-color: #f5f5f5;
                }
                .login-container {
                    background-color: white;
                    padding: 20px;
                    border-radius: 5px;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                    width: 300px;
                }
                h1 {
                    margin-top: 0;
                    color: #333;
                    font-size: 24px;
                }
                .form-group {
                    margin-bottom: 15px;
                }
                label {
                    display: block;
                    margin-bottom: 5px;
                    font-weight: bold;
                    color: #555;
                }
                input[type="text"],
                input[type="password"] {
                    width: 100%;
                    padding: 8px;
                    border: 1px solid #ddd;
                    border-radius: 3px;
                    box-sizing: border-box;
                }
                button {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 10px 15px;
                    border-radius: 3px;
                    cursor: pointer;
                    width: 100%;
                }
                .mock-warning {
                    margin-top: 20px;
                    padding: 10px;
                    background-color: #ffffd6;
                    border: 1px solid #e7e7ca;
                    border-radius: 3px;
                    font-size: 12px;
                    color: #666;
                }
            </style>
        </head>
        <body>
            <div class="login-container">
                <h1>Mock Keycloak Login</h1>
                <form action="/realms/{realm}/protocol/openid-connect/token" method="post">
                    <div class="form-group">
                        <label for="username">Username</label>
                        <input type="text" id="username" name="username" value="mock-user" required>
                    </div>
                    <div class="form-group">
                        <label for="password">Password</label>
                        <input type="password" id="password" name="password" value="mock-password" required>
                    </div>
                    <button type="submit">Login</button>
                    <div class="mock-warning">
                        This is a mock login page for development and testing.
                        Any username and password will be accepted.
                    </div>
                </form>
            </div>
        </body>
        </html>
        """.format(realm=service.keycloak_realm)
        
        return HTMLResponse(content=html)
    
    # Logout endpoint
    @router.get("/realms/{realm}/protocol/openid-connect/logout")
    async def logout(
        realm: str,
        redirect_uri: Optional[str] = None,
        id_token_hint: Optional[str] = None
    ):
        """Logout endpoint."""
        # Validate realm
        if realm != service.keycloak_realm:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Realm {realm} not found"
            )
        
        # Revoke token if provided
        if id_token_hint:
            service.revoke_token(id_token_hint)
        
        # Redirect if provided
        if redirect_uri:
            return RedirectResponse(url=redirect_uri)
        
        # Return success message
        return HTMLResponse(
            content="""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Logged Out</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 20px;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        background-color: #f5f5f5;
                    }
                    .logout-container {
                        background-color: white;
                        padding: 20px;
                        border-radius: 5px;
                        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                        width: 300px;
                        text-align: center;
                    }
                    h1 {
                        margin-top: 0;
                        color: #333;
                        font-size: 24px;
                    }
                    p {
                        color: #666;
                    }
                    .mock-warning {
                        margin-top: 20px;
                        padding: 10px;
                        background-color: #ffffd6;
                        border: 1px solid #e7e7ca;
                        border-radius: 3px;
                        font-size: 12px;
                        color: #666;
                    }
                </style>
            </head>
            <body>
                <div class="logout-container">
                    <h1>Logged Out</h1>
                    <p>You have been successfully logged out.</p>
                    <div class="mock-warning">
                        This is a mock logout page for development and testing.
                    </div>
                </div>
            </body>
            </html>
            """
        )
    
    # Return the router
    return router


def setup_mock_mode(
    app: Optional[FastAPI] = None,
    keycloak_url: str = "http://localhost:8080/auth",
    keycloak_realm: str = "mock-realm",
    client_id: str = "mock-client",
    client_secret: str = "mock-secret",
    mock_users: Optional[List[Dict[str, Any]]] = None,
    prefix: str = "",
    logger: Optional[logging.Logger] = None
) -> MockKeycloakService:
    """
    Set up mock mode for development and testing.
    
    Args:
        app: FastAPI application to add mock endpoints to (optional)
        keycloak_url: Keycloak server URL
        keycloak_realm: Keycloak realm name
        client_id: Client ID
        client_secret: Client secret
        mock_users: List of mock users (will create a default user if None)
        prefix: Prefix for mock endpoints
        logger: Logger instance
        
    Returns:
        MockKeycloakService: Mock Keycloak service instance
    """
    # Initialize logger
    logger = logger or logging.getLogger("fastapi-keycloak.mock")
    logger.info(f"Setting up mock mode with URL: {keycloak_url}, realm: {keycloak_realm}")
    
    # Create mock service
    service = MockKeycloakService(
        keycloak_url=keycloak_url,
        keycloak_realm=keycloak_realm,
        client_id=client_id,
        client_secret=client_secret,
        mock_users=mock_users,
        logger=logger
    )
    
    # Add mock endpoints to app if provided
    if app:
        # Create router
        router = create_mock_router(service)
        
        # Add router to app with optional prefix
        app.include_router(router, prefix=prefix)
        
        logger.info(f"Mock Keycloak endpoints added to FastAPI app with prefix: {prefix}")
    
    return service
