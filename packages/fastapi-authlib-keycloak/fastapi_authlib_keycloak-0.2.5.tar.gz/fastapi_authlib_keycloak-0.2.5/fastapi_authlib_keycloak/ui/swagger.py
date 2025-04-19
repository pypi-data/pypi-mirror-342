#!/usr/bin/env python3
"""
Custom Swagger UI Implementation for FastAPI-Authlib-Keycloak Integration.

This module provides a custom Swagger UI implementation that includes
authentication controls and token handling with IBM Carbon Design System styling.
"""

import os
import logging
import pkgutil
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles


def setup_swagger_ui(
    app: FastAPI,
    keycloak_url: str,
    keycloak_realm: str,
    client_id: str,
    client_secret: str,
    api_base_url: Optional[str] = None,
    custom_title: Optional[str] = None,
    custom_css_path: Optional[str] = None,
    logger: Optional[logging.Logger] = None,
):
    """
    Set up custom Swagger UI routes and OpenAPI schema.

    Args:
        app: FastAPI application instance
        keycloak_url: URL of the Keycloak server
        keycloak_realm: Keycloak realm name
        client_id: Client ID for authentication
        client_secret: Client secret
        api_base_url: Base URL for the API
        custom_title: Custom title for the Swagger UI page
        custom_css_path: Path to custom CSS file
        logger: Logger instance
    """
    # Initialize logger if not provided
    logger = logger or logging.getLogger("fastapi-keycloak.swagger")
    
    # Determine static files path
    package_dir = Path(__file__).parent
    static_dir = package_dir / "static"
    
    # Mount static files if directory exists
    if static_dir.exists() and static_dir.is_dir():
        app.mount("/keycloak-auth-static", StaticFiles(directory=str(static_dir)), name="keycloak-auth-static")
        logger.info(f"Mounted static files from {static_dir}")
    else:
        logger.warning(f"Static directory not found at {static_dir}, using default styles")

    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html(request: Request):
        """
        Custom Swagger UI that includes authentication with Carbon Design System styling.

        This implementation allows the Swagger UI to:
        1. Use the session token for auth if available
        2. Provide a login button if not authenticated
        3. Include the token in all API requests
        """
        # Check if we have a token in session
        access_token = request.session.get("access_token", "")

        # Log token presence for debugging
        if access_token:
            logger.info(f"Token found in session for /docs endpoint: {access_token[:20]}...")
        else:
            logger.warning("No token found in session for /docs endpoint")

        # Get OpenAPI schema URL
        openapi_url = "/openapi.json"
        
        # Determine base URL if not provided
        base_url = api_base_url
        if not base_url:
            # Try to determine from request
            base_url = str(request.base_url).rstrip('/')
            logger.info(f"Auto-detected API base URL: {base_url}")

        # Use custom title or app title
        title = custom_title or app.title
        
        # Try to load CSS content
        css_content = ""
        
        # If custom CSS path is provided, try to load it
        if custom_css_path and os.path.isfile(custom_css_path):
            try:
                with open(custom_css_path, 'r') as css_file:
                    css_content = css_file.read()
                logger.info(f"Loaded custom CSS from {custom_css_path}")
            except Exception as e:
                logger.error(f"Error loading custom CSS: {str(e)}")
        
        # If no custom CSS was loaded successfully, try to load default CSS
        if not css_content:
            try:
                # Check if the Carbon CSS file exists in static folder
                css_path = static_dir / "carbon-swagger.css"
                if css_path.exists():
                    with open(css_path, 'r') as css_file:
                        css_content = css_file.read()
                    logger.info("Loaded Carbon Design System CSS")
                else:
                    # Load basic CSS as a fallback
                    css_content = """
                    .custom-topbar {
                        background-color: #0f62fe;
                        padding: 10px 20px;
                        color: white;
                    }
                    .topbar-wrapper {
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                    }
                    .topbar-logo {
                        font-weight: bold;
                    }
                    .auth-controls {
                        display: flex;
                        align-items: center;
                        gap: 10px;
                    }
                    .auth-status {
                        padding: 5px 10px;
                        border-radius: 4px;
                    }
                    .not-authenticated {
                        background-color: #da1e28;
                    }
                    .authenticated {
                        background-color: #24a148;
                    }
                    .login-button, .logout-button {
                        padding: 5px 10px;
                        border: none;
                        border-radius: 4px;
                        cursor: pointer;
                    }
                    .login-button {
                        background-color: #0043ce;
                        color: white;
                    }
                    .login-button:hover {
                        background-color: #0353e9;
                    }
                    .logout-button {
                        background-color: #393939;
                        color: white;
                    }
                    .logout-button:hover {
                        background-color: #4c4c4c;
                    }
                    .modal {
                        display: none;
                        position: fixed;
                        z-index: 100;
                        left: 0;
                        top: 0;
                        width: 100%;
                        height: 100%;
                        overflow: auto;
                        background-color: rgba(0,0,0,0.4);
                    }
                    .modal-content {
                        background-color: #fefefe;
                        margin: 15% auto;
                        padding: 20px;
                        border: 1px solid #888;
                        width: 80%;
                        max-width: 600px;
                        border-radius: 4px;
                    }
                    .close {
                        color: #aaa;
                        float: right;
                        font-size: 28px;
                        font-weight: bold;
                    }
                    .close:hover,
                    .close:focus {
                        color: black;
                        text-decoration: none;
                        cursor: pointer;
                    }
                    .modal-header {
                        padding-bottom: 10px;
                        border-bottom: 1px solid #eee;
                    }
                    .modal-body {
                        padding: 20px 0;
                    }
                    .modal-footer {
                        padding-top: 10px;
                        border-top: 1px solid #eee;
                        text-align: right;
                    }
                    .form-group {
                        margin-bottom: 15px;
                    }
                    .form-group label {
                        display: block;
                        margin-bottom: 5px;
                    }
                    .form-group input {
                        width: 100%;
                        padding: 8px;
                        border: 1px solid #ddd;
                        border-radius: 4px;
                    }
                    .modal-error {
                        color: #da1e28;
                        margin: 10px 0;
                        display: none;
                    }
                    .modal-success {
                        color: #24a148;
                        margin: 10px 0;
                        display: none;
                    }
                    .token-display {
                        display: none;
                        margin-top: 20px;
                        padding: 10px;
                        background-color: #f4f4f4;
                        border-radius: 4px;
                    }
                    .token-display pre {
                        background-color: #262626;
                        color: white;
                        padding: 10px;
                        border-radius: 4px;
                        overflow-x: auto;
                    }
                    .token-info {
                        margin-top: 10px;
                        font-size: 14px;
                    }
                    .copy-button {
                        background-color: #0043ce;
                        color: white;
                        border: none;
                        padding: 5px 10px;
                        border-radius: 4px;
                        cursor: pointer;
                    }
                    .token-info-button {
                        background-color: #0043ce;
                        color: white;
                    }
                    """
                    logger.info("Using basic CSS fallback")
            except Exception as e:
                logger.error(f"Error loading default CSS: {str(e)}")
                # Minimal inline CSS as a last resort
                css_content = ".custom-topbar { background-color: #0f62fe; padding: 10px; color: white; }"

        # Render Swagger UI with authentication and styling
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link type="text/css" rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
            <title>{title} - API Documentation</title>
            <style>
                {css_content}
            </style>
        </head>
        <body>
            <!-- Custom topbar with auth controls -->
            <div class="custom-topbar">
                <div class="topbar-wrapper">
                    <div class="topbar-logo">{title}</div>
                    <div class="auth-controls">
                        <div id="auth-status" class="auth-status not-authenticated">Not authenticated</div>
                        <button id="login-btn" class="login-button">Login</button>
                        <button id="logout-btn" class="logout-button">Logout</button>
                    </div>
                </div>
            </div>

            <!-- Authentication modal -->
            <div id="auth-modal" class="modal">
                <div class="modal-content">
                    <div class="modal-header">
                        <span class="close">&times;</span>
                        <h2>Keycloak Authentication</h2>
                    </div>
                    <div class="modal-body">
                        <div class="form-group">
                            <label for="username">Username</label>
                            <input type="text" id="username" placeholder="Enter your username" />
                        </div>
                        <div class="form-group">
                            <label for="password">Password</label>
                            <input type="password" id="password" placeholder="Enter your password" />
                        </div>
                        <div id="modal-error" class="modal-error"></div>
                        <div id="modal-success" class="modal-success"></div>

                        <!-- Token display section -->
                        <div id="token-display" class="token-display">
                            <h3>Your Access Token</h3>
                            <div style="display: flex; align-items: center; justify-content: space-between;">
                                <span>Token Preview:</span>
                                <button id="copy-token" class="copy-button">Copy Full Token</button>
                            </div>
                            <pre id="token-preview"></pre>
                            <div class="token-info">
                                <div>Expires in: <span id="token-expires"></span></div>
                                <div>Scope: <span id="token-scope"></span></div>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button id="auth-close" class="login-button">Close</button>
                        <button id="modal-login-btn" class="login-button">Login</button>
                    </div>
                </div>
            </div>

            <!-- Swagger UI container -->
            <div id="swagger-ui"></div>

            <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
            <script>
                // Token and auth state management
                let currentToken = "{access_token}";
                let tokenExpiry = null;
                let tokenExpiryInterval = null;
                let tokenData = null;

                // DOM Elements
                const authStatus = document.getElementById('auth-status');
                const loginBtn = document.getElementById('login-btn');
                const logoutBtn = document.getElementById('logout-btn');
                const authModal = document.getElementById('auth-modal');
                const modalClose = document.getElementsByClassName('close')[0];
                const authClose = document.getElementById('auth-close');
                const modalLoginBtn = document.getElementById('modal-login-btn');
                const modalError = document.getElementById('modal-error');
                const modalSuccess = document.getElementById('modal-success');
                const tokenDisplay = document.getElementById('token-display');
                const tokenPreview = document.getElementById('token-preview');
                const tokenExpires = document.getElementById('token-expires');
                const tokenScope = document.getElementById('token-scope');
                const copyTokenBtn = document.getElementById('copy-token');

                // Initialize Swagger UI with custom auth plugin
                const ui = SwaggerUIBundle({{
                    url: '{openapi_url}',
                    dom_id: '#swagger-ui',
                    deepLinking: true,
                    layout: "BaseLayout",
                    showExtensions: true,
                    showCommonExtensions: true,
                    persistAuthorization: true,
                    presets: [
                        SwaggerUIBundle.presets.apis,
                        SwaggerUIBundle.SwaggerUIStandalonePreset
                    ],
                    // Called when Swagger UI has fully loaded
                    onComplete: () => {{
                        console.log("Swagger UI initialization complete");
                        // If we have a token, apply it now that Swagger UI is ready
                        if (currentToken && currentToken.length > 0) {{
                            console.log("Applying token from onComplete handler");
                            safeAuthorize(currentToken);
                        }}
                    }},
                    plugins: [
                        // Custom plugin to enhance Swagger UI behavior
                        function(system) {{
                            return {{
                                statePlugins: {{
                                    spec: {{
                                        wrapSelectors: {{
                                            allowTryItOutFor: (ori, system) => (path, method) => {{
                                                // Simply return the original result without adding custom buttons
                                                return ori(path, method);
                                            }}
                                        }}
                                    }}
                                }}
                            }}
                        }}
                    ],
                    initOAuth: {{
                        clientId: '{client_id}',
                        appName: '{title}',
                        usePkceWithAuthorizationCodeGrant: true,
                        scopes: 'openid profile email'
                    }}
                }});

                // Function to update the auth status display
                function updateAuthStatus() {{
                    if (currentToken && currentToken.length > 0) {{
                        // User is authenticated
                        authStatus.textContent = 'Authenticated';
                        authStatus.className = 'auth-status authenticated';
                        
                        // Change login button to "Token-info"
                        loginBtn.textContent = 'Token-info';
                        loginBtn.className = 'login-button token-info-button';
                    }} else {{
                        // User is not authenticated
                        authStatus.textContent = 'Not authenticated';
                        authStatus.className = 'auth-status not-authenticated';
                        
                        // Reset login button
                        loginBtn.textContent = 'Login';
                        loginBtn.className = 'login-button';
                    }}
                }}

                // Parse and decode JWT token
                function parseJwt(token) {{
                    try {{
                        const base64Url = token.split('.')[1];
                        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
                        const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {{
                            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
                        }}).join(''));
                        return JSON.parse(jsonPayload);
                    }} catch(e) {{
                        console.error('Error parsing JWT token:', e);
                        return null;
                    }}
                }}

                // Function to display token information
                function displayTokenInfo() {{
                    tokenDisplay.style.display = 'block';

                    if (tokenData) {{
                        // Format token with Bearer prefix if not present
                        const formattedToken = currentToken.startsWith('Bearer ') ? currentToken : `Bearer ${{currentToken}}`;
                        
                        // Display token preview
                        tokenPreview.textContent = formattedToken.substring(0, 40) + '...';

                        // Set expiry information
                        const expiresIn = tokenData.exp ? new Date(tokenData.exp * 1000) : null;
                        if (expiresIn) {{
                            const now = new Date();
                            const diffMs = expiresIn - now;
                            const diffMins = Math.round(diffMs / 60000);
                            tokenExpires.textContent = diffMins + ' minutes (' + expiresIn.toLocaleTimeString() + ')';
                        }} else {{
                            tokenExpires.textContent = 'Unknown';
                        }}

                        // Set scope information
                        tokenScope.textContent = tokenData.scope || 'Not specified';
                    }} else {{
                        tokenPreview.textContent = 'Could not parse token';
                        tokenExpires.textContent = 'Unknown';
                        tokenScope.textContent = 'Unknown';
                    }}
                }}

                // Safe method to authorize that avoids potential schema errors
                function safeAuthorize(token) {{
                    try {{
                        // Format the token with Bearer prefix if needed
                        const formattedToken = token.startsWith('Bearer ') ? token : `Bearer ${{token}}`;
                        
                        // Use the correct method to authorize in Swagger UI v5
                        if (ui && ui.preauthorizeApiKey) {{
                            ui.preauthorizeApiKey("bearerAuth", formattedToken);
                            console.log("Successfully authorized with Swagger UI API");
                            
                            // Also update our custom UI
                            updateAuthStatus();
                            return true;
                        }} else {{
                            console.warn("Swagger UI not fully initialized, authorization deferred");
                            return false;
                        }}
                    }} catch (e) {{
                        console.error("Error in safeAuthorize:", e);
                        return false;
                    }}
                }}

                // Function to apply token to Swagger UI
                function applyTokenToSwaggerUI(token) {{
                    // Store the token in our state
                    currentToken = token;

                    // Parse token data
                    tokenData = parseJwt(token);
                    
                    // Use our safe authorization method
                    safeAuthorize(token);
                    
                    // Update our custom UI state
                    updateAuthStatus();

                    // Start token expiry tracking if we have expiry info
                    if (tokenData && tokenData.exp) {{
                        tokenExpiry = new Date(tokenData.exp * 1000);

                        // Clear any existing interval
                        if (tokenExpiryInterval) {{
                            clearInterval(tokenExpiryInterval);
                        }}

                        // Check token expiry every minute
                        tokenExpiryInterval = setInterval(() => {{
                            const now = new Date();
                            if (now >= tokenExpiry) {{
                                // Token expired, clear it
                                clearTokenAndLogout();
                                clearInterval(tokenExpiryInterval);
                                tokenExpiryInterval = null;
                                alert('Your authentication session has expired. Please login again.');
                            }}
                        }}, 60000); // Check every minute
                    }}
                }}

                // Function to clear token and logout
                async function clearTokenAndLogout() {{
                    try {{
                        // Clear auth in Swagger UI (using a try-catch to handle potential errors)
                        try {{
                            if (ui && ui.preauthorizeApiKey) {{
                                ui.preauthorizeApiKey("bearerAuth", "");
                            }}
                        }} catch (e) {{
                            console.warn("Error clearing Swagger UI auth:", e);
                        }}
                        
                        // Clear our local state
                        currentToken = "";
                        tokenData = null;

                        // Clear any expiry interval
                        if (tokenExpiryInterval) {{
                            clearInterval(tokenExpiryInterval);
                            tokenExpiryInterval = null;
                        }}

                        // Clear token in session
                        await fetch("/logout-api", {{
                            method: 'POST'
                        }});

                        // Clear form fields
                        document.getElementById('username').value = "";
                        document.getElementById('password').value = "";

                        // Hide token display
                        tokenDisplay.style.display = 'none';

                        // Reset errors/success messages
                        modalError.style.display = "none";
                        modalSuccess.textContent = "Logged out successfully";
                        modalSuccess.style.display = "block";

                        updateAuthStatus();
                    }} catch (error) {{
                        console.error('Logout error:', error);
                        modalError.textContent = "Logout failed";
                        modalError.style.display = "block";
                    }}
                }}

                // Login functionality
                async function performLogin() {{
                    const username = document.getElementById('username').value;
                    const password = document.getElementById('password').value;

                    modalError.style.display = "none";
                    modalSuccess.style.display = "none";

                    if (!username || !password) {{
                        modalError.textContent = "Please enter both username and password";
                        modalError.style.display = "block";
                        return;
                    }}

                    try {{
                        // Get token from Keycloak
                        const response = await fetch("{keycloak_url}/realms/{keycloak_realm}/protocol/openid-connect/token", {{
                            method: 'POST',
                            headers: {{
                                'Content-Type': 'application/x-www-form-urlencoded',
                                'Accept': 'application/json',
                                'X-Requested-With': 'XMLHttpRequest'
                            }},
                            credentials: 'include',
                            body: new URLSearchParams({{
                                'client_id': '{client_id}',
                                'client_secret': '{client_secret}',
                                'grant_type': 'password',
                                'username': username,
                                'password': password
                            }})
                        }});

                        if (!response.ok) {{
                            const data = await response.json();
                            throw new Error(data.error_description || data.error || 'Authentication failed');
                        }}

                        const data = await response.json();
                        const token = data.access_token;

                        // Apply token to Swagger UI
                        applyTokenToSwaggerUI(token);

                        // Save token in session via API call
                        await fetch("/save-token", {{
                            method: 'POST',
                            headers: {{
                                'Content-Type': 'application/json'
                            }},
                            body: JSON.stringify({{
                                'access_token': token,
                                'refresh_token': data.refresh_token
                            }})
                        }});

                        // Show success message
                        modalSuccess.textContent = "Login successful!";
                        modalSuccess.style.display = "block";

                        // Show token information
                        displayTokenInfo();
                    }} catch (error) {{
                        console.error('Login error:', error);
                        modalError.textContent = error.message || "Authentication failed";
                        modalError.style.display = "block";
                        tokenDisplay.style.display = 'none';
                    }}
                }}

                // Event Listeners
                loginBtn.addEventListener('click', () => {{
                    modalError.style.display = "none";
                    modalSuccess.style.display = "none";
                    
                    // Adjust modal content based on authentication state
                    if (currentToken && currentToken.length > 0) {{
                        // User is authenticated, show token info
                        document.querySelector('.modal-header h2').textContent = 'Authentication Information';
                        displayTokenInfo();
                        tokenDisplay.style.display = 'block';
                        
                        // Hide login form elements when showing token info
                        document.querySelectorAll('.form-group').forEach(el => {{
                            el.style.display = 'none';
                        }});
                        modalLoginBtn.style.display = 'none';
                    }} else {{
                        // User is not authenticated, show login form
                        document.querySelector('.modal-header h2').textContent = 'Keycloak Authentication';
                        tokenDisplay.style.display = 'none';
                        
                        // Show login form elements
                        document.querySelectorAll('.form-group').forEach(el => {{
                            el.style.display = 'block';
                        }});
                        modalLoginBtn.style.display = 'inline-block';
                    }}
                    
                    // Show the modal
                    authModal.style.display = 'block';
                }});

                logoutBtn.addEventListener('click', clearTokenAndLogout);

                modalClose.addEventListener('click', () => {{
                    authModal.style.display = 'none';
                }});

                authClose.addEventListener('click', () => {{
                    authModal.style.display = 'none';
                }});

                modalLoginBtn.addEventListener('click', performLogin);

                copyTokenBtn.addEventListener('click', () => {{
                    if (currentToken) {{
                        // Format token with Bearer prefix if not present
                        const formattedToken = currentToken.startsWith('Bearer ') ? currentToken : `Bearer ${{currentToken}}`;
                        
                        navigator.clipboard.writeText(formattedToken)
                            .then(() => {{
                                copyTokenBtn.textContent = 'Copied!';
                                setTimeout(() => {{
                                    copyTokenBtn.textContent = 'Copy Full Token';
                                }}, 2000);
                            }})
                            .catch(err => {{
                                console.error('Failed to copy token: ', err);
                            }});
                    }}
                }});

                // Close modal when clicking outside of it
                window.addEventListener('click', (event) => {{
                    if (event.target == authModal) {{
                        authModal.style.display = 'none';
                    }}
                }});

                // Handle keyboard events
                addEventListener('keydown', (event) => {{
                    // Close modal on Escape key
                    if (event.key === 'Escape' && authModal.style.display === 'block') {{
                        authModal.style.display = 'none';
                    }}

                    // Submit form on Enter key when in the login form
                    if (event.key === 'Enter' &&
                        (document.activeElement === document.getElementById('username') ||
                         document.activeElement === document.getElementById('password'))) {{
                        performLogin();
                    }}
                }});

                // Add auth token when available on page load
                if (currentToken && currentToken.length > 0) {{
                    console.log("Initializing with token");
                    // Initialization will be handled by the onComplete callback
                    // This ensures Swagger UI is fully ready before we attempt to authorize
                    console.log("Token found, will be applied when Swagger UI is ready");
                    
                    // We'll still update our custom UI immediately
                    updateAuthStatus();
                }} else {{
                    updateAuthStatus();
                }}
            </script>
        </body>
        </html>
        """

        # Return the HTML content as a response
        return HTMLResponse(content=html_content)

    @app.get("/openapi.json", include_in_schema=False)
    async def get_open_api_endpoint():
        """Generate and return OpenAPI schema with security components."""
        schema = get_openapi(
            title=custom_title or app.title,
            version=app.version,
            description=app.description + """

