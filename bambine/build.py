#!/usr/bin/env python3
"""Bouwt de statische Bambine-site.

Bronnen staan in src/ (enkel de <main>-inhoud per pagina); dit script plakt daar
de gedeelde head, navigatie, footer, iconensprite en structured data omheen en
schrijft klaar-voor-upload HTML weg in deze map.

    python3 build.py
"""

from __future__ import annotations

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src"

SITE = "https://bambine.be"
NAAM = "Bambine"
VOLUIT = "Bambine babywellness & mamazorg"
TEL = "+32 474 78 26 91"
TEL_HREF = "+32474782691"
MAIL = "info@bambine.be"
STRAAT = "Michiel Jansplein 28 bus b2"
POSTCODE = "3920"
STAD = "Lommel"
INSTA = "https://www.instagram.com/bambine.babywellness/"
FB = "https://www.facebook.com/BambineBabywellness/"
WEBSHOP = "https://www.bambine-webshop.be/"

NAV = [
    ("tarieven.html", "Tarieven"),
    ("reserveren.html", "Reserveren"),
    ("shop.html", "Shop"),
    ("contact.html", "Contact"),
]

# --- structured data -------------------------------------------------------

BEDRIJF = {
    "@type": ["HealthAndBeautyBusiness", "ChildCare"],
    "@id": f"{SITE}/#bambine",
    "name": VOLUIT,
    "alternateName": NAAM,
    "description": (
        "Babywellness in Lommel: hydrotherapie in water van 36°C en Shantala "
        "babymassage voor baby's van 2 weken tot ongeveer 9 maanden. Daarnaast "
        "zwangerschaps- en ontspanningsmassage voor mama's en verwenmomenten "
        "voor kinderen vanaf 3 jaar."
    ),
    "url": SITE + "/",
    "telephone": TEL,
    "email": MAIL,
    "image": f"{SITE}/assets/img/bambine-og.jpg",
    "priceRange": "€€",
    "currenciesAccepted": "EUR",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": STRAAT,
        "postalCode": POSTCODE,
        "addressLocality": STAD,
        "addressRegion": "Limburg",
        "addressCountry": "BE",
    },
    "areaServed": [
        {"@type": "City", "name": "Lommel"},
        {"@type": "City", "name": "Overpelt"},
        {"@type": "City", "name": "Hamont-Achel"},
        {"@type": "City", "name": "Mol"},
        {"@type": "City", "name": "Balen"},
        {"@type": "City", "name": "Leopoldsburg"},
    ],
    "openingHoursSpecification": [
        {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": [
                "Monday", "Tuesday", "Wednesday", "Thursday",
                "Friday", "Saturday",
            ],
            "opens": "09:00",
            "closes": "18:00",
            "description": "Enkel op afspraak",
        }
    ],
    "sameAs": [INSTA, FB, WEBSHOP],
    "founder": {"@type": "Person", "name": "Ine"},
    "knowsLanguage": ["nl-BE"],
}

DIENSTEN_LD = {
    "@type": "OfferCatalog",
    "name": "Aanbod",
    "itemListElement": [
        {
            "@type": "Offer",
            "price": "55.00",
            "priceCurrency": "EUR",
            "itemOffered": {
                "@type": "Service",
                "name": "Babywellness — hydrotherapie",
                "description": "30 minuten drijven en spelen in water van ongeveer 36 °C.",
            },
        },
        {
            "@type": "Offer",
            "price": "75.00",
            "priceCurrency": "EUR",
            "itemOffered": {
                "@type": "Service",
                "name": "Babywellness — hydrotherapie & Shantala babymassage",
                "description": "30 minuten hydrotherapie gevolgd door 40 minuten Shantala babymassage.",
            },
        },
        {
            "@type": "Offer",
            "price": "150.00",
            "priceCurrency": "EUR",
            "itemOffered": {
                "@type": "Service",
                "name": "Duosessie babywellness",
                "description": "Samen met een vriendin of familielid, elk met je eigen baby.",
            },
        },
    ],
}


def jsonld(*blocks: dict) -> str:
    data = {"@context": "https://schema.org", "@graph": list(blocks)}
    return (
        '<script type="application/ld+json">'
        + json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        + "</script>"
    )


