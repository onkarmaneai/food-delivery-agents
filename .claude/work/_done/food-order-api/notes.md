## 2026-05-29 — requirements.txt
Used `uvicorn[standard]` instead of plain `uvicorn`. The `[standard]` extra bundles
helpful bits (auto-reload, faster event loop). Same package, just batteries included.
No version pins yet — kept it simple for the skeleton; we can pin later for production.

## 2026-05-29 — app/main.py (health endpoint)
FastAPI's `TestClient` needs the `httpx` package, which we didn't install. Verified the
app loads and the route registers without it instead. If we want easy in-process tests
later, add `httpx` to requirements.

## 2026-05-29 — Dockerfile (host binding)
Locally we ran uvicorn on `127.0.0.1` (loopback). Inside Docker we must use
`0.0.0.0`, otherwise the app only listens *inside* the container and the published
port can't reach it. `0.0.0.0` = "accept connections on all network interfaces".
Also put `COPY requirements.txt` + install BEFORE `COPY app/` so Docker's layer cache
skips reinstalling packages when only code changes.

## 2026-05-29 — Docker run (port clash, BLOCKED)
Container built and runs fine — verified from INSIDE via `docker exec` (health + order
both correct). But an unrelated host process `serve.py 9090` (PID 7404) already owns
port 9090, so external curl to 127.0.0.1:9090 hits serve.py (Python http.server error
pages), not our container. Lesson: two things can't bind the same host port; the host-side
mapping loses to whoever grabbed it first.
RESOLVED: user keeps serve.py on 9090; we moved the app to port 9595 (spec, test-plan,
Dockerfile updated). Rebuilt and re-tested in Docker on 9595 — all endpoints pass.
