"""Pydantic schemas for thread and message endpoints."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class CreateThreadRequest(BaseModel):
    """Request body for creating a new thread."""
    user_id: str = Field(..., description="User ID who owns the thread")
    title: Optional[str] = Field(None, description="Optional thread title")
    metadata: Optional[dict] = Field(None, description="Optional metadata")


class AddMessageRequest(BaseModel):
    """Request body for adding a message to a thread."""
    role: str = Field(
        ...,
        description="Message role",
        pattern="^(user|assistant|system)$"
    )
    content: str = Field(..., description="Message content", min_length=1)
    metadata: Optional[dict] = Field(None, description="Optional metadata")


class UpdateThreadRequest(BaseModel):
    """Request body for updating a thread."""
    title: Optional[str] = Field(None, description="New thread title")
    metadata: Optional[dict] = Field(None, description="New metadata")


class ThreadItemResponse(BaseModel):
    """Response body for a thread message/item."""
    id: str
    thread_id: str
    role: str
    content: str
    metadata: dict = Field(default_factory=dict)
    created_at: datetime

    class Config:
        from_attributes = True


class ThreadResponse(BaseModel):
    """Response body for a thread."""
    id: str
    user_id: str
    title: Optional[str] = None
    metadata: dict = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime
    items: list[ThreadItemResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True


class ThreadListResponse(BaseModel):
    """Response body for listing threads with pagination."""
    threads: list[ThreadResponse]
    next_cursor: Optional[str] = None


class MessageListResponse(BaseModel):
    """Response body for listing messages with pagination."""
    messages: list[ThreadItemResponse]
    next_cursor: Optional[str] = None
