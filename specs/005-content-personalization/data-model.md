# Data Model: Content Personalization

**Feature**: 005-content-personalization
**Date**: 2025-11-30
**Updated**: 2025-11-30 (Added book structure, progress tracking)

## Entity Relationship Diagram

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│   books     │◄──────│   parts     │◄──────│  chapters   │◄──────│   lessons   │
├─────────────┤  1:N  ├─────────────┤  1:N  ├─────────────┤  1:N  ├─────────────┤
│ id (PK)     │       │ id (PK)     │       │ id (PK)     │       │ id (PK)     │
│ slug        │       │ book_id     │       │ part_id     │       │ chapter_id  │
│ title       │       │ number      │       │ number      │       │ number      │
│ description │       │ title       │       │ local_number│       │ title       │
│ version     │       │ layer       │       │ title       │       │ slug        │
└─────────────┘       │ tier        │       │ folder_name │       │ type        │
                      │ folder_name │       │ prerequisites│      │ content_hash│
                      │ week_start  │       └─────────────┘       │ bucket_path │
                      │ week_end    │              │               │ vector_ids  │
                      └─────────────┘              │               │ sidebar_pos │
                                                   │               └─────────────┘
                                                   │                      │
┌─────────────────┐         ┌─────────────────────┐│                      │
│     users       │         │  user_preferences   ││                      │
├─────────────────┤         ├─────────────────────┤│                      │
│ id (PK, UUID)   │◄────────│ id (PK, UUID)       ││                      │
│ created_at      │    1:1  │ user_id (FK)        ││                      │
│ updated_at      │         │ education_level     ││                      │
│ onboarding_done │         │ programming_exp     ││                      │
└─────────────────┘         │ robotics_background ││                      │
        │                   │ ai_ml_experience    ││                      │
        │                   │ learning_goals      ││                      │
        │                   │ preferred_language  ││                      │
        │ 1:N               └─────────────────────┘│                      │
        │                                          │                      │
        ▼                                          │                      │
┌─────────────────────────────────┐                │                      │
│   personalized_content_cache    │                │                      │
├─────────────────────────────────┤                │                      │
│ id (PK, UUID)                   │                │                      │
│ user_id (FK)                    │                │                      │
│ lesson_slug (indexed)           │                │                      │
│ content_hash                    │                │                      │
│ preferences_hash                │                │                      │
│ personalized_content (TEXT)     │                │                      │
│ created_at                      │                │                      │
└─────────────────────────────────┘                │                      │
        │                                          │                      │
        │           ┌──────────────────────────────┘                      │
        │           │                                                     │
        ▼           ▼                                                     │
