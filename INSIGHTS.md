# Insights — How We Build This Project

Plain-English lessons from building the app so far. INTERVIEW.md holds *technical*
Q&A; this file holds *how we work* — the approach and the habits. Read this before
starting a new feature.

TL;DR: **Decide first. Build small. Prove it. Write it down.**

---

## 1. Decide the foundational question before any code

Every feature has one fork that changes everything downstream. Find it and settle it
*first*, with a real reason.

- Example: "Is an agent a plain service module or a real LLM?" We chose **service module
  with an LLM seam**. Picking wrong here would have wasted the whole feature.
- Do this in **plan mode** — explore, lay out trade-offs, get a yes, *then* write code.

Why: a wrong foundation is expensive to undo. A 2-minute decision saves a 2-hour rewrite.

---

## 2. One feature = one branch = one session

- Branch off `main`: `feature/<name>`. Build there. Merge back when done. Delete the branch.
- A fresh chat does **not** remember past chats. **Only files carry over.**
- So: if it matters beyond this chat, write it in a file (`CLAUDE.md`, `.claude/work/`,
  `notes.md`, `INTERVIEW.md`, this file). Don't just say it in chat.

Analogy: chat is your short-term memory; files are your notebook. Trust the notebook.

---

## 3. Follow the workflow loop

```
/spec-r   → write the plan (what + scope + success), no code
/tasks-r  → break the plan into small tasks
/next-r   → do one chunk, test it, commit
/verify-r → run the real app, walk every scenario
/validate-r → fresh agent checks code vs spec (unbiased)
/wrap-r   → record learnings, update CLAUDE.md, archive, merge
```

Use the **full loop** when a feature teaches a new concept (most of them).
**Go light** (just code + a clean commit) for a tiny tweak. Don't write 5 files for a
10-line change. The process serves the learning, not the other way round.

---

## 4. Bundle tiny tasks; each bundle ends in a test

- If tasks are very small and touch the same file, group them into a **bundle**.
- Each bundle ends with its own test — build a bit, prove it, move on.
- Example: Bundle 1 = agent core (test the agent alone), Bundle 2 = endpoints (test over
  HTTP), Bundle 3 = verify (local + Docker).

Why: fewer, meaningful checkpoints beat many micro-steps. But still test each layer so a
break is easy to locate.

---

## 5. Add a concept only when the app needs it

- We deferred real logging to Step 3, a database to Step 5, queues to Step 4.
- We added *light* stdlib logging now — just enough to see the agent work.

Why: every concept should solve a problem you actually have. Learning a tool without the
problem it solves makes the lesson shallow. Wait for the real need.

---

## 6. Build a seam for the future, not the future itself

- The agent has a `decide()` step. Today it's a plain rule. Later an LLM can replace it
  **without changing the message contract** (`handle(request) -> result`).

Why: leave a clean spot for what's coming, but don't build it early. A seam is cheap;
a half-built feature you don't need yet is waste.

---

## 7. Prove it for real, then get fresh eyes

- Unit tests are not enough. **Run the actual app** (uvicorn *and* Docker) and walk every
  success scenario by hand. Record evidence.
- Then `/validate-r` spawns a **fresh agent** that sees only the spec + code, not our
  reasoning. It catches drift and skipped requirements we're blind to.

Analogy: the cook tastes the dish (verify); a separate inspector checks it against the
recipe (validate). Two different safety nets.

---

## 8. Be honest about gaps and limits

- We *found* a logging gap during verify and fixed it instead of hiding it.
- We *wrote down* a known limit: in-memory state isn't thread-safe and dies on restart —
  that's what Step 5 (database) fixes.

Why: an honest note today is a saved debugging session tomorrow. Future-you trusts the
notes only if they're true.

---

## Reusable checklist for any new feature

1. Branch off `main` (`feature/<name>`).
2. In plan mode, settle the one foundational decision.
3. `/spec-r` → `/tasks-r` (bundle small tasks).
4. `/next-r` per bundle: build → test → commit.
5. `/verify-r`: run it for real, all scenarios.
6. `/validate-r`: fresh-eyes review.
7. `/wrap-r`: record learnings, update `CLAUDE.md`, archive, merge to `main`, delete branch.
8. Anything that matters beyond the chat → put it in a file.
