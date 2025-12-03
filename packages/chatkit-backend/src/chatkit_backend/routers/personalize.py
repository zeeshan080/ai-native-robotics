"""Content personalization API endpoints."""

import hashlib
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from chatkit_backend.db import get_session, User, UserPreferences, PersonalizedContentCache
from chatkit_backend.models.personalize import (
    PersonalizeRequest,
    PersonalizeResponse,
    CacheDeleteResponse,
)
from chatkit_backend.agents.personalizer import personalize_content

router = APIRouter(prefix="/personalize", tags=["Personalization"])


def compute_content_hash(content: str) -> str:
    """Compute a hash of the original content for cache invalidation."""
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def compute_preferences_hash(preferences: UserPreferences) -> str:
    """Compute a hash of relevant preferences for cache invalidation."""
    key = (
        f"{preferences.education_level}:"
        f"{preferences.programming_experience}:"
        f"{preferences.robotics_background}:"
        f"{preferences.ai_ml_experience}:"
        f"{','.join(sorted(preferences.learning_goals))}:"
        f"{preferences.preferred_language}"
    )
    return hashlib.sha256(key.encode()).hexdigest()[:16]


@router.post(
    "",
    response_model=PersonalizeResponse,
    responses={
        404: {"description": "User not found or onboarding not completed"},
        500: {"description": "Personalization generation failed"},
    },
)
async def generate_personalized_content(
    request: PersonalizeRequest,
    x_user_id: str = Header(..., alias="X-User-ID"),
    session: AsyncSession = Depends(get_session),
) -> PersonalizeResponse:
    """Generate personalized content for a lesson.

    If cached content exists with matching hashes, returns cached version.
    Otherwise generates new personalized content and caches it.
    """
    # Get user and verify onboarding completed
    user_result = await session.execute(select(User).where(User.id == x_user_id))
    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": "User not found"},
        )

    if not user.onboarding_completed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": "Onboarding not completed"},
        )

    # Get user preferences
    prefs_result = await session.execute(
        select(UserPreferences).where(UserPreferences.user_id == x_user_id)
    )
    preferences = prefs_result.scalar_one_or_none()

    if not preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": "User preferences not found"},
        )

    # Compute hashes for cache lookup
    content_hash = compute_content_hash(request.original_content)
    preferences_hash = compute_preferences_hash(preferences)

    # Check cache
    cache_result = await session.execute(
        select(PersonalizedContentCache).where(
            PersonalizedContentCache.user_id == x_user_id,
            PersonalizedContentCache.lesson_slug == request.lesson_slug,
            PersonalizedContentCache.content_hash == content_hash,
            PersonalizedContentCache.preferences_hash == preferences_hash,
        )
    )
    cached = cache_result.scalar_one_or_none()

    if cached:
        # Return cached content
        return PersonalizeResponse(
            personalized_content=cached.personalized_content,
            cached=True,
            generated_at=cached.created_at,
        )

    # Generate new personalized content
    try:
        personalized = await personalize_content(preferences, request.original_content)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "generation_failed", "message": str(e)},
        )

    # Store in cache
    now = datetime.now(timezone.utc)
    cache_entry = PersonalizedContentCache(
        user_id=x_user_id,
        lesson_slug=request.lesson_slug,
        content_hash=content_hash,
        preferences_hash=preferences_hash,
        personalized_content=personalized,
    )
    session.add(cache_entry)
    await session.flush()

    return PersonalizeResponse(
        personalized_content=personalized,
        cached=False,
        generated_at=now,
    )


@router.delete(
    "/cache",
    response_model=CacheDeleteResponse,
    responses={
        404: {"description": "User not found"},
    },
)
async def clear_cache(
    x_user_id: str = Header(..., alias="X-User-ID"),
    session: AsyncSession = Depends(get_session),
) -> CacheDeleteResponse:
    """Clear personalization cache for user.

    Called when user updates their preferences to ensure
    fresh personalized content is generated.
    """
    # Verify user exists
    user_result = await session.execute(select(User).where(User.id == x_user_id))
    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": "User not found"},
        )

    # Delete all cache entries for user
    result = await session.execute(
        delete(PersonalizedContentCache).where(
            PersonalizedContentCache.user_id == x_user_id
        )
    )

    return CacheDeleteResponse(deleted_count=result.rowcount)