┌─────────────────────────────────┐                                       │
│       user_progress             │◄──────────────────────────────────────┘
├─────────────────────────────────┤  N:1
│ id (PK, UUID)                   │
│ user_id (FK → users)            │
│ lesson_id (FK → lessons)        │
│ status                          │  'not_started' | 'in_progress' | 'completed'
│ started_at                      │
│ completed_at                    │
│ time_spent_seconds              │
│ created_at                      │
│ updated_at                      │
└─────────────────────────────────┘
```

## Table Definitions

### users

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, DEFAULT uuid_generate_v4() | Unique user identifier |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Account creation time |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update time |
| onboarding_completed | BOOLEAN | NOT NULL, DEFAULT FALSE | Has user completed onboarding |

**Indexes**:
- PRIMARY KEY on `id`

### user_preferences

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, DEFAULT uuid_generate_v4() | Preference record ID |
| user_id | UUID | FK → users(id), UNIQUE | Associated user |
| education_level | VARCHAR(50) | NOT NULL | high_school, undergraduate, graduate, professional |
| programming_experience | VARCHAR(50) | NOT NULL | none, beginner, intermediate, advanced |
| robotics_background | BOOLEAN | NOT NULL | Has robotics experience |
| ai_ml_experience | VARCHAR(50) | NOT NULL | none, basic, intermediate, advanced |
| learning_goals | TEXT[] | NOT NULL | Array: career_change, research, hobby, teaching, building_projects |
| preferred_language | VARCHAR(10) | NOT NULL, DEFAULT 'en' | en, ur |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Record creation time |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update time |

**Indexes**:
- PRIMARY KEY on `id`
- UNIQUE on `user_id`

**Validation Rules**:
- `education_level` IN ('high_school', 'undergraduate', 'graduate', 'professional')
- `programming_experience` IN ('none', 'beginner', 'intermediate', 'advanced')
- `ai_ml_experience` IN ('none', 'basic', 'intermediate', 'advanced')
- `preferred_language` IN ('en', 'ur')
- `learning_goals` elements IN ('career_change', 'research', 'hobby', 'teaching', 'building_projects')

### personalized_content_cache

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, DEFAULT uuid_generate_v4() | Cache entry ID |
| user_id | UUID | FK → users(id) | Associated user |
| lesson_slug | VARCHAR(255) | NOT NULL | Lesson identifier (e.g., "01-intro/embodiment") |
| content_hash | VARCHAR(16) | NOT NULL | SHA256 prefix of original content |
| preferences_hash | VARCHAR(16) | NOT NULL | Hash of relevant preferences |
| personalized_content | TEXT | NOT NULL | Generated personalized content |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Cache entry creation time |

**Indexes**:
- PRIMARY KEY on `id`
- UNIQUE on (`user_id`, `lesson_slug`, `content_hash`, `preferences_hash`)
- INDEX on `lesson_slug`

### books

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, DEFAULT uuid_generate_v4() | Unique book identifier |
| slug | VARCHAR(100) | NOT NULL, UNIQUE | URL-friendly identifier (e.g., 'ai-native-robotics') |
| title | VARCHAR(255) | NOT NULL | Book title |
| description | TEXT | | Book description |
| version | VARCHAR(20) | DEFAULT '1.0.0' | Semantic version |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update time |

**Indexes**:
- PRIMARY KEY on `id`
- UNIQUE on `slug`

### parts

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, DEFAULT uuid_generate_v4() | Unique part identifier |
| book_id | UUID | FK → books(id), NOT NULL | Associated book |
| number | INTEGER | NOT NULL | Part number (1-6) |
| title | VARCHAR(255) | NOT NULL | Part title |
| description | TEXT | | Part description |
| layer | VARCHAR(10) | NOT NULL | Pedagogy layer (L1, L2, L3, L4, L5) |
| tier | VARCHAR(20) | | Proficiency tier (A2, B1, B2, C1, C2) |
| folder_name | VARCHAR(100) | NOT NULL | Filesystem folder (e.g., '01-Physical-AI-Foundations') |
| week_start | INTEGER | | Starting week number |
| week_end | INTEGER | | Ending week number |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update time |

**Indexes**:
- PRIMARY KEY on `id`
- UNIQUE on (`book_id`, `number`)

**Validation Rules**:
- `layer` IN ('L1', 'L2', 'L3', 'L4', 'L5')
- `tier` IN ('A2', 'B1', 'B2', 'C1', 'C2')

### chapters

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, DEFAULT uuid_generate_v4() | Unique chapter identifier |
| part_id | UUID | FK → parts(id), NOT NULL | Associated part |
| number | INTEGER | NOT NULL | Global chapter number (1-18) |
| local_number | INTEGER | NOT NULL | Chapter number within part (1, 2, 3...) |
| title | VARCHAR(255) | NOT NULL | Chapter title |
| description | TEXT | | Chapter description |
| folder_name | VARCHAR(100) | NOT NULL | Filesystem folder (e.g., '01-what-is-physical-ai') |
| prerequisites | JSONB | DEFAULT '[]' | Array of prerequisite chapter IDs |
| transition_check | TEXT | | Transition check question |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update time |

**Indexes**:
- PRIMARY KEY on `id`
- UNIQUE on (`part_id`, `local_number`)

### lessons

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, DEFAULT uuid_generate_v4() | Unique lesson identifier |
| chapter_id | UUID | FK → chapters(id), NOT NULL | Associated chapter |
| number | INTEGER | NOT NULL | Lesson number within chapter |
| title | VARCHAR(255) | NOT NULL | Lesson title |
| slug | VARCHAR(255) | NOT NULL | URL slug (e.g., '01-lesson-digital-vs-physical-ai') |
| type | VARCHAR(20) | NOT NULL | Content type: 'lesson', 'lab', 'summary', 'index' |
| content_hash | VARCHAR(64) | | SHA-256 hash of content for cache invalidation |
| bucket_path | VARCHAR(500) | | Path in storage bucket |
| vector_ids | JSONB | DEFAULT '[]' | Array of vector DB IDs for RAG chunks |
| sidebar_position | INTEGER | | Docusaurus sidebar ordering |
| estimated_minutes | INTEGER | | Estimated reading time |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update time |

**Indexes**:
- PRIMARY KEY on `id`
- UNIQUE on (`chapter_id`, `slug`)
- INDEX on `slug`

**Validation Rules**:
- `type` IN ('lesson', 'lab', 'summary', 'index')

### user_progress

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, DEFAULT uuid_generate_v4() | Unique progress entry ID |
| user_id | UUID | FK → users(id), NOT NULL | Associated user |
| lesson_id | UUID | FK → lessons(id), NOT NULL | Associated lesson |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'not_started' | Progress status |
| started_at | TIMESTAMP | | When user started the lesson |
| completed_at | TIMESTAMP | | When user completed the lesson |
| time_spent_seconds | INTEGER | DEFAULT 0 | Total time spent on lesson |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update time |

**Indexes**:
- PRIMARY KEY on `id`
- UNIQUE on (`user_id`, `lesson_id`)
- INDEX on `status`

**Validation Rules**:
- `status` IN ('not_started', 'in_progress', 'completed')

## SQLAlchemy Models

```python
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY, UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    onboarding_completed: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    preferences: Mapped[Optional["UserPreferences"]] = relationship(
        back_populates="user", uselist=False
    )
    cache_entries: Mapped[list["PersonalizedContentCache"]] = relationship(
        back_populates="user"
    )


