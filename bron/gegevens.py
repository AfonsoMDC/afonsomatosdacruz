"""Alle gegevens van de website op één plek. Teksten staan NIET hier, maar in teksten/nl.json."""

TALEN = ["nl", "en", "fr"]
DOMEIN = "https://afonsomatosdacruz.be"
FORMULIER_ADRES = "https://formspree.io/f/mjgqenly"
EMAIL = "afonsomatos820@gmail.com"
INSTAGRAM = "https://www.instagram.com/afonso.mdc"
YOUTUBE_FILM = "https://www.youtube.com/watch?v=1lDdIhFydRo"

# Een beeld is (map, naam). De bestanden heten afbeeldingen/<map>/<naam>-klein.webp en -groot.webp
# Een werk heeft een id (voor de tekstsleutels werk.<id>.titel / .soort / .tekst) en een lijst beelden.
def beelden(map, *namen):
    return [(map, naam) for naam in namen]

VAKKEN = [
    ("affiches", [
        ("gyokeres", beelden("werken", "poster-gyokeres")),
        ("travis-scott", beelden("werken", "poster-travis-scott")),
        ("english-breakfast", beelden("werken", "poster-english-breakfast")),
        ("verbondenheid", beelden("werken", "poster-verbondenheid")),
        ("silent-spring", beelden("werken", "silent-spring")),
    ]),
    ("identiteit", [
        ("logo-afonso", beelden("werken", "logo-afonso")),
        ("the-circle", beelden("werken", "the-circle-logo", "the-circle-kaart-voor", "the-circle-kaart-achter",
                               "the-circle-mockup-1", "the-circle-mockup-2", "the-circle-mockup-3")),
        ("kaartje-vis", beelden("werken", "kaartje-vis-voor", "kaartje-vis-achter")),
        ("waveform-ticket", beelden("werken", "waveform-ticket")),
    ]),
    ("editorial", [
        ("broodthaers", beelden("werken", "broodthaers-1", "broodthaers-2", "broodthaers-3")),
        ("bertoia", beelden("werken", "bertoia-1", "bertoia-2")),
    ]),
    ("webdesign", [
        ("web-beeld-twijfel-constructie", beelden("webdesign", "beeld-twijfel-constructie")),
        ("web-disco-van-spread-naar-html", beelden("webdesign", "disco-van-spread-naar-html")),
        ("web-disco-memphis-design", beelden("webdesign", "disco-memphis-design")),
        ("web-oostende-stad-aan-zee", beelden("webdesign", "oostende-stad-aan-zee")),
        ("web-badcultuur-oostende", beelden("webdesign", "badcultuur-oostende")),
    ]),
]

# Een project heeft onderdelen. Een onderdeel is (id, beelden of video).
# Teksten: project.<id>.<onderdeel>.titel en .tekst
PROJECTEN = [
    ("smak", [
        ("schaduwaffiche", beelden("smak", "schaduwaffiche", "schaduwfoto"), None),
        ("animatie", [], "smak-posteranimatie"),
        ("archiefdoos", beelden("smak", "archiefdoos"), None),
        ("archieffoto", beelden("smak", "archieffoto", "archieffoto-bewerkt"), None),
        ("schimmenfilm", [], "smak-schimmenfilm"),
        ("bomen", beelden("smak", "bomen"), None),
        ("pixelbeeld", beelden("smak", "pixelbeeld"), None),
        ("affiche", beelden("smak", "affiche", "affiche-mockup"), None),
        ("uitnodiging", beelden("smak", "uitnodiging-voor", "uitnodiging-achter"), None),
        ("website", beelden("webdesign", "beeld-twijfel-constructie"), None),
    ]),
    ("disco", [
        ("moodboards", beelden("disco", "moodboard-1", "moodboard-2"), None),
        ("spread", beelden("disco", "spread"), None),
        ("video", [], "disco-sfeerfilm"),
        ("website1", beelden("webdesign", "disco-van-spread-naar-html"), None),
        ("website2", beelden("webdesign", "disco-memphis-design"), None),
    ]),
    ("oostende", [
        ("stijlhandleiding", beelden("oostende", "styleguide"), None),
        ("spread", beelden("oostende", "spread"), None),
        ("personage", beelden("oostende", "personage"), "oostende-personage-animatie"),
        ("website1", beelden("webdesign", "oostende-stad-aan-zee"), None),
        ("website2", beelden("webdesign", "badcultuur-oostende"), None),
    ]),
]

# Films: (id, project waar de film bij hoort). Bestanden: video/<id>.mp4 en afbeeldingen/film/<id>.webp
FILMS = [
    ("smak-schimmenfilm", "smak"),
    ("disco-sfeerfilm", "disco"),
    ("oostende-personage-animatie", "oostende"),
    ("smak-posteranimatie", "smak"),
]

AANTAL_FOTOS = 27
