# Shared image for the Python services (Data API + Dagster).
# Built on the same uv-managed, 3.12-pinned environment as local dev.
FROM python:3.12-slim

# uv, copied from its official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1

WORKDIR /app

# install dependencies first so this layer caches across code changes
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

# application code
COPY services ./services
COPY pipeline ./pipeline

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000
# default command; compose overrides per service
CMD ["uvicorn", "services.api.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