class UserPreferences(Base):
    __tablename__ = "user_preferences"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id"), unique=True
    )
    education_level: Mapped[str] = mapped_column(String(50))
    programming_experience: Mapped[str] = mapped_column(String(50))
    robotics_background: Mapped[bool] = mapped_column(Boolean)
    ai_ml_experience: Mapped[str] = mapped_column(String(50))
    learning_goals: Mapped[list[str]] = mapped_column(ARRAY(String))
    preferred_language: Mapped[str] = mapped_column(String(10), default="en")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="preferences")


class PersonalizedContentCache(Base):
    __tablename__ = "personalized_content_cache"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id")
    )
    lesson_slug: Mapped[str] = mapped_column(String(255), index=True)
    content_hash: Mapped[str] = mapped_column(String(16))
    preferences_hash: Mapped[str] = mapped_column(String(16))
    personalized_content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="cache_entries")

    __table_args__ = (
        # Composite unique constraint for cache lookup
        {"unique_together": ["user_id", "lesson_slug", "content_hash", "preferences_hash"]},
    )
```

## State Transitions

### User Onboarding State

```
┌─────────────────┐     Complete       ┌─────────────────┐
│ onboarding_done │ ───Questionnaire──►│ onboarding_done │
│     = false     │                    │     = true      │
└─────────────────┘                    └─────────────────┘
        │                                      │
        │                                      │
        ▼                                      ▼
  Can view Original                  Can view Original
  content only                       AND Personalized
```

### Cache Entry Lifecycle

```
┌──────────────┐   Cache    ┌──────────────┐   Original   ┌──────────────┐
│  No Cache    │ ──Miss───► │ Generating   │ ──Change───► │ Invalidated  │
│              │            │              │              │              │
└──────────────┘            └──────────────┘              └──────────────┘
       ▲                           │                             │
       │                           │                             │
       │                           ▼                             │
       │                    ┌──────────────┐                     │
       └───Prefs Change─────│   Cached     │◄────Regenerate──────┘
                            │              │
                            └──────────────┘
```

## Migration Strategy

### Initial Migration (001_initial_schema.py)

```python
"""Initial schema for content personalization

Revision ID: 001
Create Date: 2025-11-30
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Enable UUID extension
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    # Create users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('onboarding_completed', sa.Boolean(), nullable=False, server_default='false'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create user_preferences table
    op.create_table(
        'user_preferences',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
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
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('lesson_slug', sa.String(255), nullable=False),
        sa.Column('content_hash', sa.String(16), nullable=False),
        sa.Column('preferences_hash', sa.String(16), nullable=False),
        sa.Column('personalized_content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('user_id', 'lesson_slug', 'content_hash', 'preferences_hash')
    )
    op.create_index('ix_personalized_content_cache_lesson_slug', 'personalized_content_cache', ['lesson_slug'])


def downgrade() -> None:
    op.drop_table('personalized_content_cache')
    op.drop_table('user_preferences')
    op.drop_table('users')
```

### Book Structure Migration (002_book_structure.py)

```python
"""Add book structure tables

