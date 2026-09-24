import json, copy, random, urllib.parse, html, sys, os

S = os.environ.get('OUT', 'build/')
HOME_EL = os.path.join(os.path.dirname(__file__), '..', 'backup', 'home_el_2026-09-24.json')
UP = 'https://www.elharamainwisata.com/wp-content/uploads/2026/09/'
WA = '6281287292422'

H = {  # hotel -> jarak
    'Al-Aqeeq': 'Al-Aqeeq Madinah (±50 m)',
    'Al-Aqeeq / Al-Haram': 'Al-Aqeeq / Al-Haram (±50 m)',
    'Peninsula Worth': 'Peninsula Worth (±150 m)',
    'Peninsula / Al-Aqeeq': 'Peninsula / Al-Aqeeq (50–150 m)',
    'Movenpick Madinah': 'Movenpick Madinah',
    'Anjum': 'Anjum Hotel (±350 m)',
    'Prestige': 'Prestige Hotel (±250 m)',
    'Prestige / Anjum': 'Prestige / Anjum (250–350 m)',
    'Marwa Rotana / Movenpick': 'Marwa Rotana / Movenpick (Zamzam Tower, pelataran)',
    'Fairmont': 'Fairmont (Zamzam Tower, pelataran)',
}
BONUS_PLAT_DES = ['H-1 free menginap di hotel', 'Free wahana Toboggan + golf car Sa\'i', 'Free abaya & jaket eksklusif', 'Free GMC Tour Night Jabal Uhud']
BONUS_PLAT_JAN = ['H-1 free menginap di hotel', 'Free Jabal Khandama + golf car Sa\'i', 'Free abaya & jaket eksklusif', 'Free GMC Tour Night Jabal Uhud']
GMC = ['Free GMC Tour Night Jabal Uhud']

def P(name, tier, dates, route, days, mad, mak, prices, bonus=(), note=''):
    return dict(name=name, tier=tier, dates=dates, route=route, days=days, mad=H[mad], mak=H[mak], prices=prices, bonus=list(bonus), note=note)

