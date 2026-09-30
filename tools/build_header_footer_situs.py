"""Header & footer UAE untuk haji.biz, elharamainhaji.com, elharamain.id.

Header = desain header elharamainwisata.com (tools/build_header.py: dropdown & menu HP tanpa JavaScript),
dengan menu statis per situs. Footer = tools/build_footer_situs.py.

  python3 tools/build_header_footer_situs.py            -> wordpress/uae/<situs>-header.html & -footer.html (+ preview di build/)
  python3 tools/build_header_footer_situs.py --deploy   -> juga menimpa isi post Header/Footer UAE yang SUDAH ADA
                                                           (elharamain.id 805/807, elharamainhaji.com 3512/3514); cadangan lama
                                                           disimpan di backup/situs/<situs>/. haji.biz: REST rusak -> tempel manual.
"""
import json, os, re, sys, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('WP_USER', '-')          # build_header membaca kredensial situs utama saat import;
os.environ.setdefault('WP_APP_PASSWORD', '-')  # di sini tidak dipakai (menu statis, tanpa akses situs utama)
import build_header as bh
import build_footer_situs as fs
import build_halaman_paket as hp

ROOT = hp.ROOT
MAIN, HAJI, ID, HAJI_BIZ = fs.MAIN, fs.HAJI, fs.ID, fs.HAJI_BIZ


def m(title, url, children=(), blank=False):
    """Item menu dalam bentuk yang sama dengan menu-items REST (dipakai build_header.header_html)."""
    return {'title': {'rendered': title}, 'url': url, 'target': '_blank' if blank else '',
            'children': [{'title': {'rendered': t}, 'url': u} for t, u in children]}


KANTOR = [('Semua Kantor Cabang', MAIN + '/kantor-cabang/')] + [(f'Travel Umroh {c}', f'{MAIN}/travel-umroh-{c.lower()}/') for c, *_ in fs.bf.OFFICES]
SITUS = [('Elharamain Wisata (Web Utama)', MAIN + '/'), ('Elharamain Haji', HAJI + '/'), ('Haji.biz (Info Haji)', HAJI_BIZ + '/'),
         ('Elharamain.id (Info Umroh)', ID + '/')]

SITES = {
    'elharamain-id': dict(nama='Elharamain.id', root=ID, id_header=805, id_footer=807,
        wa="Assalamu'alaikum Elharamain Wisata, saya ingin konsultasi umroh.",
        menu=[m('Beranda', ID + '/'),
              m('Paket Umroh', '#', fs.PAKET_ID[:-1]),
              m('Haji Plus', ID + '/haji-plus-elharamain-wisata/'),
              m('Kantor Cabang', '#', KANTOR),
              m('Situs Kami', '#', SITUS)]),
    'elharamainhaji-com': dict(nama='Elharamain Haji', root=HAJI, id_header=3512, id_footer=3514,
        wa="Assalamu'alaikum Elharamain Wisata, saya ingin daftar haji plus.",
        menu=[m('Beranda', HAJI + '/'),
              m('Paket Haji Plus', HAJI + '/paket-haji-plus/'),
              m('Info Haji', HAJI_BIZ + '/'),
              m('Umroh', '#', [('Paket Umroh Musim Dingin 2026/2027', MAIN + '/paket-umroh-musim-dingin/'), ('Info Umroh', ID + '/')]),
              m('Kantor Cabang', '#', KANTOR),
              m('Situs Kami', '#', SITUS)]),
    'haji-biz': dict(nama='Haji.biz', root=HAJI_BIZ, id_header=None, id_footer=None,
        wa="Assalamu'alaikum Elharamain Wisata, saya ingin konsultasi haji plus.",
        menu=[m('Beranda', HAJI_BIZ + '/'),
              m('Paket Haji Plus 2028', HAJI_BIZ + '/paket-haji-plus-2028-elharamain-wisata/'),
              m('Umroh Desember 2026', HAJI_BIZ + '/umroh-desember-2026/'),
              m('Daftar Haji Plus', HAJI + '/paket-haji-plus/'),
              m('Kantor Cabang', '#', KANTOR),
              m('Situs Kami', '#', SITUS)]),
}


def header(key, c):
    h = bh.header_html(c['menu'])
    h = re.sub(r'<style id="eh-typo">.*?</style>', '', h, flags=re.S)  # tipografi seluruh situs: tidak ikut dipasang
    h = h.replace(f'href="{bh.SITE}/" aria-label="Elharamain Wisata - Beranda"', f'href="{c["root"]}/" aria-label="{c["nama"]} - Beranda"')
    h = h.replace('aria-label="Menu utama Elharamain Wisata"', f'aria-label="Menu utama {c["nama"]}"')
    h = h.replace(urllib.parse.quote("Assalamu'alaikum Elharamain Wisata, saya ingin konsultasi umroh."), urllib.parse.quote(c['wa']))
    return h


def simpan(key, bagian, h):
    with open(os.path.join(ROOT, 'wordpress/uae', f'{key}-{bagian}.html'), 'w', encoding='utf-8') as f:
        f.write(h)


def pasang(key, bagian, post_id, h):
    call = hp.rest(key)
    lama = call('GET', f'/wp/v2/elementor-hf/{post_id}?context=edit')
    if lama.get('title', {}).get('raw', '').strip().lower() != bagian:
        sys.exit(f'{key}: post {post_id} berjudul "{lama.get("title", {}).get("raw")}", bukan "{bagian}" - dibatalkan')
    bk = os.path.join(ROOT, 'backup', 'situs', key)
    os.makedirs(bk, exist_ok=True)
    fbk = os.path.join(bk, f'{post_id}-{bagian}-sebelum.json')
    if not os.path.exists(fbk):
        with open(fbk, 'w', encoding='utf-8') as f:
            json.dump(lama, f, ensure_ascii=False, indent=1)
    data = hp.elementor_html(('hd' if bagian == 'header' else 'ft') + key[:4].replace('-', 'x'), h)
    r = call('POST', f'/wp/v2/elementor-hf/{post_id}', {'meta': {'_elementor_edit_mode': 'builder',
                                                                  '_elementor_data': json.dumps(data, ensure_ascii=True)}})
    call('DELETE', '/elementor/v1/cache')
    print(f'  {key} {bagian} -> post {r["id"]} ({r["status"]}) terpasang; cadangan di backup/situs/{key}/')


if __name__ == '__main__':
    os.makedirs(os.path.join(ROOT, 'build'), exist_ok=True)
    for key, c in SITES.items():
        hd = header(key, c)
        ft = fs.build(key, fs.SITES[key])
        simpan(key, 'header', hd)
        with open(os.path.join(ROOT, 'build', f'preview-hf-{key}.html'), 'w', encoding='utf-8') as f:
            f.write('<html><head><meta name=viewport content="width=device-width,initial-scale=1"></head><body style="margin:0">'
                    + hd + '<div style="height:400px;background:#f3f7fd"></div>' + ft + '</body></html>')
        if '--deploy' in sys.argv and c['id_header']:
            pasang(key, 'header', c['id_header'], hd)
            pasang(key, 'footer', c['id_footer'], ft)
        elif '--deploy' in sys.argv:
            print(f'  {key}: REST rusak, tempel manual wordpress/uae/{key}-header.html & -footer.html di UAE')
