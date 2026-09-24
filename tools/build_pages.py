"""Build Elementor data for the umroh package pages, /paket-umroh-musim-dingin/ and /kantor-cabang/.

Package data, card markup and styles come from build_musim_dingin.py (everything
above its "build elementor data" marker). The page skeleton is the published
/paket-umroh-musim-dingin/ page (backup/pages/9581-*.json).

Usage:  OUT=build/ python3 tools/build_pages.py   -> build/<page_id>.json (+ seo.json, previews)
"""
import copy
import html
import json
import os
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.environ.get('OUT', os.path.join(ROOT, 'build')) + '/'
os.makedirs(OUT, exist_ok=True)

_src = open(os.path.join(HERE, 'build_musim_dingin.py')).read()
_lib = _src.split('# ---------- build elementor data ----------')[0]
_lib = _lib.replace("os.environ.get('OUT', 'build/')", repr(OUT))
exec(compile(_lib, 'build_musim_dingin.py', 'exec'))  # PERIODS, card, period_html, CSS, TAB_CSS, TAB_JS, INCLUDED, rp, WA

SITE = 'https://www.elharamainwisata.com'
ORG_ID = SITE + '/#organization'

OFFICES = [
    dict(city='Bekasi', label='Kantor Pusat Bekasi', addr='Ruko Emerald No.5 Blok EB 1, Jl. Harapan Indah Raya, Kec. Medan Satria', locality='Kota Bekasi', region='Jawa Barat', zip='17132', phone='081287292422'),
    dict(city='Jakarta', label='Kantor Jakarta', addr='Jl. Tebet Raya No.39 B, Tebet Timur, Kec. Tebet', locality='Jakarta Selatan', region='DKI Jakarta', zip='12820', phone='081214178056'),
    dict(city='Depok', label='Kantor Depok', addr='Jl. Margonda No.252 D, Kemiri Muka, Kec. Beji', locality='Kota Depok', region='Jawa Barat', zip='', phone='085179988198'),
    dict(city='Tangerang', label='Kantor Tangerang (BSD)', addr='Ruko Pasar Modern No.18 BSD, Rawa Mekar Jaya, Kec. Serpong', locality='Tangerang Selatan', region='Banten', zip='15318', phone='085693883208'),
    dict(city='Bogor', label='Kantor Bogor', addr='Ruko Graha Boulevard GBVD No.10, Jl. Summarecon Bogor, Sukatani, Kec. Sukaraja', locality='Kabupaten Bogor', region='Jawa Barat', zip='16144', phone='082260126394'),
    dict(city='Bandung', label='Kantor Bandung', addr='Jl. Boulevard Utama Blok RC No.18, Ruby Commercial Summarecon Bandung', locality='Kota Bandung', region='Jawa Barat', zip='', phone='085861345441'),
]
CITIES = ', '.join(o['city'] for o in OFFICES[:-1]) + ' & ' + OFFICES[-1]['city']


def intl(phone):
    return '62' + phone[1:]


def fmt_phone(phone):
    return f'{phone[:4]}-{phone[4:8]}-{phone[8:]}'


def maps_url(o):
    return 'https://www.google.com/maps/search/?api=1&query=' + urllib.parse.quote(f"Elharamain Wisata {o['addr']}, {o['locality']}")


