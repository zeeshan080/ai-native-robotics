"""
FastAPI application for ChatKit AI Robotics Tutor backend.

Provides:
- POST /chatkit/api - Streaming chat endpoint
- GET /health - Health check endpoint
"""

import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
from datetime import datetime, timezone
from typing import AsyncIterator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse
from pydantic import ValidationError

from .models import ChatRequest, ChatEvent
from .router import handle_chat_request
from .routers.user import router as user_router
from .routers.onboarding import router as onboarding_router
from .routers.personalize import router as personalize_router
from .routers.protected import router as protected_router
from .routers.content import router as content_router
from .routers.progress import router as progress_router


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Create FastAPI app
app = FastAPI(
    title="ChatKit AI Robotics Tutor",
    description="Backend API for the ChatKit AI Robotics Tutor feature",
    version="1.0.0"
)


# Configure CORS
# Reads from CORS_ORIGINS env var, falls back to localhost for development
def get_cors_origins():
    default_origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "https://zeeshan080.github.io",  # GitHub Pages (hardcoded fallback)
        "https://ai-native-robotics.vercel.app",  # Vercel auth (hardcoded fallback)
    ]

    # Add origins from environment variable
    env_origins = os.getenv("CORS_ORIGINS", "")
    if env_origins:
        additional = [o.strip() for o in env_origins.split(",") if o.strip()]
        default_origins.extend(additional)

    # Remove duplicates while preserving order
    seen = set()
    unique_origins = []
    for origin in default_origins:
        if origin not in seen:
            seen.add(origin)
            unique_origins.append(origin)

    logger.info(f"CORS origins configured: {unique_origins}")
    return unique_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
# Note: onboarding_router must be included BEFORE user_router
# because /api/user/preferences must match before /api/user/{user_id}
app.include_router(onboarding_router, prefix="/api")
app.include_router(user_router, prefix="/api")
app.include_router(personalize_router, prefix="/api")
app.include_router(content_router, prefix="/api")
app.include_router(progress_router, prefix="/api")
app.include_router(protected_router)  # Protected routes (has its own prefix)


@app.get("/health")
async def health_check():
    """
    Health check endpoint.

    Returns service status and configuration info.
    """
    provider = os.getenv("LLM_PROVIDER", "openai")

    return {
        "status": "healthy",
        "provider": provider,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


async def event_generator(request: ChatRequest) -> AsyncIterator[dict]:
    """
    Generate SSE events from chat request.

    Args:
        request: Validated ChatRequest

    Yields:
        dict events in SSE format
    """
    async for event in handle_chat_request(request):
        # Convert Pydantic model to dict for SSE
        yield {
            "event": "message",
            "data": event.model_dump_json()
        }


@app.post("/chatkit/api")
async def chatkit_api(request: Request):
    """
    Chat API endpoint with SSE streaming.

    Accepts chat requests and returns streaming responses.
    """
    try:
        # Parse and validate request body
        body = await request.json()
        chat_request = ChatRequest(**body)

        logger.info(f"Received chat request: {chat_request.message.id}")

        # Return SSE response
        return EventSourceResponse(
            event_generator(chat_request),
            media_type="text/event-stream"
        )

    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        return JSONResponse(
            status_code=400,
            content={
                "error": "Invalid request format",
                "details": str(e)
            }
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "details": "An unexpected error occurred"
            }
        )


@app.on_event("startup")
async def startup_event():
    """Log startup information."""
    provider = os.getenv("LLM_PROVIDER", "openai")
    logger.info(f"ChatKit backend starting with provider: {provider}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "chatkit_backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
