"""Halaman paket untuk elharamain.id (6 paket umroh) dan elharamainhaji.com (Haji Plus).

Data umroh dari data/paket-umroh.json (brosur Nov 2026-Jan 2027); data Haji Plus dari
https://www.elharamainwisata.com/paket-haji-plus/ (dibaca 30 Sep 2026).
Semua gaya inline & di-scope ke .ehp; HTML statis tanpa JavaScript (LiteSpeed menunda script).

  python3 tools/build_halaman_paket.py             -> landing-pages/situs/<situs>/<slug>.html (+ preview di build/)
  python3 tools/build_halaman_paket.py --deploy    -> juga membuat/memperbarui halaman sebagai DRAFT lewat REST
Deploy butuh env: ELHARAMAINID_WP_USER/_WP_APP_PASSWORD (elharamain.id), ELHARAMAINHAJI_WP_USER/_WP_APP_PASSWORD.
Halaman baru dibuat sebagai draft; halaman yang sudah ada (cocok slug) ditimpa isinya dengan status tetap dan
cadangan lama disimpan di backup/situs/<situs>/. Skrip tidak pernah mempublish halaman draft.
"""
import base64, html, json, os, sys, urllib.parse, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WA = '6281287292422'
IMG = 'https://res.cloudinary.com/v6gwkqrb/image/upload/c_fill,g_auto,w_700,h_500,q_auto,f_auto/'
PAKET = json.load(open(os.path.join(ROOT, 'data/paket-umroh.json'), encoding='utf-8'))['paket']

e = html.escape
rp = lambda n: 'Rp ' + f'{n:,}'.replace(',', '.')
jt = lambda n: 'Rp ' + (f'{n/1e6:g}').replace('.', ',') + ' jt'
wa = lambda t: f'https://api.whatsapp.com/send?phone={WA}&amp;text=' + urllib.parse.quote(t)

CSS = '''<style>
.ehp{--n:#1f3553;--b:#004AAD;--g:#DBC033;--m:#5b6b82;--l:#eef3fb;font-family:Poppins,sans-serif;color:var(--n);line-height:1.65;font-size:15px}
.ehp *{box-sizing:border-box}.ehp a{text-decoration:none}
.ehp-w{max-width:1200px;margin:0 auto;padding:0 24px}
.ehp-hero{background:linear-gradient(135deg,#004AAD,#1684CF);color:#fff;padding:56px 0 48px}
.ehp-hero h1{font-family:Raleway,sans-serif;font-weight:800;font-size:38px;line-height:1.2;margin:0 0 12px;color:#fff}
.ehp-hero p{margin:0 0 22px;max-width:760px;font-size:17px;opacity:.95}
.ehp-btn{display:inline-flex;align-items:center;background:#25D366;color:#fff!important;font-weight:700;padding:13px 24px;border-radius:999px}
.ehp-btn:hover{background:#1da851}
.ehp-sec{padding:44px 0}.ehp-sec.alt{background:var(--l)}
.ehp h2{font-family:Raleway,sans-serif;font-weight:800;font-size:28px;margin:0 0 6px;color:var(--n)}
.ehp .sub{color:var(--m);margin:0 0 24px}
.ehp-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}
.ehp-card{background:#fff;border:1px solid #dbe4f3;border-radius:16px;overflow:hidden;display:flex;flex-direction:column;box-shadow:0 6px 24px rgba(0,74,173,.08)}
.ehp-card .im img{display:block;width:100%;height:auto;aspect-ratio:7/5;object-fit:cover}
.ehp-card .bd{padding:18px;display:flex;flex-direction:column;gap:10px;flex:1}
.ehp-tag{align-self:flex-start;background:var(--l);color:var(--b);font-weight:700;font-size:12px;padding:3px 10px;border-radius:999px}
.ehp-card h3{margin:0;font-family:Raleway,sans-serif;font-weight:800;font-size:20px;color:var(--n)}
.ehp-card p{margin:0;color:var(--m);font-size:13.5px}
.ehp-card ul{list-style:none;margin:0;padding:0;display:grid;gap:5px;font-size:13.5px}
.ehp-card li{display:flex;justify-content:space-between;gap:12px;border-bottom:1px dashed #dbe4f3;padding-bottom:4px}
.ehp-card li span:first-child{color:var(--m)}.ehp-card li span:last-child{font-weight:600;text-align:right}
.ehp-pr{margin-top:auto}.ehp-pr small{display:block;color:var(--m);font-size:12px}
.ehp-pr b{font-family:Raleway,sans-serif;font-size:24px;color:var(--b)}
.ehp-pr em{display:block;font-style:normal;font-size:12.5px;color:var(--m)}
.ehp-card .ehp-btn{justify-content:center;padding:11px 16px;font-size:14px}
.ehp-list{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px 28px;list-style:none;margin:0;padding:0}
.ehp-list li{padding-left:26px;position:relative}
.ehp-list li::before{content:"\\2713";position:absolute;left:0;top:0;color:#fff;background:var(--b);width:18px;height:18px;border-radius:50%;font-size:11px;line-height:18px;text-align:center;top:4px}
.ehp-note{background:#fff8dc;border:1px solid var(--g);border-radius:12px;padding:14px 18px;font-size:13.5px;margin-top:20px}
.ehp-cta{background:var(--n);color:#fff;text-align:center;padding:44px 0}.ehp-cta h2{color:#fff}.ehp-cta p{margin:0 0 20px;opacity:.9}
@media(max-width:900px){.ehp-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.ehp-hero h1{font-size:30px}}
@media(max-width:600px){.ehp-w{padding:0 16px}.ehp-grid,.ehp-list{grid-template-columns:1fr}.ehp-hero{padding:40px 0 34px}.ehp-hero h1{font-size:26px}}
</style>'''

