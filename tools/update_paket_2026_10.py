"""Update paket 3 Okt 2026: brosur Riyadh Air November (update 29/09) + Ramadhan 1448 H (update 01/10).

Patch langsung HTML widget yang live (bukan build ulang), supaya edit manual di kartu harga tetap terjaga:
- Kartu harga `.ehpk` (12 halaman): Bronze November -> Hotel Madinah Al-Aqeeq, tambah Gold November,
  tambah tab "Ramadhan" (4 paket). Di halaman tier, paket tier itu ditaruh paling depan.
- Section periode `.ehp` (hanya 9581): link PDF November baru, Bronze November diperbarui, tambah Gold
  November, tambah periode "Ramadhan 1448 H" + tombol unduh brosur.

Jalankan: DRY=1 python3 tools/update_paket_2026_10.py   (tulis hasil ke OUT, tanpa POST)
          python3 tools/update_paket_2026_10.py         (backup ke backup/2026-10-03/, lalu POST)
"""
import json, os, re, sys, time, urllib.parse
sys.path.insert(0, os.path.dirname(__file__))
from wp_rest import req

DRY = os.environ.get('DRY') == '1'
OUT = os.environ.get('OUT', 'build/2026-10-03')
BACKUP = os.path.join(os.path.dirname(__file__), '..', 'backup', '2026-10-03')
UP = 'https://www.elharamainwisata.com/wp-content/uploads/2026/10/'
PDF_NOV = UP + 'paket-umroh-riyadh-air-november-2026.pdf'
PDF_RAM = UP + 'paket-umroh-ramadhan-1448h-februari-2027.pdf'
IMG = 'https://res.cloudinary.com/v6gwkqrb/image/upload/c_fill,g_auto,w_700,h_500,q_auto,f_auto/'

PAGES = [9581, 8869, 8896, 8908, 8909, 8910, 9584, 9585, 9586, 9587, 9588, 9589]
TIER_PAGE = {8869: 'bronze', 8896: 'silver', 8910: 'silver', 8908: 'platinum', 8909: 'premium'}

GOLD_NOV = dict(img='kartu-paket-23', bulan='November', label='Gold', tier='gold',
                desc='Musim Sejuk by Riyadh Air: Thaif + 2x kereta cepat + city tour Jeddah.',
                hari=10, maskapai='Riyadh Air', makkah='Marwa Rotana / Movenpick ★5', madinah='Al-Aqeeq ★5',
                berangkat='26 Nov 2026', q=46, t=49, d=52)
RAMADHAN = [
    dict(img='kartu-paket-24', bulan='Ramadhan', label='Ramadhan Bronze', tier='bronze',
         desc='Umroh Ramadhan musim dingin by Saudia: Thaif + kereta cepat, in &amp; out Jeddah.',
         hari=9, maskapai='Saudia Airlines', makkah='Al Shohada ★5', madinah='Royal Andalus ★4',
         berangkat='8, 14 &amp; 15 Feb 2027', q=39.5, t=41.5, d=43.5),
    dict(img='kartu-paket-25', bulan='Ramadhan', label='Ramadhan Platinum', tier='platinum',
         desc="Umroh Ramadhan by Saudia: Thaif + 2x kereta cepat, free umroh &amp; sa'i golf car, abaya &amp; jaket.",
         hari=9, maskapai='Saudia Airlines', makkah='Marwa Rotana ★5', madinah='Al-Aqeeq ★5',
         berangkat='14 &amp; 21 Feb 2027', q=56, t=59, d=63),
    dict(img='kartu-paket-26', bulan='Ramadhan', label='Ramadhan Premium', tier='premium',
         desc="Umroh Ramadhan by Saudia: Thaif + 2x kereta cepat, free umroh &amp; sa'i golf car, abaya &amp; jaket.",
         hari=9, maskapai='Saudia Airlines', makkah='Fairmont ★5', madinah='Al-Aqeeq ★5',
         berangkat='14 Feb 2027', q=60, t=64, d=68),
    dict(img='kartu-paket-27', bulan='Ramadhan', label="I'tikaf Silver 17 Hari", tier='silver',
         desc="I'tikaf &amp; Lailatul Qadr by Saudia: Thaif + 2x kereta cepat + GMC tour Jabal Uhud.",
         hari=17, maskapai='Saudia Airlines', makkah='Royal Majestic ★4', madinah='Al-Aqeeq ★5',
         berangkat='28 Feb 2027', q=71, t=80, d=97),
]

