#!/usr/bin/env python3
"""Bouwt de statische Bambine-site.

Bronnen staan in src/ (enkel de <main>-inhoud per pagina); dit script plakt daar
de gedeelde head, navigatie, footer, iconensprite en structured data omheen en
schrijft klaar-voor-upload HTML weg in deze map.

Diensten, prijzen en veelgestelde vragen staan maar op één plek: hieronder. In de
bronnen staan plaatshouders (<!-- carte:babywellness -->, <!-- faq:alle --> …) die
bij het bouwen worden ingevuld. Zo zeggen de pagina en de structured data altijd
hetzelfde.

    python3 build.py
"""

from __future__ import annotations

import hashlib
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src"

SITE = "https://bambine.be"
NAAM = "Bambine"
VOLUIT = "Bambine babywellness & mamazorg"
TEL = "+32 474 78 26 91"
TEL_HREF = "+32474782691"
MAIL = "info@bambine.be"
STRAAT = "Michiel Jansplein 28/b2"
POSTCODE = "3920"
STAD = "Lommel"
INSTA = "https://www.instagram.com/bambine.babywellness/"
FB = "https://www.facebook.com/BambineBabywellness/"
WEBSHOP = "https://www.bambine-webshop.be/"
KAART = "https://www.google.com/maps/search/?api=1&query=Michiel+Jansplein+28+3920+Lommel"

# Links in de navigatie op grote schermen; "Reserveren" is daar de gouden knop.
NAV = [
    ("tarieven.html", "Tarieven"),
    ("cadeaubon.html", "Cadeaubon"),
    ("index.html#ine", "Over Ine"),
    ("contact.html", "Contact"),
]
# Het mobiele menu toont alles onder elkaar.
DRAWER = [
    ("tarieven.html", "Tarieven"),
    ("reserveren.html", "Reserveren"),
    ("cadeaubon.html", "Cadeaubon"),
    ("index.html#ine", "Over Ine"),
    ("contact.html", "Contact"),
]

# --- diensten en prijzen (bron: bambine.be/tarieven) ------------------------

DIENSTEN = [
    dict(groep="babywellness", naam="Hydrotherapie", duur="30 minuten", prijs=55,
         noot="Dobberen en bubbelen in water van ongeveer 36 °C."),
    dict(groep="babywellness", naam="Sessie Bambine", duur="1 uur 10 minuten", prijs=75,
         noot="30 minuten hydrotherapie, daarna 40 minuten Shantala babymassage."),
    dict(groep="babywellness", naam="Duosessie Bambine", duur="1 uur", prijs=150,
         noot="Voor twee kindjes in twee aparte badjes, bijvoorbeeld vriendjes of een "
              "tweeling. 30 minuten hydrotherapie en 30 minuten Shantala babymassage."),
    dict(groep="babywellness", naam="Shantala babymassage", duur="± 35 minuten", prijs=40,
         noot="Je geeft je baby zelf de massage, onder begeleiding van Ine."),
    dict(groep="mama", naam="Zwangerschapsmassage", duur="± 75 minuten", prijs=90,
         noot="Eerst een ontspannend voetenbadje en een drankje, dan ongeveer een uur "
              "massage van het volledige lichaam."),
    dict(groep="mama", naam="Ontspanningsmassage voor vrouwen", duur="± 75 minuten", prijs=90,
         noot="Eerst een ontspannend voetenbadje en een drankje, dan ongeveer een uur "
              "massage van het volledige lichaam."),
    dict(groep="kids", naam="Verwensessie voor meisjes", sub="3 tot 16 jaar",
         duur="± 60 minuten", prijs=60,
         noot="Op maat van je kind: een drankje, een massage van 15 minuten, een "
              "gelaatsmasker, een voetenbadje, nagels lakken, schminken en haren invlechten."),
    dict(groep="kids", naam="Kids ontspanningsmassage", sub="6 tot 16 jaar",
         duur="± 60 minuten", prijs=75,
         noot="Eerst een ontspannend voetenbubbelbadje en een drankje, dan ongeveer "
              "45 minuten massage van het volledige lichaam."),
    dict(groep="kids", naam="Mini en me", duur="120 minuten", prijs=120,
         noot="Een sessie voor vrouw en meisje samen."),
]


def euro(bedrag: int) -> str:
    return f"€ {bedrag}"


