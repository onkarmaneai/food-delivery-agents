"""Bundle 2 tests — exercise the whole pipe over HTTP.

These use FastAPI's TestClient (a fake user that calls the app in memory, no
real server). They prove the web layer + Order Agent work together.
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_post_order_returns_id_and_size():
    resp = client.post("/orders", json={"customer": "Ada", "items": ["pizza"]})
    assert resp.status_code == 200
    body = resp.json()
    assert body["order_id"]
    assert body["status"] == "received"
    assert body["size"] == "normal"


def test_post_large_order_flagged_large():
    resp = client.post(
        "/orders", json={"customer": "Grace", "items": ["a", "b", "c", "d"]}
    )
    assert resp.status_code == 200
    assert resp.json()["size"] == "large"


def test_get_returns_stored_order():
    created = client.post(
        "/orders", json={"customer": "Edsger", "items": ["soup"]}
    ).json()

    resp = client.get(f"/orders/{created['order_id']}")
    assert resp.status_code == 200
    assert resp.json()["order_id"] == created["order_id"]
    assert resp.json()["customer"] == "Edsger"


def test_get_unknown_id_returns_404():
    resp = client.get("/orders/does-not-exist")
    assert resp.status_code == 404


def test_malformed_body_is_rejected():
    # Missing "items" — FastAPI rejects before the agent runs.
    resp = client.post("/orders", json={"customer": "Linus"})
    assert resp.status_code == 422