IC = {
    'durasi': '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    'maskapai': '<svg viewBox="0 0 24 24"><path d="M10.5 3.5 13 10h5.5a2 2 0 0 1 0 4H13l-2.5 6.5H8.5L10 14H6l-1.5 2H3l1-4-1-4h1.5L6 10h4L8.5 3.5z"/></svg>',
    'makkah': '<svg viewBox="0 0 24 24"><rect x="4" y="3" width="16" height="18" rx="1"/><path d="M8 7h2M14 7h2M8 11h2M14 11h2M10 21v-4h4v4"/></svg>',
    'madinah': '<svg viewBox="0 0 24 24"><path d="M4 21h16M6 21v-7a6 6 0 0 1 12 0v7M12 8V3M10 21v-4h4v4"/></svg>',
    'tanggal': '<svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>',
}


def rp(jt):
    return 'Rp ' + f'{int(round(jt * 1_000_000)):,}'.replace(',', '.')


def jt(v):
    return 'Rp ' + f'{v:g}'.replace('.', ',') + ' jt'


def wa(phone, teks):
    return 'https://api.whatsapp.com/send?phone=' + phone + '&amp;text=' + urllib.parse.quote(teks, safe='')


def row(k, label, v):
    return f'<li><span class="k">{IC[k]}{label}</span><span class="v">{v}</span></li>'


def kcard(p, phone):
    teks = f"Assalamualaikum, saya mau info paket umroh {p['label']} {p['hari']} hari, keberangkatan {p['berangkat']}".replace('&amp;', '&')
    return (f'<a class="card" href="{wa(phone, teks)}" target="_blank" rel="noopener">'
            f'<div class="img"><img loading="lazy" src="{IMG}{p["img"]}.jpg" alt="Paket umroh {p["label"]} {p["bulan"]}"></div>'
            f'<div class="body"><span class="tag {p["tier"]}">{p["label"]}</span><p class="desc">{p["desc"]}</p><ul class="rows">'
            + row('durasi', 'Durasi', f'{p["hari"]} hari') + row('maskapai', 'Maskapai', p['maskapai'])
            + row('makkah', 'Hotel Makkah', p['makkah']) + row('madinah', 'Hotel Madinah', p['madinah'])
            + row('tanggal', 'Berangkat', p['berangkat'])
            + f'</ul><div class="foot"><small>Mulai dari</small><b>{rp(p["q"])}</b></div>'
            f'<p class="kamar">Triple {jt(p["t"])} · Double {jt(p["d"])}</p></div></a>')


