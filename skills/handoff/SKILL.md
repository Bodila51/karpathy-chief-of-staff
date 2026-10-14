---
name: handoff
description: End-of-session handoff note for the next agent session, so context survives (inspired by the HELLO.md note Claude left for its future instances, published by Karpathy). Use at the end of a work session or before a context reset.
---

# /handoff — a note to the next session

Agents start every session "from scratch". Leave the next one a note.

Write `.cos/HELLO.md` (overwrite; keep the previous one as `.cos/hello-archive/<date>.md`):

```
# Hello, next session
Written: <date time>

## Where we are
<2-4 lines: goal, current state, branch>

## In flight
<running or half-done work, which agent, where its output is>

## Decisions made (and why)
<bullets, link to specs / council verdicts>

## Open questions for the human
<bullets>

## Next 3 steps
1.
2.
3.

## Watch out
<traps, flaky tests, things that look done but aren't>
```

Also append the session's lessons to `.cos/playbook.md` and a `## [YYYY-MM-DD] handoff | <title>` line to `.cos/wiki/log.md`. Then tell the user in 3 lines what the next session will pick up.
