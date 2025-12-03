"""
RAG (Retrieval Augmented Generation) service for textbook content.

Queries Qdrant vector database to find relevant lesson content
and formats it as context for the tutor agent.
"""

import logging
import os
from typing import Optional

from openai import AsyncOpenAI
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import ScoredPoint

logger = logging.getLogger(__name__)

# Configuration
QDRANT_URL = os.getenv(
    "QDRANT_URL",
    "https://9a320340-74d2-44b6-bab7-1d66dd10790f.us-west-1-0.aws.cloud.qdrant.io:6333"
)
QDRANT_API_KEY = os.getenv(
    "QDRANT_API_KEY",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.iJUTBXlGpJcUB3sFb4E9us5N3mWd2B7Bz70I1Qkkzlo"
)
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION", "books_lessons")
EMBEDDING_MODEL = "text-embedding-3-small"

# Singleton clients
_qdrant_client: Optional[AsyncQdrantClient] = None
_openai_client: Optional[AsyncOpenAI] = None


def get_qdrant_client() -> AsyncQdrantClient:
    """Get or create the Qdrant async client."""
    global _qdrant_client
    if _qdrant_client is None:
        _qdrant_client = AsyncQdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
        )
    return _qdrant_client


def get_openai_client() -> AsyncOpenAI:
    """Get or create the OpenAI async client."""
    global _openai_client
    if _openai_client is None:
        _openai_client = AsyncOpenAI()
    return _openai_client


async def embed_query(query: str) -> list[float]:
    """
    Generate embedding for a search query.

    Args:
        query: The user's question or search text

    Returns:
        1536-dimensional embedding vector
    """
    client = get_openai_client()
    response = await client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=query,
    )
    return response.data[0].embedding


async def search_lessons(
    query: str,
    top_k: int = 3,
    score_threshold: float = 0.5
) -> list[ScoredPoint]:
    """
    Search for relevant lesson content.

    Args:
        query: The user's question
        top_k: Number of results to return
        score_threshold: Minimum similarity score (0-1)

    Returns:
        List of scored points with metadata
    """
    try:
        # Generate query embedding
        query_embedding = await embed_query(query)

        # Search Qdrant
        qdrant = get_qdrant_client()
        results = await qdrant.query_points(
            collection_name=COLLECTION_NAME,
            query=query_embedding,
            limit=top_k,
            score_threshold=score_threshold,
        )
        results = results.points

        logger.info(f"RAG search for '{query[:50]}...' found {len(results)} results")
        return results

    except Exception as e:
        logger.error(f"RAG search error: {e}")
        return []


def file_path_to_url(file_path: str) -> str:
    """
    Convert a file path to a docs URL.

    Example: "01-Physical-AI-Foundations/01-what-is-physical-ai/02-lesson-embodiment-hypothesis.md"
          -> "/docs/01-Physical-AI-Foundations/01-what-is-physical-ai/02-lesson-embodiment-hypothesis"
    """
    # Remove .md extension
    url_path = file_path.replace(".md", "")
    # Handle index.md -> just the directory
    if url_path.endswith("/index"):
        url_path = url_path[:-6]
    return f"/docs/{url_path}"


def format_context(results: list[ScoredPoint]) -> tuple[str, list[dict]]:
    """
    Format search results as context for the tutor.

    Args:
        results: List of scored points from Qdrant

    Returns:
        Tuple of (formatted context string, list of references)
    """
    if not results:
        return "", []

    context_parts = ["## Relevant Textbook Content\n"]
    references = []

    for i, point in enumerate(results, 1):
        payload = point.payload or {}
        title = payload.get("title", "Untitled")
        content_type = payload.get("content_type", "content")
        part_num = payload.get("part_number", "")
        chapter_num = payload.get("chapter_number", "")
        file_path = payload.get("file_path", "")

        # Build location string
        location = ""
        if part_num:
            location = f"Part {part_num}"
            if chapter_num:
                location += f", Chapter {chapter_num}"

        # Generate URL
        url = file_path_to_url(file_path) if file_path else ""

        context_parts.append(f"### {i}. {title}")
        if location:
            context_parts.append(f"*{location} ({content_type})*")
        if url:
            context_parts.append(f"URL: {url}")
        context_parts.append(f"Score: {point.score:.2f}\n")

        # Add to references list
        references.append({
            "title": title,
            "url": url,
            "location": location,
            "content_type": content_type,
            "score": round(point.score, 2)
        })

    return "\n".join(context_parts), references


async def get_rag_context(query: str) -> tuple[Optional[str], list[dict]]:
    """
    Get RAG context for a user query.

    This is the main entry point for the RAG service.

    Args:
        query: The user's question

    Returns:
        Tuple of (formatted context string or None, list of references)
    """
    results = await search_lessons(query, top_k=3, score_threshold=0.5)

    if not results:
        return None, []

    return format_context(results)


async def close_clients():
    """Close async clients on shutdown."""
    global _qdrant_client, _openai_client

    if _qdrant_client:
        await _qdrant_client.close()
        _qdrant_client = None

    if _openai_client:
        await _openai_client.close()
        _openai_client = None
