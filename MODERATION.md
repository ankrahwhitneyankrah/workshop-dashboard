# Moderation: Ablauf, Sollwerte und Notfallplan

Nur für die Moderation. Die Teilnehmenden arbeiten mit der [README.md](README.md).

## Probelauf-Protokoll

| Geprüft am 06.10.2026, lokal unter Windows mit Python 3.13 | Ergebnis |
|---|---|
| Tests Startstand | 5 bestanden |
| Dashboard-Bedienung (simulierter Browser, 28 Prüfungen) | Filter, Klick auf Bereich, leere Auswahl, Zurücksetzen, Sortierung, Suche, Tooltip, CSV-Export: alle bestanden |
| Farben | Farbsehschwäche-Prüfung hell und dunkel bestanden |
| Dashboard Stand 1 | 8 · 670 h · 620 h · −50 h |
| Dashboard Stand 2 | 9 · 700 h · 670 h · −30 h |
| Fehlerhafte Datei | Abbruch mit Code 1, verständliche Meldung, kein neuer Bericht |
| Musterlösung (Zweig `loesung`) | 6 Tests bestanden. Projekte über Plan: Stand 1 = 2, Stand 2 = 4. Folie mit Tabelle erzeugt |
| PowerPoint | In PowerPoint geöffnet und als Bild exportiert. Diagramm ist ein echtes, bearbeitbares Diagramm |
| GitHub Actions (06.10.2026, github.com) | Lauf nach Push grün in 24 Sekunden: Tests, Datenprüfung, Dashboard, Download „bericht“ |

**Noch nicht geprüft:** Upload eines neuen Datenstands über die GitHub-Webseite, Fehlerfall auf GitHub, Stufe 3 auf GitHub, Copilot Agent Mode und Prompt-Dateien, Teilnehmerrechner. Das ist die Generalprobe (siehe unten).

## Sollwerte auf einen Blick

| Datenstand | Projekte | Plan | Ist | Abweichung | Ausschöpfung | Über Plan |
|---|---:|---:|---:|---:|---:|---:|
| `stand_1_september` (Start) | 8 | 670 h | 620 h | −50 h | 93 % | 2 (Rechnungsprüfung, Reisekosten) |
| ↳ Filter Bereich „Finanzen“ | 2 | 130 h | 150 h | +20 h | 115 % | 2 |
| `stand_2_september` | 9 | 700 h | 670 h | −30 h | 96 % | 4 (+ Kundenportal, Schichtplanung) |
| `stand_fehlerhaft` | – | – | – | – | – | Abbruch: Schichtplanung doppelt, Wissensdatenbank ohne Ist-Stunden |

## Vor dem Workshop (blockierend)

- [x] **GitHub:** Es werden normale, kostenlose Konten auf github.com genutzt.
- [ ] **Konten der Teilnehmenden:** Spätestens eine Woche vorher alle bitten, ein GitHub-Konto anzulegen, die E-Mail-Adresse zu bestätigen und den Benutzernamen zu schicken. Am Workshop-Tag kostet das sonst 15 Minuten.
- [ ] **Vorlage-Repository:** Dieses Projekt hochladen und beide Zweige pushen. Unter **Settings** das Häkchen **Template repository** setzen. Das Vorlage-Repository muss **öffentlich** sein, damit Personen mit eigenen Konten **Use this template** nutzen können. Das ist in Ordnung, weil es nur erfundene Daten enthält. Die Kopien der Teilnehmenden sind **privat**.
- [ ] **Copilot-Zugang:** Mit einem privaten Konto gibt es Copilot Free mit einer monatlichen Obergrenze an Chat- und Agent-Anfragen. Vorab prüfen, ob die Teilnehmenden über das Unternehmen eine Copilot-Lizenz haben, die mit ihrem Konto verknüpft ist. Falls nur Copilot Free: Die Grenze reicht für den Workshop vermutlich, aber nicht für viel Ausprobieren davor. Bitte an die Teilnehmenden: Copilot vor dem Termin nicht aufbrauchen.
- [ ] **Actions-Minuten:** Private Repositories haben 2.000 kostenlose Minuten im Monat. Ein Lauf dauert etwa 1 Minute, das reicht reichlich.
- [ ] **Actions:** Einmal einen Push machen und prüfen, ob der Lauf grün wird. Wird `pip install` blockiert, mit der IT den internen Paket-Spiegel klären.
- [ ] **Copilot:** In VS Code prüfen, ob der Agent-Modus verfügbar ist und `/kennzahl-ergaenzen` im Chat erscheint.
- [ ] **Teilnehmerrechner:** Python, Git und VS Code installiert? Aufgabe „Pakete installieren“ funktioniert? Einmal auf einem fremden Gerät durchspielen.
- [ ] **Generalprobe:** Den ganzen Ablauf mit einer Person mit wenig Vorwissen durchspielen und dabei die Zeiten stoppen. Danach die Screenshots für die Folien machen.

