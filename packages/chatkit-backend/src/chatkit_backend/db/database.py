"""Async database engine and session factory for NeonDB Serverless Postgres."""

import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

# Module-level engine (lazy initialization)
_engine: Optional[AsyncEngine] = None
_async_session_factory: Optional[async_sessionmaker[AsyncSession]] = None


def get_database_url() -> Optional[str]:
    """Get and convert DATABASE_URL for asyncpg driver."""
    url = os.getenv("DATABASE_URL")
    if not url:
        return None

    # Convert postgresql:// to postgresql+asyncpg://
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
    elif url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+asyncpg://", 1)

    # Remove parameters not supported by asyncpg
    # channel_binding and sslmode need to be handled differently
    if "?" in url:
        parts = url.split("?")
        if len(parts) == 2:
            base_url = parts[0]
            params = parts[1].split("&")
            # Filter out unsupported parameters
            filtered_params = [
                p for p in params
                if not p.startswith("channel_binding=")
                and not p.startswith("sslmode=")
            ]
            if filtered_params:
                url = f"{base_url}?{'&'.join(filtered_params)}"
            else:
                url = base_url

    return url


def get_engine() -> AsyncEngine:
    """Get or create the async database engine."""
    global _engine

    if _engine is None:
        database_url = get_database_url()
        if not database_url:
            raise RuntimeError("DATABASE_URL not configured")

        _engine = create_async_engine(
            database_url,
            echo=False,  # Set to True for SQL debugging
            pool_pre_ping=True,  # Verify connections before use
            pool_size=5,
            max_overflow=10,
            connect_args={"ssl": "require"},  # SSL for NeonDB
        )

    return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """Get or create the async session factory."""
    global _async_session_factory

    if _async_session_factory is None:
        _async_session_factory = async_sessionmaker(
            get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
        )

    return _async_session_factory


# Expose for backwards compatibility
engine = None  # Will be initialized lazily
async_session_factory = None  # Will be initialized lazily


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get an async database session.

    Usage:
        async with get_db_session() as session:
            result = await session.execute(select(User))
    """
    factory = get_session_factory()
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency for database sessions.

    Usage:
        @app.get("/users")
        async def get_users(session: AsyncSession = Depends(get_session)):
            ...
    """
    factory = get_session_factory()
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
