#!/usr/bin/env python3
"""Erzeugt alle HTML-Seiten von medjugorjereisen.de.

Aufruf (im Projektordner):  python3 werkzeug/bauen.py
Daten:  daten/botschaften.json  (Monatsbotschaften, neueste zuerst)
        daten/reisen.json        (Reisetermine)
"""
import html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = html.escape

KONTAKT = {
    "mobil": "0152 33 88 99 60", "mobil_link": "+4915233889960",
    "mail": "maria@medjugorjereisen.de",
    "mail_gruppe": "post@medjugorjereisen.de",
}

MONATE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli",
          "August", "September", "Oktober", "November", "Dezember"]

LOGO = ('<svg width="34" height="34" viewBox="0 0 34 34" fill="none" stroke="#B8913F" '
        'stroke-width="1.8" aria-hidden="true"><path d="M17 3v28M9 11h16"></path>'
        '<circle cx="17" cy="11" r="13" stroke-opacity="0.35"></circle></svg>')

NAV = [("index.html#reisen", "Reisen", "reisen"),
       ("botschaften.html", "Botschaften", "botschaften"),
       ("medjugorje.html", "Medjugorje", "medjugorje"),
       ("index.html#kinder-mariens", "Kinder Mariens", "kinder"),
       ("ueber-mich.html", "Über mich", "ueber")]


def seite(pfad, titel, beschreibung, inhalt, aktiv="", tiefe=0):
    pre = "../" * tiefe
    nav = []
    for href, text, key in NAV:
        cur = ' aria-current="page"' if key == aktiv else ""
        nav.append(f'<a href="{pre}{href}"{cur}>{text}</a>')
    nav.append(f'<a class="btn" href="{pre}anfrage.html">Reise anfragen</a>')
    kopf = f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(titel)}</title>
<meta name="description" content="{E(beschreibung)}">
<link rel="stylesheet" href="{pre}style.css">
<link rel="icon" href="{pre}bilder/favicon.svg" type="image/svg+xml">
</head>
<body>
<a class="skip" href="#inhalt">Zum Inhalt springen</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{pre}index.html">{LOGO}<span><span class="brand-name">Medjugorje Reisen</span><span class="brand-sub">Reiner Wettcke · Dobel</span></span></a>
    <nav class="nav" aria-label="Hauptmenü">{"".join(nav)}</nav>
  </div>
</header>
<main id="inhalt">
'''
    fuss = f'''</main>
<footer class="site-footer">
  <div class="wrap spalten">
    <div><span class="fname">Medjugorje Reisen</span><span>Reiner Wettcke</span><span>Höhenstraße 25</span><span>75335 Dobel</span></div>
    <div><strong>Kontakt</strong><span>Telefon <a href="tel:{KONTAKT['mobil_link']}">{KONTAKT['mobil']}</a></span><a href="mailto:{KONTAKT['mail']}">{KONTAKT['mail']}</a></div>
    <nav aria-label="Weitere Seiten" style="display:flex;flex-direction:column;gap:6px"><strong>Wichtige Seiten</strong><a href="{pre}anfrage.html">Reise anfragen</a><a href="{pre}botschaften.html">Botschaften-Archiv</a><a href="{pre}impressum.html">Impressum</a><a href="{pre}datenschutz.html">Datenschutz</a></nav>
  </div>
  <div class="wrap unten">Alle Botschaften werden unter dem Vorbehalt des abschließenden Urteils der Katholischen Kirche veröffentlicht. Texte der Monatsbotschaften: Medjugorje Deutschland e.V. · © Medjugorje Reisen, Reiner Wettcke</div>