def carte_html(groep: str | None = None, namen: list[str] | None = None) -> str:
    """Tarieven als menukaart: naam, stippellijn, prijs, en daaronder duur en inhoud."""
    rijen = []
    for d in DIENSTEN:
        if groep and d["groep"] != groep:
            continue
        if namen and d["naam"] not in namen:
            continue
        sub = f' <span class="carte-sub">{d["sub"]}</span>' if d.get("sub") else ""
        rijen.append(
            '<li class="carte-item">'
            f'<div class="carte-row"><h3 class="carte-name">{html.escape(d["naam"])}{sub}</h3>'
            '<span class="dots" aria-hidden="true"></span>'
            f'<p class="carte-price">{euro(d["prijs"])}</p></div>'
            f'<p class="carte-note"><span class="carte-duur">{d["duur"]}</span>{d["noot"]}</p>'
            "</li>"
        )
    return '<ul class="carte">' + "".join(rijen) + "</ul>"


def bon_opties_html() -> str:
    """Keuzelijst voor het bestelformulier van de fysieke cadeaubon."""
    opties = [
        f'<option value="{html.escape(d["naam"])} ({euro(d["prijs"])})">'
        f'{html.escape(d["naam"])} · {euro(d["prijs"])}</option>'
        for d in DIENSTEN
    ]
    opties.append('<option value="bedrag">Een bedrag naar keuze</option>')
    return "".join(opties)


# --- veelgestelde vragen (bron: bambine.be/veelgestelde-vragen en /tarieven) --

FAQ = {
    "leeftijd": (
        "Vanaf welke leeftijd is mijn baby welkom?",
        "Vanaf twee weken. Is je baby te vroeg geboren, dan tellen we vanaf de uitgerekende "
        "datum. Babywellness kan tot ongeveer 20 maanden, afhankelijk van hoe groot of klein "
        "je baby is.",
    ),
    "verloop": (
        "Hoe verloopt een sessie babywellness?",
        "We kleden je baby uit in een warme, aangename ruimte en doen een halskraagje aan. "
        "Dat is van schuim, dus het kan niet leeglopen. Dan mag je baby dobberen in water van "
        "ongeveer 36 graden en bubbelen met lichtjes en speeltjes. Daarna drogen we je baby af. "
        "Wie wil, sluit af met een Shantala babymassage die je erbij boekt.",
    ),
    "water": (
        "Wat doet het warme water met mijn baby?",
        "Door te dobberen in het water komen de darmpjes beter op gang. Dat kan krampjes "
        "verminderen en bij constipatie verloopt de stoelgang vlotter. Het water van ongeveer "
        "36 graden geeft je baby een veilig gevoel, zoals in de buik van mama, en is goed voor "
        "de bloedsomloop. Je baby verbruikt er ook veel energie bij en heeft nadien misschien "
        "wat sneller honger.",
    ),
    "shantala": (
        "Wat doet een Shantala babymassage?",
        "Ontspanning en een sterkere band tussen je baby en jou staan op de eerste plaats. "
        "Daarnaast kan de massage de darmtransit bevorderen en krampjes verlichten, helpen om "
        "spanningen los te laten, het slaapgedrag verbeteren en de bloedcirculatie op gang "
        "brengen.",
    ),
    "meebrengen": (
        "Wat breng ik mee?",
        "Gewoon de luiertas met een schone luier, propere kleertjes en eventueel wat eten. "
        "Voor de rest zorgt Bambine: massageolie, een floatband, handdoeken, tetradoeken en "
        "een zwemluier.",
    ),
    "personen": (
        "Hoeveel mensen mogen er mee?",
        "Dat kies je zelf, het is jullie moment. Maar hoe meer mensen erbij zijn, hoe meer "
        "prikkels en hoe minder rust je baby ervaart.",
    ),
    "moment": (
        "Wanneer plan ik best een afspraak?",
        "Kies een moment vlak nadat je baby gegeten heeft. Laat je baby vooraf eventueel een "
        "dutje doen: goed uitgeslapen geniet je kleintje extra.",
    ),
    "niet-komen": (
        "Wanneer kom ik beter niet?",
        "Als je baby zich niet lekker voelt of wat koortsig is. Heeft je baby net een prikje "
        "gekregen bij de dokter, wacht dan best een drietal dagen.",
    ),
    "annuleren": (
        "Wat als ik de afspraak niet kan nakomen?",
        "Verwittig zo snel mogelijk, minstens 24 uur op voorhand, en enkel telefonisch. "
        "Verwittig je op tijd en met een geldige reden, dan krijg je een tegoedbon. Kom je te "
        "laat, dan stopt de sessie wel op het afgesproken uur.",
    ),
    "betalen": (
        "Hoe betaal ik?",
        "Cash of met Payconiq. Met Bancontact betalen kan niet.",
    ),
    "meisjes": (
        "Hoe ziet een verwenmoment voor meisjes eruit?",
        "Er staan allerlei verwenspulletjes klaar. In ongeveer een uur tovert Ine je kind om "
        "tot een prinses: een korte massage, een voetenbadje, een gelaatsmasker, gelakte "
        "nagels, schmink en ingevlochten haren. Wie meekomt, mag blijven en krijgt ondertussen "
        "een drankje. Dat hoeft niet.",
    ),
    "massages": (
        "Voor wie zijn de ontspanningsmassages?",
        "De zwangerschapsmassage is voor zwangere vrouwen, hoe ver je ook bent. De "
        "ontspanningsmassage is voor elke vrouw, met of zonder kinderen. Beide krijg je in "
        "dezelfde setting; Ine past enkel de massagetechniek aan.",
    ),
    "cadeaubon": (
        "Kan ik een cadeaubon geven?",
        "Ja, voor mama, papa of baby, en ook voor meisjes vanaf 3 jaar. Kies een digitale "
        "bon, die je meteen online koopt, of een fysieke bon, die je via mail of telefonisch "
        "bestelt en in de zaak afhaalt. Het bedrag kies je zelf.",
    ),
    "aansprakelijkheid": (
        "Is Bambine aansprakelijk bij een ongeval?",
        "We zorgen samen met veel liefde en zorg voor je kleintje. Om administratieve redenen "
        "moet wel vermeld worden dat Bambine niet aansprakelijk gesteld kan worden voor "
        "eventuele ongevallen.",
    ),
}

