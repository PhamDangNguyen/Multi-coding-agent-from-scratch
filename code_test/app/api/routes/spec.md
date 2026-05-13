# app/api/routes/

## Purpose
FastAPI routers (controllers). Each module typically defines an `APIRouter` and endpoints for one functional area.

## What belongs here
- `math.py` router for math operations (add-two-numbers endpoint).
- Additional routers grouped by domain.

## Downstream agents may implement
- FastAPI endpoints: request parsing, calling services, returning responses.
- Minimal validation/orchestration logic.

## Must NOT be placed here
- Core business rules or computational logic (put in `app/services/`).
- Database access (not part of this simple task).
