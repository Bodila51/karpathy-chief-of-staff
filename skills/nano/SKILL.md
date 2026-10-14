---
name: nano
description: Understand anything by building the smallest working version from scratch, Karpathy's micrograd / microgpt way. Use when the user (or the Chief of Staff) doesn't really understand a mechanism, a library, or a piece of the codebase.
argument-hint: "<concept, library, or part of the codebase>"
---

# /nano — build it small to understand it (micrograd, minbpe, nanoGPT, microgpt)

Topic: $ARGUMENTS

Karpathy's way: the most atomic version that still works, no dependencies, read top to bottom in one sitting.

1. Ask the user in one line what they already know about it, so you start at the right level.
2. Write `.cos/nano/<topic>/` with ONE file of 50-200 lines that captures the core mechanism and actually runs. No frameworks, no abstractions, comments only where the idea lives.
3. Run it and show the output.
4. Walk the user through it in order, the way Karpathy does in his videos: what each block does and why it is needed. Then show where the real library or the real codebase does the same thing (file:line), and what it adds on top.
5. Give the user one small change to try themselves and predict the result before running it.
6. File a short page in `.cos/wiki/` so the understanding persists.

"You can outsource your thinking but you can't outsource your understanding."
