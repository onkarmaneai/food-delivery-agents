"""Order Agent — the first agent in the system.

What is an agent here? An autonomous component. It has:
- one job: order intake,
- its own state: the orders it created (kept in memory for now),
- one door in and one door out: ``handle(request) -> confirmation``.

No LLM yet. ``decide()`` is a plain rule today, but it is the *seam* where an
LLM "brain" could slot in later — without changing the message contract.
"""

import logging
import uuid

from app.models import OrderConfirmation, OrderRequest

logger = logging.getLogger(__name__)

# An order with this many items (or more) counts as "large".
LARGE_ORDER_ITEM_COUNT = 4


class OrderAgent:
    """Owns order intake. Remembers the orders it created."""

    def __init__(self) -> None:
        # The agent's own state: order_id -> confirmation.
        # In-memory only, so it is lost on restart. A real database is Step 5.
        self._orders: dict[str, OrderConfirmation] = {}

    def decide(self, request: OrderRequest) -> str:
        """The brain seam. Plain rule for now: flag big orders as 'large'.

        Later an LLM could make this call instead, and ``handle`` would not change.
        """
        if len(request.items) >= LARGE_ORDER_ITEM_COUNT:
            return "large"
        return "normal"

    def handle(self, request: OrderRequest) -> OrderConfirmation:
        """One door in, one door out: take an order, return a confirmation."""
        order_id = str(uuid.uuid4())
        size = self.decide(request)
        confirmation = OrderConfirmation(
            order_id=order_id,
            status="received",
            customer=request.customer,
            items=request.items,
            size=size,
        )
        self._orders[order_id] = confirmation  # remember it
        logger.info(
            "Order %s received from %s — %d item(s), size=%s",
            order_id,
            request.customer,
            len(request.items),
            size,
        )
        return confirmation

    def get(self, order_id: str) -> OrderConfirmation | None:
        """Read a stored order back. Returns None if we never saw this id."""
        return self._orders.get(order_id)
