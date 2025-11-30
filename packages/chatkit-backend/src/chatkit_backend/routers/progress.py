"""Progress tracking API endpoints."""

from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from chatkit_backend.db import get_session, User, Lesson, UserProgress, Part, Chapter
from chatkit_backend.models.content import (
    UserProgressResponse,
    ProgressUpdateRequest,
    ProgressSummaryResponse,
    RecommendationResponse,
    RecommendationsResponse,
    LessonSummary,
)

router = APIRouter(prefix="/progress", tags=["Progress"])


async def get_or_create_progress(
    session: AsyncSession, user_id: str, lesson_id: str
) -> UserProgress:
    """Get existing progress or create new entry."""
    result = await session.execute(
        select(UserProgress).where(
            UserProgress.user_id == user_id,
            UserProgress.lesson_id == lesson_id,
        )
    )
    progress = result.scalar_one_or_none()

    if not progress:
        progress = UserProgress(
            user_id=user_id,
            lesson_id=lesson_id,
            status="not_started",
        )
        session.add(progress)
        await session.flush()
        await session.refresh(progress)

    return progress


@router.get(
    "",
    response_model=ProgressSummaryResponse,
    responses={
        404: {"description": "User not found"},
    },
)
async def get_progress_summary(
    x_user_id: str = Header(..., alias="X-User-ID"),
    session: AsyncSession = Depends(get_session),
) -> ProgressSummaryResponse:
    """Get overall progress summary for user."""
    # Verify user exists
    user_result = await session.execute(select(User).where(User.id == x_user_id))
    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": "User not found"},
        )

    # Get total lessons count
    total_result = await session.execute(select(func.count(Lesson.id)))
    total_lessons = total_result.scalar() or 0

    # Get progress counts
    progress_result = await session.execute(
        select(UserProgress.status, func.count(UserProgress.id))
        .where(UserProgress.user_id == x_user_id)
        .group_by(UserProgress.status)
    )
    progress_counts = {status: count for status, count in progress_result.fetchall()}

    completed = progress_counts.get("completed", 0)
    in_progress = progress_counts.get("in_progress", 0)

    # Get total time spent
    time_result = await session.execute(
        select(func.sum(UserProgress.time_spent_seconds))
        .where(UserProgress.user_id == x_user_id)
    )
    total_time = time_result.scalar() or 0

    # Calculate per-part progress
    parts_progress = {}
    parts_result = await session.execute(
        select(Part)
        .options(
            selectinload(Part.chapters)
            .selectinload(Chapter.lessons)
        )
    )
    parts = parts_result.scalars().all()

    for part in parts:
        part_lesson_ids = []
        for chapter in part.chapters:
            for lesson in chapter.lessons:
                part_lesson_ids.append(lesson.id)

        if part_lesson_ids:
            part_progress_result = await session.execute(
                select(UserProgress.status, func.count(UserProgress.id))
                .where(
                    UserProgress.user_id == x_user_id,
                    UserProgress.lesson_id.in_(part_lesson_ids),
                )
                .group_by(UserProgress.status)
            )
            part_counts = {s: c for s, c in part_progress_result.fetchall()}

            parts_progress[f"part_{part.number}"] = {
                "title": part.title,
                "total": len(part_lesson_ids),
                "completed": part_counts.get("completed", 0),
                "in_progress": part_counts.get("in_progress", 0),
            }

    completion_percentage = (completed / total_lessons * 100) if total_lessons > 0 else 0.0

    return ProgressSummaryResponse(
        total_lessons=total_lessons,
        completed_lessons=completed,
        in_progress_lessons=in_progress,
        total_time_spent_seconds=total_time,
        completion_percentage=round(completion_percentage, 1),
        parts_progress=parts_progress,
    )


@router.get(
    "/lessons/{slug}",
    response_model=UserProgressResponse,
    responses={
        404: {"description": "Lesson not found"},
    },
)
async def get_lesson_progress(
    slug: str,
    x_user_id: str = Header(..., alias="X-User-ID"),
    session: AsyncSession = Depends(get_session),
) -> UserProgressResponse:
    """Get progress for a specific lesson."""
    # Get lesson
    lesson_result = await session.execute(
        select(Lesson).where(Lesson.slug == slug)
    )
    lesson = lesson_result.scalar_one_or_none()

    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": f"Lesson '{slug}' not found"},
        )

    progress = await get_or_create_progress(session, x_user_id, lesson.id)
    return UserProgressResponse.model_validate(progress)


@router.post(
    "/lessons/{slug}/start",
    response_model=UserProgressResponse,
    responses={
        404: {"description": "Lesson not found"},
    },
)
async def start_lesson(
    slug: str,
    x_user_id: str = Header(..., alias="X-User-ID"),
    session: AsyncSession = Depends(get_session),
) -> UserProgressResponse:
    """Mark a lesson as started."""
    # Get lesson
    lesson_result = await session.execute(
        select(Lesson).where(Lesson.slug == slug)
    )
    lesson = lesson_result.scalar_one_or_none()

    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": f"Lesson '{slug}' not found"},
        )

    progress = await get_or_create_progress(session, x_user_id, lesson.id)

    if progress.status == "not_started":
        progress.status = "in_progress"
        progress.started_at = datetime.now(timezone.utc)
        await session.flush()
        await session.refresh(progress)

    return UserProgressResponse.model_validate(progress)


