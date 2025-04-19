#!/usr/bin/env python3
"""
SSL Utilities for FastAPI-Authlib-Keycloak Integration.

This module provides utilities for managing SSL certificates in the application.
"""

import os
import json
import shutil
import logging
import urllib.request
from pathlib import Path
from typing import Optional, Dict, Union


def setup_ssl(
    ssl_cert_file: Optional[str] = None,
    ssl_key_file: Optional[str] = None,
    ssl_verify: Union[bool, str] = True,
    on_ssl_error: str = "raise",
    logger: Optional[logging.Logger] = None
) -> bool:
    """
    Set up SSL certificate verification.
    
    Args:
        ssl_cert_file: Path to SSL certificate file
        ssl_key_file: Path to SSL key file
        ssl_verify: SSL verification mode (True for standard verification,
            False to disable verification, or string path to a CA bundle)
        on_ssl_error: How to handle SSL errors ('raise', 'warn', or 'ignore')
        logger: Logger instance
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Initialize logger if not provided
    logger = logger or logging.getLogger("fastapi-keycloak.ssl")
    
    # If verification is disabled, log a warning and return immediately
    if ssl_verify is False:
        logger.warning(
            "SSL certificate verification is DISABLED. This is insecure and should only be used "
            "in development environments."
        )
        # We explicitly set environment variables to disable verification
        os.environ['REQUESTS_CA_BUNDLE'] = ""
        os.environ['SSL_CERT_FILE'] = ""
        return True
    
    # If ssl_verify is a string path to a certificate, use it instead of ssl_cert_file
    if isinstance(ssl_verify, str) and ssl_verify != "True" and ssl_verify != "False":
        if os.path.isfile(ssl_verify):
            ssl_cert_file = ssl_verify
            logger.info(f"Using certificate file from ssl_verify: {ssl_verify}")
        else:
            error_msg = f"Certificate file specified in ssl_verify not found: {ssl_verify}"
            if on_ssl_error == "raise":
                logger.error(error_msg)
                raise FileNotFoundError(error_msg)
            elif on_ssl_error == "warn":
                logger.warning(error_msg)
                return False
            else:  # ignore
                logger.info(error_msg)
                return True
    
    # Basic validation
    if not ssl_cert_file or not os.path.isfile(ssl_cert_file):
        error_msg = f"SSL certificate file not found: {ssl_cert_file}"
        if on_ssl_error == "raise":
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)
        elif on_ssl_error == "warn":
            logger.warning(error_msg)
            return False
        else:  # ignore
            logger.info(error_msg)
            return True
    
    if ssl_key_file and not os.path.isfile(ssl_key_file):
        logger.warning(f"SSL key file not found: {ssl_key_file}")
    
    # Install certificate in certifi
    cert_installed = install_cert_in_certifi(ssl_cert_file, logger)
    
    # Set environment variables
    env_vars_set = set_ssl_cert_env_vars(ssl_cert_file, logger)
    
    return cert_installed and env_vars_set


def install_cert_in_certifi(
    ssl_cert_file: str,
    logger: Optional[logging.Logger] = None
) -> bool:
    """
    Install the certificate in the certifi bundle for Python requests.
    
    This allows libraries like requests and httpx to verify the
    Keycloak server's SSL certificate.
    
    Args:
        ssl_cert_file: Path to SSL certificate file
        logger: Logger instance
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Initialize logger if not provided
        logger = logger or logging.getLogger("fastapi-keycloak.ssl")
        
        # Get the certifi CA bundle path
        try:
            import certifi
            certifi_path = certifi.where()
            logger.info(f"Certifi CA bundle located at: {certifi_path}")
        except ImportError:
            logger.error("certifi package not installed. Install it with 'pip install certifi'")
            return False
        
        # Check if certificate file exists
        if not os.path.isfile(ssl_cert_file):
            logger.error(f"SSL certificate file not found: {ssl_cert_file}")
            return False
            
        # Read the certificate file content
        with open(ssl_cert_file, 'r') as cert_file:
            cert_content = cert_file.read()
            
        # Append the certificate to the certifi bundle
        # First, make a backup of the original bundle
        certifi_backup = certifi_path + '.backup'
        if not os.path.exists(certifi_backup):
            logger.info(f"Creating backup of certifi bundle: {certifi_backup}")
            shutil.copy2(certifi_path, certifi_backup)
        
        # Append the certificate
        with open(certifi_path, 'a') as ca_bundle:
            ca_bundle.write('\n')
            ca_bundle.write(cert_content)
            
        logger.info(f"Certificate successfully added to certifi bundle")
        return True
        
    except Exception as e:
        if logger:
            logger.error(f"Error installing certificate in certifi: {str(e)}")
        return False


