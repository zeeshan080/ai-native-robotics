"""Content API endpoints for book structure."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from chatkit_backend.db import get_session, Book, Part, Chapter, Lesson
from chatkit_backend.models.content import (
    BookResponse,
    BookFullResponse,
    PartResponse,
    PartSummary,
    ChapterResponse,
    ChapterSummary,
    LessonResponse,
    LessonSummary,
    LessonContentResponse,
)

router = APIRouter(prefix="/content", tags=["Content"])


@router.get(
    "/book",
    response_model=BookFullResponse,
    responses={
        404: {"description": "Book not found"},
    },
)
async def get_book(
    session: AsyncSession = Depends(get_session),
) -> BookFullResponse:
    """Get the complete book structure with all parts, chapters, and lessons."""
    result = await session.execute(
        select(Book)
        .where(Book.slug == "ai-native-robotics")
        .options(
            selectinload(Book.parts)
            .selectinload(Part.chapters)
            .selectinload(Chapter.lessons)
        )
    )
    book = result.scalar_one_or_none()

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": "Book not found"},
        )

    # Build the response with full hierarchy
    parts_response = []
    for part in sorted(book.parts, key=lambda p: p.number):
        chapters_summary = []
        for chapter in sorted(part.chapters, key=lambda c: c.number):
            chapters_summary.append(
                ChapterSummary(
                    id=chapter.id,
                    number=chapter.number,
                    local_number=chapter.local_number,
                    title=chapter.title,
                    folder_name=chapter.folder_name,
                    lesson_count=len(chapter.lessons),
                )
            )
        parts_response.append(
            PartResponse(
                id=part.id,
                book_id=part.book_id,
                number=part.number,
                title=part.title,
                layer=part.layer,
                tier=part.tier,
                folder_name=part.folder_name,
                week_start=part.week_start,
                week_end=part.week_end,
                chapters=chapters_summary,
                created_at=part.created_at,
            )
        )

    return BookFullResponse(
        id=book.id,
        slug=book.slug,
        title=book.title,
        description=book.description,
        version=book.version,
        parts=parts_response,
        created_at=book.created_at,
        updated_at=book.updated_at,
    )


@router.get(
    "/parts",
    response_model=list[PartSummary],
)
async def list_parts(
    session: AsyncSession = Depends(get_session),
) -> list[PartSummary]:
    """List all parts with chapter counts."""
    result = await session.execute(
        select(Part)
        .options(selectinload(Part.chapters))
        .order_by(Part.number)
    )
    parts = result.scalars().all()

    return [
        PartSummary(
            id=part.id,
            number=part.number,
            title=part.title,
            layer=part.layer,
            tier=part.tier,
            folder_name=part.folder_name,
            week_start=part.week_start,
            week_end=part.week_end,
            chapter_count=len(part.chapters),
        )
        for part in parts
    ]


@router.get(
    "/parts/{number}",
    response_model=PartResponse,
    responses={
        404: {"description": "Part not found"},
    },
)
async def get_part(
    number: int,
    session: AsyncSession = Depends(get_session),
) -> PartResponse:
    """Get a specific part with its chapters."""
    result = await session.execute(
        select(Part)
        .where(Part.number == number)
        .options(
            selectinload(Part.chapters)
            .selectinload(Chapter.lessons)
        )
    )
    part = result.scalar_one_or_none()

    if not part:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": f"Part {number} not found"},
        )

    chapters_summary = []
    for chapter in sorted(part.chapters, key=lambda c: c.number):
        chapters_summary.append(
            ChapterSummary(
                id=chapter.id,
                number=chapter.number,
                local_number=chapter.local_number,
                title=chapter.title,
                folder_name=chapter.folder_name,
                lesson_count=len(chapter.lessons),
            )
        )

    return PartResponse(
        id=part.id,
        book_id=part.book_id,
        number=part.number,
        title=part.title,
        layer=part.layer,
        tier=part.tier,
        folder_name=part.folder_name,
        week_start=part.week_start,
        week_end=part.week_end,
        chapters=chapters_summary,
        created_at=part.created_at,
    )


@router.get(
    "/chapters/{number}",
    response_model=ChapterResponse,
    responses={
        404: {"description": "Chapter not found"},
    },
)
async def get_chapter(
    number: int,
    session: AsyncSession = Depends(get_session),
) -> ChapterResponse:
    """Get a specific chapter with its lessons."""
    result = await session.execute(
        select(Chapter)
        .where(Chapter.number == number)
        .options(selectinload(Chapter.lessons))
    )
    chapter = result.scalar_one_or_none()

    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": f"Chapter {number} not found"},
        )

    lessons_summary = [
        LessonSummary(
            id=lesson.id,
            number=lesson.number,
            title=lesson.title,
            slug=lesson.slug,
            type=lesson.type,
        )
        for lesson in sorted(chapter.lessons, key=lambda l: l.number)
    ]

    return ChapterResponse(
        id=chapter.id,
        part_id=chapter.part_id,
        number=chapter.number,
        local_number=chapter.local_number,
        title=chapter.title,
        folder_name=chapter.folder_name,
        prerequisites=chapter.prerequisites,
        lessons=lessons_summary,
        created_at=chapter.created_at,
    )


@router.get(
    "/lessons/{slug}",
    response_model=LessonResponse,
    responses={
        404: {"description": "Lesson not found"},
    },
)
async def get_lesson(
    slug: str,
    session: AsyncSession = Depends(get_session),
) -> LessonResponse:
    """Get a specific lesson by slug."""
    result = await session.execute(
        select(Lesson).where(Lesson.slug == slug)
    )
    lesson = result.scalar_one_or_none()

    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": f"Lesson '{slug}' not found"},
        )

    return LessonResponse.model_validate(lesson)


@router.get(
    "/lessons/{slug}/content",
    response_model=LessonContentResponse,
    responses={
        404: {"description": "Lesson not found or content not available"},
    },
)
async def get_lesson_content(
    slug: str,
    session: AsyncSession = Depends(get_session),
) -> LessonContentResponse:
    """Get lesson content from storage bucket.

    Note: This endpoint requires the MCP storage server to be running
    and the content to be synced to the bucket.
    """
    result = await session.execute(
        select(Lesson).where(Lesson.slug == slug)
    )
    lesson = result.scalar_one_or_none()

    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": f"Lesson '{slug}' not found"},
        )

    if not lesson.bucket_path or not lesson.content_hash:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "content_not_available",
                "message": "Lesson content has not been synced to storage yet",
            },
        )

    # TODO: Implement MCP storage client to fetch content
    # For now, return a placeholder response
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail={
            "error": "not_implemented",
            "message": "Storage integration pending. Content sync required.",
        },
    )
