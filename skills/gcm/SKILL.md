---
name: gcm
description: Write the commit message for the staged changes and let the user accept, edit, regenerate or cancel (Karpathy's gcm gist). Use when committing.
---

# /gcm — git commit message (from Karpathy's gcm gist)

1. Run `git diff --cached`. If nothing is staged, say so and stop.
2. Generate the message using Karpathy's prompt:
   "Below is a diff of all staged changes, coming from the command: `git diff --cached`. Please generate a concise, one-line commit message for these changes."
   If the repo's history uses a convention (e.g. `feat:`), follow it.
3. Show the message and ask: accept / edit / regenerate / cancel.
4. Only on accept (or after the user's edit) run `git commit -m "<message>"`. Never commit without that answer.