# Welke vragen op welke pagina staan (plaatshouder <!-- faq:naam -->).
FAQ_SETS = {
    "home": ["leeftijd", "meebrengen", "personen", "annuleren"],
    "reserveren": ["meebrengen", "personen", "niet-komen", "annuleren", "leeftijd"],
    "alle": list(FAQ),
}


def faq_html(sleutels: list[str]) -> str:
    items = []
    for i, k in enumerate(sleutels, start=1):
        vraag, antwoord = FAQ[k]
        items.append(
            '<div class="faq-item">'
            f'<h3 class="faq-h"><button class="faq-q" aria-expanded="false" type="button" id="v-{k}" '
            f'aria-controls="a-{k}"><span class="faq-n">{i:02d}</span><span>{vraag}</span>'
            '<span class="faq-sign" aria-hidden="true"></span></button></h3>'
            f'<div class="faq-a" id="a-{k}" role="region" aria-labelledby="v-{k}"><div><p>{antwoord}</p></div></div>'
            "</div>"
        )
    return '<div class="faq">' + "".join(items) + "</div>"


# --- structured data -------------------------------------------------------

BEDRIJF_ID = f"{SITE}/#bambine"


def aanbod_ld(groep: str | None = None) -> list[dict]:
    return [
        {
            "@type": "Offer",
            "price": f"{d['prijs']}.00",
            "priceCurrency": "EUR",
            "url": f"{SITE}/tarieven.html#{d['groep']}",
            "itemOffered": {
                "@type": "Service",
                "name": d["naam"],
                "description": f"{d['duur']}. {d['noot']}",
                "provider": {"@id": BEDRIJF_ID},
            },
        }
        for d in DIENSTEN
        if groep is None or d["groep"] == groep
    ]


BEDRIJF = {
    "@type": "HealthAndBeautyBusiness",
    "@id": BEDRIJF_ID,
    "name": VOLUIT,
    "alternateName": NAAM,
    "description": (
        "Babywellness in Lommel: hydrotherapie in water van ongeveer 36 °C en Shantala "
        "babymassage voor baby's vanaf 2 weken tot ongeveer 20 maanden. Daarnaast "
        "zwangerschaps- en ontspanningsmassage voor vrouwen en verwenmomenten voor meisjes "
        "van 3 tot 16 jaar."
    ),
    "url": SITE + "/",
    "logo": f"{SITE}/assets/img/logo-320.webp",
    "image": f"{SITE}/assets/img/bambine-og.jpg",
    "telephone": TEL,
    "email": MAIL,
    "priceRange": "€40 - €150",
    "currenciesAccepted": "EUR",
    "paymentAccepted": "Cash, Payconiq",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": STRAAT + " (galerij Vivaldi)",
        "postalCode": POSTCODE,
        "addressLocality": STAD,
        "addressRegion": "Limburg",
        "addressCountry": "BE",
    },
    "hasMap": KAART,
    "areaServed": {"@type": "City", "name": "Lommel"},
    "founder": {"@type": "Person", "name": "Ine Hendriks"},
    "sameAs": [INSTA, FB, WEBSHOP],
    "knowsLanguage": "nl-BE",
    "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "name": "Tarieven",
        "itemListElement": aanbod_ld(),
    },
}
# Openingsuren staan niet op bambine.be; ze komen hier pas bij als Bambine ze aanlevert.