UMROH_ALASAN = ['Hotel bintang 5 di Makkah &amp; Madinah', 'Program Thaif + kereta cepat Haramain',
                'Dibimbing asatidz lulusan Timur Tengah, sesuai sunnah', 'Umroh 3x, tahajjud &amp; kajian di Tanah Suci',
                'Izin Umrah SK Kemenag No. 63 Tahun 2020', 'Anggota HIMPUH &amp; IATA, terakreditasi A oleh KAN']
KETENTUAN = ['DP pendaftaran Rp 6.000.000 per jamaah', 'Pelunasan 35 hari sebelum keberangkatan',
             'Harga per jamaah; Quad = sekamar ber-empat, Triple = ber-tiga, Double = ber-dua',
             'Harga dapat berubah sewaktu-waktu sesuai ketentuan brosur']


def kartu_umroh(p):
    teks = f'Assalamualaikum, saya mau info paket umroh {p["label"]} {p["hari"]} hari, keberangkatan {p["berangkat"]}'
    return (f'<div class="ehp-card"><div class="im"><img loading="lazy" src="{IMG}{p["img"]}.jpg" alt="Paket umroh {e(p["label"])} {p["bulan"]}"></div>'
            f'<div class="bd"><span class="ehp-tag">{p["bulan"]} · {p["hari"]} hari</span><h3>{e(p["label"])}</h3><p>{e(p["desc"])}</p>'
            f'<ul><li><span>Maskapai</span><span>{e(p["maskapai"])}</span></li><li><span>Hotel Makkah</span><span>{e(p["makkah"])} ★5</span></li>'
            f'<li><span>Hotel Madinah</span><span>{e(p["madinah"])} ★5</span></li><li><span>Berangkat</span><span>{e(p["berangkat"])}</span></li></ul>'
            f'<div class="ehp-pr"><small>Mulai dari (Quad)</small><b>{rp(p["q"])}</b><em>Triple {jt(p["t"])} · Double {jt(p["d"])}</em></div>'
            f'<a class="ehp-btn" href="{wa(teks)}" target="_blank" rel="noopener">Tanya Paket Ini via WhatsApp</a></div></div>')


