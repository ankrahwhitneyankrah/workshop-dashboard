"""Stufe 1: Erstellt aus daten/projekte.xlsx das Dashboard ausgabe/dashboard.html.

Starten im Terminal:  python dashboard.py
Das Ergebnis ist eine einzige HTML-Datei. Sie funktioniert ohne Internet
und lässt sich einfach weitergeben.
"""

import os
import sys
import webbrowser
from datetime import datetime
from html import escape
from pathlib import Path

from bericht import Datenfehler, berechnen, laden, zahl

AUSGABE = Path(__file__).parent / "ausgabe" / "dashboard.html"


def karte(titel, wert, erklaerung):
    return (
        f'<div class="karte"><div class="titel">{escape(titel)}</div>'
        f'<div class="wert">{escape(wert)}</div>'
        f'<div class="erklaerung">{escape(erklaerung)}</div></div>'
    )


def balken_plan_ist(df):
    """Je Projekt zwei Balken: Plan (grau) und Ist (farbig, rot wenn über Plan)."""
    groesster = max(df["Plan_Stunden"].max(), df["Ist_Stunden"].max()) or 1
    zeilen = []
    for _, z in df.iterrows():
        klasse = "ist ueber" if z["Ist_Stunden"] > z["Plan_Stunden"] else "ist"
        zeilen.append(
            f'<div class="zeile"><div class="name">{escape(str(z["Projekt"]))}</div>'
            f'<div class="balken">'
            f'<div class="plan" style="width:{z["Plan_Stunden"] / groesster * 100:.1f}%"></div>'
            f'<div class="{klasse}" style="width:{z["Ist_Stunden"] / groesster * 100:.1f}%"></div>'
            f'</div><div class="zahl">{zahl(z["Ist_Stunden"])} / {zahl(z["Plan_Stunden"])} h</div></div>'
        )
    return "".join(zeilen)


def balken_bereiche(df):
    """Ist-Stunden je Bereich, größter Bereich oben."""
    summen = df.groupby("Bereich")["Ist_Stunden"].sum().sort_values(ascending=False)
    groesster = summen.max() or 1
    return "".join(
        f'<div class="zeile"><div class="name">{escape(str(bereich))}</div>'
        f'<div class="balken"><div class="ist" style="width:{wert / groesster * 100:.1f}%"></div></div>'
        f'<div class="zahl">{zahl(wert)} h</div></div>'
        for bereich, wert in summen.items()
    )


def tabelle(df):
    kopf = "".join(f"<th>{escape(s.replace('_', ' '))}</th>" for s in df.columns if s != "Datenstand")
    zeilen = ""
    for _, z in df.iterrows():
        zeilen += (
            f'<tr><td>{escape(str(z["Projekt"]))}</td><td>{escape(str(z["Bereich"]))}</td>'
            f'<td>{escape(str(z["Status"]))}</td><td class="r">{zahl(z["Plan_Stunden"])}</td>'
            f'<td class="r">{zahl(z["Ist_Stunden"])}</td></tr>'
        )
    return f"<table><thead><tr>{kopf}</tr></thead><tbody>{zeilen}</tbody></table>"