</footer>
</body>
</html>
'''
    ziel = os.path.join(ROOT, pfad)
    os.makedirs(os.path.dirname(ziel), exist_ok=True)
    with open(ziel, "w", encoding="utf-8") as f:
        f.write(kopf + inhalt + fuss)


def lade(name):
    with open(os.path.join(ROOT, "daten", name), encoding="utf-8") as f:
        return json.load(f)


def botschaft_zitat_html(m):
    return E(m["text"], quote=False)


def betrachtung(m, cls=""):
    if not m.get("link"):
        return ""
    return f'<a{cls} href="{E(m["link"])}" target="_blank" rel="noopener">Betrachtung zur Botschaft</a>'


def kurz(text, n=150):
    if len(text) <= n:
        return text
    cut = text[:n].rsplit(" ", 1)[0]
    return cut.rstrip(",;:") + " …“"


# ---------------- Startseite ----------------
def startseite(botschaften, reisen):
    m = botschaften[0]
    karten = []
    for r in reisen["termine"]:
        punkte = "".join(f"<li>{E(p)}</li>" for p in r["punkte"])
        badge = f'<span class="badge">{E(r["badge"])}</span>' if r.get("badge") else ""
        bild = f'<img src="bilder/{E(r["bild"])}" alt="{E(r.get("bild_alt", ""))}" loading="lazy">' if r.get("bild") else ""
        preis = (f'<span><span class="preis">{E(r["preis"])}</span> <span class="preis-info">{E(r.get("preis_info", ""))}</span></span>'
                 if r.get("preis") else f'<span class="preis-info">{E(r.get("preis_info", ""))}</span>')
        karten.append(f'''<article class="card reise">
  <div class="reise-kopf"><span class="reise-datum">{E(r["datum"])}</span>{badge}</div>
  {bild}
  <div class="reise-inhalt">
    <h3>{E(r["titel"])}</h3>
    <ul>{punkte}</ul>
    <div class="reise-fuss">{preis}<a class="btn btn-klein" href="anfrage.html?reise={E(r["id"])}">{E(r.get("knopf", "Anfragen"))}</a></div>
  </div>
</article>''')
    karten.append('''<article class="partner">
  <h3>Weitere Wallfahrten unserer Partner</h3>
  <p class="muted" style="color:#3A404C">Medjugorje Deutschland e.V. bietet das ganze Jahr Bus- und Flugwallfahrten an, etwa zum Jugendfestival, zur Kreuzerhöhung oder zum Jahreswechsel.</p>
  <a href="https://www.medjugorje.de/reisen" target="_blank" rel="noopener" style="margin-top:auto;font-weight:600">Zu den Angeboten auf medjugorje.de</a>
</article>''')

    inhalt = f'''
<section class="hero">
  <div class="wrap">
    <div class="hero-text">
      <p class="eyebrow hell">Pilgerreisen seit über 35 Jahren</p>
      <h1>Mit uns nach Medjugorje – persönlich begleitet</h1>
      <p class="hero-lead">Kleine Gruppen, kurze Wege und eine Begleitung, die den Ort seit 1985 kennt. Ich kümmere mich um Flug, Unterkunft und alles Organisatorische, damit Sie sich ganz auf die Tage in Medjugorje einlassen können.</p>
      <div class="hero-actions">
        <a class="btn btn-gold" href="anfrage.html">Reise unverbindlich anfragen</a>
        <a class="btn btn-ghost" href="#reisen">Termine ansehen</a>
      </div>
      <p class="hero-call">Lieber persönlich? Rufen Sie mich an: <a href="tel:{KONTAKT['mobil_link']}">{KONTAKT['mobil']}</a></p>
    </div>
    <img class="hero-img" src="bilder/st-jakob.jpg" alt="Die Kirche St. Jakob in Medjugorje mit ihren zwei Türmen, davor Pilger bei Sonnenschein" width="1600" height="739">
  </div>
</section>

<section class="wrap section" id="botschaft" style="padding-bottom:40px">
  <div class="botschaft-block">
    <div class="info">
      <p class="eyebrow">Aktuelle Botschaft</p>
      <h2 class="section-title">Botschaft der Königin des Friedens</h2>
      <p class="muted">Monatsbotschaft vom {E(m["date"])} an die Seherin {E(m["seer"])}</p>
      <a href="botschaften.html" style="font-weight:600">Alle Botschaften seit 1987</a>
      <img src="bilder/koenigin-des-friedens.jpg" alt="Statue der Königin des Friedens vor goldenem Hintergrund" loading="lazy">
    </div>
    <figure class="card">
      <blockquote class="zitat">{botschaft_zitat_html(m)}</blockquote>
      <figcaption class="zitat-fuss"><span>(mit kirchlicher Erlaubnis)</span>{betrachtung(m, ' style="font-weight:600"')}</figcaption>
    </figure>
  </div>
