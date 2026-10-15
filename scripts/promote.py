#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Promotion toolkit for the China Travel Guide site.

Three promotion channels that work without any account:
  1. IndexNow ping (Bing/Yandex/Seznam) — instant indexing
  2. Sitemap ping (Google/Bing deprecate this, but harmless)
  3. Social-share link generation (no API needed — 老板 posts manually)

Usage:
    python3 scripts/promote.py indexnow          # submit all URLs to IndexNow
    python3 scripts/promote.py indexnow <slug>   # submit one article URL
    python3 scripts/promote.py share <slug>      # print ready-to-post social copy
    python3 scripts/promote.py channels          # list promotion channels + status
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

HOST = "china-travel-guide-ne9.pages.dev"
SITE = f"https://{HOST}"
KEY = "fdb0af5235c8da09b83b1605116a99ea"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTICLES = os.path.join(ROOT, "src", "content", "articles")


def parse_frontmatter(path):
    """Minimal frontmatter parser (title/description/tags)."""
    fm = {}
    with open(path) as f:
        text = f.read()
    if not text.startswith("---"):
        return fm
    end = text.find("\n---", 3)
    if end == -1:
        return fm
    block = text[3:end]
    cur_key = None
    for line in block.split("\n"):
        if not line.strip():
            continue
        if line.startswith("  - ") or line.startswith("    "):
            continue
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            cur_key = k.strip()
            v = v.strip().strip('"').strip("'")
            if v:
                fm[cur_key] = v
    return fm


def indexnow(urls):
    payload = json.dumps({
        "host": HOST,
        "key": KEY,
        "keyLocation": f"{SITE}/{KEY}.txt",
        "urlList": urls,
    }).encode()
    ok = False
    for ep in ["https://api.indexnow.org/indexnow", "https://www.bing.com/indexnow"]:
        req = urllib.request.Request(
            ep, data=payload, method="POST",
            headers={"Content-Type": "application/json; charset=utf-8",
                     "User-Agent": "IndexNow/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                print(f"{ep} -> HTTP {r.status}")
                ok = ok or r.status in (200, 202)
        except Exception as e:
            print(f"{ep} -> {e}")
    return ok


def share_copy(slug):
    path = os.path.join(ARTICLES, f"{slug}.md")
    if not os.path.exists(path):
        print(f"not found: {path}")
        return 1
    fm = parse_frontmatter(path)
    title = fm.get("title", slug)
    desc = fm.get("description", "")
    url = f"{SITE}/guides/{slug}/"
    print("=" * 60)
    print("POST COPY (copy-paste to social/forum):")
    print("=" * 60)
    print()
    print(f"{title}")
    print()
    print(f"{desc}")
    print()
    print(f"Read the full guide: {url}")
    print()
    print("-" * 60)
    print("SUGGESTED CHANNELS:")
    print("  • Reddit: r/China, r/travel, r/ChinaTravel  (share as text post + link)")
    print("  • Facebook groups: 'China Travel', 'Backpacking China'")
    print("  • Quora: answer questions about China travel, link the guide")
    print("  • Pinterest: pin the guide image + link")
    print("  • Twitter/X: short hook + link")
    print("  • Forums: TripAdvisor China forum, Lonely Planet Thorn Tree")
    print()
    print(f"SHORT HOOK (<=280 chars, for Twitter/X):")
    hook = f"{title[:120]} — {desc[:100]} {url}"
    print(f"  {hook[:280]}")
    return 0


CHANNELS = [
    ("IndexNow (Bing/Yandex)", "automated", "scripts/promote.py indexnow", "free, no account"),
    ("Google Search Console", "manual", "https://search.google.com/search-console",
     "老板/大富 adds pages.dev property manually"),
    ("Bing Webmaster Tools", "manual", "https://www.bing.com/webmasters",
     "import from GSC or add manually"),
    ("Reddit (r/China, r/travel)", "manual", "scripts/promote.py share <slug>",
     "blocked from this box; 老板 posts"),
    ("Quora answers", "manual", "scripts/promote.py share <slug>", "high-intent traffic"),
    ("Pinterest", "manual", "scripts/promote.py share <slug>", "travel pinning"),
    ("Facebook travel groups", "manual", "scripts/promote.py share <slug>", "large reach"),
    ("TripAdvisor China forum", "manual", "scripts/promote.py share <slug>", "travel-intent"),
    ("RSS feed (aggregators)", "automated", f"{SITE}/rss.xml", "live, 35+ items"),
]


def channels():
    print(f"{'CHANNEL':<32} {'TYPE':<10} {'HOW'}")
    print("-" * 90)
    for name, typ, how, note in CHANNELS:
        print(f"{name:<32} {typ:<10} {how}")
    print()
    print("MANUAL channels need 老板/大富 to post (account required, blocked from box).")
    print("AUTOMATED channels run from scripts/ and are wired into cron.")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "channels"
    if cmd == "indexnow":
        if len(sys.argv) > 2:
            slug = sys.argv[2]
            urls = [f"{SITE}/guides/{slug}/"]
        else:
            req = urllib.request.Request(f"{SITE}/sitemap-0.xml",
                                         headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                xml = r.read().decode("utf-8", "replace")
            import re
            urls = re.findall(r"<loc>(.*?)</loc>", xml)
        print(f"submitting {len(urls)} url(s)")
        ok = indexnow(urls)
        print("RESULT:", "OK" if ok else "FAILED")
        return 0 if ok else 1
    if cmd == "share":
        if len(sys.argv) < 3:
            print("usage: promote.py share <slug>")
            return 1
        return share_copy(sys.argv[2])
    if cmd == "channels":
        channels()
        return 0
    print(f"unknown command: {cmd}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
