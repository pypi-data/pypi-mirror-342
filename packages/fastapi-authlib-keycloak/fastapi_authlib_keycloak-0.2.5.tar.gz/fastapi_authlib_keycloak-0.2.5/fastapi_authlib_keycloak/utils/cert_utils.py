"""
Enhanced certificate verification utilities for FastAPI-Authlib-Keycloak.

This module provides advanced SSL/TLS certificate handling capabilities,
including flexible verification modes, diagnostic tools, error handling,
and automatic issue detection and resolution.
"""

import os
import ssl
import socket
import logging
import certifi
import requests
import urllib3
import inspect
import tempfile
import platform
import sys
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, Union, Tuple, List, Set
from datetime import datetime

# Configure logger
logger = logging.getLogger("fastapi-keycloak.cert_utils")

# Constants for verification modes
VERIFICATION_MODES = {
    "default": "Use system's default CA bundle",
    "platform": "Use certifi's CA bundle (recommended)",
    "disabled": "Disable certificate verification (insecure, dev only)",
    "auto": "Auto-detect and resolve certificate issues",
}

# Keep track of what certificate fixes have been applied
_applied_fixes: Set[str] = set()


def get_available_certificate_stores() -> Dict[str, str]:
    """
    Get information about available certificate stores in the system.
    
    Returns:
        Dict[str, str]: Dictionary of certificate stores and their locations
    """
    stores = {
        "certifi": certifi.where(),
        "system": _get_system_ca_path(),
    }
    
    # Add other potential certificate store locations
    if platform.system() == "Linux":
        for path in [
            "/etc/ssl/certs/ca-certificates.crt",  # Debian/Ubuntu
            "/etc/pki/tls/certs/ca-bundle.crt",    # RHEL/CentOS
            "/etc/ssl/ca-bundle.pem",              # SUSE
        ]:
            if os.path.exists(path):
                stores[f"linux-{os.path.basename(path)}"] = path
    
    elif platform.system() == "Darwin":  # macOS
        for path in [
            "/etc/ssl/cert.pem",
            "/usr/local/etc/openssl/cert.pem",
        ]:
            if os.path.exists(path):
                stores[f"macos-{os.path.basename(path)}"] = path
    
    elif platform.system() == "Windows":
        stores["windows"] = "Windows Certificate Store (system)"
    
    return stores


def _get_system_ca_path() -> str:
    """
    Try to determine the system's default CA certificate path.
    
    Returns:
        str: Path to the system's CA certificates or a placeholder
    """
    if platform.system() == "Linux":
        # Common paths on Linux systems
        for path in [
            "/etc/ssl/certs/ca-certificates.crt",  # Debian/Ubuntu
            "/etc/pki/tls/certs/ca-bundle.crt",    # RHEL/CentOS
            "/etc/ssl/ca-bundle.pem",              # SUSE
        ]:
            if os.path.exists(path):
                return path
    
    elif platform.system() == "Darwin":  # macOS
        # Common paths on macOS
        for path in [
            "/etc/ssl/cert.pem",
            "/usr/local/etc/openssl/cert.pem",
        ]:
            if os.path.exists(path):
                return path
    
    # Default to certifi's location if system location can't be determined
    return "(system default, location unknown)"


