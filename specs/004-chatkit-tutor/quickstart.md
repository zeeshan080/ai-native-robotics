# Quickstart: ChatKit AI Robotics Tutor

**Feature**: 004-chatkit-tutor
**Date**: 2025-11-29

This guide helps developers get the ChatKit feature running locally for development.

---

## Prerequisites

- Node.js 20+ and pnpm 10+
- Python 3.11+ and uv
- OpenAI API key (or Gemini API key)
- Git

---

## 1. Clone and Setup

```bash
# Clone the repository (if not already)
git clone <repo-url>
cd ai-native-robotics

# Checkout the feature branch
git checkout 004-chatkit-tutor

# Install frontend dependencies
pnpm install
```

---

## 2. Backend Setup

### Create the package structure

```bash
# Navigate to packages directory
cd packages

# Create chatkit-backend package
mkdir -p chatkit-backend/src/chatkit_backend/agents
mkdir -p chatkit-backend/src/chatkit_backend/models
mkdir -p chatkit-backend/tests
```

### Initialize Python environment

```bash
cd chatkit-backend

# Create pyproject.toml (will be created by implementation)
# Initialize uv environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install fastapi uvicorn openai openai-agents pydantic python-dotenv sse-starlette
```

### Configure environment

```bash
# Create .env file
cat > .env << 'EOF'
# LLM Provider: "openai" or "gemini"
LLM_PROVIDER=openai

# OpenAI Configuration
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_DEFAULT_MODEL=gpt-4o-mini

# Gemini Configuration (alternative)
# GEMINI_API_KEY=your-gemini-key
# GEMINI_DEFAULT_MODEL=gemini-2.0-flash
EOF
```

### Run the backend

```bash
# From packages/chatkit-backend
uvicorn src.chatkit_backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Verify**: Open http://localhost:8000/health - should return `{"status": "healthy"}`

---

## 3. Frontend Setup

### Configure API URL

```bash
# From repository root
cd apps/docs

# Create .env.local for local development
echo "CHATKIT_API_URL=http://localhost:8000" > .env.local
```

### Run the docs site

```bash
# From apps/docs (or use turbo from root)
pnpm dev
```

**Verify**: Open http://localhost:3000 - should see docs site with chat bar at bottom

---

## 4. Test the Integration

1. Open any lesson page in the docs
2. Click the "Ask a question..." input at bottom-center
3. Type: "What is Physical AI?"
4. Press Enter or click send
5. Verify streaming response appears

---

## Development Workflow

### Backend Changes

```bash
# Terminal 1: Run backend with auto-reload
cd packages/chatkit-backend
uvicorn src.chatkit_backend.main:app --reload

# Terminal 2: Run tests
cd packages/chatkit-backend
uv pip install pytest httpx pytest-asyncio
pytest tests/
```

### Frontend Changes

```bash
# Terminal: Run docs with hot reload
cd apps/docs
pnpm dev

# Changes to src/components/ChatKit/* auto-reload
```

### Full Stack Testing

```bash
# From repository root
# Terminal 1: Backend
cd packages/chatkit-backend && uvicorn src.chatkit_backend.main:app --reload

# Terminal 2: Frontend
cd apps/docs && pnpm dev

# Terminal 3: Curl test
curl -X POST http://localhost:8000/chatkit/api \
  -H "Content-Type: application/json" \
  -d '{"type":"user_message","message":{"id":"test-123","content":"Hello"}}'
```

---

## Troubleshooting

### Backend won't start

```bash
# Check Python version
python --version  # Should be 3.11+

# Check dependencies installed
uv pip list | grep fastapi

# Check .env file exists
cat packages/chatkit-backend/.env
```

### CORS errors in browser

- Ensure backend is running on port 8000
- Check browser console for specific CORS error
- Verify CORS middleware is configured in main.py

### Chat not responding

```bash
# Test backend directly
curl http://localhost:8000/health

# Check backend logs for errors
# Look for API key issues, provider errors

# Verify LLM_PROVIDER and API key match
```

### Streaming not working

- Check browser supports EventSource (all modern browsers do)
- Look for SSE-specific errors in network tab
- Verify response Content-Type is `text/event-stream`

---

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `LLM_PROVIDER` | No | `openai` | LLM provider: "openai" or "gemini" |
| `OPENAI_API_KEY` | If OpenAI | - | OpenAI API key |
| `OPENAI_DEFAULT_MODEL` | No | `gpt-4o-mini` | OpenAI model to use |
| `GEMINI_API_KEY` | If Gemini | - | Google AI API key |
| `GEMINI_DEFAULT_MODEL` | No | `gemini-2.0-flash` | Gemini model to use |
| `CHATKIT_API_URL` | Frontend | `http://localhost:8000` | Backend API URL |

---

## Next Steps

After quickstart setup:

1. Run `/sp.tasks` to generate implementation tasks
2. Implement backend following tasks.md
3. Implement frontend components
4. Test end-to-end flow
5. Deploy (documentation TBD)
