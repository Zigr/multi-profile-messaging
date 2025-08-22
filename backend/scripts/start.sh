#!/bin/bash
set -e

# Run Alembic migrations
alembic -c alembic.ini upgrade head

# Start FastAPI with hot reload
uvicorn mpm.main:app --host 0.0.0.0 --port 8000 --reload
