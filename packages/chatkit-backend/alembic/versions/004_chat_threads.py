"""Add chat threads and thread items tables for session management

Revision ID: 004_chat_threads
Revises: 003_seed_book_data
Create Date: 2025-12-01

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '004_chat_threads'
down_revision: Union[str, None] = '003_seed_book_data'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create chat_threads table
    op.create_table(
        'chat_threads',
        sa.Column('id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('title', sa.String(255), nullable=True),
        sa.Column('metadata', postgresql.JSONB(), nullable=True, server_default='{}'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )

    # Create index on user_id for faster lookups
    op.create_index('ix_chat_threads_user_id', 'chat_threads', ['user_id'])

    # Create index on updated_at for ordering by recent
    op.create_index('ix_chat_threads_updated_at', 'chat_threads', ['updated_at'])

    # Create chat_thread_items table
    op.create_table(
        'chat_thread_items',
        sa.Column('id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('thread_id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('role', sa.String(20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('metadata', postgresql.JSONB(), nullable=True, server_default='{}'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['thread_id'], ['chat_threads.id'], ondelete='CASCADE'),
    )

    # Create index on thread_id for faster lookups
    op.create_index('ix_chat_thread_items_thread_id', 'chat_thread_items', ['thread_id'])

    # Create index on created_at for ordering messages
    op.create_index('ix_chat_thread_items_created_at', 'chat_thread_items', ['created_at'])


def downgrade() -> None:
    # Drop indexes first
    op.drop_index('ix_chat_thread_items_created_at', table_name='chat_thread_items')
    op.drop_index('ix_chat_thread_items_thread_id', table_name='chat_thread_items')
    op.drop_table('chat_thread_items')

    op.drop_index('ix_chat_threads_updated_at', table_name='chat_threads')
    op.drop_index('ix_chat_threads_user_id', table_name='chat_threads')
    op.drop_table('chat_threads')
