# Bambine in GoHighLevel zetten

> **Het makkelijkst:** open `Bambine-GHL-codeboek.pdf`. Daarin staat per pagina elke sectie
> met de naam, wat ze doet en de volledige code, klaar om over te nemen. Opnieuw maken na een
> aanpassing: `python3 build.py && python3 maak_codeboek.py` (vraagt `pip install reportlab`).

Deze map wordt gegenereerd door `python3 build.py` en bevat per pagina één blok dat je
rechtstreeks in de GHL-pagebuilder kan plakken.

| Bestand | Wat het is |
|---|---|
| `index.html`, `tarieven.html`, `reserveren.html`, `shop.html`, `contact.html` | Eén zelfstandig blok per pagina: stijl, iconen, foto en script zitten erin (route A) |
| `blokken/*.html` | Dezelfde pagina's, maar alleen de opmaak, zonder stijl en script (route B) |
| `_header-code.html` | De webfonts, voor Tracking Code → Header |
| `_stijl.css` | De volledige stijl inclusief de foto's, voor Settings → Custom CSS |
| `_stijl.min.css` | Dezelfde stijl, ingekrompen en zonder de foto's (31 kB in plaats van 53 kB) |
| `_fotos.css` | Enkel de foto's als data-URI, hoort bij `_stijl.min.css` |
| `_script.js` | Het volledige script als los bestand |
| `_footer-code.html` | Hetzelfde script, al in `<script>`-tags, voor Tracking Code → Footer |
| `secties/<pagina>/*.html` | Dezelfde pagina's, opgesplitst in losse secties (route C) |
| `globaal/*.html` | De vier blokken die op elke pagina terugkomen (stijl en script, kop, actiebalk, footer), om als globale sectie te bewaren |
| `Bambine-GHL-codeboek.pdf` | Alles hierboven als één document: per pagina elke sectie met naam, uitleg en code |
| `_proefpagina.html` | Een blok in een vreemde omgeving, om te controleren dat de stijl niet uitlekt |

## De vijf pagina's

Vul in de pagebuilder per pagina deze twee velden in. De paden zijn al in de blokken
verwerkt: de navigatie, de knoppen en de footer linken naar `/tarieven`, `/reserveren`,
enzovoort, dus je hoeft geen enkele link aan te passen.

| Bestand in deze map | Paginanaam | Path |
|---|---|---|
| `index.html` | Home | `/` (leeg laten) |
| `tarieven.html` | Tarieven | `tarieven` |
| `reserveren.html` | Reserveren | `reserveren` |
| `shop.html` | Shop | `shop` |
| `contact.html` | Contact | `contact` |

Title en meta description per pagina staan bovenaan elk bestand in het HTML-commentaar;
die horen in de pagina-instellingen (SEO), niet in het blok zelf.

Geneste paden worden ondersteund. Wil je later bijvoorbeeld `diensten/babywellness`, pas
dan het path in GHL aan én de bijbehorende regel in `GHL_PADEN` in `build.py`, en bouw
opnieuw. Dan kloppen de links in alle blokken weer.

## Route A — snelst, per pagina één blok

1. Maak in GHL een pagina aan met de paginanaam en het path uit de tabel hierboven.
2. Sleep één **Custom Code**- of **HTML**-element over de volledige breedte van de sectie.
   Zet de sectie op volle breedte en haal de standaard padding weg, anders staat er een
   marge rond het blok.
3. Plak de volledige inhoud van het bijbehorende bestand uit deze map.
4. Zet **Page title** en **Meta description** in de pagina-instellingen. De juiste teksten
   staan bovenaan elk bestand in het HTML-commentaar.
5. Herhaal per pagina. De links in de blokken wijzen al naar de paden uit de tabel, dus
   zolang je die paden aanhoudt werkt de navigatie meteen.

## Route B — netter, stijl en script één keer site-breed

Zo staat de stijl maar één keer op de site in plaats van vijf keer, en laden de pagina's
sneller.

1. **Header.** Plak `_header-code.html` in **Settings → Tracking Code → Header**. Dat zijn
   enkel de twee lettertypen.
2. **Stijl.** Plak de volledige inhoud van `_stijl.css` in **Settings → Custom CSS**. De
   foto's zitten er als data-URI in, dus je hoeft niets te uploaden.
3. **Script.** Plak `_footer-code.html` in **Settings → Tracking Code → Footer**. Dat is
   `_script.js` met de `<script>`-tags er al omheen.
4. **Per pagina.** Plak het bestand uit `blokken/` in een Custom Code-element. Dat is enkel
   `<div class="bambine-site"> … </div>` — geen stijl, geen script.

**Komt maar een deel van de opmaak door?** Dan is de stijl onderweg afgekapt: het
custom-CSS-veld van GHL heeft een limiet. Je herkent het hieraan dat koppen en knoppen wel
kloppen, maar de navigatie, de hero en de rest niet. Plak dan `_stijl.min.css` in plaats van
`_stijl.css`, en zet `_fotos.css` er als tweede blok onder (of laat dat weg: dan valt de
galerijfoto terug op een kleurvlak). Controleer na het plakken of de laatste regel van het
veld nog `display:none!important}}` is; staat daar iets anders, dan is er alsnog geknipt en
kan je beter route A nemen, want daar zit de stijl in het blok zelf.

Werkt het script niet? Controleer dan of de footer-code op paginaniveau overschreven wordt;
in GHL kan een pagina zijn eigen tracking code hebben die de site-brede vervangt.

## Route C — per sectie een blok

