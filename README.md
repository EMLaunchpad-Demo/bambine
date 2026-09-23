# Bambine: conceptsite

Conceptvoorstel voor een vernieuwde website van **Bambine babywellness & mamazorg**
(Michiel Jansplein 28/b2, 3920 Lommel, galerij Vivaldi). Gemaakt door **EM Launchpad**.

Een snelle, statische site zonder CMS of externe diensten. De inhoud is dezelfde als op
[bambine.be](https://bambine.be): dezelfde diensten, tarieven, voorwaarden, veelgestelde
vragen en contactgegevens, in warmere bewoording. Er is niets bijverzonnen. Wat nergens
te vinden was, staat op de site als *nog aan te vullen*.

## Pagina's

| Pagina | Inhoud |
|---|---|
| `index.html` | Hero met vullend beeld, hydrotherapie, het aanbod in drie rijen, over Ine, citaat met fotogalerij, cadeaubon, vier vragen en contact |
| `tarieven.html` | Alle diensten als menukaart, met ankers `#babywellness`, `#mama`, `#kids`, `#cadeaubon` en `#praktisch` (betalen, afzeggen, aansprakelijkheid) |
| `reserveren.html` | Hoe je reserveert (bellen of mailen), het verloop van een sessie babywellness en wat je vooraf moet weten |
| `cadeaubon.html` | Wat je cadeau kan geven, hoe je bestelt en afhaalt, en de link naar de webshop |
| `contact.html` | Adres, gegevens, een kaart die pas na een klik laadt, en alle veelgestelde vragen |

Verder: `sitemap.xml`, `robots.txt`, `site.webmanifest`, favicons, zelf gehoste webfonts
en een iconensprite.

## Bouwen

De pagina's worden samengesteld uit `src/*.html` (enkel de inhoud van `<main>`) plus de
gedeelde schil in `build.py`: head, navigatie, footer, meta-tags en JSON-LD.

```bash
python3 build.py
```

**Tarieven en veelgestelde vragen staan maar op één plek**, bovenaan `build.py`
(`DIENSTEN` en `FAQ`). In de bronnen staan plaatshouders die bij het bouwen ingevuld
worden:

- `<!-- carte:babywellness -->`, `<!-- carte:mama -->`, `<!-- carte:kids -->`: de menukaart van één groep
- `<!-- carte-namen:Hydrotherapie|Sessie Bambine -->`: losse diensten op naam
- `<!-- faq:home -->`, `<!-- faq:reserveren -->`, `<!-- faq:alle -->`: een set vragen (`FAQ_SETS`)

Zo zeggen de pagina en de structured data (Offer, FAQPage) altijd hetzelfde. Een prijs
aanpassen doe je dus in `build.py`, daarna opnieuw bouwen.

## Publiceren

De site staat in de root van de repository. Upload de map naar eender welke webhost, of
gebruik GitHub Pages: Settings → Pages → Deploy from a branch → map `/ (root)`.

## Bronnen van de inhoud

Alles komt van bambine.be (home, tarieven, veelgestelde vragen, over mij, cadeaubon,
contact), gelezen op 23 september 2026. Aanvullend, met akkoord van EM Launchpad, uit het
artikel over Ine op Beeldig Nieuws (3 juni 2026): haar achternaam, dat ze geboren en
getogen is in Lommel en in Balen woont, en dat ze één op één werkt.

Waar de oudere briefing en bambine.be verschilden, volgt de site bambine.be:

- Babywellness kan tot **ongeveer 20 maanden** (niet 9).
- De **Shantala babymassage** bestaat ook los (± 35 min, € 40): je geeft ze zelf, onder begeleiding van Ine.
- Voor de **cadeaubon** kies je zelf het bedrag.
- Ook op de site: zwangerschapsmassage en ontspanningsmassage (€ 90), kids
  ontspanningsmassage (€ 75) en Mini en me (€ 120).
- **Betalen** kan cash of met Payconiq, niet met Bancontact.

## Foto's en logo

Alle beelden komen van bambine.be. Ze staan als webp in `assets/img/`: 1600 px breed voor
grote beelden, 800 px voor kleine. De hero heeft ook een staande uitsnede voor smalle
schermen. Elke foto is bekeken en heeft een beschrijvende alt-tekst.

| Bestand | Wat erop staat | Waar |
|---|---|---|
| `baby-onder-handdoek-*` | Baby gluurt van onder een witte badhanddoek | Hero, deelbeeld (`bambine-og.jpg`) |
| `zeepbellen-hand-*` | Kinderhandje vol zeepbelletjes | Home, hydrotherapie |
| `baby-onder-dekentje-*` | Baby met blauwe ogen onder een wit dekentje | Home, aanbod |
| `zwangere-buik-*` | Zwangere buik in een roze jurk, handen in hartvorm | Home en tarieven, mama & vrouw |
| `meisje-gezichtsmassage-676` | Meisje krijgt een gezichtsmassage (uitsnede van `mini-en-me`) | Home, kids |
| `ine-met-baby-*` | Ine met een pasgeboren baby in de praktijk | Home, over Ine |
| `babyvoetjes-in-doek-*`, `baby-gaapt-teddybeer-*`, `handen-rond-babyvoetjes-*` | Sfeerbeelden | Galerij, tarieven, reserveren |
| `kind-rugmassage-*` | Kind krijgt een rugmassage | Tarieven, kids |
| `mini-en-me-*` | Vrouw en meisje krijgen samen een gezichtsmassage | Tarieven |
| `cadeaubon-*` | De cadeaubon van Bambine | Home, tarieven, cadeaubon |
| `logo-*`, `logo-licht-*` | Het huidige logo (gouden cirkel) en een lichte variant voor donkere vlakken | Header en footer |

De favicons (`favicon-32.png`, `apple-touch-icon.png`, `icon-192.png`, `icon-512.png`) zijn
gemaakt van het site-icoon van bambine.be.

## Ontwerp

De merkkleuren zijn goud, lichtbruin en wit.

| Rol | Kleur |
|---|---|
| Grond | wit `#ffffff` en warm crème `#fbf8f3` |
| Goud (knoppen, lijnen, accenten op donker) | `#c8aa66` |
| Goud voor grote cijfers op licht (3,3:1) | `#a8884a` |
| Goud voor tekst op licht (4,7:1 of meer) | `#8a6a35` |
| Donkerbruin (donkere secties, footer) | `#42342a` en `#2b211a` |
| Tekst | `#241d18` |

Knoppen zijn goud met donkere tekst (7:1); wit op goud zou onder de norm blijven.

Typografie: **Fraunces** (display) en **Mulish** (tekst), allebei zelf gehost in
`assets/fonts/`. De site maakt dus geen verbinding met Google tijdens het bezoek. De enige
uitzondering is de kaart op de contactpagina, en die laadt pas als de bezoeker erop klikt.

De opbouw is redactioneel, niet het gangbare stramien van kaartjes en iconen:

- een **hero met vullend beeld** en een warme bruine sluier, met de navigatie doorzichtig
  erover en een gouden knop "Reserveren";
- **genummerde secties** met een gouden haarlijn;
- **haarlijnen in plaats van kaders**, en een **asymmetrisch raster** van 12 kolommen;
- **bogen** als enige beeldvorm;
- het **aanbod als afwisselende rijen**, de **tarieven als menukaart**;
- **één groot citaat** van Ine. Er is geen reviewblok: bambine.be heeft geen reviews.

De animaties zijn rustig (tekst schuift zacht omhoog, beeld zoomt licht uit) en staan
helemaal uit bij `prefers-reduced-motion`. Zonder JavaScript blijft alles zichtbaar.

## SEO en toegankelijkheid

Per pagina een eigen title, description, canonical en OG-tags. Structured data:
`HealthAndBeautyBusiness` (adres, betaalwijzen, logo, sociale profielen en alle diensten
met hun prijs), `Service` en `Offer` per groep, `FAQPage`, `BreadcrumbList` en `WebSite`.
Verder `sitemap.xml`, `robots.txt`, `lang="nl-BE"`, één h1 per pagina, een skip-link,
alt-teksten op elke foto, toetsenbordbediening voor het menu en de vragen, en contrast
volgens WCAG AA.

## Nog aan te vullen vóór livegang

- **Openingsuren.** Die staan nergens op bambine.be. Op de site staan ze als *nog aan te
  vullen* (zoek op `class="todo"`). Voeg ze daarna ook toe als
  `openingHoursSpecification` bij `BEDRIJF` in `build.py`.
- **Online boeken.** Er is nog geen boekingsformulier: reserveren gaat per telefoon of mail.
- **Privacy- en cookiepagina.**
- **Foto's van de praktijk zelf**, als Bambine die heeft. Alleen `ine-met-baby` is in de
  zaak genomen; de andere beelden zijn sfeerbeelden.
- **301-redirects** van de oude URL's als deze site bambine.be vervangt:
  `/tarieven/` → `tarieven.html`, `/veelgestelde-vragen/` → `contact.html#faq`,
  `/over-mij/` → `index.html#ine`, `/cadeaubon/` → `cadeaubon.html`, `/contact/` → `contact.html`.
