"""Base Store interface for ChatKit thread persistence.

This module defines the abstract base class for thread storage,
following the ChatKit Store pattern from the OpenAI SDK.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import uuid4


@dataclass
class ThreadItem:
    """Represents a single message in a thread.

    Attributes:
        id: Unique identifier for the message
        thread_id: ID of the parent thread
        role: Message role ('user', 'assistant', 'system')
        content: Message text content
        metadata: Optional metadata dict (message_id, context, etc.)
        created_at: Timestamp when the message was created
    """

    id: str
    thread_id: str
    role: str
    content: str
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)

    @classmethod
    def create(
        cls,
        thread_id: str,
        role: str,
        content: str,
        metadata: Optional[dict] = None,
    ) -> "ThreadItem":
        """Factory method to create a new ThreadItem."""
        return cls(
            id=str(uuid4()),
            thread_id=thread_id,
            role=role,
            content=content,
            metadata=metadata or {},
            created_at=datetime.utcnow(),
        )


@dataclass
class Thread:
    """Represents a conversation thread.

    Attributes:
        id: Unique identifier for the thread
        user_id: ID of the user who owns the thread
        title: Optional title for the thread
        metadata: Optional metadata dict (previous_response_id, context, etc.)
        created_at: Timestamp when the thread was created
        updated_at: Timestamp when the thread was last updated
        items: List of messages in the thread (loaded separately)
    """

    id: str
    user_id: str
    title: Optional[str] = None
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    items: list[ThreadItem] = field(default_factory=list)

    @classmethod
    def create(
        cls,
        user_id: str,
        title: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> "Thread":
        """Factory method to create a new Thread."""
        now = datetime.utcnow()
        return cls(
            id=str(uuid4()),
            user_id=user_id,
            title=title,
            metadata=metadata or {},
            created_at=now,
            updated_at=now,
            items=[],
        )


class Store(ABC):
    """Abstract base class for thread storage.

    This interface defines the contract for storing and retrieving
    conversation threads and their messages. Implementations can use
    different backends (in-memory, PostgreSQL, etc.).
    """

    # =========================================================================
    # Thread Operations
    # =========================================================================

    @abstractmethod
    async def create_thread(
        self,
        user_id: str,
        title: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> Thread:
        """Create a new thread for a user.

        Args:
            user_id: The ID of the user creating the thread
            title: Optional title for the thread
            metadata: Optional metadata dict

        Returns:
            The created Thread object
        """
        pass

    @abstractmethod
    async def get_thread(self, thread_id: str) -> Optional[Thread]:
        """Get a thread by ID.

        Args:
            thread_id: The ID of the thread to retrieve

        Returns:
            The Thread object if found, None otherwise
        """
        pass

    @abstractmethod
    async def update_thread(
        self,
        thread_id: str,
        title: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> Optional[Thread]:
        """Update a thread's title or metadata.

        Args:
            thread_id: The ID of the thread to update
            title: New title (if provided)
            metadata: New metadata (if provided, replaces existing)

        Returns:
            The updated Thread object if found, None otherwise
        """
        pass

    @abstractmethod
    async def delete_thread(self, thread_id: str) -> bool:
        """Delete a thread and all its items.

        Args:
            thread_id: The ID of the thread to delete

        Returns:
            True if deleted, False if not found
        """
        pass

    @abstractmethod
    async def list_threads(
        self,
        user_id: str,
        limit: int = 20,
        cursor: Optional[str] = None,
    ) -> tuple[list[Thread], Optional[str]]:
        """List threads for a user with pagination.

        Args:
            user_id: The ID of the user
            limit: Maximum number of threads to return
            cursor: Pagination cursor (thread ID to start after)

        Returns:
            Tuple of (list of threads, next cursor or None)
        """
        pass

    # =========================================================================
    # Thread Item Operations
    # =========================================================================

    @abstractmethod
    async def add_item(
        self,
        thread_id: str,
        role: str,
        content: str,
        metadata: Optional[dict] = None,
    ) -> ThreadItem:
        """Add a message to a thread.

        Args:
            thread_id: The ID of the thread
            role: Message role ('user', 'assistant', 'system')
            content: Message text content
            metadata: Optional metadata dict

        Returns:
            The created ThreadItem object
        """
        pass

    @abstractmethod
    async def get_items(
        self,
        thread_id: str,
        limit: int = 50,
        cursor: Optional[str] = None,
    ) -> tuple[list[ThreadItem], Optional[str]]:
        """Get messages for a thread with pagination.

        Args:
            thread_id: The ID of the thread
            limit: Maximum number of items to return
            cursor: Pagination cursor (item ID to start after)

        Returns:
            Tuple of (list of items, next cursor or None)
        """
        pass

    @abstractmethod
    async def load_thread_with_items(
        self,
        thread_id: str,
        item_limit: int = 50,
    ) -> Optional[Thread]:
        """Load a thread with its messages.

        Convenience method that loads a thread and its items in one call.

        Args:
            thread_id: The ID of the thread
            item_limit: Maximum number of items to load

        Returns:
            The Thread object with items loaded, None if not found
        """
        pass
