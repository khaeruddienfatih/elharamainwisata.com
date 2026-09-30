"""Buat/perbarui halaman "Lokasi Kantor" (3 situs) dan "Tentang Kami" (elharamainhaji.com, elharamain.id).

Isi: HTML statis dalam blok wp:html, template page_landingpress.php (header/footer UAE tampil).
Teks Tentang Kami dari brosur PDF resmi (data/brosur/), atas arahan pemilik. Data kantor: tools/build_footer.py.
Usage: python3 tools/build_info_pages.py [--publish]   (tanpa --publish: hanya tulis preview ke build/)"""
import html
import os
import sys
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from build_footer import OFFICES  # noqa: E402
from deploy_uae import rest  # noqa: E402

# Urutan sesuai daftar pemilik (30 Sep 2026)
ORDER = ['Bekasi', 'Depok', 'Tangerang', 'Jakarta', 'Bandung', 'Bogor']
OFF = sorted(OFFICES, key=lambda o: ORDER.index(o[0]))

CSS = '''<style>
.ehp{--b:#004AAD;--n:#0a2e6b;--g:#DBC033;font-family:Poppins,sans-serif;color:#26364d;max-width:1100px;margin:0 auto;padding:48px 20px 64px;line-height:1.7}
.ehp *{box-sizing:border-box}
.ehp h1,.ehp h2,.ehp h3{font-family:Poppins,sans-serif!important;font-weight:700!important;text-transform:none!important}
.ehp h1{font-size:34px;line-height:1.2;color:var(--n);margin:0 0 8px;text-align:center}
.ehp .sub{text-align:center;color:#5a6b85;margin:0 auto 36px;max-width:640px}
.ehp h2{font-size:22px;color:var(--n);margin:36px 0 12px}
.ehp-g{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.ehp-c{background:#fff;border:1px solid #e1e8f3;border-radius:14px;padding:20px;box-shadow:0 8px 24px rgba(0,74,173,.06);display:flex;flex-direction:column}
.ehp-c h3{font-size:17px;color:var(--n);margin:0 0 8px}
.ehp-c p{margin:0 0 14px;font-size:14.5px;flex:1}
.ehp-a{display:flex;gap:8px;flex-wrap:wrap}
.ehp-a a{display:inline-flex;align-items:center;justify-content:center;padding:9px 14px;border-radius:10px;font-weight:600;font-size:13.5px;text-decoration:none}
.ehp-wa{background:#25D366;color:#fff!important}.ehp-wa:hover{background:#1da851}
.ehp-mp{background:#eef4fc;color:var(--b)!important}.ehp-mp:hover{background:#dce8f8}
.ehp-box{background:#f5f8fd;border-left:4px solid var(--b);border-radius:10px;padding:18px 20px;margin:14px 0}
.ehp ul{padding-left:20px;margin:8px 0}.ehp li{margin:6px 0}
.ehp-cta{text-align:center;margin-top:40px}
.ehp-cta a{display:inline-block;background:#25D366;color:#fff!important;font-weight:700;padding:14px 28px;border-radius:12px;text-decoration:none}
@media(max-width:900px){.ehp-g{grid-template-columns:1fr 1fr}}
@media(max-width:600px){.ehp{padding:32px 16px 48px}.ehp h1{font-size:27px}.ehp-g{grid-template-columns:1fr}}
</style>'''


WA_HI = "Assalamu'alaikum Elharamain Wisata "


def wa(phone, text=None):
    u = 'https://wa.me/62' + phone.replace('-', '').lstrip('0')
    return u + ('?text=' + urllib.parse.quote(text) if text else '')


def maps(addr):
    return 'https://www.google.com/maps/search/?api=1&query=' + urllib.parse.quote('Elharamain Wisata ' + addr)


def lokasi(haji_only=False):
    cards = ''.join(
        f'<div class="ehp-c"><h3>📍 {html.escape(label.replace("Kantor Pusat Bekasi", "Kantor Pusat (Bekasi)"))}</h3>'
        f'<p>{html.escape(addr)}<br>📞 {phone}</p><div class="ehp-a">'
        f'<a class="ehp-wa" href="{wa(phone, WA_HI + city)}" target="_blank" rel="noopener">WhatsApp</a>'
        f'<a class="ehp-mp" href="{maps(addr)}" target="_blank" rel="noopener">Lihat Peta</a></div></div>'
        for city, label, addr, phone, _l in OFF)
    layanan = 'Haji Plus' if haji_only else 'Haji Plus dan Umroh'
    izin = '' if haji_only else 'Izin Umrah SK Kemenag No. 63 Tahun 2020 · '
    return (f'{CSS}<div class="ehp"><h1>Lokasi Kantor Kami</h1>'
            f'<p class="sub">Kunjungi kantor Elharamain Wisata terdekat untuk konsultasi langsung. '
            f'Semua kantor melayani pendaftaran {layanan}.</p>'
            f'<div class="ehp-g">{cards}</div>'
            f'<div class="ehp-box"><b>PT Dhiyaa El Haramain El Mubarakah</b><br>'
            f'{izin}Izin Haji Plus (PIHK) SK Kemenag No. 846 Tahun 2020</div></div>')


