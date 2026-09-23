#!/usr/bin/env python3
"""Bambine — codeboek voor GoHighLevel.

Maakt ghl/Bambine-GHL-codeboek.pdf: per pagina elke sectie met naam, uitleg en de
volledige code, klaar om over te nemen in een Custom Code-element.

Draai eerst build.py (dat schrijft ghl/globaal/ en ghl/secties/ weg), daarna:
    pip install reportlab
    python3 maak_codeboek.py

Zo blijft de code in de PDF plakbaar:
- elke regel past in de breedte; lange regels worden alleen afgebroken op een
  plek waar een regeleinde niets verandert (een spatie, of in SVG-paddata vóór
  een getal of commando); lukt dat niet, dan stopt het script met een fout;
- er staat geen kop- of voettekst op de pagina's, zodat die bij het selecteren
  over een paginagrens niet mee in de code belandt;
- elke regel code wordt als één tekstregel getekend, zonder regelnummers.
"""
import json
import pathlib
import re
import sys

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Flowable, Frame, KeepTogether, PageBreak,
                                PageTemplate, Paragraph, Spacer, Table, TableStyle)

import build

ROOT = pathlib.Path(__file__).parent
GHL = ROOT / "ghl"
UIT = GHL / "Bambine-GHL-codeboek.pdf"

