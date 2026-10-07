# Moderation: Ablauf, Sollwerte und Notfallplan

Nur für die Moderation. Die Teilnehmenden arbeiten mit der [README.md](README.md).

## Die Idee in einem Satz

Jeden Monat kommt eine neue Excel-Datei in den Ordner `daten/`. GitHub prüft sie automatisch, und das Dashboard und die PowerPoint wachsen um einen Monat. Ist die Datei fehlerhaft, bleibt alles beim alten Stand, und die Fehlermeldung nennt die Datei.

## Sollwerte auf einen Blick

| Stand | Projekte | Plan | Ist | Abweichung | Ausschöpfung | Über Plan |
|---|---:|---:|---:|---:|---:|---:|
| **Start** (Juli + August in `daten/`) | 8 | 420 h | 405 h | −15 h | 96 % | 2 (Rechnungsprüfung, Reisekosten) |
| ↳ Filter Bereich „Finanzen“ | 2 | 100 h | 115 h | +15 h | 115 % | 2 |
| ↳ Filter Monat „August 2026“ | 8 | 220 h | 215 h | −5 h | 98 % | 2 (Kundenportal, Rechnungsprüfung) · Kachel Ist: ▲ +25 h ggü. Juli |
| `beispieldaten/mit_fehlern/2026-09.xlsx` hochgeladen | – | – | – | – | – | Lauf rot: Schichtplanung doppelt, Wissensdatenbank ohne Ist-Stunden |
| `beispieldaten/2026-09.xlsx` hochgeladen (Juli bis September) | 9 | 630 h | 600 h | −30 h | 95 % | 3 (Kundenportal +15, Rechnungsprüfung +10, Reisekosten +5) |
| ↳ Filter Monat „September 2026“ | 7 | 210 h | 195 h | −15 h | 93 % | 2 (Kundenportal, Schichtplanung) · Kachel Ist: ▼ −20 h ggü. August |

**Typischer Copilot-Fehler in Stufe 1:** „Über Plan“ zeigt **4** statt 2. Copilot hat Zeilen gezählt statt Projekte (jedes Projekt steht pro Monat in einer eigenen Zeile). Lösung im Chat: „Fasse zuerst je Projekt zusammen, nutze je_projekt.“ Das ist ein guter Lernmoment: Der Sollwert hat den Fehler gefunden.

## Probelauf-Protokoll

| Geprüft am 07.10.2026, lokal unter Windows mit Python 3.13 | Ergebnis |
|---|---|
| Tests Startstand | 11 bestanden |
| Musterlösung (Zweig `loesung`) | 12 bestanden. Über Plan: Start = 2, nach September = 3. Folie mit Tabelle erzeugt |
| Dashboard Start und nach September (simulierter Browser) | Kacheln, Monatsfilter, Veränderung zum Vormonat, Klick auf Säule und Bereich, Zurücksetzen, Suche, Sortierung, Tooltip, CSV: alle bestanden |
| Fehlerhafte Datei | Abbruch mit Code 1, Meldung nennt Datei und beide Fehler, kein neuer Bericht |
| PowerPoint mit Mastervorlage | In PowerPoint geöffnet und als Bild exportiert, 8 Folien, Diagramme bearbeitbar |
| GitHub Actions | siehe Komplettdurchlauf (noch offen) |

**Noch nicht geprüft:** Upload über die GitHub-Webseite mit dem neuen Ablauf, Copilot mit den neuen Prompt-Dateien, Teilnehmerrechner. Das ist der Komplettdurchlauf und die Generalprobe.

## Vor dem Workshop (blockierend)

- [x] **GitHub:** Es werden normale, kostenlose Konten auf github.com genutzt.
- [ ] **Konten der Teilnehmenden:** Spätestens eine Woche vorher alle bitten, ein GitHub-Konto anzulegen, die E-Mail-Adresse zu bestätigen und den Benutzernamen zu schicken. Am Workshop-Tag kostet das sonst 15 Minuten.
- [ ] **Vorlage-Repository:** Unter **Settings** das Häkchen **Template repository** setzen. Zwei Möglichkeiten:
  - **öffentlich:** Jede Person kann **Use this template** nutzen. Möglich, weil nur erfundene Daten enthalten sind.
  - **privat:** Jede Person unter **Settings → Collaborators** über ihren Benutzernamen einladen. Die Einladung muss innerhalb von 7 Tagen angenommen werden.

  Die Kopien der Teilnehmenden sind in beiden Fällen **privat**.
- [ ] **Zweige der Vorlage:** Auf GitHub unter **Branches** prüfen, dass nur `main` und `loesung` existieren. Testzweige werden sonst in jede Kopie übernommen.
- [ ] **Copilot-Zugang:** Mit einem privaten Konto gibt es Copilot Free mit einer monatlichen Obergrenze an Chat- und Agent-Anfragen. Vorab prüfen, ob die Teilnehmenden über das Unternehmen eine Copilot-Lizenz haben, die mit ihrem Konto verknüpft ist. Bitte an die Teilnehmenden: Copilot vor dem Termin nicht aufbrauchen.
- [ ] **Actions-Minuten:** Private Repositories haben 2.000 kostenlose Minuten im Monat. Ein Lauf dauert etwa 1 Minute, das reicht reichlich.
- [ ] **Actions:** Einmal einen Push machen und prüfen, ob der Lauf grün wird. Wird `pip install` blockiert, mit der IT den internen Paket-Spiegel klären.
- [ ] **Copilot:** In VS Code prüfen, ob der Agent-Modus verfügbar ist und `/kennzahl-ergaenzen` im Chat erscheint.
- [ ] **Einladung:** GitHub-Konto anlegen, anonyme E-Mail-Adresse heraussuchen (Settings → Emails), Ordner außerhalb von OneDrive für Projekte bereithalten.
- [ ] **Teilnehmerrechner:** Python, Git und VS Code installiert? Aufgabe „Pakete installieren“ funktioniert? Einmal auf einem fremden Gerät durchspielen.
- [ ] **Generalprobe:** Den ganzen Ablauf mit einer Person mit wenig Vorwissen durchspielen und dabei die Zeiten stoppen.

