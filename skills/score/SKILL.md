---
name: score
description: Score and rank a list of tasks, ideas or options 0-10 with a strict, parseable rubric (pattern from karpathy/jobs scoring pipeline). Use when the backlog is long and priority is unclear.
argument-hint: "[file with items | 'queue'] [criterion]"
---

# /score — rank the backlog (pattern from karpathy/jobs)

Input: $ARGUMENTS (default: `.cos/queue.md`, criterion: value to the user's current goal divided by effort and risk)

Karpathy's jobs repo scores every item independently with the same prompt and a strict JSON answer, so the scores are comparable. Do the same:

1. Agree the criterion in one line with the user (or use the default) and write a 0-10 rubric: what a 0, 5 and 10 look like.
2. Score each item independently (parallel subagents for long lists, `haiku` is enough), each returning ONLY:
   `{ "score": <0-10>, "rationale": "<2-3 sentences explaining the key factors>" }`
3. Sort by score. Show a table: item, score, one-line rationale.
4. Flag ties and items the scorers were unsure about for the user to decide.
5. Rewrite `.cos/queue.md` in the new order only after the user agrees.
