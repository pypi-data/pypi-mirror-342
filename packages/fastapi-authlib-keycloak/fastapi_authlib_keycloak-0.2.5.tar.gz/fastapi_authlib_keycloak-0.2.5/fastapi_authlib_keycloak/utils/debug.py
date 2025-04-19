#!/usr/bin/env python3
"""
Debugging utilities for FastAPI-Authlib-Keycloak.

This module provides developer-friendly tools for debugging authentication
and authorization issues, with features like token inspection, certificate
generation, and diagnostic endpoints. These features are primarily intended
for development and testing environments.

Features:
- Token inspection and validation diagnostics
- JWKS inspection and validation
- Self-signed certificate generation for development
- Debug logging utilities
- Development-only debug endpoints
- Mock authentication for testing
"""

import os
import json
import time
import uuid
import base64
import logging
import binascii
import datetime
import tempfile
from enum import Enum
from typing import Dict, List, Optional, Any, Union, Tuple, Set

from fastapi import APIRouter, Depends, HTTPException, Request, status, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# Import conditionally to avoid hard dependencies
try:
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa, padding
    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False

# Try to import JWT libraries
try:
    from authlib.jose import JsonWebToken, JsonWebKey
    from authlib.jose.errors import JoseError, ExpiredTokenError
    AUTHLIB_AVAILABLE = True
except ImportError:
    AUTHLIB_AVAILABLE = False

# Try to import metrics if available
try:
    from fastapi_authlib_keycloak.utils.metrics import (
        increment_counter,
        time_function,
        time_async_function,
        MetricsTimer
    )
    METRICS_AVAILABLE = True
except ImportError:
    METRICS_AVAILABLE = False
    # Create stub functions if metrics not available
    def increment_counter(*args, **kwargs):
        pass
    
    def time_function(*args, **kwargs):
        def decorator(func):
            return func
        return decorator
    
    def time_async_function(*args, **kwargs):
        def decorator(func):
            return func
        return decorator
    
    class MetricsTimer:
        def __init__(self, *args, **kwargs):
            pass
        def __enter__(self):
            return self
        def __exit__(self, *args, **kwargs):
            pass


# Create logger
logger = logging.getLogger("fastapi-keycloak.debug")


class DebugLogLevel(str, Enum):
    """Enumeration of debug log levels with increasing verbosity."""
    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    DEBUG = "debug"
    TRACE = "trace"


class TokenDetails(BaseModel):
    """Pydantic model for token details."""
    header: Dict[str, Any] = Field(default_factory=dict, description="Token header")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Token payload")
    signature: str = Field("", description="Token signature (base64url encoded)")
    is_valid: bool = Field(False, description="Whether the token is valid")
    validation_errors: List[str] = Field(default_factory=list, description="Validation errors if any")
    expiration: Optional[datetime.datetime] = Field(None, description="Token expiration time")
    expiration_seconds: Optional[int] = Field(None, description="Seconds until token expires")
    issuer: Optional[str] = Field(None, description="Token issuer")
    subject: Optional[str] = Field(None, description="Token subject")
    audience: Optional[List[str]] = Field(None, description="Token audience")
    issued_at: Optional[datetime.datetime] = Field(None, description="Token issue time")
    not_before: Optional[datetime.datetime] = Field(None, description="Token not valid before time")
    jwt_id: Optional[str] = Field(None, description="JWT ID")


class JWKSDetails(BaseModel):
    """Pydantic model for JWKS details."""
    keys_count: int = Field(0, description="Number of keys in JWKS")
    key_ids: List[str] = Field(default_factory=list, description="List of key IDs")
    key_types: Dict[str, str] = Field(default_factory=dict, description="Types of keys by key ID")
    key_algorithms: Dict[str, str] = Field(default_factory=dict, description="Algorithms of keys by key ID")
    is_valid: bool = Field(False, description="Whether the JWKS is valid")
    validation_errors: List[str] = Field(default_factory=list, description="Validation errors if any")


class CertificateInfo(BaseModel):
    """Pydantic model for certificate information."""
    subject: str = Field("", description="Certificate subject")
    issuer: str = Field("", description="Certificate issuer")
    not_valid_before: datetime.datetime = Field(..., description="Certificate not valid before time")
    not_valid_after: datetime.datetime = Field(..., description="Certificate not valid after time")
    serial_number: str = Field("", description="Certificate serial number")
    public_key_pem: str = Field("", description="Public key in PEM format")
    cert_pem: str = Field("", description="Certificate in PEM format")


