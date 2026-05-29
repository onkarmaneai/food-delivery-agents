"""Food Order API — now backed by the Order Agent.

The web layer is thin: it receives requests and hands the real work to the
Order Agent. The agent owns order intake and remembers the orders it created.
No database yet — the agent keeps state in memory.
"""

import logging

from fastapi import FastAPI, HTTPException

from app.agents.kitchen_agent import KitchenAgent
from app.agents.order_agent import OrderAgent
from app.models import KitchenTicket, OrderConfirmation, OrderRequest

# Turn logging on. Python's logging is silent by default, and uvicorn only sets up
# its own loggers. This one line shows INFO and above from our app (e.g. the agent's
# "order received" line) in the console / docker logs.
logging.basicConfig(level=logging.INFO)

# The app object. FastAPI uses it to register endpoints and serve requests.
app = FastAPI(title="Food Order API", version="0.3.0")

# One shared instance of each agent for the whole app. They hold state in memory,
# so every request must talk to the same instances (a new agent each time would
# forget). We build the kitchen first, then hand it to the order agent — so a new
# order is passed straight to the kitchen (two agents talking, by direct call).
kitchen_agent = KitchenAgent()
order_agent = OrderAgent(kitchen=kitchen_agent)


@app.get("/health")
def health() -> dict:
    """Simple check to confirm the app is alive."""
    return {"status": "ok"}


@app.post("/orders", response_model=OrderConfirmation)
def create_order(order: OrderRequest) -> OrderConfirmation:
    """Receive an order and hand it to the Order Agent.

    FastAPI validates the body against OrderRequest first; a bad body is
    rejected before this function runs. The agent does the rest.
    """
    return order_agent.handle(order)


@app.get("/orders/{order_id}", response_model=OrderConfirmation)
def get_order(order_id: str) -> OrderConfirmation:
    """Ask the agent for an order it stored. 404 if it never saw this id."""
    confirmation = order_agent.get(order_id)
    if confirmation is None:
        raise HTTPException(status_code=404, detail="order not found")
    return confirmation


@app.get("/kitchen/{order_id}", response_model=KitchenTicket)
def get_kitchen_ticket(order_id: str) -> KitchenTicket:
    """Read the kitchen's ticket for an order. 404 if the kitchen never got it.

    This is the kitchen's own view: the cooking status, owned by the Kitchen
    Agent. (The order's intake view lives at GET /orders/{order_id}.)
    """
    ticket = kitchen_agent.get(order_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="kitchen ticket not found")
    return ticket


@app.post("/kitchen/{order_id}/advance", response_model=KitchenTicket)
def advance_kitchen_ticket(order_id: str) -> KitchenTicket:
    """Cook one step: move the ticket received -> cooking -> ready. 404 if unknown."""
    ticket = kitchen_agent.advance(order_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="kitchen ticket not found")
    return ticket
