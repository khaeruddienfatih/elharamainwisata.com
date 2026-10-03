"""Perbaikan tampilan 3 Okt 2026 (permintaan pemilik), elharamainwisata.com:

1. Judul "Apa Kata Jamaah Tentang Elharamain Wisata?" kebesaran (50px, pecah 2-3 baris) -> 36 / 30 / 22 px
   (desktop / tablet / HP) di semua halaman yang memakainya.
2. Halaman Haji Plus 8289: jarak kosong ±200px di bawah carousel foto (9ebb303). Penyebab: foto yang belum
   di-lazyload masih placeholder GIF 1x1 yang dirender persegi (435x435), jadi tinggi slider ikut 443px padahal
   foto 16:9 cuma ±240px. Perbaikan: widget HTML kecil (posisi absolute, tidak makan tempat) berisi CSS yang
   mengunci rasio foto carousel itu ke 16:9.

Jalankan: DRY=1 python3 tools/fix_judul_dan_carousel.py   /   python3 tools/fix_judul_dan_carousel.py
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(__file__))
from wp_rest import req

DRY = os.environ.get('DRY') == '1'
BACKUP = os.path.join(os.path.dirname(__file__), '..', 'backup', '2026-10-03')
JUDUL = 'Apa Kata Jamaah'
UKURAN = {'typography_font_size': 36, 'typography_font_size_tablet': 30, 'typography_font_size_mobile': 22}
CAROUSEL_PAGE, CAROUSEL_ID, CSS_WIDGET = 8289, '9ebb303', 'c55a9e1'
CSS = ('<style>.elementor-element-9ebb303 .swiper-slide-image{width:100%;height:auto;aspect-ratio:16/9;object-fit:cover}'
       '.elementor-element-c55a9e1{position:absolute!important;width:0;height:0;overflow:hidden}</style>')


def get(path):
    for i in range(6):
        try:
            st, r = req('GET', path)
            if st == 200 and not isinstance(r, str):
                return r
        except json.JSONDecodeError:
            pass
        time.sleep(20)
    raise SystemExit('gagal GET ' + path)


def fix_judul(els):
    n = 0
    for e in els:
        st = e.get('settings', {})
        if e.get('widgetType') == 'heading' and JUDUL in st.get('title', ''):
            for k, v in UKURAN.items():
                st[k] = {'unit': 'px', 'size': v, 'sizes': []}
            st['typography_line_height'] = {'unit': 'em', 'size': 1.2, 'sizes': []}
            n += 1
        n += fix_judul(e.get('elements', []))
    return n


def fix_carousel(els):
    for e in els:
        kids = e.get('elements', [])
        for i, c in enumerate(kids):
            if c.get('id') == CAROUSEL_ID:
                assert not any(k.get('id') == CSS_WIDGET for k in kids), 'CSS sudah dipasang'
                kids.insert(i + 1, {'id': CSS_WIDGET, 'elType': 'widget', 'widgetType': 'html', 'elements': [],
                                    'settings': {'html': CSS, '_position': 'absolute',
                                                 '_margin': {'unit': 'px', 'top': '0', 'right': '0', 'bottom': '0', 'left': '0', 'isLinked': True}}})
                return True
        if fix_carousel(kids):
            return True
    return False


def main():
    os.makedirs(BACKUP, exist_ok=True)
    pages = get('/wp/v2/pages?per_page=100&status=publish,draft&context=edit&_fields=id,meta')
    todo = [p for p in pages if JUDUL in ((p.get('meta') or {}).get('_elementor_data') or '') or p['id'] == CAROUSEL_PAGE]
    for p in todo:
        pid, data = p['id'], p['meta']['_elementor_data']
        els = json.loads(data)
        n = fix_judul(els)
        c = fix_carousel(els) if pid == CAROUSEL_PAGE else False
        if not n and not c:
            continue
        if DRY:
            print('DRY', pid, 'judul', n, 'carousel', c)
            continue
        with open(f'{BACKUP}/{pid}_sebelum_judul_carousel.json', 'w') as f:
            f.write(data)
        st, r = req('POST', f'/wp/v2/pages/{pid}', {'meta': {'_elementor_data': json.dumps(els, ensure_ascii=False)}})
        print('POST', pid, st, 'judul', n, 'carousel', c)
        assert st == 200, r
    if not DRY:
        print('hapus cache elementor:', req('DELETE', '/elementor/v1/cache')[0])


if __name__ == '__main__':
    main()