def patch_ehpk(h, pid):
    n0 = h.count('<a class="card')
    phone = re.search(r'api\.whatsapp\.com/send\?phone=(\d+)', h).group(1)
    # 1. Bronze November: hotel Madinah sesuai brosur 29/09
    assert h.count('Peninsula / Al-Aqeeq ★5') >= 1
    h = h.replace('Peninsula / Al-Aqeeq ★5', 'Al-Aqeeq ★5')
    # 2. Gold November di tab November (sebelum kartu konsultasi)
    m = re.search(r'(<div class="grid g1">\n)(.*?)(<a class="card more")', h, re.S)
    assert m and 'kartu-paket-01' in m.group(2) and 'kartu-paket-23' not in h
    h = h[:m.end(2)] + kcard(GOLD_NOV, phone) + '\n' + h[m.end(2):]
    # 3. Tab Ramadhan
    assert 'ehpk-t4' not in h
    h = h.replace('<input type="radio" class="rb" name="ehpk-tab" id="ehpk-t3">',
                  '<input type="radio" class="rb" name="ehpk-tab" id="ehpk-t3"><input type="radio" class="rb" name="ehpk-tab" id="ehpk-t4">', 1)
    h = h.replace('<label class="tab" for="ehpk-t3">Januari</label>',
                  '<label class="tab" for="ehpk-t3">Januari</label><label class="tab" for="ehpk-t4">Ramadhan</label>', 1)
    css3 = '#ehpk-t3:checked~.g3{display:flex}'
    h = h.replace(css3, css3 + '\n#ehpk-t4:checked~.tabs label[for=ehpk-t4]{background:var(--navy);border-color:var(--navy);color:#fff}#ehpk-t4:checked~.g4{display:flex}', 1)
    more = re.search(r'<div class="grid g1">\n.*?(<a class="card more".*?</a>)', h, re.S).group(1)
    assert 'class="ic"' in more and 'Rp ' not in more
    more = re.sub(r'text=[^"]*', 'text=' + urllib.parse.quote('Assalamualaikum, saya mau konsultasi jadwal & paket umroh Ramadhan lainnya', safe=''), more)
    tier = TIER_PAGE.get(pid)
    ram = sorted(RAMADHAN, key=lambda p: p['tier'] != tier) if tier else RAMADHAN
    g4 = '<div class="grid g4">\n' + '\n'.join(kcard(p, phone) for p in ram) + '\n' + more + '\n</div>'
    m3 = re.search(r'<div class="grid g3">\n.*?<a class="card more".*?</a>\n</div>', h, re.S)
    assert m3
    h = h[:m3.end()] + '\n' + g4 + h[m3.end():]
    assert h.count('<a class="card') == n0 + 1 + 5, (pid, n0, h.count('<a class="card'))
    assert h.count('ehpk-t4') == 5 and h.count('class="grid g4"') == 1  # radio + label + 3x CSS
    return h


# ---------- section periode .ehp (9581) ----------
def ecard(p):
    msg = f"Assalamu'alaikum Elharamain Wisata, saya tertarik dengan {p['name']} ({p['period']}) keberangkatan {p['dates']}. Mohon info lebih lanjut."
    url = 'https://api.whatsapp.com/send?phone=6281287292422&text=' + urllib.parse.quote(msg.replace('&amp;', '&'))
    rows = ''.join(f'<tr><td>{l}</td><td>{rp(v)}</td></tr>' for l, v in zip(('Sekamar ber-4 (Quad)', 'Sekamar ber-3 (Triple)', 'Sekamar ber-2 (Double)'), p['prices']))
    bonus = ('<div class="ehp-bonus"><b>Bonus Paket</b><ul>' + ''.join(f'<li>{b}</li>' for b in p['bonus']) + '</ul></div>') if p.get('bonus') else ''
    chips = ''.join(f'<span>{c}</span>' for c in p['chips'])
    return f'''<article class="ehp-card" data-tier="{p['tier']}"><img class="ehp-img" src="https://res.cloudinary.com/v6gwkqrb/image/upload/c_fill,g_auto,w_800,h_450,f_auto,q_auto/{p['img']}.jpg" width="800" height="450" loading="lazy" alt="{p['name']} {p['period']} Elharamain Wisata">
<div class="ehp-top"><div class="ehp-tier">{p['tier'].title()} · {p['bintang']}</div><h4>{p['name']}</h4>
<div class="ehp-chips">{chips}</div></div>
<div class="ehp-body">
<div class="ehp-from">Mulai dari<b>{rp(min(p['prices']))}</b></div>
<table class="ehp-prices"><tbody>{rows}</tbody></table>
<div class="ehp-row"><i>&#128197;</i><div><small>Keberangkatan</small>{p['dates']}</div></div>
<div class="ehp-row"><i>✈</i><div><small>Rute</small>{p['route']}</div></div>
<div class="ehp-row"><i>&#128332;</i><div><small>Hotel Madinah</small>{p['mad']}</div></div>
<div class="ehp-row"><i>&#128331;</i><div><small>Hotel Makkah</small>{p['mak']}</div></div>
{bonus}
<a class="ehp-cta" href="{url}" target="_blank" rel="noopener">Tanya / Daftar via WhatsApp</a>
</div></article>'''


GOLD_NOV_E = dict(name='Paket Umroh Gold', tier='gold', bintang='Hotel Bintang 5', period='November 2026', img='kartu-paket-23',
                  chips=['10 Hari', 'Riyadh Air', '+ Thaif', '2x Kereta Cepat'], prices=(46, 49, 52), dates='26 November 2026',
                  route='Jakarta – Riyadh – Jeddah', mad='Al-Aqeeq Madinah (±50 m)',
                  mak='Marwa Rotana / Movenpick (Zamzam Tower, pelataran)', bonus=['Free GMC Tour Night Jabal Uhud'])
