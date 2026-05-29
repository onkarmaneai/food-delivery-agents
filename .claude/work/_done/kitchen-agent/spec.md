# Kitchen Agent

## Goal
Add the second agent so two agents actually talk (the heart of Step 2). When the
Order Agent creates an order, it hands it straight to the Kitchen Agent by a direct
in-process method call. The Kitchen Agent owns its own state and "cooks" the order,
moving it through `received → cooking → ready`. A queue is deferred to Step 4; the
`handle(request) -> result` contract stays the same so a queue can replace the direct
call later.

## Scope
- In:
  - `KitchenTicket` model (kitchen's own record of an order).
  - `KitchenAgent` with `handle` / `decide` / `advance` / `get`, in-memory state.
  - Order Agent hands off to the Kitchen via an optional injected reference.
  - Endpoints: `GET /kitchen/{order_id}`, `POST /kitchen/{order_id}/advance`.
  - Tests at both layers (agent-alone, over-HTTP).
- Out:
  - Queue / message bus (Step 4).
  - Async / timers / auto-cooking (Step 4). Cooking advances by an explicit step.
  - Database / persistence (Step 5) — state is in-memory, lost on restart.
  - A single combined order+kitchen view (deferred; not needed yet).

## Success criteria
- After `POST /orders`, the Kitchen Agent holds a ticket for that order at `received`
  (proves the handoff crossed from one agent to the other).
- `POST /kitchen/{id}/advance` walks the status `received → cooking → ready`; `ready`
  stays `ready`.
- Unknown id returns 404 on both kitchen endpoints.
- All existing Order Agent tests stay green (handoff is additive).

## Status (as of 2026-05-29)
- [ ] KitchenTicket model + KitchenAgent core (agent-alone tests pass)
- [ ] Order Agent hands off + kitchen endpoints wired (over-HTTP tests pass)
- [ ] Verified for real (uvicorn + Docker) and validated against this spec

## Open questions
- none
