#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Probe Cloudflare Pages project update endpoints for enabling Web Analytics."""
import json
import os
import sys
import urllib.error
import urllib.request

TOKEN = os.environ.get("CF_TOKEN", "")
ACC = os.environ.get("CF_ACCOUNT", "cff851bbae30b5bf6990cbeb530131ec")
HOST = "china-travel-guide-ne9.pages.dev"
PROJ = "china-travel-guide"
API = "https://api.cloudflare.com/client/v4"


def req(method, path, body=None):
    url = f"{API}{path}"
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(r, timeout=30) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode("utf-8", "replace"))
        except Exception:
            return e.code, {"raw": str(e)[:300]}
    except Exception as e:
        return -1, {"error": str(e)}


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "read"
    if cmd == "read":
        s, r = req("GET", f"/accounts/{ACC}/pages/projects/{PROJ}")
        print(f"HTTP {s}")
        print(json.dumps(r.get("result", r), ensure_ascii=False, indent=1)[:2500])
    elif cmd == "patch":
        # Try to enable web analytics tag on the project
        body = {"build_config": {"web_analytics_tag": "china-travel-guide", "web_analytics_token": ""}}
        s, r = req("PATCH", f"/accounts/{ACC}/pages/projects/{PROJ}", body)
        print(f"HTTP {s}")
        print(json.dumps(r, ensure_ascii=False, indent=1)[:1200])
    # probe: can we create an API token? list permission groups
    elif cmd == "perms":
        s, r = req("GET", "/user/tokens/permission_groups")
        print(f"HTTP {s}")
        res = r.get("result", [])
        for g in res[:80]:
            print(g.get("name"), "|", g.get("scopes"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