RAM_E = [
    dict(name='Paket Umroh Ramadhan Bronze', tier='bronze', bintang='Hotel Bintang 4 & 5', img='kartu-paket-24',
         chips=['9 Hari', 'Saudia Airlines', '+ Thaif'], prices=(39.5, 41.5, 43.5), dates='8, 14 &amp; 15 Februari 2027',
         route='In Jeddah – Out Jeddah', mad='Royal Andalus ★4 (±30 m)', mak='Al Shohada ★5 (±450 m)'),
    dict(name='Paket Umroh Ramadhan Platinum', tier='platinum', bintang='Hotel Bintang 5', img='kartu-paket-25',
         chips=['9 Hari', 'Saudia Airlines', '+ Thaif', '2x Kereta Cepat'], prices=(56, 59, 63), dates='14 &amp; 21 Februari 2027',
         route='In Jeddah – Out Jeddah', mad='Al-Aqeeq Madinah (±50 m)', mak='Marwa Rotana (Zamzam Tower, pelataran)',
         bonus=["Free 1x umroh &amp; sa'i by golf car", 'Free abaya &amp; jaket eksklusif']),
    dict(name='Paket Umroh Ramadhan Premium', tier='premium', bintang='Hotel Bintang 5', img='kartu-paket-26',
         chips=['9 Hari', 'Saudia Airlines', '+ Thaif', '2x Kereta Cepat'], prices=(60, 64, 68), dates='14 Februari 2027',
         route='In Jeddah – Out Jeddah', mad='Al-Aqeeq Madinah (±50 m)', mak='Fairmont (Zamzam Tower, pelataran)',
         bonus=["Free 1x umroh &amp; sa'i by golf car", 'Free abaya &amp; jaket eksklusif']),
    dict(name="Paket Umroh I'tikaf Silver 17 Hari", tier='silver', bintang='Hotel Bintang 4 & 5', img='kartu-paket-27',
         chips=['17 Hari', 'Saudia Airlines', '+ Thaif', '2x Kereta Cepat'], prices=(71, 80, 97), dates='28 Februari 2027',
         route='In Jeddah – Out Jeddah', mad='Al-Aqeeq Madinah (±50 m)', mak='Royal Majestic ★4 (±400 m)',
         bonus=['Free GMC Tour Night Jabal Uhud', "I'tikaf 10 malam terakhir &amp; Lailatul Qadr"]),
]
for p in RAM_E:
    p['period'] = 'Ramadhan 1448 H'


