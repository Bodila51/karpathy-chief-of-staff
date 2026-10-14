---
name: hindsight
description: Grade past decisions with the benefit of hindsight (adapted from karpathy/hn-time-capsule). Reviews the decisions, predictions and bets logged in the project and scores which were prescient and which were wrong. Use weekly or after a milestone.
argument-hint: "[period, e.g. 'last 2 weeks' or 'since v1.0']"
---

# /hindsight — the time capsule (adapted from karpathy/hn-time-capsule)

Period: $ARGUMENTS (default: since the last hindsight review, or the last 14 days)

Collect the record for the period: `.cos/spec/*`, `.cos/wiki/log.md` (decisions, council verdicts), `.cos/playbook.md`, `.cos/results.tsv`, git log and merged branches, and any predictions in the specs ("this will make X faster", "users will want Y").

Then write `.cos/hindsight/<YYYY-MM-DD>.md` in 6 sections, following Karpathy's prompt structure:

1. Give a brief summary of what was decided and built in this period.
2. What ended up happening? (check the code, metrics, tests, issues: what actually shipped, what broke, what was reverted)
3. Give out awards for "Most prescient" and "Most wrong" decisions or predictions, considering what happened.
4. Mention any other notable aspects (surprises, things nobody predicted).
5. **Final grades**: an unordered list in the exact format `decision or person: grade (optional comment)`, A+ to F. Grade the agents' roles too (worker, verifier, researcher, council) by how often their output survived.
6. `Hindsight score:` 0-10 for how much this period taught us.

Finish with 1-3 lessons, and append them to `.cos/playbook.md`. If a role keeps getting low grades, propose an edit to its role file in `.cos/team/` ("skill issue first").
