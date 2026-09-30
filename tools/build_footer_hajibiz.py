"""Footer haji.biz = footer elharamainwisata.com (tools/build_footer.py) apa adanya, untuk ditempel manual di UAE.

Beda dari versi utama: tanpa CSS penyembunyi footer tema LandingPress dan tanpa JSON-LD organisasi
(schema TravelAgency cukup di elharamainwisata.com). Semua tautan absolut ke elharamainwisata.com.
Usage: python3 tools/build_footer_hajibiz.py -> wordpress/uae/haji-biz-footer.html (+ build/preview-footer-hajibiz.html)
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_footer as bf

html = bf.footer_html()
html = re.sub(r'<script type="application/ld\+json">.*?</script>', '', html, flags=re.S)
html = re.sub(r'/\* hide LandingPress.*?footer#colophon\.site-footer\{display:none!important\}\n', '', html, flags=re.S)
html = html.replace('aria-label="Footer Elharamain Wisata"', 'aria-label="Footer Haji.biz"')
head = ('<!-- Footer haji.biz. Tempel ke widget "HTML" Elementor di UAE > Footer (Display: Entire Website).\n'
        '     Dibuat oleh tools/build_footer_hajibiz.py dari tools/build_footer.py; jangan edit manual. -->\n')
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
open(os.path.join(root, 'wordpress/uae/haji-biz-footer.html'), 'w').write(head + html)
os.makedirs(os.path.join(root, 'build'), exist_ok=True)
open(os.path.join(root, 'build/preview-footer-hajibiz.html'), 'w').write(
    '<html><head><meta name=viewport content="width=device-width,initial-scale=1">'
    '<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&family=Raleway:wght@800&display=swap" rel=stylesheet>'
    '</head><body style="margin:0;background:#fff"><div style="height:120px"></div>' + html + '</body></html>')
print('ok', len(html))
