# Bambine — conceptsite

Conceptvoorstel voor een vernieuwde website van **Bambine babywellness & mamazorg**
(Michiel Jansplein 28 bus b2, 3920 Lommel). Gemaakt door **EM Launchpad** als demo.

> Dit is een conceptontwerp, geen officiële Bambine-website. Dat staat in de footer van
> elke pagina.

## Live preview

https://claude.ai/code/artifact/028ac88e-6ae9-40c6-bd1e-4444dac759ca

## Wat zit erin

Vijf statische pagina's, geen build-stap nodig om te hosten — gewoon uploaden.

| Pagina | Inhoud |
|---|---|
| `index.html` | Hero, feitenrij, warm water, aanbod in drie rijen, verloop, over Ine, de praktijk, citaat, cadeaubon, vragen en contact |
| `tarieven.html` | Alle diensten op één pagina: babywellness (`#babywellness`), mama &amp; vrouw (`#mama`), kids (`#kids`), cadeaubon (`#cadeaubon`) en praktische afspraken |
| `reserveren.html` | Hoe je reserveert, plek voor het GHL-formulier, wat je kan reserveren, het verloop van een sessie, wat je meebrengt |
| `shop.html` | Cadeaubonnen en geschenkjes als artikelslots, plus hoe bestellen werkt en de plek voor de bestelmodule |
| `contact.html` | Adres, route, parkeren, openingsmomenten en de FAQ |

De aparte dienstpagina's (babywellness, mamazorg, kids) zijn samengevoegd tot één
tarievenpagina met ankers per dienst. Als die URL's ooit live hebben gestaan: zet een
301-redirect naar `tarieven.html#babywellness`, `#mama` en `#kids`.

Verder: `sitemap.xml`, `robots.txt`, `site.webmanifest`, `favicon.svg`, zelf gehoste
webfonts en een iconensprite.

**Boekingswidgets zitten er bewust niet in.** Afspraken lopen voorlopig via telefoon en
mail; het boekingsformulier en de agenda komen later in GoHighLevel. Op `reserveren.html`
en op `shop.html` staat een gemarkeerd blok (`.ghl-slot`) op de plek waar dat embed-element
hoort.

## Bouwen

De pagina's worden samengesteld uit `src/*.html` (enkel de inhoud van `<main>`) plus de
gedeelde schil in `build.py`. Kop, navigatie, footer, dialoog en structured data staan
daardoor maar op één plek.

```bash
python3 build.py       # schrijft de zes .html-bestanden, sitemap en robots.txt weg
```

Wil je liever rechtstreeks in de HTML werken, dan kan dat ook — bewerk dan de
gegenereerde bestanden en laat `build.py` achterwege.

## Ontwerp

De merkkleuren zijn goud, lichtbruin en wit.

| Rol | Kleur |
|---|---|
| Grond | wit `#ffffff` + warm crème `#faf6f0` |
| Goud (knoppen, accenten) | `#c8aa66` |
| Goud voor tekst (contrastvast) | `#8a6a35` |
| Lichtbruin | `#c9b49a` |
| Donkerbruin (donkere secties) | `#42342a` |
| Tekst | `#2f2620` |

Knoppen zijn goud met donkerbruine tekst: dat haalt 6,6:1 aan contrast, terwijl wit op goud
onder de norm zou blijven.

Typografie: **Fraunces** (display, variabel, met zachte SOFT-as en WONK uit) en
**Mulish** (UI, humanistisch en zacht). Beide zelf gehost in `assets/fonts/`, dus geen
verbinding met Google tijdens het bezoek (AVG/GDPR + snelheid).

### De opbouw

Het ontwerp gebruikt bewust **niet** het gangbare stramien van kop → drie kaartjes →
iconen in cirkels → stats-strook. In plaats daarvan:

- **Genummerde secties** (`01 — Warm water`, `02 — Het aanbod`, …) als herkenbare
  handtekening, met een gouden haarlijn erachter.
- **Haarlijnen in plaats van kaders.** Geen kaartjes met schaduw, geen afgeronde blokken.
  Scheiding gebeurt met lijnen van 1 px en witruimte.
- **Asymmetrisch raster van 12 kolommen.** Tekst en beeld staan zelden even breed; beeld
  loopt aan één kant de bladspiegel uit (`.bleed-r` / `.bleed-l`).
- **De boog** als enige vorm: alle staande beelden zijn bogen.
- **Het aanbod als redactionele rijen** die links en rechts afwisselen, met een groot
  cijfer, niet als drie identieke kaartjes.
