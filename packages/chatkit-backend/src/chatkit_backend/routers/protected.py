"""
Protected routes requiring authentication

Demonstrates how to use auth middleware with FastAPI routes.
"""

from fastapi import APIRouter, Depends
from typing import Optional

from chatkit_backend.middleware.auth import (
    AuthSession,
    require_auth,
    optional_auth,
)

router = APIRouter(prefix="/api/protected", tags=["protected"])


@router.get("/me")
async def get_current_user(session: AuthSession = Depends(require_auth)):
    """
    Get the current authenticated user.

    Requires valid session cookie from BetterAuth.
    """
    return {
        "user": {
            "id": session.user.id,
            "email": session.user.email,
            "name": session.user.name,
        },
        "session_id": session.session_id,
    }


@router.get("/whoami")
async def whoami(session: Optional[AuthSession] = Depends(optional_auth)):
    """
    Get current user if authenticated, otherwise anonymous.

    Uses optional auth - doesn't require login.
    """
    if session:
        return {
            "authenticated": True,
            "user": {
                "id": session.user.id,
                "email": session.user.email,
                "name": session.user.name,
            },
        }

    return {
        "authenticated": False,
        "user": None,
    }