class MockUserModel(BaseModel):
    """Pydantic model for mock users in development."""
    subject: str = Field(..., description="User subject/ID")
    username: str = Field(..., description="Username")
    email: Optional[str] = Field(None, description="Email address")
    given_name: Optional[str] = Field(None, description="First name")
    family_name: Optional[str] = Field(None, description="Last name")
    roles: List[str] = Field(default_factory=list, description="User roles")
    groups: List[str] = Field(default_factory=list, description="User groups")
    scopes: List[str] = Field(default_factory=list, description="User scopes")
    attributes: Dict[str, List[str]] = Field(default_factory=dict, description="User attributes")


class DebugLogger:
    """
    Enhanced logger for debugging with configurable verbosity.
    
    This class provides a wrapper around the standard logger with
    configurable verbosity levels and additional context information.
    """
    
    def __init__(
        self,
        name: str = "fastapi-keycloak.debug",
        level: Union[str, int] = logging.INFO,
        include_timestamp: bool = True,
        include_trace_id: bool = True
    ):
        """
        Initialize the debug logger.
        
        Args:
            name: Logger name
            level: Logging level
            include_timestamp: Whether to include timestamp in log messages
            include_trace_id: Whether to include trace ID in log messages
        """
        # Create or get logger
        self.logger = logging.getLogger(name)
        
        # Set level
        if isinstance(level, str):
            # Convert string level to logging constant
            self.logger.setLevel(getattr(logging, level.upper()))
        else:
            self.logger.setLevel(level)
            
        # Set configuration
        self.include_timestamp = include_timestamp
        self.include_trace_id = include_trace_id
        self.trace_id = str(uuid.uuid4())
        
    def _format_message(self, message: str) -> str:
        """
        Format a log message with additional context.
        
        Args:
            message: Log message
            
        Returns:
            str: Formatted message
        """
        parts = []
        
        # Add timestamp if enabled
        if self.include_timestamp:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            parts.append(f"[{timestamp}]")
            
        # Add trace ID if enabled
        if self.include_trace_id:
            parts.append(f"[trace:{self.trace_id}]")
            
        # Add message
        parts.append(message)
        
        return " ".join(parts)
    
    def set_trace_id(self, trace_id: str) -> None:
        """
        Set the trace ID for the logger.
        
        Args:
            trace_id: Trace ID to use
        """
        self.trace_id = trace_id
    
    def debug(self, message: str, *args, **kwargs) -> None:
        """
        Log a debug message.
        
        Args:
            message: Log message
            *args: Additional arguments
            **kwargs: Additional keyword arguments
        """
        self.logger.debug(self._format_message(message), *args, **kwargs)
    
    def info(self, message: str, *args, **kwargs) -> None:
        """
        Log an info message.
        
        Args:
            message: Log message
            *args: Additional arguments
            **kwargs: Additional keyword arguments
        """
        self.logger.info(self._format_message(message), *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs) -> None:
        """
        Log a warning message.
        
        Args:
            message: Log message
            *args: Additional arguments
            **kwargs: Additional keyword arguments
        """
        self.logger.warning(self._format_message(message), *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs) -> None:
        """
        Log an error message.
        
        Args:
            message: Log message
            *args: Additional arguments
            **kwargs: Additional keyword arguments
        """
        self.logger.error(self._format_message(message), *args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs) -> None:
        """
        Log a critical message.
        
        Args:
            message: Log message
            *args: Additional arguments
            **kwargs: Additional keyword arguments
        """
        self.logger.critical(self._format_message(message), *args, **kwargs)
    
    def trace(self, message: str, *args, **kwargs) -> None:
        """
        Log a trace message (highest verbosity).
        
        Args:
            message: Log message
            *args: Additional arguments
            **kwargs: Additional keyword arguments
        """
        if self.logger.level <= 5:  # Custom level for TRACE
            self.logger.log(5, self._format_message(message), *args, **kwargs)
    
    def log_exception(self, exc: Exception, include_traceback: bool = True) -> None:
        """
        Log an exception with optional traceback.
        
        Args:
            exc: Exception to log
            include_traceback: Whether to include traceback in log message
        """
        message = f"Exception: {exc.__class__.__name__}: {str(exc)}"
        self.error(message)
        
        if include_traceback:
            import traceback
            tb = traceback.format_exc()
            self.error(f"Traceback: {tb}")
    
    def log_request(self, request: Request) -> None:
        """
        Log details of an HTTP request.
        
        Args:
            request: FastAPI Request object
        """
        # Extract request details
        method = request.method
        url = str(request.url)
        headers = dict(request.headers)
        
        # Remove sensitive headers
        if "authorization" in headers:
            headers["authorization"] = "Bearer [REDACTED]"
        if "cookie" in headers:
            headers["cookie"] = "[REDACTED]"
            
        # Log request details
        self.debug(f"Request: {method} {url}")
        self.trace(f"Request headers: {json.dumps(headers, indent=2)}")


# Token inspection functions

