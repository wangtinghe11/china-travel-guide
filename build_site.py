#!/usr/bin/env python3
"""
China Travel Guide — static site builder.

Reads Markdown content from content/ and site_config.py, renders every page
to static HTML in build/ via Jinja2, and generates:
  - sitemap.xml + robots.txt
  - search index (search_index.json) for the Flask search API
  - JSON-LD (Article + FAQPage + BreadcrumbList) per article
  - TOC extraction from h2/h3 headings

Usage: python3 build_site.py
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

import markdown
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from site_config import SITE, CITIES, GUIDES, AD_SLOTS, AFFILIATE  # noqa: E402

CONTENT_DIR = ROOT / "content"
BUILD_DIR = ROOT / "build"
TEMPLATE_DIR = ROOT / "templates"

# Markdown extensions: tables, fenced code, TOC anchors, smart quotes
MD = markdown.Markdown(
    extensions=[
        "tables",
        "fenced_code",
        "toc",
        "sane_lists",
        "attr_list",
    ],
    extension_configs={
        "toc": {"permalink": False, "toc_depth": "2-3"},
    },
    output_format="html5",
)

ENV = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
ENV.filters["safe"] = lambda s: s  # markdown output is already safe HTML


def slugify(text: str) -> str:
    """Slugify a heading for anchor IDs (ASCII only)."""
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text.strip("-")


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Parse YAML-ish frontmatter (--- delimited) and return (meta, body)."""
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta = {}
    for line in parts[1].strip().splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip().strip('"').strip("'")
    return meta, parts[2].strip()


def extract_toc(html: str) -> list[dict]:
    """Extract h2/h3 headings with ids from rendered HTML."""
    toc = []
    for m in re.finditer(r"<h([23])\s+id=\"([^\"]+)\">(.*?)</h\1>", html, re.S):
        level = int(m.group(1))
        text = re.sub(r"<[^>]+>", "", m.group(3)).strip()
        toc.append({"id": m.group(2), "text": text, "level": level})
    return toc


def reading_time(text: str) -> int:
    """Rough reading time in minutes (200 wpm)."""
    words = len(re.findall(r"\b\w+\b", text))
    return max(1, round(words / 200))


def build_jsonld(article: dict, site: dict) -> str:
    """Build Article + FAQPage + BreadcrumbList JSON-LD."""
    url = article["url"]
    site_url = site["url"]
    author = site["author"]
    publisher = site["publisher"]

    # FAQPage from FAQ section (h2 "FAQ" followed by Q/A paragraphs)
    faq_items = []
    body = article.get("body", "")
    faq_match = re.search(r"##\s*FAQ\s*(.*?)(?=\n##\s|\Z)", body, re.S | re.I)
    if faq_match:
        qas = re.findall(
            r"\*\*Q:\s*(.+?)\?\*\*\s*\n\*\*A:\*\*\s*(.+?)(?=\n\*\*Q:|\Z)",
            faq_match.group(1),
            re.S,
        )
        for q, a in qas:
            faq_items.append(
                {
                    "@type": "Question",
                    "name": q.strip() + "?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": a.strip(),
                    },
                }
            )

    article_type = "Guide" if article.get("is_guide") else "Article"
    graph = [
        {
            "@context": "https://schema.org",
            "@type": article_type,
            "headline": article["title"],
            "description": article.get("description", ""),
            "datePublished": article.get("date", ""),
            "dateModified": article.get("updated", article.get("date", "")),
            "author": {"@type": "Person", "name": author},
            "publisher": {
                "@type": "Organization",
                "name": publisher,
                "logo": {
                    "@type": "ImageObject",
                    "url": site_url + site["logo"],
                },
            },
            "mainEntityOfPage": {"@type": "WebPage", "@id": url},
            "url": url,
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": site_url + "/"},
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "Guides" if article.get("is_guide") else "Cities",
                    "item": site_url + ("/guides/" if article.get("is_guide") else "/cities/"),
                },
                {"@type": "ListItem", "position": 3, "name": article["title"], "item": url},
            ],
        },
    ]
    if faq_items:
        graph.append(
            {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": faq_items,
            }
        )
    return json.dumps(graph, ensure_ascii=False, indent=2)


def load_articles() -> list[dict]:
    """Load all Markdown files into article dicts."""
    articles = []
    for path in sorted(CONTENT_DIR.rglob("*.md")):
        raw = path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(raw)
        if not meta.get("title"):
            continue

        rel = path.relative_to(CONTENT_DIR)
        parts = rel.parts
        is_guide = parts[0] == "guides"
        slug = path.stem

        if is_guide:
            guide_meta = next((g for g in GUIDES if g["slug"] == slug), None)
            if guide_meta is None:
                continue
            url = f"/guides/{slug}/"
            city_slug = None
            city_name = None
            guide_title = guide_meta["short_title"]
        else:
            city_slug = parts[1] if len(parts) > 1 else None
            city_meta = next((c for c in CITIES if c["slug"] == city_slug), None)
            if city_meta is None:
                continue
            url = f"/cities/{city_slug}/{slug}.html"
            city_name = city_meta["name"]
            guide_title = None

        html = MD.reset().convert(body)
        toc = extract_toc(html)
        article = {
            "slug": slug,
            "title": meta.get("title", ""),
            "description": meta.get("description", ""),
            "keywords": meta.get("keywords", ""),
            "date": meta.get("date", ""),
            "updated": meta.get("updated", meta.get("date", "")),
            "draft": meta.get("draft", "").lower() == "true",
            "type": meta.get("type", ""),
            "is_guide": is_guide,
            "city_slug": city_slug,
            "city_name": city_name,
            "guide_title": guide_title,
            "url": url,
            "body": body,
            "html": html,
            "toc": toc,
            "reading_time": reading_time(body),
        }
        article["jsonld"] = build_jsonld(article, SITE)
        articles.append(article)
    return articles


