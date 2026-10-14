# Karpathy Chief of Staff

A Chief of Staff for your AI agents, built for Claude Code from Andrej Karpathy's public work on agents: his posts, talks, podcasts and repos from 2023 to 2026.

It does not just hand out tasks. It decides **how much to trust agents on each task**, the way Karpathy describes it, and it runs on his own tools.

> "some layer that allows you to manage some of these AIs that are not yet perfect" — Andrej Karpathy, Dwarkesh Podcast, Oct 2025

## Install

Paste this into Claude Code:

```
Install the Karpathy Chief of Staff: clone https://github.com/Bodila51/karpathy-chief-of-staff to ~/.karpathy-cos and follow SETUP.md in it.
```

Or by hand:

```bash
git clone https://github.com/Bodila51/karpathy-chief-of-staff ~/.karpathy-cos
bash ~/.karpathy-cos/install.sh
```

Restart Claude Code, open any project, and tell it what you want to build. `/cos` lists everything.

## How it thinks

Every request goes through Karpathy's lenses first:

- **"That app shouldn't exist."** Could one call to a strong model replace what you are about to build? (his MenuGen lesson)
- **Automate what you can verify.** Agents fly where results can be checked and struggle with taste and novel code. Work is routed by that.
- **Jagged interns.** Every worker is "a brilliant PhD student and a 10-year-old" at once. Nothing a worker says counts until it is checked.
- **Nano first.** Don't understand it? Build the 150-line version first. "You can outsource your thinking but you can't outsource your understanding."
- **Simplicity criterion.** Deleting code with equal results is a win. A 2% gain for 500 lines of complexity is a reject (his llm.c rule).
- **Skill issue first.** When an agent fails, fix its instructions before blaming the model.

## How it works

1. **Ramble in, spec out.** You dump your idea; it writes the spec with you: goal, metric, boundaries.
2. **Autonomy slider.** Each task gets 1-5. Boilerplate runs alone; money, auth and user data wait for your approval.
3. **Parallel workers.** Tasks that don't collide run at the same time, each in its own git worktree, each with the coding rules.
4. **Verifier.** A separate agent tries to break every result. Worker output is untrusted until it passes.
5. **Net useful?** Bloat, defensive clutter and drive-by refactors get cut.
6. **Branch, not main.** Results land on a feature branch. You merge.
7. **Report like lunch.** Plain words, the point first, then what needs your decision.
8. **It learns.** After every task it writes lessons into the project playbook and gets better on your codebase ("system prompt learning").

## Commands (each one is one of Karpathy's repos or ideas)

| Command | From | What it does |
|---|---|---|
| `/council` | llm-council | Several models answer, rank each other anonymously, a chairman gives the verdict |
| `/autoresearch` | autoresearch | Overnight loop: edit, run, keep or revert, log, never stop. Any goal with a number |
| `/wiki` | llm-wiki gist | Project memory the agent writes and maintains: ingest, query, lint |
| `/oracle` | rendergit | Packs the whole repo into one file for the strongest model's hardest question |
| `/hindsight` | hn-time-capsule | Grades your past decisions with hindsight: most prescient, most wrong |
| `/port` | rustbpe | Rewrites and migrations against a reference with equality tests |
| `/nano` | micrograd, microgpt | Understand anything by building the smallest working version |
| `/read` | reader3 | Read docs, papers and books together, chapter by chapter |
| `/radar` | arxiv-sanity-lite | New papers and releases in your field, ranked by what you liked |
| `/score` | jobs | Scores the backlog 0-10 with a strict rubric |
| `/handoff` | HELLO.md gist | A note to the next session so context survives |
| `/gcm` | gcm gist | Commit message; you accept, edit, regenerate or cancel |
| `/command-center` | his "agent command center" posts | See every running agent, stop the stuck ones, re-brief |
| `/learn` | micrograd → nanochat | Zero to Hero, hands-on |
| `/cos` | | help, status, doctor, update, remove |

Every worker also gets the four coding rules (Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution) from [andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) by Forrest Chang, based on Karpathy's January 2026 notes.

## What you need

- Claude Code. Parallel agents use a lot of tokens; a Max plan is recommended.
- git. Python 3 for /oracle, /radar and the cross-provider council.
- Optional: `OPENROUTER_API_KEY` (as an environment variable) for a council across GPT, Gemini, Claude and Grok; `tmux` for the live command center.
- /autoresearch runs while your computer is on.

## Files

```
brain/BRAIN.md        how the Chief of Staff thinks and works
rules/CODING-RULES.md the four rules every worker follows
agents/               worker, verifier, researcher, council member
skills/               the 15 commands
scripts/              pack.py, radar.py, council_openrouter.py, command-center.sh
install.sh            install / --check / --remove
```

Your project's state lives in `.cos/` inside each project: specs, queue, playbook, wiki, results.

---

Built from Andrej Karpathy's public posts, talks and open-source repos. Not affiliated with or endorsed by Andrej Karpathy or Anthropic.
