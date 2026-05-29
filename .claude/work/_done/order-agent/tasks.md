# Tasks — Order Agent

Grouped into 3 bundles. Each bundle ends with its own test, green before moving on.

## Bundle 1 — Agent core
- [x] Add a `size` field (`normal` | `large`) to `OrderConfirmation`  →  app/models.py
- [x] Create the `app/agents/` package (empty `__init__.py`)
- [x] Add `OrderAgent`: in-memory store, module `logger`, `decide` (4+ items = `large`),
      `handle(request) -> confirmation` (make id, decide, store, log, return), `get(order_id)`  →  app/agents/order_agent.py
- [x] Test the agent directly in Python (no HTTP): large vs normal, store + get, missing id

## Bundle 2 — Endpoints
- [x] Wire `POST /orders` in main.py to delegate to one shared `OrderAgent`  →  app/main.py
- [x] Add `GET /orders/{order_id}`; return a clear 404 for unknown id  →  app/main.py
- [x] Test via HTTP (TestClient): post returns id+size, get returns stored order, 404 on unknown, malformed body rejected

## Bundle 3 — Verify
- [x] Run locally on port 9595, then in Docker on port 9595; walk test-plan.md
      (all 6 scenarios pass local + Docker; see logging gap below)
