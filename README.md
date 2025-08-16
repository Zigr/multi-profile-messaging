# Multi-profile-messaging

## Setup

1. Copy `.env.example` to `.env` and fill in values.
2. Run: `COMPOSE_BAKE=true docker compose watch docker-compose up --build`
3. [Backend: http://localhost:8000](http://localhost:8000)
4. [Frontend: http://localhost:3000](http://localhost:3000)
5. [MailCatcher UI: http://localhost:1080](http://localhost:1080)

## Migrations

### Manually export database Url

```bash
export DATABASE_URL="sqlite:///./mpm.sqlite"
alembic revision --autogenerate -m "create initial tables"

```

### Or use .env file

```bash
alembic revision --autogenerate -m "describe change"
alembic upgrade head

```

## Running locally

```Bash
docker-compose up --build
# FastAPI on http://localhost:8000
# MailCatcher SMTP → localhost:1025, UI → localhost:1080
# Redis → localhost:6379, Celery workers auto-attached

```

---
