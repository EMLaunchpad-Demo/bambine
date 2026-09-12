# Bambine — conceptsite

Conceptvoorstel voor een vernieuwde website van **Bambine babywellness & mamazorg**
(Michiel Jansplein 28 bus b2, 3920 Lommel). Gemaakt door **EM Launchpad** als demo.

> Dit is een conceptontwerp, geen officiële Bambine-website. Dat staat in de balk bovenaan
> elke pagina en in de footer.

## Live preview

https://claude.ai/code/artifact/028ac88e-6ae9-40c6-bd1e-4444dac759ca

## Wat zit erin

Zes statische pagina's, geen build-stap nodig om te hosten — gewoon uploaden.

| Pagina | Inhoud |
|---|---|
| `index.html` | Hero met boekingskaart, vertrouwensstrook, aanbod, verloop van een sessie, over Ine, ruimte, reviews, cadeaubon, FAQ, aanvraagformulier |
| `babywellness.html` | Hydrotherapie + Shantala, verloop, tarieven, praktische tips, volledige FAQ |
| `mamazorg.html` | Zwangerschapsmassage en ontspanningsmassage |
| `kids.html` | Verwenmomenten van 3 tot 16 jaar |
| `tarieven.html` | Alle tarieven + cadeaubon + praktische afspraken |
| `contact.html` | Adres, route, parkeren, aanvraagformulier, FAQ |

Verder: `sitemap.xml`, `robots.txt`, `site.webmanifest`, `favicon.svg`, zelf gehoste
webfonts en een iconensprite.

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

Het palet komt uit de aangeleverde foto: gebreid sage-groen, mousseline, warm beige.

| Rol | Kleur |
|---|---|
| Grond (linnen) | `#f4f1ea` |
| Kaarten (papier) | `#fbf9f5` |
| Sage (accenten, tekst) | `#5c6b50` |
| Sage donker (donkere secties, knop) | `#46523c` |
| Klei (warme accentkleur, knoppen) | `#8f5f45` |
| Zand / sage zacht | `#e2d9c9` / `#dde1d4` |

Typografie: **Fraunces** (display, variabel, met zachte SOFT-as en WONK uit) en
**Mulish** (UI, humanistisch en zacht). Beide zelf gehost in `assets/fonts/`, dus geen
verbinding met Google tijdens het bezoek (AVG/GDPR + snelheid).

Iconen zijn echte SVG-iconen uit [Lucide](https://lucide.dev) (ISC) en
[Simple Icons](https://simpleicons.org) (CC0), samengevoegd tot één inline sprite.

Animaties zijn bewust ingehouden: reveal-on-scroll, een voortgangslijn in de tijdlijn,
tellende cijfers, lichte parallax in de galerij en paginaovergangen via de View Transitions
API. Alles valt stil bij `prefers-reduced-motion: reduce`.

## Foto's toevoegen

De site is foto-gedreven opgebouwd. Twee vlakken bevatten al de aangeleverde foto
(`assets/img/baby-knuffel.webp`). De overige beeldvlakken zijn `.photo`-blokken met een
rustig linnen verloop in de merkkleuren als tijdelijke invulling, elk gemarkeerd met
`<!-- FOTO-SLOT: … -->` in `src/`.

Een echte foto zet je erin met één attribuut:

```html
<div class="photo ratio-4-5 arch" style="background-image:url('assets/img/hero-baby.jpg')" …>
```

Het icoontje in het midden verdwijnt dan automatisch. Pas ook de `aria-label` aan zodat die
de foto beschrijft. Let op: gebruik géén CSS-variabele voor het pad — een `url()` in een
custom property wordt relatief aan het stylesheet opgelost, niet aan de pagina.

## Nog na te kijken vóór livegang

- **Logo.** `Babywellness_transparant.png` en `voetjes_transparant.png` staan op bambine.be
  maar zijn vanuit deze omgeving niet te downloaden. Zet ze in `assets/img/` en vervang het
  woordmerk in de header (`BRAND` in `build.py`).
- **Foto's** van de praktijk, de badruimte, Ine en de cadeauhoek. Eén foto is aangeleverd en
  staat in de hero en de galerij; de rest van de slots wacht nog.
- **Reviews** — de drie citaten zijn voorbeeldteksten en staan ook zo gemarkeerd; te
  vervangen door echte reacties (Google, Facebook).
- **Openingsuren** — nergens publiek gevonden; nu staat er enkel "op afspraak".
- **Tarieven** voor mamazorg en kids (nu "op aanvraag") en bevestiging van de
  babywellness-tarieven (€ 55 / € 75 / € 150, overgenomen van de huidige site).
- **Btw-nummer** in de footer, en een privacy- en cookiepagina.
- **Formulier** koppelen aan een echte mailbox of aan de boekingstool (Fresha, GoHighLevel).
  Nu is het een demo die niets verstuurt en dat ook zegt.
- Adres, telefoon en e-mail komen uit publiek beschikbare bronnen; graag verifiëren.

## SEO

Per pagina een eigen title, description, canonical, OG- en Twitter-tags. Structured data:
`HealthAndBeautyBusiness` met adres, regio, openingsmomenten en sociale profielen, plus
`Service` + `Offer` per dienst, `FAQPage`, `BreadcrumbList` en `WebSite`. Verder
`sitemap.xml`, `robots.txt`, `lang="nl-BE"`, semantische koppenstructuur, skip-link,
alt-teksten op elk beeldvlak en contrastverhoudingen die WCAG AA halen.

## Compositie

De opbouw volgt de conventies voor een `local-service-booking`-site: zie
[`../composition-local-service-booking-bambine.md`](../composition-local-service-booking-bambine.md)
voor de volledige motivatie per beslissing.
