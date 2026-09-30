#!/usr/bin/env python3
"""Maakt de vijf e-mails voor de afspraak-automatisaties in GoHighLevel.

Elke e-mail is een volledig HTML-bestand: openen, alles kopiëren en plakken in de
code-editor van de e-mail in GoHighLevel. Onderwerp en voorvertoning staan bovenaan
als commentaar.

Opbouw voor e-mailprogramma's: tabellen, inline stijl, max. 600 px breed, een
knop die ook in Outlook werkt. Merge-velden komen uitsluitend uit de lijst van de
servicekalender (serviceBooking.*). De lus over de diensten staat binnen één cel,
zodat een editor die de HTML opschoont de {{#each}} niet uit de tabel duwt.

    python3 emails/maak.py
"""

from __future__ import annotations

import pathlib
import sys

HIER = pathlib.Path(__file__).parent

# --- vaste gegevens ---------------------------------------------------------
TEL = "+32 474 78 26 91"
TEL_HREF = "+32474782691"
MAIL = "info@bambine.be"
ADRES = "Michiel Jansplein 28/b2, 3920 Lommel"
BOEKEN = "https://api.leadconnectorhq.com/booking/bambine-eduh49980fd"
ROUTE = "https://www.google.com/maps/search/?api=1&query=Michiel+Jansplein+28+3920+Lommel"
REVIEW = "https://www.facebook.com/BambineBabywellness/reviews"
CADEAUBON = "https://link.fastpaydirect.com/gift-card/6ab3febee345593058111650"
INSTA = "https://www.instagram.com/bambine.babywellness/"
FB = "https://www.facebook.com/BambineBabywellness/"
# Logo zoals het nu op bambine.be staat. Beter: upload het in de mediabibliotheek
# van GoHighLevel en zet die URL hier.
LOGO = "https://bambine.be/wp-content/uploads/2024/10/bambine_logo_transparant.png"

# --- kleuren en letters (zoals de site) -------------------------------------
INK = "#241d18"
INK2 = "#5a4e44"
MUTED = "#776a5e"
GOLD = "#c8aa66"
GOLD_INK = "#8a6a35"
SHELL = "#fbf8f3"
LINE = "#eadfcc"
SERIF = "'Fraunces', Georgia, 'Times New Roman', serif"
SANS = "'Mulish', Arial, Helvetica, sans-serif"

# --- merge-velden -----------------------------------------------------------
DATUM = "{{serviceBooking.day_of_week}} {{serviceBooking.only_start_date}}"
UUR = "{{serviceBooking.only_start_time}}"


def p(tekst: str, *, kleur: str = INK2, grootte: int = 16, marge: str = "0 0 16px") -> str:
    return (
        f'<p style="margin:{marge};font-family:{SANS};font-size:{grootte}px;'
        f'line-height:1.65;color:{kleur};">{tekst}</p>'
    )


def knop(tekst: str, href: str) -> str:
    """Gouden knop met donkere tekst; de tabel zorgt dat hij ook in Outlook werkt."""
    return f"""<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:8px 0 8px;">
  <tr>
    <td bgcolor="{GOLD}" style="background:{GOLD};border-radius:2px;">
      <a href="{href}" target="_blank" style="display:inline-block;padding:15px 28px;font-family:{SANS};font-size:13px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:{INK};text-decoration:none;">{tekst}</a>
    </td>
  </tr>
</table>"""


def tekstlink(tekst: str, href: str) -> str:
    return (
        f'<a href="{href}" target="_blank" style="color:{INK};font-weight:700;'
        f'text-decoration:underline;text-decoration-color:{GOLD};">{tekst}</a>'
    )


def kop(label: str, titel: str) -> str:
    return f"""<p style="margin:0 0 12px;font-family:{SANS};font-size:11px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:{GOLD_INK};">{label}</p>
<h1 style="margin:0 0 20px;font-family:{SERIF};font-size:32px;line-height:1.15;font-weight:400;color:{INK};">{titel}</h1>"""


