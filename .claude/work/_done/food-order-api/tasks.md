# Tasks — food-order-api

- [x] Add `requirements.txt` with fastapi and uvicorn
- [x] Create `app/` package with an empty `__init__.py`
- [x] Write `app/models.py`: Pydantic models for the order request and the confirmation response
- [x] Write `app/main.py`: FastAPI app instance + `GET /health` returning {"status": "ok"}
- [x] Add `POST /orders` to `app/main.py`: accept the order, make an order id, return the confirmation
- [x] Run locally with uvicorn on port 9595 and test /health, /orders, and bad input via /docs and curl
- [x] Write `Dockerfile` (python base, install requirements, run uvicorn on 9595)
- [x] Add `.dockerignore` to keep the image small
- [x] Build the Docker image and run the container on port 9595, then re-test the endpoints
- [x] Write a short `README.md`: how to run locally and with Docker
