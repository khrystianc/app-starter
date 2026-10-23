# Project rules for Claude Code

## Stack
- Python 3.12, Flask app factory (`app/__init__.py` -> `create_app()`), blueprints in `app/`
- Postgres via `DATABASE_URL` (dev container provides one; Render provides one in production)
- Tests: pytest in `tests/`. Lint: ruff.
- Hosting: Render, defined in `render.yaml`. CI: `.github/workflows/tests.yml`.

## Commands
- Run locally: `python run.py` (port 5000)
- Test: `pytest -q`
- Lint: `ruff check .` (auto-fix: `ruff check . --fix`)

## How I work
- Start every new feature with a short plan in plain English and wait for my OK.
- Work on a branch, never directly on main. Open a PR with `gh pr create` when done.
- Explain changes in plain English first, then the technical details.
- I revise your drafts in my own voice, so keep code readable over clever.

## Code rules
- Comment code well: a docstring on every module and non-trivial function.
- Keep the file structure flat and easy to review.
- Every route gets at least one test. Tests never hit the real network:
  mock Anthropic, Stripe, and all third-party APIs.
- All secrets and settings come from env vars via `app.config`. Never hardcode keys.
- Never read, print, or commit `.env`.
- If a required API key is missing, fail closed with a clear error, never crash.
- Keep `/health` fast and dependency-free. Render uses it to gate deploys.
- Bind to `0.0.0.0` and Render's `$PORT` (already set in `render.yaml`).
- When adding a dependency, add it to `requirements.txt` (runtime) or
  `requirements-dev.txt` (test/lint only).
