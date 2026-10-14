---
name: oracle
description: Ask the hardest question with the whole codebase in one context. Packs the repo into a single text file (rendergit-style LLM view) and hands it to the strongest model. Use for cross-cutting bugs, architecture questions, or "how does all of this fit together".
argument-hint: "<the hard question>"
---

# /oracle — whole repo, one head (pattern from karpathy/rendergit + his "GPT-5 Pro as the final layer")

Question: $ARGUMENTS

1. Pack the repo: `python3 ~/.karpathy-cos/scripts/pack.py . > .cos/oracle-pack.txt` (respects .gitignore via `git ls-files`, skips binaries and files over 200 KB, prints a token estimate to stderr).
2. If the pack is too big for one context, re-run with `--include <dir>` for the relevant parts, or `--max-kb` lower. Tell the user what was left out.
3. Launch one subagent on the strongest model available (`opus`, or `fable` if the user has it) with: the pack file path, the question, and the instruction "Read the whole pack before answering. Cite file:line for every claim. Separate what you observed from what you infer."
4. Also tell the user they can paste `.cos/oracle-pack.txt` into any other top model (e.g. a "Pro" tier chat) as a second opinion. Karpathy keeps such a model as his "final layer of defense ... for the hardest things".
5. Report the answer in plain words first, then the cited evidence. Add it to the wiki if it is worth keeping.