- **Tarieven als menukaart** met stippellijnen tussen naam en prijs.
- **Eén groot citaat** in plaats van drie reviewkaartjes.
- Iconen zijn teruggebracht tot twaalf, enkel waar ze functioneel zijn (telefoon, pijl,
  menu, socials). Uit [Lucide](https://lucide.dev) (ISC) en
  [Simple Icons](https://simpleicons.org) (CC0), als één inline sprite.

Animaties zijn ingehouden: tekst schuift zacht omhoog, beeld zoomt licht uit, en
paginaovergangen lopen via de View Transitions API. Alles valt stil bij
`prefers-reduced-motion: reduce`. Let op bij het aanpassen: gebruik géén `clip-path` om
een element eerst te verbergen — een volledig weggeknipt element is ook voor de
IntersectionObserver onzichtbaar en onthult zichzelf dan nooit.

## Foto's toevoegen

De site is foto-gedreven opgebouwd. In de hero staan twee aangeleverde foto's: het grote
boogbeeld komt rechtstreeks uit de GHL-mediabibliotheek (een `https://assets.cdn.filesafe.space/…`-URL)
en het kleine ingezette beeld is `assets/img/baby-knuffel.webp`. De overige beeldvlakken zijn
`.fig`-blokken met een rustig verloop in de merkkleuren als tijdelijke invulling, elk gemarkeerd
met `<!-- FOTO-SLOT: … -->` in `src/`.

Een echte foto zet je erin met één attribuut:

```html
<div class="fig arch r-4-5" style="background-image:url('assets/img/hero-baby.jpg')" …>
```

Het icoontje in het midden verdwijnt dan automatisch. Pas ook de `aria-label` aan zodat die
de foto beschrijft. Let op: gebruik géén CSS-variabele voor het pad — een `url()` in een
custom property wordt relatief aan het stylesheet opgelost, niet aan de pagina.

## Nog na te kijken vóór livegang

- **Logo.** `Babywellness_transparant.png` en `voetjes_transparant.png` staan op bambine.be
  maar zijn vanuit deze omgeving niet te downloaden. Zet ze in `assets/img/` en vervang het
  woordmerk in de header (`BRAND` in `build.py`).
- **Foto's** van de praktijk, de badruimte, Ine en de cadeauhoek. Twee foto's zijn aangeleverd
  en staan in de hero; de rest van de slots wacht nog. De `aria-label` van het grote
  hero-beeld is nog een algemene omschrijving en hoort te beschrijven wat er echt te zien is.
- **Reviews** — de drie citaten zijn voorbeeldteksten en staan ook zo gemarkeerd; te
  vervangen door echte reacties (Google, Facebook).
- **Openingsuren** — nergens publiek gevonden; nu staat er enkel "op afspraak".
- **Tarieven** voor mamazorg en kids (nu "op aanvraag") en bevestiging van de
  babywellness-tarieven (€ 55 / € 75 / € 150, overgenomen van de huidige site).
- **Btw-nummer** in de footer, en een privacy- en cookiepagina.
- **Boekingsformulier en agenda** in GoHighLevel opzetten en het `.ghl-slot`-blok op
  `reserveren.html` daardoor vervangen.
- **Assortiment van de shop**: namen, omschrijvingen, prijzen en foto's van de artikelen.
  Elk artikel is een `.good`-blok in `src/shop.html`, gemarkeerd met `<!-- PRODUCTSLOT -->`;
  kopieer een blok voor elk extra artikel. De bestelmodule van GHL vervangt het
  `.ghl-slot`-blok onderaan.
- Adres, telefoon en e-mail komen uit publiek beschikbare bronnen; graag verifiëren.

## SEO

Per pagina een eigen title, description, canonical, OG- en Twitter-tags. Structured data:
`HealthAndBeautyBusiness` met adres, regio, openingsmomenten en sociale profielen, plus
`Service` + `Offer` per dienst, `FAQPage`, `BreadcrumbList` en `WebSite`. Verder
`sitemap.xml`, `robots.txt`, `lang="nl-BE"`, semantische koppenstructuur, skip-link,
alt-teksten op elk beeldvlak en contrastverhoudingen die WCAG AA halen.

## GoHighLevel

`build.py` schrijft ook een map `ghl/` weg met per pagina één blok dat je rechtstreeks in de
GHL-pagebuilder plakt. De stijl zit daarin ingekapseld onder `.bambine-site`, de foto zit
als data-URI in het blok en er zijn geen externe bestanden nodig. De stappen staan in
[`ghl/LEESMIJ.md`](ghl/LEESMIJ.md); `ghl/_proefpagina.html` laat zien dat het blok en het
GHL-thema elkaar niet in de weg zitten.

## Compositie

De opbouw volgt de conventies voor een `local-service-booking`-site: zie
[`../composition-local-service-booking-bambine.md`](../composition-local-service-booking-bambine.md)
voor de volledige motivatie per beslissing.
