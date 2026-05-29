"""Bundle 1 tests — exercise the KitchenAgent directly, with no HTTP.

This proves the Kitchen Agent stands on its own: it accepts a handed-off order
(handle), walks the cooking lifecycle (advance + decide), and remembers its
tickets (get). The handoff over HTTP is tested separately in Bundle 2.
"""

from app.agents.kitchen_agent import KitchenAgent
from app.models import OrderConfirmation


def _order(order_id="order-1", customer="Ada", items=None):
    """A confirmed order, as the Order Agent would hand it over."""
    return OrderConfirmation(
        order_id=order_id,
        customer=customer,
        items=items or ["pizza"],
    )


def test_handle_creates_ticket_at_received():
    agent = KitchenAgent()
    ticket = agent.handle(_order())

    assert ticket.order_id == "order-1"
    assert ticket.status == "received"
    assert ticket.customer == "Ada"
    assert ticket.items == ["pizza"]


def test_advance_walks_received_to_cooking_to_ready():
    agent = KitchenAgent()
    agent.handle(_order())

    assert agent.advance("order-1").status == "cooking"
    assert agent.advance("order-1").status == "ready"


def test_advance_on_ready_stays_ready():
    agent = KitchenAgent()
    agent.handle(_order())
    agent.advance("order-1")  # -> cooking
    agent.advance("order-1")  # -> ready

    assert agent.advance("order-1").status == "ready"


def test_advance_unknown_id_returns_none():
    agent = KitchenAgent()
    assert agent.advance("does-not-exist") is None


def test_decide_returns_next_status():
    agent = KitchenAgent()
    ticket = agent.handle(_order())
    assert agent.decide(ticket) == "cooking"


def test_get_returns_stored_ticket():
    agent = KitchenAgent()
    agent.handle(_order(order_id="abc", customer="Edsger"))

    stored = agent.get("abc")
    assert stored is not None
    assert stored.order_id == "abc"
    assert stored.customer == "Edsger"


def test_get_unknown_id_returns_none():
    agent = KitchenAgent()
    assert agent.get("does-not-exist") is None
