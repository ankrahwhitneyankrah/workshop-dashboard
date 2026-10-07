"""Stufe 4: Bericht teilen. Legt Dashboard und PowerPoint in einen Teams-Ordner
und schreibt dazu die Nachricht, die ein Teams-Workflow automatisch im Kanal postet.

Starten im Terminal:  python teilen.py

Einmal einrichten:
1. In Teams im Kanal auf "Freigegeben" bzw. "Dateien" -> "..." -> "Verknüpfung zu OneDrive
   hinzufügen" -> "Meine Dateien". Der Ordner erscheint dann im Datei-Explorer unter OneDrive.
2. Den Pfad dieses Ordners in die Datei teilen_ordner.txt schreiben (eine Zeile).
   Die Datei bleibt auf eurem Rechner und wird nie hochgeladen.
3. Optional: in Teams einen Workflow einrichten, der jede neue Datei im Unterordner
   "Meldungen" als Nachricht postet (Anleitung: ANLEITUNG_TEAMS.md).

Alles bleibt innerhalb des Unternehmens. Deshalb ist das der Weg für echte Daten.
"""

import shutil
import sys
from pathlib import Path

from bericht import Datenfehler, berechnen, laden, monat_name, ueber_plan, zahl

ORDNER = Path(__file__).parent
EINSTELLUNG = ORDNER / "teilen_ordner.txt"
DATEIEN = [ORDNER / "ausgabe" / "dashboard.html", ORDNER / "ausgabe" / "praesentation.pptx"]


def zielordner():
    if not EINSTELLUNG.exists():
        print("Noch nicht eingerichtet: Die Datei teilen_ordner.txt fehlt.")
        print("Pfad des Teams-Ordners hineinschreiben, z. B.")
        print(r"  C:\Users\<Kürzel>\OneDrive - <Firma>\<Team> - Allgemein")
        print("Anleitung: siehe Anfang von teilen.py")
        sys.exit(1)
    ziel = Path(EINSTELLUNG.read_text(encoding="utf-8").strip().strip('"'))
    if not ziel.is_dir():
        print(f"Den Ordner gibt es nicht: {ziel}")
        print("Pfad in teilen_ordner.txt prüfen. Ist die Verknüpfung in OneDrive angelegt?")
        sys.exit(1)
    return ziel


def nachricht(df, name):
    """Die Teams-Nachricht. Inhalt und Ton richten sich nach den Zahlen.

    Hier anpassen, was im Kanal stehen soll. Der Workflow in Teams schickt den Text nur weiter.
    """
    k = berechnen(df)
    letzter = sorted(df["Monat"].unique())[-1]
    zeilen = [
        f"<b>📊 Neuer Projektbericht: {monat_name(letzter)}</b>",
        f"Zeitraum: {k['zeitraum']}",
        f"{zahl(k['anzahl_projekte'])} Projekte · Plan {zahl(k['plan_stunden'])} h · "
        f"Ist {zahl(k['ist_stunden'])} h · Ausschöpfung {zahl(k['ausschoepfung'] * 100)} %",
    ]
    ueber = ueber_plan(df)
    if len(ueber):
        liste = ", ".join(f"{z['Projekt']} {zahl(z['Abweichung'], vorzeichen=True)} h" for _, z in ueber.iterrows())
        projekte = "Projekt liegt" if len(ueber) == 1 else "Projekte liegen"
        zeilen.append(f"⚠️ <b>{len(ueber)} {projekte} über Plan:</b> {liste}")
    else:
        zeilen.append("✅ Alle Projekte liegen im Plan.")
    zeilen.append(f"Dashboard und PowerPoint: <i>{name}</i> im Tab „Freigegeben“")
    return "<br>".join(zeilen)


def main():
    ziel = zielordner()
    try:
        df = laden()
    except Datenfehler as fehler:
        print("FEHLER: Mindestens eine Excel-Datei ist nicht in Ordnung. Es wurde nichts geteilt.\n")
        print(fehler)
        sys.exit(1)

    vorhanden = [d for d in DATEIEN if d.exists()]
    if not vorhanden:
        print("Im Ordner ausgabe/ liegt noch nichts. Zuerst Dashboard bzw. Präsentation erstellen.")
        sys.exit(1)

    # z. B. Projektstatus_2026-09.html – jeder Monat bleibt im Kanal erhalten
    name = f"Projektstatus_{sorted(df['Monat'].unique())[-1]}"
    for datei in vorhanden:
        shutil.copy2(datei, ziel / f"{name}{datei.suffix}")
        print(f"Geteilt: {name}{datei.suffix}")

    # Zuletzt die Nachricht: Sobald sie im Ordner "Meldungen" liegt, postet der Workflow sie
    meldungen = ziel / "Meldungen"
    meldungen.mkdir(exist_ok=True)
    (meldungen / f"{name}.txt").write_text(nachricht(df, name), encoding="utf-8")
    print(f"Nachricht abgelegt: Meldungen/{name}.txt")
    print(f"Ziel: {ziel}")


if __name__ == "__main__":
    main()
