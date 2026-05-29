"""Food Order API — walking skeleton.

A thin pipe: it accepts requests and returns responses. No database, no agents
yet. This file holds the FastAPI app and its endpoints.
"""

import uuid

from fastapi import FastAPI

from app.models import OrderConfirmation, OrderRequest

# The app object. FastAPI uses it to register endpoints and serve requests.
app = FastAPI(title="Food Order API", version="0.1.0")


@app.get("/health")
def health() -> dict:
    """Simple check to confirm the app is alive."""
    return {"status": "ok"}


@app.post("/orders", response_model=OrderConfirmation)
def create_order(order: OrderRequest) -> OrderConfirmation:
    """Receive an order and return a confirmation.

    No database yet — we just generate a unique id and echo the order back.
    FastAPI validates the incoming body against OrderRequest automatically;
    a bad body is rejected before this function even runs.
    """
    order_id = str(uuid.uuid4())  # uuid4 = a random unique id, no DB needed
    return OrderConfirmation(
        order_id=order_id,
        status="received",
        customer=order.customer,
        items=order.items,
    )
