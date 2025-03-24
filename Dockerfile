# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/engine/reference/builder/

ARG PYTHON_VERSION=3.11.5
FROM python:${PYTHON_VERSION}-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry==$POETRY_VERSION

# Copy project files
COPY pyproject.toml poetry.lock /app/

# Install dependencies
RUN poetry install --no-root --no-dev

# Copy application source code
COPY . /app

# Expose the FastAPI port
EXPOSE 8000

# Command to run the application
CMD ["poetry", "run", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
