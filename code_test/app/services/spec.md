# app/services/

## Purpose
Framework-agnostic application services / use-cases.

## What belongs here
- `math_service.py` with pure function(s) for addition.

## Downstream agents may implement
- Pure Python logic for computing results.
- Small helper functions used by routers.

## Must NOT be placed here
- FastAPI imports (`APIRouter`, `Request`, etc.).
- HTTP/response formatting.