def crumbs_ld(items: list[tuple[str, str]]) -> dict:
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": re.sub("&amp;", "&", naam),
                "item": f"{SITE}/{url}" if url else SITE + "/",
            }
            for i, (url, naam) in enumerate(items)
        ],
    }


def faq_ld(paren: list[tuple[str, str]]) -> dict:
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": v,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for v, a in paren
        ],
    }


def dienst_ld(naam: str, omschrijving: str, url: str, aanbod: list[dict] | None = None) -> dict:
    d = {
        "@type": "Service",
        "name": naam,
        "description": omschrijving,
        "serviceType": naam,
        "url": f"{SITE}/{url}",
        "provider": {"@id": f"{SITE}/#bambine"},
        "areaServed": {"@type": "City", "name": "Lommel"},
        "audience": {"@type": "Audience", "audienceType": "Ouders met jonge kinderen"},
    }
    if aanbod:
        d["hasOfferCatalog"] = {"@type": "OfferCatalog", "name": naam, "itemListElement": aanbod}
    return d


FAQ_BABY = [
    (
        "Vanaf welke leeftijd mag mijn baby mee in bad?",
        "Welkom vanaf 2 weken oud — bij prematuurtjes rekenen we vanaf de uitgerekende datum — "
        "tot ongeveer 9 maanden, afhankelijk van hoe groot of klein je baby is.",
    ),
    (
        "Hoe warm is het water?",
        "Het water is altijd ongeveer 36 °C. Die warmte geeft je baby hetzelfde veilige gevoel "
        "als in de buik van mama en is goed voor de bloedsomloop. Het kost ook energie: veel baby's "
        "hebben nadien wat sneller honger.",
    ),
    (
        "Wie mag er mee komen?",
        "Jij kiest wie meekomt — het is jullie moment. Hou er wel rekening mee: hoe meer mensen "
        "aanwezig zijn, hoe meer prikkels en hoe minder rust je baby ervaart.",
    ),
    (
        "Wat moet ik zelf meebrengen?",
        "Een handdoek, een verse luier en eventueel een flesje of een dekentje dat vertrouwd ruikt. "
        "De rest staat klaar.",
    ),
    (
        "Wat is Shantala babymassage?",
        "Een zachte massagevorm uit India die je na het badje aan je baby geeft, met begeleiding. "
        "Ontspanning en de band tussen ouder en baby staan voorop.",
    ),
    (
        "Kan ik een sessie cadeau geven?",
        "Ja. Een cadeaubon bestel je telefonisch of via mail. "
        "Je haalt hem op na afspraak of je springt gewoon even binnen.",
    ),
]

# --- pagina's ---------------------------------------------------------------

