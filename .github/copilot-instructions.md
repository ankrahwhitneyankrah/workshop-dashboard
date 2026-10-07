# Projektregeln für Copilot

Diese Regeln gelten automatisch für jede Anfrage in diesem Projekt.

## Über das Projekt
- Im Ordner `daten/` liegt **eine Excel-Datei pro Monat** (z. B. `2026-07.xlsx`). Jede neue Datei kommt dazu. Aus allen Dateien zusammen entstehen automatisch ein Dashboard (`dashboard.py`) und eine PowerPoint (`praesentation.py`).
- Eine Zeile = ein Projekt in einem Monat. `Plan_Stunden` und `Ist_Stunden` sind die Stunden **dieses Monats**. Ein Projekt steht deshalb in mehreren Zeilen.
- Kennzahlen über Projekte (z. B. „Anzahl Projekte über Plan“) **immer erst je Projekt zusammenfassen**, dafür gibt es `je_projekt` in `bericht.py`. Zeilen zu zählen wäre falsch.
- Alle Kennzahlen werden ausschließlich in `bericht.py` in der Funktion `berechnen` ermittelt. Dashboard und PowerPoint rechnen nicht selbst, sondern verwenden nur diese Werte.
- Die Prüfung einer Monatsdatei steht in `bericht.py` in der Funktion `pruefen`, das Zusammenführen aller Dateien in `laden`.
- Welche Kennzahlen als Kacheln im Dashboard erscheinen, steht in `dashboard.py` in der Liste `KARTEN`. Neue Kennzahlen erscheinen dann automatisch mit Monatsfilter und Veränderung zum Vormonat.
- Aussehen und Bedienung des Dashboards (Filter, Diagramme, Tabelle) stehen in `dashboard_vorlage.html`. Dort keine Kennzahlen berechnen.
- `praesentation.py` baut Folien aus fertigen Bausteinen (`rahmen.inhaltsfolie`, `tabelle`, `balkendiagramm`, `textfeld`, `beschriftung`, `erklaerspalte`, `notizen`). Neue Folien verwenden diese Bausteine und keine eigenen Farben oder Schriften.
- Liegt im Ordner `vorlage/` eine Firmenvorlage, nutzt die Präsentation deren Master. Diesen Ordner nie verändern und nie zu Git hinzufügen.

## Regeln
- Antworte auf Deutsch und in einfachen Worten. Die Nutzenden sind keine Entwickler.
- Verändere niemals Dateien in `daten/` oder `beispieldaten/`.
- Installiere keine neuen Pakete und ergänze `requirements.txt` nur nach ausdrücklicher Rückfrage.
- Ergänze für jede neue Kennzahl einen Test in `test_bericht.py` mit der kleinen Beispieltabelle `beispiel()`, deren Ergebnis von Hand nachgerechnet ist.
- Führe nach jeder Änderung `python -m pytest` und `python dashboard.py` aus und nenne das Ergebnis.
- Behaupte nur, dass etwas funktioniert, wenn du es tatsächlich ausgeführt hast.
- Erkläre am Ende kurz, welche Dateien du geändert hast und warum.
- Verwende ausschließlich synthetische Daten, keine echten Unternehmens- oder Personendaten.
