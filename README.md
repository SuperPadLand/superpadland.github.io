# SuperPadLand

Web de rankings de videojuegos retro, hecha con [Hugo](https://gohugo.io/) y el tema
[PaperMod](https://github.com/adityatelange/hugo-PaperMod). Antes estaba en
WordPress.com, que se cerró en octubre de 2026: esta es ahora la única web.

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
5. En los tops, cada juego lleva su puesto y su nombre para que el buscador lo encuentre y
   lleve directo a él (`/posts/top-xbox/#puesto-12`), y la captura lleva el nombre como `alt`:

   ```html
   <p id="puesto-12" data-juego="Halo 2 (2004)"><strong>12. Halo 2 (2004)</strong></p>
   <p><img alt="Halo 2 (2004)" src="/img/top-xbox/halo-2.png" width="300" height="225" loading="lazy"/>Reseña…</p>
   <hr/>
   ```

Las consolas nuevas hay que añadirlas a la lista `$orden` de
`layouts/_partials/rejilla-consolas.html`, en su sitio por orden cronológico: de ahí salen la
cuadrícula de la portada y la de la página *Consolas*.

Si cambias la dirección (`slug`) de una entrada ya publicada, añade la vieja en `aliases`
para que los enlaces antiguos sigan funcionando.

## Comentarios

Cada entrada y la página de Contacto tienen comentarios con [giscus](https://giscus.app/):
se guardan en las *Discussions* de este repositorio, un hilo por entrada. Para quitarlos de
una página, pon `comments: false` en su front matter.

## Estructura

- `content/` — las entradas y páginas (el texto).
- `static/img/` — todas las imágenes.
- `layouts/` — plantillas propias: la home con la cuadrícula de consolas, el índice del
  buscador (`index.json`), los comentarios, la página 404 y el pie en castellano.
- `assets/js/fastsearch.js` — el buscador (muestra en qué top y puesto está cada juego).
- `assets/css/extended/custom.css` — estilos propios (el morado de la cruceta y la letra pixelada).
- `static/fuentes/` — la letra pixelada de los títulos (Jersey 15, licencia OFL).
- `static/img/superpadland-compartir.png` — la imagen que sale al compartir la web en redes.
- `themes/PaperMod/` — el tema base.
- `hugo.toml` — la configuración del sitio (menú, taxonomías, etc.).
