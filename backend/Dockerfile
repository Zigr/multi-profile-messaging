# syntax=docker/dockerfile:1.4
# Use official Playwright Python image
FROM mcr.microsoft.com/playwright/python:v1.53.0-noble

WORKDIR /app

# Upgrade pip and install Playwright
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir playwright==1.53

# Install Playwright browsers
RUN playwright install --with-deps chromium

# Install uv
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Place executables in the environment at the front of the path
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#using-the-environment
ENV PATH="/app/.venv/bin:$PATH"
# Compile bytecode
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#compiling-bytecode
ENV UV_COMPILE_BYTECODE=1

# uv Cache
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#caching
ENV UV_LINK_MODE=copy

ENV PYTHONPATH=${PYTHONPATH:-/app}

# Build argument to switch between development and production
ARG MODE=production
ENV MODE=${MODE}

# Install dependencies
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

# Conditional installation
# RUN if [ "$MODE" = "development" ]; then \
# #    echo "$(ls -al) Installing dependencies in editable mode for development..." && \
# #    --mount=type=cache,target=/root/.cache/uv \
#     --mount=type=bind,source=uv.lock,target=uv.lock \
#     --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
#     uv sync --no-install-project; \
#     else \
#     echo "Installing frozen dependencies for production..." && \
#     uv sync --frozen --no-install-project; \
#     fi

# Copy the rest of your application
# COPY . /app/
COPY alembic.ini .
COPY requirements.txt .
COPY src ./src
COPY scripts ./scripts

RUN python -m playwright install --with-deps chromium

# RUN ["uvicorn", "mpm.main:app", "--host", "0.0.0.0" "--port" "8000" "--reload"]
# Default command: runs FastAPI with hot reload in development
# CMD if [ "$MODE" = "development" ]; then \
#     uvicorn mpm.main:app --host 0.0.0.0 --port 8000 --reload; \
#     else \
#     uvicorn mpm.main:app --host 0.0.0.0 --port 8000; \
#     fi
