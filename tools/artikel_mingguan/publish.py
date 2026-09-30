"""Jadwalkan 70 artikel (5/hari x 7 hari) di elharamain.id & haji.biz + SEO Rank Math.

Usage:
  python3 tools/artikel_mingguan/publish.py            # dry-run: preview HTML ke build/artikel/
  python3 tools/artikel_mingguan/publish.py --publish  # buat/perbarui post status 'future' + meta Rank Math
Jadwal WIB: elharamain.id 06.00, 09.00, 12.00, 15.00, 19.00 · haji.biz 07.00, 10.00, 13.00, 16.00, 20.00
Mulai 1 Oktober 2026. Manifest: data/jadwal-artikel-2026-10.json"""
import datetime as dt
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import haji_biz  # noqa: E402
import umroh_id  # noqa: E402
from render import CSS, cta, faq_block, fig, img_url, legal, related, toc  # noqa: E402
from extra import X, blok_haji, blok_umroh  # noqa: E402
from extra2 import X2  # noqa: E402

START = dt.date(2026, 10, 1)
MANIFEST = os.path.join(ROOT, 'data', 'jadwal-artikel-2026-10.json')
JAM = {'elharamainid': [6, 9, 12, 15, 19], 'hajibiz': [7, 10, 13, 16, 20]}
WIB = dt.timezone(dt.timedelta(hours=7))
EXISTING = {  # artikel yang sudah terbit, boleh ditautkan
    'elharamainid': {'umroh-januari-2027': 'Umroh Januari 2027: Jadwal, Harga & Pilihan Paket Musim Dingin'},
    'hajibiz': {'perbandingan-paket-haji-plus-silver-gold-platinum': 'Perbandingan 4 Paket Haji Plus: Silver, Gold, Gold Arbain, Platinum',
                'apa-itu-haji-khusus-haji-plus-dana-manfaat': 'Apa Itu Haji Khusus (Haji Plus)? Panduan Lengkap Dana Manfaat & Transparansinya',
                'cicilan-haji-plus-simulasi-angsuran-pembiayaan': 'Cicilan Haji Plus: Simulasi Angsuran & Syarat Pembiayaan Bank Muamalat'},
}


def schedule():
    out = []
    for site, arts in (('elharamainid', umroh_id.A), ('hajibiz', haji_biz.A)):
        for i, a in enumerate(arts):
            day, slot = divmod(i, 5)
            when = dt.datetime.combine(START + dt.timedelta(days=day), dt.time(JAM[site][slot]), WIB)
            out.append(dict(a, when=when))
    return out


def build(a, allarts):
    earlier = {x['slug']: x['title'] for x in allarts if x['site'] == a['site'] and x['when'] < a['when']}
    known = dict(EXISTING[a['site']], **earlier)
    links = [(f'/{s}/', known[s]) for s in a.get('rel', []) if s in known]
    if len(links) < 2:  # lengkapi dengan artikel terbaru di situs yang sama yang sudah terbit lebih dulu
        prev = sorted((x for x in allarts if x['site'] == a['site'] and x['when'] < a['when']), key=lambda x: x['when'])
        for x in reversed(prev):
            if len(links) >= 2:
                break
            if (f"/{x['slug']}/", x['title']) not in links:
                links.append((f"/{x['slug']}/", x['title']))
    same = [x for x in allarts if x['site'] == a['site']]
    idx = same.index(next(x for x in same if x['slug'] == a['slug']))
    is_umroh = a['site'] == 'elharamainid' or a['cat'] == haji_biz.CAT_MIX
    judul, isi = X[a['slug']]
    body = a['body'] + f'<h2>{judul}</h2>' + isi + X2.get(a['slug'], '') + (blok_umroh(a['slug'], idx) if is_umroh else blok_haji(a['slug'], idx))
    heads = re.findall(r'<h2>(.*?)</h2>', body) + ['Pertanyaan yang Sering Diajukan']
    cover = a['cover']
    cover_html = fig(cover, a.get('cover_alt') or a['title'], 1200, 675 if not cover.startswith('http') else None)
    html = (CSS + '<div class="ea">' + f'<p>{a["intro"]}</p>' + cover_html + toc(heads) + body
            + legal(umroh=is_umroh) + cta(*a['cta']) + faq_block(a['faqs']) + related(links) + '</div>')
    return html, links


def og_image(a):
    c = a['cover']
    return c if c.startswith('http') else img_url(c, 1200, 630)


def main():
    arts = schedule()
    os.makedirs(os.path.join(ROOT, 'build', 'artikel'), exist_ok=True)
    manifest = []
    if '--publish' in sys.argv:
        from deploy_uae import rest
    only = next((x.split('=', 1)[1] for x in sys.argv if x.startswith('--site=')), None)
    old = {(r['site'], r['slug']): r for r in json.load(open(MANIFEST))} if os.path.exists(MANIFEST) else {}
    for a in arts:
        html, links = build(a, arts)
        open(os.path.join(ROOT, 'build', 'artikel', f"{a['site']}-{a['slug']}.html"), 'w').write(
            '<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width">'
            f'<h1 style="font-family:Poppins;max-width:820px;margin:30px auto 10px">{a["title"]}</h1>' + html)
        rec = {'site': a['site'], 'slug': a['slug'], 'title': a['title'], 'kw': a['kw'],
               'terbit_wib': a['when'].strftime('%Y-%m-%d %H:%M'), 'links': len(links)}
        prev = old.get((a['site'], a['slug']), {})
        if '--publish' in sys.argv and (only and a['site'] != only or prev.get('status') == 'future'):
            rec.update({k: prev[k] for k in ('id', 'status', 'link') if k in prev})
        elif '--publish' in sys.argv:
            time.sleep(15)  # WAF hosting memblokir IP bila request terlalu rapat
            data = {'title': a['title'], 'slug': a['slug'], 'status': 'future', 'excerpt': a['desc'],
                    'content': f'<!-- wp:html -->\n{html}\n<!-- /wp:html -->', 'categories': [a['cat']],
                    'date_gmt': a['when'].astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')}
            if a.get('feat'):
                data['featured_media'] = a['feat']
            found = rest(a['site'], 'GET', f"/wp/v2/posts?slug={a['slug']}&status=future,draft,publish,pending&_fields=id")
            path = f"/wp/v2/posts/{found[0]['id']}" if found else '/wp/v2/posts'
            r = rest(a['site'], 'POST', path + '?_fields=id,status,date,link', data)
            rest(a['site'], 'POST', '/rankmath/v1/updateMeta', {'objectID': r['id'], 'objectType': 'post', 'meta': {
                'rank_math_focus_keyword': a['kw'], 'rank_math_title': a['seo_title'],
                'rank_math_description': a['desc'], 'rank_math_facebook_title': a['seo_title'],
                'rank_math_facebook_description': a['desc'], 'rank_math_facebook_image': og_image(a),
                'rank_math_twitter_use_facebook': 'on'}})
            rec.update(id=r['id'], status=r['status'], link=r['link'])
            print(a['site'], r['id'], r['status'], rec['terbit_wib'], a['slug'], flush=True)
        manifest.append(rec)
        json.dump(manifest + [r for r in old.values() if (r['site'], r['slug']) not in {(m['site'], m['slug']) for m in manifest}],
                  open(MANIFEST, 'w'), ensure_ascii=False, indent=1)  # simpan tiap artikel (bisa dilanjutkan)
    print('artikel:', len(manifest))


if __name__ == '__main__':
    main()
