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

| Rol | Kleur |
|---|---|
| Grond (crème) | `#fcf8f3` |
| Diep water (donkere secties) | `#10403e` |
| Teal (accenten, water) | `#2e706a` |
| Terracotta (enige actiekleur) | `#b15a41` |
| Aqua (baby) / blush (mama) / goud (kids) | `#8fc7c1` / `#eac3b6` / `#cf9a4f` |

Typografie: **Fraunces** (display, variabel — met SOFT- en WONK-as voor de zachte vorm)
en **Inter** (UI). Beide zelf gehost in `assets/fonts/`, dus geen verbinding met Google
tijdens het bezoek (AVG/GDPR + snelheid).

Iconen zijn echte SVG-iconen uit [Lucide](https://lucide.dev) (ISC) en
[Simple Icons](https://simpleicons.org) (CC0), samengevoegd tot één inline sprite.

Animaties: reveal-on-scroll, voortgangslijn in de tijdlijn, tellers, drijvende belletjes,
rimpelingen in het water, paginaovergangen via de View Transitions API. Alles valt stil bij
`prefers-reduced-motion: reduce`.

## Foto's toevoegen

De site is foto-gedreven opgebouwd. Elk beeldvlak is een `.photo`-blok met een
duotoonverloop in de merkkleuren als tijdelijke invulling; er zijn **14 slots**, elk
gemarkeerd met `<!-- FOTO-SLOT: … -->` in `src/`.

Een echte foto zet je erin met één custom property:

```html
<div class="photo ratio-4-5 blob-1" style="--img:url('assets/img/hero-baby.jpg')" …>
```

Het verloop blijft eronder staan als de foto nog laadt, en het icoontje in het midden
verdwijnt automatisch zodra `--img` gezet is. Pas ook de `aria-label` aan zodat die de
foto beschrijft.

## Nog na te kijken vóór livegang

- **Foto's** van de praktijk, de badruimte, Ine en de cadeauhoek.
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
