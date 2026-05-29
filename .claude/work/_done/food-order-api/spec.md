# Food Order API (Walking Skeleton)

## Goal
Build a thin, end-to-end pipe before adding any agent logic. One HTTP endpoint takes
a food order and returns a confirmation. It runs inside a Docker container on port 9595.
This proves the plumbing works so future agents can slot into a pipe that already runs.

## Scope
- In: `POST /orders` accepts `{"customer": "...", "items": [...]}` and returns
  `{order_id, status: "received", customer, items}`.
- In: `GET /health` returns `{"status": "ok"}`.
- In: FastAPI + Uvicorn, packaged in Docker, runs on port 9595.
- In: basic request-shape validation (reject malformed orders).
- Out: no database, no real agents, no kitchen/delivery logic.
- Out: no auth, no caching, no async work, no persistence.

## Success criteria
- A POST with a valid order returns a confirmation JSON with an order id.
- A POST with a malformed body is rejected with a clear error.
- The health check returns ok.
- All of the above work the same when run inside Docker on port 9595.

## Status (as of 2026-05-29)
- [ ] FastAPI app with `/orders` and `/health` endpoints
- [ ] Order request/response data models (Pydantic)
- [ ] Dockerfile + requirements, runs on port 9595
- [ ] Verified end-to-end locally and in Docker

## Open questions
- none