PERIODS = [
    dict(id='november-2026', label='November 2026', title='Paket Umroh Musim Sejuk — Riyadh Air',
         sub='Terbang perdana Riyadh Air dari Jakarta · Program 10 hari + Thaif + Kereta Cepat + Citytour Jeddah',
         pdf=UP + 'paket-umroh-riyadh-air-november.pdf', airline='Riyadh Air', badge='Terbang Perdana',
         items=[P('Paket Umroh Bronze', 'bronze', '26 November 2026', 'Jakarta – Riyadh – Jeddah', 10,
                  'Peninsula / Al-Aqeeq', 'Prestige / Anjum', (37, 40, 43))]),
    dict(id='awal-desember-2026', label='Awal–Tengah Des 2026', title='Paket Umroh Musim Dingin — Awal & Tengah Desember 2026',
         sub='Direct flight Saudia Airlines · Program 9–12 hari + Thaif + Kereta Cepat',
         pdf=UP + 'paket-umroh-awal-desember-2026.pdf', airline='Saudia Airlines',
         items=[
             P('Paket Umroh Bronze', 'bronze', '8 Desember 2026', 'In Jeddah – Out Jeddah', 9, 'Peninsula Worth', 'Anjum', (36.5, 38.5, 40.5)),
             P('Paket Umroh Bronze Plus', 'bronze', '11 & 12 Desember 2026', 'In Jeddah – Out Jeddah', 9, 'Peninsula Worth', 'Prestige', (37.5, 39.5, 41.5), note="Jum'at di Masjidil Haram"),
             P('Paket Umroh Silver (Makkah First)', 'silver', '8 Desember 2026', 'In Jeddah – Out Madinah', 9, 'Peninsula Worth', 'Anjum', (37.5, 39.5, 41.5)),
             P('Paket Umroh Silver (Madinah First)', 'silver', '1 & 7 Desember 2026', 'In Madinah – Out Jeddah', 9, 'Al-Aqeeq', 'Anjum', (38, 40, 42)),
             P('Paket Umroh Platinum', 'platinum', '7 Desember 2026', 'In Madinah – Out Jeddah', 9, 'Al-Aqeeq / Al-Haram', 'Marwa Rotana / Movenpick', (46.5, 48.5, 51.5), BONUS_PLAT_DES),
             P('Paket Umroh Silver 12 Hari (Madinah First)', 'silver', '9 Desember 2026', 'In Madinah – Out Jeddah', 12, 'Peninsula Worth', 'Anjum', (41.5, 43.5, 46.5), GMC),
         ]),
    dict(id='akhir-desember-2026', label='Akhir Des 2026', title='Paket Umroh Eksklusif — Akhir Desember 2026',
         sub='Direct flight Saudia Airlines (Jeddah – Jeddah) · Program 9–12 hari + Thaif + 2x Kereta Cepat',
         pdf=UP + 'paket-umroh-akhir-desember-2026.pdf', airline='Saudia Airlines', badge='Libur Akhir Tahun',
         items=[
             P('Paket Umroh Silver', 'silver', '21, 22 & 26 Desember 2026', 'In Jeddah – Out Jeddah', 9, 'Al-Aqeeq', 'Anjum', (47, 51, 56), GMC),
             P('Paket Umroh Platinum', 'platinum', '21, 22 & 26 Desember 2026', 'In Jeddah – Out Jeddah', 9, 'Al-Aqeeq / Al-Haram', 'Marwa Rotana / Movenpick', (54, 58, 64),
               ['H-1 free menginap di hotel', "Free wahana Toboggan + golf car Sa'i", 'Free outer & jaket eksklusif', 'Free GMC Tour Night Jabal Uhud']),
             P('Paket Umroh Silver 12 Hari', 'silver', '27 Desember 2026', 'In Jeddah – Out Jeddah', 12, 'Al-Aqeeq', 'Anjum', (53, 57, 66), GMC),
             P('Paket Umroh Gold 12 Hari', 'gold', '23 & 27 Desember 2026', 'In Jeddah – Out Jeddah', 12, 'Al-Aqeeq', 'Marwa Rotana / Movenpick', (60, 66, 75), GMC),
         ]),
    dict(id='januari-2027', label='Januari 2027', title='Paket Umroh Musim Dingin — High Season Januari 2027',
         sub='Direct flight Saudia Airlines · Program 9–12 hari + Thaif + Kereta Cepat',
         pdf=UP + 'paket-umroh-high-season-musim-dingin-januari-2027.pdf', airline='Saudia Airlines',
         items=[
             P('Paket Umroh Bronze', 'bronze', '3, 4, 9, 11, 17 & 31 Januari 2027', 'In Jeddah – Out Jeddah', 9, 'Al-Aqeeq', 'Anjum', (37.9, 40.4, 43.9)),
             P('Paket Umroh Silver', 'silver', '3, 4 & 31 Jan 2027 (Madinah – Jeddah)<br>25 Jan 2027 (Jeddah – Madinah)', 'Madinah First / Makkah First', 9, 'Al-Aqeeq', 'Anjum', (39, 41.5, 45)),
             P('Paket Umroh Platinum', 'platinum', '11, 18, 25 & 31 Januari 2027', 'In Madinah – Out Jeddah', 9, 'Movenpick Madinah', 'Marwa Rotana / Movenpick', (48.5, 51.5, 55.5), BONUS_PLAT_JAN),
             P('Paket Umroh Premium', 'premium', '11 & 31 Januari 2027', 'In Madinah – Out Jeddah', 9, 'Movenpick Madinah', 'Fairmont', (52, 56, 61), BONUS_PLAT_JAN),
             P('Paket Umroh Silver 12 Hari', 'silver', '13, 14 & 20 Januari 2027', 'In Madinah – Out Jeddah', 12, 'Al-Aqeeq', 'Anjum', (43.5, 46, 49.5), GMC),
             P('Paket Umroh Gold 12 Hari', 'gold', '14, 20 & 24 Januari 2027', 'In Madinah – Out Jeddah', 12, 'Al-Aqeeq', 'Marwa Rotana / Movenpick', (54, 57, 61), GMC),
         ]),
]


def rp(jt):
    return 'Rp ' + f'{int(round(jt * 1_000_000)):,}'.replace(',', '.')


def rp_short(jt):
    s = f'{jt:g}'.replace('.', ',')
    return f'{s} jt'