Revision ID: 002
Create Date: 2025-11-30
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create books table
    op.create_table(
        'books',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('slug', sa.String(100), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('version', sa.String(20), server_default='1.0.0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug')
    )

    # Create parts table
    op.create_table(
        'parts',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('book_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('number', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('layer', sa.String(10), nullable=False),
        sa.Column('tier', sa.String(20)),
        sa.Column('folder_name', sa.String(100), nullable=False),
        sa.Column('week_start', sa.Integer()),
        sa.Column('week_end', sa.Integer()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['book_id'], ['books.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('book_id', 'number', name='uq_part_book_number')
    )

    # Create chapters table
    op.create_table(
        'chapters',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('part_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('number', sa.Integer(), nullable=False),
        sa.Column('local_number', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('folder_name', sa.String(100), nullable=False),
        sa.Column('prerequisites', postgresql.JSONB(), server_default='[]'),
        sa.Column('transition_check', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['part_id'], ['parts.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('part_id', 'local_number', name='uq_chapter_part_local')
    )

    # Create lessons table
    op.create_table(
        'lessons',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('chapter_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('number', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('slug', sa.String(255), nullable=False),
        sa.Column('type', sa.String(20), nullable=False),
        sa.Column('content_hash', sa.String(64)),
        sa.Column('bucket_path', sa.String(500)),
        sa.Column('vector_ids', postgresql.JSONB(), server_default='[]'),
        sa.Column('sidebar_position', sa.Integer()),
        sa.Column('estimated_minutes', sa.Integer()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['chapter_id'], ['chapters.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('chapter_id', 'slug', name='uq_lesson_chapter_slug')
    )
    op.create_index('ix_lessons_slug', 'lessons', ['slug'])

    # Create user_progress table
    op.create_table(
        'user_progress',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('lesson_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('status', sa.String(20), nullable=False, server_default='not_started'),
        sa.Column('started_at', sa.DateTime(timezone=True)),
        sa.Column('completed_at', sa.DateTime(timezone=True)),
        sa.Column('time_spent_seconds', sa.Integer(), server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['lesson_id'], ['lessons.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('user_id', 'lesson_id', name='uq_user_progress')
    )
    op.create_index('ix_user_progress_status', 'user_progress', ['status'])


def downgrade() -> None:
    op.drop_table('user_progress')
    op.drop_table('lessons')
    op.drop_table('chapters')
    op.drop_table('parts')
    op.drop_table('books')
```

## New SQLAlchemy Models (Book Structure)

```python
from sqlalchemy import Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB


class Book(Base):
    """Book model for textbook metadata."""
    __tablename__ = "books"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    version: Mapped[str] = mapped_column(String(20), default="1.0.0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    parts: Mapped[list["Part"]] = relationship("Part", back_populates="book", cascade="all, delete-orphan")


class Part(Base):
    """Part model for book sections."""
    __tablename__ = "parts"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    book_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("books.id", ondelete="CASCADE"))
    number: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    layer: Mapped[str] = mapped_column(String(10), nullable=False)
    tier: Mapped[Optional[str]] = mapped_column(String(20))
    folder_name: Mapped[str] = mapped_column(String(100), nullable=False)
    week_start: Mapped[Optional[int]] = mapped_column(Integer)
    week_end: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    book: Mapped["Book"] = relationship("Book", back_populates="parts")
    chapters: Mapped[list["Chapter"]] = relationship("Chapter", back_populates="part", cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint('book_id', 'number', name='uq_part_book_number'),)


class Chapter(Base):
    """Chapter model within a part."""
    __tablename__ = "chapters"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    part_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("parts.id", ondelete="CASCADE"))
    number: Mapped[int] = mapped_column(Integer, nullable=False)
    local_number: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    folder_name: Mapped[str] = mapped_column(String(100), nullable=False)
    prerequisites: Mapped[list] = mapped_column(JSONB, default=list)
    transition_check: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    part: Mapped["Part"] = relationship("Part", back_populates="chapters")
    lessons: Mapped[list["Lesson"]] = relationship("Lesson", back_populates="chapter", cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint('part_id', 'local_number', name='uq_chapter_part_local'),)


class Lesson(Base):
    """Lesson model for individual content items."""
    __tablename__ = "lessons"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    chapter_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("chapters.id", ondelete="CASCADE"))
    number: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False)
    content_hash: Mapped[Optional[str]] = mapped_column(String(64))
    bucket_path: Mapped[Optional[str]] = mapped_column(String(500))
    vector_ids: Mapped[list] = mapped_column(JSONB, default=list)
    sidebar_position: Mapped[Optional[int]] = mapped_column(Integer)
    estimated_minutes: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    chapter: Mapped["Chapter"] = relationship("Chapter", back_populates="lessons")
    progress_entries: Mapped[list["UserProgress"]] = relationship("UserProgress", back_populates="lesson", cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint('chapter_id', 'slug', name='uq_lesson_chapter_slug'),)


class UserProgress(Base):
    """Track user progress through lessons."""
    __tablename__ = "user_progress"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    lesson_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("lessons.id", ondelete="CASCADE"))
    status: Mapped[str] = mapped_column(String(20), default="not_started")
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    time_spent_seconds: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="progress_entries")
    lesson: Mapped["Lesson"] = relationship("Lesson", back_populates="progress_entries")

    __table_args__ = (UniqueConstraint('user_id', 'lesson_id', name='uq_user_progress'),)
```

## Progress State Transitions

```
┌─────────────────┐       Start       ┌─────────────────┐      Complete     ┌─────────────────┐
│   not_started   │ ─────────────────►│   in_progress   │ ─────────────────►│    completed    │
└─────────────────┘                   └─────────────────┘                   └─────────────────┘
                                              │                                      │
                                              │       Re-read                        │
                                              │◄─────────────────────────────────────┘
```
