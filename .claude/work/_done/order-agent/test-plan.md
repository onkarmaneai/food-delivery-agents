# Test plan — Order Agent

## Scenarios
- [x] When a customer POSTs a valid order, they get back a confirmation with an order id.
  evidence: POST /orders {customer:Ada,items:[pizza]} → 200, order_id=eac0fb5f…, status=received
- [x] When an order has many items (4+), the confirmation marks it `large`.
  evidence: POST with 4 items → size=large
- [x] When an order has few items, the confirmation marks it `normal`.
  evidence: POST with 3 items → size=normal
- [x] When a customer GETs an order id that exists, they see the stored order.
  evidence: GET /orders/{id} → 200, customer=Ada, id matches=True (agent state survives across requests)
- [x] When a customer GETs an order id that does not exist, they get a clear 404.
  evidence: GET /orders/nope → status=404
- [x] When the order body is malformed, it is rejected before the agent runs.
  evidence: POST {customer:X} (no items) → status=422
- [x] When OrderAgent.handle() is called directly in a test (no HTTP), it returns a confirmation.
  evidence: pytest tests/test_order_agent.py → 5 passed (handle/decide/get, no HTTP)
- [x] All of the above behave the same when run in Docker on port 9595.
  evidence: rebuilt image, ran container → normal/large/200/404/422 all match; agent log line visible in `docker logs`
