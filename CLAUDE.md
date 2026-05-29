# Project: Food Delivery — Multi-Agent Learning System

## What this project is

A learning project. The goal is to understand **multi-agent systems** by building a
**food delivery app**, slowly, from a tiny working version all the way to a
production-grade, scalable system.

We start simple. We add each advanced topic only when the app actually needs it,
so every concept has a real reason behind it — not just theory.

## Who I'm working with

- The user is a Python-focused learner (see global memory: Desi Architect 7-phase roadmap).
- Explain everything in plain, simple English. Grade-8 reading level.
- Short sentences. Use bullets. Small examples and analogies.
- Define any technical term in one short line right after using it.
- Never use 5 words when 2 will do.
- For any complex concept explain why that concept came? What problem it solved? How it is implemented? What are the trade-offs?

## Also learning in this project

Alongside the multi-agent system, we are learning two Claude Code features:

- **Subagents** — smaller helper agents that do one focused job and report back.
- **Skills** — reusable, named instructions/commands the agent can invoke.

When these come up naturally in the build, pause and explain them in plain English.

## Stack & conventions (from food-order-api)

- App code lives in `app/` (FastAPI + Uvicorn). Plans live in `.claude/work/`.
- The app runs on **port 9595**, NOT 9090 — port 9090 is taken by an unrelated
  `serve.py` on this machine. Use 9595 for local runs and Docker.
- Local runs use the `.venv/` virtual environment; Docker handles isolation otherwise.
- Agents live in `app/agents/`, one file per agent. An agent = autonomous component:
  one job, owns its state, talks via messages (`handle(request) -> result`). Plain
  Python now, with a `decide()` seam where an LLM brain can slot in later.
- Agents hand off work by a direct in-process call for now: one agent holds an
  optional injected reference to the next (e.g. `OrderAgent(kitchen=...)`, default
  `None` so it still runs alone). `handle(order)` is the seam — a queue can replace
  the direct call at Step 4 with no agent rewrite.
- Each agent owns its own slice of state for the same order (Order = intake,
  Kitchen = cooking). Read each via its own endpoint: `GET /orders/{id}` vs `GET /kitchen/{id}`.
- Tests live in `tests/`. Dev/test deps go in `requirements-dev.txt` (kept out of the
  runtime `requirements.txt` so the Docker image stays slim).
- Gotcha: Python logging is silent by default; uvicorn only configures its own loggers.
  Put `logging.basicConfig(level=logging.INFO)` in `main.py` so app logs show.

## How we work across sessions

One feature = one git branch = one chat session. A fresh session does NOT remember
past chats — only files carry over. So decisions that matter must live in files:
`CLAUDE.md` (auto-loaded), the active `.claude/work/<feature>/` folder, `notes.md`,
`INTERVIEW.md`, and `INSIGHTS.md` (how-we-build lessons — read it before a new feature).
Rule: if it matters beyond this chat, write it down, don't just say it.

## Interview notes

`INTERVIEW.md` (project root) collects interview-style Q&A that come up during the
build. When the user asks an "interview question," answer in plain English AND append
it to `INTERVIEW.md` so it builds into a study sheet over time.

## The build process (5 steps, slow and steady)

We move to the next step only after the current one works.

1. **Pick & sketch** — Choose one known system. Draw 3 agents and each one's job.
2. **Build the core** — Make the 3 agents talk and finish one task end-to-end locally. Ugly but working.
3. **Make it solid** — Add error handling, logging, and tests.
4. **Containerize** — Put it in Docker so it runs the same anywhere.
5. **Go to production** — Add database, security, monitoring, and deploy.

## Production concepts roadmap (learn each when the app needs it)

The user wants to learn these scaling/production topics. We do NOT learn them all
at once. Each is mapped to the step where it naturally shows up.

**Step 3 — Make it solid**
- Idempotency — same request twice = same result, no double order.
- Indexing — make database lookups fast.
- Connection pooling — reuse DB connections instead of opening new ones each time.
- Secrets management — keep passwords/keys out of the code.
- Monitoring — see what the system is doing and when it breaks.

**Step 4 — Containerize**
- Async — do many tasks without waiting on each other.
- Redis caching — store hot data in memory for speed.
- Cache patterns — cache-aside, read-through, write-through, TTL (expiry time).
- Queue — buffer work so agents don't get overwhelmed.

**Step 5 — Go to production (scale)**
- Load balancer — spread traffic across many app copies.
- Horizontal scaling — add more machines instead of bigger ones.
- DB sharding & partitioning — split data across many databases.
- Read replicas — extra DB copies just for reading.
- DB separation — split databases by job/service.
- CAP theorem — the trade-off between consistency, availability, partition tolerance.

(We may move an item to a different step if it fits better. That's fine.)

## Current status

- Step: 2 (Build the core). Done: food-order-api skeleton; Order Agent; Kitchen
  Agent (handle/decide/advance/get, own state; Order Agent hands off by direct
  call; /kitchen/{id} + advance; status received→cooking→ready).
- Next (confirm with user): agent #3 — Delivery Agent — to extend the chain, OR
  move to Step 3 (make it solid: idempotency, indexing, monitoring).
- Tech: Python + FastAPI, Docker, port 9595.

## When to track fully vs. go light

Not every change needs the full spec/tasks/validate workflow. Use this rule:

- **Full workflow** (/spec-r → /tasks-r → /next-r → /validate-r → commit):
  the feature takes more than one sitting, OR it teaches a new concept.
  Most features in this project fit here — that's the point.
- **Go light** (just code it + a clear commit): small tweak, rename, config
  change, or a one-file fix. Don't write 5 files for a 10-line change.

Reason: the workflow is here to help learning, not to become the project.
A heavy process the user abandons is worse than a light one they keep.

## Working style

- Keep things small. Resist scope creep.
- Working code first, polish later.
- Confirm with the user before jumping to the next step.
