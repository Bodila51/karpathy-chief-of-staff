#!/usr/bin/env bash
# Live tmux view of all agent worktrees + the project log ("agent command center").
set -euo pipefail
command -v tmux >/dev/null || { echo "tmux is not installed (macOS: brew install tmux)"; exit 1; }
ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || { echo "Run this inside a git repository"; exit 1; }
S=cos-center
loop() { printf 'while true; do clear; %s; sleep 5; done' "$1"; }
tmux kill-session -t "$S" 2>/dev/null || true
tmux new-session -d -s "$S" -c "$ROOT" "bash -c \"$(loop 'echo PROJECT LOG; tail -n 30 .cos/wiki/log.md 2>/dev/null || echo no .cos/wiki/log.md yet')\""
git worktree list --porcelain | awk '/^worktree /{print $2}' | while read -r wt; do
  tmux split-window -t "$S" -c "$wt" "bash -c \"$(loop 'pwd; git log -1 --oneline; git status --short | head -20')\""
  tmux select-layout -t "$S" tiled >/dev/null
done
exec tmux attach -t "$S"
