"""
Models package for ChatKit backend.

Exports all Pydantic models and enums for message handling.
"""

from .messages import (
    MessageRole,
    MessageStatus,
    EventType,
    Reference,
    MessageContent,
    HistoryMessage,
    PageContext,
    ChatRequest,
    ChatEvent,
)
from .thread import (
    CreateThreadRequest,
    AddMessageRequest,
    UpdateThreadRequest,
    ThreadItemResponse,
    ThreadResponse,
    ThreadListResponse,
    MessageListResponse,
)

__all__ = [
    "MessageRole",
    "MessageStatus",
    "EventType",
    "Reference",
    "MessageContent",
    "HistoryMessage",
    "PageContext",
    "ChatRequest",
    "ChatEvent",
    # Thread models
    "CreateThreadRequest",
    "AddMessageRequest",
    "UpdateThreadRequest",
    "ThreadItemResponse",
    "ThreadResponse",
    "ThreadListResponse",
    "MessageListResponse",
]
