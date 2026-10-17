#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cloudflare analytics/visitor-stats helper for the China Travel Guide site.

Uses the CF_TOKEN env var (never hard-coded). Supports:
  python3 cf_analytics.py token        # verify token + show scopes/permissions
  python3 cf_analytics.py rum-create   # enable CF Web Analytics (RUM) for the site
  python3 cf_analytics.py rum-list     # list RUM sites
  python3 cf_analytics.py pages        # pages project info
  python3 cf_analytics.py graphql      # probe GraphQL analytics
"""
import json
import os
import sys
import urllib.error
import urllib.request

TOKEN = os.environ.get("CF_TOKEN", "")
ACC = os.environ.get("CF_ACCOUNT", "cff851bbae30b5bf6990cbeb530131ec")
HOST = "china-travel-guide-ne9.pages.dev"
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
            return e.code, {"raw": str(e)}
    except Exception as e:
        return -1, {"error": str(e)}


def show(label, res):
    print(f"\n=== {label} ===")
    print(json.dumps(res, ensure_ascii=False, indent=2)[:2000])


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "token"
    if not TOKEN:
        print("CF_TOKEN not set")
        return 1
    if cmd == "token":
        show("verify", req("GET", "/user/tokens/verify"))
        show("accounts", req("GET", "/accounts"))
    elif cmd == "pages":
        show("pages project", req("GET", f"/accounts/{ACC}/pages/projects/china-travel-guide"))
    elif cmd == "rum-create":
        s, r = req("POST", f"/accounts/{ACC}/rum/site_info",
                   {"host": HOST, "auto_install": False})
        show(f"rum create (HTTP {s})", r)
    elif cmd == "rum-list":
        show("rum list", req("GET", f"/accounts/{ACC}/rum/site_info/list"))
    elif cmd == "graphql":
        q = ('{"query":"{ viewer { accounts(filter:{accountTag:\\"%s\\"}) '
             '{ __typename } } }"}' % ACC)
        s, r = req("POST", "/graphql", json.loads(q))
        show(f"graphql (HTTP {s})", r)
    else:
        print("unknown cmd")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