</section>

<section class="wrap section" id="reisen">
  <div class="reisen-kopf">
    <div class="stack" style="gap:10px"><p class="eyebrow">Reisetermine</p><h2 class="section-title">Unsere nächsten Pilgerreisen</h2></div>
    <p class="muted" style="max-width:440px">{E(reisen.get("hinweis", ""))}</p>
  </div>
  <div class="grid grid-3">
{chr(10).join(karten)}
  </div>
</section>

<section class="band-weiss">
  <div class="wrap section stack" style="gap:40px">
    <h2 class="section-title" style="text-align:center">So einfach geht es</h2>
    <div class="schritte">
      <div class="schritt"><span class="nr">1</span><h3>Anfrage senden</h3><p>Reise wählen, Formular ausfüllen oder einfach anrufen. Unverbindlich und kostenlos.</p></div>
      <div class="schritt"><span class="nr">2</span><h3>Persönliches Gespräch</h3><p>Ich rufe Sie zurück, beantworte Ihre Fragen und übernehme die Buchung.</p></div>
      <div class="schritt"><span class="nr">3</span><h3>Gemeinsam pilgern</h3><p>Wir reisen als kleine Gruppe und erleben eine gesegnete Zeit in Medjugorje.</p></div>
    </div>
    <figure class="foto-gross">
      <img src="bilder/gruppe-kreuzberg.jpg" alt="Pilgergruppe in blauen T-Shirts sitzt gemeinsam am Gipfel des Kreuzbergs" loading="lazy">
      <figcaption>Unsere Pilgergruppe auf dem Kreuzberg</figcaption>
    </figure>
  </div>
</section>

<section class="wrap section stack" style="gap:36px;padding-bottom:0">
  <div class="stack" style="gap:10px"><p class="eyebrow">Medjugorje</p><h2 class="section-title">Orte, die Sie erleben werden</h2></div>
  <div class="grid grid-3">
    <figure class="ort"><img src="bilder/kreuzberg-kreuz.jpg" alt="Das weiße Kreuz auf dem Gipfel des Kreuzbergs" loading="lazy"><figcaption><span class="titel">Kreuzberg (Križevac)</span><span class="text">Der Kreuzweg hinauf zum großen Gipfelkreuz</span></figcaption></figure>
    <figure class="ort"><img src="bilder/erscheinungsberg.jpg" alt="Pilger auf dem steinigen Weg des Erscheinungsbergs" loading="lazy"><figcaption><span class="titel">Erscheinungsberg (Podbrdo)</span><span class="text">Hier begannen 1981 die Erscheinungen</span></figcaption></figure>
    <figure class="ort"><img src="bilder/platz-neu.jpg" alt="Pilger auf dem Platz am Außenaltar hinter der Kirche St. Jakob bei Sonnenuntergang" style="object-position:62% 50%" loading="lazy"><figcaption><span class="titel">Abendprogramm am Außenaltar</span><span class="text">Rosenkranz, Heilige Messe und Anbetung</span></figcaption></figure>
  </div>
  <p><a href="medjugorje.html" style="font-weight:600">Mehr über Medjugorje, die Geschichte und die Botschaften</a></p>
</section>