EXTRA_CSS = r'''<style>
.ehp{font-family:Poppins,sans-serif;color:#10213d}
.ehp-off{max-width:1200px;margin:0 auto;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}
.ehp-o{background:#fff;border:1px solid #e3e9f3;border-radius:14px;padding:20px;display:flex;flex-direction:column;gap:8px}
.ehp-o h3{font-family:Raleway,sans-serif;font-weight:800;font-size:18px;margin:0;color:#004AAD}
.ehp-o address{font-style:normal;font-size:14px;line-height:1.55;color:#10213d}
.ehp-o address a{color:#004AAD;font-weight:600;text-decoration:none}
.ehp-o .ehp-o-act{display:flex;gap:8px;flex-wrap:wrap;margin-top:auto;padding-top:6px}
.ehp-o .ehp-o-act a{font-size:13px;font-weight:600;padding:8px 12px;border-radius:8px;text-decoration:none}
.ehp-o .ehp-o-wa{background:#25D366;color:#fff!important}
.ehp-o .ehp-o-map{border:1.5px solid #004AAD;color:#004AAD!important}
.ehp-o iframe{width:100%;height:190px;border:0;border-radius:10px;margin-top:4px}
.ehp-area{max-width:900px;margin:0 auto 26px;text-align:center;font-size:15px;line-height:1.7;color:#10213d}
.ehp-faq{max-width:900px;margin:0 auto;display:flex;flex-direction:column;gap:12px}
.ehp-faq details{background:#fff;border-radius:12px;border:1px solid #e3e9f3;padding:0 20px}
.ehp-faq summary{cursor:pointer;list-style:none;font-weight:700;font-size:16px;padding:16px 28px 16px 0;position:relative;color:#10213d}
.ehp-faq summary::-webkit-details-marker{display:none}
.ehp-faq summary::after{content:"+";position:absolute;right:0;top:12px;font-size:22px;color:#004AAD}
.ehp-faq details[open] summary::after{content:"\2013"}
.ehp-faq details p{margin:0 0 16px;font-size:14.5px;line-height:1.7;color:#33415c}
@media (max-width:1024px){.ehp-off{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:640px){.ehp-off{grid-template-columns:1fr}}
</style>'''


def offices_html(with_maps=False, context='paket umroh'):
    cards = []
    for o in OFFICES:
        msg = urllib.parse.quote(f"Assalamu'alaikum Elharamain Wisata {o['city']}, saya ingin konsultasi {context}.")
        tag = 'h2' if with_maps else 'h3'
        mapframe = ''
        if with_maps:
            q = urllib.parse.quote(f"{o['addr']}, {o['locality']}")
            mapframe = f'<iframe loading="lazy" title="Peta {o["label"]}" src="https://maps.google.com/maps?q={q}&amp;z=16&amp;output=embed" referrerpolicy="no-referrer-when-downgrade"></iframe>'
        cards.append(f'''<div class="ehp-o"><{tag} style="font-family:Raleway,sans-serif;font-weight:800;font-size:18px;margin:0;color:#004AAD">{o['label']}</{tag}>
<address>{o['addr']}, {o['locality']}, {o['region']}{(' ' + o['zip']) if o['zip'] else ''}<br>Telp/WA: <a href="tel:+{intl(o['phone'])}">{fmt_phone(o['phone'])}</a></address>{mapframe}
<div class="ehp-o-act"><a class="ehp-o-wa" href="https://api.whatsapp.com/send?phone={intl(o['phone'])}&amp;text={msg}" target="_blank" rel="noopener">WhatsApp {o['city']}</a>
<a class="ehp-o-map" href="{maps_url(o)}" target="_blank" rel="noopener">Petunjuk Arah</a></div></div>''')
    return '<div class="ehp-off">' + ''.join(cards) + '</div>'


def area_html(what):
    return (f'<p class="ehp-area">Elharamain Wisata melayani pendaftaran <b>{what}</b> untuk jamaah dari '
            f'<b>Bekasi, Jakarta, Depok, Tangerang, Bogor, Bandung</b> dan seluruh Indonesia. '
            f'Datang langsung ke kantor terdekat untuk konsultasi gratis, manasik, dan pengambilan perlengkapan.</p>')