def decode_token_parts(token: str) -> Tuple[Dict[str, Any], Dict[str, Any], str]:
    """
    Decode JWT token parts without validation.
    
    Args:
        token: JWT token to decode
        
    Returns:
        Tuple[Dict[str, Any], Dict[str, Any], str]: Header, payload, and signature
        
    Raises:
        ValueError: If token is invalid
    """
    # Remove Bearer prefix if present
    if token.startswith("Bearer "):
        token = token[7:]
    
    # Split token
    try:
        parts = token.split(".")
        if len(parts) != 3:
            raise ValueError("Invalid token format: expected 3 parts")
        
        header_b64, payload_b64, signature_b64 = parts
        
        # Decode header
        header_bytes = base64.urlsafe_b64decode(header_b64 + "=" * (4 - len(header_b64) % 4))
        header = json.loads(header_bytes.decode("utf-8"))
        
        # Decode payload
        payload_bytes = base64.urlsafe_b64decode(payload_b64 + "=" * (4 - len(payload_b64) % 4))
        payload = json.loads(payload_bytes.decode("utf-8"))
        
        return header, payload, signature_b64
    except (ValueError, json.JSONDecodeError, binascii.Error) as e:
        raise ValueError(f"Failed to decode token: {str(e)}")


@time_function("token_inspect_duration_seconds", labels={"function": "decode_token"})
def decode_token(token: str) -> TokenDetails:
    """
    Decode a JWT token without validation and return detailed information.
    
    Args:
        token: JWT token to decode
        
    Returns:
        TokenDetails: Token details
        
    Raises:
        ValueError: If token is invalid
    """
    try:
        # Decode token parts
        header, payload, signature = decode_token_parts(token)
        
        # Create response
        result = TokenDetails(
            header=header,
            payload=payload,
            signature=signature,
            is_valid=False,  # Not validated
            validation_errors=[]
        )
        
        # Extract standard claims
        if "exp" in payload:
            result.expiration = datetime.datetime.fromtimestamp(payload["exp"])
            result.expiration_seconds = max(0, int(payload["exp"] - time.time()))
            
        if "iss" in payload:
            result.issuer = payload["iss"]
            
        if "sub" in payload:
            result.subject = payload["sub"]
            
        if "aud" in payload:
            if isinstance(payload["aud"], list):
                result.audience = payload["aud"]
            else:
                result.audience = [payload["aud"]]
                
        if "iat" in payload:
            result.issued_at = datetime.datetime.fromtimestamp(payload["iat"])
            
        if "nbf" in payload:
            result.not_before = datetime.datetime.fromtimestamp(payload["nbf"])
            
        if "jti" in payload:
            result.jwt_id = payload["jti"]
            
        return result
    except Exception as e:
        # Create error response
        return TokenDetails(
            is_valid=False,
            validation_errors=[f"Failed to decode token: {str(e)}"]
        )


@time_async_function("token_validation_debug_duration_seconds", labels={"function": "validate_token_debug"})
async def validate_token_debug(
    token: str,
    jwks: Optional[Dict[str, Any]] = None,
    issuer: Optional[str] = None,
    audience: Optional[Union[str, List[str]]] = None,
    algorithms: List[str] = None
) -> TokenDetails:
    """
    Validate a JWT token and return detailed diagnostic information.
    
    Args:
        token: JWT token to validate
        jwks: JWKS to use for validation
        issuer: Expected issuer
        audience: Expected audience
        algorithms: Allowed algorithms
        
    Returns:
        TokenDetails: Token details with validation information
    """
    if not AUTHLIB_AVAILABLE:
        return TokenDetails(
            is_valid=False,
            validation_errors=["Authlib not available"]
        )
    
    # Default algorithms
    algorithms = algorithms or ["RS256"]
    
    try:
        # First decode without validation
        result = decode_token(token)
        
        # Skip validation if jwks is not provided
        if not jwks:
            result.validation_errors.append("JWKS not provided, skipping validation")
            return result
        
        # Prepare validation options
        validate_claims = {}
        if issuer:
            validate_claims["iss"] = {"essential": True, "value": issuer}
        if audience:
            validate_claims["aud"] = {"essential": True, "value": audience}
        
        # Create JWT validator
        jwt = JsonWebToken(algorithms)
        
        # Parse JWKS
        jwks_obj = JsonWebKey.import_key_set(jwks)
        
        # Validate token
        try:
            claims = jwt.decode(
                token,
                jwks_obj,
                claims_options=validate_claims
            )
            claims.validate()
            
            # Update result with validation success
            result.is_valid = True
        except ExpiredTokenError:
            result.is_valid = False
            result.validation_errors.append("Token has expired")
        except JoseError as e:
            result.is_valid = False
            result.validation_errors.append(f"Token validation failed: {str(e)}")
            
        return result
    except Exception as e:
        # Handle any other exceptions
        return TokenDetails(
            is_valid=False,
            validation_errors=[f"Validation error: {str(e)}"]
        )


