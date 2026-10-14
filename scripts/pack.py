#!/usr/bin/env python3
"""Pack a git repo into one text file for an LLM (like rendergit's "LLM view").

Usage: python3 pack.py [repo_dir] [--include DIR ...] [--max-kb 200]
Writes the pack to stdout and a size/token estimate to stderr.
"""
import argparse, os, subprocess, sys

def is_binary(path):
    try:
        with open(path, "rb") as f:
            return b"\0" in f.read(8192)
    except OSError:
        return True

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", nargs="?", default=".")
    ap.add_argument("--include", action="append", default=[], help="only files under this path (repeatable)")
    ap.add_argument("--max-kb", type=int, default=200, help="skip files larger than this")
    a = ap.parse_args()
    try:
        files = subprocess.run(["git", "-C", a.repo, "ls-files"], capture_output=True, text=True, check=True).stdout.splitlines()
    except (subprocess.CalledProcessError, FileNotFoundError):
        sys.exit("pack.py: not a git repo (run inside a git repository)")
    if a.include:
        files = [f for f in files if any(f == p.rstrip("/") or f.startswith(p.rstrip("/") + "/") for p in a.include)]
    out, skipped, total = [], [], 0
    for rel in files:
        path = os.path.join(a.repo, rel)
        if not os.path.isfile(path):
            continue
        size = os.path.getsize(path)
        if size > a.max_kb * 1024 or is_binary(path):
            skipped.append(rel)
            continue
        with open(path, encoding="utf-8", errors="replace") as f:
            text = f.read()
        out.append(f'<document path="{rel}">\n{text}\n</document>')
        total += len(text)
    tree = "\n".join(f for f in files if f not in skipped)
    sys.stdout.write(f"<repository>\n<tree>\n{tree}\n</tree>\n" + "\n".join(out) + "\n</repository>\n")
    sys.stderr.write(f"pack.py: {len(out)} files, {total/1024:.0f} KB, ~{total//4:,} tokens; skipped {len(skipped)} (binary or > {a.max_kb} KB)\n")

if __name__ == "__main__":
    main()