PAGES = {
    "index.html": dict(
        title="Babywellness in Lommel | Bambine — hydrotherapie & Shantala babymassage",
        desc=(
            "Babywellness in Lommel. Je baby drijft in water van 36 °C, daarna een Shantala "
            "babymassage. Ook zwangerschapsmassage, ontspanningsmassage en verwenmomenten voor kids. "
            "Enkel op afspraak, één gezin per moment."
        ),
        ld=[BEDRIJF, {"@type": "WebSite", "@id": f"{SITE}/#website", "url": SITE + "/",
                      "name": VOLUIT, "inLanguage": "nl-BE",
                      "publisher": {"@id": f"{SITE}/#bambine"}},
            {**DIENSTEN_LD}, faq_ld(FAQ_BABY[:4])],
    ),
    "tarieven.html": dict(
        title="Tarieven & diensten | Bambine babywellness Lommel",
        desc=(
            "Alle diensten en tarieven van Bambine op één pagina: babywellness vanaf € 55, "
            "hydrotherapie met Shantala babymassage € 75, duosessie € 150, zwangerschaps- en "
            "ontspanningsmassage en verwenmomenten voor kinderen vanaf 3 jaar."
        ),
        ld=[
            BEDRIJF,
            {**DIENSTEN_LD},
            dienst_ld(
                "Babywellness: hydrotherapie en Shantala babymassage",
                "Je baby drijft in warm water van ongeveer 36 °C en krijgt daarna optioneel "
                "een Shantala babymassage.",
                "tarieven.html#babywellness",
                DIENSTEN_LD["itemListElement"],
            ),
            dienst_ld(
                "Mamazorg: zwangerschapsmassage en ontspanningsmassage",
                "Massage voor zwangere vrouwen in elke fase van de zwangerschap en "
                "ontspanningsmassage voor vrouwen.",
                "tarieven.html#mama",
            ),
            dienst_ld(
                "Verwenmomenten voor kinderen",
                "Verzorgings- en verwenmomenten voor kinderen van 3 tot 16 jaar.",
                "tarieven.html#kids",
            ),
            crumbs_ld([("", "Home"), ("tarieven.html", "Tarieven")]),
        ],
    ),
    "reserveren.html": dict(
        title="Reserveren | Bambine babywellness Lommel",
        desc=(
            "Een sessie reserveren bij Bambine in Lommel: bel +32 474 78 26 91 of mail "
            "info@bambine.be. Zo verloopt een sessie, wat je meebrengt en wat je vooraf "
            "moet weten."
        ),
        ld=[
            BEDRIJF,
            crumbs_ld([("", "Home"), ("reserveren.html", "Reserveren")]),
            faq_ld(FAQ_BABY[:4]),
        ],
    ),
    "shop.html": dict(
        title="Shop: cadeaubonnen, pampertaarten en geschenkjes | Bambine Lommel",
        desc=(
            "De shop van Bambine: cadeaubonnen voor een sessie babywellness, pampertaarten "
            "en gepersonaliseerde geschenkjes voor mama, papa of baby. Af te halen in Lommel."
        ),
        ld=[BEDRIJF, crumbs_ld([("", "Home"), ("shop.html", "Shop")])],
    ),
    "contact.html": dict(
        title="Contact & route | Bambine Lommel — Michiel Jansplein 28",
        desc=(
            "Bambine in Lommel: Michiel Jansplein 28 bus b2, +32 474 78 26 91, "
            "info@bambine.be. Route, parkeren, openingsmomenten en veelgestelde vragen."
        ),
        ld=[
            BEDRIJF,
            crumbs_ld([("", "Home"), ("contact.html", "Contact")]),
            faq_ld(FAQ_BABY),
        ],
    ),
}

# --- gedeelde onderdelen ---------------------------------------------------

SPRITE = (ROOT / "assets" / "icons.svg").read_text(encoding="utf-8")


def icon(name: str, cls: str = "ico") -> str:
    return f'<svg class="{cls}" aria-hidden="true"><use href="#i-{name}"></use></svg>'


def nav_html(current: str) -> str:
    items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ""
        items.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    return "".join(items)


def drawer_html(current: str) -> str:
    items = []
    for i, (href, label) in enumerate(NAV):
        cur = ' aria-current="page"' if href == current else ""
        nr = f"0{i + 1}"
        items.append(f'<li><a href="{href}"{cur}><em>{nr}</em>{label}</a></li>')
    return "".join(items)


BRAND = f"""<a class="brand" href="index.html" aria-label="{NAAM} — naar de startpagina">
  <span class="brand-name">bambine</span>
  <span class="brand-sub">babywellness &amp; mamazorg</span>
</a>"""

HEADER = """<div class="notice" data-notice>
  <div class="sheet">
    <strong>Conceptvoorstel door EM&nbsp;Launchpad</strong> — niet de officiële website van Bambine. Teksten, reviews en tarieven nog na te kijken.
  </div>
</div>
<header class="site-header">
  <nav class="sheet nav" aria-label="Hoofdnavigatie">
    <ul class="nav-links">{links}</ul>
    {brand}
    <div class="nav-side">
      <a class="nav-tel" href="tel:{telhref}">{ic_tel}{tel}</a>
      <button class="nav-toggle" aria-expanded="false" aria-controls="drawer" aria-label="Menu openen">{ic_menu}</button>
    </div>
  </nav>
</header>
<div class="drawer" id="drawer" data-open="false" aria-hidden="true">
  <div class="drawer-top">
    {brand}
    <button class="drawer-close" data-drawer-close aria-label="Menu sluiten">{ic_x}</button>
  </div>
  <ul class="drawer-links">{dlinks}</ul>
  <div class="drawer-foot">
    <a class="btn" href="tel:{telhref}">{ic_tel}{tel}</a>
    <a class="btn btn--line" href="mailto:{mail}">{ic_mail}{mail}</a>
  </div>
</div>"""

