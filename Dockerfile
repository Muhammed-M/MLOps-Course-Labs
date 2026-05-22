# Use an official Python runtime as base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1

# Install uv (fast Python package installer)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory inside container
WORKDIR /app

# Copy dependency files first (for better layer caching)
COPY pyproject.toml uv.lock ./

# Install dependencies (production only, no dev packages)
RUN uv sync --no-dev --frozen

# Copy the rest of the application
COPY app/ ./app/
COPY main.py .
COPY data/pipeline.joblib ./data/pipeline.joblib

# Expose the port Litestar will run on
EXPOSE 8000

# Command to run the API
CMD ["uv", "run", "litestar", "--app", "main:app", "run", "--host", "0.0.0.0", "--port", "8000"]