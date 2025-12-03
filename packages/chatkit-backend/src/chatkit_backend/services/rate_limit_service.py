"""
Rate limiting service for anonymous users.

Tracks message count by IP address to enforce the trial limit.
"""

import logging
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.models import AnonymousRateLimit

logger = logging.getLogger(__name__)

# Maximum messages allowed for anonymous users
ANONYMOUS_MESSAGE_LIMIT = 10


class RateLimitService:
    """Service for managing anonymous user rate limits."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_usage(self, ip_address: str) -> tuple[int, int]:
        """Get current usage for an IP address.

        Args:
            ip_address: The client's IP address

        Returns:
            Tuple of (message_count, remaining)
        """
        stmt = select(AnonymousRateLimit).where(
            AnonymousRateLimit.ip_address == ip_address
        )
        result = await self._session.execute(stmt)
        rate_limit = result.scalar_one_or_none()

        if rate_limit is None:
            return 0, ANONYMOUS_MESSAGE_LIMIT

        remaining = max(0, ANONYMOUS_MESSAGE_LIMIT - rate_limit.message_count)
        return rate_limit.message_count, remaining

    async def check_limit(self, ip_address: str) -> tuple[bool, int]:
        """Check if the IP address is within the rate limit.

        Args:
            ip_address: The client's IP address

        Returns:
            Tuple of (allowed, remaining)
        """
        count, remaining = await self.get_usage(ip_address)
        allowed = remaining > 0
        return allowed, remaining

    async def increment(self, ip_address: str) -> tuple[int, int]:
        """Increment the message count for an IP address.

        Args:
            ip_address: The client's IP address

        Returns:
            Tuple of (new_count, remaining)
        """
        stmt = select(AnonymousRateLimit).where(
            AnonymousRateLimit.ip_address == ip_address
        )
        result = await self._session.execute(stmt)
        rate_limit = result.scalar_one_or_none()

        if rate_limit is None:
            # Create new record
            rate_limit = AnonymousRateLimit(
                ip_address=ip_address,
                message_count=1,
            )
            self._session.add(rate_limit)
            await self._session.commit()
            logger.info(f"New anonymous user from {ip_address}, count: 1")
            return 1, ANONYMOUS_MESSAGE_LIMIT - 1

        # Increment existing
        rate_limit.message_count += 1
        await self._session.commit()

        remaining = max(0, ANONYMOUS_MESSAGE_LIMIT - rate_limit.message_count)
        logger.info(f"Anonymous user {ip_address}, count: {rate_limit.message_count}, remaining: {remaining}")
        return rate_limit.message_count, remaining

    async def reset(self, ip_address: str) -> bool:
        """Reset the rate limit for an IP address (admin only).

        Args:
            ip_address: The client's IP address

        Returns:
            True if reset was successful
        """
        stmt = select(AnonymousRateLimit).where(
            AnonymousRateLimit.ip_address == ip_address
        )
        result = await self._session.execute(stmt)
        rate_limit = result.scalar_one_or_none()

        if rate_limit is None:
            return False

        rate_limit.message_count = 0
        await self._session.commit()
        logger.info(f"Reset rate limit for {ip_address}")
        return True