@time_function("jwks_inspect_duration_seconds", labels={"function": "inspect_jwks"})
def inspect_jwks(jwks: Dict[str, Any]) -> JWKSDetails:
    """
    Inspect a JWKS and return detailed information.
    
    Args:
        jwks: JWKS to inspect
        
    Returns:
        JWKSDetails: JWKS details
    """
    result = JWKSDetails()
    validation_errors = []
    
    try:
        # Check JWKS format
        if not isinstance(jwks, dict):
            validation_errors.append("JWKS must be a JSON object")
            return JWKSDetails(
                is_valid=False,
                validation_errors=validation_errors
            )
            
        # Check keys property
        if "keys" not in jwks:
            validation_errors.append("JWKS must have a 'keys' property")
            return JWKSDetails(
                is_valid=False,
                validation_errors=validation_errors
            )
            
        keys = jwks["keys"]
        if not isinstance(keys, list):
            validation_errors.append("JWKS 'keys' property must be an array")
            return JWKSDetails(
                is_valid=False,
                validation_errors=validation_errors
            )
            
        # Process keys
        result.keys_count = len(keys)
        
        for key in keys:
            # Check required properties
            if "kid" not in key:
                validation_errors.append("Key is missing 'kid' property")
                continue
                
            if "kty" not in key:
                validation_errors.append(f"Key {key.get('kid')} is missing 'kty' property")
                continue
                
            # Add key information
            kid = key["kid"]
            result.key_ids.append(kid)
            result.key_types[kid] = key["kty"]
            
            # Add algorithm if available
            if "alg" in key:
                result.key_algorithms[kid] = key["alg"]
                
        # Set validation result
        result.is_valid = len(validation_errors) == 0
        result.validation_errors = validation_errors
        
        return result
    except Exception as e:
        validation_errors.append(f"Error inspecting JWKS: {str(e)}")
        return JWKSDetails(
            is_valid=False,
            validation_errors=validation_errors
        )


def find_key_by_id(jwks: Dict[str, Any], kid: str) -> Optional[Dict[str, Any]]:
    """
    Find a key in a JWKS by key ID.
    
    Args:
        jwks: JWKS to search
        kid: Key ID to find
        
    Returns:
        Optional[Dict[str, Any]]: The key if found, None otherwise
    """
    if not isinstance(jwks, dict) or "keys" not in jwks:
        return None
        
    for key in jwks["keys"]:
        if key.get("kid") == kid:
            return key
            
    return None


# Certificate generation functions

def generate_rsa_key_pair(key_size: int = 2048) -> Tuple[Any, Any]:
    """
    Generate an RSA key pair.
    
    Args:
        key_size: Key size in bits
        
    Returns:
        Tuple[Any, Any]: Private key and public key
        
    Raises:
        RuntimeError: If cryptography library is not available
    """
    if not CRYPTOGRAPHY_AVAILABLE:
        raise RuntimeError("Cryptography library not available")
        
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend()
    )
    
    # Extract public key
    public_key = private_key.public_key()
    
    return private_key, public_key


def generate_self_signed_cert(
    common_name: str,
    organization: str = "Development",
    country: str = "US",
    validity_days: int = 365,
    key_size: int = 2048
) -> CertificateInfo:
    """
    Generate a self-signed certificate for development purposes.
    
    Args:
        common_name: Certificate common name
        organization: Organization name
        country: Country code
        validity_days: Validity period in days
        key_size: Key size in bits
        
    Returns:
        CertificateInfo: Certificate information
        
    Raises:
        RuntimeError: If cryptography library is not available
    """
    if not CRYPTOGRAPHY_AVAILABLE:
        raise RuntimeError("Cryptography library not available")
        
    # Generate key pair
    private_key, public_key = generate_rsa_key_pair(key_size)
    
    # Create certificate subject
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization),
        x509.NameAttribute(NameOID.COUNTRY_NAME, country),
    ])
    
    # Create certificate
    now = datetime.datetime.utcnow()
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        public_key
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        now
    ).not_valid_after(
        now + datetime.timedelta(days=validity_days)
    ).add_extension(
        x509.BasicConstraints(ca=True, path_length=None), critical=True
    ).sign(private_key, hashes.SHA256())
    
    # Serialize keys and certificate
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')
    
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')
    
    cert_pem = cert.public_bytes(serialization.Encoding.PEM).decode('utf-8')
    
    # Create result
    return CertificateInfo(
        subject=f"CN={common_name}, O={organization}, C={country}",
        issuer=f"CN={common_name}, O={organization}, C={country}",
        not_valid_before=now,
        not_valid_after=now + datetime.timedelta(days=validity_days),
        serial_number=str(cert.serial_number),
        public_key_pem=public_key_pem,
        cert_pem=cert_pem
    )


