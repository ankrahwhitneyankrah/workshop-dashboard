# Workshop: Von der Excel zum Dashboard und zur PowerPoint

![Bericht erstellen](../../actions/workflows/bericht.yml/badge.svg)

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
| `dashboard.py` | Baut daraus das Dashboard und legt fest, welche Kennzahlen als Kacheln erscheinen (`KARTEN`). |
| `dashboard_vorlage.html` | Aussehen und Bedienung des Dashboards: Filter, Diagramme, Tabelle. Funktioniert ohne Internet. |
| `praesentation.py` | Baut aus denselben Zahlen die PowerPoint: Kennzahlen, Diagramme, Tabelle, Platz für eure Einordnung und eine Folie zur Datengrundlage. Alles bleibt bearbeitbar. |
| `vorlage/` | Optional, nur auf eurem Rechner: eure Firmenvorlage als `.pptx`. Wird nie hochgeladen. |
| `test_bericht.py` | Automatische Kontrolle: Rechnet das Programm richtig? Erkennt es fehlerhafte Daten? |
| `.github/workflows/bericht.yml` | Das „Rezept“ für GitHub: Bei jeder Änderung wird alles automatisch geprüft und neu gebaut. |
| `.github/copilot-instructions.md` | Regeln, an die sich Copilot in diesem Projekt immer hält. |
| `.github/prompts/` | Fertige Arbeitsaufträge für Copilot (im Chat mit `/` aufrufen). |
| `beispieldaten/` | Weitere Datenstände für die Übungen, darunter einer mit absichtlichen Fehlern. |

## Start (einmalig)

> **Tipp:** Fast alles in VS Code erreicht ihr über die **Befehlspalette** `Strg + Shift + P` und den Namen des Befehls. Das funktioniert unabhängig davon, wie VS Code bei euch aussieht.

0. Auf GitHub im Vorlage-Repository **Use this template → Create a new repository** wählen:
   - Sichtbarkeit **Private**
   - Häkchen bei **Include all branches** setzen (sonst fehlt die Musterlösung)
1. In VS Code `Strg + Shift + P` → `Git: Clone` → euer neues Repository wählen. Als Speicherort einen Ordner **außerhalb von OneDrive** wählen, z. B. `C:\Users\<Kürzel>\Projekte`. OneDrive sperrt beim Synchronisieren Dateien, und Git kann dann nicht schreiben.
2. Beim ersten Mal im Terminal Namen und **anonyme** GitHub-E-Mail hinterlegen. Ihr findet sie auf GitHub unter Settings → Emails → „Keep my email addresses private“. Sie sieht aus wie `12345678+name@users.noreply.github.com`.
   `git config --global user.name "Vorname Nachname"`
   `git config --global user.email "12345678+name@users.noreply.github.com"`
3. `Strg + Shift + P` → `Python: Select Interpreter` → das normale Python wählen (z. B. `Python 3.13`, **nicht** eine `.venv` aus einem anderen Projekt).
4. **Terminal → Aufgabe ausführen → „Pakete installieren (einmalig)“**.
5. **Terminal → Aufgabe ausführen → „2 · Alles prüfen (Tests)“**. Erwartung: alles grün, `passed`.

## Stufe 1: Ein Dashboard bauen

1. Im Copilot-Chat `/projekt-erklaeren` eingeben und die Erklärung lesen.
2. **Terminal → Aufgabe ausführen → „1 · Dashboard erstellen“**. Das Dashboard öffnet sich im Browser.
   **Sollwert:** 8 Projekte · 670 h Plan · 620 h Ist · −50 h Abweichung · 93 % Ausschöpfung
   Ausprobieren: Filter nach Bereich und Status, auf einen Bereich im rechten Diagramm klicken, mit der Maus über die Balken fahren, Tabelle sortieren.
   **Kontrolle:** Bereich „Finanzen“ → 2 Projekte · 130 h Plan · 150 h Ist · 115 %