def faq_html(faqs):
    return '<div class="ehp-faq">' + ''.join(
        f'<details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(faqs)) + '</div>'


def branch_schema():
    out = []
    for o in OFFICES:
        out.append({
            '@type': 'TravelAgency',
            '@id': f"{SITE}/kantor-cabang/#{o['city'].lower()}",
            'name': f"Elharamain Wisata {o['city']}",
            'parentOrganization': {'@id': ORG_ID},
            'url': SITE + '/kantor-cabang/',
            'telephone': '+' + intl(o['phone']),
            'priceRange': 'Rp 36.500.000 - Rp 75.000.000',
            'image': SITE + '/wp-content/uploads/2026/02/1.jpg',
            'address': {'@type': 'PostalAddress', 'streetAddress': o['addr'], 'addressLocality': o['locality'],
                        'addressRegion': o['region'], 'addressCountry': 'ID', **({'postalCode': o['zip']} if o['zip'] else {})},
            'hasMap': maps_url(o),
            'areaServed': o['city'],
            'openingHours': 'Mo-Su 09:00-17:00',
        })
    return out


def trip_schema(items, url):
    trips = []
    for pr, p in items:
        dates = html.unescape(p['dates'].replace('<br>', ' / '))
        trips.append({
            '@type': 'TouristTrip',
            'name': f"{p['name']} {pr['label']} ({p['days']} Hari)",
            'description': f"{p['name']} {p['days']} hari, {pr['airline']}, keberangkatan {dates}. Hotel Madinah {p['mad']}, hotel Makkah {p['mak']}.",
            'touristType': 'Jamaah umroh',
            'provider': {'@id': ORG_ID},
            'offers': {'@type': 'AggregateOffer', 'priceCurrency': 'IDR', 'lowPrice': int(min(p['prices']) * 1e6),
                       'highPrice': int(max(p['prices']) * 1e6), 'offerCount': 3, 'availability': 'https://schema.org/InStock', 'url': url},
        })
    return trips


def faq_schema(faqs):
    import re
    return {'@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': re.sub('<[^>]+>', '', a)}} for q, a in faqs]}


def ld(graph):
    return '<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False) + '</script>'


# ---------------------------------------------------------------- page specs
def jt(x):
    return f'{x:g}'.replace('.', ',') + ' juta'


COMMON_FAQ = [
    ('Apakah Elharamain Wisata travel umroh resmi?',
     'Ya. Elharamain Wisata (PT Dhiyaa El Haramain El Mubarakah) memiliki izin PPIU SK Kemenag No. 63 Tahun 2020 dan izin PIHK (Haji Plus) SK No. 846 Tahun 2020, anggota HIMPUH, IATA, dan terakreditasi A oleh KAN.'),
    ('Di mana kantor Elharamain Wisata?',
     'Kantor pusat di Ruko Emerald No.5 Blok EB 1, Harapan Indah, Medan Satria, Kota Bekasi. Kantor cabang ada di Tebet Jakarta Selatan, Margonda Depok, BSD Tangerang Selatan, Summarecon Bogor, dan Summarecon Bandung.'),
    ('Bagaimana cara daftar dan berapa DP-nya?',
     'Pendaftaran dengan DP Rp 6.000.000 per jamaah, pelunasan paling lambat 35 hari sebelum keberangkatan. Pembayaran hanya sah ke rekening a.n. PT Dhiyaa El Haramain El Mubarakah (Mandiri 156.001.150.115.4 / BSI 710.857.755.4).'),
]


def page_faq(name, items):
    lo = min(min(p['prices']) for _, p in items)
    dates = '; '.join(f"{pr['label']}: {html.unescape(p['dates'].replace('<br>', ' / '))}" for pr, p in items)
    return [
        (f'Berapa harga {name}?', f'Harga {name} mulai {rp(lo)} per jamaah (sekamar ber-4). Harga sekamar ber-3 dan ber-2 tercantum di tiap paket di atas.'),
        (f'Kapan jadwal keberangkatan {name}?', f'Jadwal keberangkatan: {dates}.'),
    ] + COMMON_FAQ


TIER_PAGES = [
    dict(id=8869, slug='umroh-bronze', name='Paket Umroh Bronze', filt=lambda p: p['tier'] == 'bronze',
         booking='https://umroh.elharamainwisata.com/bronze/',
         h1='Paket Umroh Bronze November 2026 – Januari 2027',
         kw='paket umroh bronze,umroh bronze desember 2026,travel umroh bekasi'),
    dict(id=8896, slug='paket-umroh-silver', name='Paket Umroh Silver', filt=lambda p: p['tier'] == 'silver' and p['days'] == 9,
         booking='https://umroh.elharamainwisata.com/silver/',
         h1='Paket Umroh Silver Desember 2026 & Januari 2027',
         kw='paket umroh silver,umroh silver desember 2026,travel umroh bekasi'),
    dict(id=8908, slug='umroh-platinum', name='Paket Umroh Platinum', filt=lambda p: p['tier'] == 'platinum',
         booking='https://umroh.elharamainwisata.com/platinum/',
         h1='Paket Umroh Platinum Desember 2026 & Januari 2027',
         kw='paket umroh platinum,umroh platinum desember 2026,umroh hotel zamzam tower'),
    dict(id=8909, slug='umroh-premium', name='Paket Umroh Premium', filt=lambda p: p['tier'] == 'premium',
         booking='https://umroh.elharamainwisata.com/premium/',
         h1='Paket Umroh Premium Januari 2027 – Hotel Fairmont',
         kw='paket umroh premium,umroh premium januari 2027,umroh hotel fairmont'),
    dict(id=8910, slug='umroh-silver-12-hari', name='Paket Umroh 12 Hari', filt=lambda p: p['days'] == 12,
         booking='https://umroh.elharamainwisata.com/silver12hari/',
         h1='Paket Umroh 12 Hari Desember 2026 & Januari 2027',
         kw='paket umroh 12 hari,umroh 12 hari desember 2026,umroh silver 12 hari'),
]


