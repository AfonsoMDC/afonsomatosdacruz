"""Vertaalt gewijzigde Nederlandse teksten automatisch naar Engels en Frans met DeepL.

Gebruik:  DEEPL_SLEUTEL=jouw-sleutel python3 bron/vertaal.py
Wat het doet: vergelijkt teksten/nl.json met teksten/nl_vorige.json, vertaalt alleen
nieuwe of gewijzigde sleutels en schrijft het resultaat in en.json en fr.json.
"""
import json
import os
import re
import urllib.request
from pathlib import Path

MAP = Path(__file__).parent / "teksten"
DOELTALEN = {"en": "EN-GB", "fr": "FR"}


def lees(naam):
    return json.loads((MAP / f"{naam}.json").read_text(encoding="utf8"))


def schrijf(naam, gegevens):
    tekst = json.dumps(gegevens, ensure_ascii=False, indent=1, sort_keys=True)
    (MAP / f"{naam}.json").write_text(tekst, encoding="utf8")


def deepl(teksten, doeltaal, sleutel):
    """Stuurt een lijst teksten naar DeepL en geeft de vertalingen terug, in dezelfde volgorde."""
    server = "api-free.deepl.com" if sleutel.endswith(":fx") else "api.deepl.com"
    verzoek = urllib.request.Request(
        f"https://{server}/v2/translate",
        data=json.dumps({"text": teksten, "source_lang": "NL", "target_lang": doeltaal,
                         "tag_handling": "html"}).encode(),
        headers={"Authorization": f"DeepL-Auth-Key {sleutel}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(verzoek) as antwoord:
        return [r["text"] for r in json.load(antwoord)["translations"]]


def franse_spaties(tekst):
    """Frans zet een vaste spatie voor : ; ? ! en binnen « »."""
    tekst = re.sub(r" ([:;?!»])", " \\1", tekst)
    return tekst.replace("« ", "« ")


def vertaal(nl, vorige, bestaand, taal, vertaler):
    """Geeft de vertaalde teksten van één taal terug. Alleen nieuwe of gewijzigde sleutels worden vertaald."""
    nieuw = {sleutel: tekst for sleutel, tekst in bestaand.items() if sleutel in nl}
    te_doen = [s for s in nl if s not in nieuw or vorige.get(s) != nl[s]]
    if te_doen:
        vertalingen = vertaler([nl[s] for s in te_doen], DOELTALEN[taal])
        for sleutel, tekst in zip(te_doen, vertalingen):
            nieuw[sleutel] = franse_spaties(tekst) if taal == "fr" else tekst
    return nieuw, len(te_doen)


def main():
    nl, vorige = lees("nl"), lees("nl_vorige")
    gewijzigd = [s for s in nl if vorige.get(s) != nl[s]]
    ontbreekt = [s for taal in DOELTALEN for s in nl if s not in lees(taal)]
    if not gewijzigd and not ontbreekt:
        print("Niets te vertalen.")
        return
    sleutel = os.environ["DEEPL_SLEUTEL"]  # KeyError als de sleutel ontbreekt: dat is de bedoeling
    for taal in DOELTALEN:
        nieuw, aantal = vertaal(nl, vorige, lees(taal), taal, lambda t, d: deepl(t, d, sleutel))
        schrijf(taal, nieuw)
        print(f"{taal}: {aantal} teksten vertaald")
    schrijf("nl_vorige", nl)


if __name__ == "__main__":
    main()
