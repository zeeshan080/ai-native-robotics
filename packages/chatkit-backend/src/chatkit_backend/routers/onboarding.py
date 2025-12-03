"""Onboarding and preferences API endpoints."""

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from chatkit_backend.db import get_session, User, UserPreferences
from chatkit_backend.models.user import (
    OnboardingRequest,
    UserPreferencesResponse,
    UpdatePreferencesRequest,
    ErrorResponse,
)

router = APIRouter(tags=["Onboarding"])


@router.post(
    "/onboarding",
    response_model=UserPreferencesResponse,
    responses={
        404: {"model": ErrorResponse, "description": "User not found"},
        400: {"model": ErrorResponse, "description": "Invalid preferences data"},
    },
)
async def submit_onboarding(
    request: OnboardingRequest,
    session: AsyncSession = Depends(get_session),
) -> UserPreferencesResponse:
    """Submit onboarding questionnaire and save user preferences."""
    # Get user
    result = await session.execute(select(User).where(User.id == request.user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": "User not found"},
        )

    # Check if preferences already exist
    prefs_result = await session.execute(
        select(UserPreferences).where(UserPreferences.user_id == request.user_id)
    )
    existing_prefs = prefs_result.scalar_one_or_none()

    if existing_prefs:
        # Update existing preferences
        existing_prefs.education_level = request.education_level
        existing_prefs.programming_experience = request.programming_experience
        existing_prefs.robotics_background = request.robotics_background
        existing_prefs.ai_ml_experience = request.ai_ml_experience
        existing_prefs.learning_goals = request.learning_goals
        existing_prefs.preferred_language = request.preferred_language
        preferences = existing_prefs
    else:
        # Create new preferences
        preferences = UserPreferences(
            user_id=request.user_id,
            education_level=request.education_level,
            programming_experience=request.programming_experience,
            robotics_background=request.robotics_background,
            ai_ml_experience=request.ai_ml_experience,
            learning_goals=request.learning_goals,
            preferred_language=request.preferred_language,
        )
        session.add(preferences)

    # Mark onboarding as completed
    user.onboarding_completed = True

    await session.flush()
    await session.refresh(preferences)

    return UserPreferencesResponse.model_validate(preferences)


@router.get(
    "/user/preferences",
    response_model=UserPreferencesResponse,
    responses={
        404: {"model": ErrorResponse, "description": "User or preferences not found"},
    },
)
async def get_preferences(
    x_user_id: str = Header(..., alias="X-User-ID"),
    session: AsyncSession = Depends(get_session),
) -> UserPreferencesResponse:
    """Get user preferences."""
    # Get preferences
    result = await session.execute(
        select(UserPreferences).where(UserPreferences.user_id == x_user_id)
    )
    preferences = result.scalar_one_or_none()

    if not preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": "Preferences not found"},
        )

    return UserPreferencesResponse.model_validate(preferences)


@router.put(
    "/user/preferences",
    response_model=UserPreferencesResponse,
    responses={
        404: {"model": ErrorResponse, "description": "User not found"},
    },
)
async def update_preferences(
    request: UpdatePreferencesRequest,
    x_user_id: str = Header(..., alias="X-User-ID"),
    session: AsyncSession = Depends(get_session),
) -> UserPreferencesResponse:
    """Update user preferences."""
    # Get preferences
    result = await session.execute(
        select(UserPreferences).where(UserPreferences.user_id == x_user_id)
    )
    preferences = result.scalar_one_or_none()

    if not preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": "Preferences not found"},
        )

    # Update only provided fields
    update_data = request.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            setattr(preferences, field, value)

    await session.flush()
    await session.refresh(preferences)

    return UserPreferencesResponse.model_validate(preferences)
