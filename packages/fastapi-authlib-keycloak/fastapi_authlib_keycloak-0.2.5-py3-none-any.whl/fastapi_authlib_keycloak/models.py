#!/usr/bin/env python3
"""
Data models for FastAPI-Authlib-Keycloak.

This module defines the data models used throughout the package.
"""

from typing import List, Dict, Optional
from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    """
    User model representing an authenticated user.
    
    This model contains the user information extracted from the JWT token.
    """
    
    username: str = Field(..., description="Username of the authenticated user")
    email: Optional[EmailStr] = Field(None, description="Email address of the user")
    first_name: Optional[str] = Field(None, description="First name of the user")
    last_name: Optional[str] = Field(None, description="Last name of the user")
    roles: List[str] = Field(default_factory=list, description="Roles assigned to the user")
    
    @property
    def full_name(self) -> str:
        """
        Get the full name of the user.
        
        Returns:
            str: Full name of the user, or username if no names are available
        """
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        else:
            return self.username
    
    def has_role(self, role: str) -> bool:
        """
        Check if the user has a specific role.
        
        Args:
            role: Role to check
            
        Returns:
            bool: True if the user has the role, False otherwise
        """
        return role in self.roles
    
    def has_any_role(self, roles: List[str]) -> bool:
        """
        Check if the user has any of the specified roles.
        
        Args:
            roles: List of roles to check
            
        Returns:
            bool: True if the user has any of the roles, False otherwise
        """
        return any(role in self.roles for role in roles)
    
    def has_all_roles(self, roles: List[str]) -> bool:
        """
        Check if the user has all of the specified roles.
        
        Args:
            roles: List of roles to check
            
        Returns:
            bool: True if the user has all of the roles, False otherwise
        """
        return all(role in self.roles for role in roles)


class TokenResponse(BaseModel):
    """Token response model for OAuth2 token endpoints."""
    
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(..., description="Token type, usually 'Bearer'")
    expires_in: int = Field(..., description="Token expiration time in seconds")
    refresh_token: Optional[str] = Field(None, description="Refresh token for obtaining new access tokens")
    refresh_expires_in: Optional[int] = Field(None, description="Refresh token expiration time in seconds")
    scope: Optional[str] = Field(None, description="Token scope")
