"""Pasang/perbarui header & footer UAE lewat endpoint snippet wordpress/wpcode-uae-rest.php.

Usage:
  python3 tools/deploy_uae.py <situs> list
  python3 tools/deploy_uae.py <situs> header|footer <file.html> [--id N] [--draft]
Situs: hajibiz | elharamainhaji | elharamainid  (kredensial dari env, lihat README)."""
import json, os, re, subprocess, sys, tempfile, time

SITES = {
    'hajibiz': ('https://www.haji.biz', 'HAJIBIZ_WP_USER', 'HAJIBIZ_WP_APP_PASSWORD'),
    'elharamainhaji': ('https://www.elharamainhaji.com', 'ELHARAMAINHAJI_USER', 'ELHARAMAINHAJI_WP_APP_PASSWORD'),
    'elharamainid': ('https://www.elharamain.id', 'ELHARAMAINID_WP_USER', 'ELHARAMAINID_WP_APP_PASSWORD'),
}

DEFAULT_USER = {'elharamainid': 'elharamain'}  # username bukan rahasia; env boleh menimpa


def call(site, method, body=None):
    return rest(site, method, '/eh/v1/hf', body)


def rest(site, method, path, body=None):
    """Panggil /wp-json<path> dengan login admin situs; ulangi bila kena anti-bot/WAF.
    Pakai curl: Cloudflare/WAF hosting memblokir klien HTTP Python (UA & sidik TLS)."""
    base, u, p = SITES[site]
    user = os.environ.get(u) or DEFAULT_USER.get(site)
    cfg = f'user = "{user}:{os.environ[p]}"\n'  # lewat stdin, tidak muncul di daftar proses
    cmd = ['curl', '-sS', '--max-time', '90', '-K', '-', '-X', method, '-A', 'curl/8.5.0',
           '-H', 'Content-Type: application/json', '-w', '\n%{http_code}', base + '/wp-json' + path]
    if body is not None:
        cmd[1:1] = ['--data-binary', '@' + _tmp_json(body)]
    for attempt in range(5):
        out = subprocess.run(cmd, input=cfg, capture_output=True, text=True).stdout
        raw, _, code = out.rpartition('\n')
        if raw.lstrip().startswith(('[', '{')):
            if int(code) >= 400:
                sys.exit(f'{code}: {raw[:300]}')
            return json.loads(raw)
        time.sleep(8)  # halaman anti-bot "reload" / 403 WAF sesekali; coba lagi
    sys.exit(f'Tetap diblokir anti-bot hosting ({code})')


def _tmp_json(body):
    f = tempfile.NamedTemporaryFile('w', suffix='.json', delete=False)
    json.dump(body, f)
    f.close()
    return f.name


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
