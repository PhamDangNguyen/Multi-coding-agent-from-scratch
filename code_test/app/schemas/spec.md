# app/schemas/

## Purpose
Pydantic models (DTOs) defining request/response shapes for the API.

## What belongs here
- `math.py` with `AddRequest` and `AddResponse` models.

## Downstream agents may implement
- Pydantic BaseModel classes and validation constraints.

## Must NOT be placed here
- FastAPI router code.
- Business logic.
