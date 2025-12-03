"""
BetterAuth session validation middleware for FastAPI

Validates session cookies against the BetterAuth service.
"""

import os
import httpx
from typing import Optional
from pydantic import BaseModel
from fastapi import Request, HTTPException


class AuthUser(BaseModel):
    """Authenticated user from BetterAuth session"""
    id: str
    email: str
    name: Optional[str] = None


class AuthSession(BaseModel):
    """Session data from BetterAuth"""
    user: AuthUser
    session_id: str
    expires_at: str


# Auth service URL - configurable via environment
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:3001")


async def get_session_from_cookie(request: Request) -> Optional[AuthSession]:
    """
    Validate session cookie against BetterAuth service.

    BetterAuth uses cookies for session management. This function
    forwards the cookie to the auth service to validate.

    Returns:
        AuthSession if valid, None if no session or invalid
    """
    # Get cookies from request
    cookies = request.cookies

    if not cookies:
        return None

    try:
        async with httpx.AsyncClient() as client:
            # Forward cookies to BetterAuth session endpoint
            response = await client.get(
                f"{AUTH_SERVICE_URL}/api/auth/get-session",
                cookies=dict(cookies),
                timeout=5.0,
            )

            if response.status_code != 200:
                return None

            data = response.json()

            if not data or not data.get("user"):
                return None

            return AuthSession(
                user=AuthUser(
                    id=data["user"]["id"],
                    email=data["user"]["email"],
                    name=data["user"].get("name"),
                ),
                session_id=data.get("session", {}).get("id", ""),
                expires_at=data.get("session", {}).get("expiresAt", ""),
            )

    except httpx.RequestError as e:
        # Log but don't fail - treat as no session
        print(f"Auth service request failed: {e}")
        return None
    except Exception as e:
        print(f"Session validation error: {e}")
        return None


async def require_auth(request: Request) -> AuthSession:
    """
    Dependency that requires authentication.

    Usage:
        @app.get("/protected")
        async def protected_route(session: AuthSession = Depends(require_auth)):
            return {"user": session.user.email}

    Raises:
        HTTPException 401 if not authenticated
    """
    session = await get_session_from_cookie(request)

    if not session:
        raise HTTPException(
            status_code=401,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Cookie"},
        )

    return session


async def optional_auth(request: Request) -> Optional[AuthSession]:
    """
    Dependency for optional authentication.

    Returns None if not authenticated instead of raising an error.

    Usage:
        @app.get("/maybe-protected")
        async def route(session: Optional[AuthSession] = Depends(optional_auth)):
            if session:
                return {"user": session.user.email}
            return {"user": "anonymous"}
    """
    return await get_session_from_cookie(request)
