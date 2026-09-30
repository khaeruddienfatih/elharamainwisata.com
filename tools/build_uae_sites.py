"""Generate header/footer UAE untuk haji.biz, elharamainhaji.com, elharamain.id dari satu template.

Menu (arahan pemilik 30 Sep 2026): Home, Paket, Tentang Kami, Lokasi Kantor (+ tombol WA).
"Lokasi Kantor" = halaman /lokasi-kantor/ (tools/build_info_pages.py); footer juga memuat 6 kantor.
Aturan: haji.biz khusus haji (tanpa link umroh).
Output: wordpress/uae/<situs>-header.html & -footer.html. Pasang: tools/deploy_uae.py."""
import os
import sys
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from build_footer import OFFICES  # noqa: E402  (kota, label, alamat, telp, link)

LOGO = '/wp-content/uploads/2026/09/logo-elharamain-putih.webp'  # diunggah ke media tiap situs (30 Sep 2026)
WA = '6281287292422'

SITES = {
    'haji-biz': {
        'name': 'Haji.biz', 'about': 'Portal informasi &amp; panduan haji (haji khusus/plus) dari Elharamain Wisata.',
        'wa_text': 'Assalamu\'alaikum Elharamain Wisata, saya ingin konsultasi haji.', 'cta': 'Konsultasi Gratis',
        'tentang': '/tentang-kami/', 'izin': '',  # khusus haji: tanpa izin umrah
        'paket': [('Paket Haji Plus', '/paket-haji-plus/'),
                  ('Haji Plus 2027', '/paket-haji-plus-2027-elharamain-wisata/'),
                  ('Haji Plus 2028', '/paket-haji-plus-2028-elharamain-wisata/')],
        'sister': [('Elharamain Wisata', 'https://www.elharamainwisata.com/'),
                   ('Elharamain Haji', 'https://www.elharamainhaji.com/'), ('Elharamain.id', 'https://www.elharamain.id/')],
    },
    'elharamainhaji': {
        'name': 'Elharamain Haji', 'about': 'Pendaftaran Haji Plus (haji khusus) resmi PIHK Kemenag bersama Elharamain Wisata.',
        'wa_text': 'Assalamu\'alaikum Elharamain Wisata, saya ingin daftar Haji Plus.', 'cta': 'Daftar Haji Plus',
        'tentang': '/tentang-kami/',
        'paket': [('Paket Haji Plus', '/paket-haji-plus-elharamain-wisata/')],
        'sister': [('Elharamain Wisata', 'https://www.elharamainwisata.com/'), ('Haji.biz (Info Haji)', 'https://www.haji.biz/'),
                   ('Elharamain.id (Info Umroh)', 'https://www.elharamain.id/')],
    },
    'elharamainid': {
        'name': 'Elharamain.id', 'about': 'Informasi paket &amp; panduan umroh dari Elharamain Wisata, travel resmi Kemenag.',
        'wa_text': 'Assalamu\'alaikum Elharamain Wisata, saya ingin konsultasi umroh.', 'cta': 'Konsultasi Umroh',
        'tentang': '/tentang-kami/',
        'paket': [('Umroh Silver', '/paket-umroh-silver/'), ('Umroh Platinum', '/paket-umroh-platinum/'),
                  ('Umroh Plus Turki', '/paket-umroh-plus-turki/'), ('Umroh Plus Dubai', '/paket-umroh-plus-dubai/'),
                  ('Umroh Plus Mesir', '/paket-umroh-plus-mesir/'),
                  ('Umroh Aqso + Petra', '/paket-umroh-plus-aqso-petra-saudia-airlines-14-hari/'),
                  ('Haji Plus', '/haji-plus-elharamain-wisata/')],
        'sister': [('Elharamain Wisata', 'https://www.elharamainwisata.com/'),
                   ('Elharamain Haji', 'https://www.elharamainhaji.com/'), ('Haji.biz (Info Haji)', 'https://www.haji.biz/')],
    },
}

