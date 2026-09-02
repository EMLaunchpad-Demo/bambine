# Terrakota — website concept

Conceptvoorstel voor een nieuwe website van **Terrakota**, een privé wellnessparadijs in
een botanische tuin in Diepenbeek (Limburg). Gemaakt door **EM Launchpad** als demo.

> Dit is een conceptontwerp, geen officiële Terrakota-website. Dat staat ook duidelijk in
> de balk bovenaan en in de footer van de pagina.

## Live preview

Bekijk de demo (deelbare link, licht + donker thema, responsive):
https://claude.ai/code/artifact/f24cea8e-0ca6-4057-86a9-9bfd324711fc

## Wat zit erin

`index.html` — één volledige, zelfstandige landingspagina. Alles zit inline (CSS + JS),
geen build-stap, geen externe libraries. Enkel de webfonts komen van Google Fonts.

Secties:

- **Hero** — Kota-hexagon met sfeergloed en zwevende faciliteitenkaartjes
- **Faciliteiten** — 2 sauna's, hot tub, jacuzzi, verwarmd zwembad, botanische tuin, Finse Kota
- **Aarde · Water · Vuur · Adem** — de vier elementen als rode draad
- **Verblijf** — de vakantiewoning (capaciteit, seizoen, richtprijs)
- **Beleving** — yoga (Somatic, Nidra, Kundalini, Tantra), meditatie, breathwork, rituelen, belevingsdagen
- **Samen eten** — maaltijden, grillen in de Kota, kookworkshops
- **Zakelijk** — Business Incentive Centre / teambuilding
- **Sfeer, reviews, FAQ, contact** en footer

## Ontwerp

Gebouwd op de EM Launchpad-designpatronen (sticky nav, dark panels, reveal-on-scroll,
FAQ-accordion, geanimeerde cijfers), in de **echte merkkleuren van terrakota.be**:
houtskoolgrijs + limoengroen. Dark-first (zoals de huidige site), met een lichte
thema-toggle.

| Rol | Kleur |
|-----|-------|
| Primair accent (limoengroen) | `#aecb3a` |
| Helder accent | `#c4dd60` |
| Secundair (olijfgroen) | `#7c9a45` |
| Neutraal grijs | `#9aa196` |
| Grond (donker) | `#232524` / `#1c1e1d` |
| Tekst | `#f3f5ee` op donker |

Typografie: **Spectral** (display serif) + **Outfit** (UI/tekst).

## Foto's toevoegen (belangrijk)

De pagina is foto-gedreven opgebouwd. Elk fotovlak is een `.photo`-blok met een tijdelijke
groen/grijze gradient als placeholder. Er zijn slots in de **hero**, bij **Verblijf** en in de
**Foto's**-galerij (elk gemarkeerd met `<!-- FOTO-SLOT -->` in `index.html`).

Een echte foto plaats je door de gradient te vervangen door een achtergrondafbeelding, bv.:

```html
<div class="photo" style="background-image:url('foto-zwembad.jpg')"> ... </div>
```

> In de gedeelde previewlink kunnen externe afbeeldingen niet laden (sandbox); zet foto's in
> het bestand (of embed ze als data-URI) om ze overal te tonen. Lever je de echte
> Terrakota-foto's aan, dan zetten we ze er direct in.

## Nog aan te vullen

- **Foto's** van het domein (tuin, zwembad, sauna's, Kota, interieur).
- Reviews zijn voorbeeldteksten — te vervangen door echte gastenreacties.
- Contactgegevens (Lutselusstraat 156, 3590 Diepenbeek · +32 468 19 13 33 · info@terrakota.be)
  komen uit publiek beschikbare bronnen; graag verifiëren voor livegang.

## Deployen naar GoHighLevel

De pagina is opgebouwd volgens de EM Launchpad-conventies en kan als custom HTML-blok in
GoHighLevel geplakt worden. Voor GHL: laat de `<!DOCTYPE>`, `<html>`, `<head>` en `<body>`
weg en plak enkel de inhoud daarbinnen; SEO-metatags stel je in via de pagina-instellingen
van GHL.
