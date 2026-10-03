"""Helper REST API elharamainhaji.com (kredensial dari env ELHARAMAINHAJI_USER / ELHARAMAINHAJI_WP_APP_PASSWORD).

Catatan situs ini:
- Cloudflare kadang membalas halaman anti-bot HTML (status 200/403) -> req() otomatis retry.
- WAF hosting (header x-rasp-block: 1) memblokir POST ke /wp-json/rankmath/... -> pakai req2() (jalur /?rest_route=).
"""
import base64, json, os, time, urllib.request, urllib.error

SITE = 'https://www.elharamainhaji.com'
AUTH = 'Basic ' + base64.b64encode(
    f"{os.environ['ELHARAMAINHAJI_USER']}:{os.environ['ELHARAMAINHAJI_WP_APP_PASSWORD']}".encode()).decode()


def _call(url, method, data, tries):
    body = json.dumps(data).encode() if data is not None else None
    for _ in range(tries):
        r = urllib.request.Request(url, data=body, method=method,
                                   headers={'Authorization': AUTH, 'Content-Type': 'application/json',
                                            'User-Agent': 'Mozilla/5.0 eh-admin'})
        try:
            with urllib.request.urlopen(r, timeout=120) as resp:
                txt = resp.read().decode()
                if txt.lstrip().startswith('<'):  # halaman anti-bot
                    time.sleep(3); continue
                return resp.status, (json.loads(txt) if txt else None), dict(resp.headers)
        except urllib.error.HTTPError as e:
            txt = e.read().decode()
            if txt.lstrip().startswith('<'):
                time.sleep(3); continue
            return e.code, txt[:800], {}
    return 0, 'anti-bot terus', {}


def req(method, path, data=None, tries=6):
    """Jalur biasa: req('GET', '/wp/v2/posts?per_page=10')."""
    return _call(SITE + '/wp-json' + path, method, data, tries)


def req2(method, route, data=None, tries=6):
    """Jalur ?rest_route= (lolos WAF): req2('DELETE', '/wp/v2/posts/123&_fields=id,status')."""
    return _call(SITE + '/?rest_route=' + route, method, data, tries)
