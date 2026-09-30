"""Pasang/perbarui header & footer UAE lewat endpoint snippet wordpress/wpcode-uae-rest.php.

Usage:
  python3 tools/deploy_uae.py <situs> list
  python3 tools/deploy_uae.py <situs> header|footer <file.html> [--id N] [--draft]
Situs: hajibiz | elharamainhaji | elharamainid  (kredensial dari env, lihat README)."""
import base64, json, os, re, sys, time, urllib.error, urllib.request

SITES = {
    'hajibiz': ('https://www.haji.biz', 'HAJIBIZ_WP_USER', 'HAJIBIZ_WP_APP_PASSWORD'),
    'elharamainhaji': ('https://www.elharamainhaji.com', 'ELHARAMAINHAJI_USER', 'ELHARAMAINHAJI_WP_APP_PASSWORD'),
    'elharamainid': ('https://www.elharamain.id', 'ELHARAMAINID_WP_USER', 'ELHARAMAINID_WP_APP_PASSWORD'),
}

DEFAULT_USER = {'elharamainid': 'elharamain'}  # username bukan rahasia; env boleh menimpa


def call(site, method, body=None):
    base, u, p = SITES[site]
    user = os.environ.get(u) or DEFAULT_USER.get(site)
    auth = 'Basic ' + base64.b64encode(f"{user}:{os.environ[p]}".encode()).decode()
    data = json.dumps(body).encode() if body is not None else None
    for attempt in range(4):
        req = urllib.request.Request(base + '/wp-json/eh/v1/hf', data=data, method=method,
                                     headers={'Authorization': auth, 'Content-Type': 'application/json',
                                              'User-Agent': 'curl/8.5.0'})  # UA Python diblokir Cloudflare (1010)
        try:
            raw = urllib.request.urlopen(req, timeout=60).read().decode()
        except urllib.error.HTTPError as e:
            msg = e.read().decode()
            if e.code == 403 and msg.lstrip().startswith('<'):  # blokir WAF sesekali (openresty); coba lagi
                time.sleep(6)
                continue
            sys.exit(f'{e.code}: {msg[:300]}')
        if raw.lstrip().startswith(('[', '{')):
            return json.loads(raw)
        time.sleep(6)  # halaman anti-bot "reload" hosting kadang muncul; coba lagi
    sys.exit('Tetap diblokir halaman anti-bot hosting')


if __name__ == '__main__':
    site, action = sys.argv[1], sys.argv[2]
    if action == 'list':
        for t in call(site, 'GET'):
            print(t['id'], t['status'], t['title'], t['meta'].get('ehf_template_type'))
        sys.exit()
    html = open(sys.argv[3]).read()
    html = re.sub(r'^\s*<!--.*?-->\s*', '', html, flags=re.S)  # buang komentar catatan di atas file
    body = {'type': action, 'html': html, 'title': f'{action.title()} {site}',
            'status': 'draft' if '--draft' in sys.argv else 'publish'}
    if '--id' in sys.argv:
        body['id'] = int(sys.argv[sys.argv.index('--id') + 1])
    print(call(site, 'POST', body))
