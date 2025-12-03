"""Add book structure tables

Revision ID: 002_book_structure
Revises: 001_initial
Create Date: 2025-11-30

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '002_book_structure'
down_revision: Union[str, None] = '001_initial'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create books table
    op.create_table(
        'books',
        sa.Column('id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('slug', sa.String(100), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('version', sa.String(20), nullable=False, server_default='1.0.0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug')
    )
    op.create_index('ix_books_slug', 'books', ['slug'])

    # Create parts table
    op.create_table(
        'parts',
        sa.Column('id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('book_id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('number', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('layer', sa.String(10), nullable=False),
        sa.Column('tier', sa.String(20), nullable=False),
        sa.Column('folder_name', sa.String(100), nullable=False),
        sa.Column('week_start', sa.Integer(), nullable=False),
        sa.Column('week_end', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['book_id'], ['books.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_parts_book_number', 'parts', ['book_id', 'number'], unique=True)

    # Create chapters table
    op.create_table(
        'chapters',
        sa.Column('id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('part_id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('number', sa.Integer(), nullable=False),
        sa.Column('local_number', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('folder_name', sa.String(100), nullable=False),
        sa.Column('prerequisites', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['part_id'], ['parts.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_chapters_number', 'chapters', ['number'], unique=True)
    op.create_index('ix_chapters_part_local', 'chapters', ['part_id', 'local_number'], unique=True)

    # Create lessons table
    op.create_table(
        'lessons',
        sa.Column('id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('chapter_id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('number', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('slug', sa.String(255), nullable=False),
        sa.Column('type', sa.String(20), nullable=False),
        sa.Column('content_hash', sa.String(64), nullable=True),
        sa.Column('bucket_path', sa.String(500), nullable=True),
        sa.Column('vector_ids', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['chapter_id'], ['chapters.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('slug')
    )
    op.create_index('ix_lessons_slug', 'lessons', ['slug'])
    op.create_index('ix_lessons_chapter_number', 'lessons', ['chapter_id', 'number'], unique=True)

    # Create user_progress table
    op.create_table(
        'user_progress',
        sa.Column('id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('lesson_id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('status', sa.String(20), nullable=False, server_default='not_started'),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('time_spent_seconds', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['lesson_id'], ['lessons.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_user_progress_user_lesson', 'user_progress', ['user_id', 'lesson_id'], unique=True)
    op.create_index('ix_user_progress_user_status', 'user_progress', ['user_id', 'status'])


def downgrade() -> None:
    op.drop_index('ix_user_progress_user_status', table_name='user_progress')
    op.drop_index('ix_user_progress_user_lesson', table_name='user_progress')
    op.drop_table('user_progress')

    op.drop_index('ix_lessons_chapter_number', table_name='lessons')
    op.drop_index('ix_lessons_slug', table_name='lessons')
    op.drop_table('lessons')

    op.drop_index('ix_chapters_part_local', table_name='chapters')
    op.drop_index('ix_chapters_number', table_name='chapters')
    op.drop_table('chapters')

    op.drop_index('ix_parts_book_number', table_name='parts')
    op.drop_table('parts')

    op.drop_index('ix_books_slug', table_name='books')
    op.drop_table('books')
