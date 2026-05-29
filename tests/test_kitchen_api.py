"""Bundle 2 tests — exercise the handoff and kitchen endpoints over HTTP.

These use FastAPI's TestClient (a fake user that calls the app in memory, no
real server). The key test posts an order and then reads the kitchen ticket:
if the ticket is there, the Order Agent really handed the order to the Kitchen
Agent — two agents talking.
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _place_order(customer="Ada", items=None):
    """Place an order and return its id."""
    resp = client.post("/orders", json={"customer": customer, "items": items or ["pizza"]})
    assert resp.status_code == 200
    return resp.json()["order_id"]


def test_posting_an_order_creates_a_kitchen_ticket():
    # The handoff: place an order, then the kitchen should hold a ticket for it.
    order_id = _place_order(customer="Ada")

    resp = client.get(f"/kitchen/{order_id}")
    assert resp.status_code == 200
    ticket = resp.json()
    assert ticket["order_id"] == order_id
    assert ticket["status"] == "received"
    assert ticket["customer"] == "Ada"


def test_advance_moves_status_received_to_cooking_to_ready():
    order_id = _place_order()

    assert client.post(f"/kitchen/{order_id}/advance").json()["status"] == "cooking"
    assert client.post(f"/kitchen/{order_id}/advance").json()["status"] == "ready"
    # advancing a ready ticket stays ready
    assert client.post(f"/kitchen/{order_id}/advance").json()["status"] == "ready"


def test_order_view_unchanged_by_cooking():
    # Each agent owns its own state: cooking does not change the order's intake view.
    order_id = _place_order()
    client.post(f"/kitchen/{order_id}/advance")  # -> cooking

    order = client.get(f"/orders/{order_id}").json()
    assert order["status"] == "received"


def test_get_unknown_kitchen_ticket_returns_404():
    assert client.get("/kitchen/does-not-exist").status_code == 404


def test_advance_unknown_kitchen_ticket_returns_404():
    assert client.post("/kitchen/does-not-exist/advance").status_code == 404
