# China Travel Guide

English travel guides for Western visitors to China — visa, payments, high-speed rail, eSIMs, and 10 city guides.

## Tech Stack

- **Astro 5** — static site generator
- **Cloudflare Pages** — free hosting, global CDN
- **GitHub Actions** — auto-deploy on push to `main`

## Quick Start

```bash
npm install
npm run dev       # local dev at http://localhost:4321
npm run build     # build to dist/
npm run preview   # preview the build
```

## Content

- **Cities**: `src/content/cities/*.md` — 10 city overview pages
- **Articles**: `src/content/articles/*.md` — guides (visa, payment, transport, sim, city)

### Adding a new article

1. Create `src/content/articles/my-guide.md`
2. Add frontmatter: `title`, `description`, `pubDate`, `category`, `tags`, optional `faq`, `city`
3. Push to `main` — auto-deploys

### Frontmatter schema

```yaml
---
title: "Article Title"
description: "SEO description"
pubDate: 2026-10-10
category: visa | payment | transport | sim | safety | guide | city
tags: [tag1, tag2]
city: beijing            # optional, links to city page
faq:                     # optional, renders FAQPage JSON-LD
  - question: "Q?"
    answer: "A."
draft: false
---
```

## SEO Features

- JSON-LD: Article, FAQPage, BreadcrumbList, City, WebSite
- Auto sitemap.xml + robots.txt
- Canonical URLs, Open Graph, Twitter cards
- Semantic HTML, responsive, mobile-first
- Search index (`/search-index.json`) generated at build

## Ad & Affiliate Placeholders

- `src/components/AdSlot.astro` — reserved ad positions (top/middle/bottom/sidebar)
- `src/components/AffiliateLink.astro` — partner links (Booking/Agoda/Klook), `rel="sponsored nofollow"`

## Deploy

Push to `main` → GitHub Actions builds → Cloudflare Pages deploys.

Secrets needed in GitHub repo:
- `CLOUDFLARE_API_TOKEN`
- `CLOUDFLARE_ACCOUNT_ID`

## Domain

Update `site` in `astro.config.mjs` and the sitemap URL in `public/robots.txt` once the domain is final.