<section class="wrap section" id="ueber">
  <div class="ueber">
    <img src="bilder/reiner-portrait.jpg" alt="Reiner Wettcke lächelnd vor einem hellen Haus im Abendlicht" loading="lazy">
    <div class="text">
      <p class="eyebrow">Über mich</p>
      <h2 class="section-title" style="color:#1E2430">Medjugorje ist meine geistige Heimat</h2>
      <p>1985 kam ich zum ersten Mal nach Medjugorje, damals noch als evangelischer Christ. Die spürbare Gegenwart der Muttergottes hat mein Leben verändert. Seitdem bin ich immer wieder dort und kenne viele Menschen, die vor Ort wichtige Aufgaben übernehmen.</p>
      <p>Heute möchte ich anderen den Weg an diesen besonderen Ort öffnen. Zusammen mit meiner Frau Conny lebe ich in Dobel im Nordschwarzwald.</p>
      <a href="ueber-mich.html" style="font-weight:600">Meine ganze Geschichte lesen</a>
    </div>
  </div>
</section>

<section class="wrap" id="kinder-mariens" style="padding-bottom:96px">
  <div class="banner">
    <img src="bilder/statue-rosenkranz.jpg" alt="Marienstatue mit Rosenkranz vor blauem Himmel" loading="lazy">
    <div class="text">
      <h2>Kinder Mariens – die WhatsApp-Gruppe</h2>
      <p>Erhalten Sie regelmäßig die neuesten Botschaften, Predigten und Gebete direkt auf Ihr Handy. Schreiben Sie mir eine kurze E-Mail mit Ihrer Handynummer, dann schicke ich Ihnen den Einladungslink.</p>
    </div>
    <a class="btn btn-gold" href="mailto:{KONTAKT['mail_gruppe']}?subject=Kinder%20Mariens%20%E2%80%93%20Aufnahme%20in%20die%20WhatsApp-Gruppe&amp;body=Ich%20m%C3%B6chte%20gerne%20der%20Gruppe%20%E2%80%9EKinder%20Mariens%E2%80%9C%20beitreten.%0AMeine%20Handynummer%3A%20">Der Gruppe beitreten</a>
  </div>
</section>
'''
    seite("index.html", "Medjugorje Reisen – Pilgerreisen nach Medjugorje mit Reiner Wettcke",
          "Persönlich begleitete Pilgerreisen nach Medjugorje in kleinen Gruppen. Aktuelle Monatsbotschaft, Reisetermine und Anfrage.",
          inhalt, aktiv="")


# ---------------- Anfrage ----------------
def anfrage(reisen):
    optionen = "".join(f'<option value="{E(r["titel"] + " · " + r["datum"])}" data-id="{E(r["id"])}">{E(r["titel"])} · {E(r["datum"])}</option>' for r in reisen["termine"])
    optionen += '<option value="Noch unentschlossen – bitte beraten Sie mich">Ich bin noch unentschlossen – bitte beraten Sie mich</option>'
    inhalt = f'''