def tier_periods(filt):
    out = []
    for pr in PERIODS:
        items = [p for p in pr['items'] if filt(p)]
        if items:
            q = dict(pr, items=items)
            out.append(q)
    return out


def tabs_for(periods):
    """tabs_html() from build_musim_dingin, for an arbitrary list of periods."""
    global PERIODS
    saved = PERIODS
    PERIODS = periods
    try:
        g = globals()
        tab_css = r'''<style>
.ehp-tabs-r{position:absolute;opacity:0;pointer-events:none}
.ehp-tabs{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin:0 auto 36px;max-width:1100px}
.ehp-tabs label{cursor:pointer;background:rgba(255,255,255,.12);border:1.5px solid rgba(255,255,255,.4);color:#fff;padding:12px 22px;border-radius:12px;font-weight:600;font-size:15px;line-height:1.25;text-align:center;transition:.2s;user-select:none}
.ehp-tabs label small{display:block;font-size:12px;font-weight:500;opacity:.8}
.ehp-tabs label:hover{background:rgba(255,255,255,.22)}
.ehp-panel{display:none}
''' + ''.join(
            f'#ehp-t-{p["id"]}:checked~.ehp-tabs label[for=ehp-t-{p["id"]}]{{background:#fff;color:#004AAD;border-color:#fff;box-shadow:0 6px 18px rgba(0,0,0,.18)}}'
            f'#ehp-t-{p["id"]}:checked~.ehp-panels [data-tab={p["id"]}]{{display:block}}\n' for p in periods) + r'''
@media (max-width:640px){.ehp-tabs{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:26px}.ehp-tabs label{padding:10px 8px;font-size:13.5px}}
</style>'''
        out = g['CSS'] + tab_css + '<div class="ehp">'
        if len(periods) > 1:
            out += ''.join(f'<input type="radio" class="ehp-tabs-r" name="ehp-tab" id="ehp-t-{p["id"]}" value="{p["id"]}"{" checked" if i == 0 else ""}>' for i, p in enumerate(periods))
            out += '<div class="ehp-tabs" role="tablist">' + ''.join(
                f'<label for="ehp-t-{p["id"]}" role="tab">{p["label"]}<small>{len(p["items"])} paket</small></label>' for p in periods) + '</div>'
        out += '<div class="ehp-panels">'
        for i, p in enumerate(periods):
            inner = period_html(p)[len('<div class="ehp">'):-len('</div>')]
            style = ' style="display:block"' if len(periods) == 1 else ''
            out += f'<div class="ehp-panel" data-tab="{p["id"]}"{style}>{inner}</div>'
        return out + '</div></div>' + (g['TAB_JS'] if len(periods) > 1 else '')
    finally:
        PERIODS = saved


# ---------------------------------------------------------------- elementor helpers
_used = set()


def nid():
    import random
    while True:
        i = f'{random.getrandbits(28):07x}'
        if i not in _used:
            _used.add(i)
            return i


def reid(e):
    e['id'] = nid()
    for c in e.get('elements', []):
        reid(c)
    return e


def find(nodes, pred):
    for e in nodes:
        if pred(e):
            return e
        r = find(e.get('elements', []), pred)
        if r:
            return r


def by_id(nodes, i):
    return find(nodes, lambda e: e['id'] == i)


def html_widget(code):
    return {'id': nid(), 'elType': 'widget', 'widgetType': 'html', 'settings': {'html': code}, 'elements': [], 'isInner': False}


