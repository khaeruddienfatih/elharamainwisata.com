"""Build the redesigned UAE footer (elementor-hf 8566) as one Elementor section with an HTML widget.

All styling is inline in the widget (scoped to .ehf) so LiteSpeed UCSS/CCSS caches of existing
pages cannot drop it.  Usage:
  python3 tools/build_footer.py            -> build/footer.json + build/preview-footer.html
  python3 tools/build_footer.py --deploy   -> also saves to WordPress (needs the WPCode REST snippet)
"""
import base64, json, os, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://www.elharamainwisata.com'
LOGO = SITE + '/wp-content/uploads/2026/02/Assets-LP-Haji-ONH-Plus-3-1.webp'
WA_MAIN = '6281287292422'

OFFICES = [  # city, label, address, phone (display), phone link (kept from the previous footer)
    ('Bekasi', 'Kantor Pusat Bekasi', 'Ruko Emerald No.5 Blok EB 1, Jl. Harapan Indah Raya, Kec. Medan Satria, Kota Bekasi, Jawa Barat 17132',
     '0812-8729-2422', 'https://umroh.elharamainwisata.com/fifi/'),
    ('Jakarta', 'Kantor Jakarta', 'Jl. Tebet Raya No.39 B, Tebet Timur, Kec. Tebet, Kota Jakarta Selatan, DKI Jakarta 12820',
     '0812-1417-8056', 'https://umroh.elharamainwisata.com/jakarta/'),
    ('Depok', 'Kantor Depok', 'Jl. Margonda No.252 D, Kemiri Muka, Kec. Beji, Kota Depok, Jawa Barat',
     '0851-7998-8198', 'https://umroh.elharamainwisata.com/depok/'),
    ('Tangerang', 'Kantor Tangerang', 'Ruko Ps. Modern No.18 BSD, Rw. Mekar Jaya, Kec. Serpong, Kota Tangerang Selatan, Banten 15318',
     '0856-9388-3208', 'https://umroh.elharamainwisata.com/tangerang/'),
    ('Bandung', 'Kantor Bandung', 'Jl. Bulevar Utama Blok RC No.18, Ruby Commercial – Summarecon Bandung, Kota Bandung, Jawa Barat',
     '0813-2212-344', 'https://api.whatsapp.com/send?phone=628132212344'),
    ('Bogor', 'Kantor Bogor', 'Ruko Graha Boulevard, Jl. Summarecon Bogor GBVD No.10, Sukatani, Kec. Sukaraja, Kab. Bogor, Jawa Barat 16144',
     '0822-6012-6394', 'https://umroh.elharamainwisata.com/bogor/'),
]
PAKET = [
    ('Paket Umroh Musim Dingin 2026/2027', '/paket-umroh-musim-dingin/'),
    ('Umroh Bronze', '/umroh-bronze/'),
    ('Umroh Silver', '/paket-umroh-silver/'),
    ('Umroh Platinum', '/umroh-platinum/'),
    ('Umroh Premium', '/umroh-premium/'),
    ('Umroh 12 Hari', '/umroh-silver-12-hari/'),
    ('Haji Plus', '/paket-haji-plus/'),
]
SOCIAL = [
    ('YouTube', 'https://www.youtube.com/channel/UC0R5NZ1hz3qXaqrAuHIJBLg',
     '<path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.6 12 3.6 12 3.6s-7.5 0-9.4.5A3 3 0 0 0 .5 6.2 31 31 0 0 0 0 12a31 31 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.5 9.4.5 9.4.5s7.5 0 9.4-.5a3 3 0 0 0 2.1-2.1A31 31 0 0 0 24 12a31 31 0 0 0-.5-5.8zM9.6 15.6V8.4l6.2 3.6-6.2 3.6z"/>'),
    ('Instagram', 'https://www.instagram.com/elharamainwisata/',
     '<path d="M12 2.2c3.2 0 3.6 0 4.8.1 3.3.1 4.8 1.7 4.9 4.9.1 1.3.1 1.6.1 4.8s0 3.6-.1 4.8c-.1 3.2-1.7 4.8-4.9 4.9-1.3.1-1.6.1-4.8.1s-3.6 0-4.8-.1c-3.3-.1-4.8-1.7-4.9-4.9C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.8C2.4 3.9 3.9 2.4 7.2 2.3 8.4 2.2 8.8 2.2 12 2.2zM12 0C8.7 0 8.3 0 7.1.1 2.7.3.3 2.7.1 7.1 0 8.3 0 8.7 0 12s0 3.7.1 4.9c.2 4.4 2.6 6.8 7 7 1.2.1 1.6.1 4.9.1s3.7 0 4.9-.1c4.4-.2 6.8-2.6 7-7 .1-1.2.1-1.6.1-4.9s0-3.7-.1-4.9c-.2-4.4-2.6-6.8-7-7C15.7 0 15.3 0 12 0zm0 5.8a6.2 6.2 0 1 0 0 12.4 6.2 6.2 0 0 0 0-12.4zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.4-11.8a1.4 1.4 0 1 0 0 2.9 1.4 1.4 0 0 0 0-2.9z"/>'),
    ('WhatsApp', f'https://api.whatsapp.com/send?phone={WA_MAIN}',
     '<path d="M17.5 14.4c-.3-.1-1.8-.9-2-1s-.5-.1-.7.1-.8 1-.9 1.2-.3.2-.6.1a8.2 8.2 0 0 1-4-3.5c-.3-.5.3-.5.9-1.6.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6a1.1 1.1 0 0 0-.8.4 3.4 3.4 0 0 0-1 2.5 5.9 5.9 0 0 0 1.2 3.1 13.5 13.5 0 0 0 5.2 4.6c1.9.8 2.7.9 3.6.7a3.1 3.1 0 0 0 2-1.4 2.5 2.5 0 0 0 .2-1.4c-.1-.1-.3-.2-.6-.3zM12 21.8a9.8 9.8 0 0 1-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4A9.8 9.8 0 1 1 12 21.8zM20.5 3.5A11.9 11.9 0 0 0 1.8 17.9L.1 24l6.3-1.6a11.9 11.9 0 0 0 5.7 1.4 11.9 11.9 0 0 0 8.4-20.3z"/>'),
]
ICON_PIN = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/></svg>'
ICON_PHONE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.2 11.4 11.4 0 0 0 3.6.6 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1 11.4 11.4 0 0 0 .6 3.6 1 1 0 0 1-.3 1z"/></svg>'
ICON_CHECK = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm-1.4 14.2-4-4 1.4-1.4 2.6 2.6 5.6-5.6 1.4 1.4-7 7z"/></svg>'

