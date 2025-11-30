"""
Pydantic models for ChatKit messages and events.

Defines the data structures for:
- Message roles and statuses
- Event types for streaming
- Request/response payloads
"""

from enum import Enum
from uuid import UUID
from pydantic import BaseModel, Field


class MessageRole(str, Enum):
    """Role of the message sender."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class MessageStatus(str, Enum):
    """Status of message processing."""

    PENDING = "pending"
    STREAMING = "streaming"
    COMPLETE = "complete"
    ERROR = "error"


class EventType(str, Enum):
    """Type of streaming event."""

    TEXT_DELTA = "text_delta"
    MESSAGE_COMPLETE = "message_complete"
    ERROR = "error"


class MessageContent(BaseModel):
    """Message content with ID."""

    id: UUID
    content: str = Field(..., max_length=2000, description="Message text content")


class PageContext(BaseModel):
    """Context about the current page (optional)."""

    pageUrl: str | None = Field(None, description="Current page URL path")
    pageTitle: str | None = Field(None, description="Current page title")


class ChatRequest(BaseModel):
    """Request payload from frontend to backend."""

    type: str = Field(default="user_message", description="Request type")
    message: MessageContent
    context: PageContext | None = Field(None, description="Optional page context")


class ChatEvent(BaseModel):
    """Streaming event sent from backend to frontend."""

    type: EventType
    content: str | None = Field(None, description="Text content or error message")
    done: bool = Field(..., description="Whether stream is finished")
    messageId: UUID | None = Field(None, description="ID of the message being streamed")
