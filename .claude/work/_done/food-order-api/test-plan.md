# Test plan — food-order-api

## Scenarios
- [x] When I POST a valid order (customer + items), I get back a confirmation with an order id and status "received".
  evidence: POST /orders → HTTP 200, returned order_id + status "received" + echoed items
- [x] When I POST a body missing the customer or items, I get a clear validation error (not a crash).
  evidence: POST /orders {"items":["pizza"]} → HTTP 422, "customer" Field required
- [x] When I POST items as the wrong type (e.g. a number instead of a list), I get a validation error.
  evidence: POST /orders {"items":5} → HTTP 422, "Input should be a valid list"
- [x] When I GET /health, I get {"status": "ok"}.
  evidence: GET /health → HTTP 200, {"status":"ok"}
- [x] When the app runs inside Docker on port 9595, all the above behave the same.
  evidence: all scenarios above were run against the running container food-api-test on :9595
- [x] When I open /docs in the browser, I can see and try the endpoints.
  evidence: GET /docs → HTTP 200 (interactive Swagger page served by FastAPI)
