---
description: Neue Folie in der automatisch erzeugten PowerPoint ergänzen
---

Ergänze in `praesentation.py` eine neue Folie: **${input:folie:Inhalt der Folie, z. B. Tabelle der Projekte über Plan}**.

So gehst du vor:
1. Verwende ausschließlich Werte aus `berechnen` in `bericht.py` bzw. aus der geprüften Tabelle. Rechne in `praesentation.py` keine eigenen Kennzahlen. Geht es um Projekte, verwende `je_projekt(df)`, damit jedes Projekt über alle Monate zusammengefasst ist.
2. Schreibe eine neue Funktion nach dem Muster der vorhandenen, z. B. `folie_bereiche`. Lege die Folie mit `rahmen.inhaltsfolie(titel, unterzeile, quelle)` an und verwende die vorhandenen Bausteine `tabelle`, `balkendiagramm`, `textfeld`, `beschriftung`, `erklaerspalte` und `notizen`. Keine eigenen Farben oder Schriften.
3. Formuliere den Titel als Aussage mit der Zahl, z. B. „3 Projekte liegen über Plan“.
4. Rufe die Funktion in `main` vor `folie_aussage` auf.
5. Führe `python -m pytest` und `python praesentation.py` aus.
6. Nenne mir die Zahlen auf der neuen Folie, damit ich sie mit dem Dashboard vergleichen kann.