def halaman(judul, sub, kartu_html, judul_kartu, alasan, ketentuan, wa_teks, catatan='', ket_judul='Ketentuan', sub_kartu='Harga per jamaah. Pilih jadwal yang paling pas untuk Anda.'):
    li = lambda xs: ''.join(f'<li>{x}</li>' for x in xs)
    return (CSS + '<div class="ehp">'
            f'<section class="ehp-hero"><div class="ehp-w"><h1>{judul}</h1><p>{sub}</p>'
            f'<a class="ehp-btn" href="{wa(wa_teks)}" target="_blank" rel="noopener">Konsultasi Gratis via WhatsApp</a></div></section>'
            f'<section class="ehp-sec"><div class="ehp-w"><h2>{judul_kartu}</h2><p class="sub">{sub_kartu}</p>'
            f'<div class="ehp-grid">{kartu_html}</div>{catatan}</div></section>'
            f'<section class="ehp-sec alt"><div class="ehp-w"><h2>Kenapa Elharamain Wisata?</h2><p class="sub">Penyelenggara resmi, pelayanan dari awal sampai pulang.</p>'
            f'<ul class="ehp-list">{li(alasan)}</ul></div></section>'
            f'<section class="ehp-sec"><div class="ehp-w"><h2>{ket_judul}</h2><ul class="ehp-list">{li(ketentuan)}</ul></div></section>'
            f'<section class="ehp-cta"><div class="ehp-w"><h2>Masih ada pertanyaan?</h2><p>Tim kami siap membantu memilih paket, jadwal, dan pembayaran.</p>'
            f'<a class="ehp-btn" href="{wa(wa_teks)}" target="_blank" rel="noopener">Hubungi Kami di WhatsApp</a></div></section></div>')


def umroh(judul, seo_title, sub, filt, wa_teks):
    ps = [p for p in PAKET if filt(p)]
    lo = min(p['q'] for p in ps)
    return dict(title=seo_title, body=halaman(judul, sub.format(lo=jt(lo)), ''.join(map(kartu_umroh, ps)),
                                              f'{len(ps)} Pilihan Jadwal &amp; Harga', UMROH_ALASAN, KETENTUAN, wa_teks),
                n=len(ps))


HAJI = [('Haji Plus Bintang 4', 12000, 'Royal Majestik ★4', 'Concorde Dar Alkhair ★4'),
        ('Haji Plus Bintang 5 · Paket A', 15500, 'Marwa Rotana ★5', 'Al-Aqiq Hotel ★5'),
        ('Haji Plus Bintang 5 · Paket B', 17000, 'Marwa Rotana ★5', 'Al-Aqiq Hotel ★5')]


def kartu_haji(nama, usd, mk, md):
    teks = f'Assalamualaikum, saya mau info {nama} (USD {usd:,})'.replace(',', '.')
    return (f'<div class="ehp-card"><div class="bd"><span class="ehp-tag">Estimasi berangkat 2027</span><h3>{e(nama)}</h3>'
            f'<ul><li><span>Hotel Makkah</span><span>{mk}</span></li><li><span>Hotel Madinah</span><span>{md}</span></li>'
            f'<li><span>Akomodasi</span><span>Apartemen Aziziyah</span></li><li><span>Armina</span><span>Maktab tenda ± 500 m</span></li>'
            f'<li><span>Pesawat</span><span>Saudia / Qatar / Emirates</span></li><li><span>Pembimbing</span><span>Terbaik</span></li></ul>'
            f'<div class="ehp-pr"><small>Biaya paket</small><b>USD {usd:,}</b><em>Estimasi keberangkatan 2027</em></div>'
            f'<a class="ehp-btn" href="{wa(teks)}" target="_blank" rel="noopener">Tanya Paket Ini via WhatsApp</a></div></div>').replace(f'USD {usd:,}', f'USD {usd:,}'.replace(',', '.'))


HAJI_ALASAN = ['Penyelenggara resmi PIHK, SK Kemenag No. 846 Tahun 2020', 'Masa tunggu lebih singkat, sekitar 5-9 tahun (reguler 22-40 tahun)',
               'Porsi resmi Kemenag, setoran USD 4.000 tanpa biaya tersembunyi', 'Pendaftaran cukup 8 hari kerja, dokumen bisa dikirim online',
               'Gratis voucher umrah Rp 5 juta selama masa tunggu', 'Program cicilan haji plus untuk mendapatkan nomor porsi',
               'Anggota HIMPUH &amp; IATA, terakreditasi A oleh KAN', 'Hotel bintang 4 &amp; 5, pembimbing ibadah berpengalaman']
