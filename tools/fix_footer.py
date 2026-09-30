"""Fix the UAE footer template (elementor-hf 8566): Bandung phone, typos, copyright year,
address formatting, heading levels, and links from each office name to its /travel-umroh-<kota>/ page.

Needs the WPCode snippet that exposes elementor-hf + _elementor_data to REST.
Usage: python3 tools/fix_footer.py [--dry-run]"""
import base64, json, os, sys, urllib.request

API = 'https://www.elharamainwisata.com/wp-json/wp/v2/elementor-hf/8566'
SITE = 'https://www.elharamainwisata.com'
AUTH = 'Basic ' + base64.b64encode(f"{os.environ['WP_USER']}:{os.environ['WP_APP_PASSWORD']}".encode()).decode()


def req(method, url, body=None):
    r = urllib.request.Request(url, method=method, data=None if body is None else json.dumps(body).encode(),
                               headers={'Authorization': AUTH, 'Content-Type': 'application/json', 'User-Agent': 'curl/8.5.0'})
    with urllib.request.urlopen(r, timeout=120) as f:
        raw = f.read()
        return json.loads(raw) if raw.strip() else None


def link(url):
    return {'url': url, 'is_external': '', 'nofollow': '', 'custom_attributes': ''}


TITLES = {  # id -> new title
    '2b00d537': 'Kantor Pusat Elharamain Wisata',
    '555432aa': 'Ruko Emerald No.5 Blok EB 1, Jl. Harapan Indah Raya, Kec. Medan Satria, Kota Bekasi, Jawa Barat 17132',
    '5afafae1': 'Ruko Emerald No.5 Blok EB 1, Jl. Harapan Indah Raya, Kec. Medan Satria, Kota Bekasi, Jawa Barat 17132',
    '477068a5': 'Jl. Tebet Raya No.39 B, Tebet Timur, Kec. Tebet, Kota Jakarta Selatan, DKI Jakarta 12820',
    '6a60807f': 'Jl. Margonda No.252 D, Kemiri Muka, Kec. Beji, Kota Depok, Jawa Barat',
    '303fdbe3': 'Ruko Ps. Modern No.18 BSD, Rw. Mekar Jaya, Kec. Serpong, Kota Tangerang Selatan, Banten 15318',
    '11ca2399': 'Jl. Bulevar Utama Blok RC No.18, Ruby Commercial – Summarecon Bandung, Kota Bandung, Jawa Barat',
    '7db90892': 'Ruko Graha Boulevard, Jl. Summarecon Bogor GBVD No.10, Sukatani, Kec. Sukaraja, Kab. Bogor, Jawa Barat 16144',
    'cbf46f5': '© 2026 Elharamain Wisata. All Rights Reserved.',
}
OFFICE_LINKS = {  # office-name heading -> city landing page
    '213dd9f3': 'bekasi', '33dbb5e0': 'jakarta', '64ddda77': 'depok',
    '7ae7d916': 'tangerang', '7590b1ec': 'bandung', '6bd5cb6': 'bogor',
}
OFFICE_TITLES = {'213dd9f3': 'Kantor Pusat Bekasi'}
NOT_HEADINGS = set(TITLES) | {'3f56c7c1'}  # addresses / company name / copyright are not headings
BANDUNG_BTN = 'aa8b8c9'

post = req('GET', API + '?context=edit')
data = json.loads(post['meta']['_elementor_data'])
done = []


def walk(nodes):
    for e in nodes:
        s, i = e['settings'], e['id']
        if i in TITLES:
            s['title'] = TITLES[i]; done.append(i)
        if i in NOT_HEADINGS:
            s['header_size'] = 'p'
        if i in OFFICE_LINKS:
            # link inside the title with inline colour: LiteSpeed UCSS for existing pages lacks
            # Elementor's ".elementor-heading-title a{color:inherit}" so a link setting turns dark blue
            name = OFFICE_TITLES.get(i) or (s['title'] if '<a ' not in s['title'] else s['title'].split('>', 1)[1].split('<', 1)[0])
            s.pop('link', None)
            s['title'] = (f'<a href="{SITE}/travel-umroh-{OFFICE_LINKS[i]}/" '
                          f'style="color:inherit;text-decoration:none">{name}</a>')
            done.append(i)
        if i == BANDUNG_BTN:
            s['text'] = ' 0813-2212-344'
            s['link'] = link('https://api.whatsapp.com/send?phone=628132212344'); done.append(i)
        if e.get('widgetType') == 'icon-list':
            for it in s.get('icon_list', []):
                if it.get('text', '').startswith('ZIN UMRAH'):
                    it['text'] = 'I' + it['text']; done.append(i)
        walk(e.get('elements', []))


walk(data)
print('changed:', len(set(done)), sorted(set(done)))
if '--dry-run' not in sys.argv:
    r = req('POST', API, {'meta': {'_elementor_data': json.dumps(data, ensure_ascii=True)}})
    print('saved', 'ok' if json.loads(r['meta']['_elementor_data']) == data else 'MISMATCH')
    req('DELETE', 'https://www.elharamainwisata.com/wp-json/elementor/v1/cache')
    print('elementor cache cleared')
