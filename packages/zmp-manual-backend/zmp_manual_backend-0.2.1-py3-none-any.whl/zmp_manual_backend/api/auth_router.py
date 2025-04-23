import json
import logging
import os
import sys

import urllib.parse
from typing import Optional
import requests

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm


# Import Keycloak functionality
try:
    from zmp_manual_backend.api.oauth2_keycloak import (
        KEYCLOAK_AUTH_ENDPOINT,
        KEYCLOAK_CLIENT_ID,
        KEYCLOAK_CLIENT_SECRET,
        KEYCLOAK_REDIRECT_URI,
        KEYCLOAK_TOKEN_ENDPOINT,
        KEYCLOAK_USER_ENDPOINT,
        HTTP_CLIENT_SSL_VERIFY,
        get_current_user,
        TokenData,
        oauth2_scheme as keycloak_oauth2_scheme,
        refresh_token as keycloak_refresh_token,
        KEYCLOAK_SERVER_URL,
        KEYCLOAK_REALM,
        PUBLIC_KEY,
    )
except ImportError:
    logger = logging.getLogger("appLogger")
    logger.error("Failed to import Keycloak functionality")
    raise ImportError("Keycloak authentication is required but not available")

logger = logging.getLogger("appLogger")

router = APIRouter()


def save_token_data(tokens, user_info=None):
    """Save token data to files in the user's home directory."""
    token_dir = os.path.expanduser("~/.zmp-tokens")
    os.makedirs(token_dir, exist_ok=True)

    # Save the full token response
    with open(os.path.join(token_dir, "token.json"), "w") as f:
        json.dump(
            {
                "access_token": tokens.get("access_token"),
                "refresh_token": tokens.get("refresh_token"),
                "token_type": tokens.get("token_type", "bearer"),
                "expires_in": tokens.get("expires_in"),
                "user_info": user_info,
            },
            f,
            indent=2,
        )

    # Save just the access token to a separate file
    with open(os.path.join(token_dir, "access_token.txt"), "w") as f:
        f.write(tokens.get("access_token", ""))

    # Save the bearer token format
    with open(os.path.join(token_dir, "bearer_token.txt"), "w") as f:
        f.write(f"Bearer {tokens.get('access_token', '')}")

    print(f"Token data saved to {token_dir}/")


@router.get("/keycloak/auth-url")
async def get_keycloak_auth_url(
    redirect_uri: Optional[str] = None,
    state: Optional[str] = None,
    scope: Optional[str] = "openid profile email",
):
    """Get the Keycloak authorization URL."""
    if not redirect_uri:
        redirect_uri = KEYCLOAK_REDIRECT_URI

    auth_params = {
        "client_id": KEYCLOAK_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": scope,
    }

    if state:
        auth_params["state"] = state

    auth_url = f"{KEYCLOAK_AUTH_ENDPOINT}?{urllib.parse.urlencode(auth_params)}"
    logger.info(f"Redirecting to Keycloak: {auth_url}")

    return {"auth_url": auth_url}


@router.get(
    "/docs/oauth2-redirect", summary="Keycloak OAuth2 callback for the redirect URI"
)
def callback(request: Request, code: str):
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": KEYCLOAK_REDIRECT_URI,
        "client_id": KEYCLOAK_CLIENT_ID,
        "client_secret": KEYCLOAK_CLIENT_SECRET,
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }
    idp_response = requests.post(
        KEYCLOAK_TOKEN_ENDPOINT,
        data=data,
        headers=headers,
        verify=HTTP_CLIENT_SSL_VERIFY,
    )  # verify=False: because of the SKCC self-signed certificate

    if idp_response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid token")

    tokens = idp_response.json()

    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")
    # id_token = tokens.get("id_token")

    headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json"}
    idp_response = requests.get(
        KEYCLOAK_USER_ENDPOINT, headers=headers, verify=HTTP_CLIENT_SSL_VERIFY
    )  # verify=False: because of the SKCC self-signed certificate
    if idp_response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_info = idp_response.json()

    logger.debug(f"user_info: {user_info}")

    # because the max size of the cookie is 4kb, the session middleware saves the session data in the client side cookie in default
    # so, if the session data size is over than 4kb, the session data will be lost or occur the error in client side
    # request.session['access_token'] = access_token
    # request.session['id_token'] = id_token
    request.session["refresh_token"] = refresh_token
    request.session["user_info"] = user_info

    total_bytes = _get_size(request.session)

    if total_bytes > 4096:
        logger.debug(f"Total bytes: {total_bytes}")
        logger.warning(f"The session data size({total_bytes}) is over than 4kb.")
        raise HTTPException(status_code=401, detail="Invalid token")

    # If the same-site of cookie is 'lax', the cookie will be sent only if the request is same-site request
    # If the same-site of cookie is 'strict', the cookie will not be sent
    # return RedirectResponse(url=f"{ALERT_SERVICE_ENDPOINT}/home")

    return tokens