# --- lettertypen --------------------------------------------------------------
FONTS = pathlib.Path("/usr/share/fonts/truetype/dejavu")
pdfmetrics.registerFont(TTFont("Mono", str(FONTS / "DejaVuSansMono.ttf")))
pdfmetrics.registerFont(TTFont("Sans", str(FONTS / "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("SansB", str(FONTS / "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Serif", str(FONTS / "DejaVuSerif.ttf")))

# --- kleuren (merkkleuren van Bambine) ------------------------------------------
INK = HexColor("#241d18")
INK2 = HexColor("#5a4e44")
MUTED = HexColor("#776a5e")
GOLD = HexColor("#c8aa66")
GOLD_INK = HexColor("#8a6a35")
SHELL = HexColor("#fbf8f3")
RULE = HexColor("#e3d9c9")
BROWN = HexColor("#2b211a")

PAGINA = landscape(A4)
MARGE = 30
CODE_PT = 6.6
CODE_LEAD = 8.3
CODE_PAD = 8
BREEDTE = PAGINA[0] - 2 * MARGE
TEKENBREEDTE = pdfmetrics.stringWidth("M", "Mono", CODE_PT)
MAXW = int((BREEDTE - 2 * CODE_PAD) / TEKENBREEDTE) - 2

# --- stijlen ------------------------------------------------------------------
S = {
    "titel": ParagraphStyle("titel", fontName="Serif", fontSize=34, leading=38, textColor=INK),
    "sub": ParagraphStyle("sub", fontName="Sans", fontSize=11, leading=16, textColor=INK2),
    "h1": ParagraphStyle("h1", fontName="Serif", fontSize=24, leading=28, textColor=INK, spaceAfter=6),
    "h2": ParagraphStyle("h2", fontName="Serif", fontSize=17, leading=21, textColor=INK, spaceAfter=2),
    "label": ParagraphStyle("label", fontName="SansB", fontSize=7.5, leading=10, textColor=GOLD_INK),
    "tekst": ParagraphStyle("tekst", fontName="Sans", fontSize=9, leading=13, textColor=INK2, alignment=TA_LEFT),
    "klein": ParagraphStyle("klein", fontName="Sans", fontSize=8, leading=11, textColor=MUTED),
    "cel": ParagraphStyle("cel", fontName="Sans", fontSize=8.5, leading=11.5, textColor=INK),
    "celb": ParagraphStyle("celb", fontName="SansB", fontSize=8.5, leading=11.5, textColor=INK),
    "celmono": ParagraphStyle("celmono", fontName="Mono", fontSize=8.5, leading=11.5, textColor=INK),
}


def esc(t: str) -> str:
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# --- afbreken zonder de code te veranderen ------------------------------------
PAD_ATTR = re.compile(r'\bd="')


def breek_regel(regel: str, soort: str) -> list[str]:
    """Breekt een te lange regel af op plekken waar een regeleinde niets verandert.

    Veilig zijn: een spatie buiten een CSS-tekenreeks (in HTML-tekst, tussen
    attributen, in paddata), en in SVG-paddata de plek vóór een minteken of
    padcommando dat direct op een cijfer volgt. Anders stopt het script."""
    if len(regel) <= MAXW:
        return [regel]
    if soort == "js":
        raise SystemExit(f"JavaScript-regel te lang voor de PDF ({len(regel)} tekens):\n{regel}")
    in_pad = [False] * len(regel)
    for m in re.finditer(r'\bd="([^"]*)"', regel):
        for k in range(m.start(1), m.end(1)):
            in_pad[k] = True
    in_tekst = [False] * len(regel)
    if soort == "css":
        q = None
        for k, ch in enumerate(regel):
            if q:
                in_tekst[k] = True
                if ch == q:
                    q = None
            elif ch in "\"'":
                q = ch
                in_tekst[k] = True
    inspring = len(regel) - len(regel.lstrip(" "))
    vervolg = " " * min(inspring + 4, 24)
    uit, pos, eerste = [], 0, True
    while True:
        prefix = "" if eerste else vervolg
        ruimte = MAXW - len(prefix)
        if len(regel) - pos <= ruimte:
            uit.append(prefix + regel[pos:])
            return uit
        grens = pos + ruimte
        knip = -1
        for k in range(grens, pos + 10, -1):
            if regel[k] == " " and not in_tekst[k]:
                knip = k
                break
        if knip != -1:
            uit.append(prefix + regel[pos:knip])
            pos = knip + 1
        else:
            for k in range(grens, pos + 10, -1):
                if in_pad[k] and regel[k] in "-MmLlHhVvCcSsQqTtAaZz" and (regel[k - 1].isdigit() or regel[k - 1] == "."):
                    knip = k
                    break
            if knip == -1:
                raise SystemExit(f"Geen veilige plek om af te breken ({soort}):\n{regel[pos:pos + 200]}")
            uit.append(prefix + regel[pos:knip])
            pos = knip
        eerste = False


def code_regels(bron: str) -> list[str]:
    """Deelt een blok in HTML-, CSS- en JS-stukken en breekt elk stuk veilig af."""
    regels: list[str] = []
    soort = "html"
    for regel in bron.rstrip("\n").split("\n"):
        regel = regel.rstrip()
        kaal = regel.strip().lower()
        huidig = soort
        if kaal.startswith("<style"):
            soort = huidig = "css"
        elif kaal.startswith("<script"):
            soort = huidig = "js"
        if kaal.startswith("</style") or kaal.startswith("</script"):
            huidig = "html"
            soort = "html"
        regels.extend(breek_regel(regel, huidig if not kaal.startswith("<") or huidig == "html" else "html"))
    return regels


# --- flowables ----------------------------------------------------------------
class CodeBlok(Flowable):
    """Code in een lichte kader, splitsbaar over pagina's, één tekstregel per regel."""

    def __init__(self, regels, sleutel, eerste=True, laatste=True):
        super().__init__()
        self.regels, self.sleutel, self.eerste, self.laatste = regels, sleutel, eerste, laatste

    def _hoogte(self, n):
        return n * CODE_LEAD + (CODE_PAD if self.eerste else 4) + (CODE_PAD if self.laatste else 4)

    def wrap(self, aw, ah):
        self.width = aw
        self.height = self._hoogte(len(self.regels))
        return aw, self.height

    def split(self, aw, ah):
        boven = CODE_PAD if self.eerste else 4
        past = int((ah - boven - 4) // CODE_LEAD)
        if past < 3 or past >= len(self.regels):
            return [] if past < 3 else [self]
        return [CodeBlok(self.regels[:past], self.sleutel, self.eerste, False),
                CodeBlok(self.regels[past:], self.sleutel, False, self.laatste)]

    def draw(self):
        c = self.canv
        c.saveState()
        c.setFillColor(SHELL)
        c.setStrokeColor(RULE)
        c.setLineWidth(0.6)
        c.rect(0, 0, self.width, self.height, fill=1, stroke=1)
        c.setFillColor(GOLD)
        c.rect(0, 0, 2.2, self.height, fill=1, stroke=0)
        c.setFillColor(INK)
        c.setFont("Mono", CODE_PT)
        y = self.height - (CODE_PAD if self.eerste else 4) - CODE_PT
        for r in self.regels:
            c.drawString(CODE_PAD, y, r)
            y -= CODE_LEAD
        c.restoreState()
        # paginabereik bijhouden voor de controle achteraf
        BEREIK.setdefault(self.sleutel, []).append(c.getPageNumber())


class Bladwijzer(Flowable):
    """Zet een bladwijzer in de PDF (onzichtbaar, zonder tekst)."""

    def __init__(self, sleutel, titel, niveau):
        super().__init__()
        self.sleutel, self.titel, self.niveau = sleutel, titel, niveau

    def wrap(self, aw, ah):
        return 0, 0

    def draw(self):
        self.canv.bookmarkPage(self.sleutel)
        self.canv.addOutlineEntry(self.titel, self.sleutel, level=self.niveau, closed=False)


BEREIK: dict[str, list[int]] = {}
BLOKKEN: list[dict] = []  # voor de controle: sleutel, bron, regels


# --- inhoud -------------------------------------------------------------------
PAGINAS = [
    ("home", "index.html"),
    ("tarieven", "tarieven.html"),
    ("reserveren", "reserveren.html"),
    ("shop", "shop.html"),
    ("contact", "contact.html"),
]

UITLEG = {
    ("globaal", "00"): "De volledige stijl (kleuren, lettertypen, opmaak) en het script "
        "(animaties, menu, FAQ). Zonder dit blok blijven alle andere blokken kaal.",
    ("globaal", "01"): "Navigatie bovenaan met het mobiele menu. Hierin zit ook de iconensprite: "
        "zonder dit blok zijn de icoontjes in de andere blokken leeg.",
    ("globaal", "98"): "Vaste balk onderaan op mobiel met Bellen en Mailen. Optioneel.",
    ("globaal", "99"): "De footer met adres, links en sociale media.",
    ("home", "hero"): "De hero: titel, tekst, reserveerknop en cadeaubonknop. De foto zet je als "
        "achtergrond van de GHL-sectie zelf.",
    ("home", "in-het-kort"): "De feitenrij: 36 °C, leeftijd, één gezin, vanafprijs.",
    ("home", "warm-water"): "Waarom warm water werkt, met de streepjeslijst.",
    ("home", "aanbod"): "De drie diensten als afwisselende rijen met boogfoto, tekst en prijs.",
    ("home", "verloop"): "Het verloop van een sessie in vijf stappen.",
    ("home", "over-ine"): "Donkere band met het citaat en het verhaal van Ine.",
    ("home", "de-praktijk"): "Galerij met drie boogfoto's en de waterlijn.",
    ("home", "wat-ouders-zeggen"): "Eén groot citaat (voorbeeldtekst, te vervangen door een echte review).",
    ("home", "cadeaubon"): "Band met de cadeaubon en een link naar de webshop.",
    ("home", "vragen-contact"): "De veelgestelde vragen naast de contactgegevens.",
    ("tarieven", "paginakop"): "Kop van de tarievenpagina met broodkruimel en intro.",
    ("tarieven", "babywellness"): "Tarieven babywellness als menukaart.",
    ("tarieven", "fotostrook"): "Brede sfeerfoto van de badruimte met een onderschrift.",
    ("tarieven", "mama-en-vrouw"): "Tarieven mama &amp; vrouw met foto.",
    ("tarieven", "kids"): "Tarieven voor kinderen vanaf 3 jaar.",
    ("tarieven", "cadeaubon"): "Cadeaubon, met foto.",
    ("tarieven", "praktisch"): "Praktische afspraken: annuleren, ziekte, betalen.",
    ("reserveren", "paginakop"): "Kop van de reserveerpagina.",
    ("reserveren", "reserveren"): "Reserveren in drie stappen, met de plek voor de GHL-agenda.",
    ("reserveren", "wat-kan-je-reserveren"): "Wat je kan reserveren, als menukaart.",
    ("reserveren", "verloop"): "Het verloop van een sessie in stappen.",
    ("reserveren", "vooraf"): "Wat je meebrengt en wat je vooraf weet, met foto.",
    ("shop", "paginakop"): "Kop van de shop.",
    ("shop", "cadeaubonnen"): "Drie cadeaubonnen als artikelen met foto en prijs.",
    ("shop", "geschenkjes"): "Pampertaarten en geschenkjes als artikelslots.",
    ("shop", "bestellen"): "Hoe bestellen werkt, met de plek voor de GHL-bestelmodule.",
    ("contact", "paginakop"): "Kop van de contactpagina.",
    ("contact", "waar-en-wanneer"): "Adres, route, parkeren en openingsmomenten.",
    ("contact", "afspraak"): "Afspraak maken, met de plek voor het GHL-formulier.",
    ("contact", "vragen"): "Alle veelgestelde vragen.",
}

PAGINANAAM = {"home": "Home", "tarieven": "Tarieven", "reserveren": "Reserveren",
              "shop": "Shop", "contact": "Contact"}


def titel_uit_bestand(bestand: pathlib.Path) -> str:
    naam = bestand.stem[3:].replace("-", " ")
    vervang = {"en": "&", "vragen contact": "Vragen & contact", "in het kort": "In het kort",
               "over ine": "Over Ine", "mama en vrouw": "Mama & vrouw"}
    if naam in vervang:
        return vervang[naam]
    return naam[:1].upper() + naam[1:]


def fotoslots(code: str) -> list[str]:
    return [m.strip() for m in re.findall(r"<!--\s*(?:FOTO-SLOT|PRODUCTSLOT):\s*(.*?)\s*-->", code, re.S)]


def sectie_blok(story, sleutel, kop, label, uitleg, bron, extra=None):
    """Eén sectie: kop, uitleg, plakinstructie, fotoslots en de code."""
    regels = code_regels(bron)
    BLOKKEN.append({"sleutel": sleutel, "bron": bron, "regels": regels})
    kop_deel = [
        Bladwijzer(sleutel, re.sub("<[^>]+>", "", kop).replace("&amp;", "&"), 1),
        Paragraph(esc(label).upper() if label else "", S["label"]),
        Paragraph(kop, S["h2"]),
        Paragraph(uitleg, S["tekst"]),
    ]
    if extra:
        kop_deel.append(Spacer(1, 3))
        kop_deel.extend(extra)
    slots = fotoslots(bron)
    if slots:
        kop_deel.append(Spacer(1, 3))
        kop_deel.append(Paragraph(
            "<b>Foto's in dit blok:</b> " + "; ".join(esc(s) for s in slots) + ". Zet de foto in "
            "de code op het beeldvlak onder dat commentaar: <font name='Mono'>style=\"background-image:"
            "url('URL-uit-GHL')\"</font> toevoegen aan de <font name='Mono'>&lt;div class=\"fig …\"&gt;</font>.",
            S["klein"]))
    kop_deel.append(Spacer(1, 7))
    story.append(KeepTogether(kop_deel))
    story.append(CodeBlok(regels, sleutel))
    story.append(PageBreak())


def omslag(story):
    story.append(Spacer(1, 40))
    story.append(Paragraph("BAMBINE · BABYWELLNESS &amp; MAMAZORG", S["label"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Codeboek voor GoHighLevel", S["titel"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "Per pagina elke sectie, met de naam, wat ze doet en de volledige code. Elk blok plak je "
        "in een eigen <b>Custom Code</b>-element. Conceptontwerp door EM Launchpad.", S["sub"]))
    story.append(Spacer(1, 22))

    stappen = [
        ["1", "Maak de vier <b>globale blokken</b> één keer aan en bewaar ze in GHL als "
              "<b>globale sectie</b>: stijl en script, kop en navigatie, actiebalk, footer."],
        ["2", "Maak per pagina de <b>paginanaam</b> en het <b>path</b> aan uit de tabel hieronder. De title "
              "en meta description voor de SEO-instellingen staan vooraan het hoofdstuk van elke pagina."],
        ["3", "Zet op elke pagina bovenaan <b>Stijl en script</b> en daaronder <b>Kop en navigatie</b>. "
              "Daarna de secties van die pagina, in de volgorde van de nummers. Onderaan de actiebalk en de footer."],
        ["4", "Zet elke GHL-sectie op <b>volle breedte</b> en de <b>padding op 0</b>: de blokken brengen "
              "hun eigen achtergrond en witruimte mee."],
        ["5", "Foto's zet je zelf in GHL. Bij de hero als achtergrond van de sectie; bij de andere "
              "beeldvlakken staat per blok waar de foto hoort."],
    ]
    t = Table([[Paragraph(n, S["celb"]), Paragraph(x, S["cel"])] for n, x in stappen],
              colWidths=[22, BREEDTE - 22])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TEXTCOLOR", (0, 0), (0, -1), GOLD_INK),
    ]))
    story.append(t)
    story.append(Spacer(1, 14))

    rijen = [[Paragraph("<b>Paginanaam</b>", S["cel"]), Paragraph("<b>Path</b>", S["cel"]),
              Paragraph("<b>Secties</b>", S["cel"])]]
    for map_naam, html_bestand in PAGINAS:
        naam, pad = build.GHL_PADEN[html_bestand]
        n = len([b for b in (GHL / "secties" / map_naam).glob("*.html") if b.stem[:2] not in ("00", "98", "99")])
        rijen.append([Paragraph(naam, S["cel"]),
                      Paragraph("/  (leeg laten)" if pad == "/" else esc(pad), S["celmono"]),
                      Paragraph(f"{n} + de globale blokken", S["cel"])])
    t = Table(rijen, colWidths=[160, 200, BREEDTE - 360])
    t.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, RULE),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, GOLD),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 14))
    story.append(Paragraph(
        "<b>Kopiëren uit deze PDF.</b> Klik vlak vóór de eerste regel van een codeblok, scrol naar het "
        "einde en klik met <b>Shift</b> ingedrukt na de laatste regel. Lange regels zijn alleen afgebroken "
        "op plaatsen waar een regeleinde niets verandert; er staat geen kop- of voettekst op de pagina's, "
        "dus een blok dat over meerdere pagina's loopt, kopieer je in één keer. Dezelfde code staat ook "
        "als losse bestanden in de map <font name='Mono'>ghl/globaal/</font> en "
        "<font name='Mono'>ghl/secties/</font>.", S["klein"]))
    story.append(PageBreak())