def html_seite(df, k):
    karten = "".join([
        karte("Projekte", zahl(k["anzahl_projekte"]), "Anzahl in der Excel-Datei"),
        karte("Plan-Stunden", zahl(k["plan_stunden"]), "Summe aller Projekte"),
        karte("Ist-Stunden", zahl(k["ist_stunden"]), "Summe aller Projekte"),
        karte("Abweichung", zahl(k["abweichung"], vorzeichen=True) + " h", "Ist minus Plan"),
    ])
    erstellt = datetime.now().strftime("%d.%m.%Y %H:%M")
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Projektstatus</title>
<style>
  :root {{ --text:#1d2329; --grau:#5f6b76; --linie:#dde2e7; --flaeche:#ffffff; --hintergrund:#f4f6f8;
          --akzent:#0f6e8c; --plan:#c9d1d9; --ueber:#c0392b; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--hintergrund); color:var(--text);
         font:16px/1.5 "Segoe UI", Arial, sans-serif; }}
  main {{ max-width:1100px; margin:0 auto; padding:32px 20px 48px; }}
  h1 {{ margin:0; font-size:28px; }}
  h2 {{ font-size:18px; margin:0 0 16px; }}
  .unterzeile {{ color:var(--grau); margin:4px 0 28px; }}
  .karten {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:16px; margin-bottom:24px; }}
  .karte, section {{ background:var(--flaeche); border:1px solid var(--linie); border-radius:10px; padding:20px; }}
  .karte .titel {{ color:var(--grau); font-size:14px; }}
  .karte .wert {{ font-size:34px; font-weight:600; margin:4px 0; font-variant-numeric:tabular-nums; }}
  .karte .erklaerung {{ color:var(--grau); font-size:13px; }}
  .zweispaltig {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:16px; margin-bottom:24px; }}
  .zeile {{ display:grid; grid-template-columns:150px 1fr 110px; gap:12px; align-items:center; margin:10px 0; font-size:14px; }}
  .name {{ overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }}
  .balken div {{ height:9px; border-radius:4px; margin:2px 0; }}
  .plan {{ background:var(--plan); }}
  .ist {{ background:var(--akzent); }}
  .ist.ueber {{ background:var(--ueber); }}
  .zahl {{ text-align:right; color:var(--grau); font-variant-numeric:tabular-nums; }}
  .legende {{ color:var(--grau); font-size:13px; margin-top:12px; }}
  .legende span {{ display:inline-block; width:12px; height:9px; border-radius:3px; margin:0 4px 0 12px; }}
  .tabelle-rahmen {{ overflow-x:auto; }}
  table {{ width:100%; border-collapse:collapse; font-size:14px; }}
  th, td {{ text-align:left; padding:9px 10px; border-bottom:1px solid var(--linie); }}
  th {{ color:var(--grau); font-weight:600; }}
  .r {{ text-align:right; font-variant-numeric:tabular-nums; }}
  footer {{ color:var(--grau); font-size:13px; margin-top:24px; }}
</style>
</head>
<body>
<main>
  <h1>Projektstatus</h1>
  <p class="unterzeile">Datenstand {k["datenstand"]} · erstellt am {erstellt}</p>
  <div class="karten">{karten}</div>
  <div class="zweispaltig">
    <section>
      <h2>Plan und Ist je Projekt</h2>
      {balken_plan_ist(df)}
      <div class="legende"><span style="background:var(--plan)"></span>Plan
        <span style="background:var(--akzent)"></span>Ist
        <span style="background:var(--ueber)"></span>Ist über Plan</div>
    </section>
    <section>
      <h2>Ist-Stunden je Bereich</h2>
      {balken_bereiche(df)}
    </section>
  </div>
  <section>
    <h2>Alle Projekte</h2>
    <div class="tabelle-rahmen">{tabelle(df)}</div>
  </section>
  <footer>Automatisch erzeugt aus daten/projekte.xlsx · synthetische Workshopdaten</footer>
</main>
</body>
</html>
"""


def main():
    try:
        df = laden()
    except Datenfehler as fehler:
        print("FEHLER: Die Excel-Datei ist nicht in Ordnung. Es wurde kein Dashboard erstellt.")
        print(fehler)
        sys.exit(1)

    k = berechnen(df)
    AUSGABE.parent.mkdir(exist_ok=True)
    AUSGABE.write_text(html_seite(df, k), encoding="utf-8")

    print(f"Dashboard erstellt: {AUSGABE.name} (Datenstand {k['datenstand']})")
    print(f"  Projekte: {zahl(k['anzahl_projekte'])} | Plan: {zahl(k['plan_stunden'])} h | "
          f"Ist: {zahl(k['ist_stunden'])} h | Abweichung: {zahl(k['abweichung'], vorzeichen=True)} h")

    # Lokal direkt im Browser öffnen, in GitHub Actions (CI) nicht.
    if not os.environ.get("CI"):
        webbrowser.open(AUSGABE.resolve().as_uri())


if __name__ == "__main__":
    main()