def patch_ehp(h):
    old_pdf = 'https://www.elharamainwisata.com/wp-content/uploads/2026/09/paket-umroh-riyadh-air-november.pdf'
    assert h.count(old_pdf) == 1 and 'ramadhan-1448h' not in h
    h = h.replace(old_pdf, PDF_NOV)
    h = h.replace('November 2026<small>1 paket</small>', 'November 2026<small>2 paket</small>', 1)
    assert h.count('Peninsula / Al-Aqeeq (50–150 m)') == 1
    h = h.replace('Peninsula / Al-Aqeeq (50–150 m)', 'Al-Aqeeq Madinah (±50 m)')
    h = h.replace('<div class="ehp-chips"><span>10 Hari</span><span>Riyadh Air</span><span>+ Thaif</span></div>',
                  '<div class="ehp-chips"><span>10 Hari</span><span>Riyadh Air</span><span>+ Thaif</span><span>Kereta Cepat</span></div>', 1)
    # Gold November setelah kartu Bronze November
    m = re.search(r'(<section class="ehp-period" id="november-2026">.*?)(</div></section>)', h, re.S)
    assert m and m.group(1).count('<article') == 1
    h = h[:m.end(1)] + ecard(GOLD_NOV_E) + h[m.end(1):]
    # Periode Ramadhan
    rid = 'ramadhan-1448h'
    h = h.replace('<input type="radio" class="ehp-tabs-r" name="ehp-tab" id="ehp-t-januari-2027" value="januari-2027">',
                  '<input type="radio" class="ehp-tabs-r" name="ehp-tab" id="ehp-t-januari-2027" value="januari-2027">'
                  f'<input type="radio" class="ehp-tabs-r" name="ehp-tab" id="ehp-t-{rid}" value="{rid}">', 1)
    h = h.replace('<label for="ehp-t-januari-2027" role="tab">Januari 2027<small>6 paket</small></label>',
                  '<label for="ehp-t-januari-2027" role="tab">Januari 2027<small>6 paket</small></label>'
                  f'<label for="ehp-t-{rid}" role="tab">Ramadhan 1448 H<small>Feb 2027 · 4 paket</small></label>', 1)
    css_jan = '#ehp-t-januari-2027:checked~.ehp-panels [data-tab=januari-2027]{display:block}'
    assert h.count(css_jan) == 1
    h = h.replace(css_jan, css_jan + f'\n#ehp-t-{rid}:checked~.ehp-tabs label[for=ehp-t-{rid}]{{background:#fff;color:#004AAD;border-color:#fff;box-shadow:0 6px 18px rgba(0,0,0,.18)}}'
                  f'#ehp-t-{rid}:checked~.ehp-panels [data-tab={rid}]{{display:block}}')
    panel = (f'<div class="ehp-panel" data-tab="{rid}"><section class="ehp-period" id="{rid}"><div class="ehp-head"><div>'
             '<span class="ehp-kicker">Ramadhan 1448 H</span><h3>Paket Umroh Ramadhan — Februari 2027</h3>'
             '<p>Direct flight Saudia Airlines (Jeddah – Jeddah) · Program 9 &amp; 17 hari + Thaif + Kereta Cepat · Buka puasa &amp; tarawih bersama</p></div>\n'
             f'<a class="ehp-pdf" href="{PDF_RAM}" target="_blank" rel="noopener">⬇ Download Brosur (PDF)</a></div>\n'
             '<div class="ehp-grid">' + ''.join(ecard(p) for p in RAM_E) + '</div></section></div>')
    end = '</div></section></div></div></div><script>'
    assert h.count(end) == 1
    h = h.replace(end, '</div></section></div>' + panel + '</div></div><script>')
    assert h.count('<article') == 17 + 1 + 4
    return h


# ---------- schema JSON-LD + FAQ jadwal (widget kantor/FAQ, STEP=schema) ----------
ORG_ID = 'https://www.elharamainwisata.com/#organization'


def trip(p, airline, label):
    dates = p['dates'].replace('&amp;', '&')
    return {'@type': 'TouristTrip', 'name': f"{p['name']} {label} ({p['days']} Hari)",
            'description': f"{p['name']} {p['days']} hari, {airline}, keberangkatan {dates}. Hotel Madinah {p['mad']}, hotel Makkah {p['mak']}.",
            'touristType': 'Jamaah umroh', 'provider': {'@id': ORG_ID},
            'offers': {'@type': 'AggregateOffer', 'priceCurrency': 'IDR', 'lowPrice': int(min(p['prices']) * 1e6),
                       'highPrice': int(max(p['prices']) * 1e6), 'offerCount': 3, 'availability': 'https://schema.org/InStock', 'url': None}}


GOLD_NOV_E['days'] = 10
for p, d in zip(RAM_E, (9, 9, 9, 17)):
    p['days'] = d
# Paket baru per halaman: semua di halaman umum/cabang, sesuai tier di halaman tier (8910 tidak berubah).
SCHEMA_ADD = {8869: [0], 8896: [3], 8908: [1], 8909: [2], 8910: []}


