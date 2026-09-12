# Compositienota — Bambine (local-service-booking)

**Site shape:** `local-service-booking`, met een kleine `ecommerce-catalog`-annex (cadeaubon + webshop).
**Experience bar:** geen `competitor-experience-audit` beschikbaar voor deze vertical; gewerkt met de
per-shape conventies uit `vertical-site-conventions` en met wat publiek zichtbaar is bij vergelijkbare
babyspa's in Vlaanderen (Fresha-boekingen, prijstransparantie, FAQ-zwaar).
**Bron van de inhoud:** publiek vindbare gegevens van bambine.be (bambine.be zelf is vanuit deze
omgeving niet bereikbaar), aangevuld via zoekresultaten. Alles wat niet hard te verifiëren viel, staat
expliciet als "na te kijken voor livegang" op de pagina zelf.

---

## 1. Primaire taak: boeken, meteen en dominant

De bezoeker is een ouder met een baby van enkele weken oud, vaak 's avonds op de telefoon.
De primaire taak is *een moment vastleggen*, niet *lezen over hydrotherapie*.

- De **boekingskaart staat in de hero**, boven de vouw, op alle schermformaten: drie tabs
  (Baby / Mama / Kids), per tab twee tot drie sessies met duur én prijs, en één primaire actie.
- **Eén primaire CTA** per scherm ("Afspraak aanvragen"). Bellen staat ernaast als secundaire,
  want voor deze doelgroep is telefoon nog altijd een conversiekanaal.
- **Sticky actiebalk** onderaan op mobiel (Bellen · Afspraak) zodra de bezoeker voorbij de hero scrollt.
- Elke onderpagina heeft de boekingsactie in de page-hero en opnieuw onderaan.

## 2. Layoutregister en dichtheid

Register: *image-led, warm-editorial* — geen SaaS-airy landingspagina, maar ook niet de
storefront-dichtheid van een catalogus. Baby-wellness verkoopt rust; de pagina moet rust tonen
en tegelijk alle harde feiten binnen handbereik houden.

- **Boven de vouw op desktop: 3 modules** — kop + lead, boekingskaart, fotocollage met
  36 °C-badge; direct daaronder de vertrouwensstrook met vier feiten.
- Ruime witruimte, maar de informatie is dicht: prijzen, leeftijdsgrens, watertemperatuur en
  adres staan alle vier binnen één schermhoogte na de hero.
- Visueel register (kleur, type, radius) → `design-standards` / `creative-direction`.
  Hier vastgelegd: warm crème als grond, diep teal als donkere ankers, terracotta als enige
  actiekleur, en een tint per dienstfamilie (aqua = baby, blush = mama, goud = kids).

## 3. Merchandising- en categorieoppervlak

- **Drie dienstfamilies** worden als volwaardige kaarten getoond (foto, drie bullets,
  vanafprijs, duur), elk met een eigen detailpagina. Eén vlakke tier — geen mega-menu,
  geen facetten: bij drie diensten is dat overkill.
- De **cadeaubon/webshop** is het vierde entreepunt, bewust apart als donkere band zodat
  het niet concurreert met de zorgdiensten maar wel zichtbaar blijft (het is het
  tweede-grootste aankoopmoment: kraamcadeau).
- Prijs is onderdeel van de merchandising: elke kaart toont "vanaf € 55" of eerlijk "op aanvraag".

## 4. Paden

| Pad | Status | Waar |
|---|---|---|
| Per persoon (baby / mama / kind) | **primair** | hero-tabs + hoofdnavigatie + dienstkaarten |
| Per dienst (hydrotherapie, Shantala, zwangerschapsmassage …) | **primair** | detailpagina's, tarievenpagina |
| Per prijs | secundair | eigen tarievenpagina, prijs herhaald op elke dienstpagina |
| Per gelegenheid (kraamcadeau, verjaardag) | secundair | cadeaubonband, kids-pagina |
| Per locatie / route | secundair | contactpagina, footer, chrome |
| Zoeken | **afwezig** | correct voor deze shape: zes pagina's, geen catalogus |

