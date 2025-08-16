# Multi-Profile Messaging — Live Documentation

> _This document is updated as we progress through each development thread/day._

## 1. Overview  

A web-based tool for sending templated messages (Telegram & Email) from multiple profiles, with humanized delays, list management, proxies, and pluggable connectors.

## 2. Architecture

- **Backend**: FastAPI + SQLAlchemy + Alembic + Celery (Redis)  
- **Frontend**: React + ChakraUI  
- **Workers**: Celery tasks for send-jobs, rate-limiting, retries  
- **DB**: SQLite (dev) / PostgreSQL (prod)  
- **Docs**: OpenAPI/Swagger at `/docs`  

## 3. Environment Setup

- Copy `.env.example` → `.env`  
- Set `DATABASE_URL`, `USE_MAILCATCHER`, SMTP creds, Redis URL, etc.  
- `$ python3.12 -m venv .venv && source .venv/bin/activate`  
- `pip install -r requirements.txt`
- `alembic upgrade head`

## 4. Running Locally

**Create and start containers

```bash
docker-compose up --build

```

**Now

- FastAPI on <http://localhost:8000>
- MailCatcher SMTP → localhost:1025, UI → localhost:1080
- Redis → localhost:6379, Celery workers auto-attached

**Stop and remove containers, networks:

```bash
docker compose stop --remove-orphans
```

## 5. API Endpoints

- **Auth**

  - `POST /api/telegram/login` → returns cookies JSON
- **Email Test**

  - `POST /api/test-email` → sends a single email
- **Profiles**

  - `GET/POST/PUT/DELETE /profiles`
- **Templates**

  - `GET/POST/PUT/DELETE /templates`
  - `POST /templates/preview` (renders with Jinja2)
- **Lists**

  - `GET/POST/DELETE /lists`
- **Logs**

  - `GET /logs`
- **Worker Control**

  - (TBD) endpoints to start/stop campaigns

## 6. Connector Details

- **SMTPConnector**: SSL port 465 (Gmail) or MailCatcher mode
- **PlaywrightAuth**: headless login stub for Telegram

## 7. Worker & Rate-Limit

- **Celery_- tasks live in `backend/tasks.py`
- Concurrency: `celery -A tasks worker --concurrency=4`
- Rate-limit per profile: `@task(rate_limit="1/3.6s")`

## 8. Roadmap & Thread Distribution

| Day | Thread Name              | Scope                                                                                      | Status |
| --- | ------------------------ | ------------------------------------------------------------------------------------------ | ------ |
| 1–2 | **Setup**                | Repo scaffold, Docker/CI, `database.py`, Alembic init & first migration                    | [x]    |
| 3–4 | **Auth & Profiles**      | Playwright login, Telegram connector stub, Profile CRUD endpoints & UI                     | [⧜]    |
| 5   | **Email & MailCatcher**  | SMTPConnector (Gmail + MailCatcher toggle), test-email endpoint, front-end toggle          | [⧜]    |
| 6   | **Templating & Workers** | Jinja2 integration, preview endpoint, Celery + Redis scaffold, rate-limit setup            | [  ]   |
| 7   | **Lists & Proxies**      | Whitelist/blacklist logic, proxy injection in tasks, ListEntry CRUD                        | [  ]   |
| 8   | **Logging & Dashboard**  | LogEntry CRUD, Logs API, Campaign dashboard stub in React                                  | [  ]   |
| 9   | **UI Polish & Tests**    | Build React pages for Templates/Lists/Logs, add E2E + pytest suites                        | [  ]   |
| 10  | **Docs & QA**            | Finalize README, LIVE\_DOC.md, developer guide, deployment scripts, 14-day support kickoff | [  ]   |

> **Legend**:
>
> - **Thread** = a self-contained area of work.
> - **Day** = calendar day in our 10-day timeline.
> - **⧜** = incomplete status, see [Changelog](#9-changelog)

## 9. Changelog

- *2025-07-31_: Initialized with Setup, Auth & Profiles, Email threads.

[ ] **UI** Change React+Javascript → React@18+Typescript
[ ] **UI** Use Vite for UI toolchain
[ ] **UI** Use Tanstack Router for frontend application
[ ] **SMTP Setting** CRUD UI
[ ] **Auth & Profiles** Profile resource CRUD UI
[ ] **Email & MailCatcher** frontend toggle
[ ] **Worker Control** - Endpoints to start/stop campaigns

## 10. How to Contribute

1. Pick a thread from the “Roadmap & Thread Distribution” above.
2. Branch off `feature/<thread>-day<N>`.
3. Update **LIVE\_DOC.md** with your status before opening a PR.
4. Tag PR with the day and thread name.(Example feature/)

## 11 References / Links

- [GitHub repo:](https://github.com/Zigr/multi-profile-messaging/tree/master)
- ChatGPT sessions: "Message automation tool"

---

### How to use this

1. **Commit `LIVE_DOC.md`** at the root of your monorepo.
2. At the start of each day, update the “Roadmap & Thread Distribution” row for that day (e.g. mark it in progress or done).
3. Under **Changelog**, append a line with date and summary of completed threads.

This gives everyone on the project a single “source of truth” that evolves in lockstep with your commits.

Let me know if you’d like tweaks to the sections or the thread naming!
::contentReference[oaicite:0]{index=0}