## Ablauf

| Zeit | Block | Moderation | Teilnehmende |
|---|---|---|---|
| 09:00 | Ziel | Im eigenen Repository auf Zweig `loesung` einen Datenstand hochladen und den Actions-Lauf zeigen | zusehen |
| 09:15 | **Stufe 1** | VS Code-Oberfläche zeigen, gute vs. schwache Copilot-Anfrage | README Stufe 1, Schritte 1–5 |
| 10:05 | Pause | | |
| 10:20 | **Stufe 2** | Workflow-Datei kurz erklären (Copilot fragen: „Erkläre mir bericht.yml“) | README Stufe 2, Schritte 1–4 |
| 11:15 | **Stufe 3** | Prompt-Dateien und Projektregeln zeigen | README Stufe 3, Schritte 1–5 |
| 12:05 | Transfer | Checkliste zeigen, durch den Raum gehen | Eigene Kennzahl oder eigene Spalten |
| 12:45 | Abschluss | Ausblick: Jira, SharePoint/Power Automate, Power BI, Teams, Coding Agent | Nächsten Einsatz notieren |

## Wenn etwas schiefgeht

| Problem | Lösung |
|---|---|
| `python` wird nicht gefunden | Im Terminal `py dashboard.py` probieren. Sonst Tandem bilden. |
| `No module named 'pandas'` | VS Code hat die Python-Umgebung eines anderen Projekts aktiviert (beim Test am 06.10.2026 so passiert). Unten rechts in der Statusleiste auf die Python-Version klicken und den normalen Interpreter wählen, danach ein neues Terminal öffnen. Oder Aufgabe „Pakete installieren (einmalig)“ ausführen. |
| Copilot baut etwas Falsches | Mit **Rückgängig** im Chat bzw. in der Quellcodeverwaltung verwerfen und die Anfrage genauer stellen. Das ist ein guter Lernmoment. |
| Jemand hängt bei Stufe 1 fest | Musterlösung holen: `git checkout loesung -- bericht.py dashboard.py test_bericht.py` |
| Jemand hängt bei Stufe 3 fest | `git checkout loesung -- praesentation.py .github/workflows/bericht.yml` |
| Im Tab Actions steht „There are no workflow runs yet“ | Beim allerersten Hochladen in ein neues Repository startet GitHub manchmal keinen Lauf (beim Test am 06.10.2026 so passiert). Links auf **Bericht erstellen** und dann **Run workflow** klicken, oder einfach die nächste Änderung pushen. Ab da startet er zuverlässig. |
| Actions-Lauf bleibt gelb/wartet | Kein Runner verfügbar. Lokal mit den Aufgaben 1–3 weiterarbeiten und den Lauf im Moderations-Repository zeigen. |
| Actions gar nicht verfügbar | Stufe 2 lokal: Excel in `daten/` ersetzen, Aufgabe „1 · Dashboard erstellen“. Automatisierung nur zeigen. |
| Falsche Datei hochgeladen | Einfach die richtige Datei aus `beispieldaten/…/projekte.xlsx` erneut hochladen. Unter **Commits** bleibt jede vorige Version sichtbar. |
| Nach dem Fehlerfall wieder auf grün | `beispieldaten/stand_2_september/projekte.xlsx` erneut hochladen. |
| Push wird abgelehnt („fetch first“) | Auf GitHub wurde inzwischen eine Datei hochgeladen. In VS Code zuerst **Pull**, dann **Push**. |