HEADER_CSS = '''
.bhf-hidden{display:none!important}
body.ehf-header #masthead.site-header{display:none!important}
.ehh{--hb:#004AAD;--hg:#DBC033;background:var(--hb);font-family:Poppins,sans-serif;position:relative;z-index:999}
.ehh *{box-sizing:border-box}.ehh a{text-decoration:none}
.ehh-bar{max-width:1240px;margin:0 auto;padding:10px 24px;display:flex;align-items:center;gap:24px;min-height:74px;flex-wrap:wrap}
.ehh-logo img{display:block;width:150px;height:65px;object-fit:contain}
.ehh-t,.ehh-btn{display:none}
.ehh-nav{margin-left:auto;display:flex;align-items:center;gap:4px;flex-wrap:wrap}
.ehh-nav a.l{display:block;color:#fff;font-weight:600;font-size:15px;padding:12px 14px;border-radius:8px;white-space:nowrap}
.ehh-nav a.l:hover{color:var(--hg)}
.ehh-dd{position:relative}
.ehh-dd>a.l:after{content:"";display:inline-block;margin-left:7px;border:5px solid transparent;border-top-color:currentColor;border-bottom:0;vertical-align:middle}
.ehh-sub{display:none;position:absolute;top:100%;left:0;min-width:220px;background:#fff;border-radius:10px;padding:6px;box-shadow:0 12px 32px rgba(0,40,100,.18)}
.ehh-dd:hover .ehh-sub,.ehh-dd:focus-within .ehh-sub{display:block}
.ehh-sub a{display:block;color:#0a2e6b;font-size:14px;font-weight:600;padding:10px 12px;border-radius:8px;white-space:nowrap}
.ehh-sub a:hover{background:#eef4fc;color:var(--hb)}
.ehh-cta{display:inline-flex;align-items:center;background:#25D366;color:#fff!important;font-weight:700;font-size:14px;padding:10px 16px;border-radius:10px;margin-left:8px;white-space:nowrap}
.ehh-cta:hover{background:#1da851}
@media(max-width:1024px){
 .ehh-bar{padding:8px 16px;min-height:64px;gap:12px}
 .ehh-logo img{width:120px;height:52px}
 .ehh-btn{display:flex;margin-left:auto;width:44px;height:44px;border-radius:10px;align-items:center;justify-content:center;cursor:pointer;border:1px solid rgba(255,255,255,.35)}
 .ehh-btn span,.ehh-btn span:before,.ehh-btn span:after{display:block;width:22px;height:2px;background:#fff;position:relative;content:""}
 .ehh-btn span:before{position:absolute;top:-7px}.ehh-btn span:after{position:absolute;top:7px}
 .ehh-nav{display:none;width:100%;margin:0;flex-direction:column;align-items:stretch;gap:0;padding:4px 0 10px}
 .ehh-t:checked~.ehh-nav{display:flex}
 .ehh-nav a.l{border-top:1px solid rgba(255,255,255,.12);border-radius:0;padding:13px 4px}
 .ehh-dd>a.l:after{display:none}
 .ehh-sub{display:block;position:static;min-width:0;background:none;box-shadow:none;padding:0 0 6px 14px}
 .ehh-sub a{color:#dbe6f7;font-weight:500;padding:9px 4px}
 .ehh-sub a:hover{background:none;color:var(--hg)}
 .ehh-cta{justify-content:center;margin:10px 0 0}
}
'''

FOOTER_CSS = '''
body.ehf-footer #colophon.site-footer{display:none!important}
.ehf{background:#0a2e6b;color:#dbe6f7;font-family:Poppins,sans-serif;font-size:14px;line-height:1.6}
.ehf *{box-sizing:border-box}.ehf a{color:#dbe6f7;text-decoration:none}.ehf a:hover{color:#DBC033}
.ehf-w{max-width:1240px;margin:0 auto;padding:36px 24px 18px;display:grid;grid-template-columns:1.6fr 1fr 1fr;gap:32px}
.ehf h4{color:#fff;font-size:15px;margin:0 0 10px;font-family:Poppins,sans-serif!important;font-weight:700!important}.ehf a.b{display:block;margin:5px 0}
.ehf-legal{font-size:12.5px;opacity:.85;margin-top:8px}
.ehf-k{max-width:1240px;margin:0 auto;padding:8px 24px 28px;scroll-margin-top:90px}
.ehf-kg{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.ehf-o{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:12px;padding:14px 16px;font-size:13px}
.ehf-o b{display:block;color:#fff;font-size:14px;margin-bottom:4px}
.ehf-o a.w{display:inline-block;margin-top:6px;color:#25D366;font-weight:600}
.ehf-bt{border-top:1px solid rgba(255,255,255,.18);text-align:center;padding:14px 16px;font-size:12.5px}
@media(max-width:900px){.ehf-kg{grid-template-columns:1fr 1fr}}
@media(max-width:800px){.ehf-w{grid-template-columns:1fr;padding:28px 16px 12px}.ehf-k{padding:8px 16px 24px}}
@media(max-width:560px){.ehf-kg{grid-template-columns:1fr}}
'''


