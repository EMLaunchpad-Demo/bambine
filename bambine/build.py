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
    ("babywellness.html", "Babywellness"),
    ("mamazorg.html", "Mama &amp; vrouw"),
    ("kids.html", "Kids"),
    ("tarieven.html", "Tarieven"),
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
        "Ja. Een cadeaubon bestel je telefonisch, via mail of via het contactformulier. "
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
    "babywellness.html": dict(
        title="Babywellness & hydrotherapie voor baby's | Bambine Lommel",
        desc=(
            "Hydrotherapie in water van 36 °C en Shantala babymassage voor baby's van 2 weken tot "
            "±9 maanden. Zo verloopt een sessie bij Bambine in Lommel, met tarieven en veelgestelde vragen."
        ),
        ld=[
            BEDRIJF,
            dienst_ld(
                "Babywellness: hydrotherapie en Shantala babymassage",
                "Je baby drijft in warm water van ongeveer 36 °C, speelt met lichtjes en speeltjes, "
                "en krijgt daarna optioneel een Shantala babymassage.",
                "babywellness.html",
                DIENSTEN_LD["itemListElement"],
            ),
            crumbs_ld([("", "Home"), ("babywellness.html", "Babywellness")]),
            faq_ld(FAQ_BABY),
        ],
    ),
    "mamazorg.html": dict(
        title="Zwangerschapsmassage & ontspanningsmassage | Bambine Lommel",
        desc=(
            "Mamazorg bij Bambine in Lommel: zwangerschapsmassage in elke fase van je zwangerschap "
            "en ontspanningsmassage voor vrouwen — met of zonder kinderen. Rustige praktijk, op afspraak."
        ),
        ld=[
            BEDRIJF,
            dienst_ld(
                "Mamazorg: zwangerschapsmassage en ontspanningsmassage",
                "Massage voor zwangere vrouwen in elke fase van de zwangerschap en "
                "ontspanningsmassage voor vrouwen.",
                "mamazorg.html",
            ),
            crumbs_ld([("", "Home"), ("mamazorg.html", "Mama & vrouw")]),
        ],
    ),
    "kids.html": dict(
        title="Verwenmomenten voor kinderen vanaf 3 jaar | Bambine Lommel",
        desc=(
            "Een echt verwenmoment voor kinderen van 3 tot 16 jaar: zachte gezichtsverzorging, "
            "handjes, nagels en een drankje. Alleen, met een vriendin of als klein feestje in Lommel."
        ),
        ld=[
            BEDRIJF,
            dienst_ld(
                "Verwenmomenten voor kinderen",
                "Verzorgings- en verwenmomenten voor kinderen van 3 tot 16 jaar.",
                "kids.html",
            ),
            crumbs_ld([("", "Home"), ("kids.html", "Kids")]),
        ],
    ),
    "tarieven.html": dict(
        title="Tarieven & cadeaubon | Bambine babywellness Lommel",
        desc=(
            "Alle tarieven van Bambine op één pagina: babywellness vanaf € 55, hydrotherapie met "
            "Shantala babymassage € 75, duosessie € 150. Plus cadeaubonnen en pampertaarten."
        ),
        ld=[
            BEDRIJF,
            {**DIENSTEN_LD},
            crumbs_ld([("", "Home"), ("tarieven.html", "Tarieven")]),
        ],
    ),
    "contact.html": dict(
        title="Contact & afspraak | Bambine Lommel — Michiel Jansplein 28",
        desc=(
            "Maak een afspraak bij Bambine in Lommel: Michiel Jansplein 28 bus b2, "
            "+32 474 78 26 91, info@bambine.be. Route, parkeren, openingsmomenten en "
            "veelgestelde vragen."
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
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ""
        items.append(
            f'<li><a href="{href}"{cur}>{label}{icon("chevron-right")}</a></li>'
        )
    return "".join(items)


BRAND = f"""<a class="brand" href="index.html" aria-label="{NAAM} — naar de startpagina">
  <span class="brand-mark">{icon("droplets")}</span>
  <span><span class="brand-name">bambine</span><span class="brand-sub">babywellness &amp; mamazorg</span></span>
</a>"""

HEADER = """<div class="notice" data-notice>
  <div class="wrap">
    {ic}
    <p style="margin:0"><strong>Conceptvoorstel door EM&nbsp;Launchpad</strong> — niet de officiële website van Bambine. Teksten, reviews en tarieven nog na te kijken.</p>
  </div>
</div>
<header class="site-header">
  <nav class="wrap nav" aria-label="Hoofdnavigatie">
    {brand}
    <ul class="nav-links">{links}</ul>
    <a class="nav-tel" href="tel:{telhref}">{ic_tel}{tel}</a>
    <a class="btn btn--sm" href="#afspraak" data-book="true">{ic_cal}Afspraak</a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="drawer" aria-label="Menu openen">{ic_menu}</button>
  </nav>
</header>
<div class="drawer" id="drawer" data-open="false" aria-hidden="true">
  <div class="drawer-top">
    {brand}
    <button class="dialog-close" data-drawer-close aria-label="Menu sluiten">{ic_x}</button>
  </div>
  <ul class="drawer-links">{dlinks}</ul>
  <div class="drawer-foot">
    <a class="btn btn--block" href="#afspraak" data-book="true">{ic_cal}Afspraak aanvragen</a>
    <a class="btn btn--ghost btn--block" href="tel:{telhref}">{ic_tel}{tel}</a>
  </div>
</div>"""

FOOTER = """<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <span class="brand-name">bambine</span>
        <p>Babywellness, mamazorg en verwenmomenten in hartje Lommel. Eén gezin per moment, alle tijd voor jullie twee.</p>
        <div class="socials">
          <a href="{insta}" rel="noopener me" aria-label="Bambine op Instagram">{ic_ig}</a>
          <a href="{fb}" rel="noopener me" aria-label="Bambine op Facebook">{ic_fb}</a>
          <a href="mailto:{mail}" aria-label="Mail Bambine">{ic_mail}</a>
        </div>
      </div>
      <div>
        <h4>Aanbod</h4>
        <ul>
          <li><a href="babywellness.html">Babywellness</a></li>
          <li><a href="mamazorg.html">Mama &amp; vrouw</a></li>
          <li><a href="kids.html">Kids vanaf 3 jaar</a></li>
          <li><a href="tarieven.html#cadeaubon">Cadeaubon</a></li>
          <li><a href="{shop}" rel="noopener">Webshop</a></li>
        </ul>
      </div>
      <div>
        <h4>Praktisch</h4>
        <ul>
          <li><a href="tarieven.html">Tarieven</a></li>
          <li><a href="contact.html#afspraak">Afspraak maken</a></li>
          <li><a href="contact.html#faq">Veelgestelde vragen</a></li>
          <li><a href="contact.html#route">Route &amp; parkeren</a></li>
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
      <span>© <span data-year>2026</span> {voluit} · BTW-nummer toe te voegen</span>
      <span>Conceptontwerp door <strong>EM Launchpad</strong> · niet de officiële website van Bambine</span>
    </div>
  </div>
</footer>"""

DIALOG = """<dialog id="book-dialog" aria-labelledby="dlg-title">
  <div class="dialog-in">
    <div class="dialog-head">
      <div>
        <span class="eyebrow" style="margin-bottom:.4rem">Afspraak aanvragen</span>
        <h2 id="dlg-title" style="font-size:1.6rem;margin:0">Even samen een moment kiezen</h2>
      </div>
      <button class="dialog-close" data-dialog-close aria-label="Sluiten">{ic_x}</button>
    </div>
    <form class="form" data-demo-form>
      <div class="field">
        <label for="f-dienst">Waarvoor kom je?</label>
        <select id="f-dienst" name="dienst">
          <option>Babywellness — hydrotherapie (30 min)</option>
          <option>Babywellness — hydrotherapie &amp; Shantala (1 u 10)</option>
          <option>Duosessie babywellness (1 u)</option>
          <option>Zwangerschapsmassage</option>
          <option>Ontspanningsmassage</option>
          <option>Verwenmoment kind (3–16 jaar)</option>
          <option>Cadeaubon</option>
        </select>
      </div>
      <div class="field-row">
        <div class="field">
          <label for="f-naam">Je naam</label>
          <input id="f-naam" name="naam" autocomplete="name" required>
        </div>
        <div class="field">
          <label for="f-tel">Telefoon</label>
          <input id="f-tel" name="telefoon" type="tel" autocomplete="tel" required>
        </div>
      </div>
      <div class="field-row">
        <div class="field">
          <label for="f-mail">E-mail</label>
          <input id="f-mail" name="email" type="email" autocomplete="email" required>
        </div>
        <div class="field">
          <label for="f-datum">Voorkeursdatum</label>
          <input id="f-datum" name="datum" type="date">
        </div>
      </div>
      <div class="field">
        <label for="f-bericht">Iets dat we moeten weten?</label>
        <textarea id="f-bericht" name="bericht" placeholder="Leeftijd van je baby, prematuur geboren, eerste keer …"></textarea>
      </div>
      <button class="btn btn--block" type="submit">{ic_check}Aanvraag versturen</button>
      <p class="booker-note">{ic_shield}Demo-formulier: er wordt niets verstuurd. Op de echte site komt hier de boekingskoppeling of een mail naar {mail}.</p>
    </form>
    <div data-form-ok hidden>
      <div class="ico-badge" style="margin-bottom:1rem">{ic_check}</div>
      <h3>Bedankt — dit is een demo</h3>
      <p>In de live versie krijg je nu een bevestiging per mail en komt de aanvraag in de agenda terecht.
      Wil je écht een afspraak bij Bambine? Bel <a href="tel:{telhref}">{tel}</a> of mail <a href="mailto:{mail}">{mail}</a>.</p>
    </div>
  </div>
</dialog>"""

ACTIONBAR = """<div class="action-bar">
  <a class="btn btn--ghost" href="tel:{telhref}">{ic_tel}Bellen</a>
  <a class="btn" href="#afspraak" data-book="true">{ic_cal}Afspraak</a>
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
{dialog}
{actionbar}
<script src="assets/js/site.js" defer></script>
</body>
</html>
"""


def build() -> None:
    common = dict(
        telhref=TEL_HREF, tel=TEL, mail=MAIL, straat=STRAAT, post=POSTCODE,
        stad=STAD, insta=INSTA, fb=FB, shop=WEBSHOP, voluit=VOLUIT,
        ic_tel=icon("phone"), ic_cal=icon("calendar-days"), ic_menu=icon("menu"),
        ic_x=icon("x"), ic_check=icon("check"), ic_shield=icon("shield-check"),
        ic_ig=icon("si-instagram"), ic_fb=icon("si-facebook"), ic_mail=icon("mail"),
        ic=icon("sparkles"),
    )
    footer = FOOTER.format(**common)
    dialog = DIALOG.format(**common)
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
            dialog=dialog,
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
        + "\n</main>\n" + footer + "\n" + dialog + "\n" + actionbar
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


if __name__ == "__main__":
    print("Bambine bouwen …")
    build()
    print("Klaar.")
