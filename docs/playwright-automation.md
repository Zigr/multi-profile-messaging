# Thread Summary: Playwright Automation

## Table of Contents

- [Thread Summary: Playwright Automation](#thread-summary-playwright-automation)
  - [Table of Contents](#table-of-contents)
    - [Overview](#overview)
    - [Goals](#goals)
    - [Proposed folder/file structure](#proposed-folderfile-structure)
    - [Pending Decisions \& Next Steps](#pending-decisions--next-steps)
    - [Status Legend](#status-legend)
    - [Current Status](#current-status)

### Overview

This thread is dedicated to exploring and implementing automation features using **Playwright**. The focus is on browser-driven automation for capturing session cookies, simulating user workflows, and integrating results back into the backend system.

### Goals

- Establish a **generic cookie capture** mechanism using Playwright.
- Define patterns for **automation scripts** (headless vs. interactive).
- Provide a **safe storage and retrieval flow** of cookies and session data for use in campaigns.
- Explore **integration with worker endpoints** to manage and trigger automation tasks.
- Deploy as a **Docker service**

### Proposed folder/file structure

```text
multi-profile-messaging/
├─ backend/
│  ├─ connectors/
│  │  └─ playwright_automation.py          # (already added earlier)
│  ├─ routers/
│  │  └─ automation.py                     # (API: capture/refresh cookies)
│  └─ tasks/                               # (optional) celery tasks that call automation
│     └─ automation_tasks.py
│
├─ automation/
│  └─ playwright/
│     ├─ scripts/
│     │  ├─ cookie_capture.ts             # interactive login → storage state JSON
│     │  └─ smoke_open.ts                 # simple “open page, print title” sanity test
│     ├─ runners/
│     │  ├─ run-cookie-capture.ts         # CLI wrapper around scripts/*
│     │  └─ run-script.ts                 # generic executor (script by name + args)
│     ├─ config/
│     │  ├─ default.json                  # defaults (headless=false, timeouts, ua)
│     │  └─ profiles.sample.json          # example per-profile overrides (proxy, UA)
│     ├─ storage_states/                  # *.json storage states (gitignored)
│     ├─ logs/                            # playwright traces/videos/logs (gitignored)
│     ├─ tests/
│     │  └─ smoke.spec.ts                 # playwright test that ensures basics work
│     ├─ README.md
│     └─ .env.example                     # PLAYWRIGHT_* vars for CLI runners
│
└─ package.json                            # add npm scripts to run automation

```

### Pending Decisions & Next Steps

- ✅ Create **Proposed folder/file structure** for automation
- ✅ Add/change a **Docker container**
- ✅ Create minimal contents (stubs)
- [ ] Optional: wire a “Run script” endpoint
- [ ] Decide on **where and how to store Playwright-collected cookies** (DB vs. encrypted file).
- [ ] Expose a **backend endpoint** for triggering cookie capture flows.
- [ ] Create a **basic Playwright script** template for repeatable automations.
- [ ] Define **error handling & logging** approach for automation runs.
- [ ] Investigate **scalability options** (queue workers for multiple simultaneous Playwright tasks).

### Status Legend

- ✅ Completed
- ⏳ In Progress
- ∞ Pending / Not Yet Started

### Current Status

- Proposed folder/file structure created → **∞ (incomplete)**
- v0.1.0 minimal contents (stubs) created:

  - automation/playwright/README.md
  - package.json (add scripts)
  - automation/playwright/config/default.json
  - automation/playwright/scripts/cookie_capture.ts
  - automation/playwright/scripts/smoke_open.ts
  - automation/playwright/runners/run-cookie-capture.ts
  - automation/playwright/runners/run-script.ts
  - automation/playwright/tests/smoke.spec.ts

---
This summary will evolve as the **Playwright automation** implementation proceeds.