def jsonld(*blocks: dict) -> str:
    data = {"@context": "https://schema.org", "@graph": list(blocks)}
    return (
        '<script type="application/ld+json">'
        + json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
        + "</script>"
    )


def crumbs_ld(items: list[tuple[str, str]]) -> dict:
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": naam,
                "item": f"{SITE}/{url}" if url else SITE + "/",
            }
            for i, (url, naam) in enumerate(items)
        ],
    }


def faq_ld(sleutels: list[str]) -> dict:
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": FAQ[k][0],
                "acceptedAnswer": {"@type": "Answer", "text": FAQ[k][1]},
            }
            for k in sleutels
        ],
    }


def dienst_ld(naam: str, omschrijving: str, anker: str) -> dict:
    return {
        "@type": "Service",
        "name": naam,
        "description": omschrijving,
        "url": f"{SITE}/tarieven.html#{anker}",
        "provider": {"@id": BEDRIJF_ID},
        "areaServed": {"@type": "City", "name": "Lommel"},
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": naam, "itemListElement": aanbod_ld(anker)},
    }


WEBSITE = {
    "@type": "WebSite",
    "@id": f"{SITE}/#website",
    "url": SITE + "/",
    "name": VOLUIT,
    "inLanguage": "nl-BE",
    "publisher": {"@id": BEDRIJF_ID},
}

# --- pagina's ---------------------------------------------------------------

PAGES = {
    "index.html": dict(
        title="Babywellness en babymassage in Lommel | Bambine",
        desc=(
            "Babywellness in Lommel: je baby dobbert in water van ± 36 °C, met Shantala "
            "babymassage erbij. Ook massages voor mama en verwenmomenten voor meisjes."
        ),
        ld=[BEDRIJF, WEBSITE, faq_ld(FAQ_SETS["home"])],
    ),
    "tarieven.html": dict(
        title="Tarieven | Bambine babywellness en massages in Lommel",
        desc=(
            "Hydrotherapie € 55, sessie Bambine € 75, duosessie € 150, Shantala € 40, "
            "zwangerschaps- en ontspanningsmassage € 90, verwensessie voor meisjes € 60."
        ),
        ld=[
            BEDRIJF,
            dienst_ld(
                "Babywellness",
                "Hydrotherapie in water van ongeveer 36 °C en Shantala babymassage, voor baby's "
                "vanaf 2 weken tot ongeveer 20 maanden.",
                "babywellness",
            ),
            dienst_ld(
                "Mama & vrouw",
                "Zwangerschapsmassage en ontspanningsmassage van het volledige lichaam voor "
                "vrouwen, met of zonder kinderen.",
                "mama",
            ),
            dienst_ld(
                "Kids",
                "Verwensessie voor meisjes van 3 tot 16 jaar, ontspanningsmassage voor kids van "
                "6 tot 16 jaar en Mini en me voor vrouw en meisje samen.",
                "kids",
            ),
            crumbs_ld([("", "Home"), ("tarieven.html", "Tarieven")]),
        ],
    ),
    "reserveren.html": dict(
        title="Reserveren | Bambine babywellness Lommel",
        desc=(
            "Een afspraak bij Bambine maak je telefonisch op +32 474 78 26 91 of via "
            "info@bambine.be. Zo verloopt een sessie babywellness en dit breng je mee."
        ),
        ld=[
            BEDRIJF,
            crumbs_ld([("", "Home"), ("reserveren.html", "Reserveren")]),
            faq_ld(FAQ_SETS["reserveren"]),
        ],
    ),
    "cadeaubon.html": dict(
        title="Cadeaubon | Bambine babywellness Lommel",
        desc=(
            "Een cadeaubon van Bambine voor mama, papa, baby of een meisje vanaf 3 jaar. "
            "Digitaal meteen online, of als fysieke bon om af te halen in Lommel."
        ),
        ld=[BEDRIJF, crumbs_ld([("", "Home"), ("cadeaubon.html", "Cadeaubon")])],
    ),
    "contact.html": dict(
        title="Contact en veelgestelde vragen | Bambine Lommel",
        desc=(
            "Bambine, Michiel Jansplein 28/b2, 3920 Lommel (galerij Vivaldi). Bel "
            "+32 474 78 26 91 of mail info@bambine.be. Met antwoorden op de veelgestelde vragen."
        ),
        ld=[
            BEDRIJF,
            crumbs_ld([("", "Home"), ("contact.html", "Contact")]),
            faq_ld(FAQ_SETS["alle"]),
        ],
    ),
}

