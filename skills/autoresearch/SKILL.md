---
name: autoresearch
description: Karpathy's autoresearch loop applied to any goal with a cheap, objective metric (speed, size, test pass rate, score). An agent edits one file, runs a fixed-budget experiment, keeps or reverts, logs every run, and keeps going while you sleep. Use when the user wants something optimized overnight.
argument-hint: "<goal and metric, e.g. 'make /search faster, metric: p50 ms from bench.sh'>"
---

# /autoresearch — the overnight loop (from karpathy/autoresearch program.md)

Goal: $ARGUMENTS

"If you can't evaluate, you can't autoresearch it." First make sure the metric is real.

## Setup (with the user, then never ask again)
1. **Metric.** One number, one command that prints it, lower-or-higher-is-better stated. Run it twice; if the two numbers differ a lot, make the measurement stable first (more iterations, fixed seed, warmup).
2. **Budget.** A fixed time budget per experiment (default 5 minutes). Anything over 2x the budget is killed and counted as a failure.
3. **In-scope files.** The ONE file (or small set) the agent may edit. Everything else, including the metric/eval code, is read-only. No new dependencies.
4. **Branch.** Agree a run tag from today's date (e.g. `oct14`). `git checkout -b autoresearch/<tag>` from the current main. The branch must not already exist.
5. **Log.** Create `.cos/results.tsv` with the header `commit	metric	status	description` (tab-separated; do not commit it).
6. **Baseline.** First run is always the unchanged code.
Write all of this into `.cos/spec/autoresearch-<tag>.md` and get one "go" from the user.

## The loop (verbatim rules from program.md, adapted)
LOOP FOREVER:
1. Look at the git state.
2. Change the in-scope file with one experimental idea.
3. git commit.
4. Run the experiment with output redirected to `run.log` (do NOT let output flood your context).
5. Read the metric from the log. If it is missing, the run crashed: read `tail -n 50 run.log`, fix if it is something dumb, otherwise log `crash` and move on.
6. Record the run in `.cos/results.tsv` (short commit, metric, keep/discard/crash, description).
7. If the metric improved, keep the commit and advance the branch. If equal or worse, `git reset` back.

**Simplicity criterion:** "All else being equal, simpler is better. A small improvement that adds ugly complexity is not worth it. Conversely, removing something and getting equal or better results is a great outcome." Weigh complexity cost against gain.

**NEVER STOP:** once the loop has begun, do not ask the user whether to continue. "The human might be asleep." If you run out of ideas, think harder: re-read the in-scope files, combine near-misses, try more radical changes.

Prefer running this in an interactive terminal session (tmux) so the user can watch and pitch in, not headless.

## Morning report
When the user returns: the best metric vs baseline, the kept changes as a short list (one line each, with the reason they helped), the number of experiments, and the branch name to review. The user merges; you don't.