def render_page(template_name: str, **ctx) -> str:
    """Render a template with shared context."""
    ctx.setdefault("site", SITE)
    ctx.setdefault("cities", CITIES)
    ctx.setdefault("guides", GUIDES)
    ctx.setdefault("ad_slots", AD_SLOTS)
    ctx.setdefault("affiliate", AFFILIATE)
    ctx.setdefault("year", date.today().year)
    ctx.setdefault("canonical_url", SITE["url"] + ctx.get("path", "/"))
    return ENV.get_template(template_name).render(**ctx)


def main():
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    articles = load_articles()
    by_city: dict[str, list[dict]] = {}
    for a in articles:
        if a["city_slug"]:
            by_city.setdefault(a["city_slug"], []).append(a)

    # --- Home ---
    latest = sorted(articles, key=lambda a: a["date"], reverse=True)[:6]
    (BUILD_DIR / "index.html").write_text(
        render_page("index.html", latest_articles=latest, path="/"), encoding="utf-8"
    )

    # --- Cities index ---
    for c in CITIES:
        c["article_count"] = len(by_city.get(c["slug"], []))
    cities_dir = BUILD_DIR / "cities"
    cities_dir.mkdir(parents=True, exist_ok=True)
    (cities_dir / "index.html").write_text(
        render_page("cities.html", path="/cities/"), encoding="utf-8"
    )

    # --- City pages ---
    for c in CITIES:
        city_articles = sorted(
            by_city.get(c["slug"], []), key=lambda a: a["date"], reverse=True
        )
        out = BUILD_DIR / "cities" / c["slug"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            render_page(
                "city.html",
                city=c,
                articles=city_articles,
                path=f"/cities/{c['slug']}/",
            ),
            encoding="utf-8",
        )

    # --- Guides index ---
    guides_dir = BUILD_DIR / "guides"
    guides_dir.mkdir(parents=True, exist_ok=True)
    (guides_dir / "index.html").write_text(
        render_page("guides.html", path="/guides/"), encoding="utf-8"
    )

    # --- Articles (guides + city articles) ---
    for a in articles:
        if a["is_guide"]:
            out = BUILD_DIR / "guides" / f"{a['slug']}.html"
        else:
            out = BUILD_DIR / "cities" / a["city_slug"] / f"{a['slug']}.html"
        out.parent.mkdir(parents=True, exist_ok=True)

        # Related: same city first, then guides
        related = []
        if a["city_slug"]:
            related = [
                r for r in by_city.get(a["city_slug"], []) if r["slug"] != a["slug"]
            ]
        related += [g for g in articles if g["is_guide"] and g["slug"] != a["slug"]]
        related = related[:4]

        out.write_text(
            render_page(
                "article.html",
                article=a,
                related=related,
                path=a["url"],
            ),
            encoding="utf-8",
        )

    # --- About ---
    about_dir = BUILD_DIR / "about"
    about_dir.mkdir(parents=True, exist_ok=True)
    (about_dir / "index.html").write_text(
        render_page("about.html", path="/about/"), encoding="utf-8"
    )

    # --- Search page (static shell; results come from Flask API) ---
    search_dir = BUILD_DIR / "search"
    search_dir.mkdir(parents=True, exist_ok=True)
    (search_dir / "index.html").write_text(
        render_page("search.html", search_query=None, results=None, path="/search"),
        encoding="utf-8",
    )

    # --- sitemap.xml ---
    urls = [SITE["url"] + "/"]
    urls += [SITE["url"] + "/cities/", SITE["url"] + "/guides/", SITE["url"] + "/about/"]
    urls += [SITE["url"] + f"/cities/{c['slug']}/" for c in CITIES]
    urls += [SITE["url"] + a["url"] for a in articles]
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>']
    sitemap.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for u in sorted(set(urls)):
        sitemap.append(f"  <url><loc>{u}</loc></url>")
    sitemap.append("</urlset>")
    (BUILD_DIR / "sitemap.xml").write_text("\n".join(sitemap), encoding="utf-8")

    # --- robots.txt ---
    robots = (
        "User-agent: *\n"
        "Allow: /\n"
        f"Sitemap: {SITE['url']}/sitemap.xml\n"
    )
    (BUILD_DIR / "robots.txt").write_text(robots, encoding="utf-8")

    # --- Search index ---
    search_index = []
    for a in articles:
        search_index.append(
            {
                "title": a["title"],
                "url": a["url"],
                "city_name": a["city_name"],
                "guide_title": a["guide_title"],
                "date": a["date"],
                "keywords": a["keywords"],
                "text": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", a["html"]))[:2000],
            }
        )
    (BUILD_DIR / "search_index.json").write_text(
        json.dumps(search_index, ensure_ascii=False), encoding="utf-8"
    )

    # --- Summary ---
    n_guides = sum(1 for a in articles if a["is_guide"])
    n_city = len(articles) - n_guides
    n_drafts = sum(1 for a in articles if a["draft"])
    print(f"Built {len(articles)} articles ({n_guides} guides, {n_city} city, {n_drafts} drafts)")
    print(f"Output: {BUILD_DIR}")


if __name__ == "__main__":
    main()
