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
    HOME = 'https://search.google.com/search-console?resource_id=' + urllib.parse.quote(site, safe='')

    def seen(rx):
        """True jika ada SALAH SATU elemen yang cocok dan terlihat (elemen pertama bisa tersembunyi)."""
        try:
            loc = pg.get_by_text(re.compile(rx, re.I))
            for i in range(min(loc.count(), 12)):
                if loc.nth(i).is_visible(): return True
        except Exception: pass
        try:
            return bool(pg.evaluate("""rx => { const r = new RegExp(rx, 'i');
              const w = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);
              const seenEls = (root) => { for (const el of root.querySelectorAll('*')) {
                  if (el.shadowRoot && seenEls(el.shadowRoot)) return true;
                  if (el.children.length === 0 && r.test(el.textContent || '')) {
                    const b = el.getBoundingClientRect(); if (b.width > 0 && b.height > 0) return true; } } return false; };
              return seenEls(document); }""", rx))
        except Exception: return False

    def dismiss():
        """Tutup dialog: klik tombol Dismiss/Tutup (termasuk di shadow DOM), lalu Escape sebagai cadangan."""
        try:
            ok = pg.evaluate("""() => { const names = /^(dismiss|tutup|got it|mengerti|ok)$/i;
              const find = (root) => { for (const el of root.querySelectorAll('*')) {
                  if (el.shadowRoot) { const f = find(el.shadowRoot); if (f) return f; }
                  const t = (el.textContent || '').trim();
                  if (names.test(t) && (el.tagName === 'BUTTON' || el.getAttribute('role') === 'button' || /button/i.test(el.tagName))) {
                    const b = el.getBoundingClientRect(); if (b.width > 0 && b.height > 0) return el; } } return null; };
              const el = find(document); if (el) { el.click(); return true; } return false; }""")
            if ok: return True
        except Exception: pass
        try: pg.keyboard.press('Escape')
        except Exception: pass
        return False

    def wait_any(rxs, timeout):
        """Tunggu sampai salah satu teks muncul; kembalikan regex yang cocok atau None."""
        end = time.time() + timeout
        while time.time() < end:
            for rx in rxs:
                if seen(rx): return rx
            time.sleep(1)
        return None

    RESULT = [r'URL is on Google', r'URL is not on Google', r'URL ada di Google', r'URL tidak ada di Google',
              r'URL is unknown', r'URL tidak diketahui', r'Page is not indexed', r'Halaman tidak diindeks']
    DONE = [r'Indexing requested', r'Pengindeksan diminta']
    QUO = [r'Quota exceeded', r'Kuota terlampaui']
    FAIL = [r'Indexing request rejected', r'Permintaan pengindeksan ditolak', r'Something went wrong', r'Terjadi kesalahan']

    for u in todo:
        try:
            print('-> ', u)
            pg.goto(HOME); pg.wait_for_load_state('networkidle'); time.sleep(1)
            BOX.first.click(); BOX.first.fill(u); BOX.first.press('Enter')
            print('   menunggu hasil inspeksi...')
            if not wait_any(RESULT, 180): raise PWTimeout('hasil inspeksi tidak muncul')
            btn = pg.get_by_role('button', name=BTN)
            if btn.count() == 0:
                log(u, 'TIDAK_ADA_TOMBOL'); continue
            print('   klik Minta pengindeksan (Google menguji URL live, bisa 1-2 menit)...')
            btn.first.click()
            r = wait_any(DONE + QUO + FAIL, 360)
            if r is None: raise PWTimeout('dialog hasil tidak muncul')
            if r in QUO: log(u, 'KUOTA_HABIS'); break
            if r in FAIL: log(u, 'DITOLAK_GOOGLE'); continue
            log(u, 'OK')
            dismiss(); time.sleep(2)
        except PWTimeout as e:
            log(u, 'TIMEOUT ' + str(e)[:60])
            pg.screenshot(path=os.path.join(base, 'timeout-%d.png' % int(time.time())))
        except Exception as e:
            log(u, 'ERROR ' + str(e)[:80])
            pg.screenshot(path=os.path.join(base, 'error-%d.png' % int(time.time())))
    br.close()
print('Selesai. Lihat hasil-indexing.csv')