def generate_jwks_from_rsa_key(
    private_key: Any,
    kid: str = None,
    alg: str = "RS256"
) -> Dict[str, Any]:
    """
    Generate a JWKS from an RSA private key.
    
    Args:
        private_key: RSA private key
        kid: Key ID (randomly generated if not provided)
        alg: Algorithm
        
    Returns:
        Dict[str, Any]: JWKS
        
    Raises:
        RuntimeError: If cryptography library is not available
    """
    if not CRYPTOGRAPHY_AVAILABLE:
        raise RuntimeError("Cryptography library not available")
        
    # Generate key ID if not provided
    if kid is None:
        kid = str(uuid.uuid4())
        
    # Extract public key components
    public_key = private_key.public_key()
    public_numbers = public_key.public_numbers()
    
    # Create JWKS
    jwks = {
        "keys": [
            {
                "kid": kid,
                "kty": "RSA",
                "alg": alg,
                "use": "sig",
                "n": base64.urlsafe_b64encode(
                    public_numbers.n.to_bytes(
                        (public_numbers.n.bit_length() + 7) // 8, byteorder="big"
                    )
                ).decode('utf-8').rstrip("="),
                "e": base64.urlsafe_b64encode(
                    public_numbers.e.to_bytes(
                        (public_numbers.e.bit_length() + 7) // 8, byteorder="big"
                    )
                ).decode('utf-8').rstrip("=")
            }
        ]
    }
    
    return jwks


def save_cert_files(
    cert_info: CertificateInfo,
    cert_path: str,
    private_key_path: str,
    public_key_path: str
) -> None:
    """
    Save certificate and key files.
    
    Args:
        cert_info: Certificate information
        cert_path: Path to save certificate
        private_key_path: Path to save private key
        public_key_path: Path to save public key
        
    Raises:
        IOError: If files cannot be written
    """
    try:
        # Save certificate
        with open(cert_path, "w") as f:
            f.write(cert_info.cert_pem)
            
        # Save private key
        with open(private_key_path, "w") as f:
            f.write(private_key_path)
            
        # Save public key
        with open(public_key_path, "w") as f:
            f.write(cert_info.public_key_pem)
    except IOError as e:
        raise IOError(f"Failed to save certificate files: {str(e)}")


