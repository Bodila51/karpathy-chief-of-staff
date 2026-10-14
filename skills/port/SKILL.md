---
name: port
description: Safe rewrite, port or migration the way Karpathy did rustbpe. The existing code is the reference oracle, and the new code is written against equality tests until outputs match. Use for language ports, framework migrations, big refactors.
argument-hint: "<what to port, from -> to>"
---

# /port — reference + equality tests (pattern from karpathy/rustbpe)

Task: $ARGUMENTS

Karpathy: "I wrote the Python reference code personally and from scratch and I am expert there and understand it fully. I then wrote the Rust code against this implementation with tests for equality."

1. **Reference.** Identify the reference implementation (the current code). Confirm with the user that they understand it, or run `/nano` on it first. If there is no trustworthy reference, stop: build or pin one before porting.
2. **Equality harness.** Write a test harness that feeds the same inputs to old and new and asserts identical outputs. Generate many inputs: real samples, edge cases, random/fuzzed ones. This harness is the metric.
3. **Port in slices.** Dispatch `cos-worker` agents one module at a time, each with the harness as its success check. Never port everything in one go.
4. **Verify.** `cos-verifier` adds new inputs the worker did not try. Any mismatch is a fail.
5. **Done** = the harness passes on everything, the old code can be deleted, and the user signs off. Report: modules ported, number of equality cases, anything that intentionally differs.
