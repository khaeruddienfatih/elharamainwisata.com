"""Perbarui bagian paket di beranda elharamain.id (ID 309) & elharamainhaji.com (ID 347) sesuai brosur PDF.

- elharamain.id: section 13f678b4 (kartu gambar paket 2025) diganti 1 widget HTML berisi
  landing-pages/section-harga-paket-umroh.html (data/paket-umroh.json = brosur umroh Nov 2026–Jan 2027).
- elharamainhaji.com: section 79cd5f17 (4 Paket Haji) — desain tetap, teks dikoreksi sesuai brosur Haji 1448 H
  (sumber: draft artikel "Panduan Lengkap Haji Plus 1448H", dibuat dari brosur PDF). Link brosur PDF rusak → WA.
Cadangan data lama: backup/pages/<situs>-<id>-elementor-data-2026-09-30.json.
Usage: python3 tools/update_home_paket.py [--publish]"""
import json
import os
import re
import sys
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from deploy_uae import rest  # noqa: E402

WA = 'https://api.whatsapp.com/send?phone=6281287292422&text='

HAJI = {  # id icon-list -> baris (brosur Haji Plus 1448 H, estimasi berangkat 2027)
    '44c60854': ['DP Porsi: 4.000 USD', 'Ber-4: 12.000 USD', 'Ber-3: 13.500 USD', 'Ber-2: 15.000 USD',
                 'Durasi: 22–23 Hari', 'Maktab VIP: 116 (jarak tenda 900 m)',
                 'Hotel Makkah: Anjum Hotel (±350 m)', 'Hotel Madinah: Concorde Dar Alkhair (±200 m)',
                 'Maskapai: Saudia / Qatar / Emirates', 'Bimbingan: Asatidz Berilmu & Berpengalaman',
                 'Program Arbain: –'],
    '43da53cd': ['DP Porsi: 4.000 USD', 'Ber-4: 15.500 USD', 'Ber-3: 17.000 USD', 'Ber-2: 18.500 USD',
                 'Durasi: 22–23 Hari', 'Maktab VIP: 113 (jarak tenda 500 m)',
                 'Hotel Makkah: Marwa Rotana (depan Masjidil Haram)', 'Hotel Madinah: Al-Aqeeq Hotel (±50 m)',
                 'Maskapai: Saudia / Qatar / Emirates', 'Bimbingan: Asatidz Berilmu & Berpengalaman',
                 'Program Arbain: –'],
    '4828f93e': ['DP Porsi: 4.000 USD', 'Ber-4: 17.000 USD', 'Ber-3: 18.500 USD', 'Ber-2: 20.000 USD',
                 'Durasi: 27–28 Hari', 'Maktab VIP: 113 (jarak tenda 500 m)',
                 'Hotel Makkah: Marwa Rotana (depan Masjidil Haram)', 'Hotel Madinah: Al-Aqeeq Hotel (±50 m)',
                 'Maskapai: Saudia / Qatar / Emirates', 'Bimbingan: Asatidz Berilmu & Berpengalaman',
                 'Program Arbain: Termasuk (40 waktu shalat di Masjid Nabawi)'],
    'f35cbc2': ['DP Porsi: 4.000 USD', 'Ber-4: 20.000 USD', 'Ber-3: 22.000 USD', 'Ber-2: 24.000 USD',
                'Durasi: 22–23 Hari', 'Maktab VIP: 111 (jarak tenda 200 m, paling dekat)',
                'Hotel Makkah: Fairmont Hotel (depan masjid)', 'Hotel Madinah: Movenpick Hotel (±50 m)',
                'Maskapai: Saudia / Garuda Indonesia', 'Bimbingan: Asatidz Berilmu & Berpengalaman',
                'Layanan: Premium Prioritas'],
    'dbdb55d': ['Biaya paket di atas adalah estimasi keberangkatan 2027 (1448 H); biaya final diinformasikan 1 tahun '
                'sebelum keberangkatan (estimasi kenaikan 4–5% per tahun).',
                'Pelunasan dapat dikurangi Dana Manfaat (±120 USD/tahun) dari setoran 4.000 USD yang dikelola BPKH.'],
}


def find(els, wid):
    for e in els:
        if e.get('id') == wid:
            return e
        r = find(e.get('elements', []), wid)
        if r:
            return r


def load(site, pid):
    raw = rest(site, 'GET', f'/wp/v2/pages/{pid}?context=edit&_fields=meta')['meta']['_elementor_data']
    data = json.loads(raw) if isinstance(raw, str) else raw
    return json.loads(data) if isinstance(data, str) else data