CSS = r'''
<style>
.ehp{--b:#004AAD;--b2:#1684CF;--g:#dbc033;--ink:#10213d;--mut:#5b6b84;--line:#e3e9f3;font-family:Poppins,sans-serif;color:var(--ink)}
.ehp *{box-sizing:border-box}
.ehp-nav{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin:0 auto 40px;max-width:1100px}
.ehp-nav a{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.35);color:#fff!important;padding:10px 18px;border-radius:999px;font-weight:600;font-size:14px;text-decoration:none;transition:.2s}
.ehp-nav a:hover{background:#fff;color:var(--b)!important}
.ehp-period{max-width:1200px;margin:0 auto 64px;scroll-margin-top:90px}

.ehp-head{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:16px;margin-bottom:22px;color:#fff}
.ehp-head h3{font-family:Raleway,sans-serif;font-weight:800;font-size:30px;line-height:1.2;margin:6px 0 6px;color:#fff}
.ehp-head p{margin:0;opacity:.85;font-size:15px}
.ehp-kicker{display:inline-block;background:var(--g);color:#1d1600;font-weight:700;font-size:12px;letter-spacing:.06em;text-transform:uppercase;padding:4px 12px;border-radius:999px}
.ehp-pdf{display:inline-flex;align-items:center;gap:8px;background:transparent;border:1.5px solid #fff;color:#fff!important;padding:10px 18px;border-radius:10px;font-weight:600;font-size:14px;text-decoration:none;white-space:nowrap}
.ehp-pdf:hover{background:#fff;color:var(--b)!important}
.ehp-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px}
.ehp-card{background:#fff;border-radius:16px;overflow:hidden;display:flex;flex-direction:column;box-shadow:0 10px 30px rgba(0,20,60,.18)}
.ehp-top{padding:20px 22px 16px;background:linear-gradient(135deg,var(--b),var(--b2));color:#fff;position:relative}
.ehp-card[data-tier=platinum] .ehp-top,.ehp-card[data-tier=premium] .ehp-top{background:linear-gradient(135deg,#0b1f45,#2a3f6e)}
.ehp-card[data-tier=gold] .ehp-top{background:linear-gradient(135deg,#7a5a00,#c9a227)}
.ehp-tier{font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;opacity:.9}
.ehp-top h4{font-family:Raleway,sans-serif;font-weight:800;font-size:21px;line-height:1.25;margin:4px 0 10px;color:#fff}
.ehp-chips{display:flex;flex-wrap:wrap;gap:6px}
.ehp-chips span{background:rgba(255,255,255,.18);border-radius:6px;padding:3px 9px;font-size:12px;font-weight:600}
.ehp-body{padding:18px 22px 22px;display:flex;flex-direction:column;gap:14px;flex:1}
.ehp-from{font-size:12px;color:var(--mut)}
.ehp-from b{display:block;font-size:26px;color:var(--b);font-weight:800;line-height:1.15;font-variant-numeric:tabular-nums}
.ehp-prices{width:100%;border-collapse:collapse;font-size:14px;margin:0}
.ehp-prices td{padding:7px 0;border:0;border-bottom:1px dashed var(--line);background:none!important}
.ehp-prices td:last-child{text-align:right;font-weight:700;font-variant-numeric:tabular-nums}
.ehp-row{display:flex;gap:10px;font-size:13.5px;line-height:1.45}
.ehp-row i{flex:0 0 18px;text-align:center;color:var(--b2);font-style:normal;padding-top:1px}
.ehp-row small{display:block;color:var(--mut);font-size:11.5px;text-transform:uppercase;letter-spacing:.04em;font-weight:600}
.ehp-bonus{background:#fff8dc;border-radius:10px;padding:10px 12px;font-size:13px;line-height:1.5}
.ehp-bonus b{display:block;font-size:11.5px;letter-spacing:.05em;text-transform:uppercase;color:#7a5a00}
.ehp-bonus ul{margin:4px 0 0;padding-left:18px}
.ehp-note{font-size:12.5px;font-weight:600;color:#7a5a00}
.ehp-cta{margin-top:auto;display:flex;align-items:center;justify-content:center;gap:8px;background:#25D366;color:#fff!important;font-weight:700;font-size:15px;padding:13px;border-radius:10px;text-decoration:none;transition:.2s}
.ehp-cta:hover{background:#1da851}
.ehp-inc{max-width:1200px;margin:0 auto;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px}
.ehp-box{background:#fff;border-radius:16px;padding:24px;box-shadow:0 6px 20px rgba(0,20,60,.08)}
.ehp-box h4{font-family:Raleway,sans-serif;font-weight:800;font-size:19px;margin:0 0 12px;color:var(--b)}
.ehp-box ul,.ehp-box ol{margin:0;padding-left:20px;font-size:14px;line-height:1.7;color:var(--ink)}
.ehp-bank{margin-top:14px;background:#eef4ff;border-radius:10px;padding:12px 14px;font-size:14px;line-height:1.6}
@media (max-width:1024px){.ehp-grid,.ehp-inc{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:640px){.ehp-grid,.ehp-inc{grid-template-columns:1fr}.ehp-head h3{font-size:23px}.ehp-nav{margin-bottom:28px}.ehp-nav a{font-size:13px;padding:8px 14px}.ehp-period{margin-bottom:48px}}
</style>
'''