FOOTER = """<footer class="site-footer">
  <div class="sheet">
    <div class="footer-grid">
      <div>
        <span class="brand-name">bambine</span>
        <p style="margin-top:1rem;max-width:32ch">Babywellness, mamazorg en verwenmomenten in hartje Lommel. Eén gezin per moment, alle tijd voor jullie twee.</p>
        <div class="socials">
          <a href="{insta}" rel="noopener me" aria-label="Bambine op Instagram">{ic_ig}</a>
          <a href="{fb}" rel="noopener me" aria-label="Bambine op Facebook">{ic_fb}</a>
          <a href="mailto:{mail}" aria-label="Mail Bambine">{ic_mail}</a>
        </div>
      </div>
      <div>
        <h4>Aanbod</h4>
        <ul>
          <li><a href="tarieven.html#babywellness">Babywellness</a></li>
          <li><a href="tarieven.html#mama">Mama &amp; vrouw</a></li>
          <li><a href="tarieven.html#kids">Kids vanaf 3 jaar</a></li>
          <li><a href="shop.html">Shop &amp; cadeaubon</a></li>
        </ul>
      </div>
      <div>
        <h4>Praktisch</h4>
        <ul>
          <li><a href="reserveren.html">Reserveren</a></li>
          <li><a href="contact.html#faq">Veelgestelde vragen</a></li>
          <li><a href="contact.html#route">Route &amp; parkeren</a></li>
          <li><a href="{shop}" rel="noopener">Webshop</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li>{straat}<br>{post} {stad}</li>
          <li><a href="tel:{telhref}">{tel}</a></li>
          <li><a href="mailto:{mail}">{mail}</a></li>
          <li>Enkel op afspraak</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span data-year>2026</span> {voluit} · btw-nummer toe te voegen</span>
      <span>Conceptontwerp door EM Launchpad · niet de officiële website van Bambine</span>
    </div>
  </div>
</footer>"""

ACTIONBAR = """<div class="action-bar">
  <a href="tel:{telhref}">{ic_tel}Bellen</a>
  <a href="mailto:{mail}">{ic_mail}Mailen</a>
</div>"""

LAYOUT = """<!DOCTYPE html>
<html lang="nl-BE">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{site}/{path}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="author" content="{voluit}">
<meta name="geo.region" content="BE-VLI">
<meta name="geo.placename" content="Lommel">
<meta property="og:type" content="website">
<meta property="og:locale" content="nl_BE">
<meta property="og:site_name" content="{voluit}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{site}/{path}">
<meta property="og:image" content="{site}/assets/img/bambine-og.jpg">
<meta property="og:image:alt" content="Baby drijft in warm water bij Bambine in Lommel">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="theme-color" content="#10403e">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="favicon.svg">
<link rel="manifest" href="site.webmanifest">
<link rel="preload" href="assets/fonts/fraunces-normal-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/mulish-normal-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/fonts.css">
<link rel="stylesheet" href="assets/css/site.css">
{ld}
</head>
<body>
<a class="skip-link" href="#main">Naar de inhoud</a>
{sprite}
{header}
<main id="main">
{body}
</main>
{footer}
{actionbar}
<script src="assets/js/site.js" defer></script>
</body>
</html>
"""


# --- GoHighLevel-export ----------------------------------------------------
# Paginanaam en path zoals je ze in de GHL-pagebuilder invult. De sleutel is het
# bestand in deze map; de waarde is (paginanaam, path).
GHL_PADEN = {
    "index.html": ("Home", "/"),
    "tarieven.html": ("Tarieven", "tarieven"),
    "reserveren.html": ("Reserveren", "reserveren"),
    "shop.html": ("Shop", "shop"),
    "contact.html": ("Contact", "contact"),
}


def naar_fotovars(blok: str, root: pathlib.Path) -> str:
    """Relatieve fotopaden vervangen door de variabele uit de gedeelde stijl."""
    for plaatje in sorted((root / "assets" / "img").glob("*")):
        blok = blok.replace(
            f"background-image:url('assets/img/{plaatje.name}')",
            f"background-image:var(--f-{plaatje.stem})",
        )
    return blok


def naar_ghl_links(blok: str) -> str:
    """Interne links omzetten naar de paden die in GoHighLevel gebruikt worden."""
    for bestand, (_, pad) in GHL_PADEN.items():
        doel = "/" if pad == "/" else "/" + pad
        blok = blok.replace(f'href="{bestand}#', f'href="{doel}#')
        blok = blok.replace(f'href="{bestand}"', f'href="{doel}"')
    return blok


