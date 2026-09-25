"""Build the UAE header (elementor-hf 8556) as one HTML widget with inline, scoped CSS.

Menu items are read from the WordPress menu "Menu 1" (id 4) at build time, so after changing the
menu in wp-admin re-run:  python3 tools/build_header.py --deploy

Dropdowns (desktop) and the mobile menu work with CSS only, so they keep working when LiteSpeed
delays JavaScript or serves a UCSS file without the UAE menu rules.
"""
import base64, html, json, os, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://www.elharamainwisata.com'
LOGO = SITE + '/wp-content/uploads/2024/02/AAssets-haji-biz-7.webp'  # white logo, 1366x591
AUTH = 'Basic ' + base64.b64encode(f"{os.environ['WP_USER']}:{os.environ['WP_APP_PASSWORD']}".encode()).decode()


def call(method, path, body=None):
    r = urllib.request.Request(SITE + '/wp-json' + path, method=method, data=None if body is None else json.dumps(body).encode(),
                               headers={'Authorization': AUTH, 'Content-Type': 'application/json', 'User-Agent': 'curl/8.5.0'})
    raw = urllib.request.urlopen(r, timeout=120).read()
    return json.loads(raw) if raw.strip() else None


def menu_tree():
    items = call('GET', '/wp/v2/menu-items?per_page=100&menus=4&_fields=id,title,url,parent,menu_order,target')
    items.sort(key=lambda m: m['menu_order'])
    top = [dict(m, children=[]) for m in items if not m['parent']]
    by_id = {m['id']: m for m in top}
    for m in items:
        if m['parent'] in by_id:
            by_id[m['parent']]['children'].append(m)
    return top


CSS = r'''<style>
.ehh{--hb:#004AAD;--hb2:#1684CF;--hg:#DBC033;background:var(--hb);font-family:Poppins,sans-serif;position:relative;z-index:999}
.ehh *{box-sizing:border-box}
.ehh a{text-decoration:none}
.ehh-bar{max-width:1240px;margin:0 auto;padding:10px 24px;display:flex;align-items:center;gap:24px;min-height:74px}
.ehh-logo{display:block;flex:0 0 auto}
.ehh-logo img{display:block;width:150px;height:65px;object-fit:contain}
.ehh-nav{margin-left:auto;display:flex;align-items:center}
.ehh-menu{list-style:none;margin:0;padding:0;display:flex;align-items:center;gap:4px}
.ehh-menu>li{position:relative}
.ehh-menu>li>label{display:block;margin:0}
.ehh-stgl{position:absolute;opacity:0;pointer-events:none}
.ehh-menu>li>a,.ehh-menu>li>label>span{display:flex;align-items:center;gap:6px;color:#fff;font-weight:600;font-size:15px;padding:12px 14px;border-radius:8px;cursor:pointer;white-space:nowrap}
.ehh-menu>li:hover>a,.ehh-menu>li:hover>label>span,.ehh-menu>li:focus-within>label>span,.ehh-menu>li:focus-within>a{color:var(--hg)}
.ehh-caret{width:10px;height:10px;border-right:2px solid currentColor;border-bottom:2px solid currentColor;transform:rotate(45deg) translate(-2px,-2px)}
.ehh-sub{list-style:none;margin:0;padding:8px;position:absolute;top:100%;left:0;min-width:260px;background:#fff;border-radius:12px;box-shadow:0 14px 34px rgba(0,30,80,.22);
 opacity:0;visibility:hidden;transform:translateY(6px);transition:.18s}
.ehh-menu>li:hover>.ehh-sub,.ehh-menu>li:focus-within>.ehh-sub{opacity:1;visibility:visible;transform:none}
.ehh-sub a{display:block;color:#10213d;font-size:14.5px;font-weight:500;padding:9px 12px;border-radius:8px}
.ehh-sub a:hover{background:#eef4ff;color:var(--hb)}
.ehh-sub li.ehh-hl a{font-weight:700;color:var(--hb)}
.ehh-cta{display:inline-flex;align-items:center;gap:8px;background:#25D366;color:#fff!important;font-weight:700;font-size:14px;padding:10px 16px;border-radius:10px;white-space:nowrap;margin-left:8px}
.ehh-cta:hover{background:#1da851}
.ehh-cta svg{width:17px;height:17px;fill:currentColor}
.ehh-tgl{display:none}
.ehh-burger{display:none;margin-left:auto;width:44px;height:44px;border-radius:10px;align-items:center;justify-content:center;cursor:pointer;background:rgba(255,255,255,.12)}
.ehh-burger span,.ehh-burger span::before,.ehh-burger span::after{display:block;width:22px;height:2px;background:#fff;border-radius:2px;position:relative;transition:.2s}
.ehh-burger span::before,.ehh-burger span::after{content:"";position:absolute;left:0}
.ehh-burger span::before{top:-7px}.ehh-burger span::after{top:7px}
@media (max-width:1024px){
 .ehh-bar{min-height:64px;padding:8px 16px;flex-wrap:wrap}
 .ehh-logo img{width:130px;height:56px}
 .ehh-burger{display:flex}
 .ehh-nav{display:none;width:100%;margin:0;padding:6px 0 14px}
 .ehh-tgl:checked~.ehh-nav{display:block}
 .ehh-tgl:checked~.ehh-burger span{background:transparent}
 .ehh-tgl:checked~.ehh-burger span::before{top:0;transform:rotate(45deg)}
 .ehh-tgl:checked~.ehh-burger span::after{top:0;transform:rotate(-45deg)}
 .ehh-menu{flex-direction:column;align-items:stretch;gap:0}
 .ehh-menu>li{border-top:1px solid rgba(255,255,255,.15)}
 .ehh-menu>li>a,.ehh-menu>li>label>span{padding:13px 4px;justify-content:space-between}
 .ehh-stgl:checked~label .ehh-caret{transform:rotate(-135deg) translate(-2px,-2px)}
 .ehh-sub{position:static;display:none;opacity:1;visibility:visible;transform:none;box-shadow:none;min-width:0;margin:0 0 10px}
 .ehh-stgl:checked~.ehh-sub{display:block}
 .ehh-cta{margin:12px 0 0;justify-content:center;width:100%}
}
</style>'''

