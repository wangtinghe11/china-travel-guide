#!/usr/bin/env python3
"""
China Travel Guide — Flask app.

Serves the pre-rendered static site from build/ and provides:
  - GET /search?q=...  (server-side search over search_index.json)
  - GET /api/search?q=...  (JSON API, same search)
  - GET /api/health  (health check with version)
  - GET /api/docs  (endpoint list)

Static pages are served with no-cache headers during development.
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_from_directory

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from site_config import SITE, CITIES, GUIDES  # noqa: E402
BUILD_DIR = ROOT / "build"
STATIC_DIR = ROOT / "static"
SEARCH_INDEX = BUILD_DIR / "search_index.json"

app = Flask(__name__, static_folder=str(STATIC_DIR), static_url_path="/static")
app.config["JSON_AS_ASCII"] = False

VERSION = "0.1.0"


def load_index() -> list[dict]:
    if SEARCH_INDEX.exists():
        return json.loads(SEARCH_INDEX.read_text(encoding="utf-8"))
    return []


def search(query: str, index: list[dict], limit: int = 10) -> list[dict]:
    """Simple relevance search: title > keywords > body text."""
    q = query.strip().lower()
    if not q:
        return []
    terms = [t for t in re.split(r"\s+", q) if t]

    scored = []
    for item in index:
        title = item["title"].lower()
        keywords = item["keywords"].lower()
        text = item["text"].lower()
        score = 0
        for t in terms:
            if t in title:
                score += 10
            if t in keywords:
                score += 5
            if t in text:
                score += 1
        if score > 0:
            # snippet around first match
            snippet = ""
            for t in terms:
                idx = text.find(t)
                if idx >= 0:
                    start = max(0, idx - 60)
                    end = min(len(text), idx + 120)
                    snippet = "…" + text[start:end].strip() + "…"
                    break
            item = dict(item)
            item["snippet"] = snippet
            scored.append((score, item))
    scored.sort(key=lambda x: -x[0])
    return [item for _, item in scored[:limit]]


@app.route("/")
def home():
    return send_from_directory(BUILD_DIR, "index.html")


@app.route("/<path:path>")
def static_pages(path: str):
    """Serve pre-rendered static pages (cities/, guides/, about/, search/, articles)."""
    # Try exact file, then path/index.html
    candidates = [BUILD_DIR / path, BUILD_DIR / path / "index.html"]
    for c in candidates:
        if c.is_file():
            resp = send_from_directory(BUILD_DIR, c.relative_to(BUILD_DIR).as_posix())
            resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            return resp
    # Article URLs like /cities/beijing/beijing-overview.html
    if path.endswith(".html"):
        f = BUILD_DIR / path
        if f.is_file():
            resp = send_from_directory(BUILD_DIR, path)
            resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            return resp
    return jsonify({"error": "Not found", "code": "NOT_FOUND"}), 404


@app.route("/search")
def search_page():
    q = request.args.get("q", "").strip()
    results = search(q, load_index()) if q else []
    return render_template(
        "search.html",
        search_query=q,
        results=results,
        site=SITE,
        cities=CITIES,
        guides=GUIDES,
        year=date.today().year,
        canonical_url=SITE["url"] + "/search",
    )


@app.route("/api/search")
def api_search():
    q = request.args.get("q", "").strip()
    results = search(q, load_index()) if q else []
    return jsonify({"query": q, "count": len(results), "results": results})


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "version": VERSION, "app": "china-travel-guide"})


@app.route("/api/docs")
def api_docs():
    return jsonify(
        {
            "app": "china-travel-guide",
            "version": VERSION,
            "endpoints": [
                {"method": "GET", "path": "/", "desc": "Home page"},
                {"method": "GET", "path": "/cities/", "desc": "Cities index"},
                {"method": "GET", "path": "/guides/", "desc": "Guides index"},
                {"method": "GET", "path": "/search?q=...", "desc": "Search page"},
                {"method": "GET", "path": "/api/search?q=...", "desc": "Search JSON API"},
                {"method": "GET", "path": "/api/health", "desc": "Health check"},
                {"method": "GET", "path": "/sitemap.xml", "desc": "XML sitemap"},
                {"method": "GET", "path": "/robots.txt", "desc": "Robots file"},
            ],
        }
    )


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found", "code": "NOT_FOUND"}), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method not allowed", "code": "METHOD_NOT_ALLOWED"}), 405


@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.exception("Unhandled error")
    return jsonify({"error": str(e), "code": "INTERNAL_ERROR"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8095, debug=False)