<div class="wrap form-layout">
  <aside>
    <p class="eyebrow">Reise anfragen</p>
    <h1>Ich freue mich auf Ihre Anfrage</h1>
    <p style="color:#3A404C">Füllen Sie das Formular aus. Ich melde mich innerhalb von zwei Tagen persönlich bei Ihnen. Die Anfrage ist unverbindlich und kostenlos.</p>
    <div class="card kontakt-box">
      <strong style="font-size:19px;color:#1E2430">Lieber telefonisch?</strong>
      <span>Telefon <a href="tel:{KONTAKT['mobil_link']}" style="font-weight:600">{KONTAKT['mobil']}</a></span>
      <span>E-Mail <a href="mailto:{KONTAKT['mail']}" style="font-weight:600">{KONTAKT['mail']}</a></span>
    </div>
  </aside>
  <section class="card form-karte" aria-label="Anfrageformular">
    <form class="form-stack" action="https://formsubmit.co/{KONTAKT['mail']}" method="POST">
      <input type="hidden" name="_subject" value="Neue Reiseanfrage über medjugorjereisen.de">
      <input type="hidden" name="_captcha" value="false">
      <input type="hidden" name="_next" id="weiter" value="https://medjugorjereisen.de/danke.html">
      <input class="honig" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">

      <div class="feld"><label for="reise">Welche Reise interessiert Sie?</label>
        <select id="reise" name="Reise">{optionen}</select></div>

      <div class="zwei">
        <div class="feld"><label for="personen">Anzahl Personen</label>
          <input id="personen" name="Personen" type="number" min="1" max="20" value="1" required></div>
        <fieldset><legend>Zimmer</legend>
          <div class="radios">
            <label><input type="radio" name="Zimmer" value="Doppelzimmer" checked> Doppelzimmer</label>
            <label><input type="radio" name="Zimmer" value="Einzelzimmer"> Einzelzimmer</label>
          </div>
        </fieldset>
      </div>

      <div class="zwei">
        <div class="feld"><label for="name">Name *</label><input id="name" name="Name" type="text" autocomplete="name" required></div>
        <div class="feld"><label for="tel">Telefon</label><input id="tel" name="Telefon" type="tel" autocomplete="tel"></div>
      </div>

      <div class="feld"><label for="mail">E-Mail *</label><input id="mail" name="email" type="email" autocomplete="email" required></div>

      <label class="check"><input type="checkbox" name="Rückruf gewünscht" value="Ja" checked> <span>Bitte rufen Sie mich zurück</span></label>

      <div class="feld"><label for="msg">Ihre Nachricht oder Fragen</label><textarea id="msg" name="Nachricht" rows="5"></textarea></div>

      <label class="check"><input type="checkbox" name="Datenschutz" value="zugestimmt" required> <span>Ich habe die <a href="datenschutz.html">Datenschutzerklärung</a> gelesen und bin einverstanden, dass meine Angaben zur Beantwortung meiner Anfrage übermittelt und gespeichert werden. *</span></label>

      <button class="btn" type="submit" style="align-self:flex-start;font-size:19px;min-height:56px;padding:15px 32px">Anfrage absenden</button>
      <p class="muted" style="font-size:15px">* Pflichtfelder</p>
    </form>
  </section>
</div>
<script>
(function(){{
  var w=document.getElementById('weiter');
  if(w && location.protocol.indexOf('http')===0){{ w.value=new URL('danke.html', location.href).href; }}
  var id=new URLSearchParams(location.search).get('reise');
  if(id){{ var s=document.getElementById('reise'); for(var i=0;i<s.options.length;i++){{ if(s.options[i].getAttribute('data-id')===id){{ s.selectedIndex=i; }} }} }}
}})();
</script>
'''
    seite("anfrage.html", "Reise anfragen – Medjugorje Reisen",
          "Unverbindliche Anfrage für eine Pilgerreise nach Medjugorje mit Reiner Wettcke.", inhalt)

    danke = f'''
<div class="wrap textseite">
  <p class="eyebrow">Anfrage gesendet</p>
  <h1>Vielen Dank für Ihre Anfrage!</h1>
  <p>Ich melde mich innerhalb von zwei Tagen persönlich bei Ihnen. Eine Bestätigung haben Sie per E-Mail erhalten.</p>
  <p>Wenn es eilt, erreichen Sie mich auch telefonisch unter <a href="tel:{KONTAKT['mobil_link']}">{KONTAKT['mobil']}</a>.</p>
  <p style="margin-top:28px"><a class="btn" href="index.html">Zurück zur Startseite</a></p>
</div>
'''
    seite("danke.html", "Vielen Dank – Medjugorje Reisen", "Ihre Anfrage ist bei uns eingegangen.", danke)


# ---------------- Botschaften ----------------
def botschaften_seiten(botschaften):
    jahre = sorted({m["year"] for m in botschaften}, reverse=True)
    neuestes = jahre[0]

    def jahr_nav(aktiv, pre):
        gruppen = []
        for start, label in [(2020, "Seit 2020"), (2010, "2010er Jahre"), (2000, "2000er Jahre"), (1990, "1990er Jahre"), (1980, "1987 – 1989")]:
            js = [j for j in jahre if start <= j < start + 10]
            if not js:
                continue
            kn = "".join(
                f'<a class="jahr-knopf" href="{pre}{"botschaften.html" if j == neuestes else "botschaften/" + str(j) + ".html"}" aria-pressed="{"true" if j == aktiv else "false"}" style="text-align:center;text-decoration:none;display:flex;align-items:center;justify-content:center">{j}</a>'
                for j in js)
            gruppen.append(f'<div class="gruppe"><span class="gruppe-titel">{label}</span><div class="knoepfe">{kn}</div></div>')
        return f'''<nav class="card jahre" aria-label="Botschaften nach Jahr">
  <div class="stack" style="gap:4px"><span style="font-family:Lora,Georgia,serif;font-size:22px;font-weight:600">Archiv nach Jahren</span><span class="muted" style="font-size:15px">{len(botschaften)} Monatsbotschaften seit 1987</span></div>
  {"".join(gruppen)}