# GHL werkt met losse blokken in een pagebuilder. Per pagina schrijven we één
# zelfstandig HTML-blok weg: de CSS zit ingekapseld onder .bambine-site zodat ze
# de rest van de GHL-pagina niet raakt, de foto zit als data-URI in het blok en
# er zijn geen externe bestanden nodig behalve de webfonts.

FONT_IMPORT = (
    "@import url('https://fonts.googleapis.com/css2?"
    "family=Fraunces:ital,opsz,wght,SOFT,WONK@0,9..144,300..700,0..100,0..1;"
    "1,9..144,300..700,0..100,0..1&family=Mulish:wght@300..800&display=swap');"
)


def scope_css(css: str, scope: str = ".bambine-site") -> str:
    """Prefix elke selector met `scope`, zodat de stijl binnen het blok blijft."""
    uit: list[str] = []
    i = 0
    n = len(css)
    while i < n:
        # commentaar overslaan
        if css.startswith("/*", i):
            j = css.find("*/", i + 2)
            i = (j + 2) if j != -1 else n
            continue
        if css[i].isspace():
            i += 1
            continue
        haak = css.find("{", i)
        if haak == -1:
            break
        selector = css[i:haak].strip()
        # bijpassende sluithaak zoeken
        diepte, j = 1, haak + 1
        while j < n and diepte:
            if css[j] == "{":
                diepte += 1
            elif css[j] == "}":
                diepte -= 1
            j += 1
        body = css[haak + 1:j - 1]
        i = j

        if selector.startswith("@media") or selector.startswith("@supports"):
            uit.append(f"{selector}{{{scope_css(body, scope)}}}")
        elif selector.startswith("@keyframes") or selector.startswith("@font-face"):
            uit.append(f"{selector}{{{body}}}")
        elif selector.startswith("@view-transition"):
            continue  # paginaovergangen horen bij een hele pagina, niet bij een blok
        elif selector.startswith("@"):
            uit.append(f"{selector}{{{body}}}")
        else:
            delen = []
            for sel in selector.split(","):
                sel = sel.strip()
                if not sel:
                    continue
                if sel.startswith(":root") or sel in ("html", "body"):
                    delen.append(scope + sel.replace(":root", "").replace("html", "").replace("body", ""))
                elif sel.startswith("html ") or sel.startswith("body "):
                    delen.append(scope + sel[4:] if sel.startswith("html") else scope + sel[4:])
                elif sel.startswith("::"):
                    delen.append(f"{scope} {sel}")
                else:
                    delen.append(f"{scope} {sel}")
            uit.append(f"{','.join(delen)}{{{body}}}")
    return "".join(uit)


def data_uri(pad: pathlib.Path) -> str:
    import base64
    soort = {"webp": "image/webp", "jpg": "image/jpeg", "jpeg": "image/jpeg",
             "png": "image/png", "svg": "image/svg+xml"}[pad.suffix.lstrip(".").lower()]
    return f"data:{soort};base64," + base64.b64encode(pad.read_bytes()).decode()


def split_secties(body: str) -> list[tuple[str, str]]:
    """Splits de inhoud van een pagina in losse <section>-blokken.

    Geeft per sectie een naam (uit het commentaar erboven, anders uit id of
    aria-label) en de bijbehorende opmaak terug.
    """
    import re as _re

    secties: list[tuple[str, str]] = []
    i = 0
    laatste_naam = ""
    while True:
        start = body.find("<section", i)
        if start == -1:
            break
        # commentaar tussen de vorige sectie en deze gebruiken als naam
        tussen = body[i:start]
        namen = _re.findall(r"<!--\s*=+\s*(.*?)\s*=+\s*-->", tussen)
        if namen:
            laatste_naam = namen[-1]
        # bijpassende sluittag zoeken
        diepte, j = 0, start
        while j < len(body):
            if body.startswith("<section", j):
                diepte += 1
                j += 8
            elif body.startswith("</section>", j):
                diepte -= 1
                j += 10
                if diepte == 0:
                    break
            else:
                j += 1
        blok = body[start:j]
        naam = laatste_naam
        if not naam:
            m = _re.search(r'id="([^"]+)"', blok) or _re.search(r'aria-label="([^"]+)"', blok)
            naam = m.group(1) if m else "sectie"
        secties.append((naam, blok))
        laatste_naam = ""
        i = j
    return secties


