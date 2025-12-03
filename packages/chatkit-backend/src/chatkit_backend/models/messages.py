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
    REFERENCES = "references"
    ERROR = "error"


class Reference(BaseModel):
    """A reference to textbook content."""

    title: str
    url: str
    location: str | None = None
    content_type: str | None = None
    score: float | None = None


class MessageContent(BaseModel):
    """Message content with ID."""

    id: UUID
    content: str = Field(..., max_length=2000, description="Message text content")


class HistoryMessage(BaseModel):
    """A message in the conversation history."""

    role: MessageRole
    content: str = Field(..., description="Message text content")


class PageContext(BaseModel):
    """Context about the current page and user (optional)."""

    pageUrl: str | None = Field(None, description="Current page URL path")
    pageTitle: str | None = Field(None, description="Current page title")
    userName: str | None = Field(None, description="User's name for personalization")
    user_id: str | None = Field(None, description="Authenticated user ID from BetterAuth")


class ChatRequest(BaseModel):
    """Request payload from frontend to backend."""

    type: str = Field(default="user_message", description="Request type")
    message: MessageContent
    history: list[HistoryMessage] = Field(default_factory=list, description="Conversation history")
    context: PageContext | None = Field(None, description="Optional page context")


class ChatEvent(BaseModel):
    """Streaming event sent from backend to frontend."""

    type: EventType
    content: str | None = Field(None, description="Text content or error message")
    done: bool = Field(..., description="Whether stream is finished")
    messageId: UUID | None = Field(None, description="ID of the message being streamed")
    references: list[Reference] | None = Field(None, description="References to textbook content")
