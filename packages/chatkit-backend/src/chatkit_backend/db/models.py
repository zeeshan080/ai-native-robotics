"""SQLAlchemy models for content personalization and book structure."""

from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


class User(Base):
    """User model for anonymous user tracking."""

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    onboarding_completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    # Relationships
    preferences: Mapped[Optional["UserPreferences"]] = relationship(
        "UserPreferences",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    cache_entries: Mapped[list["PersonalizedContentCache"]] = relationship(
        "PersonalizedContentCache",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    progress_entries: Mapped[list["UserProgress"]] = relationship(
        "UserProgress",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    # Note: chat_threads relationship removed since BetterAuth users are external

    def __repr__(self) -> str:
        return f"<User(id={self.id}, onboarding_completed={self.onboarding_completed})>"


class UserPreferences(Base):
    """User preferences from onboarding questionnaire."""

    __tablename__ = "user_preferences"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
    )

    # Question responses
    education_level: Mapped[str] = mapped_column(String(50))
    programming_experience: Mapped[str] = mapped_column(String(50))
    robotics_background: Mapped[bool] = mapped_column(Boolean)
    ai_ml_experience: Mapped[str] = mapped_column(String(50))
    learning_goals: Mapped[list[str]] = mapped_column(ARRAY(String))
    preferred_language: Mapped[str] = mapped_column(String(10), default="en")

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="preferences")

    def __repr__(self) -> str:
        return f"<UserPreferences(user_id={self.user_id}, language={self.preferred_language})>"


class PersonalizedContentCache(Base):
    """Cache for personalized lesson content."""

    __tablename__ = "personalized_content_cache"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    lesson_slug: Mapped[str] = mapped_column(String(255), index=True)
    content_hash: Mapped[str] = mapped_column(String(16))
    preferences_hash: Mapped[str] = mapped_column(String(16))
    personalized_content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="cache_entries")

    def __repr__(self) -> str:
        return f"<PersonalizedContentCache(user_id={self.user_id}, lesson={self.lesson_slug})>"


# =============================================================================
# Book Structure Models
# =============================================================================


class Book(Base):
    """Book model representing the textbook."""

    __tablename__ = "books"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    version: Mapped[str] = mapped_column(String(20), default="1.0.0")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    parts: Mapped[list["Part"]] = relationship(
        "Part",
        back_populates="book",
        cascade="all, delete-orphan",
        order_by="Part.number",
    )

    def __repr__(self) -> str:
        return f"<Book(slug={self.slug}, title={self.title})>"


class Part(Base):
    """Part model representing a major section of the book."""

    __tablename__ = "parts"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    book_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("books.id", ondelete="CASCADE"),
    )
    number: Mapped[int] = mapped_column(Integer)  # 1-6
    title: Mapped[str] = mapped_column(String(255))
    layer: Mapped[str] = mapped_column(String(10))  # L1, L2, L3, L4, L5
    tier: Mapped[str] = mapped_column(String(20))  # A2, B1, B2, C1, C2
    folder_name: Mapped[str] = mapped_column(String(100))
    week_start: Mapped[int] = mapped_column(Integer)
    week_end: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    # Relationships
    book: Mapped["Book"] = relationship("Book", back_populates="parts")
    chapters: Mapped[list["Chapter"]] = relationship(
        "Chapter",
        back_populates="part",
        cascade="all, delete-orphan",
        order_by="Chapter.number",
    )

    def __repr__(self) -> str:
        return f"<Part(number={self.number}, title={self.title})>"


class Chapter(Base):
    """Chapter model representing a chapter within a part."""

    __tablename__ = "chapters"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    part_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("parts.id", ondelete="CASCADE"),
    )
    number: Mapped[int] = mapped_column(Integer)  # Global chapter number (1-18)
    local_number: Mapped[int] = mapped_column(Integer)  # Number within part
    title: Mapped[str] = mapped_column(String(255))
    folder_name: Mapped[str] = mapped_column(String(100))
    prerequisites: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)  # Array of chapter IDs
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    # Relationships
    part: Mapped["Part"] = relationship("Part", back_populates="chapters")
    lessons: Mapped[list["Lesson"]] = relationship(
        "Lesson",
        back_populates="chapter",
        cascade="all, delete-orphan",
        order_by="Lesson.number",
    )

    def __repr__(self) -> str:
        return f"<Chapter(number={self.number}, title={self.title})>"


