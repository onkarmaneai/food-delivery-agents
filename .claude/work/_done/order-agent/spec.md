# Order Agent

## Goal
Introduce the first **agent** in the system. An agent here is an autonomous component:
it has one job, owns its own state, and talks to others only through messages. The Order
Agent owns order intake. The `/orders` endpoint stops doing the work inline and instead
**delegates** to the agent. The agent keeps the orders it created in memory and can hand
one back when asked. No LLM yet — but the agent has a `decide` seam where an LLM brain
could slot in later. This gives the next agents (Kitchen, Delivery) a real agent to talk to.

## Scope
- In: `app/agents/order_agent.py` with an `OrderAgent` class.
- In: one message contract — `handle(request) -> confirmation` (one way in, one way out).
- In: agent owns state — an in-memory dict of orders keyed by `order_id`.
- In: a private `decide` step with a real rule — flag an order as **large** when it has
  many items (e.g. 4+); otherwise **normal**. This is the seam an LLM could replace later.
- In: `POST /orders` delegates to the agent (no inline logic).
- In: `GET /orders/{order_id}` reads a stored order back from the agent.
- In: light logging via Python's stdlib `logging` (a few `logger.info` calls so we can
  see the agent work). No custom logger module.
- Out: no LLM / Claude API (seam left open, not filled).
- Out: real logging — JSON/structured, levels, UTC, correlation id — that is **Step 3**,
  best added when agent #2 arrives so a trace has something to follow.
- Out: no Kitchen or Delivery agents (later features).
- Out: no database — in-memory only (persistence is Step 5).
- Out: no async, no queue, no auth, no caching.

## Success criteria
- `POST /orders` with a valid order returns a confirmation with an id, via the agent.
- The confirmation shows whether the order is `large` or `normal` (the decide rule).
- `GET /orders/{order_id}` returns the stored order; unknown id returns a clear 404.
- A malformed body is still rejected before the agent runs.
- `OrderAgent.handle()` works when called directly (no HTTP) — proves the agent stands alone.
- Same behavior locally and in Docker on port 9595.

## Status (as of 2026-05-29)
- [ ] OrderAgent class: handle() + own in-memory state + decide rule
- [ ] Wire endpoints: POST /orders delegates, add GET /orders/{order_id}
- [ ] Tests (agent direct + HTTP) and verify locally and in Docker

## Open questions
- none
