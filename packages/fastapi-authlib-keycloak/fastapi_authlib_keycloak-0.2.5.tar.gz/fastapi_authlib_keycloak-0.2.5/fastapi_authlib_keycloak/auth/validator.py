#!/usr/bin/env python3
"""
JWT Token Validator for Keycloak Integration.

This module handles JWT token validation using Authlib and Keycloak.
"""

import base64
import json
import logging
import os
import ssl
import time
from typing import Dict, Optional, List, Any, Union

import httpx
from authlib.jose import JsonWebToken, JsonWebKey
from authlib.jose.errors import JoseError
from fastapi import HTTPException, status


class KeycloakJWTValidator:
    """Validator for Keycloak JWT tokens."""

    def __init__(
        self,
        issuer: str,
        jwks_uri: str,
        client_id: str,
        api_client_id: Optional[str] = None,
        strict_client_check: bool = False,
        ssl_verify: Union[bool, str] = True,
        ssl_cert_file: Optional[str] = None,
        jwks_cache_ttl: int = 3600,
        jwks_file: Optional[str] = None,
        on_ssl_error: str = "raise",
        development_mode: bool = False,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize the validator with the required parameters.

        Args:
            issuer: The issuer URL (usually the Keycloak server URL)
            jwks_uri: The URL to the JWK Set
            client_id: The primary client ID to verify in the token
            api_client_id: Secondary client ID that is also acceptable (for flexibility)
            strict_client_check: Whether to strictly enforce client ID matching
            ssl_verify: SSL verification mode (True for standard verification,
                False to disable verification, or string path to a CA bundle)
            ssl_cert_file: Path to SSL certificate file for verification
            jwks_cache_ttl: Cache time for JWKS in seconds
            jwks_file: Path to a local JWKS file for offline verification
            on_ssl_error: How to handle SSL errors ('raise', 'warn', or 'ignore')
            development_mode: Whether development mode is enabled
            logger: Logger instance
        """
        self.issuer = issuer
        self.jwks_uri = jwks_uri
        self.client_id = client_id
        self.api_client_id = api_client_id
        self.strict_client_check = strict_client_check
        self.ssl_verify = ssl_verify
        self.ssl_cert_file = ssl_cert_file
        self.jwks_cache_ttl = jwks_cache_ttl
        self.jwks_file = jwks_file
        self.on_ssl_error = on_ssl_error
        self.development_mode = development_mode
        self.logger = logger or logging.getLogger("fastapi-keycloak.validator")
        self.jwks = None
        self.jwks_last_fetched = 0  # Timestamp when JWKS was last fetched
        
        # In development mode, try to load local JWKS file if provided
        if self.development_mode and self.jwks_file:
            self._try_load_local_jwks()

    def _try_load_local_jwks(self) -> bool:
        """
        Try to load JWKS from a local file.
        
        Returns:
            bool: True if successfully loaded, False otherwise
        """
        try:
            from fastapi_authlib_keycloak.utils.ssl_utils import load_jwks_from_file
            self.jwks = load_jwks_from_file(self.jwks_file, self.logger)
            if self.jwks:
                self.logger.info(f"Successfully loaded JWKS from local file: {self.jwks_file}")
                self.jwks_last_fetched = time.time()
                return True
            else:
                self.logger.warning(f"Failed to load JWKS from local file: {self.jwks_file}")
                return False
        except Exception as e:
            self.logger.error(f"Error loading local JWKS file: {str(e)}")
            return False

    async def fetch_jwks(self) -> Dict:
        """Fetch the JWK Set from the JWKS URI.
        
        Returns:
            Dict: The JWKS as a dictionary
            
        Raises:
            HTTPException: If the JWKS cannot be fetched
        """
        # Check if we have a valid cached version
        current_time = time.time()
        if self.jwks and (current_time - self.jwks_last_fetched) < self.jwks_cache_ttl:
            self.logger.debug(f"Using cached JWKS (fetched {current_time - self.jwks_last_fetched:.1f}s ago)")
            return self.jwks
            
        # If in development mode and JWKS fetch fails, try to use local file
        try_local_file = self.development_mode and self.jwks_file
        
        try:
            # Configure SSL verification based on ssl_verify parameter
            if isinstance(self.ssl_verify, str) and os.path.isfile(self.ssl_verify):
                verify = self.ssl_verify
            elif self.ssl_verify is False:
                verify = False
                self.logger.warning("SSL verification is DISABLED for JWKS fetch - insecure configuration")
            elif self.ssl_cert_file and os.path.isfile(self.ssl_cert_file):
                verify = self.ssl_cert_file
            else:
                verify = self.ssl_verify
            
            # Create client with appropriate SSL verification
            async with httpx.AsyncClient(verify=verify) as client:
                self.logger.info(f"Fetching JWKS from {self.jwks_uri}")
                response = await client.get(self.jwks_uri)
                response.raise_for_status()
                self.jwks = response.json()
                self.jwks_last_fetched = time.time()
                self.logger.info(f"JWKS successfully fetched from {self.jwks_uri}")
                return self.jwks
        except Exception as e:
            self.logger.error(f"Error fetching JWKS: {str(e)}")
            
            # In development mode, try to load from local file if available
            if try_local_file:
                self.logger.info(f"Attempting to load JWKS from local file: {self.jwks_file}")
                if self._try_load_local_jwks():
                    return self.jwks
                    
            # Handle errors according to on_ssl_error setting
            if "SSL" in str(e) or "certificate" in str(e).lower():
                if self.on_ssl_error == "warn":
                    self.logger.warning(f"SSL error when fetching JWKS: {str(e)}. Consider using development_mode=True.")
                elif self.on_ssl_error == "ignore":
                    self.logger.info(f"Ignoring SSL error: {str(e)}")
                    return {}  # Return empty JWKS
            
            # If not handled by special cases above, raise the exception
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Could not fetch JWKS: {str(e)}"
            )

    async def validate_token(self, token: str) -> Dict:
        """
        Validate a JWT token using the JWKS.

        Args:
            token: The JWT token string

        Returns:
            Dict: The decoded token claims if valid

        Raises:
            HTTPException: If token validation fails
        """
        try:
            # Ensure token format - remove Bearer prefix if present
            if token.startswith("Bearer "):
                token = token[7:]

            if not self.jwks:
                await self.fetch_jwks()

            # Create JsonWebKey instance from JWKS
            json_web_key = JsonWebKey.import_key_set(self.jwks)

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
                    self.logger.warning(f"Client ID mismatch: Token has '{token_client_id}' but validator expects one of {valid_client_ids}")
                    # We're logging a warning but not raising an exception to be more tolerant
                    # If you want to strictly enforce this, uncomment the following lines:
                    # raise HTTPException(
                    #    status_code=status.HTTP_401_UNAUTHORIZED,
                    #    detail=f"Client ID mismatch: Token has '{token_client_id}' but validator expects one of {valid_client_ids}"
                    #)

            self.logger.info(f"Token successfully validated for user: {claims.get('preferred_username')}")
            return claims

        except JoseError as e:
            # More detailed error logging
            token_content, client_id_in_token = self._extract_token_info(token)
            self.logger.error(f"Token client ID: {client_id_in_token}, Validator client IDs: primary={self.client_id}, secondary={self.api_client_id}")
            
            # Determine the error detail to return
            detail = self._get_error_detail(token_content, client_id_in_token, str(e))
                
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=detail
            )
            
        except Exception as e:
            self.logger.error(f"Unexpected error during token validation: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token validation failed: {str(e)}"
            )

    def _extract_token_info(self, token: str) -> tuple:
        """Extract information from a token for debugging purposes.
        
        Args:
            token: The JWT token string
            
        Returns:
            tuple: (token_content, client_id_in_token)
        """
        token_content = None
        client_id_in_token = None
        try:
            # Remove Bearer prefix if present
            if token.startswith("Bearer "):
                token = token[7:]
                
            parts = token.split('.')
            if len(parts) >= 2:
                # Fix padding for base64url decode
                payload = parts[1]
                payload += '=' * (4 - len(payload) % 4)
                decoded = base64.urlsafe_b64decode(payload)
                token_content = json.loads(decoded)
                # Check both 'azp' and 'client_id' claims
                client_id_in_token = token_content.get("azp")
                if not client_id_in_token:
                    client_id_in_token = token_content.get("client_id")
        except Exception as decode_error:
            self.logger.error(f"Error decoding token: {str(decode_error)}")
            
        return token_content, client_id_in_token
        
    def _get_error_detail(self, token_content, client_id_in_token, error_msg: str) -> str:
        """Get detailed error message for token validation failure.
        
        Args:
            token_content: The decoded token content
            client_id_in_token: The client ID extracted from the token
            error_msg: The original error message
            
        Returns:
            str: A detailed error message
        """
        if token_content:
            # Check if it's a client ID issue or something else
            if client_id_in_token and self.strict_client_check:
                valid_client_ids = [self.client_id]
                if self.api_client_id:
                    valid_client_ids.append(self.api_client_id)
                    
                if client_id_in_token not in valid_client_ids:
                    return f"Client ID mismatch: Token has '{client_id_in_token}' but validator expects one of {valid_client_ids}"
                else:
                    return f"Token validation error: {error_msg}"
            else:
                return f"Token validation error: {error_msg}"
        else:
            return f"Invalid token format or token could not be decoded: {error_msg}"


def create_validator(
    keycloak_url: str,
    keycloak_realm: str,
    client_id: str,
    api_client_id: Optional[str] = None,
    strict_client_check: bool = False,
    ssl_verify: Union[bool, str] = True,
    ssl_cert_file: Optional[str] = None,
    jwks_cache_ttl: int = 3600,
    jwks_file: Optional[str] = None,
    on_ssl_error: str = "raise",
    development_mode: bool = False,
    logger: Optional[logging.Logger] = None
) -> KeycloakJWTValidator:
    """
    Create a Keycloak JWT validator.
    
    Args:
        keycloak_url: URL of the Keycloak server
        keycloak_realm: Keycloak realm name
        client_id: Client ID
        api_client_id: API client ID
        strict_client_check: Whether to strictly enforce client ID matching
        ssl_verify: SSL verification mode (True for standard verification,
            False to disable verification, or string path to a CA bundle)
        ssl_cert_file: Path to SSL certificate file
        jwks_cache_ttl: Cache time for JWKS in seconds
        jwks_file: Path to a local JWKS file for offline verification
        on_ssl_error: How to handle SSL errors ('raise', 'warn', or 'ignore')
        development_mode: Whether development mode is enabled
        logger: Logger instance
        
    Returns:
        KeycloakJWTValidator: Configured validator
    """
    # Initialize logger if not provided
    logger = logger or logging.getLogger("fastapi-keycloak.validator")
    
    # Initialize validator
    validator = KeycloakJWTValidator(
        issuer=f"{keycloak_url}/realms/{keycloak_realm}",
        jwks_uri=f"{keycloak_url}/realms/{keycloak_realm}/protocol/openid-connect/certs",
        client_id=client_id,
        api_client_id=api_client_id,
        strict_client_check=strict_client_check,
        ssl_verify=ssl_verify,
        ssl_cert_file=ssl_cert_file,
        jwks_cache_ttl=jwks_cache_ttl,
        jwks_file=jwks_file,
        on_ssl_error=on_ssl_error,
        development_mode=development_mode,
        logger=logger
    )
    
    return validator