def wa_digits(phone):
    return '62' + phone.replace('-', '').lstrip('0')


def header(s):
    wa = f'https://api.whatsapp.com/send?phone={WA}&amp;text=' + urllib.parse.quote(s['wa_text'])
    if len(s['paket']) == 1:
        paket = f'    <a class="l" href="{s["paket"][0][1]}">Paket</a>'
    else:
        sub = ''.join(f'<a href="{u}">{t}</a>' for t, u in s['paket'])
        paket = f'    <div class="ehh-dd"><a class="l" href="{s["paket"][0][1]}">Paket</a><div class="ehh-sub">{sub}</div></div>'
    return f'''<!-- Header {s['name']} — dibuat oleh tools/build_uae_sites.py; jangan edit manual. -->
<style>{HEADER_CSS}</style>
<header class="ehh" aria-label="Menu utama {s['name']}"><div class="ehh-bar">
  <a class="ehh-logo" href="/" aria-label="{s['name']} - Beranda"><img src="{LOGO}" alt="{s['name']} by Elharamain Wisata" width="1366" height="591" data-no-lazy="1" fetchpriority="high"></a>
  <input type="checkbox" id="ehh-t" class="ehh-t" aria-hidden="true">
  <label for="ehh-t" class="ehh-btn" aria-label="Buka menu"><span></span></label>
  <nav class="ehh-nav">
    <a class="l" href="/">Home</a>
{paket}
    <a class="l" href="{s['tentang']}">Tentang Kami</a>
    <a class="l" href="/lokasi-kantor/">Lokasi Kantor</a>
    <a class="ehh-cta" href="{wa}" target="_blank" rel="noopener">{s['cta']}</a>
  </nav>
</div></header>
'''


def footer(s):
    paket = '\n'.join(f'      <a class="b" href="{u}">{t}</a>' for t, u in s['paket'])
    sister = '\n'.join(f'      <a class="b" href="{u}">{t}</a>' for t, u in s['sister'])
    offices = '\n'.join(
        f'    <div class="ehf-o"><b>{label}</b>{addr}<br><a class="w" href="https://wa.me/{wa_digits(phone)}" '
        f'target="_blank" rel="noopener">WhatsApp {phone}</a></div>'
        for _c, label, addr, phone, _l in OFFICES)
    return f'''<!-- Footer {s['name']} — dibuat oleh tools/build_uae_sites.py; jangan edit manual. -->
<style>{FOOTER_CSS}</style>
<footer class="ehf" aria-label="Footer {s['name']}">
  <div class="ehf-w">
    <div>
      <h4>{s['name']}</h4>
      {s['about']}
      <div class="ehf-legal">PT Dhiyaa El Haramain El Mubarakah<br>{s.get('izin', 'Izin Umrah SK Kemenag No. 63 Tahun 2020<br>')}Izin Haji Plus SK Kemenag No. 846 Tahun 2020</div>
    </div>
    <div>
      <h4>Paket</h4>
{paket}
      <a class="b" href="{s['tentang']}">Tentang Kami</a>
    </div>
    <div>
      <h4>Situs Kami</h4>
{sister}
      <a class="b" href="https://www.instagram.com/elharamainwisata/" target="_blank" rel="noopener">Instagram</a>
      <a class="b" href="https://www.youtube.com/channel/UC0R5NZ1hz3qXaqrAuHIJBLg" target="_blank" rel="noopener">YouTube</a>
    </div>
  </div>
  <div class="ehf-k" id="lokasi-kantor">
    <h4>Lokasi Kantor</h4>
    <div class="ehf-kg">
{offices}
    </div>
  </div>
  <div class="ehf-bt">© 2026 Elharamain Wisata · PT Dhiyaa El Haramain El Mubarakah. All rights reserved.</div>
</footer>
'''


if __name__ == '__main__':
    for key, s in SITES.items():
        for part, fn in (('header', header), ('footer', footer)):
            p = os.path.join(ROOT, 'wordpress', 'uae', f'{key}-{part}.html')
            open(p, 'w').write(fn(s))
            print('wrote', os.path.relpath(p, ROOT))
