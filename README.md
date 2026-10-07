# Workshop: Von der Excel zum Dashboard und zur PowerPoint

![Bericht erstellen](../../actions/workflows/bericht.yml/badge.svg)

Jeden Monat kommt eine neue Excel-Datei dazu. In drei Stufen entsteht daraus ein Dashboard, das sich bei jeder neuen Datei von selbst erweitert, und eine PowerPoint. Alle Daten sind erfunden.

```
daten/2026-07.xlsx ┐
daten/2026-08.xlsx ├─► bericht.py (prüfen + zusammenführen + rechnen) ─┬─► dashboard.py      ─► ausgabe/dashboard.html
daten/2026-09.xlsx ┘                                                    └─► praesentation.py ─► ausgabe/praesentation.pptx
   (neue Monate kommen einfach dazu)
```

## Was ist wofür da?

| Datei | Aufgabe |
|---|---|
| `daten/` | Eine Excel-Datei pro Monat. Eine neue Datei kommt dazu, eine Datei mit gleichem Namen ersetzt die alte. |
| `bericht.py` | Das Herzstück: alle Monatsdateien laden, jede einzeln prüfen, zusammenführen, Kennzahlen berechnen. |
| `dashboard.py` | Baut daraus das Dashboard und legt fest, welche Kennzahlen als Kacheln erscheinen (`KARTEN`). |
| `dashboard_vorlage.html` | Aussehen und Bedienung des Dashboards: Filter, Monatsverlauf, Diagramme, Tabelle. Funktioniert ohne Internet. |
| `praesentation.py` | Baut aus denselben Zahlen die PowerPoint: Überblick, Entwicklung je Monat, Projekte, Platz für eure Einordnung. Alles bleibt bearbeitbar. |
| `vorlage/` | Optional, nur auf eurem Rechner: eure Firmenvorlage als `.pptx`. Wird nie hochgeladen. |
| `test_bericht.py` | Automatische Kontrolle: Rechnet das Programm richtig? Erkennt es fehlerhafte Daten? |
| `.github/workflows/bericht.yml` | Das „Rezept“ für GitHub: Bei jeder Änderung wird alles automatisch geprüft und neu gebaut. |
| `.github/copilot-instructions.md` | Regeln, an die sich Copilot in diesem Projekt immer hält. |
| `.github/prompts/` | Fertige Arbeitsaufträge für Copilot (im Chat mit `/` aufrufen). |
| `beispieldaten/` | Der nächste Monat für Stufe 2: einmal mit absichtlichen Fehlern, einmal korrekt. |

### So sieht eine Monatsdatei aus

| Monat | Projekt | Bereich | Status | Plan_Stunden | Ist_Stunden |
|---|---|---|---|---:|---:|
| 01.07.2026 | Kundenportal | Vertrieb | laufend | 40 | 35 |
| 01.07.2026 | Onboarding | Personal | laufend | 20 | 20 |

- Eine Zeile pro Projekt. Plan- und Ist-Stunden gelten **nur für diesen Monat**.
- Der Dateiname ist frei, empfohlen ist `JJJJ-MM.xlsx`. Entscheidend ist die Spalte `Monat`.
- Jede Datei wird einzeln geprüft. Ist eine fehlerhaft, entsteht **kein** neuer Bericht, und die Meldung nennt die Datei.

## Start (einmalig)

> **Tipp:** Fast alles in VS Code erreicht ihr über die **Befehlspalette** `Strg + Shift + P` und den Namen des Befehls. Das funktioniert unabhängig davon, wie VS Code bei euch aussieht.

0. Auf GitHub im Vorlage-Repository **Use this template → Create a new repository** wählen:
   - Sichtbarkeit **Private**
   - Häkchen bei **Include all branches** setzen (sonst fehlt die Musterlösung)

   Danach zeigt GitHub gelbe Hinweise „Compare & pull request“. **Diese bitte ignorieren.**
