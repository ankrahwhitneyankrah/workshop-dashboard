# Workshop: Von der Excel zum Dashboard und zur PowerPoint

Aus einer Excel-Datei entstehen in drei Stufen ein Dashboard, eine automatische Aktualisierung und eine PowerPoint. Alle Daten sind erfunden.

```
daten/projekte.xlsx ──► bericht.py (prüfen + rechnen) ──► dashboard.py      ──► ausgabe/dashboard.html
                                                     └──► praesentation.py ──► ausgabe/praesentation.pptx
```

## Was ist wofür da?

| Datei | Aufgabe |
|---|---|
| `daten/projekte.xlsx` | Die Daten. Wird eine neue Datei mit gleichem Namen hochgeladen, entsteht ein neuer Bericht. |
| `bericht.py` | Das Herzstück: Excel laden, auf Fehler prüfen, Kennzahlen berechnen. |
| `dashboard.py` | Baut daraus das Dashboard (eine HTML-Datei, funktioniert ohne Internet). |
| `praesentation.py` | Baut aus denselben Zahlen die PowerPoint. |
| `test_bericht.py` | Automatische Kontrolle: Rechnet das Programm richtig? Erkennt es fehlerhafte Daten? |
| `.github/workflows/bericht.yml` | Das „Rezept“ für GitHub: Bei jeder Änderung wird alles automatisch geprüft und neu gebaut. |
| `.github/copilot-instructions.md` | Regeln, an die sich Copilot in diesem Projekt immer hält. |
| `.github/prompts/` | Fertige Arbeitsaufträge für Copilot (im Chat mit `/` aufrufen). |
| `beispieldaten/` | Weitere Datenstände für die Übungen, darunter einer mit absichtlichen Fehlern. |

## Start (einmalig)

1. Diesen Ordner in VS Code öffnen (**Datei → Ordner öffnen**).
2. **Terminal → Aufgabe ausführen → „Pakete installieren (einmalig)“**.
3. **Terminal → Aufgabe ausführen → „2 · Alles prüfen (Tests)“**. Erwartung: alles grün, `passed`.

## Stufe 1: Ein Dashboard bauen

1. Im Copilot-Chat `/projekt-erklaeren` eingeben und die Erklärung lesen.
2. **Terminal → Aufgabe ausführen → „1 · Dashboard erstellen“**. Das Dashboard öffnet sich im Browser.
   **Sollwert:** 8 Projekte · 670 h Plan · 620 h Ist · −50 h Abweichung
3. Im Copilot-Chat (Agent-Modus) `/kennzahl-ergaenzen` eingeben:
   - Name: *Projekte über Plan*
   - Regel: *Anzahl Projekte mit Ist_Stunden größer als Plan_Stunden*
   - Sollwert: **2**
4. In der Ansicht **Quellcodeverwaltung** (linke Leiste) prüfen, was Copilot geändert hat. Stimmt der Wert im Dashboard?
5. Änderung mit einer verständlichen Nachricht **committen**.

## Stufe 2: Automatisch aktualisieren

1. **Synchronisieren** bzw. **Push**: Die Änderungen gehen zu GitHub.
2. Auf GitHub den Tab **Actions** öffnen und zusehen, wie der Bericht gebaut wird. Danach unter **Artifacts** „bericht“ herunterladen.
3. Neuer Datenstand: Auf GitHub den Ordner `daten` öffnen, **Add file → Upload files** wählen und die Datei `beispieldaten/stand_2_september/projekte.xlsx` von eurem Rechner hineinziehen. Sie ersetzt die alte Datei. **Commit changes** klicken. Ein neuer Lauf startet von selbst.
   **Sollwert:** 9 Projekte · 700 h Plan · 670 h Ist · −30 h Abweichung · 4 Projekte über Plan
4. Fehlerfall: Dasselbe mit `beispieldaten/stand_fehlerhaft/projekte.xlsx`. Der Lauf wird **rot**, es entsteht kein neuer Bericht. Die Fehlermeldung nennt die doppelte „Schichtplanung“ und die fehlenden Stunden bei „Wissensdatenbank“.
5. In VS Code **Pull** (bzw. Synchronisieren) ausführen, damit euer Rechner den neuesten Stand von GitHub hat.

## Stufe 3: Daraus eine PowerPoint machen

1. **Terminal → Aufgabe ausführen → „3 · Präsentation erstellen“** und `ausgabe/praesentation.pptx` öffnen.
2. Im Copilot-Chat `/folie-ergaenzen` eingeben: *Tabelle der Projekte über Plan*.
3. In `.github/workflows/bericht.yml` den Schritt „Präsentation erstellen“ einkommentieren (oder Copilot darum bitten).
4. Committen und pushen. GitHub liefert jetzt Dashboard **und** PowerPoint.
5. Zahlen auf den Folien mit dem Dashboard vergleichen. Die Aussage auf der letzten Folie formuliert ihr selbst.

## Auf eigene Daten übertragen

- [ ] Eigene Excel-Tabelle mit einer Kopfzeile, eine Zeile pro Eintrag, keine verbundenen Zellen.
- [ ] Spaltennamen in `PFLICHTSPALTEN` in `bericht.py` anpassen (Copilot fragen: „Passe das Projekt an meine Spalten an: …“).
- [ ] Für 3 bis 5 Zeilen die wichtigste Kennzahl von Hand ausrechnen. Das ist euer Sollwert.
- [ ] Kennzahl mit `/kennzahl-ergaenzen` einbauen und gegen den Sollwert prüfen.
- [ ] Keine echten vertraulichen Daten in ein nicht freigegebenes Repository laden.

## Wer macht was?

| Werkzeug | Aufgabe |
|---|---|
| **VS Code** | Dateien bearbeiten, Programme im Terminal ausführen |
| **GitHub Copilot** | Erklärt, schlägt vor, setzt Änderungen um, nach euren Regeln |
| **Git** | Speichert jeden Stand mit Beschreibung, alles nachvollziehbar und umkehrbar |
| **GitHub** | Gemeinsamer Ablageort, Änderungsvorschläge (Pull Requests) prüfen |
| **GitHub Actions** | Führt Prüfung und Berichtserstellung automatisch aus |