# --- gedeelde onderdelen ---------------------------------------------------

SPRITE = (ROOT / "assets" / "icons.svg").read_text(encoding="utf-8")


def icon(name: str, cls: str = "ico") -> str:
    return f'<svg class="{cls}" aria-hidden="true"><use href="#i-{name}"></use></svg>'


def links_html(items: list[tuple[str, str]], current: str, genummerd: bool = False) -> str:
    uit = []
    for i, (href, label) in enumerate(items):
        cur = ' aria-current="page"' if href == current else ""
        nr = f"<em>0{i + 1}</em>" if genummerd else ""
        uit.append(f'<li><a href="{href}"{cur}>{nr}{label}</a></li>')
    return "".join(uit)


BRAND = f"""<a class="brand" href="index.html">
  <img class="brand-logo" src="assets/img/logo-160.webp" width="160" height="160" alt="{NAAM}, babywellness and more">
  <img class="brand-logo brand-logo--licht" src="assets/img/logo-licht-160.webp" width="160" height="160" alt="" aria-hidden="true">
</a>"""

HEADER = """<header class="site-header{headerclass}">
  <nav class="sheet nav" aria-label="Hoofdnavigatie">
    <ul class="nav-links">{links}</ul>
    {brand}
    <div class="nav-side">
      <a class="nav-tel" href="tel:{telhref}">{ic_tel}{tel}</a>
      <a class="btn btn--sm nav-cta" href="reserveren.html">Reserveren</a>
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
        <img class="footer-logo" src="assets/img/logo-licht-320.webp" width="320" height="320" alt="{naam}, babywellness and more" loading="lazy">
        <p class="footer-lead">Babywellness, mamazorg en verwenmomenten in galerij Vivaldi, Lommel.</p>
        <div class="socials">
          <a href="{insta}" rel="noopener me" aria-label="Bambine op Instagram">{ic_ig}</a>
          <a href="{fb}" rel="noopener me" aria-label="Bambine op Facebook">{ic_fb}</a>
          <a href="mailto:{mail}" aria-label="Mail Bambine">{ic_mail}</a>
        </div>
      </div>
      <div>
        <h2 class="footer-h">Aanbod</h2>
        <ul>
          <li><a href="tarieven.html#babywellness">Babywellness</a></li>
          <li><a href="tarieven.html#mama">Mama &amp; vrouw</a></li>
          <li><a href="tarieven.html#kids">Kids</a></li>
          <li><a href="cadeaubon.html">Cadeaubon</a></li>
        </ul>
      </div>
      <div>
        <h2 class="footer-h">Praktisch</h2>
        <ul>
          <li><a href="reserveren.html">Reserveren</a></li>
          <li><a href="contact.html#faq">Veelgestelde vragen</a></li>
          <li><a href="index.html#ine">Over Ine</a></li>
          <li><a href="{shop}" rel="noopener">Webshop</a></li>
        </ul>
      </div>
      <div>
        <h2 class="footer-h">Contact</h2>
        <ul>
          <li>{straat}<br>{post} {stad}<br>galerij Vivaldi</li>
          <li><a href="tel:{telhref}">{tel}</a></li>
          <li><a href="mailto:{mail}">{mail}</a></li>
          <li>Openingsuren: <span class="todo">nog aan te vullen</span></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span data-year>2026</span> {voluit}</span>
      <span>Conceptontwerp door EM Launchpad</span>
    </div>
  </div>
</footer>"""

ACTIONBAR = """<div class="action-bar">
  <a href="tel:{telhref}">{ic_tel}Bellen</a>
  <a href="mailto:{mail}">{ic_mail}Mailen</a>
</div>"""

