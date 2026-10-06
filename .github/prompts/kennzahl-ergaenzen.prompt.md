---
description: Neue Kennzahl ins Dashboard einbauen und prüfen
---

Ergänze die Kennzahl **${input:name:Name der Kennzahl, z. B. Projekte über Plan}**.

Regel für die Berechnung: ${input:regel:z. B. Anzahl Projekte mit Ist_Stunden größer als Plan_Stunden}

Erwarteter Wert für die aktuelle Datei daten/projekte.xlsx (von mir nachgerechnet): ${input:sollwert:z. B. 2}

So gehst du vor:
1. Berechne die Kennzahl in `bericht.py` in der Funktion `berechnen`.
2. Zeige sie im Dashboard als zusätzliche Kachel: in `dashboard.py` eine Zeile in der Liste `KARTEN` ergänzen. Die Filter funktionieren dann automatisch mit.
3. Ergänze in `test_bericht.py` einen Test mit der kleinen Beispieltabelle und einem von Hand nachgerechneten Ergebnis.
4. Führe `python -m pytest` und `python dashboard.py` aus.
5. Vergleiche den Wert im Dashboard mit meinem erwarteten Wert und sage mir klar, ob er übereinstimmt.
6. Erkläre kurz, was du in welcher Datei geändert hast.
