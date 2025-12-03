# Quickstart: Content Personalization

**Feature**: 005-content-personalization
**Date**: 2025-11-30

## Prerequisites

- Python 3.11+
- Node.js 20+
- pnpm 10+
- NeonDB account (free tier works)
- OpenAI or Gemini API key

## Setup Steps

### 1. Backend Database Setup

```bash
# Navigate to backend package
cd packages/chatkit-backend

# Add dependencies (already in pyproject.toml after implementation)
uv add sqlalchemy[asyncio] asyncpg alembic

# Create .env with database URL
cat >> .env << 'EOF'
DATABASE_URL=postgresql+asyncpg://user:pass@ep-xxx.region.aws.neon.tech/dbname?sslmode=require
EOF
```

### 2. Get NeonDB Connection String

1. Go to [console.neon.tech](https://console.neon.tech)
2. Create a new project (or use existing)
3. Copy connection string from Dashboard
4. Replace `postgresql://` with `postgresql+asyncpg://`
5. Add `?sslmode=require` at the end

### 3. Run Database Migrations

```bash
# Initialize alembic (if not done)
alembic init alembic

# Run migrations
alembic upgrade head
```

### 4. Start Backend Server

```bash
# From packages/chatkit-backend
uv run uvicorn chatkit_backend.main:app --reload --port 8000
```

### 5. Test API Endpoints

```bash
# Create a user
curl -X POST http://localhost:8000/api/user/create \
  -H "Content-Type: application/json" \
  -d '{"user_id": "550e8400-e29b-41d4-a716-446655440000"}'

# Submit onboarding
curl -X POST http://localhost:8000/api/onboarding \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "education_level": "undergraduate",
    "programming_experience": "intermediate",
    "robotics_background": false,
    "ai_ml_experience": "basic",
    "learning_goals": ["career_change", "building_projects"],
    "preferred_language": "en"
  }'

# Get preferences
curl http://localhost:8000/api/user/preferences \
  -H "X-User-ID: 550e8400-e29b-41d4-a716-446655440000"

# Generate personalized content
curl -X POST http://localhost:8000/api/personalize \
  -H "Content-Type: application/json" \
  -H "X-User-ID: 550e8400-e29b-41d4-a716-446655440000" \
  -d '{
    "lesson_slug": "01-intro/embodiment",
    "original_content": "# The Embodiment Hypothesis\n\nPhysical AI requires robots to interact with the real world..."
  }'
```

### 6. Frontend Setup

```bash
# From repository root
cd apps/docs

# Start development server
pnpm dev
```

### 7. Test End-to-End Flow

1. Open http://localhost:3000 in a new incognito window
2. You should be redirected to /onboarding
3. Complete the 6-question questionnaire
4. Navigate to any lesson
5. Click the "Personalized" tab
6. See personalized content based on your profile

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | NeonDB connection string | `postgresql+asyncpg://user:pass@ep-xxx.neon.tech/db?sslmode=require` |
| `GEMINI_API_KEY` | Gemini API key for personalization | `AIza...` |
| `OPENAI_API_KEY` | OpenAI API key (alternative) | `sk-...` |

## Troubleshooting

### "Connection refused" errors
- Ensure NeonDB project is active (not suspended)
- Check connection string format includes `postgresql+asyncpg://`

### "Module not found" errors
- Run `uv sync` in packages/chatkit-backend
- Ensure Python 3.11+ is being used

### Personalization returns empty content
- Check LLM API key is set
- Verify user has completed onboarding
- Check backend logs for API errors

### Cache not working
- Verify content_hash changes when original content changes
- Check preferences_hash changes when preferences update

## API Quick Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/user/create` | POST | Create anonymous user |
| `/api/user/{id}` | GET | Get user info |
| `/api/onboarding` | POST | Submit questionnaire |
| `/api/user/preferences` | GET | Get preferences |
| `/api/user/preferences` | PUT | Update preferences |
| `/api/personalize` | POST | Generate personalized content |
| `/api/personalize/cache` | DELETE | Clear user's cache |
