#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Query Cloudflare GraphQL analytics for the pages.dev site (visitor stats attempt)."""
import json
import os
import urllib.error
import urllib.request

TOKEN = os.environ.get("CF_TOKEN", "")
ACC = "cff851bbae30b5bf6990cbeb530131ec"


def gql(q):
    rq = urllib.request.Request("https://api.cloudflare.com/client/v4/graphql",
                                data=json.dumps({"query": q}).encode(), method="POST",
                                headers={"Authorization": f"Bearer {TOKEN}",
                                         "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(rq, timeout=30) as x:
            return json.loads(x.read().decode())
    except urllib.error.HTTPError as e:
        try:
            return json.loads(e.read().decode())
        except Exception:
            return {"http": e.code}


# Does the account type expose RUM / pages analytics? Introspect fields matching rum/pages
q = '{__type(name:"account"){fields{name}}}'
res = gql(q)
fields = [f["name"] for f in (res.get("data", {}).get("__type", {}) or {}).get("fields", [])]
hits = [f for f in fields if any(k in f.lower() for k in ("rum", "pageload", "pagesproject", "pages"))]
print("RUM/pages-related account fields:")
for h in hits:
    print("  ", h)

# Try a real RUM data query (correct syntax)
if hits:
    field = next((f for f in hits if "Pageload" in f or "pageload" in f), hits[0])
    q2 = ('{viewer{accounts(filter:{accountTag:"%s"}){%s(limit:10){count}}}}' % (ACC, field))
    print("\nquery:", q2)
    print("result:", json.dumps(gql(q2), ensure_ascii=False)[:600])