def tussenkop(titel: str) -> str:
    return (
        f'<h2 style="margin:28px 0 12px;font-family:{SERIF};font-size:21px;line-height:1.25;'
        f'font-weight:400;color:{INK};">{titel}</h2>'
    )


def gegevens(met_details: bool = True) -> str:
    """Blok met de geboekte dienst(en), datum, uur en adres."""
    if met_details:
        dienst = (
            f'<p style="margin:0 0 14px;font-family:{SANS};font-size:16px;line-height:1.55;color:{INK};">'
            f'<strong style="font-family:{SERIF};font-size:19px;font-weight:400;">{{{{this.name}}}}</strong><br>'
            f'<span style="font-size:14px;color:{MUTED};">{{{{this.duration}}}} · bij {{{{this.user.first_name}}}}'
            f" · {{{{this.price}}}}</span></p>"
        )
    else:
        dienst = (
            f'<p style="margin:0 0 10px;font-family:{SERIF};font-size:19px;line-height:1.4;color:{INK};">'
            f"{{{{this.name}}}}</p>"
        )
    rij = lambda k, v: (  # noqa: E731
        f'<tr><td style="padding:10px 0;border-top:1px solid {LINE};font-family:{SANS};font-size:11px;'
        f'font-weight:700;letter-spacing:2px;text-transform:uppercase;color:{MUTED};width:110px;vertical-align:top;">{k}</td>'
        f'<td style="padding:10px 0;border-top:1px solid {LINE};font-family:{SANS};font-size:16px;'
        f'line-height:1.5;color:{INK};vertical-align:top;">{v}</td></tr>'
    )
    return f"""<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:8px 0 8px;background:{SHELL};border:1px solid {LINE};">
  <tr>
    <td style="padding:22px 24px 8px;">
      {{{{#each serviceBooking.services}}}}
      {dienst}
      {{{{/each}}}}
    </td>
  </tr>
  <tr>
    <td style="padding:0 24px 14px;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
        {rij("Datum", DATUM)}
        {rij("Uur", UUR)}
        {rij("Waar", "Bambine, " + ADRES + "<br>in galerij Vivaldi")}
      </table>
    </td>
  </tr>
</table>"""


def lijst(items: list[str]) -> str:
    rijen = "".join(
        f'<tr><td style="width:26px;vertical-align:top;padding:9px 0;">'
        f'<div style="width:16px;height:1px;background:{GOLD};margin-top:12px;font-size:0;line-height:0;">&nbsp;</div></td>'
        f'<td style="padding:6px 0;font-family:{SANS};font-size:15px;line-height:1.6;color:{INK2};">{i}</td></tr>'
        for i in items
    )
    return f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 8px;">{rijen}</table>'


GROET = p("Tot binnenkort,<br><span style=\"font-family:" + SERIF + ";font-size:19px;color:" + INK + ";\">Ine van Bambine</span>", marge="28px 0 0")


