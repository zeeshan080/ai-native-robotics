"""ChatKit services for business logic.

This module provides service classes that encapsulate business logic
and coordinate between stores, agents, and API layers.
"""

from .thread_service import ThreadService
from .rag import get_rag_context, close_clients as close_rag_clients

__all__ = [
    "ThreadService",
    "get_rag_context",
    "close_rag_clients",
]
