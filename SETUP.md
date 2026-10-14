# SETUP — instructions for Claude Code

You are installing the Karpathy Chief of Staff for the user. Follow these steps in order. Keep the user informed in one short line per step.

1. **Check the basics.** Run `git --version` and `python3 --version`. If git is missing, stop and tell the user how to install it for their OS. Python 3 is only needed for /oracle, /radar and the cross-provider /council; continue without it but tell the user.

2. **Get the code** into `~/.karpathy-cos`:
   - If `~/.karpathy-cos` does not exist: `git clone https://github.com/Bodila51/karpathy-chief-of-staff ~/.karpathy-cos`
   - If it exists and is this repo: `git -C ~/.karpathy-cos pull --ff-only`
   - If it exists and is something else: stop and ask the user.

3. **Install**: `bash ~/.karpathy-cos/install.sh`
   It copies 15 skills to `~/.claude/skills/`, 4 agents to `~/.claude/agents/`, and adds one import block to `~/.claude/CLAUDE.md`:
   ```
   <!-- karpathy-cos:start -->
   @~/.karpathy-cos/brain/BRAIN.md
   <!-- karpathy-cos:end -->
   ```
   It never overwrites a skill the user already has with the same name (it prints SKIP). Show the user the check output.

4. **Optional extras** (ask once, in one message, skip if the user says no):
   - Cross-provider /council: the user sets `OPENROUTER_API_KEY` as an environment variable in their shell profile. Never ask them to paste the key into chat.
   - Live /command-center: `tmux` (macOS: `brew install tmux`).

5. **Finish.** Tell the user, in this order:
   - Restart Claude Code (or open a new session) so the brain, skills and agents load.
   - Open Claude Code inside any project and just say what you want to build. The Chief of Staff plans it with you, rates how much autonomy agents get, dispatches workers in parallel, has every result attacked by a verifier, and reports back in plain words.
   - `/cos` shows all commands. Start with `/council` on a real decision, or `/nano` on something you want to understand.
   - Update any time with `/cos update`. Remove with `/cos remove`.

Do not modify any of the user's existing files other than appending the import block to `~/.claude/CLAUDE.md`.