HAJI_KET = ['Biaya paket adalah estimasi untuk keberangkatan tahun 2027', 'Biaya paket keseluruhan diinformasikan 1 tahun sebelum tahun keberangkatan',
            'Program cicilan tersedia; tanyakan simulasi ke tim kami']
HAJI_WA = "Assalamualaikum Elharamain Wisata, saya ingin konsultasi daftar haji plus."

PAGES = {
    'elharamain-id': [  # situs info umroh
        ('paket-umroh-musim-dingin-2026-2027', umroh('Paket Umroh Musim Dingin 2026/2027', 'Paket Umroh Musim Dingin 2026/2027 | Elharamain Wisata',
            'Umroh November 2026 - Januari 2027, hotel bintang 5, program Thaif &amp; kereta cepat. Mulai {lo}.', lambda p: True, 'Assalamualaikum, saya ingin info paket umroh musim dingin 2026/2027.')),
        ('umroh-bronze', umroh('Paket Umroh Bronze', 'Paket Umroh Bronze Nov 2026 & Jan 2027 | Elharamain Wisata',
            'Paket umroh hemat hotel bintang 5, mulai {lo}.', lambda p: p['tier'] == 'bronze', 'Assalamualaikum, saya ingin info paket umroh Bronze.')),
        ('paket-umroh-silver', umroh('Paket Umroh Silver', 'Paket Umroh Silver Des 2026 & Jan 2027 | Elharamain Wisata',
            'Paket umroh Silver 9 hari, hotel bintang 5, Thaif &amp; kereta cepat, mulai {lo}.', lambda p: p['tier'] == 'silver' and p['hari'] == 9, 'Assalamualaikum, saya ingin info paket umroh Silver.')),
        ('paket-umroh-platinum', umroh('Paket Umroh Platinum', 'Paket Umroh Platinum Des 2026 & Jan 2027 | Elharamain Wisata',
            'Umroh Platinum: Marwa Rotana / Movenpick, bonus hotel H-1, abaya &amp; jaket eksklusif, mulai {lo}.', lambda p: p['tier'] == 'platinum', 'Assalamualaikum, saya ingin info paket umroh Platinum.')),
        ('umroh-premium', umroh('Paket Umroh Premium', 'Paket Umroh Premium Januari 2027 | Elharamain Wisata',
            'Umroh Premium dengan Fairmont Makkah &amp; Movenpick Madinah, mulai {lo}.', lambda p: p['tier'] == 'premium', 'Assalamualaikum, saya ingin info paket umroh Premium.')),
        ('umroh-silver-12-hari', umroh('Paket Umroh Silver 12 Hari', 'Paket Umroh Silver 12 Hari Des 2026 & Jan 2027 | Elharamain Wisata',
            'Umroh 12 hari lebih santai, hotel bintang 5, mulai {lo}.', lambda p: p['tier'] == 'silver' and p['hari'] == 12, 'Assalamualaikum, saya ingin info paket umroh Silver 12 Hari.')),
    ],
    'elharamainhaji-com': [  # situs jualan haji
        ('paket-haji-plus', dict(title='Paket Haji Plus 2027 Resmi PIHK Kemenag | Elharamain Haji', n=3,
            body=halaman('Paket Haji Plus Resmi PIHK Kemenag', 'Masa tunggu 5-9 tahun, fasilitas hotel bintang 4 &amp; 5, pembimbing berpengalaman. Kuota terbatas.',
                         ''.join(kartu_haji(*h) for h in HAJI), '3 Pilihan Paket Haji ONH Plus', HAJI_ALASAN, HAJI_KET, HAJI_WA, ket_judul='Catatan Biaya', sub_kartu='Biaya paket per jamaah dalam USD. Pilih sesuai kelas hotel yang Anda inginkan.',
                         catatan='<div class="ehp-note">Biaya paket di atas adalah estimasi keberangkatan tahun 2027. Untuk detail dan simulasi cicilan, hubungi tim kami.</div>'))),
    ],
}
ENV = {'elharamain-id': ('https://www.elharamain.id', 'ELHARAMAINID'), 'elharamainhaji-com': ('https://www.elharamainhaji.com', 'ELHARAMAINHAJI')}


