"""ChatKit Store implementations for thread persistence.

This module provides different storage backends for conversation threads:
- InMemoryStore: For anonymous users or development (non-persistent)
- PostgresStore: For authenticated users (persistent via PostgreSQL)

Usage:
    from chatkit_backend.stores import Store, InMemoryStore, PostgresStore
    from chatkit_backend.stores import Thread, ThreadItem

    # For anonymous users
    store = InMemoryStore()

    # For authenticated users
    async with get_db_session() as session:
        store = PostgresStore(session)

    # Create a thread
    thread = await store.create_thread(user_id="user-123", title="My Chat")

    # Add messages
    await store.add_item(thread.id, role="user", content="Hello!")
    await store.add_item(thread.id, role="assistant", content="Hi there!")

    # Load thread with messages
    thread = await store.load_thread_with_items(thread.id)
"""

from .base import Store, Thread, ThreadItem
from .memory import InMemoryStore
from .postgres import PostgresStore

__all__ = [
    # Base types
    "Store",
    "Thread",
    "ThreadItem",
    # Implementations
    "InMemoryStore",
    "PostgresStore",
]
