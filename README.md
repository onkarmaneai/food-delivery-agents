# Food Order API

A tiny food delivery API. This is the **walking skeleton** — a thin pipe that proves
the plumbing works end to end. It takes an order and returns a confirmation. No
database or agents yet; those come later.

## What it does

- `POST /orders` — place an order, get back a confirmation with an order id.
- `GET /health` — check the app is alive.
- `GET /docs` — interactive API docs in the browser (built in by FastAPI).

The app listens on **port 9595**.

## Run locally (with a virtual environment)

A virtual environment (venv) = a private box of Python packages for this project.

```bash
# 1. create and activate the venv
python3 -m venv .venv
source .venv/bin/activate

# 2. install dependencies
pip install -r requirements.txt

# 3. start the server
uvicorn app.main:app --host 127.0.0.1 --port 9595
```

Then open http://localhost:9595/docs in your browser.

## Run with Docker

Docker packages the app so it runs the same anywhere.

```bash
# build the image
docker build -t food-api .

# run it (maps your port 9595 to the container's 9595)
docker run -d --name food-api -p 9595:9595 food-api
```

Open http://localhost:9595/docs to try it.

Handy Docker commands:

```bash
docker logs food-api      # see the app's logs
docker rm -f food-api     # stop and remove the container
```

## Try an order

```bash
curl -X POST http://localhost:9595/orders \
  -H "Content-Type: application/json" \
  -d '{"customer":"Onkar","items":["pizza","coke"]}'
```

Expected reply:

```json
{
  "order_id": "<a unique id>",
  "status": "received",
  "customer": "Onkar",
  "items": ["pizza", "coke"]
}
```

A bad order (missing customer, or empty items) returns a `422` error with a clear
message — that's FastAPI validating the request for us.

## Project layout

```
app/
  __init__.py     # marks app/ as a Python package
  main.py         # FastAPI app + endpoints
  models.py       # data shapes (Pydantic)
requirements.txt  # dependencies
Dockerfile        # how to build the container image
.dockerignore     # files Docker should skip
```
