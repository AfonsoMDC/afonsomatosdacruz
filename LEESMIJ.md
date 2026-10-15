# Website Afonso Matos da Cruz

Een statische website in gewone HTML, CSS en JavaScript, in het Nederlands, Engels en Frans.
De pagina's worden gebouwd met één klein Python-script. Er zijn geen frameworks.

## Mappen

- `bron/teksten/nl.json`: **alle teksten**. Dit is het enige bestand waarin je teksten aanpast.
- `bron/teksten/en.json` en `fr.json`: de vertalingen. Worden automatisch gemaakt.
- `bron/sjablonen/`: de HTML-opbouw van elke pagina, met `{{sleutel}}` waar een tekst moet komen.
- `bron/gegevens.py`: welke werken, projecten, films en foto's er zijn.
- `bron/bouw.py`: maakt de pagina's. `bron/vertaal.py`: vertaalt met DeepL.
- `css/stijl.css`, `javascript/`: opmaak en twee kleine scripts (vergroting, formulier).
- `afbeeldingen/<map>/<naam>-klein.webp` en `-groot.webp`, `video/`, `cv/`, `lettertypen/`, `favicon/`.

De mappen `en/`, `fr/`, `werk/`, `project/`, `film/`, `fotografie/`, `privacy/`, `index.html`,
`404.html` en `sitemap.xml` worden door het bouwscript gemaakt. Pas die niet met de hand aan.

## Een tekst aanpassen

1. Pas de tekst aan in `bron/teksten/nl.json`.
2. Vertaal: `DEEPL_SLEUTEL=jouw-sleutel python3 bron/vertaal.py`
   (alleen gewijzigde of nieuwe sleutels worden vertaald).
3. Bouw: `pip install pillow` (eenmalig), dan `python3 bron/bouw.py`.

Een gratis DeepL-sleutel maak je aan op deepl.com (DeepL API Free). Sleutel nooit in de code of op GitHub zetten.
Lees de Franse en Engelse tekst na een vertaling altijd even na.

## Een werk toevoegen

1. Zet `<naam>-klein.webp` (max 1000 px breed) en `<naam>-groot.webp` (max 2400 px) in `afbeeldingen/werken/`.
2. Voeg het werk toe in `bron/gegevens.py`, onder het juiste vak.
3. Voeg in `nl.json` toe: `werk.<id>.titel`, `werk.<id>.soort`, `werk.<id>.tekst` en `alt.werken/<naam>`.
4. Vertalen en bouwen zoals hierboven.

## Lokaal bekijken

`python3 -m http.server 8000` in deze map, en open http://localhost:8000.

## Publiceren

Zet de hele map (zonder niets weg te laten) op een statische hosting met HTTPS en laat `afonsomatosdacruz.be` ernaar wijzen.
Dien daarna `https://afonsomatosdacruz.be/sitemap.xml` in bij Google Search Console.
Het contactformulier verstuurt naar Formspree; berichten komen in je mailbox.
