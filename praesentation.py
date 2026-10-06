"""Stufe 3: Erstellt aus denselben Zahlen die PowerPoint ausgabe/praesentation.pptx.

Starten im Terminal:  python praesentation.py
Die Zahlen und das Diagramm entstehen automatisch. Das Diagramm ist ein echtes,
bearbeitbares PowerPoint-Diagramm. Die Aussage auf der letzten Folie
formuliert ein Mensch.
"""

import sys
from pathlib import Path

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.util import Inches, Pt

from bericht import Datenfehler, berechnen, laden, zahl

AUSGABE = Path(__file__).parent / "ausgabe" / "praesentation.pptx"
TEXT = RGBColor(0x1D, 0x23, 0x29)
GRAU = RGBColor(0x5F, 0x6B, 0x76)
AKZENT = RGBColor(0x0F, 0x6E, 0x8C)
PLAN = RGBColor(0xC9, 0xD1, 0xD9)


def textfeld(folie, links, oben, breite, hoehe, text, groesse=18, farbe=TEXT, fett=False):
    feld = folie.shapes.add_textbox(Inches(links), Inches(oben), Inches(breite), Inches(hoehe))
    feld.text_frame.word_wrap = True
    absatz = feld.text_frame.paragraphs[0]
    absatz.text = text
    absatz.font.size = Pt(groesse)
    absatz.font.color.rgb = farbe
    absatz.font.bold = fett
    return feld


def neue_folie(praes, ueberschrift, datenstand):
    folie = praes.slides.add_slide(praes.slide_layouts[6])  # leeres Layout
    textfeld(folie, 0.6, 0.4, 12, 0.8, ueberschrift, groesse=30, fett=True)
    textfeld(folie, 0.6, 6.9, 12, 0.4, f"Datenstand {datenstand} · automatisch erzeugt", groesse=11, farbe=GRAU)
    return folie


def folie_titel(praes, k):
    folie = praes.slides.add_slide(praes.slide_layouts[6])
    textfeld(folie, 0.8, 2.6, 11.5, 1.2, "Projektstatus", groesse=44, fett=True)
    textfeld(folie, 0.8, 3.7, 11.5, 0.6, f"Datenstand {k['datenstand']}", groesse=22, farbe=AKZENT)


def folie_kennzahlen(praes, k):
    folie = neue_folie(praes, "Kennzahlen auf einen Blick", k["datenstand"])
    kacheln = [
        ("Projekte", zahl(k["anzahl_projekte"])),
        ("Plan-Stunden", zahl(k["plan_stunden"])),
        ("Ist-Stunden", zahl(k["ist_stunden"])),
        ("Abweichung", zahl(k["abweichung"], vorzeichen=True) + " h"),
    ]
    for i, (titel, wert) in enumerate(kacheln):
        links = 0.6 + i * 3.1
        textfeld(folie, links, 2.4, 2.9, 1.2, wert, groesse=40, farbe=AKZENT, fett=True)
        textfeld(folie, links, 3.5, 2.9, 0.5, titel, groesse=16, farbe=GRAU)


def folie_diagramm(praes, df, k):
    folie = neue_folie(praes, "Plan und Ist je Projekt", k["datenstand"])
    daten = CategoryChartData()
    daten.categories = list(df["Projekt"])
    daten.add_series("Plan", [float(w) for w in df["Plan_Stunden"]])
    daten.add_series("Ist", [float(w) for w in df["Ist_Stunden"]])
    diagramm = folie.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.6), Inches(1.4), Inches(12.1), Inches(5.3), daten
    ).chart
    diagramm.has_legend = True
    diagramm.legend.position = XL_LEGEND_POSITION.BOTTOM
    diagramm.legend.include_in_layout = False
    diagramm.legend.font.size = Pt(12)
    diagramm.category_axis.tick_labels.font.size = Pt(11)
    diagramm.value_axis.tick_labels.font.size = Pt(11)
    diagramm.value_axis.major_gridlines.format.line.color.rgb = RGBColor(0xDD, 0xE2, 0xE7)
    diagramm.value_axis.format.line.fill.background()  # keine Achsenlinie
    for serie, farbe in zip(diagramm.plots[0].series, [PLAN, AKZENT]):
        serie.format.fill.solid()
        serie.format.fill.fore_color.rgb = farbe


def folie_aussage(praes, k):
    folie = neue_folie(praes, "Aussage und nächste Schritte", k["datenstand"])
    textfeld(folie, 0.6, 1.8, 12, 1.0, "[Hier formuliert ihr die Aussage.]", groesse=24, farbe=GRAU)
    textfeld(folie, 0.6, 2.8, 12, 1.0,
             "Die Zahlen auf den Folien davor entstehen automatisch. "
             "Die Bewertung und die Empfehlung kommen von euch.", groesse=16, farbe=GRAU)


def main():
    try:
        df = laden()
    except Datenfehler as fehler:
        print("FEHLER: Die Excel-Datei ist nicht in Ordnung. Es wurde keine Präsentation erstellt.")
        print(fehler)
        sys.exit(1)

    k = berechnen(df)
    praes = Presentation()
    praes.slide_width, praes.slide_height = Inches(13.333), Inches(7.5)  # 16:9

    folie_titel(praes, k)
    folie_kennzahlen(praes, k)
    folie_diagramm(praes, df, k)
    folie_aussage(praes, k)

    AUSGABE.parent.mkdir(exist_ok=True)
    praes.save(AUSGABE)
    print(f"Präsentation erstellt: {AUSGABE.name} ({len(praes.slides)} Folien, Datenstand {k['datenstand']})")


if __name__ == "__main__":
    main()
