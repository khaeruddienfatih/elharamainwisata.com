"""Helper kecil untuk WordPress REST API elharamainwisata.com."""
import base64, json, os, sys, urllib.request, urllib.error

try:
    import winreg
    def _env(name):
        v = os.environ.get(name)
        if v:
            return v
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment') as k:
            return winreg.QueryValueEx(k, name)[0]
except ImportError:
    def _env(name):
        return os.environ[name]

BASE = 'https://www.elharamainwisata.com/wp-json'
AUTH = 'Basic ' + base64.b64encode(f"{_env('WP_USER')}:{_env('WP_APP_PASSWORD')}".encode()).decode()


def req(method, path, data=None):
    body = json.dumps(data).encode() if data is not None else None
    r = urllib.request.Request(BASE + path, data=body, method=method,
                               headers={'Authorization': AUTH, 'Content-Type': 'application/json',
                                        'User-Agent': 'Mozilla/5.0 eh-admin'})
    try:
        with urllib.request.urlopen(r, timeout=120) as resp:
            txt = resp.read().decode()
            return resp.status, (json.loads(txt) if txt else None)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:500]


def find(els, wid, parent=None):
    for e in els:
        if e.get('id') == wid:
            return e, parent
        r = find(e.get('elements', []), wid, e)
        if r:
            return r
    return None


def get_public(url):
    r = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache'})
    with urllib.request.urlopen(r, timeout=60) as resp:
        return resp.read().decode('utf-8', 'replace')
