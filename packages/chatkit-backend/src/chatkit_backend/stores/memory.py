"""In-memory Store implementation for ChatKit thread persistence.

This implementation stores threads and items in memory, suitable for
anonymous users or development/testing. Data is lost when the server restarts.
"""

from datetime import datetime
from typing import Optional

from .base import Store, Thread, ThreadItem


class InMemoryStore(Store):
    """In-memory implementation of the Store interface.

    Stores threads and items in dictionaries. Useful for:
    - Anonymous users who don't need persistent storage
    - Development and testing
    - Short-lived sessions

    Note: Data is not persisted across server restarts.
    """

    def __init__(self):
        """Initialize the in-memory store."""
        self._threads: dict[str, Thread] = {}
        self._items: dict[str, list[ThreadItem]] = {}  # thread_id -> items

    # =========================================================================
    # Thread Operations
    # =========================================================================

    async def create_thread(
        self,
        user_id: str,
        title: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> Thread:
        """Create a new thread in memory."""
        thread = Thread.create(user_id=user_id, title=title, metadata=metadata)
        self._threads[thread.id] = thread
        self._items[thread.id] = []
        return thread

    async def get_thread(self, thread_id: str) -> Optional[Thread]:
        """Get a thread by ID from memory."""
        return self._threads.get(thread_id)

    async def update_thread(
        self,
        thread_id: str,
        title: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> Optional[Thread]:
        """Update a thread in memory."""
        thread = self._threads.get(thread_id)
        if not thread:
            return None

        if title is not None:
            thread.title = title
        if metadata is not None:
            thread.metadata = metadata
        thread.updated_at = datetime.utcnow()

        return thread

    async def delete_thread(self, thread_id: str) -> bool:
        """Delete a thread and its items from memory."""
        if thread_id not in self._threads:
            return False

        del self._threads[thread_id]
        self._items.pop(thread_id, None)
        return True

    async def list_threads(
        self,
        user_id: str,
        limit: int = 20,
        cursor: Optional[str] = None,
    ) -> tuple[list[Thread], Optional[str]]:
        """List threads for a user with pagination."""
        # Filter threads by user_id
        user_threads = [
            t for t in self._threads.values()
            if t.user_id == user_id
        ]

        # Sort by updated_at descending (most recent first)
        user_threads.sort(key=lambda t: t.updated_at, reverse=True)

        # Apply cursor-based pagination
        if cursor:
            # Find the index of the cursor thread
            cursor_index = next(
                (i for i, t in enumerate(user_threads) if t.id == cursor),
                -1,
            )
            if cursor_index >= 0:
                user_threads = user_threads[cursor_index + 1:]

        # Apply limit
        result = user_threads[:limit]

        # Determine next cursor
        next_cursor = result[-1].id if len(result) == limit else None

        return result, next_cursor

    # =========================================================================
    # Thread Item Operations
    # =========================================================================

    async def add_item(
        self,
        thread_id: str,
        role: str,
        content: str,
        metadata: Optional[dict] = None,
    ) -> ThreadItem:
        """Add a message to a thread in memory."""
        if thread_id not in self._threads:
            raise ValueError(f"Thread {thread_id} not found")

        item = ThreadItem.create(
            thread_id=thread_id,
            role=role,
            content=content,
            metadata=metadata,
        )

        self._items[thread_id].append(item)

        # Update thread's updated_at
        self._threads[thread_id].updated_at = datetime.utcnow()

        return item

    async def get_items(
        self,
        thread_id: str,
        limit: int = 50,
        cursor: Optional[str] = None,
    ) -> tuple[list[ThreadItem], Optional[str]]:
        """Get messages for a thread with pagination."""
        items = self._items.get(thread_id, [])

        # Sort by created_at ascending (oldest first)
        items = sorted(items, key=lambda i: i.created_at)

        # Apply cursor-based pagination
        if cursor:
            cursor_index = next(
                (i for i, item in enumerate(items) if item.id == cursor),
                -1,
            )
            if cursor_index >= 0:
                items = items[cursor_index + 1:]

        # Apply limit
        result = items[:limit]

        # Determine next cursor
        next_cursor = result[-1].id if len(result) == limit else None

        return result, next_cursor

    async def load_thread_with_items(
        self,
        thread_id: str,
        item_limit: int = 50,
    ) -> Optional[Thread]:
        """Load a thread with its messages from memory."""
        thread = await self.get_thread(thread_id)
        if not thread:
            return None

        items, _ = await self.get_items(thread_id, limit=item_limit)
        thread.items = items

        return thread

    # =========================================================================
    # Utility Methods
    # =========================================================================

    def clear(self) -> None:
        """Clear all data from memory. Useful for testing."""
        self._threads.clear()
        self._items.clear()

    def get_thread_count(self) -> int:
        """Get the total number of threads in memory."""
        return len(self._threads)

    def get_item_count(self, thread_id: str) -> int:
        """Get the number of items in a specific thread."""
        return len(self._items.get(thread_id, []))
