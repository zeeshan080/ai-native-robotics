"""
FastAPI application for ChatKit AI Robotics Tutor backend.

Provides:
- POST /chatkit/api - Streaming chat endpoint
- GET /health - Health check endpoint
"""

import os
import logging
import ipaddress
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
from datetime import datetime, timezone
from typing import AsyncIterator, Optional

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse
from pydantic import ValidationError

from .models import ChatRequest, ChatEvent
from .router import handle_chat_request
from .db.database import get_db_session
from .services.rate_limit_service import RateLimitService, ANONYMOUS_MESSAGE_LIMIT
from .routers.user import router as user_router
from .routers.onboarding import router as onboarding_router
from .routers.personalize import router as personalize_router
from .routers.protected import router as protected_router
from .routers.content import router as content_router
from .routers.progress import router as progress_router
from .routers.threads import router as threads_router


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
app.include_router(threads_router, prefix="/api")  # Thread management routes
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


def validate_ip(ip: str) -> Optional[str]:
    """Validate and normalize an IP address.

    Returns the validated IP string, or None if invalid.
    """
    try:
        # This validates both IPv4 and IPv6
        validated = ipaddress.ip_address(ip.strip())
        return str(validated)
    except ValueError:
        return None


def get_client_ip(request: Request) -> str:
    """Extract and validate client IP address from request headers or connection.

    Handles proxied requests by checking X-Forwarded-For header first.
    Validates IP format to prevent injection attacks.
    """
    # Check for forwarded IP (when behind proxy/load balancer)
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # X-Forwarded-For can contain multiple IPs; first one is the client
        raw_ip = forwarded_for.split(",")[0].strip()
        validated = validate_ip(raw_ip)
        if validated:
            return validated
        logger.warning(f"Invalid IP in X-Forwarded-For header: {raw_ip}")

    # Check X-Real-IP header (common alternative)
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        validated = validate_ip(real_ip)
        if validated:
            return validated
        logger.warning(f"Invalid IP in X-Real-IP header: {real_ip}")

    # Fall back to direct connection IP
    if request.client:
        validated = validate_ip(request.client.host)
        if validated:
            return validated

    return "unknown"


@app.post("/chatkit/api")
async def chatkit_api(request: Request):
    """
    Chat API endpoint with SSE streaming.

    Accepts chat requests and returns streaming responses.
    Enforces rate limiting for anonymous users based on IP address.
    """
    try:
        # Parse and validate request body
        body = await request.json()
        chat_request = ChatRequest(**body)

        logger.info(f"Received chat request: {chat_request.message.id}")

        # Check if this is an anonymous user
        # Frontend sends user_id in context when authenticated via BetterAuth
        user_id = chat_request.context.user_id if chat_request.context else None
        is_anonymous = user_id is None

        if is_anonymous:
            # Get client IP for rate limiting
            client_ip = get_client_ip(request)
            logger.info(f"Anonymous request from IP: {client_ip}")

            # Check rate limit
            async with get_db_session() as session:
                rate_service = RateLimitService(session)
                allowed, remaining = await rate_service.check_limit(client_ip)

                if not allowed:
                    logger.warning(f"Rate limit exceeded for IP: {client_ip}")
                    return JSONResponse(
                        status_code=429,
                        content={
                            "error": "Rate limit exceeded",
                            "message": f"You have reached the {ANONYMOUS_MESSAGE_LIMIT} message limit for anonymous users. Please sign up to continue.",
                            "limit": ANONYMOUS_MESSAGE_LIMIT,
                            "remaining": 0,
                        },
                        headers={
                            "X-RateLimit-Limit": str(ANONYMOUS_MESSAGE_LIMIT),
                            "X-RateLimit-Remaining": "0",
                        }
                    )

                # Increment the counter BEFORE processing (to prevent race conditions)
                new_count, remaining = await rate_service.increment(client_ip)
                logger.info(f"IP {client_ip}: message {new_count}/{ANONYMOUS_MESSAGE_LIMIT}, remaining: {remaining}")

        # Return SSE response with rate limit headers
        response = EventSourceResponse(
            event_generator(chat_request),
            media_type="text/event-stream"
        )

        # Add rate limit headers to response if anonymous
        if is_anonymous:
            response.headers["X-RateLimit-Limit"] = str(ANONYMOUS_MESSAGE_LIMIT)
            response.headers["X-RateLimit-Remaining"] = str(remaining)

        return response

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