def _is_cert_valid(cert_path: str) -> bool:
    """
    Check if a certificate file exists and is valid.
    
    Args:
        cert_path: Path to certificate file
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not os.path.exists(cert_path):
        return False
    
    try:
        # Try to create an SSL context with this certificate
        context = ssl.create_default_context(cafile=cert_path)
        return True
    except Exception as e:
        logger.debug(f"Certificate validation failed for {cert_path}: {e}")
        return False


def set_cert_verify_mode(mode: str = "default", path: Optional[str] = None) -> Dict[str, Any]:
    """
    Set the global certificate verification mode for the process.
    
    Args:
        mode: Verification mode:
            - "default": Use system's CA bundle
            - "platform": Use certifi's CA bundle (recommended)
            - "disabled": Disable certificate verification (insecure)
            - "auto": Automatically detect and fix issues
            - Any path: Use a custom CA bundle file
        path: Optional path to custom CA bundle (overrides path in mode)
        
    Returns:
        Dict[str, Any]: Information about what was configured
    """
    global _applied_fixes
    result = {
        "mode": mode,
        "applied_fixes": [],
        "status": "success",
        "path": None,
    }
    
    # If path is provided, it takes precedence
    if path and os.path.exists(path):
        mode = path
    
    if mode == "default":
        # Default behavior - use system's CA bundle
        if "REQUESTS_CA_BUNDLE" in os.environ:
            del os.environ["REQUESTS_CA_BUNDLE"]
        if "SSL_CERT_FILE" in os.environ:
            del os.environ["SSL_CERT_FILE"]
        
        # Reset urllib3 to default
        try:
            urllib3.util.ssl_.DEFAULT_CIPHERS = "DEFAULT:@SECLEVEL=2"
        except AttributeError:
            pass
            
        result["path"] = _get_system_ca_path()
        result["applied_fixes"].append("reset_to_system_defaults")
        _applied_fixes.add("default")
        
    elif mode == "platform":
        # Use certifi's CA bundle
        cert_path = certifi.where()
        os.environ["REQUESTS_CA_BUNDLE"] = cert_path
        os.environ["SSL_CERT_FILE"] = cert_path
        
        # Update other libraries if available
        try:
            # Set the default for httpx
            os.environ["HTTPX_CA_CERTS"] = cert_path
            result["applied_fixes"].append("httpx_env_var_set")
        except Exception:
            pass
            
        # Update urllib3 pool manager if possible
        try:
            # Create a new pool manager with the certifi CA bundle
            temp_pool = urllib3.PoolManager(
                cert_reqs="CERT_REQUIRED",
                ca_certs=cert_path
            )
            # This doesn't actually replace the global pool manager
            # but is used as an example for client libraries
            result["applied_fixes"].append("urllib3_example_pool_created")
        except Exception:
            pass
            
        result["path"] = cert_path
        result["applied_fixes"].append("certifi_ca_bundle_set")
        _applied_fixes.add("platform")
        
    elif mode == "disabled":
        # Disable certificate verification (insecure)
        logger.warning(
            "Certificate verification has been DISABLED. This is INSECURE and "
            "should ONLY be used in development environments."
        )
        
        # Set empty environment variables to disable verification
        os.environ["REQUESTS_CA_BUNDLE"] = ""
        os.environ["SSL_CERT_FILE"] = ""
        
        # Disable warnings from urllib3
        urllib3.disable_warnings()
        
        # Try to set default for httpx
        try:
            os.environ["HTTPX_CA_CERTS"] = ""
            result["applied_fixes"].append("httpx_env_var_unset")
        except Exception:
            pass
            
        # Update urllib3 pool manager if possible
        try:
            # Create a new pool manager with verification disabled
            temp_pool = urllib3.PoolManager(
                cert_reqs="CERT_NONE",
                ca_certs=None
            )
            result["applied_fixes"].append("urllib3_example_pool_created_unverified")
        except Exception:
            pass
            
        result["path"] = None
        result["applied_fixes"].append("verification_disabled")
        _applied_fixes.add("disabled")
        
    elif mode == "auto":
        # Auto-detect and fix issues by trying different approaches
        result = auto_configure_ssl()
        
    elif Path(mode).exists():
        # Use a custom CA bundle
        cert_path = str(Path(mode).absolute())
        logger.info(f"Using custom CA bundle: {cert_path}")
        
        # Validate the certificate file
        if not _is_cert_valid(cert_path):
            logger.warning(f"The specified certificate file may not be valid: {cert_path}")
            result["warnings"] = ["certificate_validation_failed"]
            
        os.environ["REQUESTS_CA_BUNDLE"] = cert_path
        os.environ["SSL_CERT_FILE"] = cert_path
        
        # Try to set default for httpx
        try:
            os.environ["HTTPX_CA_CERTS"] = cert_path
            result["applied_fixes"].append("httpx_env_var_set")
        except Exception:
            pass
            
        # Update urllib3 pool manager if possible
        try:
            # Create a new pool manager with the custom CA bundle
            temp_pool = urllib3.PoolManager(
                cert_reqs="CERT_REQUIRED",
                ca_certs=cert_path
            )
            result["applied_fixes"].append("urllib3_example_pool_created")
        except Exception:
            pass
            
        result["path"] = cert_path
        result["applied_fixes"].append("custom_ca_bundle_set")
        _applied_fixes.add(f"custom:{cert_path}")
        
    else:
        # Invalid mode
        logger.error(f"Invalid certificate verification mode: {mode}")
        result["status"] = "error"
        result["error"] = f"Invalid verification mode: {mode}"
        return result
        
    # Log what was configured
    logger.info(f"Certificate verification configured: mode={mode}, path={result['path']}")
    return result


def create_ssl_context(
    verify: Union[bool, str] = True,
    cert_file: Optional[str] = None,
    key_file: Optional[str] = None
) -> ssl.SSLContext:
    """
    Create a custom SSL context for certificate verification.
    
    Args:
        verify: Verification mode:
            - True: Verify certificates (default)
            - False: Disable verification (insecure)
            - path string: Use a custom CA bundle
        cert_file: Path to client certificate file
        key_file: Path to client key file
        
    Returns:
        ssl.SSLContext: Configured SSL context
    """
    if verify is True:
        # Use certifi's CA bundle for verification (most secure option)
        context = ssl.create_default_context(cafile=certifi.where())
        
    elif verify is False:
        # Disable verification (insecure)
        logger.warning(
            "Certificate verification has been DISABLED for this context. "
            "This is INSECURE and should ONLY be used in development environments."
        )
        context = ssl._create_unverified_context()
        
    elif isinstance(verify, str) and Path(verify).exists():
        # Use a custom CA bundle
        logger.info(f"Using custom CA bundle: {verify}")
        context = ssl.create_default_context(cafile=verify)
        
    else:
        # Invalid verification mode
        logger.error(f"Invalid verification mode: {verify}")
        raise ValueError(f"Invalid verification mode: {verify}")
    
    # Add client certificate and key if provided
    if cert_file:
        if not Path(cert_file).exists():
            logger.error(f"Client certificate file not found: {cert_file}")
            raise FileNotFoundError(f"Client certificate file not found: {cert_file}")
        
        if key_file and not Path(key_file).exists():
            logger.error(f"Client key file not found: {key_file}")
            raise FileNotFoundError(f"Client key file not found: {key_file}")
        
        context.load_cert_chain(cert_file, key_file)
    
    return context


def create_requests_session(
    verify: Union[bool, str] = True,
    cert: Optional[Union[str, Tuple[str, str]]] = None
) -> requests.Session:
    """
    Create a requests session with custom certificate verification.
    
    Args:
        verify: Verification mode:
            - True: Verify certificates (default)
            - False: Disable verification (insecure)
            - path string: Use a custom CA bundle
        cert: Client certificate:
            - Path to client certificate and key as a single file
            - Tuple of (cert_file, key_file) paths
            
    Returns:
        requests.Session: Configured requests session
    """
    session = requests.Session()
    
    # Set verification mode
    if verify is True:
        # Use certifi's CA bundle (most secure option)
        session.verify = certifi.where()
        
    elif verify is False:
        # Disable verification (insecure)
        logger.warning(
            "Certificate verification has been DISABLED for this session. "
            "This is INSECURE and should ONLY be used in development environments."
        )
        session.verify = False
        urllib3.disable_warnings()
        
    elif isinstance(verify, str) and Path(verify).exists():
        # Use a custom CA bundle
        logger.info(f"Using custom CA bundle: {verify}")
        session.verify = verify
        
    else:
        # Invalid verification mode
        logger.error(f"Invalid verification mode: {verify}")
        raise ValueError(f"Invalid verification mode: {verify}")
    
    # Set client certificate if provided
    if cert:
        session.cert = cert
    
    return session


def check_server_certificate(
    host: str,
    port: int = 443,
    timeout: int = 10,
    verify: Union[bool, str] = True
) -> Dict[str, Any]:
    """
    Check the server's SSL/TLS certificate.
    
    Args:
        host: Hostname to check
        port: Port to connect to
        timeout: Connection timeout in seconds
        verify: Verification mode
        
    Returns:
        Dict[str, Any]: Certificate information
    """
    try:
        # Create context based on verify mode
        if verify is True:
            context = ssl.create_default_context(cafile=certifi.where())
        elif verify is False:
            context = ssl._create_unverified_context()
        elif isinstance(verify, str) and Path(verify).exists():
            context = ssl.create_default_context(cafile=verify)
        else:
            logger.error(f"Invalid verification mode: {verify}")
            raise ValueError(f"Invalid verification mode: {verify}")
        
        # Connect to the server
        with socket.create_connection((host, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssl_sock:
                # Get certificate information
                cert = ssl_sock.getpeercert()
                cipher = ssl_sock.cipher()
                version = ssl_sock.version()
                
                # Parse certificate fields
                valid_from = datetime.strptime(cert["notBefore"], "%b %d %H:%M:%S %Y %Z")
                valid_to = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
                now = datetime.now()
                
                # Extract subject and issuer
                subject = {item[0][0]: item[0][1] for item in cert.get("subject", [])}
                issuer = {item[0][0]: item[0][1] for item in cert.get("issuer", [])}
                
                # Check certificate hostname
                try:
                    ssl.match_hostname(cert, host)
                    hostname_matches = True
                except ssl.CertificateError:
                    hostname_matches = False
                
                return {
                    "valid": True,
                    "subject": subject,
                    "issuer": issuer,
                    "valid_from": valid_from.isoformat(),
                    "valid_to": valid_to.isoformat(),
                    "expired": now > valid_to,
                    "not_yet_valid": now < valid_from,
                    "hostname_matches": hostname_matches,
                    "cipher": cipher,
                    "version": version,
                    "verify_mode": "certifi" if verify is True else 
                                  "disabled" if verify is False else 
                                  f"custom: {verify}"
                }
                
    except ssl.SSLError as e:
        return {
            "valid": False,
            "error": "ssl_error",
            "message": str(e),
            "verify_mode": "certifi" if verify is True else 
                          "disabled" if verify is False else 
                          f"custom: {verify}"
        }
    except socket.gaierror as e:
        return {
            "valid": False,
            "error": "dns_error",
            "message": str(e),
            "verify_mode": "certifi" if verify is True else 
                          "disabled" if verify is False else 
                          f"custom: {verify}"
        }
    except socket.timeout as e:
        return {
            "valid": False,
            "error": "timeout",
            "message": str(e),
            "verify_mode": "certifi" if verify is True else 
                          "disabled" if verify is False else 
                          f"custom: {verify}"
        }
    except Exception as e:
        return {
            "valid": False,
            "error": "unknown_error",
            "message": str(e),
            "verify_mode": "certifi" if verify is True else 
                          "disabled" if verify is False else 
                          f"custom: {verify}"
        }


def check_url_certificate(url: str, verify: Union[bool, str] = True) -> Dict[str, Any]:
    """
    Check the certificate of a URL using requests.
    
    Args:
        url: URL to check
        verify: Verification mode
        
    Returns:
        Dict[str, Any]: Certificate check results
    """
    if not url.startswith("https://"):
        return {"valid": False, "error": "not_https", "message": "URL is not HTTPS"}
    
    try:
        # Create session with custom verification
        session = create_requests_session(verify=verify)
        
        # Make a HEAD request to the URL
        response = session.head(url, timeout=10, allow_redirects=True)
        
        # Check if the request was successful
        return {
            "valid": True,
            "status_code": response.status_code,
            "url": response.url,
            "redirected": response.url != url,
            "redirect_count": len(response.history),
            "response_time_ms": int(response.elapsed.total_seconds() * 1000),
            "verify_mode": "certifi" if verify is True else 
                          "disabled" if verify is False else 
                          f"custom: {verify}"
        }
        
    except requests.exceptions.SSLError as e:
        return {
            "valid": False,
            "error": "ssl_error",
            "message": str(e),
            "verify_mode": "certifi" if verify is True else 
                          "disabled" if verify is False else 
                          f"custom: {verify}"
        }
    except requests.exceptions.ConnectionError as e:
        return {
            "valid": False,
            "error": "connection_error",
            "message": str(e),
            "verify_mode": "certifi" if verify is True else 
                          "disabled" if verify is False else 
                          f"custom: {verify}"
        }
    except requests.exceptions.Timeout as e:
        return {
            "valid": False,
            "error": "timeout",
            "message": str(e),
            "verify_mode": "certifi" if verify is True else 
                          "disabled" if verify is False else 
                          f"custom: {verify}"
        }
    except Exception as e:
        return {
            "valid": False,
            "error": "unknown_error",
            "message": str(e),
            "verify_mode": "certifi" if verify is True else 
                          "disabled" if verify is False else 
                          f"custom: {verify}"
        }


def check_keycloak_certificate(
    keycloak_url: str,
    verify: Union[bool, str] = True
) -> Dict[str, Any]:
    """
    Check the certificate of a Keycloak URL.
    
    Args:
        keycloak_url: Keycloak URL
        verify: Verification mode
        
    Returns:
        Dict[str, Any]: Certificate check results
    """
    if not keycloak_url.startswith("https://"):
        return {"valid": True, "error": "not_https", "message": "URL is not HTTPS, no certificate to check"}
    
    # Extract hostname and port
    hostname = keycloak_url.split("//")[1].split("/")[0]
    if ":" in hostname:
        hostname, port_str = hostname.split(":")
        port = int(port_str)
    else:
        port = 443
    
    # Check the certificate
    cert_info = check_server_certificate(hostname, port, verify=verify)
    
    # Also check the URL with requests
    url_info = check_url_certificate(keycloak_url, verify=verify)
    
    # Combine the results
    results = {
        "valid": cert_info.get("valid", False) and url_info.get("valid", False),
        "cert_check": cert_info,
        "url_check": url_info,
        "keycloak_url": keycloak_url,
        "hostname": hostname,
        "port": port,
    }
    
    # Add common issues
    issues = []
    
    if "error" in cert_info:
        issues.append(f"Certificate error: {cert_info['error']} - {cert_info.get('message', '')}")
    
    if "error" in url_info and url_info["error"] != "not_https":
        issues.append(f"URL error: {url_info['error']} - {url_info.get('message', '')}")
    
    if cert_info.get("expired", False):
        issues.append("Certificate is expired")
    
    if cert_info.get("not_yet_valid", False):
        issues.append("Certificate is not yet valid")
    
    if cert_info.get("hostname_matches") is False:
        issues.append(f"Certificate hostname does not match {hostname}")
    
    results["issues"] = issues
    results["has_issues"] = len(issues) > 0
    
    # Add suggestions for fixing the issues
    if results["has_issues"]:
        results["suggestions"] = generate_certificate_suggestions(issues)
    
    return results


def generate_certificate_suggestions(issues: List[str]) -> List[str]:
    """
    Generate suggestions for fixing certificate issues.
    
    Args:
        issues: List of certificate issues
        
    Returns:
        List[str]: Suggestions for fixing the issues
    """
    suggestions = []
    
    # Analyze each issue and provide suggestions
    for issue in issues:
        if "certificate verify failed" in issue.lower():
            suggestions.append(
                "Try setting cert_verify_mode='platform' to use certifi's CA bundle"
            )
            suggestions.append(
                "For development environments, you can use cert_verify_mode='disabled' (insecure)"
            )
            
        elif "hostname doesn't match" in issue.lower() or "hostname_matches" in issue.lower():
            suggestions.append(
                "The server certificate doesn't match the hostname. This could be due to:"
            )
            suggestions.append(
                "- Incorrect hostname in the URL"
            )
            suggestions.append(
                "- Misconfigured server certificate"
            )
            suggestions.append(
                "For development, you can use cert_verify_mode='disabled' to bypass this check (insecure)"
            )
            
        elif "expired" in issue.lower():
            suggestions.append(
                "The server certificate has expired. Contact the server administrator."
            )
            suggestions.append(
                "For development, you can use cert_verify_mode='disabled' to bypass this check (insecure)"
            )
            
        elif "not_yet_valid" in issue.lower():
            suggestions.append(
                "The server certificate is not yet valid (check your system clock)."
            )
            
        elif "connection_error" in issue.lower():
            suggestions.append(
                "Unable to connect to the server. Check that it's running and accessible."
            )
            suggestions.append(
                "If using a local Keycloak server, make sure it's running and the URL is correct."
            )
    
    # Add general suggestions
    if not suggestions:
        suggestions.append(
            "Try running auto_configure_ssl() to automatically fix certificate issues"
        )
        suggestions.append(
            "For development environments, you can use cert_verify_mode='disabled' (insecure)"
        )
    
    # Add the auto configuration option if not already suggested
    has_auto_suggest = any(
        "auto_configure_ssl" in suggestion for suggestion in suggestions
    )
    if not has_auto_suggest:
        suggestions.append(
            "Try running auto_configure_ssl() to automatically fix certificate issues"
        )
    
    return suggestions


def extract_server_certificate(url: str, output_path: Optional[str] = None) -> Optional[str]:
    """
    Extract the server's certificate to a file.
    
    Args:
        url: HTTPS URL to extract certificate from
        output_path: Path to save the certificate (optional)
        
    Returns:
        Optional[str]: Path to the saved certificate or None if failed
    """
    if not url.startswith("https://"):
        logger.error("URL must use HTTPS protocol")
        return None
    
    # Extract hostname and port
    hostname = url.split("//")[1].split("/")[0]
    if ":" in hostname:
        hostname, port_str = hostname.split(":")
        port = int(port_str)
    else:
        port = 443
    
    # Create a temporary file if no output path is provided
    if not output_path:
        fd, output_path = tempfile.mkstemp(suffix=".pem", prefix=f"{hostname}-cert-")
        os.close(fd)
    
    try:
        # Create an unverified context to get the certificate
        context = ssl._create_unverified_context()
        
        with socket.create_connection((hostname, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssl_sock:
                # Get the binary certificate
                der_cert = ssl_sock.getpeercert(binary_form=True)
                
                # Convert to PEM format
                from cryptography.hazmat.primitives.serialization import Encoding
                from cryptography.x509 import load_der_x509_certificate
                
                cert = load_der_x509_certificate(der_cert)
                pem_cert = cert.public_bytes(Encoding.PEM).decode("ascii")
                
                # Save to file
                with open(output_path, "w") as f:
                    f.write(pem_cert)
                
                logger.info(f"Certificate extracted and saved to {output_path}")
                return output_path
                
    except ImportError:
        # Try using OpenSSL command-line tool as fallback
        return _extract_cert_with_openssl(hostname, port, output_path)
        
    except Exception as e:
        logger.error(f"Failed to extract certificate: {str(e)}")
        return None


def _extract_cert_with_openssl(hostname: str, port: int, output_path: str) -> Optional[str]:
    """
    Extract certificate using the OpenSSL command-line tool.
    
    Args:
        hostname: Server hostname
        port: Server port
        output_path: Path to save the certificate
        
    Returns:
        Optional[str]: Path to the saved certificate or None if failed
    """
    try:
        cmd = [
            "openssl", "s_client",
            "-connect", f"{hostname}:{port}",
            "-servername", hostname,
            "-showcerts"
        ]
        
        # Run OpenSSL command
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Send EOF and get output
        stdout, stderr = process.communicate(b"\n")
        if process.returncode != 0:
            logger.error(f"OpenSSL command failed: {stderr.decode()}")
            return None
        
        # Extract and save the certificate
        cert_data = stdout.decode()
        cert_start = "-----BEGIN CERTIFICATE-----"
        cert_end = "-----END CERTIFICATE-----"
        
        start_idx = cert_data.find(cert_start)
        if start_idx == -1:
            logger.error("No certificate found in OpenSSL output")
            return None
        
        end_idx = cert_data.find(cert_end, start_idx) + len(cert_end)
        certificate = cert_data[start_idx:end_idx]
        
        with open(output_path, "w") as f:
            f.write(certificate)
        
        logger.info(f"Certificate extracted with OpenSSL and saved to {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Failed to extract certificate with OpenSSL: {str(e)}")
        return None


def auto_configure_ssl() -> Dict[str, Any]:
    """
    Automatically detect and fix SSL certificate issues.
    
    This function tries different certificate verification modes
    to find one that works, prioritizing security where possible.
    
    Returns:
        Dict[str, Any]: Results of the auto-configuration
    """
    result = {
        "mode": "auto",
        "detected_issues": [],
        "applied_fixes": [],
        "status": "success",
        "path": None,
        "test_results": {},
    }
    
    # Test URL to check connectivity (using common HTTPS endpoints)
    test_urls = [
        "https://www.google.com",
        "https://www.microsoft.com",
        "https://www.cloudflare.com",
    ]
    
    # Step 1: Test with system default settings
    logger.info("Auto-configure: Testing with system default settings")
    set_cert_verify_mode("default")
    
    system_results = {}
    system_success = True
    
    for url in test_urls:
        check = check_url_certificate(url, verify=True)
        system_results[url] = check
        if not check["valid"]:
            system_success = False
            result["detected_issues"].append(f"System CA bundle failed for {url}: {check.get('error')}")
    
    result["test_results"]["system_default"] = system_results
    
    # If system settings work, we're done
    if system_success:
        logger.info("Auto-configure: System default settings work correctly")
        result["path"] = _get_system_ca_path()
        result["applied_fixes"].append("using_system_defaults")
        return result
    
    # Step 2: Try using certifi's CA bundle
    logger.info("Auto-configure: Testing with certifi's CA bundle")
    set_cert_verify_mode("platform")
    
    certifi_results = {}
    certifi_success = True
    
    for url in test_urls:
        check = check_url_certificate(url, verify=certifi.where())
        certifi_results[url] = check
        if not check["valid"]:
            certifi_success = False
            result["detected_issues"].append(f"Certifi CA bundle failed for {url}: {check.get('error')}")
    
    result["test_results"]["certifi"] = certifi_results
    
    # If certifi works, use it
    if certifi_success:
        logger.info("Auto-configure: Certifi CA bundle works correctly")
        result["path"] = certifi.where()
        result["applied_fixes"].append("using_certifi_ca_bundle")
        result["mode"] = "platform"
        return result
    
    # Step 3: For development-only or testing, offer to disable verification
    logger.warning(
        "Auto-configure: Both system default and certifi CA bundles failed. "
        "In development environments, you can disable verification entirely (insecure)."
    )
    
    # Test with verification disabled
    disabled_results = {}
    
    for url in test_urls:
        check = check_url_certificate(url, verify=False)
        disabled_results[url] = check
    
    result["test_results"]["disabled"] = disabled_results
    
    # Recommend disabling verification for development only
    result["detected_issues"].append("All certificate verification methods failed")
    result["status"] = "partial_success"
    result["recommendations"] = [
        "For development environments, use cert_verify_mode='disabled' (insecure)",
        "For production, fix your system's CA certificates or provide a custom CA bundle",
    ]
    
    # Return without actually applying the insecure setting
    # Let the user decide whether to use it
    return result


def fix_certificate_issues(mode: str = "platform", keycloak_url: Optional[str] = None) -> Dict[str, Any]:
    """
    Fix common certificate issues by setting the verification mode.
    
    Args:
        mode: Verification mode:
            - "platform": Use certifi's CA bundle (recommended)
            - "disabled": Disable certificate verification (insecure)
            - "auto": Automatically detect and fix issues
            - any path: Use a custom CA bundle
        keycloak_url: Optional Keycloak URL to test after fixing
        
    Returns:
        Dict[str, Any]: Results of the fix operation
    """
    result = {
        "success": True,
        "mode": mode,
        "keycloak_test": None,
    }
    
    # Apply the fix
    fix_result = set_cert_verify_mode(mode)
    result.update(fix_result)
    
    # Test Keycloak URL if provided
    if keycloak_url and keycloak_url.startswith("https://"):
        try:
            keycloak_test = check_keycloak_certificate(keycloak_url, verify=(mode != "disabled"))
            result["keycloak_test"] = {
                "url": keycloak_url,
                "success": keycloak_test["valid"],
                "issues": keycloak_test.get("issues", [])
            }
            
            # If test failed but mode is "auto", try other modes
            if not keycloak_test["valid"] and mode == "auto":
                logger.info("Auto mode: Keycloak test failed, trying platform mode")
                set_cert_verify_mode("platform")
                
                platform_test = check_keycloak_certificate(keycloak_url, verify=True)
                if platform_test["valid"]:
                    result["keycloak_test"]["success"] = True
                    result["keycloak_test"]["issues"] = []
                    result["mode"] = "platform"
                    result["applied_fixes"].append("fallback_to_platform_mode")
                else:
                    # As a last resort for development, try disabled mode
                    logger.warning("Auto mode: Platform mode failed, trying disabled mode (insecure)")
                    set_cert_verify_mode("disabled")
                    
                    disabled_test = check_keycloak_certificate(keycloak_url, verify=False)
                    if disabled_test["valid"]:
                        result["keycloak_test"]["success"] = True
                        result["keycloak_test"]["issues"] = ["Using insecure mode (verification disabled)"]
                        result["mode"] = "disabled"
                        result["applied_fixes"].append("fallback_to_disabled_mode")
                        result["warnings"] = ["Using insecure mode with verification disabled"]
        except Exception as e:
            result["keycloak_test"] = {
                "url": keycloak_url,
                "success": False,
                "error": str(e)
            }
    
    return result


def get_applied_fixes() -> Set[str]:
    """
    Get the list of certificate fixes that have been applied.
    
    Returns:
        Set[str]: Set of applied fixes
    """
    return _applied_fixes.copy()


def diagnostic_report() -> Dict[str, Any]:
    """
    Generate a diagnostic report about the SSL/certificate configuration.
    
    Returns:
        Dict[str, Any]: Diagnostic information
    """
    report = {
        "platform": {
            "system": platform.system(),
            "python_version": platform.python_version(),
            "implementation": platform.python_implementation(),
            "ssl_version": ssl.OPENSSL_VERSION,
        },
        "certificate_stores": get_available_certificate_stores(),
        "environment_variables": {
            "REQUESTS_CA_BUNDLE": os.environ.get("REQUESTS_CA_BUNDLE", "(not set)"),
            "SSL_CERT_FILE": os.environ.get("SSL_CERT_FILE", "(not set)"),
            "HTTPX_CA_CERTS": os.environ.get("HTTPX_CA_CERTS", "(not set)"),
        },
        "applied_fixes": list(get_applied_fixes()),
        "tests": {},
    }
    
    # Test system behavior with different verification modes
    report["tests"]["default"] = {}
    report["tests"]["certifi"] = {}
    report["tests"]["disabled"] = {}
    
    # Use common HTTPS websites for testing
    test_urls = [
        "https://www.google.com",
        "https://www.microsoft.com",
    ]
    
    # Test with system defaults
    set_cert_verify_mode("default")
    for url in test_urls:
        try:
            report["tests"]["default"][url] = check_url_certificate(url, verify=True)
        except Exception as e:
            report["tests"]["default"][url] = {"error": str(e), "valid": False}
    
    # Test with certifi
    set_cert_verify_mode("platform")
    for url in test_urls:
        try:
            report["tests"]["certifi"][url] = check_url_certificate(url, verify=True)
        except Exception as e:
            report["tests"]["certifi"][url] = {"error": str(e), "valid": False}
    
    # Test with verification disabled
    set_cert_verify_mode("disabled")
    for url in test_urls:
        try:
            report["tests"]["disabled"][url] = check_url_certificate(url, verify=False)
        except Exception as e:
            report["tests"]["disabled"][url] = {"error": str(e), "valid": False}
    
    # Restore platform mode as the most secure default
    set_cert_verify_mode("platform")
    
    # Generate recommendations
    def are_all_valid(test_results):
        return all(result.get("valid", False) for result in test_results.values())
    
    recommendations = []
    if are_all_valid(report["tests"]["default"]):
        recommendations.append("System default certificate verification works correctly")
        recommendations.append("Recommended setting: cert_verify_mode='default'")
    elif are_all_valid(report["tests"]["certifi"]):
        recommendations.append("Certifi certificate verification works correctly")
        recommendations.append("Recommended setting: cert_verify_mode='platform'")
    elif are_all_valid(report["tests"]["disabled"]):
        recommendations.append("Certificate verification only works when disabled")
        recommendations.append("For development: cert_verify_mode='disabled' (INSECURE)")
        recommendations.append("For production: Fix your system's CA certificates")
    else:
        recommendations.append("All certificate verification methods failed")
        recommendations.append("Try updating your system's CA certificates")
        recommendations.append("Or provide a custom CA bundle with the server's certificate")
    
    report["recommendations"] = recommendations
    
    return report
