#!/usr/bin/env python3
"""Convierte el HTML de WordPress a contenido Hugo limpio.

- Deriva la consola del título.
- Limpia atributos basura de WordPress (data-*, srcset, class, estilos con vars de WP).
- Reescribe las imágenes a rutas locales /img/<slug>/<archivo>.
- Genera ficheros content/posts/<slug>.html con front matter YAML.
- Produce _migration/downloads.json con la lista (url -> ruta local) para descargar.
"""
import html
import json
import os
import re

from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "_migration", "raw")

# --- clasificación de consola a partir del título -------------------------
CONSOLA_PAIRS = [
    ("gamecube", "GameCube"),
    ("dreamcast", "Dreamcast"),
    ("megadrive", "Mega Drive"), ("genesis", "Mega Drive"),
    ("saturn", "Saturn"),
    ("super nintendo", "Super Nintendo"), ("super famicom", "Super Nintendo"),
    ("psone", "PlayStation"), ("psx", "PlayStation"), ("ps1", "PlayStation"),
    ("ps one", "PlayStation"),
    ("nintendo 64", "Nintendo 64"), ("n64", "Nintendo 64"),
    ("master system", "Master System"), ("mark iii", "Master System"),
    ("game boy", "Game Boy"), ("gameboy", "Game Boy"),
    ("pc engine", "PC Engine"), ("turbografx", "PC Engine"),
    ("wiiu", "Wii U"), ("wii u", "Wii U"),
    ("3do", "3DO"),
    ("atari jaguar", "Atari Jaguar"),
    ("nes", "NES"), ("famicom", "NES"),
]


def consola_de(title):
    t = title.lower()
    for k, v in CONSOLA_PAIRS:
        if k in t:
            return v
    return None


# --- limpieza de HTML -----------------------------------------------------
KEEP_STYLE = {"text-align"}


def clean_style(style):
    keep = []
    for decl in style.split(";"):
        if ":" not in decl:
            continue
        prop, val = decl.split(":", 1)
        prop = prop.strip().lower()
        val = val.strip()
        if prop in KEEP_STYLE and "var(" not in val and val:
            keep.append(f"{prop}: {val}")
    return "; ".join(keep)


def clean_html(content, slug, img_map, downloads):
    soup = BeautifulSoup(content, "lxml")

    # imágenes
    first_img = None
    for img in soup.find_all("img"):
        src = img.get("src", "")
        if not src:
            img.decompose()
            continue
        canon = src.split("?")[0]
        if canon not in img_map:
            base = canon.rsplit("/", 1)[-1]
            local = base
            i = 1
            used = set(img_map.values())
            while f"/img/{slug}/{local}" in used:
                name, _, ext = base.rpartition(".")
                local = f"{name}-{i}.{ext}"
                i += 1
            img_map[canon] = f"/img/{slug}/{local}"
            downloads.append([canon, f"static/img/{slug}/{local}"])
        newsrc = img_map[canon]
        if first_img is None:
            first_img = newsrc
        alt = img.get("alt", "")
        w = img.get("width")
        h = img.get("height")
        img.attrs = {}
        img["src"] = newsrc
        if alt:
            img["alt"] = alt
        if w:
            img["width"] = w
        if h:
            img["height"] = h
        img["loading"] = "lazy"

    # resto de etiquetas: quitar class/data-*/estilos-WP
    for tag in soup.find_all(True):
        if tag.name == "img":
            continue
        attrs = dict(tag.attrs)
        new = {}
        if "href" in attrs:
            new["href"] = attrs["href"]
        if "src" in attrs:
            new["src"] = attrs["src"]
        if "style" in attrs:
            s = clean_style(attrs["style"])
            if s:
                new["style"] = s
        tag.attrs = new

    body = soup.body
    out = "".join(str(c) for c in body.contents) if body else str(soup)
    # colapsar líneas en blanco excesivas
    out = re.sub(r"(\s*<p>(&nbsp;|\s)*</p>\s*)+", "\n", out)
    return out.strip(), first_img


def yaml_escape(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def main():
    posts = json.load(open(os.path.join(RAW, "posts.json")))
    img_map = {}
    downloads = []
    slug_to_url = {}

    os.makedirs(os.path.join(ROOT, "content", "posts"), exist_ok=True)

    META_SLUGS = {"esto-sigue-vivo", "consulta-a-los-lectores"}

    rendered = []
    for p in posts:
        title = html.unescape(p["title"]).strip()
        slug = p["slug"]
        date = p["date"]
        modified = p.get("modified", date)
        cats_orig = list(p["categories"].keys())
        tags = list(p.get("tags", {}).keys())
        consola = consola_de(title)
        is_ranking = title.lower().startswith("top ") and consola

        if is_ranking:
            categoria = "Rankings"
        elif slug in META_SLUGS:
            categoria = "Noticias"
        else:
            categoria = "Artículos"

        body, first_img = clean_html(p["content"], slug, img_map, downloads)

        fm = ["---"]
        fm.append(f"title: {yaml_escape(title)}")
        fm.append(f"date: {date}")
        if modified and modified != date:
            fm.append(f"lastmod: {modified}")
        fm.append(f"slug: {slug}")
        fm.append(f"categories: [{yaml_escape(categoria)}]")
        if consola:
            fm.append(f"consolas: [{yaml_escape(consola)}]")
        if tags:
            fm.append("tags: [" + ", ".join(yaml_escape(t) for t in tags) + "]")
        if is_ranking and first_img:
            fm.append("cover:")
            fm.append(f"  image: {first_img}")
            fm.append(f"  alt: {yaml_escape(title)}")
            fm.append("  relative: false")
        fm.append("---")
        fmtext = "\n".join(fm)

        path = os.path.join(ROOT, "content", "posts", f"{slug}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(fmtext + "\n\n" + body + "\n")
        slug_to_url[slug] = f"/posts/{slug}/"
        rendered.append((slug, categoria, consola, len(body)))

    # reescribir enlaces internos de wordpress a rutas locales
    rewrite_internal_links(slug_to_url)

    with open(os.path.join(ROOT, "_migration", "downloads.json"), "w") as f:
        json.dump(downloads, f, indent=2)

    print(f"Entradas convertidas: {len(rendered)}")
    for slug, cat, con, n in rendered:
        print(f"  {cat:10} {str(con):14} {slug:42} ({n} bytes)")
    print(f"\nImágenes a descargar: {len(downloads)}")


def rewrite_internal_links(slug_to_url):
    """Reemplaza enlaces https://superpadland.wordpress.com/.../<slug>/ por rutas locales."""
    postdir = os.path.join(ROOT, "content", "posts")
    pat = re.compile(r'href="https?://superpadland\.wordpress\.com/[^"]*?/([a-z0-9\-]+)/?"')

    def repl(m):
        s = m.group(1)
        if s in slug_to_url:
            return f'href="{slug_to_url[s]}"'
        return m.group(0)

    for fn in os.listdir(postdir):
        path = os.path.join(postdir, fn)
        with open(path, encoding="utf-8") as f:
            txt = f.read()
        new = pat.sub(repl, txt)
        if new != txt:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new)


if __name__ == "__main__":
    main()
