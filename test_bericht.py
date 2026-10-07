"""Automatische Kontrolle: Rechnet das Programm richtig, und erkennt es fehlerhafte Daten?

Jeder Test nimmt eine kleine Beispieltabelle, deren Ergebnis wir von Hand kennen,
und vergleicht. Starten im Terminal:  python -m pytest
"""

import pandas as pd
import pytest

from bericht import Datenfehler, berechnen, je_projekt, laden, pruefen, veraenderung


def eine_datei():
    """So sieht EINE Monatsdatei aus: jedes Projekt genau einmal, ein Monat."""
    return pd.DataFrame({
        "Monat": [pd.Timestamp("2026-07-01")] * 3,
        "Projekt": ["A", "B", "C"],
        "Bereich": ["IT", "IT", "Personal"],
        "Status": ["laufend", "geplant", "abgeschlossen"],
        "Plan_Stunden": [10, 20, 30],
        "Ist_Stunden": [12, 0, 30],
    })


def beispiel():
    """Zwei Monate zusammen, so wie laden() sie liefert. Von Hand nachgerechnet:

    Juli:   A 10/12, B 20/0          August: A 10/18, C 40/30
    Plan 80 h, Ist 60 h, Abweichung -20 h, 3 verschiedene Projekte.
    Je Projekt: A 20/30 (über Plan), B 20/0, C 40/30.
    """
    return pd.DataFrame({
        "Monat": ["2026-07", "2026-07", "2026-08", "2026-08"],
        "Projekt": ["A", "B", "A", "C"],
        "Bereich": ["IT", "IT", "IT", "Personal"],
        "Status": ["laufend", "geplant", "abgeschlossen", "laufend"],
        "Plan_Stunden": [10, 20, 10, 40],
        "Ist_Stunden": [12, 0, 18, 30],
    })


# --- Rechnen --------------------------------------------------------------

def test_kennzahlen_stimmen():
    k = berechnen(beispiel())
    assert k["anzahl_projekte"] == 3  # A zählt nur einmal, obwohl es in zwei Monaten vorkommt
    assert k["plan_stunden"] == 80
    assert k["ist_stunden"] == 60
    assert k["abweichung"] == -20
    assert k["ausschoepfung"] == pytest.approx(0.75)  # 60 von 80 Stunden
    assert k["zeitraum"] == "Juli bis August 2026"


def test_projekte_ueber_plan():
    # Je Projekt über beide Monate: nur A liegt über Plan (30 > 20). Zeilenweise wären es 2.
    assert berechnen(beispiel())["projekte_ueber_plan"] == 1


def test_je_projekt_addiert_die_monate():
    p = je_projekt(beispiel()).set_index("Projekt")
    assert p.loc["A", "Plan_Stunden"] == 20
    assert p.loc["A", "Ist_Stunden"] == 30
    assert p.loc["A", "Status"] == "abgeschlossen"  # Status aus dem letzten Monat
    assert p.loc["A", "Monate"] == 2


def test_veraenderung_zum_vormonat():
    df = beispiel()
    august = berechnen(df[df["Monat"] == "2026-08"])
    juli = berechnen(df[df["Monat"] == "2026-07"])
    v = veraenderung(august, juli)
    assert v["ist_stunden"] == 36   # 48 h im August, 12 h im Juli
    assert v["plan_stunden"] == 20  # 50 h im August, 30 h im Juli
    assert "zeitraum" not in v      # Text wird nicht verglichen


# --- Prüfen einer Datei ---------------------------------------------------

def test_gueltige_datei_wird_akzeptiert():
    pruefen(eine_datei())  # darf keinen Fehler auslösen


def test_doppeltes_projekt_wird_gestoppt():
    df = eine_datei()
    df.loc[1, "Projekt"] = "A"
    with pytest.raises(Datenfehler, match="mehrfach"):
        pruefen(df)


def test_fehlende_stunden_werden_gestoppt():
    df = eine_datei()
    df.loc[0, "Ist_Stunden"] = None
    with pytest.raises(Datenfehler, match="Ist_Stunden fehlt"):
        pruefen(df)


def test_unbekannter_status_wird_gestoppt():
    df = eine_datei()
    df.loc[2, "Status"] = "fertig"
    with pytest.raises(Datenfehler, match="Unbekannter Status"):
        pruefen(df)


def test_zwei_monate_in_einer_datei_werden_gestoppt():
    df = eine_datei()
    df.loc[2, "Monat"] = pd.Timestamp("2026-08-01")
    with pytest.raises(Datenfehler, match="nur einen Monat"):
        pruefen(df)


# --- Laden mehrerer Dateien -------------------------------------------------

def test_laden_fuegt_monatsdateien_zusammen(tmp_path):
    juli = eine_datei()
    august = eine_datei().assign(Monat=pd.Timestamp("2026-08-01"))
    juli.to_excel(tmp_path / "2026-07.xlsx", index=False)
    august.to_excel(tmp_path / "2026-08.xlsx", index=False)
    df = laden(tmp_path)
    assert len(df) == 6
    assert sorted(df["Monat"].unique()) == ["2026-07", "2026-08"]


def test_gleicher_monat_in_zwei_dateien_wird_gestoppt(tmp_path):
    eine_datei().to_excel(tmp_path / "2026-07.xlsx", index=False)
    eine_datei().to_excel(tmp_path / "juli_kopie.xlsx", index=False)
    with pytest.raises(Datenfehler, match="mehreren Dateien"):
        laden(tmp_path)


def test_fehlermeldung_nennt_die_datei(tmp_path):
    kaputt = eine_datei()
    kaputt.loc[0, "Ist_Stunden"] = None
    kaputt.to_excel(tmp_path / "2026-07.xlsx", index=False)
    with pytest.raises(Datenfehler, match="2026-07.xlsx"):
        laden(tmp_path)
