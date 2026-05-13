# app/api/

## Purpose
HTTP API layer: versioning, routing composition, and controller organization.

## What belongs here
- Router registration modules (e.g., `routes/__init__.py` exports routers).
- API-level concerns: tags, prefixes, dependencies (if introduced later).

## Downstream agents may implement
- Router aggregation and API versioning strategy.

## Must NOT be placed here
- Business logic calculations (belongs in `app/services/`).
- Pydantic schemas (belongs in `app/schemas/`).
