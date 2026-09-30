"""Footer per situs untuk haji.biz, elharamainhaji.com, elharamain.id (ditempel manual di UAE > Footer).

Desain, data kantor & izin sama dengan footer elharamainwisata.com (tools/build_footer.py, tidak diubah);
yang beda per situs: ajakan (CTA), deskripsi, dua kolom tautan, dan logo/nama di baris hak cipta.
Tanpa CSS penyembunyi footer LandingPress dan tanpa JSON-LD (schema organisasi cukup di situs utama).
Usage: python3 tools/build_footer_situs.py  -> wordpress/uae/<situs>-footer.html + build/preview-footer-<situs>.html
"""
import os, re, sys, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_footer as bf

MAIN = bf.SITE
HAJI_BIZ, HAJI, ID = 'https://www.haji.biz', 'https://www.elharamainhaji.com', 'https://www.elharamain.id'
SITUS_KAMI = [('Elharamain Wisata (Web Utama)', MAIN + '/'), ('Elharamain Haji (Daftar Haji Plus)', HAJI + '/'),
              ('Haji.biz (Info Haji)', HAJI_BIZ + '/'), ('Elharamain.id (Info Umroh)', ID + '/')]
KANTOR = [(f'Travel Umroh {c}', f'{MAIN}/travel-umroh-{c.lower()}/') for c, *_ in bf.OFFICES] + [('Semua Kantor Cabang', MAIN + '/kantor-cabang/')]

SITES = {
    'haji-biz': dict(
        nama='Haji.biz', wa='Assalamu\'alaikum Elharamain Wisata, saya ingin konsultasi haji plus.',
        cta=('Ingin tahu haji plus lebih jauh?', 'Tanya syarat, biaya &amp; masa tunggu haji khusus langsung ke tim resmi kami.'),
        btn='Konsultasi Haji via WhatsApp',
        about='Portal informasi &amp; panduan haji khusus (haji plus) dari Elharamain Wisata, PIHK resmi.',
        area='Untuk pendaftaran &amp; paket haji plus, hubungi tim kami di Bekasi, Jakarta, Depok, Tangerang, Bogor dan Bandung.',
        col2=('Info &amp; Paket Haji', [('Beranda Haji.biz', HAJI_BIZ + '/'), ('Paket Haji Plus 2028', HAJI_BIZ + '/paket-haji-plus-2028-elharamain-wisata/'),
                                        ('Umroh Desember 2026', HAJI_BIZ + '/umroh-desember-2026/'), ('Paket Haji Plus (Web Utama)', MAIN + '/paket-haji-plus/')]),
        col3=('Situs Elharamain', SITUS_KAMI)),
    'elharamainhaji-com': dict(
        nama='Elharamain Haji', wa='Assalamu\'alaikum Elharamain Wisata, saya ingin daftar haji plus.',
        cta=('Siap daftar haji plus bersama Elharamain?', 'Konsultasi gratis paket, dana &amp; pembayaran haji plus — langsung dengan tim kami.'),
        btn='Daftar Haji Plus via WhatsApp',
        about='Travel haji plus (haji khusus) resmi dengan porsi Kemenag RI, fasilitas VIP, dan bimbingan ibadah sesuai sunnah.',
        area='Melayani jamaah haji plus dari Bekasi, Jakarta, Depok, Tangerang, Bogor, Bandung dan sekitarnya.',
        col2=('Haji Plus', [('Beranda Elharamain Haji', HAJI + '/'), ('Paket Haji Plus', MAIN + '/paket-haji-plus/'),
                            ('Info Haji Khusus (Haji.biz)', HAJI_BIZ + '/'), ('Paket Umroh Musim Dingin', MAIN + '/paket-umroh-musim-dingin/')]),
        col3=('Situs Elharamain', SITUS_KAMI)),
    'elharamain-id': dict(
        nama='Elharamain.id', wa='Assalamu\'alaikum Elharamain Wisata, saya ingin konsultasi umroh.',
        cta=('Siap berangkat umroh bersama Elharamain?', 'Konsultasi gratis paket, jadwal &amp; pembayaran umroh — langsung dengan tim kami.'),
        btn='Konsultasi Umroh via WhatsApp',
        about='Portal informasi &amp; panduan umroh dari Elharamain Wisata: persiapan, manasik, biaya, dan tips ibadah sesuai sunnah.',
        area='Untuk pendaftaran paket umroh, hubungi tim kami di Bekasi, Jakarta, Depok, Tangerang, Bogor dan Bandung.',
        col2=('Paket Umroh', [(t, MAIN + u) for t, u in bf.PAKET if 'haji' not in u]),
        col3=('Travel Umroh Terdekat', KANTOR)),
}


def build(key, c):
    html = bf.footer_html()
    html = re.sub(r'<script type="application/ld\+json">.*?</script>', '', html, flags=re.S)
    html = re.sub(r'/\* hide LandingPress.*?footer#colophon\.site-footer\{display:none!important\}\n', '', html, flags=re.S)
    html = html.replace('aria-label="Footer Elharamain Wisata"', f'aria-label="Footer {c["nama"]}"')
    wa = f'https://api.whatsapp.com/send?phone={bf.WA_MAIN}&amp;text=' + urllib.parse.quote(c['wa'])
    # CTA
    html = re.sub(r'<div class="ehf-cta">.*?</a></div></div>', lambda m: (
        f'<div class="ehf-cta"><div class="ehf-wrap"><div><b>{c["cta"][0]}</b><span>{c["cta"][1]}</span></div>'
        f'<a class="ehf-btn" href="{wa}" target="_blank" rel="noopener">{bf.svg(bf.SOCIAL[2][2])} {c["btn"]}</a></div></div>'), html, count=1, flags=re.S)
    # deskripsi & area
    html = re.sub(r'<p class="ehf-about">.*?</p>', f'<p class="ehf-about">{c["about"]}</p>', html, count=1)
    html = re.sub(r'<p class="ehf-area">.*?</p>', f'<p class="ehf-area">{c["area"]}</p>', html, count=1)
    # kolom 2 & 3
    def col(title, links):
        return (f'<div><div class="ehf-h">{title}</div><ul class="ehf-links">'
                + ''.join(f'<li><a href="{u}">{t}</a></li>' for t, u in links) + '</ul></div>')
    cols = re.search(r'(<div><div class="ehf-h">Paket Umroh</div>.*?</ul></div>)(<div><div class="ehf-h">Travel Umroh Terdekat</div>.*?</ul></div>)', html, flags=re.S)
    html = html.replace(cols.group(0), col(*c['col2']) + col(*c['col3']))
    # hak cipta
    html = html.replace('© 2026 Elharamain Wisata ·', f'© 2026 {c["nama"]} ·', 1)
    head = (f'<!-- Footer {c["nama"]}. Tempel ke widget "HTML" Elementor di UAE > Footer (Display: Entire Website).\n'
            '     Dibuat oleh tools/build_footer_situs.py; jangan edit manual. -->\n')
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    open(os.path.join(root, f'wordpress/uae/{key}-footer.html'), 'w', encoding='utf-8').write(head + html)
    os.makedirs(os.path.join(root, 'build'), exist_ok=True)
    open(os.path.join(root, f'build/preview-footer-{key}.html'), 'w', encoding='utf-8').write(
        '<html><head><meta name=viewport content="width=device-width,initial-scale=1"></head><body style="margin:0"><div style="height:60px"></div>' + html + '</body></html>')
    print(key, len(html))


for k, v in SITES.items():
    build(k, v)
