#!/usr/bin/env python3
"""
Authentication routes for FastAPI + Keycloak integration.

This module implements the OAuth2/OpenID Connect authentication
flow with Keycloak, including login, callback, refresh, and logout.
"""

import logging
import os
import httpx
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from pydantic import BaseModel

from authlib.integrations.starlette_client import OAuth
from fastapi_authlib_keycloak.auth.validator import KeycloakJWTValidator
from fastapi_authlib_keycloak.models import TokenResponse


def create_auth_router(
    oauth: OAuth,
    validator: KeycloakJWTValidator,
    keycloak_url: str,
    keycloak_realm: str,
    client_id: str,
    client_secret: str,
    api_client_id: str,
    api_client_secret: str,
    api_base_url: Optional[str] = None,
    logger: Optional[logging.Logger] = None,
) -> APIRouter:
    """
    Create an API router with authentication routes.
    
    Args:
        oauth: OAuth client
        validator: Keycloak JWT validator
        keycloak_url: URL of the Keycloak server
        keycloak_realm: Keycloak realm name
        client_id: Client ID
        client_secret: Client secret
        api_client_id: API client ID
        api_client_secret: API client secret
        api_base_url: Base URL for the API
        logger: Logger instance
        
    Returns:
        APIRouter: Router with auth routes
    """
    # Initialize logger if not provided
    logger = logger or logging.getLogger("fastapi-keycloak.routes")
    
    # Create router
    router = APIRouter(tags=["auth"])

    @router.get("/login")
    async def login(request: Request):
        """Initiate Keycloak login flow."""
        # Clear any existing session data before starting new auth flow
        request.session.clear()
        
        # Determine base URL if not provided
        base_url = api_base_url
        if not base_url:
            # Try to determine from request
            base_url = str(request.base_url).rstrip('/')
        
        # Get the redirect URI for the callback
        redirect_uri = f"{base_url}/callback"
        
        # Generate a state parameter and store in session
        state = os.urandom(16).hex()
        request.session["oauth_state"] = state
        
        logger.info(f"Starting login flow with redirect to {redirect_uri}")
        
        # Start authorization flow with explicit state parameter
        return await oauth.keycloak.authorize_redirect(
            request, 
            redirect_uri,
            state=state
        )


    @router.get("/callback")
    async def callback(request: Request):
        """Handle OAuth callback after Keycloak login."""
        try:
            # Get the state from the request
            request_state = request.query_params.get("state")
            session_state = request.session.get("oauth_state")
            
            logger.info(f"Callback received. Session state: {session_state}, Request state: {request_state}")
            
            # If session state is missing but request state exists,
            # restore it from the request (workaround for state validation)
            if (not session_state or session_state != request_state) and request_state:
                logger.warning(f"State mismatch: Session={session_state}, Request={request_state}. Fixing...")
                request.session["oauth_state"] = request_state
            
            # Complete OAuth flow and get tokens
            token = await oauth.keycloak.authorize_access_token(request)
            
            logger.info("Received token from Keycloak")
            
            # Store tokens in session
            request.session["access_token"] = token["access_token"]
            request.session["refresh_token"] = token["refresh_token"]
            
            # Add debugging
            logger.info(f"Token stored in session: {token['access_token'][:20]}...")
            
            # Redirect to docs with token
            response = RedirectResponse(url="/docs")
            return response
        except Exception as e:
            logger.error(f"Error in callback: {str(e)}")
            
            # If it's a state mismatch error, provide a more helpful error message and action
            if "mismatching_state" in str(e):
                # Create a recovery URL that will try to fix the state issue
                recovery_url = f"/auth-recovery?state={request.query_params.get('state', '')}&code={request.query_params.get('code', '')}"
                
                return HTMLResponse(f"""
                <html>
                    <head>
                        <title>Authentication Error</title>
                        <style>
                            body {{ font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; max-width: 800px; margin: 0 auto; }}
                            h1 {{ color: #d9534f; }}
                            .error {{ background-color: #f2dede; border: 1px solid #ebccd1; color: #a94442; padding: 15px; border-radius: 4px; margin-bottom: 20px; }}
                            .btn {{ display: inline-block; font-weight: 400; text-align: center; white-space: nowrap; vertical-align: middle; user-select: none; border: 1px solid transparent; padding: .375rem .75rem; font-size: 1rem; line-height: 1.5; border-radius: .25rem; transition: color .15s ease-in-out,background-color .15s ease-in-out,border-color .15s ease-in-out,box-shadow .15s ease-in-out; }}
                            .btn-primary {{ color: #fff; background-color: #007bff; border-color: #007bff; }}
                            .btn-primary:hover {{ color: #fff; background-color: #0069d9; border-color: #0062cc; }}
                        </style>
                    </head>
                    <body>
                        <h1>Authentication Error</h1>
                        <div class="error">
                            <p><strong>Error:</strong> {str(e)}</p>
                            <p>Your browser session may have expired or cookies are blocked.</p>
                        </div>
                        <p>Click the button below to recover your authentication session:</p>
                        <a href="{recovery_url}" class="btn btn-primary">Recover Session</a>
                        <p>Or try again in a private/incognito window if the issue persists.</p>
                    </body>
                </html>
                """)
            
            return JSONResponse({"error": str(e)}, status_code=400)


    @router.get("/auth-recovery")
    async def auth_recovery(request: Request):
        """Recovery endpoint to handle CSRF state validation issues."""
        try:
            # Get the state and code from the query parameters
            state = request.query_params.get("state")
            code = request.query_params.get("code")
            
            if not state or not code:
                return JSONResponse({"error": "Missing state or code parameter"}, status_code=400)
            
            logger.info(f"Auth recovery initiated with state: {state}, code: {code[:10]}...")
            
            # Manually set the state in the session
            request.session["oauth_state"] = state
            
            # Determine base URL if not provided
            base_url = api_base_url
            if not base_url:
                # Try to determine from request
                base_url = str(request.base_url).rstrip('/')
            
            # Manually construct URL parameters for the callback
            callback_url = f"{base_url}/callback?state={state}&code={code}"
            
            # Redirect to the callback endpoint with the parameters
            return RedirectResponse(url=callback_url)
        except Exception as e:
            logger.error(f"Error in auth recovery: {str(e)}")
            return JSONResponse({"error": str(e)}, status_code=400)


    @router.get("/refresh", response_model=TokenResponse)
    async def refresh_token(refresh_token: str = None, request: Request = None):
        """
        Refresh an access token using a refresh token.
        
        Args:
            refresh_token: Refresh token (optional if available in session)
            request: Request object for session access
            
        Returns:
            TokenResponse: New tokens
            
        Raises:
            HTTPException: If refresh fails
        """
        try:
            # Get refresh token from query param or session
            if not refresh_token and request:
                refresh_token = request.session.get("refresh_token")

            if not refresh_token:
                raise HTTPException(status_code=400, detail="Refresh token required")

            # Prepare refresh token request
            token_endpoint = f"{keycloak_url}/realms/{keycloak_realm}/protocol/openid-connect/token"
            payload = {
                "grant_type": "refresh_token",
                "client_id": client_id,
                "client_secret": client_secret,
                "refresh_token": refresh_token
            }

            # Send refresh request
            async with httpx.AsyncClient() as client:
                response = await client.post(token_endpoint, data=payload)

            if response.status_code != 200:
                logger.error(f"Token refresh failed: {response.text}")
                raise HTTPException(status_code=401, detail="Token refresh failed")

            # Parse token response
            token_data = response.json()

            # Update session if applicable
            if request:
                request.session["access_token"] = token_data["access_token"]
                request.session["refresh_token"] = token_data["refresh_token"]

            return TokenResponse(
                access_token=token_data["access_token"],
                token_type=token_data["token_type"],
                expires_in=token_data["expires_in"],
                refresh_token=token_data["refresh_token"],
                refresh_expires_in=token_data.get("refresh_expires_in"),
                scope=token_data.get("scope")
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error refreshing token: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Token refresh error: {str(e)}")


    @router.get("/logout")
    def logout(request: Request):
        """
        Log out by clearing session and redirecting to Keycloak logout.
        
        Args:
            request: Request object for session access
            
        Returns:
            RedirectResponse: Redirect to Keycloak logout
        """
        # Clear session
        request.session.clear()

        # Determine base URL if not provided
        base_url = api_base_url
        if not base_url:
            # Try to determine from request
            base_url = str(request.base_url).rstrip('/')

        # Construct Keycloak logout URL
        logout_url = f"{keycloak_url}/realms/{keycloak_realm}/protocol/openid-connect/logout"
        redirect_url = f"{base_url}/docs"

        # Redirect to Keycloak logout
        return RedirectResponse(f"{logout_url}?redirect_uri={redirect_url}")


    # Token saving endpoint for Swagger UI login
    @router.post("/save-token")
    async def save_token(request: Request):
        """
        Save token in session - Used by the Swagger UI login form.
        
        Args:
            request: Request object with token data
            
        Returns:
            Dict: Success message
            
        Raises:
            HTTPException: If token is missing
        """
        data = await request.json()
        access_token = data.get("access_token")
        refresh_token = data.get("refresh_token")
        
        if not access_token:
            return JSONResponse({"error": "Access token required"}, status_code=400)
        
        # Store tokens in session
        request.session["access_token"] = access_token
        if refresh_token:
            request.session["refresh_token"] = refresh_token
        
        logger.info(f"Token saved in session via API: {access_token[:20]}...")
        
        return {"status": "success", "message": "Token saved in session"}


    # API logout endpoint for Swagger UI
    @router.post("/logout-api")
    async def logout_api(request: Request):
        """
        Clear session - Used by the Swagger UI logout button.
        
        Args:
            request: Request object for session access
            
        Returns:
            Dict: Success message
        """
        # Clear session
        request.session.clear()
        logger.info("Session cleared via API logout")
        
        return {"status": "success", "message": "Logged out successfully"}


    # Debug endpoint to check session data (useful for troubleshooting)
    @router.get("/debug/session", include_in_schema=False)
    async def debug_session(request: Request):
        """
        Debug endpoint to check session data.
        
        Args:
            request: Request object for session access
            
        Returns:
            Dict: Session data with token preview
        """
        session_data = {}
        for key, value in request.session.items():
            if key == "access_token" and value:
                session_data[key] = f"{value[:20]}..." # Show only the beginning of the token
            else:
                session_data[key] = value
        
        return {"session": session_data}
    
    # API endpoint to get a token from username/password
    @router.post("/token", response_model=TokenResponse)
    async def get_token(username: str, password: str):
        """
        Get a token using username and password credentials.
        
        Args:
            username: Keycloak username
            password: Keycloak password
            
        Returns:
            TokenResponse: Token response
            
        Raises:
            HTTPException: If authentication fails
        """
        try:
            # Prepare token request
            token_endpoint = f"{keycloak_url}/realms/{keycloak_realm}/protocol/openid-connect/token"
            payload = {
                "grant_type": "password",
                "client_id": client_id,
                "client_secret": client_secret,
                "username": username,
                "password": password
            }

            # Send token request
            async with httpx.AsyncClient() as client:
                response = await client.post(token_endpoint, data=payload)

            if response.status_code != 200:
                logger.error(f"Token request failed: {response.text}")
                raise HTTPException(status_code=401, detail="Authentication failed")

            # Parse token response
            token_data = response.json()

            return TokenResponse(
                access_token=token_data["access_token"],
                token_type=token_data["token_type"],
                expires_in=token_data["expires_in"],
                refresh_token=token_data["refresh_token"],
                refresh_expires_in=token_data.get("refresh_expires_in"),
                scope=token_data.get("scope")
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting token: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Token request error: {str(e)}")
    
    return router
