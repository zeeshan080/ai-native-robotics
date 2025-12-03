"""User management API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from chatkit_backend.db import get_session, User
from chatkit_backend.models.user import (
    CreateUserRequest,
    UserResponse,
    ErrorResponse,
)

router = APIRouter(prefix="/user", tags=["User"])


@router.post(
    "/create",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {"model": ErrorResponse, "description": "User already exists"},
    },
)
async def create_user(
    request: CreateUserRequest,
    session: AsyncSession = Depends(get_session),
) -> UserResponse:
    """Create a new anonymous user.

    The user_id is client-generated (UUID v4 from localStorage).
    """
    # Check if user already exists
    result = await session.execute(select(User).where(User.id == request.user_id))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": "conflict", "message": "User with this ID already exists"},
        )

    # Create new user
    user = User(id=request.user_id, onboarding_completed=False)
    session.add(user)
    await session.flush()
    await session.refresh(user)

    return UserResponse.model_validate(user)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    responses={
        404: {"model": ErrorResponse, "description": "User not found"},
    },
)
async def get_user(
    user_id: str,
    session: AsyncSession = Depends(get_session),
) -> UserResponse:
    """Get user information by ID."""
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": "User not found"},
        )

    return UserResponse.model_validate(user)
