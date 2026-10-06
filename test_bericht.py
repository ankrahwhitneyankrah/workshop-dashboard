"""Automatische Kontrolle: Rechnet das Programm richtig, und erkennt es fehlerhafte Daten?

Jeder Test nimmt eine kleine Beispieltabelle, deren Ergebnis wir von Hand kennen,
und vergleicht. Starten im Terminal:  python -m pytest
"""

import pandas as pd
import pytest

from bericht import Datenfehler, berechnen, pruefen


def beispiel():
    """Drei Projekte, von Hand nachgerechnet: Plan 60 h, Ist 42 h, Abweichung -18 h."""
    return pd.DataFrame({
        "Projekt": ["A", "B", "C"],
        "Bereich": ["IT", "IT", "Personal"],
        "Status": ["laufend", "geplant", "abgeschlossen"],
        "Plan_Stunden": [10, 20, 30],
        "Ist_Stunden": [12, 0, 30],
        "Datenstand": [pd.Timestamp("2026-09-01")] * 3,
    })


def test_kennzahlen_stimmen():
    k = berechnen(beispiel())
    assert k["anzahl_projekte"] == 3
    assert k["plan_stunden"] == 60
    assert k["ist_stunden"] == 42
    assert k["abweichung"] == -18
    assert k["ueber_plan"] == 1
    assert k["ausschoepfung"] == pytest.approx(0.7)  # 42 von 60 Stunden
    assert k["datenstand"] == "01.09.2026"


def test_ueber_plan_wird_richtig_gezaehlt():
    """Vier Projekte, von Hand nachgerechnet: 2 Projekte sind über Plan."""
    df = pd.DataFrame({
        "Projekt": ["A", "B", "C", "D"],
        "Bereich": ["IT", "IT", "Personal", "Einkauf"],
        "Status": ["laufend", "geplant", "abgeschlossen", "laufend"],
        "Plan_Stunden": [10, 20, 30, 5],
        "Ist_Stunden": [12, 20, 31, 4],
        "Datenstand": [pd.Timestamp("2026-09-01")] * 4,
    })

    k = berechnen(df)
    assert k["ueber_plan"] == 2


def test_gueltige_daten_werden_akzeptiert():
    pruefen(beispiel())  # darf keinen Fehler auslösen


def test_doppeltes_projekt_wird_gestoppt():
    df = beispiel()
    df.loc[1, "Projekt"] = "A"
    with pytest.raises(Datenfehler, match="mehrfach"):
        pruefen(df)


def test_fehlende_stunden_werden_gestoppt():
    df = beispiel()
    df.loc[0, "Ist_Stunden"] = None
    with pytest.raises(Datenfehler, match="Ist_Stunden fehlt"):
        pruefen(df)


def test_unbekannter_status_wird_gestoppt():
    df = beispiel()
    df.loc[2, "Status"] = "fertig"
    with pytest.raises(Datenfehler, match="Unbekannter Status"):
        pruefen(df)
