#!/usr/bin/env python3
"""Bot "Request Indexing" Search Console untuk Windows (dibuat jadi .exe via GitHub Actions).

Cara kerja: membuka Google Chrome milik Anda dengan profil khusus (login Google SENDIRI sekali, tersimpan),
lalu untuk tiap URL di urls.txt membuka URL Inspection dan menekan "Minta pengindeksan".
Tidak menyimpan/menanyakan password. Hasil dicatat ke hasil-indexing.csv.
Pakai:  gsc-indexing-bot.exe [urls.txt] [--site sc-domain:haji.biz] [--max 10]
"""
import argparse, csv, os, re, sys, time, urllib.parse
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

ap = argparse.ArgumentParser()
ap.add_argument('urls', nargs='?', default='urls.txt')
ap.add_argument('--site', default='', help='mis. sc-domain:haji.biz atau https://haji.biz/ (default: coba keduanya)')
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

import glob, socket, subprocess
def find_chrome():
    for pat in (r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
                os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe')):
        if os.path.exists(pat): return pat
    sys.exit('Google Chrome tidak ditemukan. Pasang Chrome dulu.')

PORT = 9222
def port_open():
    with socket.socket() as k:
        k.settimeout(0.5); return k.connect_ex(('127.0.0.1', PORT)) == 0

# Chrome dibuka SEPERTI BIASA (tanpa kontrol otomatis) supaya Google mau menerima login.
# Profil khusus disimpan di folder profil-chrome (login sekali, tersimpan).
if not port_open():
    subprocess.Popen([find_chrome(), f'--remote-debugging-port={PORT}', '--no-first-run',
                      '--user-data-dir=' + os.path.join(base, 'profil-chrome'),
                      'https://search.google.com/search-console'])
    for _ in range(40):
        if port_open(): break
        time.sleep(0.5)
print('Chrome terbuka. Login ke Google di jendela itu sampai halaman Search Console tampil.')
input('Setelah login selesai, tekan ENTER di sini untuk mulai... ')

with sync_playwright() as p:
    br = p.chromium.connect_over_cdp(f'http://127.0.0.1:{PORT}')
    ctx = br.contexts[0]
    pg = ctx.new_page()
    cands = [a.site] if a.site else ['sc-domain:haji.biz', 'https://haji.biz/', 'https://www.haji.biz/']
    site = None
    for c in cands:
        pg.goto('https://search.google.com/search-console?resource_id=' + urllib.parse.quote(c, safe=''))
        pg.wait_for_load_state('networkidle'); time.sleep(2)
        t = pg.inner_text('body')
        if not re.search(r'(not found|404|tidak ditemukan|don.t have access|tidak memiliki akses)', t, re.I) \
           and pg.get_by_role('combobox').count() + pg.locator('input[type=text],input[type=search]').count() > 0:
            site = c; break
    if not site:
        pg.screenshot(path=os.path.join(base, 'gagal-properti.png'))
        sys.exit('Properti haji.biz tidak ditemukan di akun ini. Pastikan sudah login dengan akun yang benar dan properti sudah ditambahkan. Lihat gagal-properti.png')
    print('Properti dipakai:', site)
    BOX = pg.locator('input[aria-label*="Inspect" i], input[aria-label*="Periksa" i], input[placeholder*="Inspect" i], input[placeholder*="Periksa" i]')
    for u in todo:
        try:
            if BOX.count() == 0:
                pg.goto('https://search.google.com/search-console?resource_id=' + urllib.parse.quote(site, safe=''))
                pg.wait_for_load_state('networkidle')
            BOX.first.click(); BOX.first.fill(u); BOX.first.press('Enter')
            pg.wait_for_selector('text=/URL is on Google|URL is not on Google|URL ada di Google|URL tidak ada di Google|URL is unknown|URL tidak diketahui/i', timeout=180000)
            btn = pg.get_by_role('button', name=BTN)
            if btn.count() == 0:
                log(u, 'TIDAK_ADA_TOMBOL'); continue
            btn.first.click()
            pg.wait_for_selector('text=/Indexing requested|Pengindeksan diminta|Quota exceeded|Kuota terlampaui/i', timeout=300000)
            t = pg.inner_text('body')
            if QUOTA.search(t): log(u, 'KUOTA_HABIS'); break
            log(u, 'OK')
            pg.keyboard.press('Escape'); time.sleep(3)
            pg.goto('https://search.google.com/search-console?resource_id=' + urllib.parse.quote(site, safe=''))
            pg.wait_for_load_state('networkidle')
        except PWTimeout:
            log(u, 'TIMEOUT')
            pg.screenshot(path=os.path.join(base, 'timeout-%d.png' % int(time.time())))
        except Exception as e:
            log(u, 'ERROR ' + str(e)[:80])
    br.close()
print('Selesai. Lihat hasil-indexing.csv')
