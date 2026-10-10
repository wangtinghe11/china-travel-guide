#!/usr/bin/env python3
"""Generate draft placeholder articles for cities without content yet."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_config import CITIES

DRAFT_TEMPLATE = """---
title: "{name} Travel Guide 2026: First-Timer's Complete Guide"
description: "{name} for first-timers: {tagline}. A complete city guide for Western travelers. (Draft — full content coming soon.)"
keywords: "{name} travel guide, {name} visa free, {tagline}"
date: 2026-10-10
updated: 2026-10-10
type: city-overview
city: {slug}
draft: true
---

# {name} Travel Guide 2026: First-Timer's Complete Guide

> **Draft placeholder.** The full {name} guide is being written. Check back soon for the complete first-timer's guide.

## Why visit {name}

{intro}

## Getting there

_Content coming soon — airports, high-speed rail connections, and arrival tips._

## Getting around

_Content coming soon — metro, Didi, taxis, and walking._

## Where to stay

_Content coming soon — neighborhoods, hotel picks, and budget options._

## What to see (top 5)

_Content coming soon — the must-see sights._

## Food & drink

_Content coming soon — local specialties and where to eat._

## Sample itinerary

_Content coming soon — 3-day itinerary._

## Practical tips

_Content coming soon — money, language, and local tips._

## FAQ

_Content coming soon — common questions answered._
"""

def main():
    root = Path(__file__).resolve().parent
    content_dir = root / "content" / "cities"
    written = []
    for city in CITIES:
        slug = city["slug"]
        if slug in ("beijing", "shanghai"):
            continue  # already have real content
        out = content_dir / slug / f"{slug}-overview.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        if out.exists():
            continue  # don't overwrite real content
        out.write_text(DRAFT_TEMPLATE.format(**city), encoding="utf-8")
        written.append(slug)
    print(f"Generated {len(written)} draft articles: {', '.join(written)}")

if __name__ == "__main__":
    main()
