# ChatKit Backend - AI Robotics Tutor

FastAPI backend for the ChatKit AI Robotics Tutor feature, using the OpenAI Agents SDK.

## Features

- Streaming chat responses via Server-Sent Events (SSE)
- Support for OpenAI and Gemini (via OpenAI-compatible API)
- Educational AI tutor specialized in robotics and Physical AI
- Context-aware responses (page URL/title)
- Action prefix handling (Explain, Translate, Summarize)

## Setup

### 1. Install Dependencies

Using `uv` (recommended):

```bash
cd packages/chatkit-backend
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

### 2. Configure Environment

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# LLM Provider: "openai" or "gemini"
LLM_PROVIDER=openai

# API Keys (provide the one matching your provider)
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...

# Model Selection (optional, uses defaults if not set)
OPENAI_DEFAULT_MODEL=gpt-4o-mini
GEMINI_DEFAULT_MODEL=gemini-2.0-flash-exp
```

## Running the Server

### Development Mode (with auto-reload)

```bash
uvicorn chatkit_backend.main:app --reload --port 8000
```

Or using the main module:

```bash
python -m chatkit_backend.main
```

### Production Mode

```bash
uvicorn chatkit_backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### POST /chatkit/api

Chat endpoint with SSE streaming.

**Request:**
```json
{
  "type": "user_message",
  "message": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "content": "What is bipedal locomotion?"
  },
  "context": {
    "pageUrl": "/docs/Physical-AI-Foundations/lesson-embodiment",
    "pageTitle": "The Embodiment Hypothesis"
  }
}
```

**Response (SSE stream):**
```
data: {"type":"text_delta","content":"Bipedal","done":false,"messageId":"..."}

data: {"type":"text_delta","content":" locomotion","done":false,"messageId":"..."}

data: {"type":"message_complete","done":true,"messageId":"..."}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "provider": "openai",
  "timestamp": "2025-11-30T12:00:00Z"
}
```

## Project Structure

```
src/chatkit_backend/
├── __init__.py          # Package exports
├── main.py              # FastAPI app and endpoints
├── router.py            # Event routing and streaming logic
├── models/              # Pydantic models
│   ├── __init__.py
│   └── messages.py      # Message, Event, Request models
└── agents/              # Agent definitions
    ├── __init__.py
    ├── factory.py       # LLM provider factory
    └── tutor.py         # Robotics tutor agent
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                      │
│                                                          │
│   POST /chatkit/api                                      │
│   { message: "What is ROS 2?" }                         │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│               FastAPI Backend (main.py)                  │
│                                                          │
│   1. Validate ChatRequest (Pydantic)                     │
│   2. Route to handle_chat_request()                      │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│             Router (router.py)                           │
│                                                          │
│   1. Get tutor agent (singleton)                         │
│   2. Run Runner.run_streamed()                           │
│   3. Convert chunks to ChatEvent                         │
│   4. Yield SSE events                                    │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│            Tutor Agent (tutor.py)                        │
│                                                          │
│   - Educational instructions                             │
│   - Uses create_model() for LLM                          │
│   - Handles action prefixes                              │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│         LLM Provider (factory.py)                        │
│                                                          │
│   - OpenAI or Gemini                                     │
│   - Environment-based selection                          │
└──────────────────────────────────────────────────────────┘
```

## Testing

Run tests:

```bash
pytest tests/
```

Test with coverage:

```bash
pytest --cov=chatkit_backend tests/
```

## Error Handling

The backend handles errors gracefully:

- **Validation errors** (400): Invalid request format
- **Provider errors** (500): API key missing, rate limits, etc.
- **Runtime errors** (500): Unexpected failures

All errors yield user-friendly messages to the frontend:

```json
{
  "type": "error",
  "content": "Sorry, I encountered an error. Please try again.",
  "done": true,
  "messageId": "..."
}
```

## Action Prefixes

The tutor agent recognizes these prefixes in user messages:

- **"Explain: [text]"** - Detailed explanation of a concept
- **"Translate to Urdu: [text]"** - Translation to Urdu
- **"Summarize: [text]"** - Concise summary

Example:
```json
{
  "message": {
    "content": "Explain: The embodiment hypothesis proposes that intelligence emerges from the interaction between a body and its environment"
  }
}
```

## Switching LLM Providers

### Use OpenAI (Default)

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

### Use Gemini

```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=...
```

No code changes required. The factory handles provider selection automatically.

## Security Notes

- Never commit `.env` file
- API keys are server-side only (never sent to frontend)
- CORS is configured for localhost (update for production)
- Use HTTPS in production
- Consider rate limiting for production deployments

## Troubleshooting

### "OPENAI_API_KEY is required" error

Set the API key in `.env`:
```env
OPENAI_API_KEY=sk-your-key-here
```

### No response from agent

Check logs for errors:
```bash
uvicorn chatkit_backend.main:app --log-level debug
```

### CORS errors in browser

Add your frontend domain to `allow_origins` in `main.py`:
```python
allow_origins=["http://localhost:3000", "https://yoursite.com"]
```

## License

Part of the AI-Native Robotics Textbook project.
