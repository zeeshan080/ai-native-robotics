"""Add anonymous_rate_limits table for IP-based rate limiting

Revision ID: 005_anonymous_rate_limits
Revises: 004_chat_threads
Create Date: 2025-12-01

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '005_anonymous_rate_limits'
down_revision: Union[str, None] = '004_chat_threads'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create anonymous_rate_limits table
    op.create_table(
        'anonymous_rate_limits',
        sa.Column('id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('ip_address', sa.String(45), nullable=False),  # IPv6 max length
        sa.Column('message_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('first_message_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('last_message_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )

    # Create unique index on ip_address for fast lookups and uniqueness
    op.create_index(
        'ix_anonymous_rate_limits_ip_address',
        'anonymous_rate_limits',
        ['ip_address'],
        unique=True
    )


def downgrade() -> None:
    op.drop_index('ix_anonymous_rate_limits_ip_address', table_name='anonymous_rate_limits')
    op.drop_table('anonymous_rate_limits')
