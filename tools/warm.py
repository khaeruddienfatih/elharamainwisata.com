"""Re-render every published page once (cache-busting query) so Elementor regenerates the
per-page CSS files after an Elementor cache clear. Run after every deploy."""
import json, os, base64, random, subprocess, urllib.request

AUTH = 'Basic ' + base64.b64encode(f"{os.environ['WP_USER']}:{os.environ['WP_APP_PASSWORD']}".encode()).decode()
req = urllib.request.Request('https://www.elharamainwisata.com/wp-json/wp/v2/pages?per_page=100&status=publish&_fields=id,link',
                             headers={'Authorization': AUTH, 'User-Agent': 'curl/8.5.0'})
pages = json.load(urllib.request.urlopen(req, timeout=60))
bad = []
for p in pages:
    subprocess.run(['curl', '-sS', '-o', '/dev/null', '--max-time', '90', f"{p['link']}?warm={random.randint(1, 10**9)}"])
    code = subprocess.run(['curl', '-sS', '-o', '/dev/null', '-w', '%{http_code}', '--max-time', '60',
                           f"https://www.elharamainwisata.com/wp-content/uploads/elementor/css/post-{p['id']}.css"],
                          capture_output=True, text=True).stdout
    if code != '200':
        bad.append((p['id'], p['link'], code))
print(f'warmed {len(pages)} pages; missing css: {bad or "none"}')
