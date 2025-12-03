"""Thread management API endpoints.

Provides endpoints for managing chat conversation threads:
- POST /threads - Create a new thread
- GET /threads - List user's threads
- GET /threads/{thread_id} - Get thread with messages
- PATCH /threads/{thread_id} - Update thread title/metadata
- DELETE /threads/{thread_id} - Delete a thread
- POST /threads/{thread_id}/messages - Add a message to a thread
- GET /threads/{thread_id}/messages - Get messages with pagination
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from chatkit_backend.db import get_session
from chatkit_backend.stores import PostgresStore
from chatkit_backend.services import ThreadService
from chatkit_backend.models.thread import (
    CreateThreadRequest,
    AddMessageRequest,
    UpdateThreadRequest,
    ThreadResponse,
    ThreadItemResponse,
    ThreadListResponse,
    MessageListResponse,
)
from chatkit_backend.models.user import ErrorResponse

router = APIRouter(prefix="/threads", tags=["Threads"])


def _thread_to_response(thread) -> ThreadResponse:
    """Convert a Thread dataclass to ThreadResponse."""
    return ThreadResponse(
        id=thread.id,
        user_id=thread.user_id,
        title=thread.title,
        metadata=thread.metadata,
        created_at=thread.created_at,
        updated_at=thread.updated_at,
        items=[
            ThreadItemResponse(
                id=item.id,
                thread_id=item.thread_id,
                role=item.role,
                content=item.content,
                metadata=item.metadata,
                created_at=item.created_at,
            )
            for item in thread.items
        ],
    )


def _item_to_response(item) -> ThreadItemResponse:
    """Convert a ThreadItem dataclass to ThreadItemResponse."""
    return ThreadItemResponse(
        id=item.id,
        thread_id=item.thread_id,
        role=item.role,
        content=item.content,
        metadata=item.metadata,
        created_at=item.created_at,
    )


async def get_thread_service(
    session: AsyncSession = Depends(get_session),
) -> ThreadService:
    """Dependency to get ThreadService with PostgresStore."""
    store = PostgresStore(session)
    return ThreadService(store)


@router.post(
    "",
    response_model=ThreadResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request"},
    },
)
async def create_thread(
    request: CreateThreadRequest,
    service: ThreadService = Depends(get_thread_service),
) -> ThreadResponse:
    """Create a new chat thread.

    Creates an empty thread for the user. The title can be provided
    or will be auto-generated from the first user message.
    """
    thread = await service.create_thread(
        user_id=request.user_id,
        title=request.title,
        metadata=request.metadata,
    )
    return _thread_to_response(thread)


@router.get(
    "",
    response_model=ThreadListResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request"},
    },
)
async def list_threads(
    user_id: str = Query(..., description="User ID to list threads for"),
    limit: int = Query(20, ge=1, le=100, description="Max threads to return"),
    cursor: Optional[str] = Query(None, description="Pagination cursor"),
    service: ThreadService = Depends(get_thread_service),
) -> ThreadListResponse:
    """List threads for a user.

    Returns threads ordered by most recently updated, with cursor-based
    pagination for efficient scrolling through large lists.
    """
    threads, next_cursor = await service.list_threads(
        user_id=user_id,
        limit=limit,
        cursor=cursor,
    )
    return ThreadListResponse(
        threads=[_thread_to_response(t) for t in threads],
        next_cursor=next_cursor,
    )


@router.get(
    "/{thread_id}",
    response_model=ThreadResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Thread not found"},
    },
)
async def get_thread(
    thread_id: str,
    user_id: str = Query(..., description="User ID for ownership validation"),
    message_limit: int = Query(50, ge=1, le=200, description="Max messages to load"),
    service: ThreadService = Depends(get_thread_service),
) -> ThreadResponse:
    """Get a thread with its messages.

    Returns the thread details along with the most recent messages,
    validating that the requesting user owns the thread.
    """
    thread = await service.get_thread_with_messages(
        thread_id=thread_id,
        user_id=user_id,
        message_limit=message_limit,
    )
    if not thread:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": "Thread not found or unauthorized"},
        )
    return _thread_to_response(thread)


@router.patch(
    "/{thread_id}",
    response_model=ThreadResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Thread not found"},
    },
)
async def update_thread(
    thread_id: str,
    request: UpdateThreadRequest,
    user_id: str = Query(..., description="User ID for ownership validation"),
    service: ThreadService = Depends(get_thread_service),
) -> ThreadResponse:
    """Update a thread's title or metadata.

    Only the thread owner can update the thread.
    """
    thread = await service.update_thread(
        thread_id=thread_id,
        user_id=user_id,
        title=request.title,
        metadata=request.metadata,
    )
    if not thread:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": "Thread not found or unauthorized"},
        )
    return _thread_to_response(thread)


@router.delete(
    "/{thread_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"model": ErrorResponse, "description": "Thread not found"},
    },
)
async def delete_thread(
    thread_id: str,
    user_id: str = Query(..., description="User ID for ownership validation"),
    service: ThreadService = Depends(get_thread_service),
) -> None:
    """Delete a thread and all its messages.

    Only the thread owner can delete the thread. This operation
    is permanent and cannot be undone.
    """
    success = await service.delete_thread(
        thread_id=thread_id,
        user_id=user_id,
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": "Thread not found or unauthorized"},
        )


@router.post(
    "/{thread_id}/messages",
    response_model=ThreadItemResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        404: {"model": ErrorResponse, "description": "Thread not found"},
    },
)
async def add_message(
    thread_id: str,
    request: AddMessageRequest,
    user_id: str = Query(..., description="User ID for ownership validation"),
    service: ThreadService = Depends(get_thread_service),
) -> ThreadItemResponse:
    """Add a message to a thread.

    If this is the first user message and the thread has no title,
    a title will be auto-generated from the message content.
    """
    item = await service.add_message(
        thread_id=thread_id,
        user_id=user_id,
        role=request.role,
        content=request.content,
        metadata=request.metadata,
    )
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": "Thread not found or unauthorized"},
        )
    return _item_to_response(item)


@router.get(
    "/{thread_id}/messages",
    response_model=MessageListResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Thread not found"},
    },
)
async def get_messages(
    thread_id: str,
    user_id: str = Query(..., description="User ID for ownership validation"),
    limit: int = Query(50, ge=1, le=200, description="Max messages to return"),
    cursor: Optional[str] = Query(None, description="Pagination cursor"),
    service: ThreadService = Depends(get_thread_service),
) -> MessageListResponse:
    """Get messages for a thread with pagination.

    Returns messages in chronological order (oldest first),
    with cursor-based pagination for loading history.
    """
    result = await service.get_messages(
        thread_id=thread_id,
        user_id=user_id,
        limit=limit,
        cursor=cursor,
    )
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": "Thread not found or unauthorized"},
        )
    messages, next_cursor = result
    return MessageListResponse(
        messages=[_item_to_response(m) for m in messages],
        next_cursor=next_cursor,
    )
