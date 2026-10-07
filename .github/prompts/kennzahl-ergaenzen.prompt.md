---
description: Neue Kennzahl ins Dashboard einbauen und prüfen
---

Ergänze die Kennzahl **${input:name:Name der Kennzahl, z. B. Über Plan}**.

Regel für die Berechnung: ${input:regel:z. B. Anzahl Projekte, bei denen die Ist_Stunden über alle Monate zusammen größer sind als die Plan_Stunden}

Erwarteter Wert für alle Monatsdateien, die jetzt in daten/ liegen (von mir nachgerechnet): ${input:sollwert:z. B. 2}

So gehst du vor:
1. Berechne die Kennzahl in `bericht.py` in der Funktion `berechnen`. Achtung: Jedes Projekt steht pro Monat in einer eigenen Zeile. Geht es um Projekte, fasse sie zuerst mit `je_projekt` zusammen.
2. Zeige sie im Dashboard als zusätzliche Kachel: in `dashboard.py` eine Zeile in der Liste `KARTEN` ergänzen. Filter und Vergleich zum Vormonat funktionieren dann automatisch mit.
3. Ergänze in `test_bericht.py` einen Test mit der Beispieltabelle `beispiel()` und einem von Hand nachgerechneten Ergebnis.
4. Führe `python -m pytest` und `python dashboard.py` aus.
5. Vergleiche den Wert im Dashboard mit meinem erwarteten Wert und sage mir klar, ob er übereinstimmt.
6. Erkläre kurz, was du in welcher Datei geändert hast.
