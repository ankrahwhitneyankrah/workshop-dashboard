---
description: Neue Folie in der automatisch erzeugten PowerPoint ergänzen
---

Ergänze in `praesentation.py` eine neue Folie: **${input:folie:Inhalt der Folie, z. B. Tabelle der Projekte über Plan}**.

So gehst du vor:
1. Verwende ausschließlich Werte aus `berechnen` in `bericht.py` bzw. aus der geprüften Tabelle. Rechne in `praesentation.py` keine eigenen Kennzahlen.
2. Halte dich an die Gestaltung der vorhandenen Folien: gleiche Überschrift, gleiche Farben, Datenstand in der Fußzeile.
3. Füge die Folie vor der Folie „Aussage und nächste Schritte“ ein.
4. Führe `python -m pytest` und `python praesentation.py` aus.
5. Nenne mir die Zahlen auf der neuen Folie, damit ich sie mit dem Dashboard vergleichen kann.