class Lesson(Base):
    """Lesson model representing individual content items."""

    __tablename__ = "lessons"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    chapter_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("chapters.id", ondelete="CASCADE"),
    )
    number: Mapped[int] = mapped_column(Integer)  # Lesson number in chapter
    title: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    type: Mapped[str] = mapped_column(String(20))  # 'lesson', 'lab', 'summary', 'index'
    content_hash: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)  # SHA-256
    bucket_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    vector_ids: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)  # Array of vector DB IDs
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    chapter: Mapped["Chapter"] = relationship("Chapter", back_populates="lessons")
    progress_entries: Mapped[list["UserProgress"]] = relationship(
        "UserProgress",
        back_populates="lesson",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Lesson(slug={self.slug}, title={self.title})>"


# =============================================================================
# Progress Tracking Models
# =============================================================================


class UserProgress(Base):
    """User progress tracking for lessons."""

    __tablename__ = "user_progress"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    lesson_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("lessons.id", ondelete="CASCADE"),
    )
    status: Mapped[str] = mapped_column(
        String(20),
        default="not_started",
    )  # 'not_started', 'in_progress', 'completed'
    started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    time_spent_seconds: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="progress_entries")
    lesson: Mapped["Lesson"] = relationship("Lesson", back_populates="progress_entries")

    def __repr__(self) -> str:
        return f"<UserProgress(user_id={self.user_id}, lesson_id={self.lesson_id}, status={self.status})>"


# =============================================================================
# Anonymous Rate Limiting
# =============================================================================


class AnonymousRateLimit(Base):
    """Rate limiting for anonymous (unauthenticated) users.

    Tracks message count by IP address to enforce the 10-message trial limit.
    This prevents users from bypassing the limit by clearing localStorage.
    """

    __tablename__ = "anonymous_rate_limits"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    ip_address: Mapped[str] = mapped_column(
        String(45),  # IPv6 max length
        unique=True,
        index=True,
    )
    message_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )
    first_message_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    last_message_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self) -> str:
        return f"<AnonymousRateLimit(ip={self.ip_address}, count={self.message_count})>"


# =============================================================================
# Chat Thread Models (Session Management)
# =============================================================================


class ChatThread(Base):
    """Chat thread model for storing conversation sessions.

    Each thread represents a conversation between a user and the AI tutor.
    Threads can have a title (auto-generated or user-defined) and store
    metadata like the previous_response_id for conversation continuity.

    Note: user_id is a String (not UUID) to support both:
    - Anonymous users with UUID strings from our system
    - BetterAuth users with non-UUID strings like '0Dl6dRx1wnFPoz4A68X9mYMmsLBhBP2T'
    """

    __tablename__ = "chat_threads"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    # String type to accept both UUIDs and BetterAuth IDs (no FK since BetterAuth users are external)
    user_id: Mapped[str] = mapped_column(
        String(255),
        index=True,
    )
    title: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    thread_metadata: Mapped[Optional[dict]] = mapped_column(
        "metadata",  # Database column name stays 'metadata'
        JSONB,
        nullable=True,
        default=dict,
    )  # Stores previous_response_id, context, etc.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships (no user relationship since user_id can be external BetterAuth ID)
    items: Mapped[list["ChatThreadItem"]] = relationship(
        "ChatThreadItem",
        back_populates="thread",
        cascade="all, delete-orphan",
        order_by="ChatThreadItem.created_at",
    )

    def __repr__(self) -> str:
        return f"<ChatThread(id={self.id}, user_id={self.user_id}, title={self.title})>"


class ChatThreadItem(Base):
    """Chat thread item model for storing individual messages.

    Each item represents a single message in a conversation thread,
    storing the role (user/assistant), content, and associated metadata.
    """

    __tablename__ = "chat_thread_items"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    thread_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("chat_threads.id", ondelete="CASCADE"),
        index=True,
    )
    role: Mapped[str] = mapped_column(
        String(20),
    )  # 'user', 'assistant', 'system'
    content: Mapped[str] = mapped_column(
        Text,
    )
    item_metadata: Mapped[Optional[dict]] = mapped_column(
        "metadata",  # Database column name stays 'metadata'
        JSONB,
        nullable=True,
        default=dict,
    )  # Stores message_id, context, timestamps, etc.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    # Relationships
    thread: Mapped["ChatThread"] = relationship("ChatThread", back_populates="items")

    def __repr__(self) -> str:
        return f"<ChatThreadItem(id={self.id}, thread_id={self.thread_id}, role={self.role})>"
