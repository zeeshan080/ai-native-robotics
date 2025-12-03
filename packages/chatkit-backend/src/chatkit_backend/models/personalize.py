"""Pydantic schemas for personalization endpoints."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class PersonalizeRequest(BaseModel):
    """Request body for content personalization."""
    lesson_slug: str = Field(
        ...,
        description="Lesson identifier (e.g., '01-intro/embodiment')",
        examples=["01-what-is-physical-ai/embodiment-hypothesis"]
    )
    original_content: str = Field(
        ...,
        description="Original lesson content in Markdown format"
    )


class PersonalizeResponse(BaseModel):
    """Response body for personalized content."""
    personalized_content: str = Field(
        ...,
        description="Personalized lesson content in Markdown format"
    )
    cached: bool = Field(
        ...,
        description="Whether the content was served from cache"
    )
    generated_at: datetime = Field(
        ...,
        description="When the personalized content was generated"
    )


class CacheDeleteResponse(BaseModel):
    """Response for cache deletion."""
    deleted_count: int = Field(
        ...,
        description="Number of cache entries deleted"
    )
