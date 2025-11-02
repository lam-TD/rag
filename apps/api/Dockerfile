FROM ghcr.io/astral-sh/uv:latest AS uv-bin

FROM python:3.12-slim

# Provide uv binaries without requiring BuildKit-only copy syntax.
COPY --from=uv-bin /uv /usr/local/bin/uv
COPY --from=uv-bin /uvx /usr/local/bin/uvx

WORKDIR /api

# Copy dependency manifests first for better build caching.
COPY pyproject.toml ./
RUN uv sync

# Copy the application source after dependencies are installed.
COPY app ./app


CMD ["/api/.venv/bin/uvicorn", "app.main:app", "--port", "8000", "--host", "0.0.0.0", "--reload"]
