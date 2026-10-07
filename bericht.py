"""Das Herzstück: alle Monatsdateien laden, prüfen und Kennzahlen berechnen.

Im Ordner daten/ liegt eine Excel-Datei pro Monat. Jede neue Datei kommt dazu,
das Dashboard zeigt dann alle Monate zusammen.

dashboard.py und praesentation.py verwenden beide diese Datei.
So zeigen Dashboard und PowerPoint garantiert dieselben Zahlen.
"""

from numbers import Number
from pathlib import Path

import pandas as pd

DATEN_ORDNER = Path(__file__).parent / "daten"
PFLICHTSPALTEN = ["Monat", "Projekt", "Bereich", "Status", "Plan_Stunden", "Ist_Stunden"]
ERLAUBTER_STATUS = ["geplant", "laufend", "abgeschlossen"]
MONATSNAMEN = ["Januar", "Februar", "März", "April", "Mai", "Juni",
               "Juli", "August", "September", "Oktober", "November", "Dezember"]


class Datenfehler(Exception):
    """Mindestens eine Excel-Datei ist fehlerhaft. Dann wird nichts erzeugt."""


def laden(ordner=DATEN_ORDNER):
    """Liest alle Monatsdateien, prüft jede einzeln und fügt sie zu einer Tabelle zusammen."""
    # "~$..." sind Sperrdateien, die Excel anlegt, solange eine Datei geöffnet ist
    dateien = sorted(d for d in Path(ordner).glob("*.xlsx") if not d.name.startswith("~$"))
    if not dateien:
        raise Datenfehler(f"Im Ordner {Path(ordner).name}/ liegt keine Excel-Datei.")

    teile, fehler, herkunft = [], [], {}
    for datei in dateien:
        df = pd.read_excel(datei)  # erstes Tabellenblatt
        try:
            pruefen(df)
        except Datenfehler as f:
            fehler.append(f"{datei.name}:\n{f}")
            continue
        df["Monat"] = monat_schluessel(df["Monat"])
        herkunft.setdefault(df["Monat"].iloc[0], []).append(datei.name)
        teile.append(df)

    for monat, namen in herkunft.items():
        if len(namen) > 1:
            fehler.append(f"Der Monat {monat_name(monat)} steht in mehreren Dateien: " + ", ".join(namen))
    if fehler:
        raise Datenfehler("\n\n".join(fehler))
    return pd.concat(teile, ignore_index=True).sort_values(["Monat", "Projekt"], ignore_index=True)


def pruefen(df):
    """Prüft EINE Monatsdatei. Sammelt alle Fehler und stoppt, falls es welche gibt."""
    fehlende = [spalte for spalte in PFLICHTSPALTEN if spalte not in df.columns]
    if fehlende:
        raise Datenfehler("Diese Spalten fehlen: " + ", ".join(fehlende))
    if df.empty:
        raise Datenfehler("Die Tabelle enthält keine Projekte.")

    fehler = []

    doppelt = df.loc[df["Projekt"].duplicated(), "Projekt"].unique()
    if len(doppelt):
        fehler.append("Projekt mehrfach vorhanden: " + ", ".join(map(str, doppelt)))

    for spalte in ["Plan_Stunden", "Ist_Stunden"]:
        werte = pd.to_numeric(df[spalte], errors="coerce")
        leer = df.loc[werte.isna(), "Projekt"]
        if len(leer):
            fehler.append(f"{spalte} fehlt oder ist keine Zahl bei: " + ", ".join(map(str, leer)))
        negativ = df.loc[werte < 0, "Projekt"]
        if len(negativ):
            fehler.append(f"{spalte} ist negativ bei: " + ", ".join(map(str, negativ)))

    unbekannt = df.loc[~df["Status"].isin(ERLAUBTER_STATUS), "Projekt"]
    if len(unbekannt):
        fehler.append(
            "Unbekannter Status bei: " + ", ".join(map(str, unbekannt))
            + " (erlaubt: " + ", ".join(ERLAUBTER_STATUS) + ")"
        )

    monate = pd.to_datetime(df["Monat"], errors="coerce")
    if monate.isna().any():
        fehler.append("Monat fehlt oder ist kein Datum bei: " + ", ".join(map(str, df.loc[monate.isna(), "Projekt"])))
    elif monat_schluessel(monate).nunique() != 1:
        fehler.append("Eine Datei darf nur einen Monat enthalten. Gefunden: "
                      + ", ".join(sorted(monat_schluessel(monate).unique())))

    if fehler:
        raise Datenfehler("\n".join(fehler))


def berechnen(df):
    """Berechnet die Kennzahlen für eine Auswahl von Zeilen. Neue Kennzahlen werden hier ergänzt.

    Achtung: Ein Projekt steht in jedem Monat in einer eigenen Zeile. Kennzahlen über
    Projekte deshalb immer erst je Projekt zusammenfassen (siehe je_projekt).
    """
    plan = df["Plan_Stunden"].sum()
    ist = df["Ist_Stunden"].sum()
    return {
        "anzahl_projekte": df["Projekt"].nunique(),
        "plan_stunden": plan,
        "ist_stunden": ist,
        "abweichung": ist - plan,
        "ausschoepfung": ist / plan if plan else None,  # z. B. 0.96 = 96 % des Plans verbraucht
        "zeitraum": zeitraum(df["Monat"]),
    }


def je_projekt(df):
    """Fasst die Monate je Projekt zusammen: Stunden addiert, Status aus dem letzten Monat."""
    df = df.sort_values("Monat")
    return (df.groupby("Projekt")
              .agg(Bereich=("Bereich", "last"), Status=("Status", "last"),
                   Plan_Stunden=("Plan_Stunden", "sum"), Ist_Stunden=("Ist_Stunden", "sum"),
                   Monate=("Monat", "nunique"))
              .reset_index())


def veraenderung(jetzt, vorher):
    """Unterschied zweier Ergebnisse von berechnen(), z. B. September gegenüber August."""
    return {
        schluessel: wert - vorher[schluessel]
        for schluessel, wert in jetzt.items()
        if isinstance(wert, Number) and isinstance(vorher.get(schluessel), Number)
        and not isinstance(wert, bool)
    }


# ---------------------------------------------------------------------------
# Hilfsfunktionen für Monate und Zahlen
# ---------------------------------------------------------------------------

def monat_schluessel(werte):
    """Macht aus Datumswerten einheitliche Monatsangaben wie "2026-09"."""
    return pd.to_datetime(werte).dt.strftime("%Y-%m")


def monat_name(schluessel):
    """ "2026-09" -> "September 2026" """
    jahr, monat = schluessel.split("-")
    return f"{MONATSNAMEN[int(monat) - 1]} {jahr}"


def zeitraum(monate):
    """Beschreibt die enthaltenen Monate, z. B. "Juli bis September 2026"."""
    liste = sorted(set(monate))
    if not liste:
        return ""
    erster, letzter = monat_name(liste[0]), monat_name(liste[-1])
    if len(liste) == 1:
        return erster
    if liste[0][:4] == liste[-1][:4]:
        erster = erster.split(" ")[0]
    return f"{erster} bis {letzter}"


def zahl(wert, vorzeichen=False):
    """Formatiert eine Zahl deutsch, z. B. 1.250 oder +30."""
    text = f"{wert:+,.0f}" if vorzeichen and round(wert) != 0 else f"{wert:,.0f}"
    return text.replace(",", ".")
