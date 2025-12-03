# ChatKit Backend Dockerfile for Render.com deployment
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml .
COPY README.md .
COPY src/ src/
COPY alembic/ alembic/
COPY alembic.ini .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install .

# Expose port (Render uses 10000 by default)
EXPOSE 10000

# Run database migrations and start the server
CMD alembic upgrade head && uvicorn chatkit_backend.main:app --host 0.0.0.0 --port ${PORT:-10000}
