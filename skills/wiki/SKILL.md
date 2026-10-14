---
name: wiki
description: Project memory using Karpathy's llm-wiki pattern. The agent keeps a persistent, interlinked markdown wiki in .cos/wiki (ingest sources, answer queries from it, lint it). Use to store decisions, research, docs, meeting notes, and to answer "what do we know about X".
argument-hint: "ingest <file|url|text> | query <question> | lint"
---

# /wiki — the project wiki (pattern from Karpathy's llm-wiki gist)

Request: $ARGUMENTS

Three layers:
- **Raw sources** in `.cos/raw/`: documents, notes, transcripts, URLs saved as markdown. Immutable: read, never edit.
- **The wiki** in `.cos/wiki/`: markdown pages you write and own (summaries, entity pages, concept pages, decisions, comparisons). The user reads; you write.
- **The schema**: this file plus `.cos/wiki/SCHEMA.md` (create it on first use: page types, naming, conventions for this project). Co-evolve it with the user.

Two special files:
- `.cos/wiki/index.md`: catalog of every page with a link and a one-line summary, grouped by category. Read it first on every query.
- `.cos/wiki/log.md`: append-only, each entry starts with `## [YYYY-MM-DD] <op> | <title>` so `grep "^## \[" .cos/wiki/log.md | tail -5` shows the last 5.

## Operations
- **ingest**: save the source to `.cos/raw/`, read it, tell the user the 3-5 key takeaways, write a summary page, update every related page (a source may touch 10-15 pages), note contradictions with older claims, update index.md, append to log.md.
- **query**: read index.md, open the relevant pages, answer with citations to wiki pages and raw sources. If the answer is valuable (a comparison, an analysis, a connection), file it back as a new page.
- **lint**: find contradictions, stale claims, orphan pages, concepts mentioned without their own page, missing cross-links, and gaps a web search could fill. Fix what is safe, list the rest, suggest new questions and sources.

No argument: show the last 5 log entries and the index categories.