## Authentication

This API uses Keycloak for authentication. You can authenticate in two ways:

1. Use the **Login** button in the top bar to sign in with your Keycloak credentials
2. Click the **Authorize** button below and enter your token manually

Protected endpoints are marked with a 🔒 icon. Click this icon for quick authentication.

## Token Information

After logging in, you can view your token information by clicking your authentication status in the top bar.
            """,
            routes=app.routes,
        )

        # Add security schemes - use bearerAuth with enhanced description
        schema["components"] = schema.get("components", {})
        schema["components"]["securitySchemes"] = {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": f"""
## JWT Bearer Authentication

Enter your JWT token in the format: `Bearer {{token}}`

### How to get a token:

1. **Recommended**: Use the **Login** button at the top of the page
2. Use the `/token` endpoint with username and password parameters
3. Use a direct request to Keycloak's token endpoint:

```bash
curl -X POST \\
  {keycloak_url}/realms/{keycloak_realm}/protocol/openid-connect/token \\
  -H 'Content-Type: application/x-www-form-urlencoded' \\
  -d 'client_id={client_id}&client_secret={client_secret}&grant_type=password&username=YOUR_USERNAME&password=YOUR_PASSWORD'
```

The token will be returned in the `access_token` field of the response.
                """
            }
        }

        # Apply security globally
        schema["security"] = [{"bearerAuth": []}]

        # Add response examples and descriptions to enhance documentation
        for path in schema.get("paths", {}).values():
            for method in path.values():
                if "security" in method and method["security"]:
                    # Add 401 and 403 responses for secured endpoints
                    method["responses"] = method.get("responses", {})

                    # Add 401 response
                    method["responses"]["401"] = {
                        "description": "Unauthorized - Authentication required or token is invalid",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "detail": {"type": "string", "example": "Not authenticated"}
                                    }
                                }
                            }
                        }
                    }

                    # Add 403 response for role-restricted endpoints
                    if "/admin" in method.get("operationId", "") or "/developer" in method.get("operationId", ""):
                        method["responses"]["403"] = {
                            "description": "Forbidden - Insufficient permissions for this resource",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "detail": {"type": "string", "example": "Insufficient permissions. Required roles: ['admin']"}
                                        }
                                    }
                                }
                            }
                        }

        return schema