def tentang():
    """Isi dari brosur PDF resmi (data/brosur/*.pdf, update Sep 2026): 4 keunggulan sampul, fasilitas, oleh-oleh, kantor."""
    wa_hq = wa(OFF[0][3], "Assalamu'alaikum Elharamain Wisata, saya ingin konsultasi.")
    pilar = [('✈️', 'Penerbangan Langsung', 'Direct flight Saudia Airlines dan penerbangan premium Riyadh Air.'),
             ('🏨', 'Hotel Bintang Lima', 'Menginap di hotel bintang lima di Makkah dan Madinah.'),
             ('📖', 'Bimbingan Sesuai Sunnah', 'Program ibadah dibimbing secara intensif dan sesuai sunnah.'),
             ('🤝', 'Pelayanan Utama', 'Mengedepankan pelayanan dan kenyamanan untuk jamaah.')]
    layanan = ['Manasik umroh di hotel berbintang', 'Pembimbing &amp; mutawwif berpengalaman',
               'Visa umroh dan asuransi perjalanan', 'Umroh dan kajian menggunakan aplikasi Audio Hajj',
               'Fasilitasi umroh sampai 3x', 'Program tahajjud bersama &amp; kajian',
               'Free city tour Thaif &amp; kuliner Arab Saudi', 'Perlengkapan umroh eksklusif (koper, ihram/mukena, buku panduan &amp; doa, dll.)']
    oleh = 'Album foto, kurma Ajwa &amp; Sukkari, cokelat, parfum eksklusif, sertifikat umroh, tumbler, dan air zamzam.'
    cards = ''.join(f'<div class="ehp-c"><h3>{i} {t}</h3><p>{d}</p></div>' for i, t, d in pilar)
    kantor = ', '.join(c for c, *_ in OFF)
    return (f'{CSS}<div class="ehp"><h1>Tentang Kami</h1>'
            f'<p class="sub"><b>Umroh lebih nyaman dan berkesan bersama Elharamain Wisata.</b> Kami melayani perjalanan '
            f'ibadah Umroh dan Haji Plus di bawah naungan PT Dhiyaa El Haramain El Mubarakah.</p>'
            f'<div class="ehp-g" style="grid-template-columns:repeat(auto-fit,minmax(220px,1fr))">{cards}</div>'
            f'<h2>Layanan untuk Jamaah</h2><ul>' + ''.join(f'<li>{x}</li>' for x in layanan) + '</ul>'
            f'<h2>Oleh-oleh dari Elharamain</h2><p>{oleh}</p>'
            f'<h2>Legalitas</h2><div class="ehp-box">PT Dhiyaa El Haramain El Mubarakah — Izin Umrah SK Kemenag No. 63 '
            f'Tahun 2020 · Izin Haji Plus (PIHK) SK Kemenag No. 846 Tahun 2020.</div>'
            f'<h2>Kantor Kami</h2><p>Elharamain Wisata hadir di {kantor}. '
            f'<a href="/lokasi-kantor/">Lihat alamat, peta &amp; kontak semua kantor →</a></p>'
            f'<div class="ehp-cta"><a href="{wa_hq}" target="_blank" rel="noopener">Konsultasi Gratis via WhatsApp</a></div></div>')


PAGES = [  # situs, slug, judul, isi
    ('hajibiz', 'lokasi-kantor', 'Lokasi Kantor', lokasi(haji_only=True)),
    ('elharamainhaji', 'lokasi-kantor', 'Lokasi Kantor', lokasi()),
    ('elharamainid', 'lokasi-kantor', 'Lokasi Kantor', lokasi()),
    ('elharamainhaji', 'tentang-kami', 'Tentang Kami', tentang()),
    ('elharamainid', 'tentang-kami', 'Tentang Kami', tentang()),
]


def upsert(site, slug, title, body):
    content = f'<!-- wp:html -->\n{body}\n<!-- /wp:html -->'
    found = rest(site, 'GET', f'/wp/v2/pages?slug={slug}&status=publish,draft&_fields=id,status')
    data = {'title': title, 'slug': slug, 'content': content, 'status': 'publish', 'template': 'page_landingpress.php'}
    if found:
        r = rest(site, 'POST', f'/wp/v2/pages/{found[0]["id"]}', data)
    else:
        r = rest(site, 'POST', '/wp/v2/pages', data)
    return r['id'], r['status'], r['link']


if __name__ == '__main__':
    os.makedirs(os.path.join(ROOT, 'build'), exist_ok=True)
    for site, slug, title, body in PAGES:
        prev = os.path.join(ROOT, 'build', f'page-{site}-{slug}.html')
        open(prev, 'w').write('<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width">' + body)
        if '--publish' in sys.argv:
            print(site, slug, *upsert(site, slug, title, body))
        else:
            print('preview', os.path.relpath(prev, ROOT))