def set_ssl_cert_env_vars(
    ssl_cert_file: str,
    logger: Optional[logging.Logger] = None
) -> bool:
    """
    Set environment variables for SSL certificate verification.
    
    This ensures that libraries like requests, httpx, and urllib use
    the correct certificate for verification.
    
    Args:
        ssl_cert_file: Path to SSL certificate file
        logger: Logger instance
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Initialize logger if not provided
        logger = logger or logging.getLogger("fastapi-keycloak.ssl")
        
        # Set environment variables for certificate verification
        os.environ['REQUESTS_CA_BUNDLE'] = ssl_cert_file
        os.environ['SSL_CERT_FILE'] = ssl_cert_file
        
        # Configure urllib to use our certificate
        try:
            # Create an SSL context with our certificate
            import ssl
            ssl_context = ssl.create_default_context(cafile=ssl_cert_file)
            # Install it as the default HTTPS context
            urllib.request.install_opener(
                urllib.request.build_opener(
                    urllib.request.HTTPSHandler(context=ssl_context)
                )
            )
            logger.info("SSL context configured for urllib")
        except Exception as ssl_ctx_error:
            logger.error(f"Error configuring SSL context for urllib: {str(ssl_ctx_error)}")
            
        logger.info("SSL environment variables set successfully")
        return True
        
    except Exception as e:
        if logger:
            logger.error(f"Error setting SSL environment variables: {str(e)}")
        return False


def configure_oauth_ssl(
    ssl_enabled: bool = False,
    ssl_verify: Union[bool, str] = True,
    ssl_cert_file: Optional[str] = None,
    allow_http: bool = False,
    development_mode: bool = False,
    logger: Optional[logging.Logger] = None
) -> Dict[str, any]:
    """
    Configure SSL certificate verification for the OAuth client.
    
    Args:
        ssl_enabled: Whether SSL verification is enabled
        ssl_verify: SSL verification mode (True for standard verification,
            False to disable verification, or string path to a CA bundle)
        ssl_cert_file: Path to SSL certificate file
        allow_http: Allow HTTP for Keycloak URL
        development_mode: Whether development mode is enabled
        logger: Logger instance
    
    Returns:
        dict: Client kwargs with SSL configuration
    """
    logger = logger or logging.getLogger("fastapi-keycloak.ssl")
    
    client_kwargs = {
        "scope": "openid email profile",
    }
    
    # Handle ssl_verify parameter
    if ssl_enabled:
        if isinstance(ssl_verify, str) and ssl_verify not in ("True", "False"):
            # If ssl_verify is a path to a certificate
            if os.path.isfile(ssl_verify):
                client_kwargs["verify"] = ssl_verify
                logger.info(f"OAuth client using certificate: {ssl_verify}")
            else:
                logger.warning(f"Certificate not found: {ssl_verify}, using default verification")
        elif ssl_verify is False:
            client_kwargs["verify"] = False
            logger.warning("OAuth client SSL verification DISABLED - insecure configuration")
        elif ssl_cert_file and os.path.isfile(ssl_cert_file):
            client_kwargs["verify"] = ssl_cert_file
            logger.info(f"OAuth client using certificate: {ssl_cert_file}")
    elif development_mode and not ssl_enabled:
        # In development mode, if SSL is not enabled, disable verification
        client_kwargs["verify"] = False
        logger.warning("Development mode: OAuth client SSL verification DISABLED")


def load_jwks_from_file(jwks_file: str, logger: Optional[logging.Logger] = None) -> Optional[Dict]:
    """
    Load JWKS from a local file.
    
    This is useful for development environments or when Keycloak is unreachable.
    
    Args:
        jwks_file: Path to the JWKS file
        logger: Logger instance
        
    Returns:
        Optional[Dict]: The JWKS as a dictionary, or None if the file cannot be loaded
    """
    logger = logger or logging.getLogger("fastapi-keycloak.ssl")
    
    try:
        if not os.path.isfile(jwks_file):
            logger.error(f"JWKS file not found: {jwks_file}")
            return None
            
        with open(jwks_file, 'r') as f:
            jwks = json.loads(f.read())
            logger.info(f"Successfully loaded JWKS from file: {jwks_file}")
            return jwks
    except Exception as e:
        logger.error(f"Error loading JWKS from file: {str(e)}")
        return None
    
    return client_kwargs
