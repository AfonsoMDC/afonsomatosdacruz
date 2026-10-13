# Portfolio Afonso Matos da Cruz — afonsomatosdacruz.be

Gewone HTML, CSS en JavaScript. Geen frameworks, geen build, geen tracking.

## Mappen
- `index.html`, `archief.html`, `fotografie.html`, `privacy.html`, `404.html` — Nederlandse pagina's
- `projecten/` — de drie projecten (NL)
- `en/` — dezelfde pagina's in het Engels
- `css/stijl.css` — alle stijl (kleuren en lettergroottes staan bovenaan bij "variabelen")
- `javascript/script.js` — scroll-effect en beeldvenster (±70 regels)
- `afbeeldingen/`, `video/`, `lettertypen/`, `favicon/`, `cv/`
- `schoolwebsites/` — schoolopdrachten, ongewijzigd (laden Google Fonts)
- `sitemap.xml`, `robots.txt`

## Aanpassen
- **Kleur**: `--papier`, `--inkt`, `--grijs`, `--accent` bovenaan `css/stijl.css`.
- **Tekst**: open het HTML-bestand en wijzig de tekst tussen de tags. Doe dit in `x.html` én in `en/` voor de vertaling.
- **Nieuw werk**: kopieer een bestaande projectpagina, pas tekst en afbeeldingen aan, en voeg de URL toe aan `sitemap.xml`.
- **Afbeeldingen**: WebP, in meerdere breedtes (`-480`, `-960`, `-1600`...) voor `srcset`.

## Publiceren
Upload de inhoud van deze map naar een statische host (Netlify, Cloudflare Pages, GitHub Pages...), zet de DNS van afonsomatosdacruz.be erheen, activeer HTTPS en laat www doorverwijzen naar afonsomatosdacruz.be. Voeg daarna de site toe in Google Search Console en dien `https://afonsomatosdacruz.be/sitemap.xml` in.
