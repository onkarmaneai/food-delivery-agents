"""Bundle 1 tests — exercise the OrderAgent directly, with no HTTP.

This proves the agent stands on its own: its brain (decide), its memory (store +
get), and its one door (handle). The web layer is tested separately in Bundle 2.
"""

from app.agents.order_agent import OrderAgent
from app.models import OrderRequest


def test_handle_returns_confirmation_with_id():
    agent = OrderAgent()
    confirmation = agent.handle(OrderRequest(customer="Ada", items=["pizza"]))

    assert confirmation.order_id  # a non-empty id was generated
    assert confirmation.status == "received"
    assert confirmation.customer == "Ada"
    assert confirmation.items == ["pizza"]


def test_decide_flags_large_order():
    agent = OrderAgent()
    big = OrderRequest(customer="Grace", items=["a", "b", "c", "d"])  # 4 items
    assert agent.decide(big) == "large"
    assert agent.handle(big).size == "large"


def test_decide_flags_small_order_normal():
    agent = OrderAgent()
    small = OrderRequest(customer="Linus", items=["a", "b", "c"])  # 3 items
    assert agent.decide(small) == "normal"
    assert agent.handle(small).size == "normal"


def test_get_returns_stored_order():
    agent = OrderAgent()
    confirmation = agent.handle(OrderRequest(customer="Edsger", items=["soup"]))

    stored = agent.get(confirmation.order_id)
    assert stored is not None
    assert stored.order_id == confirmation.order_id
    assert stored.customer == "Edsger"


def test_get_unknown_id_returns_none():
    agent = OrderAgent()
    assert agent.get("does-not-exist") is None
