#!/usr/bin/env python3
"""Bot "Request Indexing" Search Console untuk Windows (dibuat jadi .exe via GitHub Actions).

Cara kerja: membuka Google Chrome milik Anda dengan profil khusus (login Google sekali, tersimpan),
lalu untuk tiap URL di urls.txt membuka URL Inspection dan menekan "Minta pengindeksan".
Tidak menyimpan/menanyakan password. Hasil dicatat ke hasil-indexing.csv.
Pakai:  gsc-indexing-bot.exe [urls.txt] [--site sc-domain:haji.biz] [--max 10]
"""
import argparse, csv, os, re, sys, time, urllib.parse
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

ap = argparse.ArgumentParser()
ap.add_argument('urls', nargs='?', default='urls.txt')
ap.add_argument('--site', default='sc-domain:haji.biz')
ap.add_argument('--max', type=int, default=10, help='batas URL per jalan (kuota harian Google ~10-20)')
a = ap.parse_args()

base = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__))
urls_path = a.urls if os.path.isabs(a.urls) else os.path.join(os.getcwd(), a.urls)
if not os.path.exists(urls_path): urls_path = os.path.join(base, a.urls)
urls = [l.strip() for l in open(urls_path, encoding='utf-8') if l.strip() and not l.startswith('#')]
log_path = os.path.join(base, 'hasil-indexing.csv')
done = set()
if os.path.exists(log_path):
    done = {r[1] for r in csv.reader(open(log_path, encoding='utf-8')) if len(r) > 2 and r[2] == 'OK'}
todo = [u for u in urls if u not in done][:a.max]
print(f'{len(urls)} URL, {len(done)} sudah OK, diproses sekarang: {len(todo)}')

BTN = re.compile(r'(Request indexing|Minta pengindeksan)', re.I)
OKTXT = re.compile(r'(Indexing requested|Pengindeksan diminta)', re.I)
QUOTA = re.compile(r'(Quota exceeded|Kuota terlampaui)', re.I)
ALREADY = re.compile(r'(URL is on Google|URL ada di Google)', re.I)

def log(url, status):
    with open(log_path, 'a', newline='', encoding='utf-8') as f:
        csv.writer(f).writerow([datetime.now().isoformat(timespec='seconds'), url, status])
    print(status, url)

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(os.path.join(base, 'profil-chrome'), channel='chrome', headless=False,
                                               viewport={'width': 1280, 'height': 900})
    pg = ctx.pages[0] if ctx.pages else ctx.new_page()
    pg.goto('https://search.google.com/search-console')
    print('Jika diminta, login Google di jendela Chrome (sekali saja). Menunggu sampai Search Console terbuka...')
    pg.wait_for_url(re.compile(r'search\.google\.com/search-console'), timeout=600000)
    for u in todo:
        try:
            pg.goto('https://search.google.com/search-console/inspect?resource_id=' + urllib.parse.quote(a.site, safe='')
                    + '&id=' + urllib.parse.quote(u, safe=''))
            pg.wait_for_selector('text=/URL is on Google|URL is not on Google|URL ada di Google|URL tidak ada di Google|URL is unknown/i', timeout=120000)
            btn = pg.get_by_role('button', name=BTN)
            if btn.count() == 0:
                log(u, 'TIDAK_ADA_TOMBOL'); continue
            btn.first.click()
            pg.wait_for_selector('text=/Indexing requested|Pengindeksan diminta|Quota exceeded|Kuota terlampaui|Testing if live URL/i', timeout=240000)
            t = pg.inner_text('body')
            if QUOTA.search(t): log(u, 'KUOTA_HABIS'); break
            pg.wait_for_selector('text=/Indexing requested|Pengindeksan diminta/i', timeout=240000)
            log(u, 'OK')
            time.sleep(3)
        except PWTimeout:
            log(u, 'TIMEOUT')
        except Exception as e:
            log(u, 'ERROR ' + str(e)[:80])
    ctx.close()
print('Selesai. Lihat hasil-indexing.csv')