def light_section(heading_tpl, title, subtitle, body_html, anchor=None, bg='#FFFFFF'):
    head = reid(copy.deepcopy(heading_tpl))
    w = head['elements'][0]['elements']
    w[0]['settings']['title'] = title
    w[0]['settings']['header_size'] = 'h2'
    w[2]['settings']['editor'] = f'<p>{subtitle}</p>'
    settings = {'background_background': 'classic', 'background_color': bg,
                'padding': {'unit': 'px', 'top': '70', 'right': '0', 'bottom': '70', 'left': '0', 'isLinked': False},
                'padding_mobile': {'unit': 'px', 'top': '50', 'right': '16', 'bottom': '50', 'left': '16', 'isLinked': False},
                'content_width': {'unit': 'px', 'size': 1240, 'sizes': []}}
    if anchor:
        settings['_element_id'] = anchor
    return {'id': nid(), 'elType': 'section', 'isInner': False, 'settings': settings,
            'elements': [{'id': nid(), 'elType': 'column', 'isInner': False, 'settings': {'_column_size': 100, '_inline_size': None},
                          'elements': [head, html_widget(f'<div class="ehp">{body_html}</div>')]}]}


CSS_VER = os.environ.get('CSS_VER', '1')


def pin_post_css(data, page_id):
    """Load the page's own Elementor CSS directly (bypassing LiteSpeed UCSS, which
    keeps serving CSS generated from the page's previous design until it is purged)."""
    tag = (f'<link rel="stylesheet" data-noptimize="1" data-no-optimize="1" data-no-minify="1" '
           f'href="{SITE}/wp-content/uploads/elementor/css/post-{page_id}.css?ver={CSS_VER}" media="all">'
           '<link rel="stylesheet" data-noptimize="1" data-no-optimize="1" data-no-minify="1" '
           'href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&amp;family=Raleway:wght@600;700;800&amp;display=swap" media="all">')
    first_col = data[0]['elements'][0]
    first_col['elements'].insert(0, html_widget(tag))
    return data


def to_ascii_safe(data):
    s = json.dumps(data, ensure_ascii=False)
    s = ''.join('' if ord(c) == 0xFE0F else (f'&#{ord(c)};' if ord(c) > 0xFFFF else c) for c in s)
    return json.loads(s)


# ---------------------------------------------------------------- build
import random as _random
_random.seed(20260924)  # stable element ids between builds
base_page = json.load(open(os.path.join(ROOT, 'backup', 'pages', '9581-paket-umroh-musim-dingin.json')))
BASE = json.loads(base_page['meta']['_elementor_data'])
for e in BASE:
    reid(e)  # fresh ids, so nothing collides with the ids we add below
BASE_IDX = {k: i for i, e in enumerate(BASE) for k in [e['settings'].get('_element_id')] if k}
PKG_I = BASE_IDX['paket-umroh']
INC_TITLE_TPL = BASE[PKG_I + 1]['elements'][0]['elements'][0]  # light-background heading block


def section_index(data, heading_text):
    for i, e in enumerate(data):
        if find([e], lambda x: x.get('widgetType') == 'heading' and heading_text in x['settings'].get('title', '')):
            return i
    raise KeyError(heading_text)


