"""Change chat_threads.user_id from UUID to VARCHAR for BetterAuth compatibility

BetterAuth user IDs are strings like '0Dl6dRx1wnFPoz4A68X9mYMmsLBhBP2T', not UUIDs.
This migration:
1. Drops the foreign key constraint to users.id (BetterAuth users are in a different DB)
2. Changes user_id column from UUID to VARCHAR(255)

Revision ID: 006_fix_user_id_type
Revises: 005_anonymous_rate_limits
Create Date: 2025-12-02

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '006_fix_user_id_type'
down_revision: Union[str, None] = '005_anonymous_rate_limits'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Step 1: Drop the foreign key constraint
    # The constraint name follows PostgreSQL's naming convention: <table>_<column>_fkey
    op.drop_constraint('chat_threads_user_id_fkey', 'chat_threads', type_='foreignkey')

    # Step 2: Change the column type from UUID to VARCHAR(255)
    # This allows both UUID strings and BetterAuth's non-UUID strings
    op.alter_column(
        'chat_threads',
        'user_id',
        existing_type=postgresql.UUID(as_uuid=False),
        type_=sa.String(255),
        existing_nullable=False,
    )


def downgrade() -> None:
    # Step 1: Change the column type back to UUID
    # Note: This will fail if there are non-UUID values in the column
    op.alter_column(
        'chat_threads',
        'user_id',
        existing_type=sa.String(255),
        type_=postgresql.UUID(as_uuid=False),
        existing_nullable=False,
    )

    # Step 2: Re-add the foreign key constraint
    op.create_foreign_key(
        'chat_threads_user_id_fkey',
        'chat_threads',
        'users',
        ['user_id'],
        ['id'],
        ondelete='CASCADE',
    )
