---
name: command-center
description: See and steer all running agents in one view, the "agent command center" Karpathy asked for. Shows what each agent is doing, which are idle or stuck, and lets the user pitch in. Use when several agents are running.
---

# /command-center — all agents at a glance

Karpathy: "I want nice, interactive sessions running in tmux so that I can see what they are doing, pitch in, etc." and "I want to see/hide toggle them, see if any are idle".

1. List every agent you launched in this session that is still running or recently finished: name/role, task (one line), state (running / idle / stuck / done / failed), how long, last output line, branch or worktree.
2. Flag: idle agents (give them the next queue item or stop them), agents looping or repeating themselves (stop and re-brief), finished results waiting for the verifier.
3. Show the queue (`.cos/queue.md`) top 5 and token/usage notes if available.
4. Offer actions in one line each: stop X, re-brief Y, send next task to Z, show diff of W.

Optional live view: if `tmux` is installed, offer `bash ~/.karpathy-cos/scripts/command-center.sh`, which opens a tmux grid with one pane per git worktree (`git worktree list`) showing `git log -1` and `git status` refreshing every few seconds, plus one pane tailing `.cos/wiki/log.md`.