def pagina_overzicht(story, map_naam, bestand, secties):
    meta = build.PAGES[bestand]
    naam, pad = build.GHL_PADEN[bestand]
    story.append(Bladwijzer(f"p-{map_naam}", f"Pagina: {naam}", 0))
    story.append(Paragraph("PAGINA", S["label"]))
    story.append(Paragraph(naam, S["h1"]))
    rijen = [
        ["Paginanaam", naam],
        ["Path", "/  (leeg laten)" if pad == "/" else pad],
        ["Title (SEO)", meta["title"]],
        ["Meta description", meta["desc"]],
    ]
    t = Table([[Paragraph(a, S["celb"]), Paragraph(esc(b), S["celmono"] if a == "Path" else S["cel"])]
               for a, b in rijen], colWidths=[120, BREEDTE - 120])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 14))
    story.append(Paragraph("Volgorde op deze pagina", S["celb"]))
    story.append(Spacer(1, 4))
    volg = [["Globaal", "Stijl en script"], ["Globaal", "Kop en navigatie"]]
    volg += [[f"{nr}", titel] for nr, titel, _ in secties]
    volg += [["Globaal", "Actiebalk mobiel (optioneel)"], ["Globaal", "Footer"]]
    t = Table([[Paragraph(a, S["klein"]), Paragraph(esc(b), S["cel"])] for a, b in volg],
              colWidths=[60, BREEDTE - 60])
    t.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t)
    story.append(PageBreak())


