"""Das Herzstück: Excel laden, prüfen und Kennzahlen berechnen.

dashboard.py und praesentation.py verwenden beide diese Datei.
So zeigen Dashboard und PowerPoint garantiert dieselben Zahlen.
"""

from pathlib import Path

import pandas as pd

DATEI = Path(__file__).parent / "daten" / "projekte.xlsx"
PFLICHTSPALTEN = ["Projekt", "Bereich", "Status", "Plan_Stunden", "Ist_Stunden", "Datenstand"]
ERLAUBTER_STATUS = ["geplant", "laufend", "abgeschlossen"]


class Datenfehler(Exception):
    """Die Excel-Datei ist fehlerhaft. Dann wird nichts erzeugt."""


def laden(datei=DATEI):
    """Liest die Excel-Datei und prüft sie, bevor irgendetwas berechnet wird."""
    df = pd.read_excel(datei, sheet_name="Projekte")
    pruefen(df)
    return df


def pruefen(df):
    """Sammelt alle Fehler in der Tabelle und stoppt, falls es welche gibt."""
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

    if df["Datenstand"].nunique() != 1:
        fehler.append("Der Datenstand muss in allen Zeilen gleich sein.")

    if fehler:
        raise Datenfehler("\n".join(fehler))


def berechnen(df):
    """Berechnet die Kennzahlen. Neue Kennzahlen werden hier ergänzt."""
    plan = df["Plan_Stunden"].sum()
    ist = df["Ist_Stunden"].sum()
    return {
        "anzahl_projekte": len(df),
        "plan_stunden": plan,
        "ist_stunden": ist,
        "abweichung": ist - plan,
        "ausschoepfung": ist / plan if plan else None,  # z. B. 0.93 = 93 % des Plans verbraucht
        "datenstand": pd.to_datetime(df["Datenstand"].iloc[0]).strftime("%d.%m.%Y"),
    }


def zahl(wert, vorzeichen=False):
    """Formatiert eine Zahl deutsch, z. B. 1.250 oder +30."""
    text = f"{wert:+,.0f}" if vorzeichen else f"{wert:,.0f}"
    return text.replace(",", ".")