def deploy(situs, slug, pg):
    base, pre = ENV[situs]
    auth = 'Basic ' + base64.b64encode(f"{os.environ[pre + '_WP_USER']}:{os.environ[pre + '_WP_APP_PASSWORD']}".encode()).decode()

    def call(m, u, b=None):
        r = urllib.request.Request(base + '/wp-json' + u, method=m, data=None if b is None else json.dumps(b).encode(),
                                   headers={'Authorization': auth, 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 eh-admin'})
        try:
            raw = urllib.request.urlopen(r, timeout=120).read().decode('utf-8', 'replace')
        except urllib.error.HTTPError as ex:
            sys.exit(f'HTTP {ex.code} {m} {u}: ' + ex.read().decode('utf-8', 'replace')[:600])
        # server kadang menyelipkan <style> Elementor / notice PHP sebelum JSON: cari awal JSON sebenarnya
        dec = json.JSONDecoder()
        for i in range(len(raw)):
            if raw[i:i + 2] in ('{"', '[{', '[]') or raw[i:i + 4] == 'null':
                try:
                    return dec.raw_decode(raw[i:])[0]
                except ValueError:
                    continue
        if not raw.strip():
            return None
        sys.exit(f'Jawaban bukan JSON untuk {m} {u}: ' + raw[:600])
    data = [{'id': 'a0' + slug[:6].replace('-', 'x'), 'elType': 'section', 'isInner': False, 'settings': {'layout': 'full_width', 'gap': 'no',
             'padding': {'unit': 'px', 'top': '0', 'right': '0', 'bottom': '0', 'left': '0', 'isLinked': True}},
             'elements': [{'id': 'b0' + slug[:6].replace('-', 'x'), 'elType': 'column', 'isInner': False, 'settings': {'_column_size': 100},
                           'elements': [{'id': 'c0' + slug[:6].replace('-', 'x'), 'elType': 'widget', 'widgetType': 'html', 'isInner': False,
                                         'settings': {'html': pg['body']}, 'elements': []}]}]}]
    body = {'title': pg['title'].split(' | ')[0], 'slug': slug, 'template': 'elementor_header_footer',
            'meta': {'_elementor_edit_mode': 'builder', '_elementor_data': json.dumps(data, ensure_ascii=True),
                     'rank_math_title': pg['title']}}
    ada = call('GET', f'/wp/v2/pages?slug={slug}&status=any&context=edit&_fields=id,status')
    if ada:
        lama = call('GET', f'/wp/v2/pages/{ada[0]["id"]}?context=edit')
        bk = os.path.join(ROOT, 'backup', 'situs', situs)
        os.makedirs(bk, exist_ok=True)
        with open(os.path.join(bk, f'{ada[0]["id"]}-{slug}-sebelum.json'), 'w', encoding='utf-8') as f:
            json.dump(lama, f, ensure_ascii=False, indent=1)
        print(f'  cadangan halaman lama id {ada[0]["id"]} ({ada[0]["status"]}) disimpan di backup/situs/{situs}/')
        body.pop('template')  # halaman lama: pertahankan template-nya
        r = call('POST', f'/wp/v2/pages/{ada[0]["id"]}', body)   # status tidak diubah (draft tetap draft, publish tetap publish)
    else:
        r = call('POST', '/wp/v2/pages', dict(body, status='draft'))
    call('DELETE', '/elementor/v1/cache')
    print(f'  {situs}/{slug} -> id {r["id"]} ({r["status"]}) {r["link"]}')


if __name__ == '__main__':
    os.makedirs(os.path.join(ROOT, 'build'), exist_ok=True)
    for situs, pages in PAGES.items():
        os.makedirs(os.path.join(ROOT, 'landing-pages/situs', situs), exist_ok=True)
        for slug, pg in pages:
            open(os.path.join(ROOT, 'landing-pages/situs', situs, slug + '.html'), 'w', encoding='utf-8').write(pg['body'])
            open(os.path.join(ROOT, 'build', f'preview-{situs}-{slug}.html'), 'w', encoding='utf-8').write(
                '<html><head><meta name=viewport content="width=device-width,initial-scale=1"></head><body style="margin:0">' + pg['body'] + '</body></html>')
            print(situs, slug, pg['n'], 'paket', len(pg['body']), 'char')
            if '--deploy' in sys.argv:
                deploy(situs, slug, pg)