# ikon diambil dari baris asli (backup) dengan awalan yang sama, supaya tiap baris tetap berikon sesuai artinya
ICON_SRC = {'DP': 'DP Porsi', 'Ber-': 'Opsi Kamar', 'Durasi': 'Durasi', 'Maktab': 'Maktab', 'Hotel Makkah': 'Hotel Makkah',
            'Hotel Madinah': 'Hotel Madinah', 'Maskapai': 'Maskapai', 'Bimbingan': 'Bimbingan',
            'Program Arbain': 'Program Arbain', 'Layanan': 'Layanan'}


def original_icons(wid):
    orig = json.loads(open(os.path.join(ROOT, 'backup', 'pages', 'elharamainhaji-347-elementor-data-2026-09-30.json')).read())
    orig = json.loads(orig) if isinstance(orig, str) else orig
    icons = {}
    for it in find(orig, wid)['settings']['icon_list']:
        plain = re.sub('<[^>]+>', '', it['text'])
        for src in ICON_SRC.values():
            if plain.startswith(src):
                icons[src] = it.get('selected_icon')
    return icons


def patch_haji(data):
    sec = [find(data, '79cd5f17')]
    for wid, lines in HAJI.items():
        items = find(sec, wid)['settings']['icon_list']
        icons = original_icons(wid) if wid != 'dbdb55d' else {}
        new = []
        for i, text in enumerate(lines):
            it = dict(items[0])
            it['text'] = text
            it['_id'] = f'eh{wid[:4]}{i}'
            src = next((v for k, v in ICON_SRC.items() if text.startswith(k)), None)
            if src and icons.get(src):
                it['selected_icon'] = icons[src]
            new.append(it)
        find(sec, wid)['settings']['icon_list'] = new
    # kartu Platinum: urutan disamakan dengan kartu lain (daftar dulu, tombol di bawah)
    col = find(sec, '121247a9')
    order = ['3be9fa86', '53b4136a', '143f75ea', 'f35cbc2', 'df02e0d', '10aa0570']
    col['elements'] = sorted(col['elements'], key=lambda e: order.index(e['id']) if e['id'] in order else 99)
    find(sec, '6a7c8e1a')['settings']['title'] = '4 Paket Haji Plus 1448 H (Estimasi Berangkat 2027)'
    btn = find(sec, '4623ffff')['settings']
    btn['text'] = 'Minta Brosur Haji 1448 H via WhatsApp'
    btn['link'] = {'url': WA + urllib.parse.quote("Assalamu'alaikum Elharamain Wisata, saya minta brosur Haji Plus 1448 H."),
                   'is_external': 'on', 'nofollow': '', 'custom_attributes': ''}
    return data


def patch_umroh(data):
    html = open(os.path.join(ROOT, 'landing-pages', 'section-harga-paket-umroh.html')).read()
    html = html.split('-->', 1)[1].lstrip()  # buang komentar catatan build (LiteSpeed membaca tag di komentar)
    i = [e['id'] for e in data].index('13f678b4')
    zero = {'unit': 'px', 'top': '0', 'right': '0', 'bottom': '0', 'left': '0', 'isLinked': True}
    data[i] = {'id': 'eh13f6a0', 'elType': 'section', 'isInner': False,
               'settings': {'layout': 'full_width', 'gap': 'no', 'padding': zero, 'background_background': 'classic',
                            'background_color': '#FFFFFF', '_element_id': 'paket'},
               'elements': [{'id': 'eh13f6a1', 'elType': 'column', 'isInner': False,
                             'settings': {'_column_size': 100, 'padding': zero},
                             'elements': [{'id': 'eh13f6a2', 'elType': 'widget', 'widgetType': 'html', 'isInner': False,
                                           'settings': {'html': html}, 'elements': []}]}]}
    return data


def save(site, pid, data):
    rest(site, 'POST', f'/wp/v2/pages/{pid}', {'meta': {'_elementor_data': json.dumps(data, ensure_ascii=True)}})
    back = load(site, pid)
    print(site, pid, 'tersimpan', 'OK' if back == json.loads(json.dumps(data, ensure_ascii=True)) else 'BEDA — cek!')
    rest(site, 'DELETE', '/elementor/v1/cache')


if __name__ == '__main__':
    haji = patch_haji(load('elharamainhaji', 347))
    umroh = patch_umroh(load('elharamainid', 309))
    os.makedirs(os.path.join(ROOT, 'build'), exist_ok=True)
    json.dump(haji, open(os.path.join(ROOT, 'build', 'home-elharamainhaji-347.json'), 'w'), ensure_ascii=False, indent=1)
    json.dump(umroh, open(os.path.join(ROOT, 'build', 'home-elharamainid-309.json'), 'w'), ensure_ascii=False, indent=1)
    if '--publish' in sys.argv:
        save('elharamainhaji', 347, haji)
        save('elharamainid', 309, umroh)
    else:
        print('dry-run: lihat build/home-*.json')
