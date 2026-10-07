"""Stufe 1: Erstellt aus allen Monatsdateien in daten/ das Dashboard ausgabe/dashboard.html.

Starten im Terminal:  python dashboard.py
Das Ergebnis ist eine einzige HTML-Datei mit Filtern. Sie funktioniert ohne
Internet und lässt sich einfach weitergeben.

Aufgabenteilung:
- bericht.py              prüft die Daten und berechnet die Kennzahlen
- dashboard.py (hier)     legt fest, welche Kennzahlen als Kacheln erscheinen
- dashboard_vorlage.html  Aussehen und Bedienung (Filter, Diagramme, Tabelle)
"""

import json
import os
import sys
import webbrowser
from datetime import datetime
from pathlib import Path

from bericht import (DATEN_ORDNER, ERLAUBTER_STATUS, Datenfehler, berechnen, laden, monat_name,
                     veraenderung, zahl)

ORDNER = Path(__file__).parent
VORLAGE = ORDNER / "dashboard_vorlage.html"
AUSGABE = ORDNER / "ausgabe" / "dashboard.html"
ALLE = "Alle"

# Die Kacheln oben im Dashboard. Für eine neue Kennzahl: in bericht.py berechnen
# und hier eine Zeile ergänzen. Formate: zahl, stunden, abweichung, prozent
KARTEN = [
    # Schlüssel aus berechnen()  Titel             Erklärung                      Format
    ("anzahl_projekte",          "Projekte",       "in der Auswahl",              "zahl"),
    ("plan_stunden",             "Plan-Stunden",   "Summe der Planung",           "stunden"),
    ("ist_stunden",              "Ist-Stunden",    "Summe des Aufwands",          "stunden"),
    ("abweichung",               "Abweichung",     "Ist minus Plan",              "abweichung"),
    ("ausschoepfung",            "Ausschöpfung",   "Anteil des Plans verbraucht", "prozent"),
]


def kennzahlen_je_auswahl(df):
    """Berechnet die Kennzahlen für jede Filterkombination aus Bereich und Monat.

    Dazu für jeden einzelnen Monat die Veränderung zum Vormonat.
    So rechnet das Dashboard beim Filtern nichts selbst, sondern zeigt immer
    Werte aus bericht.py an.
    """
    monate = sorted(df["Monat"].unique())
    kennzahlen, vergleich = {}, {}
    for bereich in [ALLE, *sorted(df["Bereich"].unique())]:
        teil = df if bereich == ALLE else df[df["Bereich"] == bereich]
        kennzahlen[f"{bereich}|{ALLE}"] = berechnen(teil) if len(teil) else None
        for i, monat in enumerate(monate):
            auswahl = teil[teil["Monat"] == monat]
            kennzahlen[f"{bereich}|{monat}"] = berechnen(auswahl) if len(auswahl) else None
            vormonat = kennzahlen.get(f"{bereich}|{monate[i - 1]}") if i else None
            if kennzahlen[f"{bereich}|{monat}"] and vormonat:
                vergleich[f"{bereich}|{monat}"] = {
                    "vormonat": monat_name(monate[i - 1]),
                    "werte": veraenderung(kennzahlen[f"{bereich}|{monat}"], vormonat),
                }
    return kennzahlen, vergleich


def json_wert(wert):
    """Wandelt Zahlen aus pandas/numpy in normale Python-Zahlen für JSON um."""
    if hasattr(wert, "item"):
        return wert.item()
    raise TypeError(f"Nicht in JSON umwandelbar: {wert!r}")


def dashboard_daten(df, k, dateien):
    kennzahlen, vergleich = kennzahlen_je_auswahl(df)
    zeilen = [
        {
            "Monat": str(z["Monat"]),
            "Projekt": str(z["Projekt"]),
            "Bereich": str(z["Bereich"]),
            "Status": str(z["Status"]),
            "Plan_Stunden": float(z["Plan_Stunden"]),
            "Ist_Stunden": float(z["Ist_Stunden"]),
        }
        for _, z in df.iterrows()
    ]
    return {
        "zeitraum": k["zeitraum"],
        "erstellt": datetime.now().strftime("%d.%m.%Y %H:%M"),
        "dateien": dateien,
        "monate": [{"schluessel": m, "name": monat_name(m)} for m in sorted(df["Monat"].unique())],
        "bereiche": sorted(df["Bereich"].unique().tolist()),
        "status": ERLAUBTER_STATUS,
        "zeilen": zeilen,
        "karten": [
            {"schluessel": s, "titel": t, "erklaerung": e, "format": f} for s, t, e, f in KARTEN
        ],
        "kennzahlen": kennzahlen,
        "vergleich": vergleich,
    }


def main():
    try:
        df = laden()
    except Datenfehler as fehler:
        print("FEHLER: Mindestens eine Excel-Datei ist nicht in Ordnung. Es wurde kein Dashboard erstellt.\n")
        print(fehler)
        sys.exit(1)

    k = berechnen(df)
    dateien = sorted(d.name for d in DATEN_ORDNER.glob("*.xlsx") if not d.name.startswith("~$"))
    daten = json.dumps(dashboard_daten(df, k, dateien), ensure_ascii=False, default=json_wert)
    daten = daten.replace("</", "<\\/")  # damit Projektnamen das HTML nicht stören können
    html = VORLAGE.read_text(encoding="utf-8").replace("__DATEN__", daten)

    AUSGABE.parent.mkdir(exist_ok=True)
    AUSGABE.write_text(html, encoding="utf-8")

    print(f"Dashboard erstellt: {AUSGABE.name} ({k['zeitraum']}, {len(dateien)} Monatsdateien)")
    print(f"  Projekte: {zahl(k['anzahl_projekte'])} | Plan: {zahl(k['plan_stunden'])} h | "
          f"Ist: {zahl(k['ist_stunden'])} h | Abweichung: {zahl(k['abweichung'], vorzeichen=True)} h")

    # Lokal direkt im Browser öffnen, in GitHub Actions (CI) nicht.
    if not os.environ.get("CI"):
        webbrowser.open(AUSGABE.resolve().as_uri())


if __name__ == "__main__":
    main()
