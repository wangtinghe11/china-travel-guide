#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Visitor statistics reader for the China Travel Guide site.

Reads the anonymous counters written by the in-page tracker
(countapi.mileshilliard.com, no cookies, no signup) and prints a
human-readable traffic report.

Usage:
    python3 scripts/stats.py            # last 7 days + totals + top pages
    python3 scripts/stats.py 14         # last 14 days
    python3 scripts/stats.py json       # machine-readable JSON
"""
import datetime as dt
import json
import sys
import urllib.error
import urllib.request

API = "https://countapi.mileshilliard.com/api/v1/get/"
TIMEOUT = 20


def get(key):
    """Return counter value for key; 0 if the key doesn't exist yet, None if unreachable."""
    try:
        req = urllib.request.Request(API + key, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            d = json.loads(r.read().decode("utf-8", "replace"))
            return int(d.get("value", 0))
    except urllib.error.HTTPError as e:
        if e.code == 404:  # key not created yet -> effectively 0, service IS reachable
            return 0
        return None
    except Exception:
        return None  # unknown (don't conflate with 0)


def day_key(d):
    return f"ctg-pv-{d:%Y-%m-%d}"


def main():
    days = 7
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        days = int(sys.argv[1])
    as_json = len(sys.argv) > 1 and sys.argv[1] == "json"

    today = dt.date.today()
    rows = []
    for i in range(days - 1, -1, -1):
        d = today - dt.timedelta(days=i)
        pv = get(day_key(d))
        uv = get(f"ctg-uv-{d:%Y-%m-%d}")
        rows.append({"date": d.isoformat(), "pageviews": pv, "uniques": uv})

    pv_total = get("ctg-pv-total")
    uv_total = get("ctg-uv-total")

    # Top pages (probe a fixed list of known slugs; countapi has no "list" API)
    top_slugs = [
        "home", "cities-beijing", "cities-shanghai", "cities-xian",
        "cities-chengdu", "cities-chongqing", "cities-guangzhou",
        "cities-shenzhen", "cities-hangzhou", "cities-guilin",
        "cities-zhangjiajie",
        "guides-china-visa-guide", "guides-how-to-pay-in-china",
        "guides-china-high-speed-rail-guide", "guides-best-esim-for-china",
        "guides-is-china-safe-for-tourists",
        "guides-visa-free-china", "guides-payments-in-china",
        "guides-high-speed-rail-china", "guides-esim-china",
        "guides-safety-in-china", "guides-china-visa-free-transit-240-hours",
    ]
    pages = []
    for s in top_slugs:
        v = get(f"ctg-page-{s}")
        if v:
            pages.append({"slug": s, "views": v})
    pages.sort(key=lambda x: -x["views"])

    if as_json:
        print(json.dumps({
            "days": rows, "pageviews_total": pv_total,
            "uniques_total": uv_total, "top_pages": pages[:15],
        }, indent=2))
        return 0

    print("=" * 58)
    print(" China Travel Guide — 访问统计 (anonymous, cookie-free)")
    print("=" * 58)
    print(f"\n{'日期':<14}{'浏览量':>10}{'独立访客':>12}")
    print("-" * 58)
    reachable = False
    for r in rows:
        pv = "—" if r["pageviews"] is None else r["pageviews"]
        uv = "—" if r["uniques"] is None else r["uniques"]
        if r["pageviews"] is not None:
            reachable = True
        print(f"{r['date']:<14}{str(pv):>10}{str(uv):>12}")
    print("-" * 58)
    print(f"{'累计浏览 (总)':<14}{str(pv_total if pv_total is not None else '—'):>10}")
    print(f"{'累计独立访客':<14}{str(uv_total if uv_total is not None else '—'):>10}")

    recent_pv = sum(r["pageviews"] for r in rows if r["pageviews"])
    print(f"\n近 {days} 天浏览量合计: {recent_pv}")

    if pages:
        print(f"\n{'热门页面':<45}{'浏览量':>8}")
        print("-" * 58)
        for p in pages[:15]:
            print(f"{p['slug']:<45}{p['views']:>8}")
    else:
        print("\n热门页面: 暂无数据（流量少或统计服务未响应）")

    if not reachable:
        print("\n⚠️  统计服务暂时不可达，稍后重试。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
