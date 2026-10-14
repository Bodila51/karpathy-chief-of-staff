---
name: read
description: Read a document, paper, book or long docs together with the LLM, one chapter at a time (pattern from karpathy/reader3). Use when the user wants to actually understand a text, not just get a summary.
argument-hint: "<file path or URL>"
---

# /read — don't read alone (pattern from karpathy/reader3)

Source: $ARGUMENTS

Karpathy: "Don't read books alone." Models know a book only hazily, so load the actual text into context instead of relying on memory.

1. Get the text (file, URL, EPUB, PDF) and save it to `.cos/raw/`. Split it into chapters or sections. Show the table of contents.
2. For the current section: a 5-line summary first so the user knows what is coming, then they read, then you discuss. Answer questions only from the loaded text plus clearly marked outside knowledge.
3. Track progress in `.cos/raw/<name>.progress.md` (current section, open questions).
4. After each section, offer to file key ideas into the wiki (/wiki ingest).
