"""ThreadService for managing chat conversation threads.

This service provides business logic for thread operations, including
auto-generating titles from first messages and coordinating with stores.
"""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.models import User
from ..stores import Store, Thread, ThreadItem


class ThreadService:
    """Service for managing chat threads and messages.

    This service wraps a Store implementation and provides additional
    business logic such as:
    - Auto-generating thread titles from first messages
    - Validating user ownership of threads
    - Coordinating thread and message operations

    Usage:
        store = PostgresStore(session)
        service = ThreadService(store)

        # Create a thread
        thread = await service.create_thread(user_id="user-123")

        # Add a message (auto-generates title on first user message)
        item = await service.add_message(
            thread_id=thread.id,
            user_id="user-123",
            role="user",
            content="What is Physical AI?"
        )
    """

    # Maximum length for auto-generated titles
    MAX_TITLE_LENGTH = 50

    def __init__(self, store: Store):
        """Initialize the ThreadService.

        Args:
            store: Store implementation for persistence
        """
        self._store = store

    # =========================================================================
    # Thread Operations
    # =========================================================================

    async def create_thread(
        self,
        user_id: str,
        title: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> Thread:
        """Create a new thread for a user.

        Args:
            user_id: The ID of the user creating the thread
            title: Optional title (if not provided, will be auto-generated)
            metadata: Optional metadata dict

        Returns:
            The created Thread object
        """
        return await self._store.create_thread(
            user_id=user_id,
            title=title,
            metadata=metadata,
        )

    async def get_thread(
        self,
        thread_id: str,
        user_id: Optional[str] = None,
    ) -> Optional[Thread]:
        """Get a thread by ID, optionally validating ownership.

        Args:
            thread_id: The ID of the thread to retrieve
            user_id: If provided, validates that the thread belongs to this user

        Returns:
            The Thread object if found and authorized, None otherwise
        """
        thread = await self._store.get_thread(thread_id)

        if not thread:
            return None

        # Validate ownership if user_id provided
        if user_id and thread.user_id != user_id:
            return None

        return thread

    async def get_thread_with_messages(
        self,
        thread_id: str,
        user_id: Optional[str] = None,
        message_limit: int = 50,
    ) -> Optional[Thread]:
        """Get a thread with its messages.

        Args:
            thread_id: The ID of the thread
            user_id: If provided, validates ownership
            message_limit: Maximum number of messages to load

        Returns:
            Thread with messages loaded, None if not found/unauthorized
        """
        thread = await self._store.load_thread_with_items(
            thread_id=thread_id,
            item_limit=message_limit,
        )

        if not thread:
            return None

        # Validate ownership if user_id provided
        if user_id and thread.user_id != user_id:
            return None

        return thread

    async def update_thread(
        self,
        thread_id: str,
        user_id: str,
        title: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> Optional[Thread]:
        """Update a thread's title or metadata.

        Args:
            thread_id: The ID of the thread to update
            user_id: The ID of the user (for ownership validation)
            title: New title (if provided)
            metadata: New metadata (if provided)

        Returns:
            Updated Thread if successful, None if not found/unauthorized
        """
        # First verify ownership
        thread = await self.get_thread(thread_id, user_id)
        if not thread:
            return None

        return await self._store.update_thread(
            thread_id=thread_id,
            title=title,
            metadata=metadata,
        )

    async def delete_thread(
        self,
        thread_id: str,
        user_id: str,
    ) -> bool:
        """Delete a thread and all its messages.

        Args:
            thread_id: The ID of the thread to delete
            user_id: The ID of the user (for ownership validation)

        Returns:
            True if deleted, False if not found/unauthorized
        """
        # First verify ownership
        thread = await self.get_thread(thread_id, user_id)
        if not thread:
            return False

        return await self._store.delete_thread(thread_id)

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
            cursor: Pagination cursor

        Returns:
            Tuple of (list of threads, next cursor or None)
        """
        return await self._store.list_threads(
            user_id=user_id,
            limit=limit,
            cursor=cursor,
        )

    # =========================================================================
    # Message Operations
    # =========================================================================

    async def add_message(
        self,
        thread_id: str,
        user_id: str,
        role: str,
        content: str,
        metadata: Optional[dict] = None,
        auto_title: bool = True,
    ) -> Optional[ThreadItem]:
        """Add a message to a thread.

        If this is the first user message and auto_title is True,
        automatically generates a title from the message content.

        Args:
            thread_id: The ID of the thread
            user_id: The ID of the user (for ownership validation)
            role: Message role ('user', 'assistant', 'system')
            content: Message text content
            metadata: Optional metadata dict
            auto_title: Whether to auto-generate title from first user message

        Returns:
            The created ThreadItem, None if thread not found/unauthorized
        """
        # Verify ownership
        thread = await self.get_thread(thread_id, user_id)
        if not thread:
            return None

        # Add the message
        item = await self._store.add_item(
            thread_id=thread_id,
            role=role,
            content=content,
            metadata=metadata,
        )

        # Auto-generate title if needed
        if auto_title and role == "user" and not thread.title:
            title = self._generate_title(content)
            await self._store.update_thread(thread_id=thread_id, title=title)

        return item

    async def get_messages(
        self,
        thread_id: str,
        user_id: str,
        limit: int = 50,
        cursor: Optional[str] = None,
    ) -> Optional[tuple[list[ThreadItem], Optional[str]]]:
        """Get messages for a thread with pagination.

        Args:
            thread_id: The ID of the thread
            user_id: The ID of the user (for ownership validation)
            limit: Maximum number of messages to return
            cursor: Pagination cursor

        Returns:
            Tuple of (list of messages, next cursor) or None if unauthorized
        """
        # Verify ownership
        thread = await self.get_thread(thread_id, user_id)
        if not thread:
            return None

        return await self._store.get_items(
            thread_id=thread_id,
            limit=limit,
            cursor=cursor,
        )

    # =========================================================================
    # Helper Methods
    # =========================================================================

    def _generate_title(self, content: str) -> str:
        """Generate a thread title from message content.

        Takes the first line or sentence of the content, truncates if needed.

        Args:
            content: The message content

        Returns:
            A generated title string
        """
        # Clean up whitespace
        content = content.strip()

        # Take first line
        first_line = content.split("\n")[0].strip()

        # Take first sentence if line is too long
        if len(first_line) > self.MAX_TITLE_LENGTH:
            # Try to find sentence boundary
            for sep in [".", "?", "!"]:
                if sep in first_line[:self.MAX_TITLE_LENGTH]:
                    idx = first_line.index(sep)
                    if idx > 10:  # Ensure we have at least some content
                        return first_line[: idx + 1]

            # No sentence boundary, just truncate with ellipsis
            return first_line[: self.MAX_TITLE_LENGTH - 3] + "..."

        return first_line
