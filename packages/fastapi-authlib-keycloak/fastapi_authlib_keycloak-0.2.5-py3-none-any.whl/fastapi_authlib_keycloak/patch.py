"""
Patch module for FastAPI-Authlib-Keycloak.

This module provides convenient functions for patching common issues
with SSL certificates, environment variables, and other runtime problems.
"""

import os
import sys
import logging
import warnings
from typing import Optional, Dict, Any, Union

# Configure logger
logger = logging.getLogger("fastapi-keycloak.patch")

# Check if cert_utils is available
try:
    from fastapi_authlib_keycloak.utils.cert_utils import (
        fix_certificate_issues,
        check_keycloak_certificate,
        diagnostic_report
    )
    CERT_UTILS_AVAILABLE = True
except ImportError:
    CERT_UTILS_AVAILABLE = False

# List of applied patches
_applied_patches = []


def fix_ssl_certificate_issue(mode: str = "platform", url: Optional[str] = None) -> Dict[str, Any]:
    """
    Fix SSL certificate verification issues.
    
    This is a convenience function that wraps the more detailed certificate
    utilities to provide a simple way to fix common SSL certificate issues.
    
    Args:
        mode: Certificate verification mode:
            - "platform": Use certifi's CA bundle (recommended)
            - "disabled": Disable certificate verification (insecure)
            - "auto": Automatically detect and fix issues
            - A path to a custom CA bundle file
        url: Optional URL to test after applying the fix
        
    Returns:
        Dict[str, Any]: Results of the fix operation
    """
    if not CERT_UTILS_AVAILABLE:
        logger.warning(
            "Certificate utilities are not available. "
            "Make sure you have the required dependencies installed."
        )
        return {
            "success": False,
            "error": "Certificate utilities not available",
            "recommendation": "Install with: pip install fastapi-authlib-keycloak[all]"
        }
    
    # Apply the certificate fix
    logger.info(f"Applying certificate fix with mode: {mode}")
    result = fix_certificate_issues(mode, url)
    
    # Record the patch
    _applied_patches.append({
        "name": "ssl_certificate_fix",
        "mode": mode,
        "result": result.get("success", False)
    })
    
    return result


def apply_all_patches(development_mode: bool = False) -> Dict[str, Any]:
    """
    Apply all available patches automatically.
    
    This function applies all available patches to fix common issues
    with SSL certificates, environment variables, and other runtime problems.
    
    Args:
        development_mode: Whether to apply development-friendly patches
        
    Returns:
        Dict[str, Any]: Results of the patch operations
    """
    results = {
        "success": True,
        "patches_applied": [],
        "patches_failed": []
    }
    
    # Apply SSL certificate fix in auto mode
    if CERT_UTILS_AVAILABLE:
        try:
            mode = "auto" if development_mode else "platform"
            ssl_result = fix_ssl_certificate_issue(mode)
            
            if ssl_result.get("success", False):
                results["patches_applied"].append("ssl_certificate_fix")
            else:
                results["patches_failed"].append({
                    "name": "ssl_certificate_fix",
                    "error": ssl_result.get("error", "Unknown error")
                })
                results["success"] = False
        except Exception as e:
            results["patches_failed"].append({
                "name": "ssl_certificate_fix",
                "error": str(e)
            })
            results["success"] = False
    
    # Set environment variables for development mode
    if development_mode:
        try:
            # Set environment variables for development
            os.environ["KEYCLOAK_DEVELOPMENT_MODE"] = "true"
            os.environ["KEYCLOAK_ALLOW_HTTP"] = "true"
            
            if "SSL_CERT_FILE" not in os.environ and CERT_UTILS_AVAILABLE:
                import certifi
                os.environ["SSL_CERT_FILE"] = certifi.where()
                
            if "REQUESTS_CA_BUNDLE" not in os.environ and CERT_UTILS_AVAILABLE:
                import certifi
                os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
                
            results["patches_applied"].append("development_env_vars")
        except Exception as e:
            results["patches_failed"].append({
                "name": "development_env_vars",
                "error": str(e)
            })
            results["success"] = False
    
    return results


def auto_patch() -> None:
    """
    Automatically apply patches based on environment variables.
    
    This function is called automatically when the KEYCLOAK_AUTO_PATCH
    environment variable is set.
    """
    logger.info("Auto-patching FastAPI-Authlib-Keycloak")
    
    development_mode = os.environ.get("KEYCLOAK_DEVELOPMENT_MODE", "").lower() in ["true", "1", "yes", "y"]
    cert_mode = os.environ.get("KEYCLOAK_CERT_MODE", "auto" if development_mode else "platform")
    
    # Apply all patches
    results = apply_all_patches(development_mode)
    
    # Log results
    if results["success"]:
        logger.info(f"Auto-patching completed successfully: {', '.join(results['patches_applied'])}")
    else:
        logger.warning(
            f"Auto-patching partially failed. Applied: {', '.join(results['patches_applied'])}, "
            f"Failed: {len(results['patches_failed'])}"
        )
        for failed in results["patches_failed"]:
            logger.warning(f"Failed patch '{failed['name']}': {failed['error']}")
