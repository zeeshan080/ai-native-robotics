#!/usr/bin/env python3
"""
Index all lesson content into Qdrant for RAG.

This script reads all markdown files from the docs directory,
generates embeddings using OpenAI, and upserts them to Qdrant Cloud.
"""

import os
import re
import hashlib
from pathlib import Path
from typing import Optional
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from openai import OpenAI

# Configuration
QDRANT_URL = "https://9a320340-74d2-44b6-bab7-1d66dd10790f.us-west-1-0.aws.cloud.qdrant.io:6333"
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.iJUTBXlGpJcUB3sFb4E9us5N3mWd2B7Bz70I1Qkkzlo"
COLLECTION_NAME = "books_lessons"
DOCS_DIR = Path(__file__).parent.parent.parent.parent / "apps" / "docs" / "docs"
EMBEDDING_MODEL = "text-embedding-3-small"


def extract_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown."""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return {}

    frontmatter = {}
    for line in match.group(1).split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip().strip('"\'')
    return frontmatter


def extract_content_summary(content: str, max_chars: int = 4000) -> str:
    """Extract key content for embedding, removing code blocks and excess whitespace."""
    # Remove frontmatter
    content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)

    # Remove code blocks
    content = re.sub(r'```[\s\S]*?```', '', content)

    # Remove inline code
    content = re.sub(r'`[^`]+`', '', content)

    # Remove HTML tags
    content = re.sub(r'<[^>]+>', '', content)

    # Remove image/link references
    content = re.sub(r'!\[.*?\]\(.*?\)', '', content)
    content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)

    # Normalize whitespace
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = re.sub(r' {2,}', ' ', content)

    # Truncate if too long
    if len(content) > max_chars:
        content = content[:max_chars] + "..."

    return content.strip()


def parse_file_path(file_path: Path) -> dict:
    """Extract metadata from file path structure."""
    parts = file_path.relative_to(DOCS_DIR).parts

    metadata = {
        "file_path": str(file_path.relative_to(DOCS_DIR)),
        "filename": file_path.name,
    }

    # Parse part (e.g., "01-Physical-AI-Foundations")
    if len(parts) >= 1 and parts[0].startswith("0"):
        part_match = re.match(r'^(\d+)-(.+)$', parts[0])
        if part_match:
            metadata["part_number"] = int(part_match.group(1))
            metadata["part_title"] = part_match.group(2).replace("-", " ")

    # Parse chapter (e.g., "01-what-is-physical-ai")
    if len(parts) >= 2 and parts[1].startswith("0"):
        chapter_match = re.match(r'^(\d+)-(.+)$', parts[1])
        if chapter_match:
            metadata["chapter_number"] = int(chapter_match.group(1))
            metadata["chapter_title"] = chapter_match.group(2).replace("-", " ")

    # Parse lesson type from filename
    if "lesson" in file_path.name.lower():
        metadata["content_type"] = "lesson"
        lesson_match = re.match(r'^(\d+)-lesson-(.+)\.md$', file_path.name)
        if lesson_match:
            metadata["lesson_number"] = int(lesson_match.group(1))
            metadata["lesson_slug"] = lesson_match.group(2)
    elif "lab" in file_path.name.lower():
        metadata["content_type"] = "lab"
    elif "summary" in file_path.name.lower():
        metadata["content_type"] = "summary"
    elif file_path.name == "index.md":
        metadata["content_type"] = "index"
    else:
        metadata["content_type"] = "other"

    return metadata


def generate_doc_id(file_path: Path) -> str:
    """Generate a unique ID for a document."""
    rel_path = str(file_path.relative_to(DOCS_DIR))
    return hashlib.md5(rel_path.encode()).hexdigest()[:16]


def main():
    print("Initializing clients...")
    openai_client = OpenAI()
    qdrant_client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
    )

    # Find all markdown files
    md_files = list(DOCS_DIR.rglob("*.md"))
    print(f"Found {len(md_files)} markdown files")

    points = []
    texts_to_embed = []

    for file_path in md_files:
        print(f"Processing: {file_path.relative_to(DOCS_DIR)}")

        content = file_path.read_text(encoding="utf-8")
        frontmatter = extract_frontmatter(content)
        summary = extract_content_summary(content)
        metadata = parse_file_path(file_path)

        # Add frontmatter title if available
        if "title" in frontmatter:
            metadata["title"] = frontmatter["title"]

        # Create text for embedding (title + content)
        embed_text = f"{metadata.get('title', metadata['filename'])}\n\n{summary}"
        texts_to_embed.append(embed_text)

        # Store metadata for later
        points.append({
            "id": generate_doc_id(file_path),
            "metadata": metadata,
        })

    # Generate embeddings in batch
    print(f"\nGenerating embeddings for {len(texts_to_embed)} documents...")
    response = openai_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts_to_embed,
    )

    # Create Qdrant points
    qdrant_points = []
    for i, (point_data, embedding_data) in enumerate(zip(points, response.data)):
        qdrant_points.append(
            PointStruct(
                id=point_data["id"],
                vector=embedding_data.embedding,
                payload=point_data["metadata"],
            )
        )

    # Upsert to Qdrant
    print(f"\nUpserting {len(qdrant_points)} points to Qdrant...")
    qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
        points=qdrant_points,
    )

    print("\nIndexing complete!")
    print(f"  - Collection: {COLLECTION_NAME}")
    print(f"  - Documents indexed: {len(qdrant_points)}")

    # Verify
    collection_info = qdrant_client.get_collection(COLLECTION_NAME)
    print(f"  - Total points in collection: {collection_info.points_count}")


if __name__ == "__main__":
    main()