def _get_size(obj, seen=None):
    """Recursively find the size of objects including nested objects."""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Mark as seen
    seen.add(obj_id)
    # Recursively add sizes of referred objects
    if isinstance(obj, dict):
        size += sum([_get_size(v, seen) for v in obj.values()])
        size += sum([_get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, "__dict__"):
        size += _get_size(obj.__dict__, seen)
    elif hasattr(obj, "__iter__") and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([_get_size(i, seen) for i in obj])
    return size


async def get_token(request: Request):
    """Extract and validate the token from the Authorization header."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = auth_header.split("Bearer ")[1]

    # Do a basic token validation to ensure it's a proper JWT
    parts = token.split(".")
    if len(parts) != 3:
        logger.error(
            f"Invalid token format: token has {len(parts)} segments, expected 3"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token


@router.post("/refresh")
async def refresh_access_token(request: Request):
    """Refresh an access token using a refresh token."""
    # Try to get the refresh token from the request body
    try:
        body = await request.json()
        refresh_token_str = body.get("refresh_token")
    except Exception:
        refresh_token_str = None

    # If not in the body, try to get it from the headers
    if not refresh_token_str:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            refresh_token_str = auth_header[7:]

    if not refresh_token_str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Refresh token is required",
        )

    try:
        # Use Keycloak's refresh token mechanism
        tokens = keycloak_refresh_token(refresh_token_str)

        # Get user info using the new access token
        access_token = tokens.get("access_token")
        if access_token:
            user_info = get_current_user(access_token)
            # Save tokens to files for CLI usage
            save_token_data(tokens, user_info)

        return tokens
    except Exception as e:
        logger.error(f"Error refreshing token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error refreshing token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/users/me", summary="Get the current user info from IDP(Keycloak)")
def read_users_me(token: str = Depends(keycloak_oauth2_scheme)):
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    idp_response = requests.get(
        KEYCLOAK_USER_ENDPOINT, headers=headers, verify=HTTP_CLIENT_SSL_VERIFY
    )  # verify=False: because of the SKCC self-signed certificate
    if idp_response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid token")

    return idp_response.json()


@router.get(
    "/users/oauth_user",
    summary="Get the current user info from Token",
    openapi_extra={"security": [{"OAuth2AuthorizationCodeBearer": []}]},
)
def read_oauth_user(oauth_user: TokenData = Depends(get_current_user)):
    return oauth_user


@router.get("/debug/oauth2")
async def debug_oauth2():
    """Debug endpoint to get information about the OAuth2 configuration.

    This endpoint returns information about the OAuth2 configuration for debugging purposes.
    It is not included in the API schema.
    """
    # Get the OpenID configuration from the Keycloak server
    openid_config = {}
    try:
        openid_url = f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/.well-known/openid-configuration"
        response = requests.get(openid_url, verify=HTTP_CLIENT_SSL_VERIFY, timeout=10)
        if response.status_code == 200:
            openid_config = response.json()
        else:
            openid_config = {
                "error": f"Failed to get OpenID configuration: {response.status_code}"
            }
    except Exception as e:
        openid_config = {"error": f"Error getting OpenID configuration: {str(e)}"}

    return {
        "message": "OAuth2 Configuration Debug Information",
        "public_key_available": PUBLIC_KEY is not None,
        "keycloak_config": {
            "server_url": KEYCLOAK_SERVER_URL,
            "realm": KEYCLOAK_REALM,
            "client_id": KEYCLOAK_CLIENT_ID,
            "auth_endpoint": KEYCLOAK_AUTH_ENDPOINT,
            "token_endpoint": KEYCLOAK_TOKEN_ENDPOINT,
            "user_endpoint": KEYCLOAK_USER_ENDPOINT,
            "jwks_endpoint": f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/certs",
        },
        "environment": {
            "KEYCLOAK_SERVER_URL": os.environ.get("KEYCLOAK_SERVER_URL", "Not set"),
            "KEYCLOAK_REALM": os.environ.get("KEYCLOAK_REALM", "Not set"),
            "KEYCLOAK_CLIENT_ID": os.environ.get("KEYCLOAK_CLIENT_ID", "Not set"),
        },
        "openid_configuration": openid_config,
    }


@router.post("/login")
@router.get("/login")
async def login_redirect():
    """
    Login endpoint that redirects to Keycloak OAuth2 login.
    This endpoint is provided for backward compatibility with any clients
    still using the /login endpoint.
    """
    logger.info("Received login request, redirecting to Keycloak OAuth2 flow")
    auth_params = {
        "client_id": KEYCLOAK_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": KEYCLOAK_REDIRECT_URI,
        "scope": "openid profile email",
    }

    auth_url = f"{KEYCLOAK_AUTH_ENDPOINT}?{urllib.parse.urlencode(auth_params)}"
    return RedirectResponse(url=auth_url)


@router.post("/token")
async def token_exchange(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    Token endpoint that exchanges credentials for access token.
    This endpoint is compatible with the OAuth2 token endpoint and
    forwards the request to Keycloak.
    """
    logger.info(
        f"Token request received for client: {form_data.client_id or KEYCLOAK_CLIENT_ID}"
    )

    try:
        # Forward the token request to Keycloak
        data = {
            "grant_type": "password",
            "username": form_data.username,
            "password": form_data.password,
            "client_id": form_data.client_id or KEYCLOAK_CLIENT_ID,
            "scope": " ".join(form_data.scopes)
            if form_data.scopes
            else "openid profile email",
        }

        # Add client secret if available
        if KEYCLOAK_CLIENT_SECRET:
            data["client_secret"] = KEYCLOAK_CLIENT_SECRET

        response = requests.post(
            KEYCLOAK_TOKEN_ENDPOINT,
            data=data,
            verify=HTTP_CLIENT_SSL_VERIFY,
            timeout=10,
        )

        if response.status_code != 200:
            logger.error(f"Token exchange failed: Status {response.status_code}")
            return JSONResponse(
                status_code=response.status_code,
                content=response.json(),
            )

        tokens = response.json()

        # Get user info using the access token
        access_token = tokens.get("access_token")
        if access_token:
            user_info = get_current_user(access_token)
            # Save tokens to files for CLI usage
            save_token_data(tokens, user_info)

        return tokens
    except Exception as e:
        logger.error(f"Error exchanging token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error exchanging token: {str(e)}",
        )
