#!/usr/bin/env python3
"""
OAuth module for FastAPI-Authlib-Keycloak integration.

This module initializes the OAuth client for Keycloak integration.
"""

import logging
from typing import Optional, Union

from authlib.integrations.starlette_client import OAuth
from fastapi_authlib_keycloak.utils.ssl_utils import configure_oauth_ssl


def setup_oauth(
    keycloak_url: str,
    keycloak_realm: str,
    client_id: str,
    client_secret: str,
    ssl_enabled: bool = False,
    ssl_verify: Union[bool, str] = True,
    ssl_cert_file: Optional[str] = None,
    allow_http: bool = False,
    development_mode: bool = False,
    logger: Optional[logging.Logger] = None
) -> OAuth:
    """
    Set up OAuth client for Keycloak.
    
    Args:
        keycloak_url: URL of the Keycloak server
        keycloak_realm: Keycloak realm name
        client_id: Client ID
        client_secret: Client secret
        ssl_enabled: Whether SSL verification is enabled
        ssl_verify: SSL verification mode (True for standard verification,
            False to disable verification, or string path to a CA bundle)
        ssl_cert_file: Path to SSL certificate file
        allow_http: Allow HTTP for Keycloak URL (insecure, for development only)
        development_mode: Whether development mode is enabled
        logger: Logger instance
        
    Returns:
        OAuth: Configured OAuth client
    """
    # Initialize logger if not provided
    logger = logger or logging.getLogger("fastapi-keycloak.oauth")
    
    # Handle HTTP/HTTPS in Keycloak URL
    server_url = keycloak_url
    if development_mode and allow_http and not server_url.startswith("http"):
        server_url = f"http://{server_url}" if not server_url.startswith("http://") else server_url
        logger.warning(f"Development mode: Using HTTP for Keycloak URL: {server_url}")
    elif not server_url.startswith("http"):
        server_url = f"https://{server_url}" if not server_url.startswith("https://") else server_url
    
    # Initialize OAuth
    oauth = OAuth()
    
    # Get client kwargs with SSL configuration
    client_kwargs = configure_oauth_ssl(
        ssl_enabled=ssl_enabled,
        ssl_verify=ssl_verify,
        ssl_cert_file=ssl_cert_file,
        allow_http=allow_http,
        development_mode=development_mode,
        logger=logger
    )
    
    # Register Keycloak as an OAuth provider
    oauth.register(
        name="keycloak",
        server_metadata_url=f"{server_url}/realms/{keycloak_realm}/.well-known/openid-configuration",
        client_id=client_id,
        client_secret=client_secret,
        client_kwargs=client_kwargs
    )
    
    logger.info(f"OAuth client initialized for {server_url}/realms/{keycloak_realm}")
    
    return oauth
