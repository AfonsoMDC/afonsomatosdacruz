"""Bouwt de hele website uit sjablonen/ en teksten/. Gebruik: python3 bron/bouw.py

Elke pagina wordt in drie talen geschreven: nl in de hoofdmap, en/ en fr/ in submappen.
Een ontbrekende tekstsleutel of een ontbrekend beeld stopt de bouw met een foutmelding.
"""
import html
import json
import re
from pathlib import Path

from PIL import Image

import gegevens as g

WORTEL = Path(__file__).parent.parent
SJABLONEN = Path(__file__).parent / "sjablonen"
NAAM = "Afonso Matos da Cruz"
LANDCODES = {"nl": "nl_BE", "en": "en_GB", "fr": "fr_BE"}


# ---------- Teksten en sjablonen ----------
def laad_teksten():
    alle = {taal: json.loads((Path(__file__).parent / "teksten" / f"{taal}.json").read_text(encoding="utf8"))
            for taal in g.TALEN}
    for taal in g.TALEN:
        ontbreekt = set(alle["nl"]) - set(alle[taal])
        assert not ontbreekt, f"{taal}.json mist sleutels: {sorted(ontbreekt)[:5]}. Draai eerst bron/vertaal.py"
    return alle


def veilig(tekst):
    """Maakt tekst veilig voor HTML, maar laat <br> staan."""
    return html.escape(tekst, quote=False).replace("&lt;br&gt;", "<br>")


def vul(sjabloon_naam, waarden):
    """Vult {{sleutel}} in een sjabloon, ook in ingevoegde blokken, tot er niets meer te vullen is."""
    tekst = (SJABLONEN / f"{sjabloon_naam}.html").read_text(encoding="utf8")
    for _ in range(5):
        tekst = re.sub(r"\{\{([\w.\-]+)\}\}", lambda m: waarden[m.group(1)], tekst)
        if "{{" not in tekst:
            return tekst
    raise ValueError(f"Sjabloon {sjabloon_naam} bevat nog onvolledige placeholders")


# ---------- Adressen ----------
def url(taal, pad=""):
    voorvoegsel = "" if taal == "nl" else f"/{taal}"
    return f"{voorvoegsel}/{pad}"


# ---------- Beelden ----------
maten = {}


def maat(map, naam, formaat):
    sleutel = (map, naam, formaat)
    if sleutel not in maten:
        with Image.open(WORTEL / f"afbeeldingen/{map}/{naam}-{formaat}.webp") as beeld:
            maten[sleutel] = beeld.size
    return maten[sleutel]


def beeld(tekst, map, naam, sizes, laden="lazy"):
    klein, groot = maat(map, naam, "klein"), maat(map, naam, "groot")
    bron = f"/afbeeldingen/{map}/{naam}"
    return (f'<img src="{bron}-klein.webp" srcset="{bron}-klein.webp {klein[0]}w, {bron}-groot.webp {groot[0]}w" '
            f'sizes="{sizes}" width="{klein[0]}" height="{klein[1]}" alt="{html.escape(tekst[f"alt.{map}/{naam}"])}" '
            f'loading="{laden}" decoding="async">')


def vergroting_gegevens(tekst, lijst):
    return html.escape(json.dumps([{"src": f"/afbeeldingen/{m}/{n}-groot.webp", "alt": tekst[f"alt.{m}/{n}"]}
                                   for m, n in lijst], ensure_ascii=False), quote=True)


def tegel(tekst, lijst, titel="", soort="", uitleg="", start=0):
    """Een vierkante tegel die bij een klik de beelden in een groot venster toont."""
    map, naam = lijst[start]
    aantal = f" · {len(lijst)} {tekst['algemeen.beelden']}" if len(lijst) > 1 and soort else ""
    onderschrift = (f'<span class="onderschrift"><b>{veilig(titel)}</b><span>{veilig(soort)}{aantal}</span></span>'
                    if titel and soort else "")
    return (f'<a class="tegel" href="/afbeeldingen/{map}/{naam}-groot.webp" data-start="{start}" '
            f'data-beelden="{vergroting_gegevens(tekst, lijst)}" data-titel="{html.escape(titel)}" '
            f'data-tekst="{html.escape(uitleg)}"><span class="beeld">'
            f'{beeld(tekst, map, naam, "(min-width: 1100px) 25vw, (min-width: 700px) 33vw, 50vw")}</span>'
            f'{onderschrift}</a>')