CSS = r'''<style>
/* Elharamain brand: #004AAD (biru tua), #1684CF (biru), #DBC033 (emas), putih */
.ehf{--ehf-bg:#004AAD;--ehf-bg2:#003C8C;--ehf-blue:#1684CF;--ehf-gold:#DBC033;--ehf-txt:#FFFFFF;--ehf-mut:#DCE8FA;--ehf-line:rgba(255,255,255,.18);
 background:var(--ehf-bg);color:var(--ehf-txt);font-family:Poppins,sans-serif;font-size:14px;line-height:1.65;text-align:left}
.ehf *{box-sizing:border-box}
.ehf a{color:inherit;text-decoration:none}
.ehf svg{width:16px;height:16px;fill:currentColor;flex:0 0 16px}
.ehf-wrap{max-width:1200px;margin:0 auto;padding:0 24px}
.ehf-cta{background:#1684CF;color:#fff}
.ehf-cta .ehf-wrap{display:flex;align-items:center;justify-content:space-between;gap:20px;padding-top:28px;padding-bottom:28px;flex-wrap:wrap}
.ehf-cta b{display:block;font-family:Raleway,sans-serif;font-weight:800;font-size:24px;line-height:1.25;color:#fff}
.ehf-cta span{opacity:.9}
.ehf-btn{display:inline-flex;align-items:center;gap:8px;background:#25D366;color:#fff!important;font-weight:700;padding:13px 22px;border-radius:10px;white-space:nowrap;transition:.2s}
.ehf-btn:hover{background:#1da851}
.ehf-btn.ehf-gold{background:var(--ehf-gold);color:#004AAD!important}.ehf-btn.ehf-gold:hover{background:#fff}
.ehf-main{display:grid;grid-template-columns:1.35fr 1fr 1fr 1.15fr;gap:36px;padding-top:48px;padding-bottom:36px}
.ehf-brand{display:flex;align-items:center;gap:12px;margin-bottom:14px}
.ehf-brand img{width:52px;height:auto;aspect-ratio:317/384;background:#fff;border-radius:12px;padding:4px}
.ehf-brand b{display:block;font-family:Raleway,sans-serif;font-weight:800;font-size:19px;color:#fff;line-height:1.2}
.ehf-brand small{color:var(--ehf-mut);font-size:12px;letter-spacing:.02em}
.ehf-about{margin:0 0 14px;color:var(--ehf-mut)}
.ehf-legal{list-style:none;margin:0 0 18px;padding:0;display:grid;gap:6px}
.ehf-legal li{display:flex;gap:8px;align-items:flex-start;font-size:13px}
.ehf-legal svg{color:var(--ehf-gold);margin-top:3px}
.ehf-social{display:flex;gap:10px}
.ehf-social a{width:38px;height:38px;border-radius:50%;background:rgba(255,255,255,.14);display:inline-flex;align-items:center;justify-content:center;transition:.2s}
.ehf-social a:hover{background:var(--ehf-gold);color:#004AAD}
.ehf-social svg{width:18px;height:18px;flex-basis:18px}
.ehf-h{font-family:Raleway,sans-serif;font-weight:800;font-size:16px;color:#fff;margin:0 0 14px;letter-spacing:.02em}
.ehf-h::after{content:"";display:block;width:32px;height:3px;background:var(--ehf-gold);border-radius:2px;margin-top:8px}
.ehf-links{list-style:none;margin:0;padding:0;display:grid;gap:7px}
.ehf-links a{color:var(--ehf-txt);transition:.15s}
.ehf-links a:hover{color:var(--ehf-gold);padding-left:3px}
.ehf-hq p{display:flex;gap:8px;margin:0 0 10px;align-items:flex-start}
.ehf-hq svg{margin-top:3px;color:var(--ehf-gold)}
.ehf-hq a.ehf-tel{font-weight:700;color:#fff}
.ehf-offices{border-top:1px solid var(--ehf-line);padding-top:30px;padding-bottom:34px}
.ehf-offices .ehf-h{margin-bottom:18px}
.ehf-og{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.ehf-o{background:rgba(255,255,255,.08);border:1px solid var(--ehf-line);border-radius:12px;padding:16px;display:flex;flex-direction:column;gap:8px}
.ehf-o a.ehf-on{font-weight:700;color:#fff;font-size:15px}
.ehf-o a.ehf-on:hover{color:var(--ehf-gold)}
.ehf-o address{font-style:normal;font-size:12.5px;line-height:1.55;color:var(--ehf-mut);flex:1}
.ehf-o a.ehf-op{display:inline-flex;align-items:center;gap:6px;align-self:flex-start;font-size:13px;font-weight:700;color:#004AAD!important;background:#fff;padding:6px 12px;border-radius:8px}
.ehf-o a.ehf-op:hover{background:var(--ehf-gold)}
.ehf-bottom{background:var(--ehf-bg2);font-size:12.5px;color:var(--ehf-mut)}
.ehf-bottom .ehf-wrap{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;padding-top:16px;padding-bottom:16px}
.ehf-bottom a:hover{color:var(--ehf-gold)}
@media (max-width:1024px){.ehf-main{grid-template-columns:1fr 1fr}.ehf-og{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:640px){.ehf-wrap{padding:0 16px}.ehf-cta b{font-size:20px}.ehf-cta .ehf-btn{width:100%;justify-content:center}
 .ehf-main{grid-template-columns:1fr 1fr;gap:28px 18px;padding-top:36px}.ehf-main>div:first-child,.ehf-main>div:last-child{grid-column:1/-1}
 .ehf-og{grid-template-columns:1fr}.ehf-bottom .ehf-wrap{justify-content:center;text-align:center}}
</style>'''