WA_ICON = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1s-.5-.1-.7.1-.8 1-.9 1.2-.3.2-.6.1a8.2 8.2 0 0 1-4-3.5c-.3-.5.3-.5.9-1.6.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6a1.1 1.1 0 0 0-.8.4 3.4 3.4 0 0 0-1 2.5 5.9 5.9 0 0 0 1.2 3.1 13.5 13.5 0 0 0 5.2 4.6c1.9.8 2.7.9 3.6.7a3.1 3.1 0 0 0 2-1.4 2.5 2.5 0 0 0 .2-1.4c-.1-.1-.3-.2-.6-.3zM12 21.8a9.8 9.8 0 0 1-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4A9.8 9.8 0 1 1 12 21.8zM20.5 3.5A11.9 11.9 0 0 0 1.8 17.9L.1 24l6.3-1.6a11.9 11.9 0 0 0 5.7 1.4 11.9 11.9 0 0 0 8.4-20.3z"/></svg>')


def header_html(tree):
    wa = 'https://api.whatsapp.com/send?phone=6281287292422&amp;text=' + urllib.parse.quote(
        "Assalamu'alaikum Elharamain Wisata, saya ingin konsultasi umroh.")
    li = []
    for m in tree:
        title = html.escape(html.unescape(m['title']['rendered']))
        if m['title']['rendered'].strip().lower() == 'kontak':
            continue  # replaced by the WhatsApp button
        url = m['url']
        tgt = ' target="_blank" rel="noopener"' if m.get('target') == '_blank' else ''
        if m['children']:
            real = url and not url.startswith('#')
            sub = ''
            for c in m['children']:
                hl = ' class="ehh-hl"' if 'musim-dingin' in c['url'] else ''
                sub += f'<li{hl}><a href="{c["url"]}">{html.escape(html.unescape(c["title"]["rendered"]))}</a></li>'
            if real:  # parent is a page too: link it first in the dropdown
                sub = f'<li class="ehh-hl"><a href="{url}">{title}</a></li>' + sub
            n = len(li)
            li.append(f'<li class="ehh-has"><input type="checkbox" id="ehh-s{n}" class="ehh-stgl">'
                      f'<label for="ehh-s{n}" tabindex="0"><span>{title}<i class="ehh-caret"></i></span></label>'
                      f'<ul class="ehh-sub">{sub}</ul></li>')
        else:
            li.append(f'<li><a href="{url}"{tgt}>{title}</a></li>')
    return (CSS + '<header class="ehh" aria-label="Menu utama Elharamain Wisata"><div class="ehh-bar">'
            f'<a class="ehh-logo" href="{SITE}/" aria-label="Elharamain Wisata - Beranda">'
            f'<img src="{LOGO}" alt="Elharamain Wisata" width="1366" height="591" data-no-lazy="1" fetchpriority="high"></a>'
            '<input type="checkbox" id="ehh-tgl" class="ehh-tgl" aria-label="Buka menu">'
            '<label for="ehh-tgl" class="ehh-burger" aria-hidden="true"><span></span></label>'
            '<nav class="ehh-nav"><ul class="ehh-menu">' + ''.join(li) + '</ul>'
            f'<a class="ehh-cta" href="{wa}" target="_blank" rel="noopener">{WA_ICON} Konsultasi Gratis</a></nav>'
            '</div></header>')