def patch_schema(h, pid):
    assert 'Ramadhan 1448 H' not in h, pid
    h = h.replace('Peninsula / Al-Aqeeq (50–150 m)', 'Al-Aqeeq Madinah (±50 m)')
    idx = SCHEMA_ADD.get(pid, [0, 1, 2, 3])
    ram = [RAM_E[i] for i in idx]
    gold = pid not in SCHEMA_ADD
    jadwal = ''.join(f"; Ramadhan 1448 H: {p['dates'].replace('&amp;', '&')}" for p in ram)

    def ld(m):
        d = json.loads(m.group(1))
        g = d['@graph']
        url = next(x['offers']['url'] for x in g if x['@type'] == 'TouristTrip')
        new = ([trip(GOLD_NOV_E, 'Riyadh Air', 'November 2026')] if gold else []) + [trip(p, 'Saudia Airlines', 'Februari 2027') for p in ram]
        for t in new:
            t['offers']['url'] = url
        last = max(i for i, x in enumerate(g) if x['@type'] == 'TouristTrip')
        g[last + 1:last + 1] = new
        return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + '</script>'

    h, n = re.subn(r'<script type="application/ld\+json">(.*?)</script>', ld, h, flags=re.S)
    assert n == 1, (pid, n)
    # Jawaban FAQ jadwal: di JSON-LD dan teks yang tampil
    if jadwal:
        h, k = re.subn(r'(Jadwal keberangkatan: [^<"]*?)\.(?=</p>|")', lambda m: m.group(1) + jadwal + '.', h)
        if gold:
            h = h.replace('November 2026: 26 November 2026;', 'November 2026: 26 November 2026 (Bronze &amp; Gold);'.replace('&amp;', '&'))
    return h


def main_schema():
    for pid in PAGES:
        raw = get_page(pid)
        data = raw['meta']['_elementor_data']
        if not DRY:
            with open(f'{BACKUP}/{pid}_sebelum_schema.json', 'w') as f:
                f.write(data)
        els = json.loads(data)
        n = walk(els, lambda h: patch_schema(h, pid) if 'application/ld+json' in h and '"TouristTrip"' in h else None)
        assert n == (0 if pid == 8910 else 1), (pid, n)
        if not n:
            print(pid, 'schema tidak berubah')
            continue
        new = json.dumps(els, ensure_ascii=False)
        with open(f'{OUT}/{pid}-schema.json', 'w') as f:
            f.write(new)
        if DRY:
            print(pid, 'schema OK (dry)')
            continue
        st, r = req('POST', f'/wp/v2/pages/{pid}', {'meta': {'_elementor_data': new}})
        print(pid, 'schema', st)
        assert st == 200, r
    if not DRY:
        print('hapus cache elementor:', req('DELETE', '/elementor/v1/cache')[0])


def get_page(pid):
    # Hosting kadang membalas halaman anti-bot "One moment, please..." (bukan JSON); tunggu lalu ulangi.
    for i in range(6):
        try:
            st, raw = req('GET', f'/wp/v2/pages/{pid}?context=edit')
            if st == 200 and isinstance(raw, dict):
                return raw
        except json.JSONDecodeError:
            pass
        time.sleep(20)
    raise SystemExit(f'gagal GET {pid}')


def walk(els, fn):
    n = 0
    for e in els:
        s = e.get('settings', {})
        h = s.get('html', '')
        if e.get('widgetType') == 'html' and h:
            new = fn(h)
            if new is not None and new != h:
                s['html'] = new
                n += 1
        n += walk(e.get('elements', []), fn)
    return n


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(BACKUP, exist_ok=True)
    for pid in PAGES:
        raw = get_page(pid)
        data = raw['meta']['_elementor_data']
        if not DRY:
            with open(f'{BACKUP}/{pid}_sebelum_ramadhan.json', 'w') as f:
                f.write(data)
        els = json.loads(data)
        n = walk(els, lambda h: patch_ehpk(h, pid) if 'class="ehpk"' in h else None)
        if pid == 9581:
            n += walk(els, lambda h: patch_ehp(h) if 'class="ehp-tabs-r"' in h else None)
        assert n == (2 if pid == 9581 else 1), (pid, n)
        new = json.dumps(els, ensure_ascii=False)
        with open(f'{OUT}/{pid}.json', 'w') as f:
            f.write(new)
        if DRY:
            print(pid, 'OK (dry)', n, 'widget')
            continue
        st, r = req('POST', f'/wp/v2/pages/{pid}', {'meta': {'_elementor_data': new}})
        print(pid, st, n, 'widget')
        assert st == 200, r
    if not DRY:
        print('hapus cache elementor:', req('DELETE', '/elementor/v1/cache')[0])


if __name__ == '__main__':
    main_schema() if os.environ.get('STEP') == 'schema' else main()