## 5. Merkhouding, over de hele pagina

Warm, nabij, Vlaams, zonder zweverigheid. Die toon is doorgetrokken tot in de randen:
navigatie ("Kies je moment"), lege staten, formulierlabels ("Iets dat we moeten weten?"),
de bevestiging na verzenden en de footer. Beeldhouding is consequent documentair-warm:
geen illustratie-stijlbreuk halverwege. De fotovlakken zijn duotoonverlopen in de merkkleuren
met korrel — bewust ontworpen, geen grijze blokken — zodat het beeldritme nu al klopt.

## 6. Vertrouwens- en conversiesignalen

Aanwezig: watertemperatuur (36 °C, expliciet en herhaald), leeftijdsgrens (2 weken – ± 9 maanden,
inclusief prematuren-regel), één gezin per sessie, prijstransparantie, adres + regio,
telefoon als click-to-call, cadeaubon-voorwaarden, wat meebrengen, ziekte/verzetten,
persoon achter de praktijk (Ine), FAQ op twee plaatsen.

Eerlijkheidsgrens voor deze demo: reviews staan als **voorbeeldtekst** gemarkeerd, het
boekingsformulier zegt bij verzenden expliciet dat er niets verstuurd wordt, en bij de
tarieven staat welke bedragen publiek gevonden zijn en welke nog ingevuld moeten worden.
Telefoon, e-mail en adres zijn wél echt.

## 7. Synthesecheck (conventies van deze vertical)

| Conventie | Status |
|---|---|
| Boekingsactie boven de vouw | aanwezig |
| Click-to-call in de chrome | aanwezig |
| Prijzen publiek, zonder formulier | aanwezig (gedeeltelijk "op aanvraag", eerlijk gelabeld) |
| Adres + regio + route | aanwezig |
| Openingsmomenten | **deels** — enkel "op afspraak"; echte uren ontbreken (niet publiek vindbaar) |
| Reviews / sociale bewijskracht | aanwezig, als voorbeeld gemarkeerd → vervangen door echte Google-reviews |
| FAQ | aanwezig (6 vragen, ook als FAQPage-schema) |
| Cadeaubon | aanwezig |
| Persoon achter de praktijk | aanwezig |
| Wat verwachten / verloop van een sessie | aanwezig (tijdlijn met 5 stappen) |
| Foto's van de ruimte | **slots klaar**, echte foto's nog aan te leveren |
| Online agenda-integratie | afwezig — bewuste keuze: demo zonder backend |

Twee items niet volledig: openingsuren (ontbrekende data) en echte foto's (aangeleverd door de klant).
Beide zijn data, geen compositiefouten — de modules staan er en zijn één invulbeurt van klaar.

## Wedge

Concurrerende babyspa-sites in de regio leunen op templates: stockfoto's, prijzen achter een
mailtje, en een hero vol sfeerwoorden. De wedge hier is **radicale duidelijkheid in een zachte
vorm**: prijs, duur, leeftijd en watertemperatuur staan in het eerste scherm, het verloop van
een sessie staat minuut per minuut uitgeschreven, en de toon blijft die van iemand die naast je
staat in plaats van van een wellnessbrochure.

## Hand-off

- **Foto's** — 14 slots, elk met een `<!-- FOTO-SLOT -->`-commentaar en de gewenste beeldinhoud.
  Invullen gebeurt per slot met `style="--img:url('assets/img/….jpg')"`.
- **`design-standards`** — tokens staan in `bambine/assets/css/site.css` (sectie 1). Kleur, radius
  en schaal zijn daar centraal; niets is hardgecodeerd in de pagina's.
- **`frontend-component-build`** — het boekingsformulier is nu een demo; koppelen aan de echte
  agenda (Fresha of GoHighLevel) is het enige stuk dat nog backend nodig heeft.
- **`seo-onpage`** — meta, canonical, OG, LocalBusiness/Service/FAQPage/BreadcrumbList-schema,
  sitemap en robots.txt staan klaar; nog te doen na livegang: echte OG-afbeelding en BTW-nummer.
