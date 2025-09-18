#!/usr/bin/env python3
"""
Generate a normalized articles.json from markdown files in the articles/ directory.

- Looks for title in the first markdown heading ("# Title")
- Parses **URL:** and **Published:** lines if present
- Preserves manual_title values from an existing articles.json (if present) by matching on URL or filename
- Output is a JSON array written to the --output path
"""

import argparse
import json
import re
from pathlib import Path

def parse_mdfile(path):
    data = {
        "id": None,
        "title": None,
        "url": None,
        "published": None,
        "source": None,
        "filepath": str(path),
        "manual_title": None
    }
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    # Title: first line that starts with '# '
    for line in lines:
        if line.startswith("# "):
            data["title"] = line[2:].strip()
            break
    # Look for metadata lines like "**URL:** <url>"
    for line in lines:
        m = re.match(r'^\*\*URL:\*\*\s*(.+)$', line)
        if m:
            data["url"] = m.group(1).strip()
        m2 = re.match(r'^\*\*Published:\*\*\s*(.+)$', line)
        if m2:
            data["published"] = m2.group(1).strip()
        m3 = re.match(r'^\*\*Source:\*\*\s*(.+)$', line)
        if m3:
            data["source"] = m3.group(1).strip()
    # Fallback id: filename
    data["id"] = path.name
    # If no title fallback to filename without extension
    if not data["title"]:
        data["title"] = Path(path.name).stem
    return data

def load_existing_articles(path):
    if not Path(path).exists():
        return []
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return []

def build_lookup(existing):
    # Build lookup by url, then by id
    by_url = {}
    by_id = {}
    for a in existing:
        url = a.get("url")
        if url:
            by_url[url] = a
        idv = a.get("id")
        if idv:
            by_id[idv] = a
    return by_url, by_id

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--articles-dir", default="articles")
    p.add_argument("--output", default="articles.json")
    p.add_argument("--existing", default="articles.json")
    args = p.parse_args()

    art_dir = Path(args.articles_dir)
    existing = load_existing_articles(args.existing)
    by_url, by_id = build_lookup(existing)

    md_files = sorted(art_dir.glob("*.md"))
    out = []
    for md in md_files:
        item = parse_mdfile(md)
        # preserve manual_title if it exists in existing data
        found = None
        if item.get("url") and item["url"] in by_url:
            found = by_url[item["url"]]
        elif item["id"] in by_id:
            found = by_id[item["id"]]
        if found and found.get("manual_title"):
            item["manual_title"] = found.get("manual_title")
        out.append(item)

    Path(args.output).write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(out)} entries to {args.output}")

if __name__ == "__main__":
    main()