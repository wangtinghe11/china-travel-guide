#!/usr/bin/env bash
# Daily promotion + visitor stats for the China Travel Guide site.
# Runs: IndexNow re-submit (all URLs) + a share-copy snippet for the newest
# article + a compact traffic report. Output is a short Chinese brief.
set -uo pipefail
cd /root/china_travel_guide

echo "===== 旅游站每日推广 & 流量简报 $(date -u +%F) ====="
echo

# 1) IndexNow: re-submit all URLs to Bing/Yandex (instant indexing signal)
echo "【1】IndexNow 收录 (Bing/Yandex):"
python3 scripts/promote.py indexnow 2>&1 | tail -3
echo

# 2) Newest article -> ready-to-post social copy
LATEST=$(ls -t src/content/articles/*.md 2>/dev/null | head -1)
if [ -n "$LATEST" ]; then
  SLUG=$(basename "$LATEST" .md)
  echo "【2】最新文章推广文案 (发到 Reddit/Quora/FB 等平台):"
  python3 scripts/promote.py share "$SLUG" 2>&1 | head -20
  echo
fi

# 3) Visitor stats (last 7 days + totals + top pages)
echo "【3】访问统计 (匿名, 无 cookie):"
python3 scripts/stats.py 7 2>&1 | tail -25
