# Notes — Order Agent

## 2026-05-29 — Bundle 1 (Agent core)
No tests or pytest were committed from the food-order-api skeleton — those TestClient
runs (INTERVIEW Q1/Q2) were ad-hoc. Added `pytest` in a new `requirements-dev.txt`,
kept separate from `requirements.txt` so the Docker image stays slim. Bundle 2 will
add `httpx` there too (TestClient needs it). Tests live in `tests/`.

## 2026-05-29 — Bundle 3 verify: logging gap found
All 6 test-plan scenarios pass locally and in Docker on 9595. BUT the agent's
`logger.info` lines never show — Python logging is off by default, and uvicorn only
configures its own loggers, not the root. Fix is one line in main.py:
`logging.basicConfig(level=logging.INFO)`. Spec lists "light logging so we can see the
agent work" as in-scope, so this needs the fix before /wrap-r.
FIXED: added `logging.basicConfig(level=logging.INFO)` to main.py. Agent line now shows:
`INFO:app.agents.order_agent:Order <id> received from <name> — N item(s), size=...`.
Tests still 10/10.

## 2026-05-29 — Bundle 2 (Endpoints)
Used one shared `OrderAgent` instance in main.py — a per-request agent would forget
its in-memory orders. TestClient prints a harmless warning ("install httpx2"); tests
still pass (10/10). Left as-is; revisit if it ever breaks. Malformed body returns 422
(FastAPI's validation code), not 400 — updated that expectation in the test.
