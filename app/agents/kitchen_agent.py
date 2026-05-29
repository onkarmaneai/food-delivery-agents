"""Kitchen Agent — the second agent in the system.

It does one job: cook orders. The Order Agent hands it a confirmed order
(a direct method call for now), and the Kitchen walks that order through its
cooking lifecycle: ``received -> cooking -> ready``. It keeps its own state —
the tickets it is working on — in memory.

Like the Order Agent, ``decide()`` is the brain seam. Today it is a plain rule.
Later an LLM (or a timer) could decide cook time without changing ``handle()``.
"""

import logging

from app.models import KitchenTicket, OrderConfirmation

logger = logging.getLogger(__name__)

# The cooking lifecycle, in order. Each advance() step moves to the next stage;
# the last one ("ready") is the end of the line.
COOKING_STAGES = ["received", "cooking", "ready"]


class KitchenAgent:
    """Owns the cooking lifecycle. Remembers the tickets it is working on."""

    def __init__(self) -> None:
        # The agent's own state: order_id -> kitchen ticket.
        # In-memory only, so it is lost on restart. A real database is Step 5.
        self._tickets: dict[str, KitchenTicket] = {}

    def decide(self, ticket: KitchenTicket) -> str:
        """The brain seam. Plain rule for now: return the next cooking status.

        ``received -> cooking -> ready``. "ready" is the end, so it stays "ready".
        Later an LLM could make this call instead, and ``advance`` would not change.
        """
        stage = COOKING_STAGES.index(ticket.status)
        if stage + 1 < len(COOKING_STAGES):
            return COOKING_STAGES[stage + 1]
        return ticket.status  # already "ready" — nothing after it

    def handle(self, order: OrderConfirmation) -> KitchenTicket:
        """One door in: take a handed-off order, start a ticket at "received"."""
        ticket = KitchenTicket(
            order_id=order.order_id,
            status="received",
            customer=order.customer,
            items=order.items,
        )
        self._tickets[order.order_id] = ticket  # remember it
        logger.info(
            "Kitchen received order %s for %s — %d item(s)",
            order.order_id,
            order.customer,
            len(order.items),
        )
        return ticket

    def advance(self, order_id: str) -> KitchenTicket | None:
        """Move a ticket one step along the cooking lifecycle.

        Returns the updated ticket, or None if we never saw this id.
        """
        ticket = self._tickets.get(order_id)
        if ticket is None:
            return None
        ticket.status = self.decide(ticket)
        logger.info("Kitchen order %s is now %s", order_id, ticket.status)
        return ticket

    def get(self, order_id: str) -> KitchenTicket | None:
        """Read a stored ticket back. Returns None if we never saw this id."""
        return self._tickets.get(order_id)
