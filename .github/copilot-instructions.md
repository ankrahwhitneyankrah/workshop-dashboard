# Projektregeln für Copilot

Diese Regeln gelten automatisch für jede Anfrage in diesem Projekt.

## Über das Projekt
- Aus `daten/projekte.xlsx` entstehen automatisch ein Dashboard (`dashboard.py`) und eine PowerPoint (`praesentation.py`).
- Alle Kennzahlen werden ausschließlich in `bericht.py` in der Funktion `berechnen` ermittelt. Dashboard und PowerPoint rechnen nicht selbst, sondern verwenden nur diese Werte.
- Die Prüfung der Excel-Datei steht in `bericht.py` in der Funktion `pruefen`.
- Welche Kennzahlen als Kacheln im Dashboard erscheinen, steht in `dashboard.py` in der Liste `KARTEN`.
- Aussehen und Bedienung des Dashboards (Filter, Diagramme, Tabelle) stehen in `dashboard_vorlage.html`. Dort keine Kennzahlen berechnen.

## Regeln
- Antworte auf Deutsch und in einfachen Worten. Die Nutzenden sind keine Entwickler.
- Verändere niemals Dateien in `daten/` oder `beispieldaten/`.
- Installiere keine neuen Pakete und ergänze `requirements.txt` nur nach ausdrücklicher Rückfrage.
- Ergänze für jede neue Kennzahl einen Test in `test_bericht.py` mit einer kleinen Beispieltabelle, deren Ergebnis von Hand nachgerechnet ist.
- Führe nach jeder Änderung `python -m pytest` und `python dashboard.py` aus und nenne das Ergebnis.
- Behaupte nur, dass etwas funktioniert, wenn du es tatsächlich ausgeführt hast.
- Erkläre am Ende kurz, welche Dateien du geändert hast und warum.
- Verwende ausschließlich synthetische Daten, keine echten Unternehmens- oder Personendaten.
