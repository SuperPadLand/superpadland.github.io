#!/usr/bin/env python3
"""Descarga todo el contenido público de superpadland.wordpress.com vía la API REST."""
import json
import os
import urllib.request

SITE = "superpadland.wordpress.com"
BASE = f"https://public-api.wordpress.com/rest/v1.1/sites/{SITE}"
OUT = os.path.join(os.path.dirname(__file__), "raw")
os.makedirs(OUT, exist_ok=True)

FIELDS = "ID,title,date,modified,slug,status,categories,tags,content,excerpt,featured_image,type,parent"


def fetch(kind):
    """kind: 'post' o 'page'. Devuelve lista de items con contenido completo."""
    items = []
    page = 1
    while True:
        url = f"{BASE}/posts/?type={kind}&number=100&page={page}&fields={FIELDS}&status=publish"
        with urllib.request.urlopen(url) as r:
            data = json.load(r)
        batch = data.get("posts", [])
        if not batch:
            break
        items.extend(batch)
        if len(items) >= data.get("found", 0):
            break
        page += 1
    return items


def main():
    for kind in ("post", "page"):
        items = fetch(kind)
        path = os.path.join(OUT, f"{kind}s.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        print(f"{kind}: {len(items)} guardados en {path}")


if __name__ == "__main__":
    main()