# Mock authentication for development
class MockAuthProvider:
    """
    Mock authentication provider for development purposes.
    
    This class provides mock authentication for development environments
    without requiring a real Keycloak server.
    """
    
    def __init__(
        self,
        issuer: str = "http://localhost:8080/auth/realms/development",
        token_expiration: int = 3600,
        private_key: Any = None,
        kid: str = None
    ):
        """
        Initialize the mock authentication provider.
        
        Args:
            issuer: Issuer URI
            token_expiration: Token expiration in seconds
            private_key: RSA private key (generated if not provided)
            kid: Key ID (randomly generated if not provided)
        """
        self.issuer = issuer
        self.token_expiration = token_expiration
        self.logger = DebugLogger(name="fastapi-keycloak.mock-auth")
        
        # Generate key pair if not provided
        if private_key is None:
            if not CRYPTOGRAPHY_AVAILABLE:
                self.logger.warning("Cryptography library not available, mock auth will not work")
                self.private_key = None
                self.jwks = None
                return
                
            self.private_key, _ = generate_rsa_key_pair()
        else:
            self.private_key = private_key
            
        # Generate JWKS
        self.kid = kid or str(uuid.uuid4())
        self.jwks = generate_jwks_from_rsa_key(self.private_key, self.kid)
        
        # Mock users database
        self.users = {}
        
        # Add default admin user
        self.add_user(
            MockUserModel(
                subject="admin",
                username="admin",
                email="admin@example.com",
                given_name="Admin",
                family_name="User",
                roles=["admin"],
                groups=["Administrators"],
                scopes=["openid", "profile", "email"]
            )
        )
        
        self.logger.info(f"Mock auth provider initialized with issuer: {issuer}")
    
    def add_user(self, user: MockUserModel) -> None:
        """
        Add a mock user.
        
        Args:
            user: User model
        """
        self.users[user.subject] = user
        self.logger.debug(f"Added mock user: {user.username}")
    
    def get_user(self, subject: str) -> Optional[MockUserModel]:
        """
        Get a mock user by subject.
        
        Args:
            subject: User subject
            
        Returns:
            Optional[MockUserModel]: User if found, None otherwise
        """
        return self.users.get(subject)
    
    def generate_token(
        self,
        subject: str,
        client_id: str = "mock-client",
        audience: str = "mock-audience",
        additional_claims: Dict[str, Any] = None
    ) -> str:
        """
        Generate a mock JWT token.
        
        Args:
            subject: User subject
            client_id: Client ID
            audience: Audience
            additional_claims: Additional claims to include
            
        Returns:
            str: JWT token
            
        Raises:
            ValueError: If subject is not found
            RuntimeError: If cryptography library is not available
        """
        if not CRYPTOGRAPHY_AVAILABLE:
            raise RuntimeError("Cryptography library not available")
            
        # Check if user exists
        user = self.get_user(subject)
        if not user:
            raise ValueError(f"Mock user with subject {subject} not found")
            
        # Create token payload
        now = int(time.time())
        expires = now + self.token_expiration
        
        payload = {
            "iss": self.issuer,
            "sub": user.subject,
            "aud": audience,
            "exp": expires,
            "iat": now,
            "auth_time": now,
            "azp": client_id,
            "preferred_username": user.username,
            "email": user.email,
            "email_verified": True,
            "given_name": user.given_name,
            "family_name": user.family_name,
            "name": f"{user.given_name} {user.family_name}".strip(),
            "roles": user.roles,
            "groups": user.groups,
            "scope": " ".join(user.scopes),
            "client_id": client_id,
        }
        
        # Add user attributes if available
        if user.attributes:
            for key, value in user.attributes.items():
                payload[key] = value
                
        # Add additional claims if provided
        if additional_claims:
            payload.update(additional_claims)
            
        # Create token header
        header = {
            "alg": "RS256",
            "typ": "JWT",
            "kid": self.kid
        }
        
        # Encode header and payload
        header_bytes = json.dumps(header, separators=(",", ":")).encode("utf-8")
        header_b64 = base64.urlsafe_b64encode(header_bytes).decode("utf-8").rstrip("=")
        
        payload_bytes = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        payload_b64 = base64.urlsafe_b64encode(payload_bytes).decode("utf-8").rstrip("=")
        
        # Create signature
        data_to_sign = f"{header_b64}.{payload_b64}".encode("utf-8")
        signature = self.private_key.sign(
            data_to_sign,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        signature_b64 = base64.urlsafe_b64encode(signature).decode("utf-8").rstrip("=")
        
        # Create token
        token = f"{header_b64}.{payload_b64}.{signature_b64}"
        
        self.logger.debug(f"Generated mock token for user: {user.username}")
        return token


def validate_mock_token(token: str, mock_auth: MockAuthProvider) -> TokenDetails:
    """
    Validate a mock token.
    
    Args:
        token: JWT token to validate
        mock_auth: Mock authentication provider
        
    Returns:
        TokenDetails: Token details with validation information
    """
    result = decode_token(token)
    
    try:
        # Perform basic validation
        header, payload, _ = decode_token_parts(token)
        
        # Check issuer
        if payload.get("iss") != mock_auth.issuer:
            result.validation_errors.append(f"Invalid issuer: {payload.get('iss')}")
            result.is_valid = False
            return result
            
        # Check expiration
        if "exp" in payload:
            if payload["exp"] < time.time():
                result.validation_errors.append("Token has expired")
                result.is_valid = False
                return result
                
        # Validate signature if possible
        if AUTHLIB_AVAILABLE:
            jwt = JsonWebToken(["RS256"])
            jwks = JsonWebKey.import_key_set(mock_auth.jwks)
            
            try:
                claims = jwt.decode(token, jwks)
                claims.validate()
                result.is_valid = True
            except Exception as e:
                result.validation_errors.append(f"Signature validation failed: {str(e)}")
                result.is_valid = False
        else:
            # Skip signature validation if Authlib is not available
            result.validation_errors.append("Signature validation skipped (Authlib not available)")
            result.is_valid = True
            
        return result
    except Exception as e:
        result.validation_errors.append(f"Validation error: {str(e)}")
        result.is_valid = False
        return result


# Debug router for development endpoints
def create_debug_router(
    development_mode: bool = False,
    mock_auth: Optional[MockAuthProvider] = None
) -> APIRouter:
    """
    Create a FastAPI router with debug endpoints.
    
    Args:
        development_mode: Whether development mode is enabled
        mock_auth: Mock authentication provider
        
    Returns:
        APIRouter: FastAPI router
    """
    if not development_mode:
        # Create a disabled router in production
        router = APIRouter()
        
        @router.get("/debug/disabled")
        def debug_disabled():
            """Show that debug endpoints are disabled in production."""
            return {"message": "Debug endpoints are disabled in production"}
            
        return router
    
    # Create a debug router for development
    router = APIRouter(prefix="/debug", tags=["debug"])
    
    @router.post("/token/decode", response_model=TokenDetails)
    def decode_token_endpoint(token: str = Body(..., embed=True)):
        """
        Decode a JWT token without validation.
        
        Args:
            token: JWT token to decode
            
        Returns:
            TokenDetails: Token details
        """
        try:
            result = decode_token(token)
            return result
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to decode token: {str(e)}"
            )
    
    @router.post("/token/validate", response_model=TokenDetails)
    async def validate_token_endpoint(
        token: str = Body(..., embed=True),
        issuer: Optional[str] = Body(None, embed=True),
        audience: Optional[Union[str, List[str]]] = Body(None, embed=True)
    ):
        """
        Validate a JWT token and return detailed information.
        
        Args:
            token: JWT token to validate
            issuer: Expected issuer
            audience: Expected audience
            
        Returns:
            TokenDetails: Token details with validation information
        """
        try:
            # Use mock auth if available, otherwise fetch JWKS from issuer
            if mock_auth:
                result = validate_mock_token(token, mock_auth)
            else:
                # TODO: Implement fetching JWKS from issuer
                result = await validate_token_debug(
                    token=token,
                    jwks=mock_auth.jwks if mock_auth else None,
                    issuer=issuer,
                    audience=audience
                )
                
            return result
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to validate token: {str(e)}"
            )
    
    @router.post("/jwks/inspect", response_model=JWKSDetails)
    def inspect_jwks_endpoint(jwks: Dict[str, Any] = Body(...)):
        """
        Inspect a JWKS and return detailed information.
        
        Args:
            jwks: JWKS to inspect
            
        Returns:
            JWKSDetails: JWKS details
        """
        try:
            result = inspect_jwks(jwks)
            return result
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to inspect JWKS: {str(e)}"
            )
    
    @router.post("/cert/generate", response_model=CertificateInfo)
    def generate_cert_endpoint(
        common_name: str = Body(...),
        organization: str = Body("Development"),
        country: str = Body("US"),
        validity_days: int = Body(365)
    ):
        """
        Generate a self-signed certificate for development purposes.
        
        Args:
            common_name: Certificate common name
            organization: Organization name
            country: Country code
            validity_days: Validity period in days
            
        Returns:
            CertificateInfo: Certificate information
        """
        if not CRYPTOGRAPHY_AVAILABLE:
            raise HTTPException(
                status_code=400,
                detail="Cryptography library not available"
            )
            
        try:
            result = generate_self_signed_cert(
                common_name=common_name,
                organization=organization,
                country=country,
                validity_days=validity_days
            )
            return result
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to generate certificate: {str(e)}"
            )
    
    @router.post("/mock/user/add", response_model=MockUserModel)
    def add_mock_user_endpoint(user: MockUserModel):
        """
        Add a mock user for development.
        
        Args:
            user: User model
            
        Returns:
            MockUserModel: Added user
        """
        if not mock_auth:
            raise HTTPException(
                status_code=400,
                detail="Mock authentication provider not available"
            )
            
        try:
            mock_auth.add_user(user)
            return user
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to add mock user: {str(e)}"
            )
    
    @router.post("/mock/token/generate", response_model=Dict[str, Any])
    def generate_mock_token_endpoint(
        subject: str = Body(...),
        client_id: str = Body("mock-client"),
        audience: str = Body("mock-audience"),
        additional_claims: Optional[Dict[str, Any]] = Body(None)
    ):
        """
        Generate a mock JWT token for development.
        
        Args:
            subject: User subject
            client_id: Client ID
            audience: Audience
            additional_claims: Additional claims to include
            
        Returns:
            Dict[str, Any]: Generated token and details
        """
        if not mock_auth:
            raise HTTPException(
                status_code=400,
                detail="Mock authentication provider not available"
            )
            
        try:
            token = mock_auth.generate_token(
                subject=subject,
                client_id=client_id,
                audience=audience,
                additional_claims=additional_claims
            )
            
            details = decode_token(token)
            
            return {
                "token": token,
                "details": details
            }
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to generate mock token: {str(e)}"
            )
    
    @router.get("/jwks")
    def get_mock_jwks():
        """
        Get the mock JWKS for development.
        
        Returns:
            Dict[str, Any]: JWKS
        """
        if not mock_auth or not mock_auth.jwks:
            raise HTTPException(
                status_code=400,
                detail="Mock authentication provider not available"
            )
            
        return mock_auth.jwks
    
    @router.get("/status")
    def get_debug_status():
        """
        Get debug status information.
        
        Returns:
            Dict[str, Any]: Status information
        """
        return {
            "development_mode": development_mode,
            "mock_auth_available": mock_auth is not None,
            "authlib_available": AUTHLIB_AVAILABLE,
            "cryptography_available": CRYPTOGRAPHY_AVAILABLE,
            "metrics_available": METRICS_AVAILABLE,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
        
    return router


# HTTP client debugging
def log_http_request(
    logger: Union[logging.Logger, DebugLogger],
    method: str,
    url: str,
    headers: Dict[str, str] = None,
    body: Any = None,
    redact_headers: List[str] = None,
    redact_body_fields: List[str] = None
):
    """
    Log an HTTP request with sensitive information redacted.
    
    Args:
        logger: Logger to use
        method: HTTP method
        url: URL
        headers: Request headers
        body: Request body
        redact_headers: Headers to redact
        redact_body_fields: Body fields to redact
    """
    # Default headers to redact
    redact_headers = redact_headers or ["authorization", "cookie", "x-api-key"]
    redact_body_fields = redact_body_fields or ["password", "token", "secret", "key"]
    
    # Create log message
    log_message = f"HTTP Request: {method} {url}"
    
    # Add headers with redaction
    if headers:
        redacted_headers = headers.copy()
        for header in redact_headers:
            if header.lower() in [h.lower() for h in redacted_headers.keys()]:
                redacted_headers[header] = "[REDACTED]"
                
        log_message += f"\nHeaders: {json.dumps(redacted_headers, indent=2)}"
        
    # Add body with redaction
    if body:
        if isinstance(body, dict):
            redacted_body = body.copy()
            for field in redact_body_fields:
                if field in redacted_body:
                    redacted_body[field] = "[REDACTED]"
                    
            log_message += f"\nBody: {json.dumps(redacted_body, indent=2)}"
        else:
            log_message += f"\nBody: (non-JSON body, not logged)"
            
    # Log the message
    if isinstance(logger, DebugLogger):
        logger.debug(log_message)
    else:
        logger.debug(log_message)


def log_http_response(
    logger: Union[logging.Logger, DebugLogger],
    status_code: int,
    url: str,
    headers: Dict[str, str] = None,
    body: Any = None,
    duration: float = None,
    redact_headers: List[str] = None,
    redact_body_fields: List[str] = None
):
    """
    Log an HTTP response with sensitive information redacted.
    
    Args:
        logger: Logger to use
        status_code: HTTP status code
        url: URL
        headers: Response headers
        body: Response body
        duration: Request duration in seconds
        redact_headers: Headers to redact
        redact_body_fields: Body fields to redact
    """
    # Default headers to redact
    redact_headers = redact_headers or ["set-cookie", "x-api-key"]
    redact_body_fields = redact_body_fields or ["password", "token", "secret", "key"]
    
    # Create log message
    log_message = f"HTTP Response: {status_code} {url}"
    
    # Add duration if available
    if duration is not None:
        log_message += f" ({duration:.3f}s)"
        
    # Add headers with redaction
    if headers:
        redacted_headers = headers.copy()
        for header in redact_headers:
            if header.lower() in [h.lower() for h in redacted_headers.keys()]:
                redacted_headers[header] = "[REDACTED]"
                
        log_message += f"\nHeaders: {json.dumps(redacted_headers, indent=2)}"
        
    # Add body with redaction
    if body:
        if isinstance(body, dict):
            redacted_body = body.copy()
            for field in redact_body_fields:
                if field in redacted_body:
                    redacted_body[field] = "[REDACTED]"
                    
            log_message += f"\nBody: {json.dumps(redacted_body, indent=2)}"
        elif isinstance(body, str):
            try:
                # Try to parse as JSON
                body_dict = json.loads(body)
                redacted_body = body_dict.copy()
                for field in redact_body_fields:
                    if field in redacted_body:
                        redacted_body[field] = "[REDACTED]"
                        
                log_message += f"\nBody: {json.dumps(redacted_body, indent=2)}"
            except json.JSONDecodeError:
                # Not JSON, log length only
                log_message += f"\nBody: (non-JSON body, length: {len(body)})"
        else:
            log_message += f"\nBody: (non-string body, not logged)"
            
    # Log the message
    if isinstance(logger, DebugLogger):
        logger.debug(log_message)
    else:
        logger.debug(log_message)


# Initialize a MockAuthProvider if in development mode
mock_auth_provider = None

def init_debug_environment(
    development_mode: bool = False,
    mock_issuer: str = "http://localhost:8080/auth/realms/development"
) -> Optional[MockAuthProvider]:
    """
    Initialize the debug environment.
    
    Args:
        development_mode: Whether development mode is enabled
        mock_issuer: Issuer URI for mock tokens
        
    Returns:
        Optional[MockAuthProvider]: Mock authentication provider if created
    """
    global mock_auth_provider
    
    if not development_mode:
        return None
        
    try:
        if CRYPTOGRAPHY_AVAILABLE:
            mock_auth_provider = MockAuthProvider(issuer=mock_issuer)
            return mock_auth_provider
        else:
            logger.warning("Cryptography library not available, mock authentication disabled")
            return None
    except Exception as e:
        logger.error(f"Failed to initialize debug environment: {str(e)}")
        return None
