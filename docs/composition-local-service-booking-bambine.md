# Compositienota — Bambine (local-service-booking)

**Site shape:** `local-service-booking`, met een kleine `ecommerce-catalog`-annex (cadeaubon + webshop).
**Experience bar:** geen `competitor-experience-audit` beschikbaar voor deze vertical; gewerkt met de
per-shape conventies uit `vertical-site-conventions` en met wat publiek zichtbaar is bij vergelijkbare
babyspa's in Vlaanderen (Fresha-boekingen, prijstransparantie, FAQ-zwaar).
**Bron van de inhoud:** publiek vindbare gegevens van bambine.be (bambine.be zelf is vanuit deze
omgeving niet bereikbaar), aangevuld via zoekresultaten. Alles wat niet hard te verifiëren viel, staat
expliciet als "na te kijken voor livegang" op de pagina zelf.

---

## 1. Primaire taak: contact opnemen, straks boeken in GoHighLevel

De bezoeker is een ouder met een baby van enkele weken oud, vaak 's avonds op de telefoon.
De primaire taak is *een moment vastleggen*. De boekingstool komt later in GoHighLevel, dus
tot dan is bellen of mailen de actie die de site moet uitlokken.

- **Het telefoonnummer is de enige actie in de chrome**: een gouden knop met het nummer,
  op elke pagina, op elk schermformaat.
- De hero stuurt meteen door naar de reserveerpagina, met de tarievenpagina
  ernaast als secundaire stap voor wie eerst prijzen wil zien. Bellen blijft één klik weg
  in de chrome.
- **Sticky actiebalk** onderaan op mobiel (Bellen · Mailen) zodra de bezoeker voorbij de hero scrollt.
- Er is een eigen **reserveerpagina** die de hele stap draagt: hoe het gaat, wat je kan
  reserveren, het verloop van een sessie en wat je meebrengt. Bovenaan staat een gemarkeerd
  blok (`.ghl-slot`) precies waar het GHL-formulier of de agenda komt. Geen nepformulier in
  de tussentijd: dat zou aanvragen opslokken die nergens aankomen.
- De **shoppagina** draagt het tweede aankoopmoment (cadeaubon, pampertaart, geschenkje),
  met dezelfde constructie voor de bestelmodule.

## 2. Layoutregister en dichtheid

Register: *redactioneel, boetiek* — geen SaaS-airy landingspagina, maar ook niet de
storefront-dichtheid van een catalogus. Baby-wellness verkoopt rust; de pagina moet rust tonen
en tegelijk alle harde feiten binnen handbereik houden.

Het gangbare stramien (kop → drie kaartjes → iconen in cirkels → stats-strook → donkere
CTA-band) is bewust losgelaten: dat leest als een template. In de plaats: genummerde secties,
haarlijnen in plaats van kaders, een asymmetrisch raster van twaalf kolommen, beeld dat aan
één kant de bladspiegel uit loopt, het aanbod als afwisselende redactionele rijen, tarieven
als menukaart en één groot citaat in plaats van drie reviewkaartjes.

- **Boven de vouw op desktop**: één schermvullend beeld met daarop de kop, de lead, twee
  acties (reserveren, cadeaubonnen) en een regel met de vier harde feiten. Direct daaronder
  de vertrouwensstrook met diezelfde feiten uitgeschreven. Dat register is overgenomen van
  een babyspa die de klant mooi vond (bubbeline.be), maar dan in de eigen merkkleuren:
  een warme bruine sluier over de foto in plaats van blauw, en goud als enige actiekleur.
- Ruime witruimte, maar de informatie is dicht: prijzen, leeftijdsgrens, watertemperatuur en
  adres staan alle vier binnen één schermhoogte na de hero.
- Visueel register (kleur, type, radius) → `design-standards` / `creative-direction`.
  Hier vastgelegd: wit en crème als grond, donkerbruin als donkere ankers, goud als enige
  actiekleur, en een zachte tint per dienstfamilie. De merkkleuren (goud, lichtbruin, wit)
  komen van de klant zelf; goud is voor tekst naar `#8a6a35` gebracht om contrastvast te zijn.

## 3. Merchandising- en categorieoppervlak

- **Drie dienstfamilies** staan op de homepage als redactionele rijen (groot cijfer,
  boog-foto, tekst, vanafprijs), links en rechts afwisselend, en leiden alle drie naar hun
  anker op de tarievenpagina. Eén vlakke tier — geen mega-menu, geen facetten.
- De navigatie is teruggebracht tot vier bestemmingen: Tarieven, Reserveren, Shop, Contact.
  Dat maakt de twee handelingen (reserveren, bestellen) tot de ruggengraat van het menu.
- De **cadeaubon/webshop** is het vierde entreepunt, bewust apart als donkere band zodat
  het niet concurreert met de zorgdiensten maar wel zichtbaar blijft (het is het
  tweede-grootste aankoopmoment: kraamcadeau).
- Prijs is onderdeel van de merchandising: elke kaart toont "vanaf € 55" of eerlijk "op aanvraag".

## 4. Paden

| Pad | Status | Waar |
|---|---|---|
| Per persoon (baby / mama / kind) | **primair** | hero-tabs + hoofdnavigatie + dienstkaarten |
| Per dienst (hydrotherapie, Shantala, zwangerschapsmassage …) | **primair** | tarievenpagina met een anker per dienst |
| Per prijs | **primair** | de tarievenpagina draagt nu alle diensten, met menukaart per familie |
| Per gelegenheid (kraamcadeau, verjaardag) | secundair | shoppagina met cadeaubonnen en geschenkjes |
| Per locatie / route | secundair | contactpagina, footer, chrome |
| Zoeken | **afwezig** | correct voor deze shape: zes pagina's, geen catalogus |

## 5. Merkhouding, over de hele pagina

Warm, nabij, Vlaams, zonder zweverigheid. Die toon is doorgetrokken tot in de randen:
navigatie ("Kies je moment"), lege staten, formulierlabels ("Iets dat we moeten weten?"),
de bevestiging na verzenden en de footer. Beeldhouding is consequent documentair-warm:
geen illustratie-stijlbreuk halverwege. De nog lege fotovlakken zijn
bijna-monochrome linnenvlakken met korrel, dus ze vallen niet op als gekleurde blokken.

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
| Online agenda-integratie | uitgesteld: komt in GoHighLevel, plek staat klaar (`.ghl-slot`) |

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
  Invullen gebeurt per slot met `style="background-image:url('assets/img/….jpg')"`.
  Eén foto is al aangeleverd en staat in de hero en de galerij.
- **`design-standards`** — tokens staan in `assets/css/site.css` (sectie 1). Kleur, radius
  en schaal zijn daar centraal; niets is hardgecodeerd in de pagina's.
- **GoHighLevel** — `build.py` exporteert de pagina's als plakbare blokken in `ghl/`,
  met de stijl ingekapseld onder `.bambine-site`. Het boekingsformulier en de agenda worden
  daar opgezet en vervangen het `.ghl-slot`-blok op de contactpagina.
- **`seo-onpage`** — meta, canonical, OG, LocalBusiness/Service/FAQPage/BreadcrumbList-schema,
  sitemap en robots.txt staan klaar; nog te doen na livegang: echte OG-afbeelding en BTW-nummer.