def card(p, period):
    minp = min(p['prices'])
    msg = f"Assalamu'alaikum Elharamain Wisata, saya tertarik dengan {p['name']} ({period['label']}) keberangkatan {html.unescape(p['dates'].replace('<br>', ' / '))}. Mohon info lebih lanjut."
    wa = f"https://api.whatsapp.com/send?phone={WA}&text={urllib.parse.quote(msg)}"
    rows = ''.join(f'<tr><td>{lbl}</td><td>{rp(v)}</td></tr>' for lbl, v in zip(('Sekamar ber-4 (Quad)', 'Sekamar ber-3 (Triple)', 'Sekamar ber-2 (Double)'), p['prices']))
    bonus = ''
    if p['bonus']:
        bonus = '<div class="ehp-bonus"><b>Bonus Paket</b><ul>' + ''.join(f'<li>{b}</li>' for b in p['bonus']) + '</ul></div>'
    note = f'<div class="ehp-note">★ {p["note"]}</div>' if p['note'] else ''
    return f'''<article class="ehp-card" data-tier="{p['tier']}">
<div class="ehp-top"><div class="ehp-tier">{p['tier'].title()} · Hotel Bintang 5</div><h4>{p['name']}</h4>
<div class="ehp-chips"><span>{p['days']} Hari</span><span>{period['airline']}</span><span>+ Thaif</span></div></div>
<div class="ehp-body">
<div class="ehp-from">Mulai dari<b>{rp(minp)}</b></div>
<table class="ehp-prices"><tbody>{rows}</tbody></table>
<div class="ehp-row"><i>📅</i><div><small>Keberangkatan</small>{p['dates']}</div></div>
<div class="ehp-row"><i>✈️</i><div><small>Rute</small>{p['route']}</div></div>
<div class="ehp-row"><i>🕌</i><div><small>Hotel Madinah</small>{p['mad']}</div></div>
<div class="ehp-row"><i>🕋</i><div><small>Hotel Makkah</small>{p['mak']}</div></div>
{note}{bonus}
<a class="ehp-cta" href="{wa}" target="_blank" rel="noopener">Tanya / Daftar via WhatsApp</a>
</div></article>'''


def period_html(pr, with_css=False, with_nav=False):
    out = CSS if with_css else ''
    out += '<div class="ehp">'
    if with_nav:
        out += '<nav class="ehp-nav">' + ''.join(f'<a href="#{x["id"]}">{x["label"]}</a>' for x in PERIODS) + '</nav>'
    kicker = f'<span class="ehp-kicker">{pr["badge"]}</span>' if pr.get('badge') else f'<span class="ehp-kicker">{pr["label"]}</span>'
    out += f'''<section class="ehp-period" id="{pr['id']}"><div class="ehp-head"><div>{kicker}<h3>{pr['title']}</h3><p>{pr['sub']}</p></div>
<a class="ehp-pdf" href="{pr['pdf']}" target="_blank" rel="noopener">⬇ Download Brosur (PDF)</a></div>
<div class="ehp-grid">{''.join(card(p, pr) for p in pr['items'])}</div></section></div>'''
    return out


TAB_CSS = r'''<style>
.ehp-tabs-r{position:absolute;opacity:0;pointer-events:none}
.ehp-tabs{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin:0 auto 36px;max-width:1100px}
.ehp-tabs label{cursor:pointer;background:rgba(255,255,255,.12);border:1.5px solid rgba(255,255,255,.4);color:#fff;padding:12px 22px;border-radius:12px;font-weight:600;font-size:15px;line-height:1.25;text-align:center;transition:.2s;user-select:none}
.ehp-tabs label small{display:block;font-size:12px;font-weight:500;opacity:.8}
.ehp-tabs label:hover{background:rgba(255,255,255,.22)}
.ehp-panel{display:none}
''' + ''.join(
    f'#ehp-t-{p["id"]}:checked~.ehp-tabs label[for=ehp-t-{p["id"]}]{{background:#fff;color:#004AAD;border-color:#fff;box-shadow:0 6px 18px rgba(0,0,0,.18)}}'
    f'#ehp-t-{p["id"]}:checked~.ehp-panels [data-tab={p["id"]}]{{display:block}}\n' for p in PERIODS) + r'''
#ehp-t-november-2026:focus-visible~.ehp-tabs label[for=ehp-t-november-2026]{outline:2px solid #dbc033}
@media (max-width:640px){.ehp-tabs{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:26px}.ehp-tabs label{padding:10px 8px;font-size:13.5px}}
</style>'''