@router.post(
    "/lessons/{slug}/complete",
    response_model=UserProgressResponse,
    responses={
        404: {"description": "Lesson not found"},
    },
)
async def complete_lesson(
    slug: str,
    x_user_id: str = Header(..., alias="X-User-ID"),
    session: AsyncSession = Depends(get_session),
) -> UserProgressResponse:
    """Mark a lesson as completed."""
    # Get lesson
    lesson_result = await session.execute(
        select(Lesson).where(Lesson.slug == slug)
    )
    lesson = lesson_result.scalar_one_or_none()

    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": f"Lesson '{slug}' not found"},
        )

    progress = await get_or_create_progress(session, x_user_id, lesson.id)

    now = datetime.now(timezone.utc)
    if progress.status != "completed":
        progress.status = "completed"
        progress.completed_at = now
        if not progress.started_at:
            progress.started_at = now
        await session.flush()
        await session.refresh(progress)

    return UserProgressResponse.model_validate(progress)


@router.put(
    "/lessons/{slug}/time",
    response_model=UserProgressResponse,
    responses={
        404: {"description": "Lesson not found"},
    },
)
async def update_time_spent(
    slug: str,
    request: ProgressUpdateRequest,
    x_user_id: str = Header(..., alias="X-User-ID"),
    session: AsyncSession = Depends(get_session),
) -> UserProgressResponse:
    """Update time spent on a lesson."""
    # Get lesson
    lesson_result = await session.execute(
        select(Lesson).where(Lesson.slug == slug)
    )
    lesson = lesson_result.scalar_one_or_none()

    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": f"Lesson '{slug}' not found"},
        )

    progress = await get_or_create_progress(session, x_user_id, lesson.id)

    if request.time_spent_seconds is not None:
        progress.time_spent_seconds = request.time_spent_seconds
        await session.flush()
        await session.refresh(progress)

    return UserProgressResponse.model_validate(progress)


@router.get(
    "/recommendations",
    response_model=RecommendationsResponse,
    responses={
        404: {"description": "User not found"},
    },
)
async def get_recommendations(
    x_user_id: str = Header(..., alias="X-User-ID"),
    limit: int = 5,
    session: AsyncSession = Depends(get_session),
) -> RecommendationsResponse:
    """Get personalized lesson recommendations.

    Algorithm:
    1. Get user's completed lessons
    2. Find next sequential lessons in incomplete chapters
    3. Check prerequisites (completed chapters required)
    4. Factor in pedagogy layer progression (L1→L2→L3)
    5. Score and rank candidates
    6. Return top N with reasons
    """
    # Verify user exists
    user_result = await session.execute(select(User).where(User.id == x_user_id))
    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": "User not found"},
        )

    # Get user's completed lesson IDs
    completed_result = await session.execute(
        select(UserProgress.lesson_id)
        .where(
            UserProgress.user_id == x_user_id,
            UserProgress.status == "completed",
        )
    )
    completed_lesson_ids = set(row[0] for row in completed_result.fetchall())

    # Get all lessons with their chapter and part info
    lessons_result = await session.execute(
        select(Lesson)
        .options(
            selectinload(Lesson.chapter)
            .selectinload(Chapter.part)
        )
        .order_by(Lesson.chapter_id, Lesson.number)
    )
    all_lessons = lessons_result.scalars().all()

    # Get completed chapters (all lessons in chapter completed)
    chapters_result = await session.execute(
        select(Chapter).options(selectinload(Chapter.lessons))
    )
    chapters = chapters_result.scalars().all()

    completed_chapter_ids = set()
    for chapter in chapters:
        chapter_lesson_ids = {lesson.id for lesson in chapter.lessons}
        if chapter_lesson_ids and chapter_lesson_ids.issubset(completed_lesson_ids):
            completed_chapter_ids.add(chapter.id)

    # Score and rank recommendations
    recommendations = []

    for lesson in all_lessons:
        if lesson.id in completed_lesson_ids:
            continue  # Skip completed lessons

        chapter = lesson.chapter
        part = chapter.part

        # Check prerequisites
        prereqs = chapter.prerequisites or []
        if prereqs and not all(p in completed_chapter_ids for p in prereqs):
            continue  # Prerequisites not met

        # Calculate priority score (lower is better)
        priority = 0

        # Prefer earlier parts/chapters
        priority += part.number * 10
        priority += chapter.local_number

        # Prefer lessons in chapters where user has started
        chapter_lesson_ids = {l.id for l in chapter.lessons}
        if chapter_lesson_ids & completed_lesson_ids:
            priority -= 5  # Boost lessons in started chapters

        # Prefer first uncompleted lesson in a chapter
        chapter_lessons_sorted = sorted(chapter.lessons, key=lambda l: l.number)
        for i, ch_lesson in enumerate(chapter_lessons_sorted):
            if ch_lesson.id not in completed_lesson_ids:
                if ch_lesson.id == lesson.id and i == 0:
                    priority -= 3  # First uncompleted in chapter
                break

        # Generate reason
        if not completed_lesson_ids:
            reason = "Start your learning journey here"
        elif chapter_lesson_ids & completed_lesson_ids:
            reason = f"Continue in {chapter.title}"
        else:
            reason = f"Begin {chapter.title} in {part.title}"

        recommendations.append(
            RecommendationResponse(
                lesson=LessonSummary(
                    id=lesson.id,
                    number=lesson.number,
                    title=lesson.title,
                    slug=lesson.slug,
                    type=lesson.type,
                ),
                reason=reason,
                priority=priority,
                chapter_title=chapter.title,
                part_title=part.title,
            )
        )

    # Sort by priority and limit
    recommendations.sort(key=lambda r: r.priority)
    recommendations = recommendations[:limit]

    return RecommendationsResponse(
        recommendations=recommendations,
        total=len(recommendations),
    )