def build_package_page(name, h1, subtitle, periods, url, booking=None, pkg_title=None, pkg_sub=None):
    data = copy.deepcopy(BASE)
    for e in data:
        reid(e)
    hero = data[0]
    hs = [x for x in [find([hero], lambda x, t=t: x.get('widgetType') == 'heading' and x['settings'].get('header_size') == t) for t in ('h3', 'h1', 'p')]]
    hs[0]['settings']['header_size'] = 'div'  # "Elharamain Wisata" label above the H1
    hs[1]['settings']['title'] = h1
    hs[2]['settings']['title'] = subtitle

    pkg = data[PKG_I]
    col = pkg['elements'][0]['elements']
    hw = col[0]['elements'][0]['elements']
    hw[0]['settings']['title'] = pkg_title or f'Harga & Jadwal {name}'
    hw[2]['settings']['editor'] = f'<p>{pkg_sub or "Hotel Bintang 5 · Harga per jamaah"}</p>'
    body = tabs_for(periods)
    if booking:
        body += (f'<p style="text-align:center;margin:34px 0 0"><a href="{booking}" style="display:inline-block;background:#dbc033;color:#1d1600;'
                 f'font-family:Poppins,sans-serif;font-weight:700;padding:14px 26px;border-radius:10px;text-decoration:none">Booking Online {name}</a></p>')
    col[1] = html_widget(body)

    items = [(pr, p) for pr in periods for p in pr['items']]
    faqs = page_faq(name, items)
    faq_sec = light_section(INC_TITLE_TPL, f'Pertanyaan Seputar {name}', 'FAQ', EXTRA_CSS + faq_html(faqs), anchor='faq', bg='#F3F7FD')
    off_sec = light_section(INC_TITLE_TPL, 'Kantor Elharamain Wisata Terdekat', 'Bekasi · Jakarta · Depok · Tangerang · Bogor · Bandung',
                            EXTRA_CSS + area_html(name) + offices_html(context=name) +
                            ld(trip_schema(items, url) + [faq_schema(faqs)]), anchor='kantor')
    cta_i = section_index(data, 'Wujudkan Ibadah')
    data[cta_i:cta_i] = [faq_sec, off_sec]
    return to_ascii_safe(data), items


def seo_for(name, items, kw, extra=''):
    lo = min(min(p['prices']) for _, p in items)
    months = []
    for pr, _ in items:
        m = {'november-2026': 'Nov 2026', 'awal-desember-2026': 'Des 2026', 'akhir-desember-2026': 'Des 2026', 'januari-2027': 'Jan 2027'}[pr['id']]
        if m not in months:
            months.append(m)
    title = f"{name.replace('Paket ', '')} {' & '.join(months[-2:]) if len(months) > 1 else months[0]} | Elharamain Wisata"
    if len(title) > 60:
        title = f"{name.replace('Paket ', '')} {months[-1]} | Elharamain Wisata"
    span = months[0] if len(months) == 1 else f'{months[0]}–{months[-1]}'
    cities = ['Bekasi', 'Jakarta', 'Depok', 'Tangerang', 'Bogor', 'Bandung']
    while True:
        desc = (f"{name} {span} mulai Rp {jt(lo)}. Hotel bintang 5, {extra}Thaif + kereta cepat. "
                f"Kantor {', '.join(cities[:-1])} & {cities[-1]}.")
        if len(desc) <= 160 or len(cities) <= 2:
            break
        cities.pop()
    return {'rank_math_title': title, 'rank_math_description': desc, 'rank_math_focus_keyword': kw,
            'rank_math_facebook_image': SITE + '/wp-content/uploads/2026/02/1.jpg', 'rank_math_facebook_image_id': '8791',
            'rank_math_twitter_use_facebook': 'on'}


SEO = {}
for spec in TIER_PAGES:
    periods = tier_periods(spec['filt'])
    url = f"{SITE}/{spec['slug']}/"
    lo = min(min(p['prices']) for pr in periods for p in pr['items'])
    sub = (f"{spec['name']} Elharamain Wisata mulai {rp(lo)}: hotel bintang 5, direct flight, program Thaif & kereta cepat, "
           f"dibimbing asatidz lulusan Timur Tengah. Berangkat dari Jakarta, kantor di {CITIES}.")
    data, items = build_package_page(spec['name'], spec['h1'], sub, periods, url, booking=spec['booking'])
    json.dump(pin_post_css(data, spec['id']), open(OUT + f"{spec['id']}.json", 'w'), ensure_ascii=False)
    airlines = sorted({pr['airline'] for pr in periods})
    SEO[spec['id']] = seo_for(spec['name'], items, spec['kw'], extra=' & '.join(a.replace(' Airlines', '') for a in airlines) + ', ')
    print(spec['id'], spec['slug'], sum(len(p['items']) for p in periods), 'paket', [p['label'] for p in periods])

# /paket-umroh-musim-dingin/ : same page, plus FAQ + kantor + schema
data, items = build_package_page(
    'Paket Umroh Musim Dingin', 'Paket Umroh Desember 2026 & Januari 2027',
    'Pilihan paket umroh musim dingin bersama Elharamain Wisata: hotel bintang 5, penerbangan Saudia Airlines & Riyadh Air, '
    f'program Thaif dan kereta cepat, dibimbing asatidz lulusan Timur Tengah. Kantor di {CITIES}.',
    PERIODS, SITE + '/paket-umroh-musim-dingin/',
    pkg_title='Paket Umroh Musim Dingin 2026/2027', pkg_sub='November 2026 · Desember 2026 · Januari 2027 — Hotel Bintang 5')