Handig als je de pagina in GHL uit losse secties wil opbouwen, bijvoorbeeld om er later
tussen te schuiven of om een sectie op meerdere pagina's te hergebruiken. **Je hebt hiervoor
geen Custom CSS nodig**: het eerste blok draagt de stijl en het script voor de hele pagina.

1. Plak `secties/<pagina>/00-kop-en-navigatie.html` als **eerste** blok op de pagina. Daarin
   zitten de stijl, de iconensprite en het script. Zonder dit blok blijft de rest kaal.
2. Plak daarna per GHL-sectie één bestand uit dezelfde map, in de volgorde van de nummers.
3. Zet elke GHL-sectie op volle breedte zonder padding: de blokken brengen hun eigen
   achtergrond en witruimte mee.

Staat `_header-code.html` al in de tracking code, dan laden de lettertypen sneller, maar
nodig is het niet: blok 00 haalt ze zelf op.

De homepagina bestaat uit deze blokken:

| Bestand | Wat het is |
|---|---|
| `00-kop-en-navigatie.html` | Navigatie en mobiel menu. **Hoort op elke pagina**, want de iconensprite zit erin |
| `01-hero.html` | De hero: titel, tekst, reserveerknop en cadeaubonknop. **Zonder foto**: die zet je als achtergrond van de GHL-sectie |
| `02-in-het-kort.html` | De feitenrij met 36 °C, leeftijd, één gezin, vanafprijs |
| `03-warm-water.html` | Waarom warm water werkt, met de streepjeslijst |
| `04-aanbod.html` | De drie diensten als redactionele rijen |
| `05-verloop.html` | Het verloop van een sessie in vijf stappen |
| `06-over-ine.html` | De donkere band met het citaat van Ine |
| `07-de-praktijk.html` | De galerij met drie bogen en de waterlijn |
| `08-wat-ouders-zeggen.html` | Het grote citaat |
| `09-cadeaubon.html` | De cadeaubonband |
| `10-vragen-contact.html` | De FAQ naast de contactgegevens |
| `98-actiebalk-mobiel.html` | De vaste balk onderaan op mobiel. Optioneel |
| `99-footer.html` | De footer |

De andere pagina's zijn op dezelfde manier opgesplitst in `secties/tarieven/`,
`secties/reserveren/`, `secties/shop/` en `secties/contact/`.

## Route D — globale secties (wat het codeboek volgt)

1. Maak de vier blokken uit `globaal/` één keer aan en bewaar ze in GHL als **globale sectie**.
2. Zet op elke pagina bovenaan `00-stijl-en-script` en `01-kop-en-navigatie`, daaronder de
   secties `01`, `02`, … uit `secties/<pagina>/` (niet het blok `00` uit die map), en onderaan
   `98-actiebalk-mobiel` en `99-footer`.
3. De actieve pagina in de navigatie wordt door het script bepaald, dus één globale navigatie
   volstaat voor alle pagina's.

De blokken dragen geen foto's: die zet je in GHL zelf. Bij de hero als achtergrond van de
sectie, bij de andere beeldvlakken met `style="background-image:url('…')"` op het
`<div class="fig …">` onder het `FOTO-SLOT`-commentaar.

## Goed om te weten

- **Alles zit ingekapseld onder `.bambine-site`.** De stijl raakt de rest van de
  GHL-pagina niet, en omgekeerd overschrijven de thema-instellingen van GHL de pagina niet.
  Open `_proefpagina.html` in een browser om dat te zien.
- **Boekingswidgets zitten er bewust niet in.** Op `reserveren.html` staat een blok met een
  stippellijn (`.ghl-slot`) op de plek waar het formulier of de agenda hoort, en op
  `shop.html` staat hetzelfde blok voor de bestelmodule. Vervang die blokken door de
  embed-elementen uit GHL.
- **De foto zit als data-URI in het blok**, dus je hoeft niets te uploaden. Wil je liever
  de GHL-mediabibliotheek gebruiken: zoek in het bestand naar `--f-baby-knuffel` en zet
  daar de URL van de geüploade foto neer.
- **Webfonts** komen via een `@import` van Google Fonts. Voor strikte AVG/GDPR-naleving kan
  je de bestanden uit `../assets/fonts/` naar de mediabibliotheek van GHL uploaden en de
  `@import`-regel vervangen door `@font-face`-regels met die URL's.
- **De foto van de hero zet je in GoHighLevel zelf**: sectie-instellingen → Background →
  Image, op de sectie waar `01-hero.html` in staat. Het blok is doorzichtig, dus die foto
  komt er gewoon doorheen. De donkere sluier eroverheen houdt de witte tekst leesbaar; bij
  een heel lichte foto mag je in de stijl `.hero-scrim` wat donkerder zetten.
- **In de losse secties schuift de hero niet onder de navigatie** (dat kan niet, want de
  sectie-achtergrond van GHL loopt niet mee omhoog). In de pagina-in-één-blok (route A) wel.
- **De hero schuift bewust onder de navigatie**, zodat de kop doorzichtig over de foto staat.
  Zet die GHL-sectie dus op volle breedte zonder padding. Loopt het in GHL toch niet mooi
  samen, zet dan op het hero-blok `style="--header-h:0px"`: dan begint de foto netjes onder
  de navigatie in plaats van eronder door te lopen.
- **De vermelding dat dit een concept is** staat nu enkel nog in de footer, in de onderste
  regel. Voor livegang haal je die regel weg.
- Na elke aanpassing in `src/` of `assets/`: `python3 build.py` opnieuw draaien en de
  blokken opnieuw plakken.
