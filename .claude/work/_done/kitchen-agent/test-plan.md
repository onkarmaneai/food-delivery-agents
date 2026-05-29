# Test plan — kitchen-agent

## Scenarios
- [x] When I `POST /orders`, then `GET /kitchen/{order_id}`, I see a kitchen ticket
      for that order with status `received` (the handoff happened across agents).
- [x] When I `POST /kitchen/{order_id}/advance` once, the status becomes `cooking`.
- [x] When I advance again, the status becomes `ready`.
- [x] When I advance an order that is already `ready`, it stays `ready`.
- [x] When I `GET /kitchen/{unknown_id}`, I get a 404.
- [x] When I `POST /kitchen/{unknown_id}/advance`, I get a 404.
- [x] The order's own view (`GET /orders/{id}`) still reads `received` — the Order
      Agent's record is unchanged by cooking (each agent owns its own state).
