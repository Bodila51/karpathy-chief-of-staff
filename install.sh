#!/usr/bin/env bash
# Karpathy Chief of Staff installer for Claude Code.
#   bash install.sh           install or update (idempotent)
#   bash install.sh --check   report what is installed
#   bash install.sh --remove  uninstall (project .cos/ folders are not touched)
set -euo pipefail

HOME_DIR="$HOME/.karpathy-cos"
CLAUDE_DIR="$HOME/.claude"
SKILLS_DIR="$CLAUDE_DIR/skills"
AGENTS_DIR="$CLAUDE_DIR/agents"
MEMORY="$CLAUDE_DIR/CLAUDE.md"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
START="<!-- karpathy-cos:start -->"
END="<!-- karpathy-cos:end -->"
MARK=".karpathy-cos"

say() { printf '%s\n' "$*"; }
ok() { printf '  OK    %s\n' "$*"; }
bad() { printf '  MISS  %s\n' "$*"; }

strip_block() {
  [ -f "$MEMORY" ] || return 0
  awk -v s="$START" -v e="$END" '$0==s{skip=1;next} $0==e{skip=0;next} !skip' "$MEMORY" > "$MEMORY.tmp" && mv "$MEMORY.tmp" "$MEMORY"
}

check() {
  say "Karpathy Chief of Staff - check"
  [ -f "$HOME_DIR/brain/BRAIN.md" ] && ok "brain at ~/.karpathy-cos/brain/BRAIN.md" || bad "brain (~/.karpathy-cos missing)"
  grep -qF "$START" "$MEMORY" 2>/dev/null && ok "brain imported in ~/.claude/CLAUDE.md" || bad "import line in ~/.claude/CLAUDE.md"
  for d in "$SRC"/skills/*/; do n=$(basename "$d"); [ -f "$SKILLS_DIR/$n/$MARK" ] && ok "/$n" || bad "/$n"; done
  for f in "$SRC"/agents/*.md; do n=$(basename "$f"); [ -f "$AGENTS_DIR/$n" ] && ok "agent ${n%.md}" || bad "agent ${n%.md}"; done
  command -v git >/dev/null && ok "git" || bad "git (required)"
  command -v python3 >/dev/null && ok "python3" || bad "python3 (needed for /oracle, /radar, cross-provider /council)"
  command -v tmux >/dev/null && ok "tmux (optional, live /command-center)" || say "  --    tmux not installed (optional)"
  [ -n "${OPENROUTER_API_KEY:-}" ] && ok "OPENROUTER_API_KEY set (cross-provider /council)" || say "  --    OPENROUTER_API_KEY not set (optional; /council uses Claude models)"
}

remove() {
  for d in "$SRC"/skills/*/; do n=$(basename "$d"); [ -f "$SKILLS_DIR/$n/$MARK" ] && rm -rf "${SKILLS_DIR:?}/$n"; done
  for f in "$SRC"/agents/*.md; do rm -f "$AGENTS_DIR/$(basename "$f")"; done
  strip_block
  say "Removed skills, agents and the brain import. ~/.karpathy-cos and project .cos/ folders were left in place."
}

install() {
  # make sure the repo is reachable at ~/.karpathy-cos (paths in the brain and skills point there)
  if [ "$SRC" != "$HOME_DIR" ] && [ ! -e "$HOME_DIR" ]; then ln -s "$SRC" "$HOME_DIR"; fi
  mkdir -p "$SKILLS_DIR" "$AGENTS_DIR"
  for d in "$SRC"/skills/*/; do
    n=$(basename "$d")
    if [ -e "$SKILLS_DIR/$n" ] && [ ! -f "$SKILLS_DIR/$n/$MARK" ]; then
      say "  SKIP  /$n (you already have a different skill with this name; left it alone)"; continue
    fi
    rm -rf "${SKILLS_DIR:?}/$n"; cp -R "$d" "$SKILLS_DIR/$n"; touch "$SKILLS_DIR/$n/$MARK"
  done
  cp "$SRC"/agents/*.md "$AGENTS_DIR"/
  touch "$MEMORY"; strip_block
  [ -s "$MEMORY" ] && [ -n "$(tail -c1 "$MEMORY")" ] && printf '\n' >> "$MEMORY"
  printf '%s\n@~/.karpathy-cos/brain/BRAIN.md\n%s\n' "$START" "$END" >> "$MEMORY"
  chmod +x "$SRC"/scripts/*.sh "$SRC"/scripts/*.py 2>/dev/null || true
  say "Installed. Restart Claude Code, then type /cos"
  check
}

case "${1:-}" in
  --check) check ;;
  --remove) remove ;;
  "") install ;;
  *) say "usage: install.sh [--check|--remove]"; exit 1 ;;
esac