1. In VS Code `Strg + Shift + P` → `Git: Clone` → euer neues Repository wählen. Als Speicherort einen Ordner **außerhalb von OneDrive** wählen, z. B. `C:\Users\<Kürzel>\Projekte`. Am schnellsten findet ihr euren Benutzerordner, wenn ihr im Datei-Explorer `%USERPROFILE%` in die Adresszeile tippt und Enter drückt. OneDrive sperrt beim Synchronisieren Dateien, und Git kann dann nicht schreiben.
2. Beim ersten Mal im Terminal Namen und **anonyme** GitHub-E-Mail hinterlegen. Ihr findet sie auf GitHub unter Settings → Emails → „Keep my email addresses private“. Sie sieht aus wie `12345678+name@users.noreply.github.com`.
   `git config --global user.name "Vorname Nachname"`
   `git config --global user.email "12345678+name@users.noreply.github.com"`
3. `Strg + Shift + P` → `Python: Select Interpreter` → das normale Python wählen (z. B. `Python 3.13`, **nicht** eine `.venv` aus einem anderen Projekt).
4. **Terminal → Aufgabe ausführen → „Pakete installieren (einmalig)“**.
5. **Terminal → Aufgabe ausführen → „2 · Alles prüfen (Tests)“**. Erwartung: alles grün, `11 passed`.

## Stufe 1: Ein Dashboard bauen

Im Ordner `daten/` liegen schon zwei Monate: Juli und August.

1. Im Copilot-Chat `/projekt-erklaeren` eingeben und die Erklärung lesen.
2. **Terminal → Aufgabe ausführen → „1 · Dashboard erstellen“**. Das Dashboard öffnet sich im Browser.
   **Sollwert:** 8 Projekte · 420 h Plan · 405 h Ist · −15 h Abweichung · 96 % Ausschöpfung
   Ausprobieren: Monat „August 2026“ wählen. Unter den Kacheln steht jetzt die Veränderung zum Juli, z. B. **▲ +25 h ggü. Juli 2026**. Auf eine Säule im Monatsverlauf oder einen Bereich klicken, mit der Maus über die Balken fahren, Tabelle sortieren.
   **Kontrolle:** Bereich „Finanzen“, alle Monate → 2 Projekte · 100 h Plan · 115 h Ist · 115 %
3. Eigenen Branch anlegen: `Strg + Shift + P` → `Git: Create Branch` → `uebung-kennzahl`.
4. Im Copilot-Chat den Modus **Agent** wählen und `/kennzahl-ergaenzen` eingeben. Copilot fragt drei Angaben nacheinander ab:
   - Name: *Über Plan*
   - Regel: *Anzahl Projekte, bei denen die Ist_Stunden über alle Monate zusammen größer sind als die Plan_Stunden*
   - Sollwert: **2**

   Wenn Copilot nach Erlaubnis fragt (Dateien ändern, Tests ausführen), bestätigen. Bietet Copilot am Ende an, die Kennzahl auch in die Präsentation einzubauen: **Nein**, das kommt in Stufe 3.
5. Prüfen: neue Kachel „Über Plan“ = **2** (Rechnungsprüfung und Reisekosten), auch gefiltert nach „Finanzen“ = **2**. Erst dann im Chat **Keep** klicken (bei falschem Ergebnis **Undo**).
   Zeigt die Kachel **4**? Dann hat Copilot Zeilen gezählt statt Projekte: Jedes Projekt steht pro Monat in einer eigenen Zeile. Im Chat schreiben: „Fasse zuerst je Projekt zusammen, nutze je_projekt.“
6. In der **Quellcodeverwaltung** (linke Leiste) ansehen, was geändert wurde, eine verständliche Nachricht eintragen und **Commit** klicken.

   Jede Person bekommt von Copilot eine etwas andere Lösung. Das ist in Ordnung, entscheidend ist der Sollwert.

