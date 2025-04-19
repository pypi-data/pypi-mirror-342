"""
Diagnostic tools for FastAPI-Authlib-Keycloak.

This module provides utilities for diagnosing and troubleshooting
configuration and connectivity issues with Keycloak integration.
"""

import os
import sys
import json
import logging
import platform
import socket
import ssl
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Union

# Check if certifi is available
try:
    import certifi
    CERTIFI_AVAILABLE = True
except ImportError:
    CERTIFI_AVAILABLE = False

# Check if requests is available
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

# Import cert_utils if available
try:
    from fastapi_authlib_keycloak.utils.cert_utils import (
        check_url_certificate,
        check_keycloak_certificate,
        get_available_certificate_stores,
        diagnostic_report as cert_diagnostic_report
    )
    CERT_UTILS_AVAILABLE = True
except ImportError:
    CERT_UTILS_AVAILABLE = False

# Import config model if available
try:
    from fastapi_authlib_keycloak.config_model import (
        KeycloakConfig,
        diagnose_configuration,
        validate_config
    )
    CONFIG_MODEL_AVAILABLE = True
except ImportError:
    CONFIG_MODEL_AVAILABLE = False

# Configure logger
logger = logging.getLogger("fastapi-keycloak.diagnostic")


def check_system_configuration() -> Dict[str, Any]:
    """
    Check the system configuration for potential issues.
    
    Returns:
        Dict[str, Any]: System configuration information and issues
    """
    report = {
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "architecture": platform.machine(),
            "python_version": platform.python_version(),
            "python_implementation": platform.python_implementation(),
        },
        "environment": {
            "ssl_version": ssl.OPENSSL_VERSION if hasattr(ssl, 'OPENSSL_VERSION') else None,
            "ssl_path": os.environ.get("SSL_CERT_FILE", "Not set"),
            "requests_ca_bundle": os.environ.get("REQUESTS_CA_BUNDLE", "Not set"),
            "httpx_ca_certs": os.environ.get("HTTPX_CA_CERTS", "Not set"),
        },
        "libraries": {
            "certifi": CERTIFI_AVAILABLE,
            "requests": REQUESTS_AVAILABLE,
            "cert_utils": CERT_UTILS_AVAILABLE,
            "config_model": CONFIG_MODEL_AVAILABLE,
        },
        "certificate_stores": {},
        "issues": [],
        "recommendations": [],
    }
    
    # Check certificate stores
    if CERT_UTILS_AVAILABLE:
        report["certificate_stores"] = get_available_certificate_stores()
    elif CERTIFI_AVAILABLE:
        report["certificate_stores"]["certifi"] = certifi.where()
    
    # Check for common issues
    if not CERTIFI_AVAILABLE:
        report["issues"].append("certifi library not installed")
        report["recommendations"].append("Install certifi: pip install certifi")
    
    if not REQUESTS_AVAILABLE:
        report["issues"].append("requests library not installed")
        report["recommendations"].append("Install requests: pip install requests")
    
    # Check SSL configuration
    if ssl.OPENSSL_VERSION.startswith("OpenSSL 1.0") and platform.system() == "Linux":
        report["issues"].append("Outdated OpenSSL version detected")
        report["recommendations"].append("Consider upgrading OpenSSL to version 1.1.1 or later")
    
    # Check environment variables
    if report["environment"]["ssl_path"] == "Not set":
        report["issues"].append("SSL_CERT_FILE environment variable not set")
        if CERTIFI_AVAILABLE:
            report["recommendations"].append(f"Set SSL_CERT_FILE environment variable to {certifi.where()}")
    
    if report["environment"]["requests_ca_bundle"] == "Not set":
        report["issues"].append("REQUESTS_CA_BUNDLE environment variable not set")
        if CERTIFI_AVAILABLE:
            report["recommendations"].append(f"Set REQUESTS_CA_BUNDLE environment variable to {certifi.where()}")
    
    # Test basic HTTPS connectivity
    try:
        test_url = "https://www.google.com"
        if REQUESTS_AVAILABLE:
            response = requests.head(test_url, timeout=5)
            report["https_connectivity"] = {
                "success": response.status_code < 400,
                "status_code": response.status_code,
                "response_time_ms": int(response.elapsed.total_seconds() * 1000),
            }
        else:
            # Fallback to socket-based check
            hostname = "www.google.com"
            context = ssl.create_default_context()
            with socket.create_connection((hostname, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssl_sock:
                    report["https_connectivity"] = {
                        "success": True,
                        "protocol": ssl_sock.version(),
                    }
    except Exception as e:
        report["https_connectivity"] = {
            "success": False,
            "error": str(e),
        }
        report["issues"].append(f"Basic HTTPS connectivity test failed: {str(e)}")
        report["recommendations"].append("Check your internet connection and SSL configuration")
    
    return report


def test_keycloak_connectivity(
    keycloak_url: str,
    keycloak_realm: str,
    ssl_verify: Union[bool, str] = True,
    timeout: int = 10
) -> Dict[str, Any]:
    """
    Test connectivity to essential Keycloak endpoints.
    
    Args:
        keycloak_url: Keycloak server URL
        keycloak_realm: Keycloak realm name
        ssl_verify: SSL verification mode
        timeout: Connection timeout in seconds
        
    Returns:
        Dict[str, Any]: Connectivity test results
    """
    report = {
        "keycloak_url": keycloak_url,
        "keycloak_realm": keycloak_realm,
        "ssl_verify": ssl_verify,
        "endpoints": {},
        "issues": [],
        "success": True,
    }
    
    # Define essential endpoints to test
    endpoints = {
        "realm": f"{keycloak_url}/realms/{keycloak_realm}",
        "openid_configuration": f"{keycloak_url}/realms/{keycloak_realm}/.well-known/openid-configuration",
        "jwks": f"{keycloak_url}/realms/{keycloak_realm}/protocol/openid-connect/certs",
        "token": f"{keycloak_url}/realms/{keycloak_realm}/protocol/openid-connect/token",
    }
    
    # Test each endpoint
    for name, url in endpoints.items():
        try:
            if REQUESTS_AVAILABLE:
                # Use requests library if available
                response = requests.get(url, verify=ssl_verify, timeout=timeout)
                result = {
                    "url": url,
                    "success": response.status_code < 400,
                    "status_code": response.status_code,
                    "response_time_ms": int(response.elapsed.total_seconds() * 1000),
                }
                
                if response.status_code >= 400:
                    report["issues"].append(f"Endpoint {name} returned status code {response.status_code}")
                    report["success"] = False
                    
            elif url.startswith("https://"):
                # Fallback to socket-based check for HTTPS
                hostname = url.split("//")[1].split("/")[0]
                path = "/" + "/".join(url.split("/")[3:])
                
                context = ssl.create_default_context()
                if ssl_verify is False:
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                elif isinstance(ssl_verify, str):
                    context = ssl.create_default_context(cafile=ssl_verify)
                
                with socket.create_connection((hostname, 443), timeout=timeout) as sock:
                    with context.wrap_socket(sock, server_hostname=hostname) as ssl_sock:
                        # Send HTTP request
                        request = f"GET {path} HTTP/1.1\r\nHost: {hostname}\r\n\r\n"
                        ssl_sock.send(request.encode())
                        
                        # Get response status line
                        response = ssl_sock.recv(4096).decode()
                        status_line = response.split("\r\n")[0]
                        status_code = int(status_line.split(" ")[1])
                        
                        result = {
                            "url": url,
                            "success": status_code < 400,
                            "status_code": status_code,
                        }
                        
                        if status_code >= 400:
                            report["issues"].append(f"Endpoint {name} returned status code {status_code}")
                            report["success"] = False
            else:
                # Fallback to socket-based check for HTTP
                hostname = url.split("//")[1].split("/")[0]
                path = "/" + "/".join(url.split("/")[3:])
                
                with socket.create_connection((hostname, 80), timeout=timeout) as sock:
                    # Send HTTP request
                    request = f"GET {path} HTTP/1.1\r\nHost: {hostname}\r\n\r\n"
                    sock.send(request.encode())
                    
                    # Get response status line
                    response = sock.recv(4096).decode()
                    status_line = response.split("\r\n")[0]
                    status_code = int(status_line.split(" ")[1])
                    
                    result = {
                        "url": url,
                        "success": status_code < 400,
                        "status_code": status_code,
                    }
                    
                    if status_code >= 400:
                        report["issues"].append(f"Endpoint {name} returned status code {status_code}")
                        report["success"] = False
                        
        except Exception as e:
            result = {
                "url": url,
                "success": False,
                "error": str(e),
            }
            report["issues"].append(f"Failed to connect to {name} endpoint: {str(e)}")
            report["success"] = False
        
        report["endpoints"][name] = result
    
    # Check SSL certificate if using HTTPS
    if keycloak_url.startswith("https://") and CERT_UTILS_AVAILABLE:
        cert_check = check_keycloak_certificate(keycloak_url, verify=ssl_verify)
        report["certificate"] = cert_check
        
        if not cert_check["valid"]:
            report["issues"].extend(cert_check.get("issues", []))
            report["success"] = False
    
    return report


def analyze_common_issues(report: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze diagnostic report and identify common issues with solutions.
    
    Args:
        report: Diagnostic report
        
    Returns:
        Dict[str, Any]: Analysis with issues and solutions
    """
    analysis = {
        "detected_issues": [],
        "recommendations": [],
    }
    
    # Check for certificate issues
    cert_issues = [issue for issue in report.get("issues", []) if "certificate" in issue.lower() or "ssl" in issue.lower()]
    if cert_issues:
        analysis["detected_issues"].append({
            "type": "certificate",
            "description": "SSL/TLS certificate issues detected",
            "details": cert_issues,
        })
        
        analysis["recommendations"].append({
            "title": "Fix certificate issues",
            "steps": [
                "Set cert_verify_mode='platform' to use certifi's CA bundle",
                "For development, you can use cert_verify_mode='disabled' (insecure)",
                "For custom CA, provide the path: cert_verify_mode='/path/to/ca.pem'",
            ],
            "code_example": """
# Example for fixing certificate issues
from fastapi_authlib_keycloak.utils.cert_utils import fix_certificate_issues

# Use platform mode (recommended)
fix_certificate_issues(mode="platform")

# OR for development only:
fix_certificate_issues(mode="disabled")
            """,
        })
    
    # Check for connectivity issues
    if "endpoints" in report and any(not endpoint.get("success", False) for endpoint in report["endpoints"].values()):
        failed_endpoints = [name for name, endpoint in report["endpoints"].items() if not endpoint.get("success", False)]
        
        analysis["detected_issues"].append({
            "type": "connectivity",
            "description": "Failed to connect to Keycloak endpoints",
            "details": [f"Failed endpoints: {', '.join(failed_endpoints)}"],
        })
        
        analysis["recommendations"].append({
            "title": "Fix connectivity issues",
            "steps": [
                "Ensure Keycloak server is running and accessible",
                "Check firewall and network settings",
                "Verify the Keycloak URL and realm name are correct",
                "For development, try using 'localhost' instead of '127.0.0.1'",
            ],
        })
    
    # Check for HTTP usage in production
    if "keycloak_url" in report and report["keycloak_url"].startswith("http://") and not report.get("development_mode"):
        analysis["detected_issues"].append({
            "type": "security",
            "description": "Using HTTP for Keycloak URL in non-development mode",
            "details": ["HTTP is insecure and should only be used for development"],
        })
        
        analysis["recommendations"].append({
            "title": "Use HTTPS for production",
            "steps": [
                "Configure Keycloak to use HTTPS",
                "Update the Keycloak URL to use HTTPS",
                "If using HTTP for development, set development_mode=True",
            ],
        })
    
    # Check for issues with development mode in production
    if report.get("development_mode") and not report.get("mock_mode"):
        analysis["detected_issues"].append({
            "type": "security",
            "description": "Development mode enabled in production",
            "details": ["Development mode may use insecure defaults"],
        })
        
        analysis["recommendations"].append({
            "title": "Disable development mode for production",
            "steps": [
                "Set development_mode=False for production environments",
                "Configure secure settings explicitly instead of relying on defaults",
            ],
        })
    
    # Check for missing required configuration
    required_fields = ["keycloak_url", "keycloak_realm", "client_id", "client_secret"]
    missing_fields = [field for field in required_fields if field not in report or not report.get(field)]
    
    if missing_fields:
        analysis["detected_issues"].append({
            "type": "configuration",
            "description": "Missing required configuration fields",
            "details": [f"Missing fields: {', '.join(missing_fields)}"],
        })
        
        analysis["recommendations"].append({
            "title": "Provide required configuration",
            "steps": [
                f"Set {field} in configuration" for field in missing_fields
            ],
            "code_example": """
# Example for providing required configuration
from fastapi_authlib_keycloak.config_model import create_config
from fastapi_authlib_keycloak import KeycloakAuth

config = create_config(
    keycloak_url="https://keycloak.example.com/auth",
    keycloak_realm="your-realm",
    client_id="your-client-id",
    client_secret="your-client-secret"
)

# OR use environment variables:
# KEYCLOAK_URL=https://keycloak.example.com/auth
# KEYCLOAK_REALM=your-realm
# CLIENT_ID=your-client-id
# CLIENT_SECRET=your-client-secret
            """,
        })
    
    return analysis


def run_diagnostic_wizard(
    keycloak_url: Optional[str] = None,
    keycloak_realm: Optional[str] = None,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    development_mode: bool = False,
    mock_mode: bool = False,
    ssl_verify: Union[bool, str] = True,
    verbose: bool = False,
    config: Optional[Any] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Run a comprehensive diagnostic wizard for FastAPI-Authlib-Keycloak.
    
    Args:
        keycloak_url: Keycloak server URL
        keycloak_realm: Keycloak realm name
        client_id: Client ID
        client_secret: Client secret
        development_mode: Whether development mode is enabled
        mock_mode: Whether mock mode is enabled
        ssl_verify: SSL verification mode
        verbose: Whether to include verbose output
        config: Optional configuration object
        **kwargs: Additional configuration options
        
    Returns:
        Dict[str, Any]: Comprehensive diagnostic report
    """
    # Initialize logger
    log_level = logging.DEBUG if verbose else logging.INFO
    logger.setLevel(log_level)
    
    # Create console handler if not already present
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    logger.info("Starting FastAPI-Authlib-Keycloak diagnostic wizard")
    
    # Prepare the diagnostic report
    report = {
        "timestamp": datetime.now().isoformat(),
        "system": check_system_configuration(),
        "config": {},
        "connectivity": {},
        "certificate": {},
        "development_mode": development_mode,
        "mock_mode": mock_mode,
        "issues": [],
        "success": True,
    }
    
    # Extract configuration from config object if provided
    if config is not None:
        if CONFIG_MODEL_AVAILABLE and isinstance(config, KeycloakConfig):
            # Use values from the config object
            keycloak_url = config.keycloak_url
            keycloak_realm = config.keycloak_realm
            client_id = config.client_id
            client_secret = config.client_secret
            development_mode = config.development_mode
            mock_mode = config.mock_mode
            ssl_verify = config.ssl_verify
            
            # Add config diagnostics
            report["config"] = diagnose_configuration(config)
            report["issues"].extend(report["config"].get("issues", []))
            
            # Update success status
            if not report["config"].get("valid", True):
                report["success"] = False
    
    # Add configuration details
    report["keycloak_url"] = keycloak_url
    report["keycloak_realm"] = keycloak_realm
    report["client_id"] = client_id
    if client_secret:
        report["client_secret"] = "***hidden***"  # Hide for security
    
    # Check for missing required configuration
    required_fields = ["keycloak_url", "keycloak_realm", "client_id", "client_secret"]
    missing_fields = []
    
    for field in required_fields:
        value = locals().get(field)
        if not value:
            missing_fields.append(field)
            report["issues"].append(f"{field} is required but not provided")
    
    if missing_fields:
        logger.warning(f"Missing required configuration: {', '.join(missing_fields)}")
        report["success"] = False
    else:
        # Test Keycloak connectivity
        logger.info(f"Testing connectivity to Keycloak server: {keycloak_url}")
        connectivity_report = test_keycloak_connectivity(
            keycloak_url=keycloak_url,
            keycloak_realm=keycloak_realm,
            ssl_verify=ssl_verify
        )
        
        report["connectivity"] = connectivity_report
        report["issues"].extend(connectivity_report.get("issues", []))
        
        # Update success status
        if not connectivity_report.get("success", True):
            report["success"] = False
    
    # Check SSL certificate if using HTTPS
    if keycloak_url and keycloak_url.startswith("https://") and CERT_UTILS_AVAILABLE:
        logger.info("Checking SSL certificate")
        cert_check = check_keycloak_certificate(keycloak_url, verify=ssl_verify)
        report["certificate"] = cert_check
        
        if not cert_check["valid"]:
            report["issues"].extend(cert_check.get("issues", []))
            report["success"] = False
    
    # Get certificate diagnostic report if available
    if CERT_UTILS_AVAILABLE:
        report["certificate_diagnostics"] = cert_diagnostic_report()
    
    # Add verbose system information if requested
    if verbose:
        report["system"]["python_path"] = sys.path
        report["system"]["environment_variables"] = {
            key: value for key, value in os.environ.items()
            if key.startswith(("SSL", "REQUESTS", "HTTPX", "KEYCLOAK", "CLIENT", "API"))
        }
    
    # Analyze common issues and provide recommendations
    analysis = analyze_common_issues(report)
    report["analysis"] = analysis
    
    # Log summary
    if report["success"]:
        logger.info("Diagnostic completed successfully with no critical issues")
    else:
        logger.warning(
            f"Diagnostic completed with {len(report['issues'])} issues. "
            f"See report for details and recommendations."
        )
    
    return report


def print_diagnostic_report(report: Dict[str, Any], format: str = "text") -> None:
    """
    Print a diagnostic report in the specified format.
    
    Args:
        report: Diagnostic report
        format: Output format (text, json, or summary)
    """
    if format == "json":
        # Print as JSON
        print(json.dumps(report, indent=2))
        
    elif format == "summary":
        # Print a brief summary
        print("\n=== FastAPI-Authlib-Keycloak Diagnostic Summary ===")
        print(f"Timestamp: {report['timestamp']}")
        print(f"Success: {report['success']}")
        print(f"Issues: {len(report['issues'])}")
        
        if report["issues"]:
            print("\nDetected Issues:")
            for i, issue in enumerate(report["issues"], 1):
                print(f"{i}. {issue}")
        
        if "analysis" in report and "recommendations" in report["analysis"]:
            print("\nRecommendations:")
            for i, rec in enumerate(report["analysis"]["recommendations"], 1):
                print(f"{i}. {rec['title']}")
                for step in rec.get("steps", []):
                    print(f"   - {step}")
                
        print("\nFor detailed information, use the 'text' or 'json' format.")
        
    else:
        # Print as formatted text
        print("\n====================================================")
        print("=== FastAPI-Authlib-Keycloak Diagnostic Report ===")
        print("====================================================")
        print(f"Timestamp: {report['timestamp']}")
        print(f"Success: {report['success']}")
        print(f"Platform: {report['system']['platform']['system']} {report['system']['platform']['release']}")
        print(f"Python: {report['system']['platform']['python_version']} ({report['system']['platform']['python_implementation']})")
        
        if "keycloak_url" in report:
            print(f"\nKeycloak URL: {report['keycloak_url']}")
            print(f"Keycloak Realm: {report.get('keycloak_realm', 'Not provided')}")
            print(f"Development Mode: {report.get('development_mode', False)}")
            print(f"Mock Mode: {report.get('mock_mode', False)}")
        
        if "connectivity" in report and "endpoints" in report["connectivity"]:
            print("\nEndpoint Connectivity:")
            for name, endpoint in report["connectivity"]["endpoints"].items():
                status = "✓" if endpoint.get("success", False) else "✗"
                print(f"  {status} {name}: {endpoint.get('status_code', 'N/A')}")
        
        if report["issues"]:
            print("\nDetected Issues:")
            for i, issue in enumerate(report["issues"], 1):
                print(f"{i}. {issue}")
        
        if "analysis" in report and "recommendations" in report["analysis"]:
            print("\nRecommendations:")
            for i, rec in enumerate(report["analysis"]["recommendations"], 1):
                print(f"{i}. {rec['title']}")
                for step in rec.get("steps", []):
                    print(f"   - {step}")
                
                if "code_example" in rec:
                    print("\n   Example Code:")
                    print("   " + "\n   ".join(rec["code_example"].strip().split("\n")))
                    print()
        
        if "certificate" in report and "issues" in report["certificate"]:
            print("\nCertificate Issues:")
            for issue in report["certificate"]["issues"]:
                print(f"  - {issue}")
            
            if "suggestions" in report["certificate"]:
                print("\nCertificate Fix Suggestions:")
                for suggestion in report["certificate"]["suggestions"]:
                    print(f"  - {suggestion}")
        
        print("\n====================================================")


def diagnose_command_line() -> None:
    """
    Run the diagnostic wizard from the command line.
    
    This function is designed to be used as an entry point for a
    command-line diagnostic tool.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="FastAPI-Authlib-Keycloak Diagnostic Wizard")
    parser.add_argument("--url", help="Keycloak server URL")
    parser.add_argument("--realm", help="Keycloak realm name")
    parser.add_argument("--client-id", help="Client ID")
    parser.add_argument("--client-secret", help="Client secret")
    parser.add_argument("--development", action="store_true", help="Enable development mode")
    parser.add_argument("--mock", action="store_true", help="Enable mock mode")
    parser.add_argument("--no-verify", action="store_true", help="Disable SSL verification")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--format", choices=["text", "json", "summary"], default="text", help="Output format")
    
    args = parser.parse_args()
    
    # Run the diagnostic wizard
    report = run_diagnostic_wizard(
        keycloak_url=args.url,
        keycloak_realm=args.realm,
        client_id=args.client_id,
        client_secret=args.client_secret,
        development_mode=args.development,
        mock_mode=args.mock,
        ssl_verify=not args.no_verify,
        verbose=args.verbose
    )
    
    # Print the report
    print_diagnostic_report(report, args.format)


if __name__ == "__main__":
    diagnose_command_line()
