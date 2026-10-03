"""Widget "Fasilitas Elharamain Wisata": semua hotel paket + bus, menggantikan Image Carousel lama di 9581.

Foto: gabungan 3 foto per hotel dari brosur PDF (eksterior, kamar, lobi/restoran), Cloudinary folder
Elharamainwisata/Fasilitas (public_id fasilitas-hotel-<slug>, fasilitas-bus). Tab CSS (radio), tanpa JavaScript.

Jalankan: python3 tools/fasilitas_hotel.py              -> tulis landing-pages/widget/fasilitas-hotel-bus.html
          DEPLOY=1 python3 tools/fasilitas_hotel.py     -> juga ganti widget carousel 73bd261 di halaman 9581
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(__file__))

ROOT = os.path.join(os.path.dirname(__file__), '..')
OUT = os.path.join(ROOT, 'landing-pages', 'widget', 'fasilitas-hotel-bus.html')
IMG = 'https://res.cloudinary.com/v6gwkqrb/image/upload/c_fill,w_{w},h_{h},q_auto,f_auto/{id}.jpg'
PAGE, OLD_WIDGET = 9581, '73bd261'

# (slug, nama, bintang, jarak, paket)
MAKKAH = [
    ('anjum', 'Anjum Hotel', 5, '±350 m ke Masjidil Haram', 'Bronze · Silver · Silver 12 Hari'),
    ('prestige', 'Prestige Hotel', 5, '±250 m ke Masjidil Haram', 'Bronze November · Bronze Plus'),
    ('marwa-rotana', 'Marwa Rotana', 5, 'Zamzam Tower, pelataran Masjidil Haram', 'Platinum · Gold · Ramadhan Platinum'),
    ('movenpick-hajar', 'Movenpick Hajar Tower', 5, 'Zamzam Tower, pelataran Masjidil Haram', 'Platinum · Gold'),
    ('fairmont', 'Fairmont Clock Royal Tower', 5, 'Zamzam Tower, pelataran Masjidil Haram', 'Premium · Ramadhan Premium'),
    ('al-shohada', 'Al Shohada Hotel', 5, '±450 m ke Masjidil Haram', 'Ramadhan Bronze'),
    ('royal-majestic', 'Royal Majestic Hotel', 4, '±400 m ke Masjidil Haram', "I'tikaf Silver 17 Hari"),
]
MADINAH = [
    ('al-aqeeq', 'Al-Aqeeq Hotel', 5, '±50 m ke Masjid Nabawi', 'Sebagian besar paket'),
    ('peninsula-worth', 'Peninsula Worth', 5, '±150 m ke Masjid Nabawi', 'Bronze · Bronze Plus · Silver (Desember)'),
    ('movenpick-madinah', 'Movenpick Madinah', 5, '±50 m ke Masjid Nabawi', 'Platinum · Premium (Januari)'),
    ('royal-andalus', 'Royal Andalus', 4, '±30 m ke Masjid Nabawi', 'Ramadhan Bronze'),
]

PIN = '<svg viewBox="0 0 24 24"><path d="M12 22s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/></svg>'
TAG = '<svg viewBox="0 0 24 24"><path d="M20 12 12 20l-8-8V4h8z"/><circle cx="8" cy="8" r="1.5"/></svg>'

CSS = '''<style>
.ehf{--b:#004AAD;--b2:#1684CF;--ink:#10213d;--mut:#5b6b84;--line:#e3e9f3;font-family:Poppins,sans-serif;color:var(--ink);max-width:1160px;margin:0 auto;padding:0 16px}
.ehf *{box-sizing:border-box}
.ehf-r{position:absolute;opacity:0;pointer-events:none}
.ehf-tabs{display:flex;justify-content:center;gap:10px;flex-wrap:wrap;margin:6px 0 28px}
.ehf-tabs label{cursor:pointer;border:1.5px solid var(--line);background:#fff;color:var(--mut);border-radius:999px;padding:10px 20px;font-weight:600;font-size:14.5px;line-height:1.2;transition:.2s;user-select:none}
.ehf-tabs label small{font-weight:500;opacity:.75}
.ehf-tabs label:hover{border-color:var(--b2);color:var(--b)}
#ehf-makkah:checked~.ehf-tabs label[for=ehf-makkah],#ehf-madinah:checked~.ehf-tabs label[for=ehf-madinah],#ehf-bus:checked~.ehf-tabs label[for=ehf-bus]{background:var(--b);border-color:var(--b);color:#fff}
.ehf-g{display:none;flex-wrap:wrap;justify-content:center;gap:22px}
#ehf-makkah:checked~.g-makkah,#ehf-madinah:checked~.g-madinah,#ehf-bus:checked~.g-bus{display:flex}
.ehf-c{width:calc((100% - 22px)/2);margin:0;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 8px 26px rgba(0,40,100,.13);display:flex;flex-direction:column}
.ehf-c img{display:block;width:100%;height:auto;aspect-ratio:25/13;object-fit:cover;background:#dbe7f7}
.ehf-c figcaption{padding:16px 18px 18px;display:flex;flex-direction:column;gap:6px}
.ehf-st{color:#e0a800;font-size:14px;letter-spacing:2px;line-height:1}
.ehf-st span{color:var(--mut);font-size:12px;letter-spacing:0;font-weight:600;margin-left:6px}
.ehf-c h4{margin:2px 0 4px;font-family:Raleway,sans-serif;font-weight:800;font-size:19px;line-height:1.3;color:var(--ink)}
.ehf-c p{margin:0;display:flex;gap:8px;align-items:flex-start;font-size:13.5px;line-height:1.5;color:var(--mut)}
.ehf-c p svg{flex:none;width:16px;height:16px;margin-top:2px;stroke:var(--b2);fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.ehf-c p b{color:var(--ink);font-weight:600}
.ehf-note{text-align:center;font-size:12.5px;color:var(--mut);margin:22px 0 0}
@media (max-width:767px){.ehf-c{width:100%}.ehf-tabs label{padding:9px 14px;font-size:13.5px}.ehf-c h4{font-size:17px}}
</style>'''


def stars(n):
    return f'<div class="ehf-st">{"★" * n}<span>Hotel Bintang {n}</span></div>'


def img(pid, alt):
    src = IMG.format(w=800, h=416, id=pid)
    srcset = ', '.join(f'{IMG.format(w=w, h=round(w * 0.52), id=pid)} {w}w' for w in (480, 800, 1000))
    return (f'<img src="{src}" srcset="{srcset}" sizes="(max-width:767px) 100vw, 560px" '
            f'width="1000" height="520" loading="lazy" decoding="async" alt="{alt}">')


def hotel(slug, nama, bintang, jarak, paket, kota):
    return (f'<figure class="ehf-c">{img("fasilitas-hotel-" + slug, nama + " " + kota + " - hotel paket umroh Elharamain Wisata")}'
            f'<figcaption>{stars(bintang)}<h4>{nama} {kota}</h4>'
            f'<p>{PIN}<span>{jarak}</span></p><p>{TAG}<span>Paket: <b>{paket}</b></span></p></figcaption></figure>')


BUS = (f'<figure class="ehf-c">{img("fasilitas-bus", "Bus terbaru jamaah umroh Elharamain Wisata")}'
       '<figcaption><div class="ehf-st"><span style="margin:0">Transportasi</span></div><h4>Bus Terbaru Ber-AC</h4>'
       f'<p>{PIN}<span>Penjemputan bandara, perjalanan antar kota Makkah – Madinah – Jeddah, dan seluruh program ziarah &amp; city tour.</span></p>'
       f'<p>{TAG}<span>Madinah → Makkah naik <b>Kereta Cepat Haramain</b> (sesuai paket).</span></p></figcaption></figure>')


def build():
    return (CSS + '<div class="ehf">'
            '<input type="radio" class="ehf-r" name="ehf-tab" id="ehf-makkah" checked>'
            '<input type="radio" class="ehf-r" name="ehf-tab" id="ehf-madinah">'
            '<input type="radio" class="ehf-r" name="ehf-tab" id="ehf-bus">'
            '<div class="ehf-tabs" role="tablist">'
            f'<label for="ehf-makkah" role="tab">Hotel Makkah <small>({len(MAKKAH)})</small></label>'
            f'<label for="ehf-madinah" role="tab">Hotel Madinah <small>({len(MADINAH)})</small></label>'
            '<label for="ehf-bus" role="tab">Bus</label></div>'
            '<div class="ehf-g g-makkah">' + ''.join(hotel(*h, 'Makkah') for h in MAKKAH) + '</div>'
            '<div class="ehf-g g-madinah">' + ''.join(hotel(*h, 'Madinah') for h in MADINAH) + '</div>'
            '<div class="ehf-g g-bus">' + BUS + '</div>'
            '<p class="ehf-note">Hotel sesuai paket yang dipilih atau setaraf. Jarak perkiraan dari brosur resmi Elharamain Wisata.</p>'
            '</div>')


def deploy(html):
    from wp_rest import req
    for i in range(6):
        try:
            st, raw = req('GET', f'/wp/v2/pages/{PAGE}?context=edit')
            if st == 200 and isinstance(raw, dict):
                break
        except json.JSONDecodeError:
            pass
        time.sleep(20)
    data = raw['meta']['_elementor_data']
    bdir = os.path.join(ROOT, 'backup', '2026-10-03')
    os.makedirs(bdir, exist_ok=True)
    with open(os.path.join(bdir, f'{PAGE}_sebelum_fasilitas.json'), 'w') as f:
        f.write(data)
    els = json.loads(data)

    def swap(es):
        for i, e in enumerate(es):
            if e.get('id') == OLD_WIDGET:
                assert e.get('widgetType') == 'image-carousel', e.get('widgetType')
                es[i] = {'id': 'f4c1b05', 'elType': 'widget', 'widgetType': 'html', 'elements': [],
                         'settings': {'html': html, '_margin': {'unit': 'px', 'top': '10', 'right': '0', 'bottom': '25', 'left': '0', 'isLinked': False}}}
                return True
            if swap(e.get('elements', [])):
                return True
        return False

    assert swap(els), 'widget carousel tidak ditemukan'
    st, r = req('POST', f'/wp/v2/pages/{PAGE}', {'meta': {'_elementor_data': json.dumps(els, ensure_ascii=False)}})
    print('POST', PAGE, st)
    assert st == 200, r
    print('hapus cache elementor:', req('DELETE', '/elementor/v1/cache')[0])


if __name__ == '__main__':
    html = build()
    assert '<!--' not in html
    with open(OUT, 'w') as f:
        f.write(html + '\n')
    print('tulis', OUT, len(html), 'byte')
    if os.environ.get('DEPLOY') == '1':
        deploy(html)