## Stufe 2: Ein neuer Monat kommt dazu, automatisch

1. **Branch veröffentlichen**. Auf GitHub erscheint **Compare & pull request** für `uebung-kennzahl` → **Create pull request**. Prüfung abwarten („All checks have passed“), dann **Merge pull request** → **Confirm merge**.
2. Auf GitHub den Tab **Actions** öffnen und zusehen, wie der Bericht für `main` gebaut wird. Danach unter **Artifacts** „bericht“ herunterladen.
3. **Der September-Export kommt, leider mit Fehlern:** Auf GitHub den Ordner `daten` öffnen, **Add file → Upload files** wählen und `beispieldaten/mit_fehlern/2026-09.xlsx` von eurem Rechner hineinziehen. **Commit changes** klicken.
   **Sollwert:** Der Lauf wird **rot**, es entsteht kein neuer Bericht. Die Fehlermeldung nennt die Datei `2026-09.xlsx`, die doppelte „Schichtplanung“ und die fehlenden Stunden bei „Wissensdatenbank“. Juli und August bleiben unverändert.
4. **Korrigierte Datei hochladen:** Genauso `beispieldaten/2026-09.xlsx` hochladen. Sie heißt gleich und **ersetzt** die fehlerhafte Datei. Ein neuer Lauf startet von selbst und wird grün.
   **Sollwert** (Juli bis September): 9 Projekte · 630 h Plan · 600 h Ist · −30 h Abweichung · 95 % Ausschöpfung · Über Plan **3**
   Im Dashboard hat der Monatsverlauf jetzt **drei Säulen**. September gewählt: **▼ −20 h ggü. August 2026**.
5. In VS Code `Strg + Shift + P` → `Git: Checkout to…` → **main**, dann **Synchronisieren**, damit euer Rechner den neuesten Stand von GitHub hat.

## Stufe 3: Daraus eine PowerPoint machen

1. **Terminal → Aufgabe ausführen → „3 · Präsentation erstellen“** und `ausgabe/praesentation.pptx` öffnen.
   Mit eigener Firmenvorlage: Ordner `vorlage` anlegen, die Vorlage als `.pptx` hineinlegen und erneut erstellen. Schrift, Farben, Fußzeile und Titelbild kommen dann aus der Vorlage. Der Ordner wird nie zu GitHub hochgeladen, die Version aus GitHub Actions ist deshalb immer im neutralen Design.
2. Im Copilot-Chat (Agent) `/folie-ergaenzen` eingeben: *Tabelle der Projekte über Plan*. Ergebnis prüfen, dann **Keep**.
   **Sollwert:** **3 Projekte liegen über Plan**: Kundenportal +15 h, Rechnungsprüfung +10 h, Reisekosten +5 h.
3. In `.github/workflows/bericht.yml` den Schritt „Präsentation erstellen“ einkommentieren (oder Copilot darum bitten).
4. Committen und synchronisieren. GitHub liefert jetzt Dashboard **und** PowerPoint.
5. Zahlen auf den Folien mit dem Dashboard vergleichen. Die Aussage auf der Folie „Einordnung und nächste Schritte“ formuliert ihr selbst.

## Auf eigene Daten übertragen

- [ ] Eigene Excel-Tabellen: eine Datei pro Zeitraum (Monat, Woche …), eine Kopfzeile, eine Zeile pro Eintrag, keine verbundenen Zellen.
- [ ] Spaltennamen in `PFLICHTSPALTEN` in `bericht.py` anpassen (Copilot fragen: „Passe das Projekt an meine Spalten an: …“).
- [ ] Klären: Enthält jede Datei nur den neuen Zeitraum (wie hier) oder jeweils den Gesamtstand? Davon hängt ab, ob addiert werden darf.
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
| **GitHub Actions** | Führt Prüfung und Berichtserstellung bei jeder neuen Datei automatisch aus |
