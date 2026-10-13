from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

NAAM_BREEDTE = 4.5 * cm
CEL_BREEDTE = 1.9 * cm  # minimale breedte per kolom zodat koppen niet over elkaar vallen


def _bouw_tabel(kop, rijen, kolombreedtes, vet_laatste=False):
    tabel = Table([kop] + rijen, colWidths=kolombreedtes, repeatRows=1)
    stijl = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F3A5F")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("ALIGN", (0, 0), (0, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EEF2F7")]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#B0B8C4")),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    if vet_laatste:
        stijl.append(("FONTNAME", (-1, 1), (-1, -1), "Helvetica-Bold"))
    tabel.setStyle(TableStyle(stijl))
    return tabel


def maak_pdf(spelers, bestandsnaam="sjoelen_scores.pdf"):
    """Maakt een PDF met naam, ronde 1, ronde 2, ..., gemiddelde, max, min en totaal.

    Past de tabel niet op één pagina, dan worden de rondes over meerdere
    tabellen verdeeld en komen gemiddelde/max/min/totaal in een eigen tabel.
    """
    doc = SimpleDocTemplate(
        bestandsnaam,
        pagesize=landscape(A4),
        leftMargin=1.5 * cm, rightMargin=1.5 * cm,
        topMargin=1.5 * cm, bottomMargin=1.5 * cm,
    )
    stijlen = getSampleStyleSheet()

    aantal_rondes = max((len(s.get_scores()) for s in spelers), default=0)
    gesorteerd = sorted(spelers, key=lambda s: s.get_totaal_score(), reverse=True)

    def ronde_cellen(s, start, eind):
        scores = s.get_scores()
        return [str(scores[i]) if i < len(scores) else "-" for i in range(start, eind)]

    def stat_cellen(s):
        return [str(round(s.get_gemiddelde())), str(s.get_max_score()),
                str(s.get_min_score()), str(s.get_totaal_score())]

    stat_kop = ["Gemiddelde", "Max", "Min", "Totaal"]
    max_kolommen = int((doc.width - NAAM_BREEDTE) // CEL_BREEDTE)
    breedte_cel = min(2.5 * cm, (doc.width - NAAM_BREEDTE) / max_kolommen)

    story = [Paragraph("Sjoelen - scoreoverzicht", stijlen["Title"]), Spacer(1, 0.5 * cm)]

    if aantal_rondes + len(stat_kop) <= max_kolommen:
        # alles past in één tabel
        kop = ["Naam"] + [f"Ronde {i}" for i in range(1, aantal_rondes + 1)] + stat_kop
        rijen = [[s.get_naam()] + ronde_cellen(s, 0, aantal_rondes) + stat_cellen(s)
                 for s in gesorteerd]
        breedtes = [NAAM_BREEDTE] + [breedte_cel] * (len(kop) - 1)
        story.append(_bouw_tabel(kop, rijen, breedtes, vet_laatste=True))
    else:
        # rondes in blokken, daarna een samenvattingstabel
        for start in range(0, aantal_rondes, max_kolommen):
            eind = min(start + max_kolommen, aantal_rondes)
            kop = ["Naam"] + [f"Ronde {i}" for i in range(start + 1, eind + 1)]
            rijen = [[s.get_naam()] + ronde_cellen(s, start, eind) for s in gesorteerd]
            breedtes = [NAAM_BREEDTE] + [breedte_cel] * (len(kop) - 1)
            story.append(_bouw_tabel(kop, rijen, breedtes))
            story.append(Spacer(1, 0.6 * cm))
        kop = ["Naam"] + stat_kop
        rijen = [[s.get_naam()] + stat_cellen(s) for s in gesorteerd]
        breedtes = [NAAM_BREEDTE] + [3 * cm] * len(stat_kop)
        story.append(_bouw_tabel(kop, rijen, breedtes, vet_laatste=True))

    doc.build(story)
    return bestandsnaam