3. Eigenen Branch anlegen: `Strg + Shift + P` → `Git: Create Branch` → `uebung-kennzahl`.
4. Im Copilot-Chat den Modus **Agent** wählen und `/kennzahl-ergaenzen` eingeben. Copilot fragt drei Angaben nacheinander ab:
   - Name: *Über Plan*
   - Regel: *Anzahl Projekte, bei denen Ist_Stunden größer als Plan_Stunden ist*
   - Sollwert: **2**

   Wenn Copilot nach Erlaubnis fragt (Dateien ändern, Tests ausführen), bestätigen. Bietet Copilot am Ende an, die Kennzahl auch in die Präsentation einzubauen: **Nein**, das kommt in Stufe 3.
5. Prüfen: neue Kachel „Über Plan“ = **2**, auch gefiltert nach „Finanzen“ = **2**. Erst dann im Chat **Keep** klicken (bei falschem Ergebnis **Undo**).
6. In der **Quellcodeverwaltung** (linke Leiste) ansehen, was geändert wurde, eine verständliche Nachricht eintragen und **Commit** klicken.

   Jede Person bekommt von Copilot eine etwas andere Lösung. Das ist in Ordnung, entscheidend ist der Sollwert.

## Stufe 2: Automatisch aktualisieren

1. **Branch veröffentlichen** bzw. **Synchronisieren**: Die Änderungen gehen zu GitHub. Optional als Pull Request: auf GitHub **Compare & pull request**, Prüfung abwarten, dann **Merge** oder in der Übung **Close pull request**.
2. Auf GitHub den Tab **Actions** öffnen und zusehen, wie der Bericht gebaut wird. Danach unter **Artifacts** „bericht“ herunterladen.
3. Neuer Datenstand: Auf GitHub den Ordner `daten` öffnen, **Add file → Upload files** wählen und die Datei `beispieldaten/stand_2_september/projekte.xlsx` von eurem Rechner hineinziehen. Sie ersetzt die alte Datei. **Commit changes** klicken. Ein neuer Lauf startet von selbst.
   **Sollwert:** 9 Projekte · 700 h Plan · 670 h Ist · −30 h Abweichung · 96 % Ausschöpfung · 4 Projekte über Plan
4. Fehlerfall: Dasselbe mit `beispieldaten/stand_fehlerhaft/projekte.xlsx`. Der Lauf wird **rot**, es entsteht kein neuer Bericht. Die Fehlermeldung nennt die doppelte „Schichtplanung“ und die fehlenden Stunden bei „Wissensdatenbank“.
5. In VS Code **Pull** (bzw. Synchronisieren) ausführen, damit euer Rechner den neuesten Stand von GitHub hat.

## Stufe 3: Daraus eine PowerPoint machen

1. **Terminal → Aufgabe ausführen → „3 · Präsentation erstellen“** und `ausgabe/praesentation.pptx` öffnen.
   Mit eigener Firmenvorlage: Ordner `vorlage` anlegen, die Vorlage als `.pptx` hineinlegen und erneut erstellen. Schrift, Farben, Fußzeile und Titelbild kommen dann aus der Vorlage. Der Ordner wird nie zu GitHub hochgeladen, die Version aus GitHub Actions ist deshalb immer im neutralen Design.
2. Im Copilot-Chat `/folie-ergaenzen` eingeben: *Tabelle der Projekte über Plan*. Ergebnis prüfen, dann **Keep**.
3. In `.github/workflows/bericht.yml` den Schritt „Präsentation erstellen“ einkommentieren (oder Copilot darum bitten).
4. Committen und pushen. GitHub liefert jetzt Dashboard **und** PowerPoint.
5. Zahlen auf den Folien mit dem Dashboard vergleichen. Die Aussage auf der Folie „Einordnung und nächste Schritte“ formuliert ihr selbst.
   **Sollwert** (Datenstand 15.09.2026 aus Stufe 2): **4 Projekte liegen über Plan**: Rechnungsprüfung +20 h, Kundenportal, Schichtplanung und Reisekosten je +5 h.

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
