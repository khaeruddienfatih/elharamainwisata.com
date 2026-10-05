#!/usr/bin/env python3
"""Kirim sitemap ke Google Search Console lewat API resmi (sitemaps.submit) dan tampilkan statusnya.

Kredensial (jangan masuk repo): env GSC_SA_JSON = isi JSON service account.
Service account harus ditambahkan di GSC > Setelan > Pengguna dan izin (minimal "Penuh"/Owner).
Pemakaian: python3 tools/gsc_submit_sitemap.py [SITE] [SITEMAP...]
  default: sc-domain:haji.biz  https://haji.biz/sitemap_index.xml
Catatan: API Search Console TIDAK menyediakan "Request Indexing" untuk artikel biasa; sitemap
adalah jalur otomatis yang resmi. Indexing API Google hanya untuk JobPosting/BroadcastEvent.
"""
import json, os, sys, time, base64, urllib.parse, urllib.request
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

SITE = sys.argv[1] if len(sys.argv) > 1 else 'sc-domain:haji.biz'
MAPS = sys.argv[2:] or ['https://haji.biz/sitemap_index.xml']
raw = os.environ.get('GSC_SA_JSON')
if not raw:
    print('GSC_SA_JSON tidak diset; lewati.'); sys.exit(0)
sa = json.loads(raw)

def b64(b): return base64.urlsafe_b64encode(b).rstrip(b'=')
now = int(time.time())
head = b64(json.dumps({'alg': 'RS256', 'typ': 'JWT'}).encode())
claim = b64(json.dumps({'iss': sa['client_email'], 'scope': 'https://www.googleapis.com/auth/webmasters',
                        'aud': 'https://oauth2.googleapis.com/token', 'iat': now, 'exp': now + 3600}).encode())
key = serialization.load_pem_private_key(sa['private_key'].encode(), None)
sig = b64(key.sign(head + b'.' + claim, padding.PKCS1v15(), hashes.SHA256()))
body = urllib.parse.urlencode({'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
                               'assertion': (head + b'.' + claim + b'.' + sig).decode()}).encode()
tok = json.load(urllib.request.urlopen(urllib.request.Request('https://oauth2.googleapis.com/token', body)))['access_token']

def call(method, url):
    r = urllib.request.Request(url, method=method, headers={'Authorization': 'Bearer ' + tok, 'Content-Length': '0'})
    with urllib.request.urlopen(r) as x:
        t = x.read().decode(); return json.loads(t) if t else {}

base = 'https://www.googleapis.com/webmasters/v3/sites/' + urllib.parse.quote(SITE, safe='') + '/sitemaps/'
for m in MAPS:
    call('PUT', base + urllib.parse.quote(m, safe=''))
    s = call('GET', base + urllib.parse.quote(m, safe=''))
    print(m, '| terakhir dikirim:', s.get('lastSubmitted'), '| error:', s.get('errors'), '| warning:', s.get('warnings'))
    for c in s.get('contents', []):
        print('  ', c.get('type'), 'dikirim:', c.get('submitted'), 'terindeks:', c.get('indexed'))
