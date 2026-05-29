# Tasks — kitchen-agent

## Bundle 1 — model + agent core (test the agent alone)
- [x] Add `KitchenTicket` model to `app/models.py` (order_id, status default `received`, customer, items)  →  app/models.py
- [x] Write `app/agents/kitchen_agent.py` — `KitchenAgent` with in-memory `_tickets`, `handle`, `decide`, `advance`, `get`, mirroring the Order Agent's shape  →  app/agents/order_agent.py
- [x] Test the agent alone in `tests/test_kitchen_agent.py`: handle creates a ticket at `received`; advance walks received→cooking→ready; advance on ready stays ready; get unknown id → None; decide rule

## Bundle 2 — handoff + endpoints (test over HTTP)
- [x] Wire the handoff in `app/agents/order_agent.py`: `__init__(self, kitchen=None)`; in `handle`, if kitchen is set, call `self._kitchen.handle(confirmation)`. Keep returning the OrderConfirmation unchanged  →  app/agents/order_agent.py
- [x] Update `app/main.py`: create `kitchen_agent`, inject into `OrderAgent`, add `GET /kitchen/{order_id}` (404 if none) and `POST /kitchen/{order_id}/advance` (404 if none), bump version to 0.3.0  →  app/main.py
- [x] Test over HTTP in `tests/test_kitchen_api.py`: POST /orders then GET /kitchen/{id} shows ticket at `received` (proves handoff); advance moves status; unknown id → 404 on both endpoints
- [x] Run the full suite — confirm existing Order Agent + orders-API tests stay green

## Bundle 3 — verify for real
- [x] Run uvicorn on 9595 and walk the curl flow: post order → read kitchen ticket → advance twice → see received→cooking→ready
- [x] Rebuild the Docker image and repeat the flow to confirm parity (INTERVIEW Q10)