</nav>'''

    ziele = [(j, 1, f"botschaften/{j}.html") for j in jahre] + [(neuestes, 0, "botschaften.html")]
    for j, tiefe, pfad in ziele:
        pre = "../" * tiefe
        ms = [m for m in botschaften if m["year"] == j]
        karten = []
        for m in ms:
            monat = re.sub(r"^\d+\.\s*", "", m["date"])
            karten.append(f'''<article class="card monat" id="m{m["iso"][5:7]}">
  <div class="zeile"><h3>{E(monat)}</h3><span class="wer">{E(m["date"])} · {E(m["seer"])}</span></div>
  <blockquote>{botschaft_zitat_html(m)}</blockquote>
  <div class="fuss"><span>(mit kirchlicher Erlaubnis)</span>{betrachtung(m)}</div>
</article>''')
        inhalt = f'''
<section class="page-hero">
  <img src="{pre}bilder/statue-rosenkranz.jpg" alt="" aria-hidden="true">
  <div class="wrap">
    <p class="eyebrow hell">Botschaften</p>
    <h1>Die Monatsbotschaften der Königin des Friedens</h1>
    <p class="lead">Seit dem 25. Januar 1987 gibt die Gottesmutter am 25. jeden Monats durch die Seherin Marija Pavlović-Lunetti eine Botschaft an die Welt.</p>
  </div>
</section>
<div class="wrap archiv">
  {jahr_nav(j, pre)}
  <div class="archiv-liste">
    <div class="kopf"><h2>Botschaften {j}</h2><span class="muted">{len(ms)} {"Botschaft" if len(ms) == 1 else "Botschaften"}</span></div>
    {"".join(karten)}
    <p class="muted" style="font-size:15px;margin-top:12px">Quelle der Botschaftstexte: Medjugorje Deutschland e.V., <a href="https://www.medjugorje.de" target="_blank" rel="noopener">www.medjugorje.de</a>. Alle Botschaften werden unter dem Vorbehalt des abschließenden Urteils der Katholischen Kirche veröffentlicht.</p>
  </div>
</div>
<section class="wrap" style="padding-bottom:96px">
  <div class="banner">
    <div class="text"><h2>Jede neue Botschaft aufs Handy</h2><p>In unserer WhatsApp-Gruppe „Kinder Mariens“ erhalten Sie die Botschaft am 25. direkt zugeschickt.</p></div>
    <a class="btn btn-gold" href="{pre}index.html#kinder-mariens">Mehr erfahren</a>
  </div>
</section>
'''
        seite(pfad, f"Monatsbotschaften {j} – Medjugorje Reisen",
              f"Alle Monatsbotschaften der Königin des Friedens aus Medjugorje aus dem Jahr {j}.",
              inhalt, aktiv="botschaften", tiefe=tiefe)


# ---------------- Medjugorje ----------------
def medjugorje(botschaften):
    neueste = "".join(f'''<figure class="kurz-botschaft">
  <figcaption>{E(m["date"])} · {E(m["seer"])}</figcaption>
  <blockquote>{E(kurz(m["text"]), quote=False)}</blockquote>
  <p class="muted" style="font-size:15px">(mit kirchlicher Erlaubnis)</p>
  <a href="botschaften.html" style="margin-top:auto;font-weight:600;font-size:16px">Weiterlesen</a>
