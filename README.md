# SuperPadLand

Web de rankings de videojuegos retro, hecha con [Hugo](https://gohugo.io/) y el tema
[PaperMod](https://github.com/adityatelange/hugo-PaperMod). Migrada desde
WordPress.com.

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

## Chuletas retro

Las entradas con `categories: ["Artículos"]` salen solas en el apartado *Chuletas retro* de la
portada y en su página (`/chuletas-retro/`), de la más nueva a la más antigua. Para que la
tarjeta quede bien, añade al front matter:

```yaml
description: "Una o dos frases: es lo que enseña Google debajo del título."
chuleta:
  titulo: "Título corto"
  frase: "Frase corta para la portada"
  icono: rayo   # rayo, pantalla, candado, balanza u hoja
```

Los iconos están en `layouts/_partials/icono-pixel.html`.

## Versión en gallego

La web está en castellano (en la raíz) y en gallego (en `/gl/`). El contenido gallego está en
`content-gl/`, con **los mismos nombres de fichero** que en `content/`: así cada página sabe
cuál es su traducción, y el selector **ES · GL** del encabezado lleva de una a otra. Los
comentarios de las dos versiones de una entrada van al mismo hilo.

- Los textos fijos de las plantillas (botones, avisos, pie…) están en `i18n/es.yaml` e
  `i18n/gl.yaml`.
- Las páginas con `url` fija llevan `/gl/` delante en su versión gallega (`url: "/gl/contacto/"`).
- Un top con la introducción traducida pero las reseñas aún en castellano lleva
  `pendienteTraducir: true`, que muestra un aviso arriba. Al terminar de traducirlo, se quita.
- Si una entrada no tiene versión gallega, no sale en `/gl/`, y el selector lleva a la portada
  gallega.

## Comentarios

Cada entrada y la página de Contacto tienen comentarios con [giscus](https://giscus.app/):
se guardan en las *Discussions* de este repositorio, un hilo por entrada. Para quitarlos de
una página, pon `comments: false` en su front matter.

## Estructura

- `content/` — las entradas y páginas en castellano; `content-gl/`, en gallego.
- `static/img/` — todas las imágenes.
- `layouts/` — plantillas propias: la home con la cuadrícula de consolas, el índice del
  buscador (`index.json`), los comentarios, la página 404 y el pie en castellano.
- `assets/js/fastsearch.js` — el buscador (muestra en qué top y puesto está cada juego).
- `assets/css/extended/custom.css` — estilos propios (el morado de la cruceta y la letra pixelada).
- `static/fuentes/` — la letra pixelada de los títulos (Jersey 15, licencia OFL).
- `static/img/superpadland-compartir.png` — la imagen que sale al compartir la web en redes.
- `themes/PaperMod/` — el tema base.
- `hugo.toml` — la configuración del sitio (menú, taxonomías, etc.).