def layout(*, onderwerp: str, voorvertoning: str, inhoud: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="nl-BE" xmlns="http://www.w3.org/1999/xhtml">
<head>
<!-- Onderwerp: {onderwerp}
     Voorvertoning: {voorvertoning}
     Kopieer dit hele bestand in de code-editor van de e-mail in GoHighLevel. -->
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="x-apple-disable-message-reformatting">
<meta name="color-scheme" content="light">
<meta name="supported-color-schemes" content="light">
<title>{onderwerp}</title>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400&family=Mulish:wght@400;700&display=swap" rel="stylesheet">
<style>
  body {{ margin:0; padding:0; background:{SHELL}; }}
  a {{ color:{INK}; }}
  @media only screen and (max-width: 620px) {{
    .kaart {{ width:100% !important; }}
    .binnen {{ padding-left:22px !important; padding-right:22px !important; }}
    h1 {{ font-size:27px !important; }}
  }}
</style>
</head>
<body style="margin:0;padding:0;background:{SHELL};">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;mso-hide:all;">{voorvertoning}&#8199;&#65279;&#847;&#8199;&#65279;&#847;&#8199;&#65279;&#847;&#8199;&#65279;&#847;</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="{SHELL}" style="background:{SHELL};">
  <tr>
    <td align="center" style="padding:32px 12px;">
      <table role="presentation" class="kaart" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px;background:#ffffff;border:1px solid {LINE};">
        <tr>
          <td align="center" style="padding:30px 20px 18px;border-bottom:1px solid {GOLD};">
            <a href="https://bambine.be" target="_blank"><img src="{LOGO}" width="112" height="112" alt="Bambine, babywellness and more" style="display:block;border:0;width:112px;height:112px;"></a>
          </td>
        </tr>
        <tr>
          <td class="binnen" style="padding:36px 44px 40px;">
{inhoud}
          </td>
        </tr>
        <tr>
          <td class="binnen" align="center" style="padding:26px 44px 30px;background:#42342a;">
            <p style="margin:0 0 6px;font-family:{SERIF};font-size:18px;color:#ffffff;">Bambine babywellness &amp; mamazorg</p>
            <p style="margin:0 0 12px;font-family:{SANS};font-size:13px;line-height:1.6;color:#e9e1d5;">{ADRES} · galerij Vivaldi<br>
              <a href="tel:{TEL_HREF}" style="color:#e9e1d5;text-decoration:none;">{TEL}</a> · <a href="mailto:{MAIL}" style="color:#e9e1d5;text-decoration:none;">{MAIL}</a></p>
            <p style="margin:0;font-family:{SANS};font-size:12px;font-weight:700;letter-spacing:2px;text-transform:uppercase;">
              <a href="{INSTA}" target="_blank" style="color:{GOLD};text-decoration:none;">Instagram</a>
              <span style="color:#8c7b6a;">&nbsp;·&nbsp;</span>
              <a href="{FB}" target="_blank" style="color:{GOLD};text-decoration:none;">Facebook</a>
            </p>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
</body>
</html>
"""


MEEBRENGEN = (
    "<strong style=\"color:" + INK + ";\">Kom je voor babywellness?</strong> Breng de luiertas mee met een "
    "schone luier, propere kleertjes en eventueel wat eten. Voor massageolie, een floatband, "
    "handdoeken, tetradoeken en een zwemluier zorgt Bambine."
)
AFZEGGEN = (
    "<strong style=\"color:" + INK + ";\">Kan je toch niet komen?</strong> Verwittig zo snel mogelijk en "
    f"minstens 24 uur op voorhand, enkel telefonisch op <a href=\"tel:{TEL_HREF}\" style=\"color:{INK};\">{TEL}</a>."
)
BETALEN = "<strong style=\"color:" + INK + ";\">Betalen</strong> doe je cash of met Payconiq. Bancontact is er niet."

EMAILS = {
    "01-afspraak-bevestigd.html": dict(
        onderwerp="Je afspraak bij Bambine is bevestigd",
        voorvertoning=f"{DATUM} om {UUR} in galerij Vivaldi, Lommel.",
        inhoud="\n".join([
            kop("Afspraak bevestigd", "Fijn, je moment<br>staat vast"),
            p("Hallo,"),
            p("Bedankt voor je reservatie bij Bambine. Hieronder vind je alles op een rij. "
              "Ine kijkt ernaar uit om jullie te ontvangen."),
            gegevens(),
            knop("Route plannen", ROUTE),
            tussenkop("Goed om te weten"),
            lijst([
                MEEBRENGEN,
                "Geef je baby vooraf eventueel nog te eten en laat hem een dutje doen: "
                "goed uitgeslapen geniet je kleintje extra.",
                BETALEN,
                AFZEGGEN,
            ]),
            GROET,
        ]),
    ),
    "02-annulering.html": dict(
        onderwerp="Je afspraak bij Bambine is geannuleerd",
        voorvertoning=f"Je afspraak van {DATUM} om {UUR} gaat niet door.",
        inhoud="\n".join([
            kop("Afspraak geannuleerd", "Je afspraak<br>gaat niet door"),
            p("Hallo,"),
            p(f"Je afspraak bij Bambine van {DATUM} om {UUR} is geannuleerd. Het ging om:"),
            gegevens(met_details=False),
            p("Wil je een nieuw moment kiezen? Dat kan meteen online, of bel Ine op "
              f'<a href="tel:{TEL_HREF}" style="color:{INK};">{TEL}</a>.', marge="16px 0 16px"),
            knop("Een nieuw moment kiezen", BOEKEN),
            p("Heb je deze afspraak niet zelf geannuleerd? Laat het ons dan zeker weten via "
              f'{tekstlink(MAIL, "mailto:" + MAIL)} of telefonisch.', grootte=14, kleur=MUTED, marge="24px 0 0"),
            GROET,
        ]),
    ),
    "03-opnieuw-inplannen.html": dict(
        onderwerp="Je afspraak bij Bambine is verplaatst",
        voorvertoning=f"Je nieuwe moment: {DATUM} om {UUR}.",
        inhoud="\n".join([
            kop("Afspraak verplaatst", "Je afspraak heeft<br>een nieuw moment"),
            p("Hallo,"),
            p("Je afspraak bij Bambine is verplaatst. Dit zijn de nieuwe gegevens:"),
            gegevens(),
            knop("Route plannen", ROUTE),
            tussenkop("Past dit toch niet?"),
            p("Bel Ine zo snel mogelijk en minstens 24 uur op voorhand op "
              f'<a href="tel:{TEL_HREF}" style="color:{INK};">{TEL}</a>. Afzeggen kan enkel telefonisch.'),
            GROET,
        ]),
    ),
    "04-herinnering.html": dict(
        onderwerp="Tot binnenkort bij Bambine",
        voorvertoning=f"Een herinnering aan je afspraak op {DATUM} om {UUR}.",
        inhoud="\n".join([
            kop("Herinnering", "Tot binnenkort<br>bij Bambine"),
            p("Hallo,"),
            p("Een kleine herinnering aan je afspraak. Ine maakt alles voor jullie klaar."),
            gegevens(),
            knop("Route plannen", ROUTE),
            tussenkop("Vergeet niet"),
            lijst([
                MEEBRENGEN,
                "<strong style=\"color:" + INK + ";\">Is je baby ziek?</strong> Voelt je baby zich niet lekker "
                "of is hij wat koortsig, of kreeg hij net een prikje bij de dokter? Dan kom je beter niet. "
                "Na een prikje wacht je best een drietal dagen.",
                BETALEN,
                AFZEGGEN,
            ]),
            GROET,
        ]),
    ),
    "05-opvolging-review.html": dict(
        onderwerp="Bedankt voor je bezoek aan Bambine",
        voorvertoning="Hoe vond je het? We horen het graag.",
        inhoud="\n".join([
            kop("Bedankt", "Bedankt voor<br>jullie bezoek"),
            p("Hallo,"),
            p("Het was fijn om jullie te ontvangen bij Bambine. We hopen dat jullie er echt van "
              "genoten hebben."),
            p("Wil je in een paar woorden vertellen hoe je het vond? Andere ouders hebben er veel "
              "aan, en voor Ine betekent het veel."),
            knop("Schrijf een review", REVIEW),
            tussenkop("Nog eens langskomen?"),
            p(f"Je volgende moment reserveer je zo: {tekstlink('reserveer online', BOEKEN)}. "
              f"Of verras iemand met een {tekstlink('cadeaubon', CADEAUBON)}: een origineel cadeau "
              "voor mama, papa of baby."),
            GROET.replace("Tot binnenkort,", "Warme groet,"),
        ]),
    ),
}


def main() -> None:
    for naam, e in EMAILS.items():
        (HIER / naam).write_text(layout(**e), encoding="utf-8")
        print(f"  ✓ emails/{naam}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