</figure>''' for m in botschaften[:3])
    with open(os.path.join(ROOT, "werkzeug", "medjugorje_inhalt.html"), encoding="utf-8") as f:
        vorlage = f.read()
    seite("medjugorje.html", "Medjugorje – Geschichte, Geschehen und Botschaften – Medjugorje Reisen",
          "Medjugorje: die ersten sieben Tage 1981, die fünf Hauptbotschaften, die Haltung der Kirche und die Geschichte des Ortes.",
          vorlage.replace("{{NEUESTE_BOTSCHAFTEN}}", neueste), aktiv="medjugorje")


def textseiten():
    for datei, titel, beschr, aktiv in [
        ("ueber-mich", "Über mich – Reiner Wettcke – Medjugorje Reisen", "Reiner Wettcke über seinen Weg nach Medjugorje.", "ueber"),
        ("impressum", "Impressum – Medjugorje Reisen", "Impressum von medjugorjereisen.de", ""),
        ("datenschutz", "Datenschutzerklärung – Medjugorje Reisen", "Datenschutzerklärung von medjugorjereisen.de", ""),
        ("404", "Seite nicht gefunden – Medjugorje Reisen", "Diese Seite gibt es nicht.", ""),
    ]:
        with open(os.path.join(ROOT, "werkzeug", f"{datei}_inhalt.html"), encoding="utf-8") as f:
            seite(f"{datei}.html", titel, beschr, f.read(), aktiv=aktiv)


ALTE_ADRESSEN = {
    "home": "index.html", "medjugorje": "medjugorje.html",
    "medjugorje/das-geschehen": "medjugorje.html#anfang",
    "medjugorje/medjugorje-die-geschichte": "medjugorje.html#geschichte",
    "medjugorje/medjugorje-botschaften": "botschaften.html",
    "botschaften": "botschaften.html", "kontakt": "anfrage.html",
    "kontakt/anfrage": "anfrage.html", "kontakt/impressum": "impressum.html",
    "kontakt/datenschutzerklaerung": "datenschutz.html", "ueber-uns": "ueber-mich.html",
    "2853-2": "index.html#kinder-mariens",
}


def weiterleitungen():
    """Kleine Seiten unter den alten WordPress-Adressen, die auf die neuen Seiten weiterleiten."""
    for alt, neu in ALTE_ADRESSEN.items():
        ziel = "/" + neu
        ordner = os.path.join(ROOT, alt)
        os.makedirs(ordner, exist_ok=True)
        with open(os.path.join(ordner, "index.html"), "w", encoding="utf-8") as f:
            f.write(f'''<!doctype html>
<html lang="de"><head><meta charset="utf-8"><title>Weiterleitung – Medjugorje Reisen</title>
<meta name="robots" content="noindex"><link rel="canonical" href="https://medjugorjereisen.de{ziel}">
<meta http-equiv="refresh" content="0; url={ziel}"></head>
<body><p>Diese Seite ist umgezogen: <a href="{ziel}">weiter zur neuen Seite</a>.</p></body></html>
''')


def sitemap(botschaften):
    jahre = sorted({m["year"] for m in botschaften}, reverse=True)
    seiten = ["", "anfrage.html", "medjugorje.html", "botschaften.html", "ueber-mich.html",
              "impressum.html", "datenschutz.html"] + [f"botschaften/{j}.html" for j in jahre]
    urls = "".join(f"<url><loc>https://medjugorjereisen.de/{s}</loc></url>" for s in seiten)
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write("User-agent: *\nAllow: /\nSitemap: https://medjugorjereisen.de/sitemap.xml\n")


if __name__ == "__main__":
    b = lade("botschaften.json")
    b.sort(key=lambda x: x["iso"], reverse=True)
    r = lade("reisen.json")
    startseite(b, r)
    anfrage(r)
    botschaften_seiten(b)
    medjugorje(b)
    textseiten()
    weiterleitungen()
    sitemap(b)
    print("Fertig:", len(b), "Botschaften,", len(r["termine"]), "Reisetermine")