import urllib.parse  # noqa: E402


def elementor_data(tree):
    return [{'id': 'a0ead001', 'elType': 'section', 'isInner': False,
             'settings': {'layout': 'full_width', 'gap': 'no',
                          'padding': {'unit': 'px', 'top': '0', 'right': '0', 'bottom': '0', 'left': '0', 'isLinked': True}},
             'elements': [{'id': 'a0ead002', 'elType': 'column', 'isInner': False,
                           'settings': {'_column_size': 100, '_inline_size': None,
                                        'padding': {'unit': 'px', 'top': '0', 'right': '0', 'bottom': '0', 'left': '0', 'isLinked': True}},
                           'elements': [{'id': 'a0ead003', 'elType': 'widget', 'widgetType': 'html', 'isInner': False,
                                         'settings': {'html': header_html(tree)}, 'elements': []}]}]}]


if __name__ == '__main__':
    tree = menu_tree()
    data = elementor_data(tree)
    os.makedirs(os.path.join(ROOT, 'build'), exist_ok=True)
    json.dump(data, open(os.path.join(ROOT, 'build', 'header.json'), 'w'), ensure_ascii=False)
    body = ('<div style="height:900px;background:#f3f7fd;padding:40px;font-family:sans-serif">Konten halaman…</div>')
    open(os.path.join(ROOT, 'build', 'preview-header.html'), 'w').write(
        '<html><head><meta name=viewport content="width=device-width,initial-scale=1">'
        '<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel=stylesheet>'
        '</head><body style="margin:0">' + header_html(tree) + body + '</body></html>')
    print('menu:', [html.unescape(m['title']['rendered']) + (f" ({len(m['children'])})" if m['children'] else '') for m in tree])
    if '--deploy' in sys.argv:
        cur = call('GET', '/wp/v2/elementor-hf/8556?context=edit')
        json.dump(cur, open(os.path.join(ROOT, 'backup', 'pages', '8556-header-before-redesign.json'), 'w'), ensure_ascii=False, indent=1)
        r = call('POST', '/wp/v2/elementor-hf/8556', {'meta': {'_elementor_data': json.dumps(data, ensure_ascii=True)}})
        print('saved', 'ok' if json.loads(r['meta']['_elementor_data']) == data else 'MISMATCH')
        call('DELETE', '/elementor/v1/cache')
        print('elementor cache cleared')