def omslag(tekst, naam, adres, titel, soort):
    return (f'<a class="tegel" href="{adres}"><span class="beeld"><img src="/afbeeldingen/omslag/{naam}.webp" '
            f'width="1200" height="1200" alt="" loading="lazy" decoding="async"></span>'
            f'<span class="onderschrift"><b>{veilig(titel)}</b><span>{veilig(soort)}</span></span></a>')


def video(tekst, naam, titel):
    return (f'<figure class="film"><video controls preload="none" poster="/afbeeldingen/film/{naam}.webp" '
            f'aria-label="{html.escape(titel)}"><source src="/video/{naam}.mp4" type="video/mp4">'
            f'{veilig(tekst["film.geen_video"])}</video>@@onderschrift@@</figure>')


# ---------- Blokken per pagina ----------
def blok_werk(taal, tekst):
    projecten = "".join(
        omslag(tekst, pid, url(taal, f"project/{pid}/"),
               tekst[f"project.{pid}.titel"], tekst[f"project.{pid}.ondertitel"])
        for pid, _ in g.PROJECTEN)
    vakken = [("projecten", f'<div class="tegels drie">{projecten}</div>')]
    for vak, werken in g.VAKKEN:
        tegels = "".join(
            tegel(tekst, lijst, tekst[f"werk.{wid}.titel"], tekst[f"werk.{wid}.soort"], tekst[f"werk.{wid}.tekst"])
            for wid, lijst in werken)
        vakken.append((vak, f'<div class="tegels">{tegels}</div>'))
    return "".join(
        f'<section class="vak raster"><div class="vak-kop"><h2>{veilig(tekst[f"werk.vak_{vak}"])}</h2>'
        f'<p>{veilig(tekst[f"werk.vak_{vak}_tekst"])}</p></div>{inhoud}</section>' for vak, inhoud in vakken)


def blok_project(taal, tekst, pid):
    onderdelen = dict(g.PROJECTEN)[pid]
    html_onderdelen = []
    for nummer, (oid, lijst, film) in enumerate(onderdelen, 1):
        sleutel = f"project.{pid}.{oid}"
        titel, uitleg = tekst[f"{sleutel}.titel"], tekst[f"{sleutel}.tekst"]
        media = "".join(tegel(tekst, lijst, titel, "", uitleg, start=i) for i in range(len(lijst)))
        if film:
            media += video(tekst, film, tekst[f"film.{film}.titel"]).replace("@@onderschrift@@", "")
        html_onderdelen.append(
            f'<section class="onderdeel raster"><div class="tekstblok"><span class="nummer">{nummer:02d}</span>'
            f'<h3>{veilig(titel)}</h3><p>{veilig(uitleg)}</p></div><div class="media">{media}</div></section>')
    return "".join(html_onderdelen)


def blok_gegevens(tekst, pid):
    rijen = [("project.label_soort", tekst["project.soort_school"]),
             ("project.label_school", f'{tekst["project.school_dbsdw"]} · {tekst[f"project.{pid}.klas"]}')]
    if f"project.{pid}.wanneer" in tekst:
        rijen.append(("project.label_wanneer", tekst[f"project.{pid}.wanneer"]))
    rijen.append(("project.label_gemaakt", tekst[f"project.{pid}.gemaakt"]))
    return "".join(f'<div><dt>{veilig(tekst[k])}</dt><dd>{veilig(w)}</dd></div>' for k, w in rijen)


def blok_films(taal, tekst):
    lijst = []
    for fid, pid in g.FILMS:
        onderschrift = (f'<figcaption><b>{veilig(tekst[f"film.{fid}.titel"])}</b>{veilig(tekst[f"film.{fid}.tekst"])}'
                        f'<p class="klein">{veilig(tekst["film.duur"])} {tekst[f"film.{fid}.duur"]} · '
                        f'{veilig(tekst["film.uit_project"])}: <a class="tekstlink" href="{url(taal, f"project/{pid}/")}">'
                        f'{veilig(tekst[f"project.{pid}.titel"])}</a></p></figcaption>')
        lijst.append(video(tekst, fid, tekst[f"film.{fid}.titel"]).replace("@@onderschrift@@", onderschrift))
    return "".join(lijst)


