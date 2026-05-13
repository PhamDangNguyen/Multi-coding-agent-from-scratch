# code_test — Agent Specification (Architecture)

## Goal
Provide a minimal, professional scaffold for a simple **"add two numbers"** HTTP API.

## Chosen defaults (empty target directory)
- Language: **Python**
- Web framework: **FastAPI** (default per instructions)
- Pattern: **Router/Controller + Schema/DTO + Service/Use-Case**
- Tests: **pytest**-compatible skeleton

## High-level architecture
- `app/main.py` creates the FastAPI app and includes routers.
- `app/api/routes/` contains API routers (controllers).
- `app/schemas/` contains request/response models (Pydantic DTOs).
- `app/services/` contains pure business logic (use-cases/services), independent of FastAPI.

## Add-two-numbers feature placement
- Route/controller: `app/api/routes/math.py`
  - Defines endpoint (e.g., `POST /math/add` or `GET /math/add`) and handles HTTP concerns.
  - Validates/parses inputs via `app/schemas/math.py`.
  - Calls the service in `app/services/math_service.py`.

- Schema/DTOs: `app/schemas/math.py`
  - `AddRequest(a: float, b: float)` (or int) and `AddResponse(result: float)`.

- Service/use-case: `app/services/math_service.py`
  - `add(a, b) -> result` (pure function / simple service).

## Conventions
- Keep services framework-agnostic (no FastAPI imports).
- Routers only orchestrate: request -> schema -> service -> response.
- Avoid cross-layer imports that invert dependencies.

## Downstream agent implementation boundaries
Allowed to implement later:
- FastAPI endpoint logic in `app/api/routes/*.py`
- Pydantic models in `app/schemas/*.py`
- Business logic in `app/services/*.py`
- Tests in `tests/`

Not allowed to place:
- Business logic inside routers
- FastAPI-specific objects inside services

