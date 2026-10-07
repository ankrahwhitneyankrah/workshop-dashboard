# Stufe 4: Bericht in Teams teilen, mit automatischer Nachricht

**Ziel:** Ein Klick in VS Code, und im Teams-Kanal liegen Dashboard und PowerPoint. Dazu erscheint automatisch eine Nachricht mit den wichtigsten Zahlen und **@alle**.

```
VS Code: Aufgabe „4 · Bericht teilen“
   └─► Teams-Ordner: Projektstatus_2026-09.html / .pptx  +  Meldungen/Projektstatus_2026-09.txt
          └─► Workflow in Teams: neue Datei in „Meldungen“ ─► Nachricht im Kanal mit @alle
```

**Wer macht was?** Python (`teilen.py`) schreibt die Nachricht und entscheidet nach den Zahlen, was darin steht. Der Workflow in Teams ist nur der **Bote**: Er postet, was in der Datei steht. Will man die Nachricht ändern, ändert man `nachricht()` in `teilen.py`.

**Warum nicht direkt von GitHub?** Viele Unternehmen sperren Nachrichten von außen nach Teams. Dieser Weg bleibt komplett im Unternehmen und eignet sich deshalb auch für echte Daten.

Dauer beim ersten Mal: etwa 20 Minuten. Danach für jeden weiteren Kanal etwa 5 Minuten.

---

## Teil A · Ordner verbinden (5 Min.)

1. In Teams den Kanal öffnen → oben **Freigegeben** (oder **Dateien**).
2. Oben **…** → **Verknüpfung zu OneDrive hinzufügen** → **Meine Dateien**.
3. Datei-Explorer öffnen (`Win + E`) → links **OneDrive – <Firma>**. Nach etwa 30 Sekunden erscheint ein Ordner wie **„<Team> - <Kanal>“**.
4. Den Ordner öffnen, oben in die Adresszeile klicken, Pfad kopieren.
5. In VS Code im Projekt eine Datei **`teilen_ordner.txt`** anlegen, den Pfad einfügen, speichern. Git lädt diese Datei nie hoch.
6. **Terminal → Aufgabe ausführen → „4 · Bericht teilen (Teams-Ordner)“**.
   ✅ **Erwartet:** In Teams unter **Freigegeben** liegen nach einigen Sekunden `Projektstatus_….html`, `….pptx` und ein Ordner **Meldungen**.

## Teil B · Tag „alle“ anlegen (3 Min.)

Ein Workflow kann nicht den ganzen Kanal erwähnen, aber einen **Tag**. Ein Tag „alle“ mit allen Mitgliedern wirkt genauso.

1. In Teams links beim Team auf **…** → **Tags verwalten**.
2. **Tag erstellen** → Name `alle` → alle Mitglieder hinzufügen → **Erstellen**.

Fehlt „Tags verwalten“, darf in diesem Team nur der Besitzer Tags anlegen. Dann den Besitzer bitten oder Teil C ohne Erwähnung bauen (Schritt C4 weglassen).

## Teil C · Workflow bauen (10 Min.)

1. Im Browser **https://make.powerautomate.com** öffnen → links **+ Erstellen** → **Automatisierter Cloud-Flow**.
2. Name: `Bericht melden – <Kanal>`. Als Trigger nach **„Wenn eine Datei erstellt wird (nur Eigenschaften)“** (SharePoint) suchen und wählen → **Erstellen**.
3. Den Trigger anklicken und ausfüllen:
   - **Websiteadresse:** die Website des Teams (gleicher Name wie das Team)
   - **Bibliotheksname:** **Dokumente**
   - **Ordner:** auf das Ordnersymbol → **Allgemein** (bzw. euer Kanal) → **Meldungen**
4. **+ Neuer Schritt** → nach **„@mention-Token für ein Tag abrufen“** (Microsoft Teams) suchen:
   - **Team:** euer Team · **Tag:** `alle`
5. **+ Neuer Schritt** → **„Dateiinhalt abrufen“** (SharePoint):
   - **Websiteadresse:** wie oben
   - **Dateibezeichner:** im Feld auf das Blitz-Symbol (dynamischer Inhalt) → **Bezeichner** aus dem Trigger
6. **+ Neuer Schritt** → **„Nachricht in einem Chat oder Kanal posten“** (Microsoft Teams):
   - **Posten als:** **Benutzer**
   - **Posten in:** **Kanal** · **Team** und **Kanal** auswählen
   - **Nachricht:** zuerst aus dem dynamischen Inhalt **@mention-Token** (aus Schritt 4) einfügen, ein Leerzeichen, dann **Dateiinhalt** (aus Schritt 5).
7. Oben rechts **Speichern**.
   ✅ **Erwartet:** keine rote Meldung. Unter **Meine Flows** steht der Flow auf **Ein**.

## Teil D · Testen (2 Min.)

1. In VS Code **„4 · Bericht teilen (Teams-Ordner)“** ausführen.
2. Im Kanal unter **Beiträge** warten. Das dauert 1 bis 5 Minuten, weil Teams den Ordner nur regelmäßig prüft.
   ✅ **Erwartet:** eine Nachricht mit **@alle**, fettem Titel, den Kennzahlen und ggf. ⚠️ Projekten über Plan.

**Wichtig:** Der Workflow meldet nur **neue** Dateien. Wird derselbe Monat erneut geteilt, wird die Datei nur überschrieben, und es kommt keine neue Nachricht. Zum erneuten Testen die Datei in `Meldungen` vorher in Teams löschen.

---

## Wenn etwas nicht klappt

| Problem | Lösung |
|---|---|
| In der Nachricht steht `{"$content-type": …}` oder Zeichensalat statt Text | In Schritt C6 statt **Dateiinhalt** einen **Ausdruck** einfügen: `base64ToString(body('Dateiinhalt_abrufen')?['$content'])` |
| Die Nachricht zeigt `<b>` und `<br>` als Text | Im Nachrichtenfeld oben auf **</>** (Codeansicht) umschalten und den Inhalt dort einfügen |
| @alle ist nicht blau bzw. niemand wird benachrichtigt | Prüfen, ob in C6 **Posten als: Benutzer** gewählt ist und der Tag Mitglieder hat |
| Flow steht auf **Angehalten** | In make.powerautomate.com den Flow öffnen: Oben steht der Grund. Bei „DLP“ oder „Richtlinie“ blockiert die IT diese Kombination. |
| Keine Nachricht nach 10 Minuten | Flow öffnen → **Ausführungsverlauf**. Kein Eintrag: Ordner im Trigger prüfen (muss **Meldungen** sein). Roter Eintrag: anklicken, der fehlerhafte Schritt ist markiert. |

## Für den eigenen Fall übernehmen

- Neuer Kanal: Teil A und C wiederholen, nur Ordner und Kanal ändern. Oder den fertigen Flow unter **…** → **Speichern unter** kopieren und umstellen.
- **Nachricht ändern:** in `teilen.py` die Funktion `nachricht()` anpassen, z. B. andere Kennzahlen oder eine andere Warnregel. Copilot hilft: „Ändere die Teams-Nachricht so, dass …“.
- **Flows laufen über das Konto der Person, die sie angelegt hat.** Für alles, was dauerhaft laufen soll: unter **Freigeben** eine zweite Person als Mitbesitzer eintragen.