def bestandsnaam(nummer: int, naam: str) -> str:
    import re as _re
    kaal = naam.lower()
    for a, b in [("á", "a"), ("é", "e"), ("ë", "e"), ("ï", "i"), ("ó", "o"), ("ü", "u"), ("&amp;", "en"), ("&", "en")]:
        kaal = kaal.replace(a, b)
    kaal = _re.sub(r"[^a-z0-9]+", "-", kaal).strip("-") or "sectie"
    return f"{nummer:02d}-{kaal}.html"


def ghl_export(header_html: str, footer_html: str, actionbar_html: str) -> None:
    ghl_map = ROOT / "ghl"
    ghl_map.mkdir(exist_ok=True)
    # een paar regels die voorkomen dat de stijl van het GHL-thema naar binnen lekt
    harden = (
        ".bambine-site{text-align:left;box-sizing:border-box}"
        ".bambine-site a{color:inherit}"
        ".bambine-site h1,.bambine-site h2,.bambine-site h3,.bambine-site h4{margin-top:0}"
        ".bambine-site ul,.bambine-site ol{list-style:none}"
    )
    css = harden + scope_css((ROOT / "assets" / "css" / "site.css").read_text(encoding="utf-8"))
    kale_blokken: dict[str, str] = {}
    # elke foto één keer als variabele, ook voor de gedeelde stijl van route B
    alle_fotos = "".join(
        f"--f-{plaatje.stem}:url({data_uri(plaatje)});"
        for plaatje in sorted((ROOT / "assets" / "img").glob("*"))
    )
    fotocss_gedeeld = f".bambine-site{{{alle_fotos}}}" if alle_fotos else ""
    js = (ROOT / "assets" / "js" / "site.js").read_text(encoding="utf-8")

    for pad, meta in PAGES.items():
        body = (SRC / pad).read_text(encoding="utf-8")
        kop = HEADER.format(brand=BRAND, links=nav_html(pad), dlinks=drawer_html(pad), **COMMON)
        blok = kop + f"\n<main id=\"main\">\n{body}\n</main>\n" + footer_html + "\n" + actionbar_html
        # foto's één keer als data-URI in een variabele, zodat het blok zelfstandig
        # werkt zonder dezelfde afbeelding meermaals mee te sturen
        fotos = ""
        for plaatje in sorted((ROOT / "assets" / "img").glob("*")):
            sleutel = "--f-" + plaatje.stem
            if f"assets/img/{plaatje.name}" in blok:
                fotos += f"{sleutel}:url({data_uri(plaatje)});"
                blok = blok.replace(
                    f"background-image:url('assets/img/{plaatje.name}')",
                    f"background-image:var({sleutel})",
                )
        fotocss = f".bambine-site{{{fotos}}}" if fotos else ""
        blok = naar_ghl_links(blok)
        paginanaam, ghl_pad = GHL_PADEN.get(pad, (meta["title"], pad.replace(".html", "")))
        kale_blokken[pad] = f'<div class="bambine-site">\n{SPRITE}\n{blok}\n</div>\n'

        # per sectie een eigen blok, voor wie de pagina in GHL-secties opbouwt
        sect_map = ghl_map / "secties" / ("home" if pad == "index.html" else pad.replace(".html", ""))
        sect_map.mkdir(parents=True, exist_ok=True)
        for oud in sect_map.glob("*.html"):
            oud.unlink()
        kop_blok = naar_ghl_links(kop)
        (sect_map / "00-kop-en-navigatie.html").write_text(
            f"<!-- Bambine - kop en navigatie ({paginanaam})\n"
            f"     Plaats dit als eerste blok op de pagina, of als globale sectie.\n"
            f"     De iconensprite zit hierin, dus dit blok hoort op elke pagina.\n"
            f"-->\n"
            f'<div class="bambine-site">\n{SPRITE}\n{kop_blok}\n</div>\n',
            encoding="utf-8",
        )
        secties = split_secties(naar_ghl_links(naar_fotovars(body, ROOT)))
        for nr, (naam, stuk) in enumerate(secties, start=1):
            (sect_map / bestandsnaam(nr, naam)).write_text(
                f"<!-- Bambine - {paginanaam} · sectie {nr}: {naam}\n"
                f"     Eén GHL-sectie. Stijl en script staan site-breed (route B).\n"
                f"-->\n"
                f'<div class="bambine-site">\n{stuk}\n</div>\n',
                encoding="utf-8",
            )
        (sect_map / "98-actiebalk-mobiel.html").write_text(
            "<!-- Bambine - vaste balk onderaan op mobiel (bellen en mailen).\n"
            "     Optioneel; plaats onderaan de pagina of als globale sectie. -->\n"
            f'<div class="bambine-site">\n{naar_ghl_links(actionbar_html)}\n</div>\n',
            encoding="utf-8",
        )
        (sect_map / "99-footer.html").write_text(
            "<!-- Bambine - footer. Plaats als laatste blok of als globale sectie. -->\n"
            f'<div class="bambine-site">\n{naar_ghl_links(footer_html)}\n</div>\n',
            encoding="utf-8",
        )
        print(f"  ~ ghl/secties/{sect_map.name}/ ({len(secties)} secties)")
        (ghl_map / pad).write_text(
            f"<!-- Bambine - {paginanaam}\n"
            f"     Plak dit volledige blok in een Custom Code / HTML-element in GoHighLevel.\n"
            f"     In de pagebuilder:\n"
            f"     Paginanaam:  {paginanaam}\n"
            f"     Path:        {ghl_pad}\n"
            f"     In de pagina-instellingen (SEO):\n"
            f"     Title:       {meta['title']}\n"
            f"     Description: {meta['desc']}\n"
            f"-->\n"
            f"<style>{FONT_IMPORT}{css}{fotocss}</style>\n"
            f"<div class=\"bambine-site\">\n{SPRITE}\n{blok}\n</div>\n"
            f"<script>{js}</script>\n",
            encoding="utf-8",
        )
        print(f"  ~ ghl/{pad}")

    # proefpagina: het blok in een vreemde omgeving, om te zien of de stijl
    # niet naar buiten lekt en het thema van GHL niet naar binnen
    proef = (ghl_map / "index.html").read_text(encoding="utf-8")
    (ghl_map / "_proefpagina.html").write_text(
        "<!DOCTYPE html><html lang=\"nl\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
        "<title>Proefpagina GoHighLevel-blok</title><style>"
        "body{margin:0;font-family:Arial,sans-serif;background:#eef;color:#036}"
        ".ghl-bar{padding:14px 20px;background:#036;color:#fff;font-weight:bold}"
        "h1,h2,h3{font-family:Arial,sans-serif;color:#036}a{color:#06c}"
        "</style></head><body>"
        "<div class=\"ghl-bar\">Sectie van het GHL-thema erboven</div>"
        + proef +
        "<div class=\"ghl-bar\">Sectie van het GHL-thema eronder</div>"
        "</body></html>",
        encoding="utf-8",
    )
    # --- route B: stijl en script één keer site-breed --------------------
    # De webfonts komen dan via de header-code binnen: een @import moet als
    # eerste regel van een stylesheet staan en dat is in het custom-CSS-veld
    # van GHL niet gegarandeerd.
    (ghl_map / "_header-code.html").write_text(
        "<!-- Bambine - plak dit in Settings > Tracking Code > Header -->\n"
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
        "family=Fraunces:ital,opsz,wght,SOFT,WONK@0,9..144,300..700,0..100,0..1;"
        "1,9..144,300..700,0..100,0..1&family=Mulish:wght@300..800&display=swap\">\n",
        encoding="utf-8",
    )
    (ghl_map / "_stijl.css").write_text(
        "/* Bambine - plak dit in Settings > Custom CSS.\n"
        "   De webfonts komen binnen via _header-code.html.\n"
        "   De foto's zitten onderaan als data-URI, dus er is geen upload nodig. */\n"
        + css + "\n" + fotocss_gedeeld + "\n",
        encoding="utf-8",
    )
    (ghl_map / "_script.js").write_text(js, encoding="utf-8")
    (ghl_map / "_footer-code.html").write_text(
        "<!-- Bambine - plak dit in Settings > Tracking Code > Footer -->\n"
        "<script>\n" + js + "</script>\n",
        encoding="utf-8",
    )

    # --- route B: per pagina enkel de opmaak, zonder stijl en script ------
    blokken = ghl_map / "blokken"
    blokken.mkdir(exist_ok=True)
    for bestand, kaal in kale_blokken.items():
        paginanaam, ghl_pad = GHL_PADEN[bestand]
        (blokken / bestand).write_text(
            f"<!-- Bambine - {paginanaam}\n"
            f"     Alleen de opmaak. Gebruik dit als _stijl.css en _script.js al\n"
            f"     site-breed staan; anders het bestand uit de map erboven nemen.\n"
            f"     Paginanaam:  {paginanaam}\n"
            f"     Path:        {ghl_pad}\n"
            f"-->\n" + kaal,
            encoding="utf-8",
        )
    print("  ~ ghl/_stijl.css, _script.js, _header-code.html, _footer-code.html")
    print(f"  ~ ghl/blokken/ ({len(kale_blokken)} pagina's zonder stijl en script)")
    print("  ~ ghl/_proefpagina.html")


