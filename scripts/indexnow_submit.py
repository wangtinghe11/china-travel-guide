#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Submit all site URLs to IndexNow (Bing/Yandex/etc.) for instant indexing.

IndexNow is free, needs no account, and supports *.pages.dev.
Reads URLs from the live sitemap, POSTs them in batches.

Usage:
    python3 scripts/indexnow_submit.py            # submit all URLs from live sitemap
    python3 scripts/indexnow_submit.py <url> ...  # submit specific URLs
"""
import json
import sys
import urllib.error
import urllib.request

HOST = "china-travel-guide-ne9.pages.dev"
SITE = f"https://{HOST}"
KEY = "fdb0af5235c8da09b83b1605116a99ea"
KEY_LOCATION = f"{SITE}/{KEY}.txt"

# IndexNow accepts api.indexnow.org (shared) or per-engine endpoints.
ENDPOINTS = [
    "https://api.indexnow.org/indexnow",
    "https://www.bing.com/indexnow",
]


def fetch_sitemap_urls():
    """Read all <loc> URLs from the live sitemap."""
    req = urllib.request.Request(
        f"{SITE}/sitemap-0.xml",
        headers={"User-Agent": "Mozilla/5.0 (compatible; IndexNow/1.0)"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        xml = r.read().decode("utf-8", errors="replace")
    import re

    urls = re.findall(r"<loc>(.*?)</loc>", xml)
    return urls


def submit(urls):
    if not urls:
        print("no urls to submit")
        return 0
    payload = json.dumps({
        "host": HOST,
        "key": KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls,
    }).encode()
    ok = 0
    for ep in ENDPOINTS:
        req = urllib.request.Request(
            ep, data=payload, method="POST",
            headers={"Content-Type": "application/json; charset=utf-8",
                     "User-Agent": "IndexNow/1.0"},
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                code = r.status
            # 200 = OK, 202 = accepted (key validation pending)
            print(f"{ep} -> HTTP {code} ({len(urls)} urls)")
            if code in (200, 202):
                ok += 1
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")[:200]
            print(f"{ep} -> HTTP {e.code} {body}")
        except Exception as e:
            print(f"{ep} -> ERROR {e}")
    return ok


def main():
    if len(sys.argv) > 1:
        urls = [u if u.startswith("http") else f"{SITE}{u}" for u in sys.argv[1:]]
    else:
        urls = fetch_sitemap_urls()
        print(f"fetched {len(urls)} urls from sitemap")
    ok = submit(urls)
    print("RESULT:", "OK" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
