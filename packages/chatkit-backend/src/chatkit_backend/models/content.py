"""Pydantic schemas for content API endpoints."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


# =============================================================================
# Lesson Schemas
# =============================================================================


class LessonBase(BaseModel):
    """Base lesson schema."""
    number: int
    title: str
    slug: str
    type: str = Field(description="Lesson type: 'lesson', 'lab', 'summary', 'index'")


class LessonResponse(LessonBase):
    """Lesson response schema."""
    id: str
    chapter_id: str
    content_hash: Optional[str] = None
    bucket_path: Optional[str] = None
    vector_ids: Optional[list[str]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LessonSummary(LessonBase):
    """Lesson summary for list views."""
    id: str

    class Config:
        from_attributes = True


class LessonContentResponse(BaseModel):
    """Response for lesson content endpoint."""
    slug: str
    title: str
    content: str
    content_hash: str


# =============================================================================
# Chapter Schemas
# =============================================================================


class ChapterBase(BaseModel):
    """Base chapter schema."""
    number: int
    local_number: int
    title: str
    folder_name: str


class ChapterResponse(ChapterBase):
    """Chapter response schema."""
    id: str
    part_id: str
    prerequisites: Optional[list[str]] = None
    lessons: list[LessonSummary] = []
    created_at: datetime

    class Config:
        from_attributes = True


class ChapterSummary(ChapterBase):
    """Chapter summary for list views."""
    id: str
    lesson_count: int = 0

    class Config:
        from_attributes = True


# =============================================================================
# Part Schemas
# =============================================================================


class PartBase(BaseModel):
    """Base part schema."""
    number: int
    title: str
    layer: str
    tier: str
    folder_name: str
    week_start: int
    week_end: int


class PartResponse(PartBase):
    """Part response schema."""
    id: str
    book_id: str
    chapters: list[ChapterSummary] = []
    created_at: datetime

    class Config:
        from_attributes = True


class PartSummary(PartBase):
    """Part summary for list views."""
    id: str
    chapter_count: int = 0

    class Config:
        from_attributes = True


# =============================================================================
# Book Schemas
# =============================================================================


class BookBase(BaseModel):
    """Base book schema."""
    slug: str
    title: str
    description: Optional[str] = None
    version: str


class BookResponse(BookBase):
    """Book response schema."""
    id: str
    parts: list[PartSummary] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BookFullResponse(BookBase):
    """Full book response with complete hierarchy."""
    id: str
    parts: list[PartResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# =============================================================================
# Progress Schemas
# =============================================================================


class UserProgressBase(BaseModel):
    """Base user progress schema."""
    status: str = Field(description="Progress status: 'not_started', 'in_progress', 'completed'")


class UserProgressResponse(UserProgressBase):
    """User progress response schema."""
    id: str
    user_id: str
    lesson_id: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    time_spent_seconds: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProgressUpdateRequest(BaseModel):
    """Request to update progress."""
    status: Optional[str] = None
    time_spent_seconds: Optional[int] = None


class ProgressSummaryResponse(BaseModel):
    """Summary of user progress."""
    total_lessons: int
    completed_lessons: int
    in_progress_lessons: int
    total_time_spent_seconds: int
    completion_percentage: float
    parts_progress: dict[str, dict] = Field(default_factory=dict)


# =============================================================================
# Recommendation Schemas
# =============================================================================


class RecommendationResponse(BaseModel):
    """Lesson recommendation."""
    lesson: LessonSummary
    reason: str
    priority: int = Field(description="Lower is higher priority")
    chapter_title: str
    part_title: str


class RecommendationsResponse(BaseModel):
    """List of recommendations."""
    recommendations: list[RecommendationResponse]
    total: int
