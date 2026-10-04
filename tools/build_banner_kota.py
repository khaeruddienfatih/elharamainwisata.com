"""Banner 1200x630 per kota untuk haji.biz (featured image / OG). Render dengan Chromium (playwright).
Teks dirender sendiri (bukan gambar AI) supaya ejaan, harga, dan nama kota selalu benar.
Pakai: python3 tools/build_banner_kota.py   -> wordpress/haji-biz/gambar/haji-plus-<kota>.png
"""
import os, base64, subprocess, json, tempfile, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'wordpress', 'haji-biz', 'gambar')
spec = importlib.util.spec_from_file_location('bk', os.path.join(HERE, 'build_haji_kota.py'))
bk = importlib.util.module_from_spec(spec); spec.loader.exec_module(bk)


def font(w):
    b = open(os.path.join(HERE, 'fonts', 'poppins-latin-%d-normal.woff2' % w), 'rb').read()
    return "@font-face{font-family:P;font-weight:%d;src:url(data:font/woff2;base64,%s) format('woff2')}" % (w, base64.b64encode(b).decode())


def page(kota, kantor):
    return f"""<!doctype html><meta charset=utf-8><style>{font(500)}{font(700)}{font(800)}
*{{box-sizing:border-box;margin:0}}body{{width:1200px;height:630px;font-family:P,sans-serif;color:#fff;overflow:hidden;
background:linear-gradient(135deg,#0a2e6b 0%,#004AAD 55%,#1684CF 100%);position:relative}}
.pat{{position:absolute;right:-120px;top:-60px;width:760px;height:760px;opacity:.16}}
.arch{{position:absolute;right:70px;bottom:0;width:360px;height:520px}}
.in{{position:absolute;left:64px;top:56px;width:700px}}
.tag{{display:inline-block;font-size:21px;font-weight:700;letter-spacing:.08em;color:#DBC033;border:2px solid #DBC033;border-radius:999px;padding:8px 20px}}
h1{{font-size:58px;font-weight:700;line-height:1.1;margin-top:34px}}
h2{{font-size:118px;font-weight:800;line-height:1.02;color:#DBC033;margin-top:2px}}
.sub{{font-size:27px;font-weight:500;margin-top:26px;color:#e6efff}}
.chips{{position:absolute;left:64px;bottom:48px;display:flex;gap:14px}}
.chip{{background:rgba(255,255,255,.14);border:1.5px solid rgba(255,255,255,.4);border-radius:14px;padding:12px 20px;font-size:23px;font-weight:700}}
.chip small{{display:block;font-size:15px;font-weight:500;color:#cfe0ff}}
.brand{{position:absolute;right:64px;top:52px;font-size:23px;font-weight:700;letter-spacing:.04em}}
</style>
<svg class="pat" viewBox="0 0 200 200"><g fill="none" stroke="#fff" stroke-width="1.2">
<polygon points="100,10 122,60 176,60 132,94 150,148 100,116 50,148 68,94 24,60 78,60"/>
<polygon points="100,28 116,66 156,66 124,90 136,130 100,106 64,130 76,90 44,66 84,66"/>
<circle cx="100" cy="100" r="90"/><circle cx="100" cy="100" r="70"/></g></svg>
<svg class="arch" viewBox="0 0 360 520"><path d="M20 520V230C20 120 90 40 180 20C270 40 340 120 340 230V520" fill="none" stroke="#DBC033" stroke-width="7"/>
<path d="M60 520V240C60 150 110 84 180 66C250 84 300 150 300 240V520" fill="rgba(255,255,255,.07)" stroke="rgba(219,192,51,.55)" stroke-width="3"/>
<defs><mask id="m"><rect width="360" height="520" fill="#fff"/><circle cx="196" cy="160" r="27" fill="#000"/></mask></defs><circle cx="180" cy="170" r="32" fill="#DBC033" mask="url(#m)"/></svg>
<div class="brand">ELHARAMAIN WISATA</div>
<div class="in"><span class="tag">PIHK RESMI KEMENAG RI</span><h1>Paket Haji Plus</h1><h2>{kota}</h2>
<div class="sub">{kantor}. Daftar bisa dari mana saja.</div></div>
<div class="chips"><div class="chip"><small>Paket mulai</small>12.000 USD</div><div class="chip"><small>Setoran awal</small>4.000 USD</div><div class="chip"><small>SK Kemenag</small>No. 846/2020</div></div>"""


def main():
    os.makedirs(OUT, exist_ok=True)
    files = []
    for c in bk.KOTA:
        slug = 'haji-plus-' + c['kota'].lower()
        h = os.path.join(OUT, slug + '.html')
        open(h, 'w').write(page(c['kota'], c['kantor']))
        files.append((h, os.path.join(OUT, slug + '.png')))
    js = os.path.join(HERE, 'shot_html.js')
    subprocess.run(['node', js] + [x for pair in files for x in pair], check=True)
    for _, png in files:
        print('ok', os.path.relpath(png, os.path.join(HERE, '..')))


if __name__ == '__main__':
    main()
