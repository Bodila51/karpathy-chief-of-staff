---
name: cos
description: Control panel for the Karpathy Chief of Staff - help, status, doctor, update, remove. Use when the user types /cos or asks what the Chief of Staff can do.
argument-hint: "[help | status | doctor | update | remove]"
---

# /cos — Chief of Staff control panel

Request: $ARGUMENTS (default: help)

- **help**: explain in 8 lines what the Chief of Staff does and list the commands: /council, /autoresearch, /wiki, /oracle, /hindsight, /port, /nano, /read, /radar, /score, /handoff, /gcm, /command-center, /learn. Then say: "Or just tell me what you want to build."
- **status**: for the current project, show `.cos/HELLO.md` (if any), the last 5 wiki log entries, queue top 5, playbook lesson count, and running agents.
- **doctor**: run `bash ~/.karpathy-cos/install.sh --check` and report each line in plain words. Fix what it says is fixable after the user agrees.
- **update**: `git -C ~/.karpathy-cos pull --ff-only && bash ~/.karpathy-cos/install.sh`, then show what changed (`git -C ~/.karpathy-cos log --oneline -5`).
- **remove**: confirm with the user, then `bash ~/.karpathy-cos/install.sh --remove`. Project `.cos/` folders are left untouched unless the user asks.
