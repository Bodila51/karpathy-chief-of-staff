---
name: radar
description: Daily radar of new papers, releases and repos in the user's field, ranked by what the user has liked before (idea from karpathy/arxiv-sanity-lite). Use for "what's new in X", staying current, or a morning briefing.
argument-hint: "[topic keywords] | like <arxiv id or url> | setup"
---

# /radar — stay current (idea from karpathy/arxiv-sanity-lite)

Request: $ARGUMENTS

Setup (first run or `setup`): ask the user for 3-8 topics and arXiv categories (e.g. cs.LG, cs.CL, cs.SE) and save them to `.cos/radar/topics.txt`. Papers the user marks as interesting go to `.cos/radar/likes.txt` (one arXiv id per line; `like <id>` appends one).

Run:
1. `python3 ~/.karpathy-cos/scripts/radar.py --days 2` fetches recent arXiv papers for the saved topics and ranks them by TF-IDF similarity to the liked papers (like arxiv-sanity-lite's tag-based ranking), falling back to keyword matches when there are no likes yet.
2. Also search the web for new releases in the same topics from the last 48 hours: model releases, framework releases, notable GitHub repos. Use primary sources.
3. Report the top 5-10 items: title, one plain sentence on why it matters to THIS user's project, link. Mark anything you could not verify.
4. Ask the user to `like` the ones they found useful, so tomorrow's ranking gets better.