json.dump(pin_post_css(data, 9581), open(OUT + '9581.json', 'w'), ensure_ascii=False)

# /kantor-cabang/
KC_FAQ = COMMON_FAQ[:2] + [
    ('Apakah bisa konsultasi umroh langsung di kantor cabang?',
     'Bisa. Semua kantor Elharamain Wisata melayani konsultasi gratis, pendaftaran, pembayaran, dan pengambilan perlengkapan umroh setiap hari pukul 09.00–17.00 WIB. Hubungi WhatsApp kantor terdekat sebelum datang.'),
]
kc_body = (EXTRA_CSS + area_html('umroh & haji plus') + offices_html(with_maps=True, context='umroh & haji plus')
           + ld(branch_schema() + [faq_schema(KC_FAQ)]))
kc_hero_tpl = copy.deepcopy(INC_TITLE_TPL)
kc = [
    light_section(INC_TITLE_TPL, 'Kantor Elharamain Wisata', 'Kantor pusat Bekasi & 5 kantor cabang — konsultasi umroh dan haji plus gratis', kc_body, bg='#F3F7FD'),
    light_section(INC_TITLE_TPL, 'Pertanyaan Seputar Kantor Elharamain Wisata', 'FAQ', EXTRA_CSS + faq_html(KC_FAQ)),
]
# first heading on the page is the H1
kc[0]['elements'][0]['elements'][0]['elements'][0]['elements'][0]['settings']['header_size'] = 'h1'
kc[0]['settings']['padding'] = {'unit': 'px', 'top': '50', 'right': '0', 'bottom': '70', 'left': '0', 'isLinked': False}
json.dump(pin_post_css(to_ascii_safe(kc), 9099), open(OUT + '9099.json', 'w'), ensure_ascii=False)
SEO[9099] = {'rank_math_title': 'Kantor Travel Umroh Bekasi, Jakarta & Cabang | Elharamain',
             'rank_math_description': 'Alamat kantor Elharamain Wisata: pusat di Harapan Indah Bekasi, cabang Tebet Jakarta, Margonda Depok, BSD Tangerang, Summarecon Bogor & Bandung.',
             'rank_math_focus_keyword': 'travel umroh bekasi,travel umroh jakarta,kantor elharamain wisata',
             'rank_math_facebook_image': SITE + '/wp-content/uploads/2026/02/1.jpg', 'rank_math_facebook_image_id': '8791'}
SEO[9581] = {'rank_math_description': 'Paket umroh Nov-Des 2026 & Januari 2027 mulai Rp 36,5 juta. Hotel bintang 5, Saudia & Riyadh Air, Thaif + kereta cepat. Kantor Bekasi, Jakarta & Depok.'}

json.dump(SEO, open(OUT + 'seo.json', 'w'), ensure_ascii=False, indent=1)
for k, v in SEO.items():
    print(k, len(v.get('rank_math_title', '')), v.get('rank_math_title', ''), '|', len(v['rank_math_description']))

# static previews of the HTML widgets (for screenshots)
def collect_html(data):
    out = []
    def w(n):
        for e in n:
            if e.get('widgetType') == 'html':
                out.append(e['settings']['html'])
            w(e.get('elements', []))
    w(data)
    return out

for pid in [s['id'] for s in TIER_PAGES] + [9581, 9099]:
    d = json.load(open(OUT + f'{pid}.json'))
    parts = collect_html(d)
    page = ('<html><head><meta name=viewport content="width=device-width,initial-scale=1"><link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&family=Raleway:wght@800&display=swap" rel=stylesheet></head><body style="margin:0">'
            + ''.join(f'<div style="background:{"#004AAD" if "ehp-tabs" in p or "ehp-grid" in p else "#F3F7FD"};padding:40px 16px">{p}</div>' for p in parts) + '</body></html>')
    open(OUT + f'preview-{pid}.html', 'w').write(page)