LAYOUT = """<!DOCTYPE html>
<html lang="nl-BE" class="no-js">
<head>
<meta charset="utf-8">
<script>document.documentElement.className="js"</script>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{site}/{path}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:locale" content="nl_BE">
<meta property="og:site_name" content="{voluit}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{site}/{path}">
<meta property="og:image" content="{site}/assets/img/bambine-og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Baby gluurt van onder een witte badhanddoek">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#42342a">
<link rel="icon" href="favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<link rel="preload" href="assets/fonts/fraunces-normal-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/mulish-normal-latin.woff2" as="font" type="font/woff2" crossorigin>
{preload}<link rel="stylesheet" href="assets/css/fonts.css">
<link rel="stylesheet" href="assets/css/site.css?v={v_css}">
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
<script src="assets/js/site.js?v={v_js}" defer></script>
</body>
</html>
"""

COMMON = dict(
    naam=NAAM, telhref=TEL_HREF, tel=TEL, mail=MAIL, straat=STRAAT, post=POSTCODE,
    stad=STAD, insta=INSTA, fb=FB, shop=WEBSHOP, voluit=VOLUIT,
    ic_tel=icon("phone"), ic_menu=icon("menu"), ic_x=icon("x"),
    ic_ig=icon("si-instagram"), ic_fb=icon("si-facebook"), ic_mail=icon("mail"),
)


def vul_in(body: str) -> str:
    """Plaatshouders in de bronnen vervangen door tarieven en vragen."""
    body = re.sub(
        r"<!-- carte:([a-z]+) -->",
        lambda m: carte_html(groep=m.group(1)),
        body,
    )
    body = re.sub(
        r"<!-- carte-namen:(.+?) -->",
        lambda m: carte_html(namen=[n.strip() for n in m.group(1).split("|")]),
        body,
    )
    body = re.sub(r"<!-- faq:([a-z]+) -->", lambda m: faq_html(FAQ_SETS[m.group(1)]), body)
    body = body.replace("<!-- bon-opties -->", bon_opties_html())
    over = re.findall(r"<!-- (?:carte|faq|bon-)[^>]*-->", body)
    if over:
        raise SystemExit(f"Onbekende plaatshouder: {over}")
    return body


def versie(pad: str) -> str:
    """Korte hash van een bestand, zodat browsers na een wijziging de nieuwe versie laden."""
    return hashlib.md5((ROOT / pad).read_bytes()).hexdigest()[:8]


def build() -> None:
    footer = FOOTER.format(**COMMON)
    v_css, v_js = versie("assets/css/site.css"), versie("assets/js/site.js")
    actionbar = ACTIONBAR.format(**COMMON)

    for path, meta in PAGES.items():
        body = vul_in((SRC / path).read_text(encoding="utf-8"))
        heeft_cover = 'class="hero-cover"' in body
        header = HEADER.format(
            brand=BRAND,
            links=links_html(NAV, path),
            dlinks=links_html(DRAWER, path, genummerd=True),
            # Boven de hero start de kop doorzichtig, ook voor het script loopt.
            headerclass=" is-over" if heeft_cover else "",
            **COMMON,
        )
        # Het hero-beeld is het grootste element boven de vouw: vroeg laden.
        preload = (
            '<link rel="preload" as="image" type="image/webp" '
            'href="assets/img/baby-onder-handdoek-1600.webp" '
            'imagesrcset="assets/img/baby-onder-handdoek-800.webp 800w, '
            'assets/img/baby-onder-handdoek-1600.webp 1600w" imagesizes="100vw" '
            'media="(min-aspect-ratio: 4/5)">\n'
            '<link rel="preload" as="image" type="image/webp" '
            'href="assets/img/baby-onder-handdoek-staand-900.webp" media="(max-aspect-ratio: 4/5)">\n'
            if heeft_cover else ""
        )
        page = LAYOUT.format(
            title=html.escape(meta["title"], quote=True),
            desc=html.escape(meta["desc"], quote=True),
            path="" if path == "index.html" else path,
            site=SITE,
            voluit=html.escape(VOLUIT),
            preload=preload,
            ld=jsonld(*meta["ld"]),
            v_css=v_css,
            v_js=v_js,
            sprite=SPRITE,
            header=header,
            body=body,
            footer=footer,
            actionbar=actionbar,
        )
        (ROOT / path).write_text(page, encoding="utf-8")
        print(f"  ✓ {path}  ({len(page) // 1024} kB)")

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
    sys.stdout.reconfigure(encoding="utf-8")  # Windows-console kent ✓ niet
    print("Bambine bouwen …")
    build()
    print("Klaar.")