def svg(path):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true">{path}</svg>'


def footer_html():
    hq = OFFICES[0]
    wa_txt = "Assalamu'alaikum Elharamain Wisata, saya ingin konsultasi umroh."
    wa = f'https://api.whatsapp.com/send?phone={WA_MAIN}&amp;text=' + urllib.parse.quote(wa_txt)
    legal = ['Izin Umrah SK Kemenag No. 63 Tahun 2020', 'Izin Haji Plus SK Kemenag No. 846 Tahun 2020',
             'Anggota HIMPUH &amp; IATA', 'Terakreditasi A oleh KAN']
    h = CSS + '<footer class="ehf" aria-label="Footer Elharamain Wisata">'
    h += (f'<div class="ehf-cta"><div class="ehf-wrap"><div><b>Siap berangkat umroh bersama Elharamain?</b>'
          f'<span>Konsultasi gratis paket, jadwal &amp; pembayaran — langsung dengan tim kami.</span></div>'
          f'<a class="ehf-btn" href="{wa}" target="_blank" rel="noopener">{svg(SOCIAL[2][2])} Konsultasi Gratis via WhatsApp</a></div></div>')
    h += '<div class="ehf-wrap ehf-main">'
    h += (f'<div><div class="ehf-brand"><img src="{LOGO}" alt="Logo Elharamain Wisata" width="317" height="384" loading="lazy" data-no-lazy="1">'
          f'<div><b>Elharamain Wisata</b><small>PT Dhiyaa El Haramain El Mubarakah</small></div></div>'
          f'<p class="ehf-about">Travel umroh &amp; haji plus resmi dengan hotel bintang 5, direct flight, dan bimbingan ibadah sesuai sunnah.</p>'
          '<ul class="ehf-legal">' + ''.join(f'<li>{ICON_CHECK}<span>{x}</span></li>' for x in legal) + '</ul>'
          '<div class="ehf-social">' + ''.join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="{n}">{svg(p)}</a>' for n, u, p in SOCIAL) + '</div></div>')
    h += ('<div><div class="ehf-h">Paket Umroh</div><ul class="ehf-links">'
          + ''.join(f'<li><a href="{SITE}{u}">{t}</a></li>' for t, u in PAKET) + '</ul></div>')
    h += ('<div><div class="ehf-h">Travel Umroh Terdekat</div><ul class="ehf-links">'
          + ''.join(f'<li><a href="{SITE}/travel-umroh-{c.lower()}/">Travel Umroh {c}</a></li>' for c, *_ in OFFICES)
          + f'<li><a href="{SITE}/kantor-cabang/">Semua Kantor Cabang</a></li></ul></div>')
    h += (f'<div class="ehf-hq"><div class="ehf-h">Kantor Pusat</div>'
          f'<p>{ICON_PIN}<span>{hq[2]}</span></p>'
          f'<p>{ICON_PHONE}<a class="ehf-tel" href="{hq[4]}">{hq[3]}</a></p>'
          f'<p><a class="ehf-btn ehf-gold" style="padding:10px 16px;font-size:13.5px" href="https://www.google.com/maps/search/?api=1&amp;query='
          + urllib.parse.quote('Elharamain Wisata Harapan Indah Bekasi') + f'" target="_blank" rel="noopener">{ICON_PIN} Petunjuk Arah</a></p></div>')
    h += '</div>'
    h += ('<div class="ehf-wrap ehf-offices"><div class="ehf-h">Kantor Elharamain Wisata</div><div class="ehf-og">'
          + ''.join(f'<div class="ehf-o"><a class="ehf-on" href="{SITE}/travel-umroh-{c.lower()}/">{label}</a>'
                    f'<address>{addr}</address><a class="ehf-op" href="{link}" target="_blank" rel="noopener">{ICON_PHONE}{phone}</a></div>'
                    for c, label, addr, phone, link in OFFICES) + '</div></div>')
    h += (f'<div class="ehf-bottom"><div class="ehf-wrap"><span>© 2026 Elharamain Wisata · PT Dhiyaa El Haramain El Mubarakah. All rights reserved.</span>'
          f'<span><a href="{SITE}/kantor-cabang/">Kantor Cabang</a> · <a href="{SITE}/privacy-policy/">Kebijakan Privasi</a></span></div></div>')
    return h + '</footer>'


import urllib.parse  # noqa: E402  (used inside footer_html)


def elementor_data():
    return [{'id': 'f0071e01', 'elType': 'section', 'isInner': False,
             'settings': {'layout': 'full_width', 'gap': 'no', 'stretch_section': 'section-stretched',
                          'padding': {'unit': 'px', 'top': '0', 'right': '0', 'bottom': '0', 'left': '0', 'isLinked': True},
                          'margin': {'unit': 'px', 'top': '0', 'right': 0, 'bottom': '0', 'left': 0, 'isLinked': True}},
             'elements': [{'id': 'f0071e02', 'elType': 'column', 'isInner': False,
                           'settings': {'_column_size': 100, '_inline_size': None,
                                        'padding': {'unit': 'px', 'top': '0', 'right': '0', 'bottom': '0', 'left': '0', 'isLinked': True}},
                           'elements': [{'id': 'f0071e03', 'elType': 'widget', 'widgetType': 'html', 'isInner': False,
                                         'settings': {'html': footer_html()}, 'elements': []}]}]}]


if __name__ == '__main__':
    os.makedirs(os.path.join(ROOT, 'build'), exist_ok=True)
    data = elementor_data()
    json.dump(data, open(os.path.join(ROOT, 'build', 'footer.json'), 'w'), ensure_ascii=False)
    open(os.path.join(ROOT, 'build', 'preview-footer.html'), 'w').write(
        '<html><head><meta name=viewport content="width=device-width,initial-scale=1">'
        '<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&family=Raleway:wght@800&display=swap" rel=stylesheet>'
        '</head><body style="margin:0;background:#fff"><div style="height:120px"></div>' + footer_html() + '</body></html>')
    print('built', len(footer_html()), 'chars')
    if '--deploy' in sys.argv:
        auth = 'Basic ' + base64.b64encode(f"{os.environ['WP_USER']}:{os.environ['WP_APP_PASSWORD']}".encode()).decode()

        def call(m, u, b=None):
            r = urllib.request.Request(SITE + '/wp-json' + u, method=m, data=None if b is None else json.dumps(b).encode(),
                                       headers={'Authorization': auth, 'Content-Type': 'application/json', 'User-Agent': 'curl/8.5.0'})
            raw = urllib.request.urlopen(r, timeout=120).read()
            return json.loads(raw) if raw.strip() else None

        cur = call('GET', '/wp/v2/elementor-hf/8566?context=edit')
        json.dump(cur, open(os.path.join(ROOT, 'backup', 'pages', '8566-footer-before-redesign.json'), 'w'), ensure_ascii=False, indent=1)
        r = call('POST', '/wp/v2/elementor-hf/8566', {'meta': {'_elementor_data': json.dumps(data, ensure_ascii=True)}})
        print('saved', 'ok' if json.loads(r['meta']['_elementor_data']) == data else 'MISMATCH')
        call('DELETE', '/elementor/v1/cache')
        print('elementor cache cleared')
