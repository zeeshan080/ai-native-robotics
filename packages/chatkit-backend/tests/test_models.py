"""
Tests for Pydantic models.
"""

import pytest
from uuid import uuid4
from pydantic import ValidationError

from chatkit_backend.models import (
    MessageRole,
    MessageStatus,
    EventType,
    MessageContent,
    PageContext,
    ChatRequest,
    ChatEvent,
)


def test_message_role_enum():
    """Test MessageRole enum values."""
    assert MessageRole.USER == "user"
    assert MessageRole.ASSISTANT == "assistant"
    assert MessageRole.SYSTEM == "system"


def test_event_type_enum():
    """Test EventType enum values."""
    assert EventType.TEXT_DELTA == "text_delta"
    assert EventType.MESSAGE_COMPLETE == "message_complete"
    assert EventType.ERROR == "error"


def test_message_content_valid():
    """Test valid MessageContent creation."""
    msg_id = uuid4()
    content = MessageContent(id=msg_id, content="What is ROS 2?")

    assert content.id == msg_id
    assert content.content == "What is ROS 2?"


def test_message_content_max_length():
    """Test MessageContent enforces max length."""
    msg_id = uuid4()
    long_content = "x" * 2001  # Over 2000 char limit

    with pytest.raises(ValidationError):
        MessageContent(id=msg_id, content=long_content)


def test_page_context_optional():
    """Test PageContext with optional fields."""
    # All fields optional
    context = PageContext()
    assert context.pageUrl is None
    assert context.pageTitle is None

    # With values
    context = PageContext(
        pageUrl="/docs/lesson",
        pageTitle="Lesson Title"
    )
    assert context.pageUrl == "/docs/lesson"
    assert context.pageTitle == "Lesson Title"


def test_chat_request_minimal():
    """Test minimal ChatRequest."""
    msg_id = uuid4()
    request = ChatRequest(
        message=MessageContent(id=msg_id, content="Hello")
    )

    assert request.type == "user_message"
    assert request.message.content == "Hello"
    assert request.context is None


def test_chat_request_with_context():
    """Test ChatRequest with page context."""
    msg_id = uuid4()
    request = ChatRequest(
        message=MessageContent(id=msg_id, content="Explain this"),
        context=PageContext(
            pageUrl="/docs/lesson",
            pageTitle="Lesson"
        )
    )

    assert request.message.content == "Explain this"
    assert request.context.pageUrl == "/docs/lesson"


def test_chat_event_text_delta():
    """Test ChatEvent for text streaming."""
    msg_id = uuid4()
    event = ChatEvent(
        type=EventType.TEXT_DELTA,
        content="Hello",
        done=False,
        messageId=msg_id
    )

    assert event.type == EventType.TEXT_DELTA
    assert event.content == "Hello"
    assert event.done is False
    assert event.messageId == msg_id


def test_chat_event_complete():
    """Test ChatEvent for completion."""
    msg_id = uuid4()
    event = ChatEvent(
        type=EventType.MESSAGE_COMPLETE,
        done=True,
        messageId=msg_id
    )

    assert event.type == EventType.MESSAGE_COMPLETE
    assert event.content is None
    assert event.done is True


def test_chat_event_error():
    """Test ChatEvent for errors."""
    msg_id = uuid4()
    event = ChatEvent(
        type=EventType.ERROR,
        content="Connection failed",
        done=True,
        messageId=msg_id
    )

    assert event.type == EventType.ERROR
    assert event.content == "Connection failed"
    assert event.done is True