def blok_start(taal, tekst):
    tegels = "".join([
        omslag(tekst, "werk", url(taal, "werk/"), tekst["nav.werk"], tekst["start.tegel_werk"]),
        omslag(tekst, "fotografie", url(taal, "fotografie/"), tekst["nav.fotografie"], tekst["start.tegel_fotografie"]),
        omslag(tekst, "film", url(taal, "film/"), tekst["nav.film"], tekst["start.tegel_film"]),
    ])
    opleiding = "".join(f'<li><span>{veilig(tekst[f"over.opleiding_{i}_jaar"])}</span>{veilig(tekst[f"over.opleiding_{i}"])}</li>'
                        for i in (1, 2, 3))
    foto = beeld(tekst, "algemeen", "aan-het-werk", "(min-width: 900px) 33vw, 100vw")
    cv_taal = "nl" if taal == "nl" else "en"  # er is geen Franse cv: Frans verwijst naar de Engelse
    return {"start_tegels": tegels, "opleiding_lijst": opleiding, "over_foto": foto,
            "cv_url": f"/cv/cv-afonso-matos-da-cruz-{cv_taal}.pdf"}


# ---------- Pagina's ----------
def menu(taal, tekst, actief):
    items = [("werk/", "nav.werk"), ("fotografie/", "nav.fotografie"), ("film/", "nav.film"),
             ("#over", "nav.over"), ("#contact", "nav.contact")]
    schakels = []
    for pad, sleutel in items:
        adres = url(taal, pad) if not pad.startswith("#") else url(taal) + pad
        huidig = ' aria-current="page"' if pad == actief else ""
        schakels.append(f'<a href="{adres}"{huidig}>{veilig(tekst[sleutel])}</a>')
    return "".join(schakels)


def taalkeuze(taal, pad):
    return "".join(f'<a href="{url(t, pad)}" hreflang="{t}" lang="{t}"'
                   f'{" aria-current=\"true\"" if t == taal else ""}>{t.upper()}</a>' for t in g.TALEN)


def hreflang(pad):
    regels = [f'<link rel="alternate" hreflang="{t}" href="{g.DOMEIN}{url(t, pad)}">' for t in g.TALEN]
    regels.append(f'<link rel="alternate" hreflang="x-default" href="{g.DOMEIN}{url("nl", pad)}">')
    return "\n".join(regels)


def json_ld(gegevens):
    return f'<script type="application/ld+json">{json.dumps(gegevens, ensure_ascii=False)}</script>'


def persoon(taal, tekst):
    return {"@type": "Person", "@id": f"{g.DOMEIN}/#afonso", "name": NAAM, "url": g.DOMEIN + "/",
            "description": tekst["start.beschrijving"], "sameAs": [g.INSTAGRAM],
            "address": {"@type": "PostalAddress", "addressLocality": "Gent", "addressCountry": "BE"}}


def schrijf_pagina(taal, tekst, pad, sjabloon, titel, beschrijving, blokken, actief=None, scripts=(), lichtbak=False,
                   gestructureerd=None):
    waarden = {sleutel: veilig(waarde) for sleutel, waarde in tekst.items()}
    waarden.update(blokken)
    waarden.update({
        "taal": taal, "landcode": LANDCODES[taal], "domein": g.DOMEIN,
        "paginatitel": html.escape(titel), "paginabeschrijving": html.escape(beschrijving),
        "canoniek": g.DOMEIN + url(taal, pad), "hreflang": hreflang(pad),
        "start_url": url(taal), "privacy_url": url(taal, "privacy/"),
        "menu": menu(taal, tekst, actief), "taalkeuze": taalkeuze(taal, pad),
        "email": g.EMAIL, "instagram": g.INSTAGRAM, "formulier_adres": g.FORMULIER_ADRES, "youtube": g.YOUTUBE_FILM,
        "gestructureerde_gegevens": json_ld(gestructureerd) if gestructureerd else "",
        "scripts": "".join(f'<script src="/javascript/{s}.js" defer></script>' for s in scripts),
    })
    waarden["inhoud"] = vul(sjabloon, waarden)
    waarden["vergroting"] = vul("vergroting", waarden) if lichtbak else ""
    uitvoer = WORTEL / url(taal, pad).strip("/")
    if not pad.endswith(".html"):
        uitvoer = uitvoer / "index.html"
    uitvoer.parent.mkdir(parents=True, exist_ok=True)
    uitvoer.write_text(vul("basis", waarden), encoding="utf8")