def main():
    story = []
    omslag(story)

    # globale blokken
    story.append(Bladwijzer("globaal", "Globale blokken", 0))
    glob_titels = {"00": "Stijl en script", "01": "Kop en navigatie",
                   "98": "Actiebalk mobiel", "99": "Footer"}
    for bestand in sorted((GHL / "globaal").glob("*.html")):
        nr = bestand.stem[:2]
        sectie_blok(story, f"g-{nr}", glob_titels[nr], f"Globaal blok · {nr}",
                    UITLEG[("globaal", nr)] + " Eén keer aanmaken en als <b>globale sectie</b> op elke pagina zetten.",
                    bestand.read_text(encoding="utf-8"))

    # per pagina
    for map_naam, html_bestand in PAGINAS:
        bestanden = [b for b in sorted((GHL / "secties" / map_naam).glob("*.html"))
                     if b.stem[:2] not in ("00", "98", "99")]
        secties = [(b.stem[:2], titel_uit_bestand(b), b) for b in bestanden]
        pagina_overzicht(story, map_naam, html_bestand, secties)
        for nr, titel, b in secties:
            sleutel_naam = b.stem[3:]
            uitleg = UITLEG.get((map_naam, sleutel_naam), "Sectie van de pagina " + PAGINANAAM[map_naam] + ".")
            sectie_blok(story, f"{map_naam}-{nr}", f"{nr} — {esc(titel)}",
                        f"{PAGINANAAM[map_naam]} · sectie {nr}", uitleg,
                        b.read_text(encoding="utf-8"))

    doc = BaseDocTemplate(str(UIT), pagesize=PAGINA, leftMargin=MARGE, rightMargin=MARGE,
                          topMargin=MARGE, bottomMargin=MARGE,
                          title="Bambine — codeboek voor GoHighLevel",
                          author="EM Launchpad", subject="Secties en code per pagina")
    frame = Frame(MARGE, MARGE, BREEDTE, PAGINA[1] - 2 * MARGE, id="f", leftPadding=0,
                  rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame])])
    doc.build(story)

    # bijhouden welke pagina's bij welk blok horen, voor de controle
    (GHL / ".codeboek-blokken.json").write_text(json.dumps(
        [{"sleutel": b["sleutel"], "regels": b["regels"], "paginas": sorted(set(BEREIK.get(b["sleutel"], [])))}
         for b in BLOKKEN], ensure_ascii=False), encoding="utf-8")
    print(f"  ✓ {UIT.relative_to(ROOT)}  ({len(BLOKKEN)} blokken, max {MAXW} tekens per regel)")


if __name__ == "__main__":
    sys.exit(main())