TAB_JS = '''<script>(function(){function pick(){var h=(location.hash||'').slice(1);var r=h&&document.getElementById('ehp-t-'+h);if(r){r.checked=true;var w=document.getElementById('paket-umroh');if(w)w.scrollIntoView();}}
pick();window.addEventListener('hashchange',pick);document.querySelectorAll('.ehp-tabs-r').forEach(function(r){r.addEventListener('change',function(){if(history.replaceState)history.replaceState(null,'','#'+r.value);});});})();</script>'''


def tabs_html():
    out = CSS + TAB_CSS + '<div class="ehp">'
    out += ''.join(f'<input type="radio" class="ehp-tabs-r" name="ehp-tab" id="ehp-t-{p["id"]}" value="{p["id"]}"{" checked" if i == 0 else ""}>' for i, p in enumerate(PERIODS))
    out += '<div class="ehp-tabs" role="tablist">' + ''.join(
        f'<label for="ehp-t-{p["id"]}" role="tab">{p["label"]}<small>{len(p["items"])} paket</small></label>' for p in PERIODS) + '</div>'
    out += '<div class="ehp-panels">'
    for p in PERIODS:
        inner = period_html(p)
        inner = inner[len('<div class="ehp">'):-len('</div>')]
        out += f'<div class="ehp-panel" data-tab="{p["id"]}">{inner}</div>'
    return out + '</div></div>' + TAB_JS


INCLUDED = '''<div class="ehp"><div class="ehp-inc">
<div class="ehp-box"><h4>Harga Sudah Termasuk</h4><ul>
<li>Tiket pesawat PP kelas ekonomi</li><li>Visa umroh &amp; asuransi perjalanan</li><li>Hotel bintang 5 sesuai paket, makan fullboard 3x sehari</li>
<li>Perlengkapan umroh eksklusif</li><li>Manasik di hotel berbintang &amp; VIP Lounge Umroh Soekarno-Hatta</li><li>Airport tax &amp; handling bandara</li>
<li>Bus terbaru, pembimbing &amp; mutawwif berpengalaman</li><li>Fasilitasi umroh sampai 3x dengan Audio Hajj</li>
<li>Free citytour Thaif, ATV &amp; naik unta di Madinah</li><li>Kuliner Nasi Mandhi + Kunafa</li>
<li>Bagasi 35 kg, air zamzam 5 liter</li><li>Album foto, sertifikat umroh &amp; gift Elharamain</li></ul></div>
<div class="ehp-box"><h4>Belum Termasuk</h4><ul>
<li>Pembuatan paspor</li><li>Suntik meningitis &amp; polio</li><li>Keperluan pribadi</li><li>Kelebihan bagasi</li>
<li>Penyesuaian biaya akibat kebijakan terbaru kedua negara (kesehatan, tiket, hotel, visa)</li></ul>
<h4 style="margin-top:20px">Dokumen yang Dibutuhkan</h4><ul>
<li>Paspor berlaku min. 10 bulan, nama min. 2 suku kata</li><li>Pas foto 4x6</li><li>Fotokopi KTP &amp; KK</li><li>Fotokopi buku nikah (suami-istri)</li><li>Sertifikat vaksin &amp; BPJS</li></ul></div>
<div class="ehp-box"><h4>Cara Pendaftaran</h4><ol>
<li>DP <b>Rp 6.000.000</b> / jamaah untuk booking seat</li><li>Pelunasan paling lambat <b>35 hari</b> sebelum keberangkatan</li>
<li>Reschedule maksimal 40 hari sebelum keberangkatan</li></ol>
<div class="ehp-bank">Pembayaran <b>hanya sah</b> ke rekening a.n.<br><b>PT Dhiyaa El Haramain El Mubarakah</b><br>Bank Mandiri: <b>156.001.150.115.4</b><br>Bank BSI: <b>710.857.755.4</b></div>
<p style="font-size:12px;color:#5b6b84;margin:12px 0 0">Harga dapat berubah mengikuti kebijakan Arab Saudi &amp; kurs (asumsi maks. Rp 17.000/USD). Hotel dapat diganti dengan hotel setaraf bila penuh.</p></div>
</div></div>'''

