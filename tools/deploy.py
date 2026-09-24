"""Push build/<id>.json (Elementor data) + build/seo.json (Rank Math) to WordPress.

Usage: WP_USER=... WP_APP_PASSWORD=... python3 tools/deploy.py [page_id ...] [--publish]
Clears the Elementor CSS cache afterwards."""
import base64, json, os, sys, urllib.request

SITE = 'https://www.elharamainwisata.com/wp-json'
AUTH = 'Basic ' + base64.b64encode(f"{os.environ['WP_USER']}:{os.environ['WP_APP_PASSWORD']}".encode()).decode()
BUILD = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'build')


def call(method, path, body=None):
    req = urllib.request.Request(SITE + path, method=method, data=None if body is None else json.dumps(body).encode(),
                                 headers={'Authorization': AUTH, 'Content-Type': 'application/json', 'User-Agent': 'curl/8.5.0'})
    with urllib.request.urlopen(req, timeout=120) as r:
        raw = r.read()
        return json.loads(raw) if raw.strip() else None


args = [a for a in sys.argv[1:] if not a.startswith('--')]
publish = '--publish' in sys.argv
seo = json.load(open(os.path.join(BUILD, 'seo.json')))
for pid in args:
    data = json.load(open(os.path.join(BUILD, f'{pid}.json')))
    body = {'meta': {'_elementor_edit_mode': 'builder', '_elementor_data': json.dumps(data, ensure_ascii=True)}}
    if publish:
        body['status'] = 'publish'
    r = call('POST', f'/wp/v2/pages/{pid}', body)
    ok = json.loads(r['meta']['_elementor_data']) == data
    s = seo.get(str(pid))
    if s:
        call('POST', '/rankmath/v1/updateMeta', {'objectType': 'post', 'objectID': int(pid), 'meta': s})
    print(pid, r['status'], r['link'], 'data ok' if ok else 'DATA MISMATCH', '+seo' if s else '')
call('DELETE', '/elementor/v1/cache')
print('elementor cache cleared')
