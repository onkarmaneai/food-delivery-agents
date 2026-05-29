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

## Also learning in this project

Alongside the multi-agent system, we are learning two Claude Code features:

- **Subagents** — smaller helper agents that do one focused job and report back.
- **Skills** — reusable, named instructions/commands the agent can invoke.

When these come up naturally in the build, pause and explain them in plain English.

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

- Step: 1 (Pick & sketch) — system chosen: **Food delivery**.
- Next: sketch the 3 agents, then start first feature with /spec-r.
- Tech: Python. Docker comes at step 4.

## Working style

- Keep things small. Resist scope creep.
- Working code first, polish later.
- Confirm with the user before jumping to the next step.
