# Copilot / AI Agent Instructions for Nova

This file contains concise, actionable guidance for AI coding agents working in the Nova repository. Focus on discoverable patterns, workflows, and concrete code examples so an agent can be productive immediately.

1. Big-picture architecture
- **API**: The FastAPI entrypoint is `app/main.py`. It configures logging first, then loads `app.config.settings` and includes routers (e.g. `app.routers.core`). Use `uvicorn app.main:app` to run in dev.
- **Routing**: Add route groups under `app/routers/*` and include them in `main.py` via `app.include_router(...)`.
- **Models / Responses**: All responses use Pydantic wrappers defined in `app/models/base.py`: `BaseResponse`, `ErrorResponse`, and `Meta`. Endpoints should return these shapes rather than raw dicts.
- **Utilities**: `app/utils/meta.py` builds consistent `Meta` metadata for responses; `app/utils/logging_config.py` sets JSON logging and must be configured before importing modules that log.
- **DB layer (Phase 2)**: DB helpers live in `app/db/session.py`. The module lazily loads SQLAlchemy and provides `get_engine()` and a FastAPI-style generator `get_session()` for `Depends`. Note: the DB module is intentionally *not* imported at startup to avoid failing when DB is absent.

2. Settings & environment
- Single settings object: `app/config/settings.py` exposes `settings` (singleton). Precedence: defaults < system env < `.env` file. `.env` (at project root) wins over system env per design.
- Key env vars: `NOVA_ENV`, `NOVA_LOG_LEVEL`, `NOVA_DATABASE_URL` / `DATABASE_URL`, `NOVA_ACTIONS_TOKEN`.
- `version.json` at the project root provides `settings.version` metadata used across endpoints and `app.state.version_info` on startup.

3. Logging and observability
- Logging is JSON-formatted via `app/utils/logging_config.py`. `configure_logging()` is called at top of `app/main.py` so that later imports use the configured handlers.
- Default log directory: `./logs` for dev/test; `/var/log/nova` for prod. Logs are written to `logs/nova.log` with rotation.
- Use `get_logger(name)` to obtain a logger; include structured `extra` fields like `event_type`, `path`, and `status_code` as shown in `main.py` and `core.py`.

4. Error handling and response patterns
- Consistent error shape: always return `ErrorResponse(error=ErrorInfo(...), meta=Meta(...))`. See global Exception handlers in `app/main.py`.
- Use `build_meta()` from `app/utils/meta.py` in handlers for consistent metadata.

5. Security / integration patterns
- Actions handshake: `GET /actions/handshake` is implemented in `app/routers/core.py`. If `NOVA_ACTIONS_TOKEN` is set, expect `X-Nova-Actions-Token` header for authorization.

6. Tests & test conventions
- Tests live in `tests/`. They commonly monkeypatch env vars (`monkeypatch.setenv` / `delenv`) and reset module caches. Example: `tests/test_db_session.py` uses an in-memory SQLite URL (`sqlite:///:memory:`) to avoid requiring Postgres.
- To run tests locally: `pytest -q` (project uses standard pytest conventions). Ensure you run tests from the repository root so relative paths (e.g., `version.json`) resolve.

7. Typical developer workflows (commands)
- Run app locally (dev): `uvicorn app.main:app --reload --port 8000`.
- Run tests: `pytest -q`.
- Linting / formatting: none enforced by repo; prefer `black`/`ruff` if adding tooling.

8. Code patterns to follow when editing
- Always configure logging before importing modules that log (see `main.py` ordering).
- Return `BaseResponse` or `ErrorResponse` Pydantic models from endpoints (avoid returning raw dicts without the wrapper).
- Keep database imports lazy: prefer using `get_session()` dependency rather than importing engine creation at module import time.
- When adding public endpoints, include `meta=build_meta()` and use `get_logger(...)` for consistent structured logs.

9. Files you will reference most often
- `app/main.py` — startup, middleware, exception handlers, root endpoints
- `app/config/settings.py` — environment precedence and `settings` object
- `app/models/base.py` — canonical response shapes
- `app/utils/logging_config.py` — JSON logging behavior
- `app/db/session.py` — DB engine/session factory (lazy; Phase 2)
- `app/routers/core.py` — example router and Actions handshake
- `version.json` — authoritative version metadata used by `settings` and endpoints

10. When to ask the maintainer
- If you need a real DB to run integration tests — confirm the intended connection string and any test fixtures.
- If you must change logging behavior in prod (like log path or rotation), confirm operational requirements before editing `logging_config.py`.

If any section is unclear or you want more examples (e.g., a sample new route that follows project patterns), say which area and I will expand it.