COMMON = dict(
    telhref=TEL_HREF, tel=TEL, mail=MAIL, straat=STRAAT, post=POSTCODE,
    stad=STAD, insta=INSTA, fb=FB, shop=WEBSHOP, voluit=VOLUIT,
    ic_tel=icon("phone"), ic_cal=icon("calendar-days"), ic_menu=icon("menu"),
    ic_x=icon("x"), ic_check=icon("check"), ic_shield=icon("shield-check"),
    ic_ig=icon("si-instagram"), ic_fb=icon("si-facebook"), ic_mail=icon("mail"),
    ic=icon("sparkles"),
)


def build() -> None:
    common = COMMON
    footer = FOOTER.format(**common)
    actionbar = ACTIONBAR.format(**common)

    for path, meta in PAGES.items():
        body = (SRC / path).read_text(encoding="utf-8")
        header = HEADER.format(
            brand=BRAND, links=nav_html(path), dlinks=drawer_html(path), **common
        )
        html = LAYOUT.format(
            title=meta["title"],
            desc=meta["desc"],
            path="" if path == "index.html" else path,
            site=SITE,
            voluit=VOLUIT,
            ld=jsonld(*meta["ld"]),
            sprite=SPRITE,
            header=header,
            body=body,
            footer=footer,
            actionbar=actionbar,
        )
        (ROOT / path).write_text(html, encoding="utf-8")
        print(f"  ✓ {path}  ({len(html) // 1024} kB)")

    # losse variant voor de Artifact-preview: zonder <html>/<head>/<body>,
    # want die schil levert de artifact-host zelf aan
    art = ROOT / "_artifact"
    art.mkdir(exist_ok=True)
    body = (SRC / "index.html").read_text(encoding="utf-8")
    meta = PAGES["index.html"]
    header = HEADER.format(brand=BRAND, links=nav_html("index.html"),
                           dlinks=drawer_html("index.html"), **common)
    (art / "index.html").write_text(
        f"<title>{meta['title']}</title>\n"
        f'<meta name="description" content="{meta["desc"]}">\n'
        '<link rel="stylesheet" href="assets/css/fonts.css">\n'
        '<link rel="stylesheet" href="assets/css/site.css">\n'
        + jsonld(*meta["ld"]) + "\n"
        + '<a class="skip-link" href="#main">Naar de inhoud</a>\n'
        + SPRITE + "\n" + header + '\n<main id="main">\n' + body
        + "\n</main>\n" + footer + "\n" + actionbar
        + '\n<script src="assets/js/site.js" defer></script>\n',
        encoding="utf-8",
    )
    print("  ✓ _artifact/index.html")

    # sitemap
    urls = "".join(
        f"<url><loc>{SITE}/{'' if p == 'index.html' else p}</loc>"
        f"<changefreq>monthly</changefreq>"
        f"<priority>{'1.0' if p == 'index.html' else '0.8'}</priority></url>"
        for p in PAGES
    )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + urls
        + "</urlset>\n",
        encoding="utf-8",
    )
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8"
    )
    print("  ✓ sitemap.xml, robots.txt")

    ghl_export(header_html="", footer_html=footer, actionbar_html=actionbar)


if __name__ == "__main__":
    print("Bambine bouwen …")
    build()
    print("Klaar.")
