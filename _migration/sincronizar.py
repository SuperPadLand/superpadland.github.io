#!/usr/bin/env python3
"""Trae a Hugo las entradas nuevas del WordPress sin tocar las que ya están.

Uso: python3 _migration/sincronizar.py [slug ...]
Sin argumentos lista lo que hay en WordPress y no en content/posts; con slugs,
los convierte como convert.py, añade sus imágenes a downloads.json y las baja.
"""
import glob
import html
import json
import os
import re
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import convert  # noqa: E402
import download_images  # noqa: E402

ROOT = convert.ROOT
API = ("https://public-api.wordpress.com/rest/v1.1/sites/superpadland.wordpress.com"
       "/posts/?type=post&number=100&status=publish"
       "&fields=ID,title,date,modified,slug,categories,tags,content")
META_SLUGS = {"esto-sigue-vivo", "consulta-a-los-lectores", "actualizacion-pequena"}


def slugs_hugo():
    """slug -> ruta, incluidos los alias de las entradas renombradas."""
    out = {}
    for f in glob.glob(os.path.join(ROOT, "content", "posts", "*.html")):
        fm = open(f, encoding="utf-8").read().split("\n---\n", 1)[0]
        slug = re.search(r"^slug: (.*)$", fm, re.M).group(1).strip()
        out[slug] = f"/posts/{slug}/"
        al = re.search(r"^aliases: \[(.*)\]$", fm, re.M)
        if al:
            for a in re.findall(r'"/posts/([^/"]+)/?"', al.group(1)):
                out[a] = f"/posts/{slug}/"
    return out


def convertir(p, img_map, downloads):
    title = html.unescape(p["title"]).strip()
    slug = p["slug"]
    consola = convert.consola_de(title)
    is_ranking = title.lower().startswith("top ") and consola
    categoria = "Rankings" if is_ranking else "Noticias" if slug in META_SLUGS else "Artículos"
    body, first_img = convert.clean_html(p["content"], slug, img_map, downloads)

    fm = ["---", f"title: {convert.yaml_escape(title)}", f"date: {p['date']}"]
    if p.get("modified") and p["modified"] != p["date"]:
        fm.append(f"lastmod: {p['modified']}")
    fm.append(f"slug: {slug}")
    fm.append(f"categories: [{convert.yaml_escape(categoria)}]")
    if consola:
        fm.append(f"consolas: [{convert.yaml_escape(consola)}]")
    tags = list(p.get("tags", {}).keys())
    if tags:
        fm.append("tags: [" + ", ".join(convert.yaml_escape(t) for t in tags) + "]")
    if is_ranking and first_img:
        fm += ["cover:", f"  image: {first_img}", f"  alt: {convert.yaml_escape(title)}",
               "  relative: false"]
    fm.append("---")
    path = os.path.join(ROOT, "content", "posts", f"{slug}.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(fm) + "\n\n" + body + "\n")
    print(f"  {categoria:10} {str(consola):12} {slug}")


def main():
    with urllib.request.urlopen(API) as r:
        posts = json.loads(r.read(), strict=False)["posts"]
    hugo = slugs_hugo()
    if len(sys.argv) == 1:
        for p in posts:
            if p["slug"] not in hugo:
                print(f"{p['date'][:10]}  {p['slug']}  ({html.unescape(p['title'])})")
        return

    manifest = os.path.join(ROOT, "_migration", "downloads.json")
    downloads = json.load(open(manifest))
    img_map = {u: d[len("static"):] for u, d in downloads}
    nuevas = []
    for p in posts:
        if p["slug"] in sys.argv[1:]:
            convertir(p, img_map, nuevas)
            hugo[p["slug"]] = f"/posts/{p['slug']}/"
    convert.rewrite_internal_links(hugo)
    with open(manifest, "w") as f:
        json.dump(downloads + nuevas, f, indent=2)
    print(f"Imágenes nuevas: {len(nuevas)}")
    download_images.main()


if __name__ == "__main__":
    main()