## Ablauf

| Zeit | Block | Moderation | Teilnehmende |
|---|---|---|---|
| 09:00 | Ziel | Im eigenen Repository einen neuen Monat hochladen und zeigen, wie das Dashboard um eine Säule wächst | zusehen |
| 09:15 | **Stufe 1** | VS Code-Oberfläche zeigen, gute vs. schwache Copilot-Anfrage | README Stufe 1, Schritte 1–6 |
| 10:05 | Pause | | |
| 10:20 | **Stufe 2** | Workflow-Datei kurz erklären (Copilot fragen: „Erkläre mir bericht.yml“) | README Stufe 2, Schritte 1–5 |
| 11:15 | **Stufe 3** | Prompt-Dateien und Projektregeln zeigen | README Stufe 3, Schritte 1–5 |
| 12:05 | Transfer | Checkliste zeigen, durch den Raum gehen. Bezug: eigene Fälle mit regelmäßigen Exporten, z. B. monatliche Nutzungszahlen oder Umfrageergebnisse | Eigene Kennzahl oder eigene Spalten |
| 12:45 | Abschluss | Ausblick: Jira, SharePoint/Power Automate, Power BI, Teams, Coding Agent | Nächsten Einsatz notieren |

## Wenn etwas schiefgeht

| Problem | Lösung |
|---|---|
| `python` wird nicht gefunden | Im Terminal `py dashboard.py` probieren. Sonst Tandem bilden. |
| `No module named 'pandas'` | VS Code hat die Python-Umgebung eines anderen Projekts aktiviert (beim Test am 06.10.2026 so passiert). Unten rechts in der Statusleiste auf die Python-Version klicken und den normalen Interpreter wählen, danach ein neues Terminal öffnen. Oder Aufgabe „Pakete installieren (einmalig)“ ausführen. |
| „Über Plan“ zeigt 4 statt 2 | Copilot zählt Zeilen statt Projekte. Im Chat: „Fasse zuerst je Projekt zusammen, nutze je_projekt.“ |
| Copilot baut etwas Falsches | Mit **Undo** im Chat bzw. in der Quellcodeverwaltung verwerfen und die Anfrage genauer stellen. Das ist ein guter Lernmoment. |
| Jemand hängt bei Stufe 1 fest | Musterlösung holen: `git checkout origin/loesung -- bericht.py dashboard.py test_bericht.py` |
| Jemand hängt bei Stufe 3 fest | Musterlösung **komplett** holen: `git checkout origin/loesung -- bericht.py dashboard.py test_bericht.py praesentation.py .github/workflows/bericht.yml`. Nur einzelne Dateien passen nicht zusammen, weil Copilot eigene interne Namen vergibt. |
| `origin/loesung` nicht gefunden | Beim Erstellen aus der Vorlage fehlte „Include all branches“. Musterlösung direkt aus dem Vorlage-Repository auf GitHub öffnen (Zweig `loesung`) und Dateien kopieren, oder Repository neu aus der Vorlage erstellen. |
| Gelbe Banner „Compare & pull request“ für `loesung` | Ignorieren. Wer dort einen Pull Request erstellt und mergt, hat die Musterlösung in `main`. |
| Symbol oder Knopf nicht zu finden | Immer über die Befehlspalette: `Strg + Shift + P` und den Befehl tippen, z. B. `Git: Create Branch`, `Python: Select Interpreter`. |
| Copilot fragt nach Name, Regel, Sollwert | So gewollt: Die Prompt-Datei fragt die drei Angaben ab. Antworten stehen in der README, Stufe 1. |
| Unter dem Chat „Keep“ und „Undo“ | Erst Ergebnis prüfen, dann **Keep**. Bei falschem Ergebnis **Undo** und genauer fragen. |
| `Permission denied` bei Git | Repository liegt in OneDrive. Neu klonen in einen Ordner außerhalb von OneDrive. |
| Im Tab Actions steht „There are no workflow runs yet“ | Links auf **Bericht erstellen** und dann **Run workflow** klicken, oder einfach die nächste Änderung hochladen. |
| Actions-Lauf bleibt gelb/wartet | „Queued“ ist für einige Sekunden normal. Dauert es Minuten: kein Runner verfügbar. Lokal mit den Aufgaben 1–3 weiterarbeiten und den Lauf im Moderations-Repository zeigen. |
| Actions gar nicht verfügbar | Stufe 2 lokal: Datei aus `beispieldaten/` in `daten/` kopieren, Aufgabe „1 · Dashboard erstellen“. Automatisierung nur zeigen. |
| Datei mit anderem Namen hochgeladen, z. B. `September.xlsx` | Dann liegen zwei Dateien für September in `daten/`, und der Lauf meldet „Der Monat September 2026 steht in mehreren Dateien“. Auf GitHub eine der beiden Dateien löschen (Datei öffnen → **…** → **Delete file**). |
| Nach dem Fehlerfall wieder auf grün | `beispieldaten/2026-09.xlsx` hochladen. Sie hat denselben Namen und ersetzt die fehlerhafte Datei. |
| Push wird abgelehnt („fetch first“) | Auf GitHub wurde inzwischen eine Datei hochgeladen. In VS Code zuerst **Pull**, dann **Push**. |