# ---------- build elementor data ----------
used = set()
def nid():
    while True:
        i = f'{random.getrandbits(28):07x}'
        if i not in used:
            used.add(i); return i

def widget(wtype, settings):
    return {'id': nid(), 'elType': 'widget', 'widgetType': wtype, 'settings': settings, 'elements': [], 'isInner': False}

def section(elements, settings, inner=False):
    return {'id': nid(), 'elType': 'section', 'isInner': inner, 'settings': settings,
            'elements': [{'id': nid(), 'elType': 'column', 'isInner': inner, 'settings': {'_column_size': 100, '_inline_size': None}, 'elements': elements}]}

home = json.load(open(HOME_EL))
data = copy.deepcopy(home)
idx = next(i for i, e in enumerate(data) if e['id'] == '472c0642')
old = data[idx]
heading_block = copy.deepcopy(old['elements'][0]['elements'][0])  # title + divider + subtitle
h = heading_block['elements'][0]['elements']
h[0]['settings']['title'] = 'Paket Umroh Musim Dingin 2026/2027'
h[0]['settings']['header_size'] = 'h2'

# hero: H1 khusus halaman ini (homepage asli tidak diubah)
def byid(n, i):
    for e in n:
        if e['id'] == i: return e
        r = byid(e.get('elements', []), i)
        if r: return r
byid(data, '399d789c')['settings']['title'] = 'Paket Umroh Desember 2026 & Januari 2027'
byid(data, '6a4aede1')['settings']['title'] = 'Pilihan paket umroh musim dingin bersama Elharamain Wisata: hotel bintang 5, penerbangan Saudia Airlines & Riyadh Air, program Thaif dan kereta cepat, dibimbing asatidz lulusan Timur Tengah.'
byid(data, '6a4aede1')['settings']['header_size'] = 'p'
h[2]['settings']['editor'] = '<p>November 2026 · Desember 2026 · Januari 2027 — Hotel Bintang 5</p>'

pkg_settings = copy.deepcopy(old['settings'])
pkg_settings['_element_id'] = 'paket-umroh'
pkg_settings['padding_mobile'] = {'unit': 'px', 'top': '50', 'right': '16', 'bottom': '50', 'left': '16', 'isLinked': False}
widgets = [heading_block]
widgets.append(widget('html', {'html': tabs_html()}))
pkg = {'id': nid(), 'elType': 'section', 'isInner': False, 'settings': pkg_settings,
       'elements': [{'id': nid(), 'elType': 'column', 'isInner': False, 'settings': {'_column_size': 100, '_inline_size': None}, 'elements': widgets}]}

inc_title = copy.deepcopy(heading_block)
def reid(e):
    e['id'] = nid()
    for c in e.get('elements', []): reid(c)
reid(inc_title)
t = inc_title['elements'][0]['elements']
t[0]['settings']['title'] = 'Fasilitas & Ketentuan Paket'
t[0]['settings']['title_color'] = '#004AAD'
t[2]['settings']['editor'] = '<p>Berlaku untuk seluruh paket di atas</p>'
t[2]['settings'].pop('text_color', None)
inc = section([inc_title, widget('html', {'html': INCLUDED})],
              {'background_background': 'classic', 'background_color': '#F3F7FD',
               'padding': {'unit': 'px', 'top': '70', 'right': '0', 'bottom': '70', 'left': '0', 'isLinked': False},
               'padding_mobile': {'unit': 'px', 'top': '50', 'right': '16', 'bottom': '50', 'left': '16', 'isLinked': False},
               'content_width': {'unit': 'px', 'size': 1240, 'sizes': []}})

data[idx:idx + 1] = [pkg, inc]

# hero CTA -> jump to packages; keep WA button elsewhere
json.dump(data, open(S + 'new_el.json', 'w'), ensure_ascii=False)
open(S + 'preview.html', 'w').write('<html><head><meta name=viewport content="width=device-width,initial-scale=1"><link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&family=Raleway:wght@800&display=swap" rel=stylesheet></head><body style="margin:0;background:#004AAD;padding:40px 16px">'
    + '<div id="paket-umroh">' + tabs_html() + '</div>' +'<div style="background:#F3F7FD;padding:40px 0;margin:40px -16px 0">' + INCLUDED + '</div></body></html>')
print('ok', sum(len(p['items']) for p in PERIODS), 'paket')
