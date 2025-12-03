"""PostgreSQL Store implementation for ChatKit thread persistence.

This implementation stores threads and items in PostgreSQL using SQLAlchemy,
suitable for authenticated users who need persistent conversation history.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.models import ChatThread, ChatThreadItem
from .base import Store, Thread, ThreadItem


class PostgresStore(Store):
    """PostgreSQL implementation of the Store interface.

    Stores threads and items in PostgreSQL using async SQLAlchemy.
    Suitable for:
    - Authenticated users with persistent storage needs
    - Production deployments
    - Long-term conversation history

    Requires an active database connection via AsyncSession.
    """

    def __init__(self, session: AsyncSession):
        """Initialize the PostgreSQL store.

        Args:
            session: SQLAlchemy AsyncSession for database operations
        """
        self._session = session

    # =========================================================================
    # Helper Methods
    # =========================================================================

    def _model_to_thread(self, model: ChatThread) -> Thread:
        """Convert a SQLAlchemy model to a Thread dataclass."""
        return Thread(
            id=model.id,
            user_id=model.user_id,
            title=model.title,
            metadata=model.thread_metadata or {},
            created_at=model.created_at,
            updated_at=model.updated_at,
            items=[],
        )

    def _model_to_item(self, model: ChatThreadItem) -> ThreadItem:
        """Convert a SQLAlchemy model to a ThreadItem dataclass."""
        return ThreadItem(
            id=model.id,
            thread_id=model.thread_id,
            role=model.role,
            content=model.content,
            metadata=model.item_metadata or {},
            created_at=model.created_at,
        )

    # =========================================================================
    # Thread Operations
    # =========================================================================

    async def create_thread(
        self,
        user_id: str,
        title: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> Thread:
        """Create a new thread in the database."""
        model = ChatThread(
            user_id=user_id,
            title=title,
            thread_metadata=metadata or {},
        )
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)

        return self._model_to_thread(model)

    async def get_thread(self, thread_id: str) -> Optional[Thread]:
        """Get a thread by ID from the database."""
        result = await self._session.execute(
            select(ChatThread).where(ChatThread.id == thread_id)
        )
        model = result.scalar_one_or_none()

        if not model:
            return None

        return self._model_to_thread(model)

    async def update_thread(
        self,
        thread_id: str,
        title: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> Optional[Thread]:
        """Update a thread in the database."""
        # Build update values
        values = {"updated_at": datetime.utcnow()}
        if title is not None:
            values["title"] = title
        if metadata is not None:
            values["thread_metadata"] = metadata

        # Execute update
        result = await self._session.execute(
            update(ChatThread)
            .where(ChatThread.id == thread_id)
            .values(**values)
            .returning(ChatThread)
        )
        model = result.scalar_one_or_none()

        if not model:
            return None

        return self._model_to_thread(model)

    async def delete_thread(self, thread_id: str) -> bool:
        """Delete a thread and its items from the database."""
        # Items are deleted automatically via CASCADE
        result = await self._session.execute(
            delete(ChatThread).where(ChatThread.id == thread_id)
        )
        return result.rowcount > 0

    async def list_threads(
        self,
        user_id: str,
        limit: int = 20,
        cursor: Optional[str] = None,
    ) -> tuple[list[Thread], Optional[str]]:
        """List threads for a user with cursor-based pagination."""
        # Build base query
        query = (
            select(ChatThread)
            .where(ChatThread.user_id == user_id)
            .order_by(ChatThread.updated_at.desc())
        )

        # Apply cursor if provided
        if cursor:
            # Get the cursor thread's updated_at
            cursor_result = await self._session.execute(
                select(ChatThread.updated_at).where(ChatThread.id == cursor)
            )
            cursor_time = cursor_result.scalar_one_or_none()

            if cursor_time:
                # Get threads updated before or at the same time as cursor
                # but with a different ID (to handle same-timestamp edge case)
                query = query.where(
                    (ChatThread.updated_at < cursor_time) |
                    ((ChatThread.updated_at == cursor_time) & (ChatThread.id < cursor))
                )

        # Apply limit + 1 to check if there are more results
        query = query.limit(limit + 1)

        result = await self._session.execute(query)
        models = result.scalars().all()

        # Determine if there are more results
        has_more = len(models) > limit
        if has_more:
            models = models[:limit]

        threads = [self._model_to_thread(m) for m in models]
        next_cursor = threads[-1].id if has_more and threads else None

        return threads, next_cursor

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
        """Add a message to a thread in the database."""
        # Create the item
        model = ChatThreadItem(
            thread_id=thread_id,
            role=role,
            content=content,
            item_metadata=metadata or {},
        )
        self._session.add(model)

        # Update thread's updated_at
        await self._session.execute(
            update(ChatThread)
            .where(ChatThread.id == thread_id)
            .values(updated_at=datetime.utcnow())
        )

        await self._session.flush()
        await self._session.refresh(model)

        return self._model_to_item(model)

    async def get_items(
        self,
        thread_id: str,
        limit: int = 50,
        cursor: Optional[str] = None,
    ) -> tuple[list[ThreadItem], Optional[str]]:
        """Get messages for a thread with cursor-based pagination."""
        # Build base query (oldest first)
        query = (
            select(ChatThreadItem)
            .where(ChatThreadItem.thread_id == thread_id)
            .order_by(ChatThreadItem.created_at.asc())
        )

        # Apply cursor if provided
        if cursor:
            cursor_result = await self._session.execute(
                select(ChatThreadItem.created_at).where(ChatThreadItem.id == cursor)
            )
            cursor_time = cursor_result.scalar_one_or_none()

            if cursor_time:
                query = query.where(
                    (ChatThreadItem.created_at > cursor_time) |
                    ((ChatThreadItem.created_at == cursor_time) & (ChatThreadItem.id > cursor))
                )

        # Apply limit + 1 to check if there are more results
        query = query.limit(limit + 1)

        result = await self._session.execute(query)
        models = result.scalars().all()

        # Determine if there are more results
        has_more = len(models) > limit
        if has_more:
            models = models[:limit]

        items = [self._model_to_item(m) for m in models]
        next_cursor = items[-1].id if has_more and items else None

        return items, next_cursor

    async def load_thread_with_items(
        self,
        thread_id: str,
        item_limit: int = 50,
    ) -> Optional[Thread]:
        """Load a thread with its messages from the database."""
        thread = await self.get_thread(thread_id)
        if not thread:
            return None

        items, _ = await self.get_items(thread_id, limit=item_limit)
        thread.items = items

        return thread
