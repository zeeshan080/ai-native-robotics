# Research: Content Personalization

**Feature**: 005-content-personalization
**Date**: 2025-11-30

## Research Tasks Completed

### 1. SQLAlchemy 2.0 Async with NeonDB

**Decision**: Use SQLAlchemy 2.0 async with asyncpg driver

**Rationale**:
- SQLAlchemy 2.0 has native async/await support
- asyncpg is the fastest PostgreSQL driver for Python
- NeonDB is compatible with standard PostgreSQL drivers
- Alembic migrations work with async engines

**Alternatives Considered**:
- Drizzle ORM: Rejected - JavaScript only, backend is Python
- Raw asyncpg: Rejected - No ORM benefits, more boilerplate
- SQLModel: Considered - Built on SQLAlchemy, but less mature async support

**Best Practices**:
```python
# Connection string format for NeonDB
DATABASE_URL = "postgresql+asyncpg://user:pass@ep-xxx.region.aws.neon.tech/dbname?sslmode=require"

# Async session factory
async_session = async_sessionmaker(engine, expire_on_commit=False)

# Context manager for sessions
async with async_session() as session:
    async with session.begin():
        # queries here
```

### 2. User Identification Without Auth

**Decision**: Generate UUID v4 client-side, store in localStorage

**Rationale**:
- No server-side session management needed for MVP
- UUID v4 has negligible collision probability
- Simple to implement, easy to migrate to auth later

**Alternatives Considered**:
- Server-generated ID: Requires extra roundtrip on first visit
- Fingerprinting: Privacy concerns, inconsistent
- BetterAuth immediately: Slows down MVP delivery

**Best Practices**:
```typescript
// Generate or retrieve user ID
const getUserId = (): string => {
  let userId = localStorage.getItem('user_id');
  if (!userId) {
    userId = crypto.randomUUID();
    localStorage.setItem('user_id', userId);
  }
  return userId;
};
```

### 3. Content Personalization Caching Strategy

**Decision**: Cache by (user_id, lesson_slug, content_hash, preferences_hash)

**Rationale**:
- content_hash detects original content changes
- preferences_hash detects user preference changes
- Composite key ensures cache invalidation on any relevant change

**Alternatives Considered**:
- Time-based expiry only: Stale content if original changes
- No caching: Poor UX on repeated visits
- Pre-generation: Too many combinations to pre-compute

**Best Practices**:
```python
import hashlib

def compute_content_hash(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()[:16]

def compute_preferences_hash(prefs: UserPreferences) -> str:
    key = f"{prefs.education_level}:{prefs.programming_experience}:{prefs.preferred_language}"
    return hashlib.sha256(key.encode()).hexdigest()[:16]
```

### 4. LLM Personalization Agent Design

**Decision**: Single-shot prompt with user profile context

**Rationale**:
- Simpler than multi-turn agent
- Full context in one request
- Predictable cost and latency

**Alternatives Considered**:
- Multi-turn refinement: Higher latency, more complex
- Fine-tuned model: Expensive, overkill for content adaptation
- Template-based adaptation: Less flexible, more maintenance

**Best Practices**:
```python
PERSONALIZATION_PROMPT = """
You are a content personalization agent for a robotics textbook.

User Profile:
- Education: {education_level}
- Programming: {programming_experience}
- Robotics Background: {has_robotics_background}
- AI/ML Experience: {ai_ml_experience}
- Goals: {learning_goals}
- Language: {preferred_language}

Adaptation Rules:
- If beginner programmer: Add more code explanations, simpler examples
- If advanced: Skip basics, add deeper insights
- If robotics background: Use technical terminology
- If no robotics background: Add analogies, real-world examples
- If Urdu preferred: Translate content (keep technical terms in English)

Original Content:
{original_content}

Output the personalized content in Markdown format.
"""
```

### 5. Frontend Tab Component Architecture

**Decision**: Docusaurus Tabs component with lazy-loaded personalized content

**Rationale**:
- Docusaurus has built-in Tabs component
- Lazy loading avoids unnecessary API calls
- React Query for caching and loading states

**Alternatives Considered**:
- Custom tabs: More work, less consistent
- Pre-load both tabs: Wastes API calls
- Server-side rendering: Complex for personalized content

**Best Practices**:
```tsx
// Use Docusaurus Tabs
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

// Lazy load personalized content
const PersonalizedContent = lazy(() => import('./PersonalizedContent'));
```

## NEEDS CLARIFICATION Resolved

| Item | Resolution |
|------|------------|
| ORM choice | SQLAlchemy 2.0 async (not Drizzle) |
| Auth approach | Skip for MVP, use localStorage user_id |
| Caching granularity | Per-user, per-lesson, per-content-hash |
| Personalization timing | On-demand (not pre-generated) |

## References

- [SQLAlchemy 2.0 Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [NeonDB Connection Guide](https://neon.tech/docs/connect/connect-from-any-app)
- [Alembic Async Support](https://alembic.sqlalchemy.org/en/latest/cookbook.html#using-asyncio-with-alembic)
- [Docusaurus Tabs](https://docusaurus.io/docs/markdown-features/tabs)
