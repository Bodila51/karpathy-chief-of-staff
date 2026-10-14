#!/usr/bin/env python3
"""Rank recent arXiv papers by similarity to papers you liked (idea from arxiv-sanity-lite).

Reads .cos/radar/topics.txt (one topic or arXiv category per line, e.g. "cs.CL" or "coding agents")
and .cos/radar/likes.txt (arXiv ids). Prints the top papers. Stdlib only.
Usage: python3 radar.py [--days 2] [--top 15]
"""
import argparse, math, re, sys, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime, timedelta, timezone

NS = {"a": "http://www.w3.org/2005/Atom"}
API = "https://export.arxiv.org/api/query?"
STOP = set("a an the of and or for to in on with by from is are we our this that these using via as at be can it its into than which".split())

def fetch(query, n):
    url = API + urllib.parse.urlencode({"search_query": query, "start": 0, "max_results": n, "sortBy": "submittedDate", "sortOrder": "descending"})
    with urllib.request.urlopen(url, timeout=60) as r:
        root = ET.fromstring(r.read())
    papers = []
    for e in root.findall("a:entry", NS):
        pid = e.find("a:id", NS).text.rsplit("/abs/", 1)[-1]
        papers.append({
            "id": re.sub(r"v\d+$", "", pid),
            "title": " ".join(e.find("a:title", NS).text.split()),
            "summary": " ".join(e.find("a:summary", NS).text.split()),
            "published": e.find("a:published", NS).text,
        })
    return papers

def query_for(topic):
    topic = topic.strip()
    if re.fullmatch(r"[a-z\-]+\.[A-Za-z\-]+", topic):
        return f"cat:{topic}"
    return f'all:"{topic}"' if " " in topic else f"all:{topic}"

def tokens(text):
    return [w for w in re.findall(r"[a-z][a-z0-9\-]+", text.lower()) if w not in STOP and len(w) > 2]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=2)
    ap.add_argument("--top", type=int, default=15)
    ap.add_argument("--dir", default=".cos/radar")
    a = ap.parse_args()
    try:
        topics = [t for t in open(f"{a.dir}/topics.txt").read().splitlines() if t.strip() and not t.startswith("#")]
    except FileNotFoundError:
        sys.exit("radar.py: no .cos/radar/topics.txt yet - run /radar setup first")
    try:
        likes = [l.strip() for l in open(f"{a.dir}/likes.txt").read().splitlines() if l.strip()]
    except FileNotFoundError:
        likes = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=a.days)
    pool = {}
    for t in topics:
        try:
            got = fetch(query_for(t), 100)
        except Exception as e:
            sys.exit(f"radar.py: could not reach arXiv ({e}). Check your internet connection.")
        for p in got:
            if datetime.fromisoformat(p["published"].replace("Z", "+00:00")) >= cutoff:
                pool[p["id"]] = p
    if not pool:
        print(f"No new papers in the last {a.days} day(s) for these topics.")
        return
    liked_docs = []
    if likes:
        url = API + urllib.parse.urlencode({"id_list": ",".join(likes[-50:]), "max_results": 50})
        with urllib.request.urlopen(url, timeout=60) as r:
            root = ET.fromstring(r.read())
        liked_docs = [tokens(e.find("a:title", NS).text + " " + e.find("a:summary", NS).text) for e in root.findall("a:entry", NS)]
    docs = {pid: tokens(p["title"] + " " + p["summary"]) for pid, p in pool.items()}
    all_docs = list(docs.values()) + liked_docs
    df = Counter(w for d in all_docs for w in set(d))
    N = len(all_docs)
    def vec(d):
        tf = Counter(d)
        v = {w: (c / len(d)) * math.log((1 + N) / (1 + df[w])) for w, c in tf.items()} if d else {}
        n = math.sqrt(sum(x * x for x in v.values())) or 1.0
        return {w: x / n for w, x in v.items()}
    if liked_docs:
        centroid = Counter()
        for d in liked_docs:
            for w, x in vec(d).items():
                centroid[w] += x / len(liked_docs)
        score = lambda d: sum(x * centroid.get(w, 0.0) for w, x in vec(d).items())
        mode = f"similarity to {len(liked_docs)} liked papers"
    else:
        kw = set(w for t in topics for w in tokens(t))
        score = lambda d: sum(1 for w in d if w in kw) / (len(d) or 1)
        mode = "keyword match (like some papers to personalize)"
    ranked = sorted(pool.values(), key=lambda p: -score(docs[p["id"]]))[: a.top]
    print(f"{len(pool)} new papers in the last {a.days} day(s); ranked by {mode}\n")
    for i, p in enumerate(ranked, 1):
        print(f"{i}. {p['title']}\n   https://arxiv.org/abs/{p['id']}  ({p['published'][:10]})\n   {p['summary'][:220]}...\n")

if __name__ == "__main__":
    main()
