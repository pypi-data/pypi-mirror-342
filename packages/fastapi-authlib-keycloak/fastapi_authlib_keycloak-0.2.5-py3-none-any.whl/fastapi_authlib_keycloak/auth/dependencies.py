#!/usr/bin/env python3
"""
Authentication dependencies for FastAPI routes.

This module provides dependency functions that can be used with FastAPI
to implement authentication and authorization.
"""

import logging
from typing import Dict, List, Optional, Callable, Any

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from fastapi_authlib_keycloak.models import User
from fastapi_authlib_keycloak.auth.validator import KeycloakJWTValidator


def create_get_token_header(
    security: HTTPBearer, 
    validator: KeycloakJWTValidator
) -> Callable:
    """
    Create a dependency function to validate and decode JWT token from Authorization header.
    
    Args:
        security: HTTP Bearer security scheme
        validator: Keycloak JWT validator
        
    Returns:
        Callable: Dependency function for FastAPI
    """
    async def get_token_header(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict:
        """
        Validate and decode JWT token from Authorization header.

        Args:
            credentials: HTTP Authorization credentials

        Returns:
            Dict: Decoded JWT token payload

        Raises:
            HTTPException: If token is invalid or expired
        """
        token = credentials.credentials
        return await validator.validate_token(token)
    
    return get_token_header


def create_get_current_user(
    get_token_header: Callable,
    logger: Optional[logging.Logger] = None
) -> Callable:
    """
    Create a dependency function to get the current user from the token.
    
    Args:
        get_token_header: Dependency function for getting the token
        logger: Logger instance
        
    Returns:
        Callable: Dependency function for FastAPI
    """
    # Initialize logger if not provided
    logger = logger or logging.getLogger("fastapi-keycloak.dependencies")
    
    async def get_current_user(token: Dict = Depends(get_token_header)) -> User:
        """
        Get the current user from the token.

        Args:
            token: Decoded JWT token

        Returns:
            User: Current user object
            
        Raises:
            HTTPException: If user information cannot be extracted from token
        """
        try:
            # Extract user info from token
            username = token.get("preferred_username")
            email = token.get("email")
            first_name = token.get("given_name")
            last_name = token.get("family_name")

            # Extract roles from token
            realm_access = token.get("realm_access", {})
            roles = realm_access.get("roles", [])

            return User(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                roles=roles
            )
        except Exception as e:
            logger.error(f"Error extracting user info: {str(e)}")
            raise HTTPException(status_code=401, detail="Invalid user info in token")
    
    return get_current_user


def create_require_roles(
    get_current_user: Callable,
    logger: Optional[logging.Logger] = None
) -> Callable:
    """
    Create a dependency function factory to require specific roles.
    
    Args:
        get_current_user: Dependency function for getting the current user
        logger: Logger instance
        
    Returns:
        Callable: Function that creates role-based dependencies
    """
    # Initialize logger if not provided
    logger = logger or logging.getLogger("fastapi-keycloak.dependencies")
    
    def require_roles(required_roles: List[str]) -> Callable:
        """
        Dependency function to require specific roles.

        Args:
            required_roles: List of roles required to access the endpoint

        Returns:
            Callable: Dependency function for FastAPI
        """
        async def role_checker(user: User = Depends(get_current_user)) -> User:
            for role in required_roles:
                if role in user.roles:
                    return user

            # If we get here, user doesn't have any of the required roles
            logger.warning(f"User {user.username} does not have required roles: {required_roles}")
            raise HTTPException(
                status_code=403,
                detail=f"Insufficient permissions. Required roles: {required_roles}"
            )

        return role_checker
    
    return require_roles
