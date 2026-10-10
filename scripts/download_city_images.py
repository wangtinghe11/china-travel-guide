#!/usr/bin/env python3
"""Download unique city images with verified distinct IDs."""
import urllib.request
import os
import hashlib

# Each city gets a DISTINCT source. Sources verified reachable earlier.
# Unsplash IDs (from probe: confirmed OK)
UNSPLASH_OK = [
    "1518391846015-55a9cc003b25",
    "1528164344705-47542687000d",
    "1519501025264-65ba15a82390",
    "1528181304800-259b08848526",
    "1522383225653-ed111181a951",
    "1518005020951-eccb494ad742",
    "1529156069898-49953e39b3ac",
    "1508804185872-d7badad00f7d",  # beijing (already have)
    "1501339847302-ac426a4a7cbb",  # chengdu (already have)
    "1514565131-fce0801e5785",     # shenzhen (already have)
    "1528127269322-539801943592",  # hangzhou (already have)
    "1533105079780-92b9be482077",  # guilin (already have)
]

# Pexels IDs (from probe: confirmed OK)
PEXELS_OK = [3787839, 1029614, 2506923, 2506922, 3785708, 3785709, 3785710]

# Assignment: city -> (source, id)
# Use DIFFERENT ids for each city to avoid duplicates
ASSIGN = {
    "beijing": ("unsplash", "1508804185872-d7badad00f7d"),
    "shanghai": ("pexels", 3787839),
    "xian": ("pexels", 1029614),
    "chengdu": ("unsplash", "1501339847302-ac426a4a7cbb"),
    "chongqing": ("pexels", 3785708),
    "guangzhou": ("pexels", 2506923),
    "shenzhen": ("unsplash", "1514565131-fce0801e5785"),
    "hangzhou": ("unsplash", "1528127269322-539801943592"),
    "guilin": ("unsplash", "1533105079780-92b9be482077"),
    "zhangjiajie": ("pexels", 3785709),
    "hero-china": ("unsplash", "1518391846015-55a9cc003b25"),
}

OUT = "/root/china_travel_guide/public/images/cities"
os.makedirs(OUT, exist_ok=True)

def fetch(url, path):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    with open(path, "wb") as f:
        f.write(data)
    return data

seen = {}
for city, (src, pid) in ASSIGN.items():
    path = os.path.join(OUT, f"{city}.webp")
    if src == "unsplash":
        url = f"https://images.unsplash.com/photo-{pid}?w=1200&q=80&fm=webp&fit=crop"
    else:
        url = f"https://images.pexels.com/photos/{pid}/pexels-photo-{pid}.jpeg?w=1200&h=800&fit=crop"
    try:
        data = fetch(url, path)
        h = hashlib.md5(data).hexdigest()[:8]
        dup = "DUP!" if h in seen else ""
        seen[h] = city
        print(f"{city}: {len(data)//1024}KB md5={h} {dup}")
    except Exception as e:
        print(f"{city}: FAIL {e}")
