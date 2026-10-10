#!/usr/bin/env python3
"""Full-site verification probe for the China Travel Guide static site (dist/).

Run from /root/china_travel_guide after `npm run build`:
    python3 scripts/verify_site.py

Checks (mirrors the QA pass reported to 大富):
1. Every HTML page returns HTTP 200 (spins up a local http.server on a free port)
2. No broken internal links (href="/..." resolves to a file in dist/)
3. Every article has at least one JSON-LD block (expected 3: Article + FAQPage + BreadcrumbList)
4. Every article and city page has the "Book Your Trip" affiliate block
5. sitemap-0.xml URL count == page count minus the 404 page
6. search-index.json has no "undefined" URLs

Exit code 0 = all pass, 1 = failures. Prints a compact report.
"""
import json
import os
import re
import sys
import threading
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")
MIN_JSONLD = 1  # articles normally carry 3; fail only on zero, report the min


def all_html():
    out = []
    for root, _dirs, files in os.walk(DIST):
        for f in files:
            if f.endswith(".html"):
                out.append(os.path.join(root, f))
    return out


def url_for(rel):
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def check_http_200(htmls):
    handler = lambda *a, **kw: SimpleHTTPRequestHandler(*a, directory=DIST, **kw)
    srv = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    port = srv.server_address[1]
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    try:
        ok, fails = 0, []
        for h in htmls:
            rel = os.path.relpath(h, DIST)
            url = f"http://127.0.0.1:{port}{url_for(rel)}"
            try:
                r = urllib.request.urlopen(url, timeout=5)
                if r.status == 200:
                    ok += 1
                else:
                    fails.append((url, r.status))
            except Exception as e:
                fails.append((url, str(e)))
        return ok, fails
    finally:
        srv.shutdown()


def check_internal_links(htmls):
    broken = []
    for h in htmls:
        content = open(h, encoding="utf-8", errors="ignore").read()
        for m in re.finditer(r'href="(/[^"#]*)"', content):
            url = m.group(1)
            p = os.path.join(DIST, url.lstrip("/"))
            if url.endswith("/"):
                p = os.path.join(p, "index.html")
            if not os.path.exists(p):
                broken.append((os.path.relpath(h, DIST), url))
    return broken


def main():
    htmls = all_html()
    print(f"HTML pages: {len(htmls)}")
    fails = []

    ok, http_fails = check_http_200(htmls)
    print(f"HTTP 200: {ok}/{len(htmls)}")
    fails += [("http", f"{u} -> {s}") for u, s in http_fails]

    broken = check_internal_links(htmls)
    print(f"Broken internal links: {len(broken)}")
    fails += [("link", f"{src} -> {url}") for src, url in broken]

    # Articles = dist/guides/<slug>/index.html, excluding the guides listing page
    guides = [h for h in htmls
              if "/guides/" in h and h.endswith("index.html")
              and not h.endswith("/guides/index.html")]
    ld_counts = {}
    for h in guides:
        n = len(re.findall(r"application/ld\+json",
                           open(h, encoding="utf-8", errors="ignore").read()))
        ld_counts[os.path.relpath(h, DIST)] = n
    zero_ld = [p for p, n in ld_counts.items() if n < MIN_JSONLD]
    print(f"Articles: {len(guides)}, JSON-LD min={min(ld_counts.values()) if ld_counts else 0}, "
          f"zero-JSON-LD: {len(zero_ld)}")
    fails += [("jsonld", p) for p in zero_ld]

    no_aff = [os.path.relpath(h, DIST) for h in guides + [h for h in htmls if "/cities/" in h and h.endswith("index.html")]
              if "Book Your Trip" not in open(h, encoding="utf-8", errors="ignore").read()]
    print(f"Articles/city pages missing 'Book Your Trip': {len(no_aff)}")
    fails += [("affiliate", p) for p in no_aff]

    sm = os.path.join(DIST, "sitemap-0.xml")
    if os.path.exists(sm):
        n = len(re.findall(r"<loc>", open(sm, encoding="utf-8").read()))
        expected = len(htmls) - 1  # 404 page is not in sitemap
        print(f"Sitemap URLs: {n} (expected {expected})")
        if n != expected:
            fails.append(("sitemap", f"{n} != {expected}"))

    si = os.path.join(DIST, "search-index.json")
    if os.path.exists(si):
        d = json.load(open(si, encoding="utf-8"))
        entries = d if isinstance(d, list) else d.get("items", [])
        undef = [e["url"] for e in entries if "undefined" in e.get("url", "")]
        print(f"Search index entries: {len(entries)}, undefined URLs: {len(undef)}")
        fails += [("search-index", u) for u in undef]

    if fails:
        print("\nFAILURES:")
        for kind, detail in fails[:20]:
            print(f"  [{kind}] {detail}")
        sys.exit(1)
    print("\n✅ All checks passed")


if __name__ == "__main__":
    main()
