# SuperPadLand

Web de rankings de videojuegos retro, hecha con [Hugo](https://gohugo.io/) y el tema
[PaperMod](https://github.com/adityatelange/hugo-PaperMod). Migrada desde
`superpadland.wordpress.com`.

## Ver la web en local

```bash
hugo server
```

Luego abre <http://localhost:1313> en el navegador. Mientras el servidor está en marcha,
cualquier cambio que guardes se recarga solo.

## Publicar (GitHub Pages)

El despliegue es **automático**: cada vez que subes cambios a la rama `main`, GitHub compila
y publica la web (ver `.github/workflows/hugo.yml`).

```bash
git add -A
git commit -m "Lo que has cambiado"
git push
```

A los 1-2 minutos los cambios están online.

> **Configuración inicial (solo una vez):** en GitHub, ve a *Settings → Pages* y en
> *Build and deployment → Source* elige **GitHub Actions**.

## Añadir un ranking o artículo nuevo

1. Crea un fichero en `content/posts/`, por ejemplo `content/posts/top-xbox.html`.
2. Empieza con el "front matter" (los metadatos entre `---`):

   ```yaml
   ---
   title: "Top 100 Xbox"
   date: 2026-06-13
   slug: top-xbox
   categories: ["Rankings"]
   consolas: ["Xbox"]
   cover:
     image: /img/top-xbox/portada.png
     alt: "Top 100 Xbox"
     relative: false
   ---
   ```

3. Debajo, escribe el contenido en HTML (o crea el fichero como `.md` para escribir en
   Markdown, más sencillo).
4. Pon las imágenes en `static/img/top-xbox/` y enlázalas como `/img/top-xbox/loquesea.png`.

Las consolas nuevas aparecen solas en la página *Consolas* y en la home.

## Estructura

- `content/` — las entradas y páginas (el texto).
- `static/img/` — todas las imágenes (3228 portadas migradas).
- `layouts/` — plantillas propias (la home con la cuadrícula de consolas).
- `assets/css/extended/custom.css` — estilos propios.
- `themes/PaperMod/` — el tema base.
- `hugo.toml` — la configuración del sitio (menú, taxonomías, etc.).
- `_migration/` — los scripts que se usaron para traer el contenido de WordPress
  (no afectan a la web; se pueden borrar).
