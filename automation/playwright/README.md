# Playwright Automation

## What this contains

- `scripts/`  reusable automation bits (cookie capture, smoke open)
- `runners/`  small CLIs wrapping scripts (node/ts-node)
- `config/`   defaults & optional per-profile overrides
- `storage_states/` browser storage (cookies+localStorage) JSON
- `tests/`    playwright test(s) to sanity-check the toolchain

## Quick start

1. `npm i` (from repo root) – ensure devDeps include playwright & ts-node
2. `npx playwright install --with-deps chromium`
3. Run a smoke test:
