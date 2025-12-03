"""Initial schema for content personalization

Revision ID: 001_initial
Revises:
Create Date: 2025-11-30

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('onboarding_completed', sa.Boolean(), nullable=False, server_default='false'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create user_preferences table
    op.create_table(
        'user_preferences',
        sa.Column('id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('education_level', sa.String(50), nullable=False),
        sa.Column('programming_experience', sa.String(50), nullable=False),
        sa.Column('robotics_background', sa.Boolean(), nullable=False),
        sa.Column('ai_ml_experience', sa.String(50), nullable=False),
        sa.Column('learning_goals', postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column('preferred_language', sa.String(10), nullable=False, server_default='en'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('user_id')
    )

    # Create personalized_content_cache table
    op.create_table(
        'personalized_content_cache',
        sa.Column('id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('lesson_slug', sa.String(255), nullable=False),
        sa.Column('content_hash', sa.String(16), nullable=False),
        sa.Column('preferences_hash', sa.String(16), nullable=False),
        sa.Column('personalized_content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )

    # Create indexes
    op.create_index('ix_personalized_content_cache_lesson_slug', 'personalized_content_cache', ['lesson_slug'])
    op.create_index(
        'ix_personalized_content_cache_lookup',
        'personalized_content_cache',
        ['user_id', 'lesson_slug', 'content_hash', 'preferences_hash'],
        unique=True
    )


def downgrade() -> None:
    op.drop_index('ix_personalized_content_cache_lookup', table_name='personalized_content_cache')
    op.drop_index('ix_personalized_content_cache_lesson_slug', table_name='personalized_content_cache')
    op.drop_table('personalized_content_cache')
    op.drop_table('user_preferences')
    op.drop_table('users')
