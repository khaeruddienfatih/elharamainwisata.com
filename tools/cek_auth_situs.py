"""Diagnosis auth REST (Application Password) per situs, tanpa mengubah apa pun.

  python3 tools/cek_auth_situs.py [elharamain-id|elharamainhaji-com|haji-biz ...]

1. /wp-json (tanpa login): apakah WordPress mengiklankan "application-passwords". Kalau tidak, fitur itu MATI di
   situs tersebut, biasanya karena WordPress tidak mendeteksi HTTPS (is_ssl() false di belakang Cloudflare/proxy)
   atau dimatikan plugin keamanan. Ini dugaan utama untuk auth haji.biz yang rusak.
2. /wp/v2/users/me dengan Basic auth: login berhasil atau tidak, dan kode error WordPress-nya.
"""
import base64, json, os, sys, urllib.request, urllib.error
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_halaman_paket import ENV


def get(url, auth=None):
    h = {'User-Agent': 'Mozilla/5.0 eh-admin'}
    if auth:
        h['Authorization'] = auth
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=60) as r:
            return r.status, r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', 'replace')


def jsn(raw):
    i = raw.find('{')
    try:
        return json.JSONDecoder().raw_decode(raw[i:])[0] if i >= 0 else {}
    except ValueError:
        return {}


for situs in sys.argv[1:] or list(ENV):
    base, pre = ENV[situs]
    print(f'== {situs} ({base})')
    st, raw = get(base + '/wp-json/')
    idx = jsn(raw)
    ap = (idx.get('authentication') or {}).get('application-passwords')
    print(f'  /wp-json: HTTP {st}; application-passwords diiklankan: {"YA" if ap else "TIDAK (fitur mati: cek HTTPS/is_ssl atau plugin keamanan)"}')
    u, p = os.environ.get(pre + '_WP_USER'), os.environ.get(pre + '_WP_APP_PASSWORD')
    if not (u and p):
        print(f'  kredensial {pre}_WP_USER / {pre}_WP_APP_PASSWORD belum di-set'); continue
    st, raw = get(base + '/wp-json/wp/v2/users/me?context=edit',
                  'Basic ' + base64.b64encode(f'{u}:{p}'.encode()).decode())
    me = jsn(raw)
    if st == 200 and me.get('id'):
        print(f'  login OK sebagai "{me.get("slug")}" (id {me["id"]}), peran: {me.get("roles")}')
    else:
        print(f'  login GAGAL: HTTP {st}, kode {me.get("code")}: {me.get("message")}')