def bouw_taal(taal, tekst):
    start_blokken = blok_start(taal, tekst)
    schrijf_pagina(taal, tekst, "", "start", tekst["start.titel"], tekst["start.beschrijving"], start_blokken,
                   scripts=["formulier"],
                   gestructureerd={"@context": "https://schema.org", "@graph": [persoon(taal, tekst)]})
    schrijf_pagina(taal, tekst, "werk/", "werk", tekst["werk.titel"], tekst["werk.beschrijving"],
                   {"vakken": blok_werk(taal, tekst)}, actief="werk/", scripts=["vergroting"], lichtbak=True)
    ids = [pid for pid, _ in g.PROJECTEN]
    for nummer, pid in enumerate(ids):
        volgend = ids[(nummer + 1) % len(ids)]
        titel_p = f'{tekst[f"project.{pid}.titel"]} — {NAAM}'
        schrijf_pagina(taal, tekst, f"project/{pid}/", "project", titel_p, tekst[f"project.{pid}.beschrijving"], {
            "projecttitel": veilig(tekst[f"project.{pid}.titel"]),
            "projectondertitel": veilig(tekst[f"project.{pid}.ondertitel"]),
            "projectintro": veilig(tekst[f"project.{pid}.intro"]),
            "project_gegevens": blok_gegevens(tekst, pid),
            "onderdelen": blok_project(taal, tekst, pid),
            "volgend_url": url(taal, f"project/{volgend}/"), "volgend_titel": veilig(tekst[f"project.{volgend}.titel"]),
        }, actief="werk/", scripts=["vergroting"], lichtbak=True,
            gestructureerd={"@context": "https://schema.org", "@type": "CreativeWork",
                            "name": tekst[f"project.{pid}.titel"], "description": tekst[f"project.{pid}.beschrijving"],
                            "url": g.DOMEIN + url(taal, f"project/{pid}/"), "inLanguage": taal,
                            "image": f"{g.DOMEIN}/afbeeldingen/omslag/{pid}.webp",
                            "author": {"@id": f"{g.DOMEIN}/#afonso"}})
    fotos = [("fotografie", f"straat-{i:02d}") for i in range(1, g.AANTAL_FOTOS + 1)]
    foto_tegels = "".join(tegel(tekst, fotos, start=i) for i in range(len(fotos)))
    schrijf_pagina(taal, tekst, "fotografie/", "fotografie", tekst["fotografie.titel"], tekst["fotografie.beschrijving"],
                   {"foto_tegels": foto_tegels}, actief="fotografie/", scripts=["vergroting"], lichtbak=True)
    schrijf_pagina(taal, tekst, "film/", "film", tekst["film.titel"], tekst["film.beschrijving"],
                   {"film_lijst": blok_films(taal, tekst)}, actief="film/")
    schrijf_pagina(taal, tekst, "privacy/", "privacy", tekst["privacy.titel"], tekst["privacy.beschrijving"], {})
    schrijf_pagina(taal, tekst, "404.html", "fout", tekst["fout.titel"], tekst["fout.beschrijving"], {})


def schrijf_sitemap():
    paden = ["", "werk/", *[f"project/{p}/" for p, _ in g.PROJECTEN], "fotografie/", "film/", "privacy/"]
    regels = ['<?xml version="1.0" encoding="UTF-8"?>',
              '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for pad in paden:
        for taal in g.TALEN:
            regels.append(f"<url><loc>{g.DOMEIN}{url(taal, pad)}</loc>")
            regels += [f'<xhtml:link rel="alternate" hreflang="{t}" href="{g.DOMEIN}{url(t, pad)}"/>' for t in g.TALEN]
            regels.append(f'<xhtml:link rel="alternate" hreflang="x-default" href="{g.DOMEIN}{url("nl", pad)}"/></url>')
    regels.append("</urlset>")
    (WORTEL / "sitemap.xml").write_text("\n".join(regels), encoding="utf8")


def main():
    teksten = laad_teksten()
    for taal in g.TALEN:
        bouw_taal(taal, teksten[taal])
    schrijf_sitemap()
    print("Klaar: 3 talen gebouwd.")


if __name__ == "__main__":
    main()
