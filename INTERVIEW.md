# Interview Q&A

A growing list of interview-style questions from this project, with plain-English answers.

---

## Q1. What is FastAPI's `TestClient`?

**TestClient = a fake user that calls your API inside your test code.**

Normally to test an API you'd start the server, open another terminal, and send a
real request over the network. That's slow. `TestClient` skips all that — it calls
your app **directly in memory** (no server, no network) and returns the response.

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
response = client.get("/health")
assert response.json() == {"status": "ok"}
```

**Why it exists:** test APIs fast and automatically, without spinning up a real server.

---

## Q2. Why does TestClient need `httpx` and not the built-in `http`?

- **`http`** — Python's built-in web module. Low-level, verbose, no async. Clunky.
- **`httpx`** — a modern, separate library for web requests. Clean, simple, supports
  **async** (many requests without waiting).

`TestClient` is built **on top of `httpx`**. So `httpx` is the engine, `TestClient`
is the steering wheel. No engine, no drive — that's why we got a `ModuleNotFoundError`.

| | `http` (built-in) | `httpx` (needed) |
|---|---|---|
| Style | Low-level, verbose | Clean, simple |
| Async support | No | Yes |
| Used by TestClient? | No | Yes |

**Why we didn't have it:** `httpx` is an *optional* dependency. FastAPI doesn't
force-install it, since not everyone uses TestClient. Smaller default install is the
trade-off; you add `httpx` yourself when you want it.

---

## Q3. Docker shares the host kernel — so is `python:3.12-slim` just the Python interpreter?

**No. It's a mini-Linux + Python, riding on the host's kernel.**

- Containers **share the host kernel** (the OS core that talks to hardware), so they
  don't ship a full OS like a VM does — that's why they're small and fast.
- But the image is not *only* the interpreter. Layers:
  ```
  your app
  Python 3.12 interpreter
  minimal Linux userland (basic libs, shell)   ← the "slim" part
  ──────────────────────────────────────
  host kernel (shared, NOT in the image)
  ```
- "slim" = a stripped-down Debian with the extras removed to stay small.

Analogy: a VM brings engine + car; a container brings just the car body and borrows
the host's engine (kernel).

---

## Q4. Does a Docker container get its own RAM and disk (ROM)?

**No. A container is not a separate computer.** It borrows the host's hardware.

- **RAM:** shares the host's RAM. No fixed slice by default — uses what it needs. You
  can cap it (`docker run --memory=512m`), but that's a limit, not dedicated memory.
- **Disk:** no separate disk. Files live as **layers on the host's disk**. Anything
  written is lost when the container stops — unless you attach a **volume** (storage
  that survives restarts).

| | Virtual Machine | Docker container |
|---|---|---|
| Own kernel? | Yes | No (shares host) |
| Own RAM? | Yes, fixed slice | No, shares host (can cap) |
| Own disk? | Yes, virtual disk | No, layered on host disk |
| Size | GBs | MBs |

One-liner: a container isolates *how the app sees things* but borrows the host's real
RAM, disk, and kernel. It's a fenced area in your house, not a separate house.

---

## Q5. Handy Docker commands (cheat sheet)

```bash
docker ps                     # see running containers
docker logs food-api-test     # see the app's log output
docker logs -f food-api-test  # follow logs live (Ctrl+C to stop)
docker logs -t food-api-test  # show logs with timestamps (UTC)
docker rm -f food-api-test    # stop & remove the container when done
```

`docker logs` just replays whatever the app printed to stdout/stderr.

---

## Q6. In a log line like `INFO: 192.168.65.1:65334 - "GET /health" 200 OK`, what is `192.168.65.1:65334`?

It's **client IP : client source port** — NOT a process id.

- `192.168.65.1` = who made the request. On Docker Desktop (Mac), this is the
  **gateway** between the Mac and Docker's internal network, so host requests appear
  to come from here.
- `65334` = the client's **source port**, a random high port picked per connection.
  It changes every request.

Reads as: "client 192.168.65.1, via port 65334, asked GET /health, got 200 OK."

---

## Q7. The logs show GMT/UTC time. Can I get IST? Should I change log contents?

- uvicorn's default access line has **no timestamp**. Timestamps appear with
  `docker logs -t`, and Docker always stamps them in **UTC** (`Z` = UTC = GMT).
- **Container clock → IST:** run with `-e TZ=Asia/Kolkata` (changes the app's own
  timestamps; the `docker logs -t` stamps stay UTC).
- **App logs → IST:** customize Python's logging format to print local time.
- You don't edit `docker logs` itself — you change the **app's** logging.

**Good idea?** Adding fields (timestamp, request id) = yes. Switching to IST locally =
fine. IST **in production = no** — servers log in **UTC** so logs from different
regions line up on one clock. Convert to local time when *viewing*, not when storing.

---

## Q8. Difference between the per-task test, `/verify-r`, and `/validate-r`?

Three layers of checking, each catching what the others miss.

| | Per-task test | `/verify-r` | `/validate-r` |
|---|---|---|---|
| Question | "Did this piece work?" | "Does the feature behave right?" | "Does code match the spec?" |
| When | While building one task | After whole feature built | Near the end, after verify |
| Size | One task | Whole feature | Whole feature |
| Runs the app? | A little | Yes, fully | No — reads spec + code |
| Who checks | Me (builder) | Me (builder) | A fresh, independent agent |
| Catches | A broken step | Wrong behavior | Missing / drifted scope |

Restaurant analogy:
- **Per-task test** = cook tasting the sauce at each step.
- **/verify-r** = waiter checking the finished plate matches the order before serving.
- **/validate-r** = a separate inspector comparing the dish to the official recipe —
  someone who didn't cook it, so they're unbiased.

Why three? I can build each step perfectly and the app can run fine, yet I might have
quietly skipped a spec requirement. Only a fresh reader (validate) reliably catches
that blind spot.
