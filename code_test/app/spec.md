# app/

## Purpose
Top-level Python package containing the FastAPI application and all application code.

## What belongs here
- App entrypoint (`main.py`) that constructs the FastAPI app.
- API layer (routers/controllers) under `api/`.
- Data schemas/DTOs under `schemas/`.
- Business logic/services (use-cases) under `services/`.

## Downstream agents may implement
- `main.py` app creation, router inclusion, middleware wiring.

## Must NOT be placed here
- Tests (they belong in `tests/`).
- Ad-hoc scripts; keep runtime code within the app package.
