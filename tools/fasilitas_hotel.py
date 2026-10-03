"""Widget "Fasilitas Elharamain Wisata": semua hotel paket + bus, menggantikan Image Carousel lama di 9581.

Foto: gabungan 3 foto per hotel dari brosur PDF (eksterior, kamar, lobi/restoran), Cloudinary folder
Elharamainwisata/Fasilitas (public_id fasilitas-hotel-<slug>, fasilitas-bus). Slider scroll-snap (bisa digeser tanpa JS);
panah, titik & autoplay pakai JS kecil yang dikecualikan dari optimasi LiteSpeed (pola sama dengan pembimbing-slider).

Jalankan: python3 tools/fasilitas_hotel.py              -> tulis landing-pages/widget/fasilitas-hotel-bus.html
          DEPLOY=1 [SITE=wisata|id|haji] [PAGES=id,id] [DRY=1] python3 tools/fasilitas_hotel.py
              -> ganti carousel fasilitas lama (atau slider versi sebelumnya) di halaman SITES[site]
"""
import base64, json, os, re, sys, time, urllib.error, urllib.request

ROOT = os.path.join(os.path.dirname(__file__), '..')
OUT = os.path.join(ROOT, 'landing-pages', 'widget', 'fasilitas-hotel-bus.html')
IMG = 'https://res.cloudinary.com/v6gwkqrb/image/upload/c_fill,w_{w},h_{h},q_auto,f_auto/{id}.jpg'
NEW_WIDGET = 'f4c1b05'

# (slug, nama, bintang, jarak, paket)
MAKKAH = [
    ('anjum', 'Anjum Hotel', 5, '±350 m ke Masjidil Haram', 'Bronze · Silver · Silver 12 Hari'),
    ('prestige', 'Prestige Hotel', 5, '±250 m ke Masjidil Haram', 'Bronze November · Bronze Plus'),
    ('marwa-rotana', 'Marwa Rotana', 5, 'Zamzam Tower, pelataran Masjidil Haram', 'Platinum · Gold · Ramadhan Platinum'),
    ('movenpick-hajar', 'Movenpick Hajar Tower', 5, 'Zamzam Tower, pelataran Masjidil Haram', 'Platinum · Gold'),
    ('fairmont', 'Fairmont Clock Royal Tower', 5, 'Zamzam Tower, pelataran Masjidil Haram', 'Premium · Ramadhan Premium'),
    ('al-shohada', 'Al Shohada Hotel', 5, '±450 m ke Masjidil Haram', 'Ramadhan Bronze'),
    ('royal-majestic', 'Royal Majestic Hotel', 4, '±400 m ke Masjidil Haram', "I'tikaf Silver 17 Hari"),
]
MADINAH = [
    ('al-aqeeq', 'Al-Aqeeq Hotel', 5, '±50 m ke Masjid Nabawi', 'Sebagian besar paket'),
    ('peninsula-worth', 'Peninsula Worth', 5, '±150 m ke Masjid Nabawi', 'Bronze · Bronze Plus · Silver (Desember)'),
    ('movenpick-madinah', 'Movenpick Madinah', 5, '±50 m ke Masjid Nabawi', 'Platinum · Premium (Januari)'),
    ('royal-andalus', 'Royal Andalus', 4, '±30 m ke Masjid Nabawi', 'Ramadhan Bronze'),
]

PIN = '<svg viewBox="0 0 24 24"><path d="M12 22s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/></svg>'
TAG = '<svg viewBox="0 0 24 24"><path d="M20 12 12 20l-8-8V4h8z"/><circle cx="8" cy="8" r="1.5"/></svg>'

CSS = '''<style>
.ehfs{--b:#004AAD;--b2:#1684CF;--ink:#10213d;--mut:#5b6b84;--line:#e3e9f3;--gap:22px;--per:2;position:relative;max-width:1160px;margin:0 auto;padding:4px 52px 8px;font-family:Poppins,sans-serif;color:var(--ink)}
.ehfs *{box-sizing:border-box}
.ehfs .track{display:flex;gap:var(--gap);overflow-x:auto;scroll-snap-type:x mandatory;scroll-behavior:smooth;scrollbar-width:none;padding:6px 2px 18px;-webkit-overflow-scrolling:touch}
.ehfs .track::-webkit-scrollbar{display:none}
.ehfs .slide{flex:0 0 calc((100% - (var(--per) - 1) * var(--gap)) / var(--per));scroll-snap-align:start;margin:0;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 8px 22px rgba(0,40,100,.13);display:flex;flex-direction:column}
.ehfs .slide img{display:block;width:100%;height:auto;aspect-ratio:25/13;object-fit:cover;background:#dbe7f7}
.ehfs figcaption{padding:14px 18px 18px;display:flex;flex-direction:column;gap:6px}
.ehfs .kota{align-self:flex-start;background:var(--b);color:#fff;font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;padding:3px 10px;border-radius:999px}
.ehfs .kota.mad{background:#0f7a4a}.ehfs .kota.bus{background:#7a5a00}
.ehfs .st{color:#e0a800;font-size:14px;letter-spacing:2px;line-height:1}
.ehfs .st span{color:var(--mut);font-size:12px;letter-spacing:0;font-weight:600;margin-left:6px}
.ehfs h4{margin:2px 0 2px;font-family:Raleway,sans-serif;font-weight:800;font-size:19px;line-height:1.3;color:var(--ink)}
.ehfs figcaption p{margin:0;display:flex;gap:8px;align-items:flex-start;font-size:13.5px;line-height:1.5;color:var(--mut)}
.ehfs figcaption p svg{flex:none;width:16px;height:16px;margin-top:2px;stroke:var(--b2);fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.ehfs figcaption p b{color:var(--ink);font-weight:600}
.ehfs .nav{position:absolute;top:calc(50% - 40px);width:42px;height:42px;border-radius:50%;border:1px solid var(--line);background:#fff;color:var(--b);display:grid;place-items:center;cursor:pointer;box-shadow:0 4px 12px rgba(0,40,100,.18);transition:.2s;padding:0}
.ehfs .nav:hover{background:var(--b);color:#fff}
.ehfs .nav svg{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round}
.ehfs .prev{left:0}.ehfs .next{right:0}
.ehfs .dots{display:flex;justify-content:center;flex-wrap:wrap;gap:8px;margin-top:2px}
.ehfs .dots button{width:9px;height:9px;border-radius:50%;border:0;padding:0;background:#c9d1de;cursor:pointer;transition:.2s}
.ehfs .dots button.on{background:var(--b);width:22px;border-radius:5px}
.ehfs-note{text-align:center;font-size:12.5px;color:#5b6b84;margin:14px 0 0;font-family:Poppins,sans-serif}
@media (max-width:760px){.ehfs{--per:1.12;--gap:14px;padding:4px 0 8px}.ehfs .nav{display:none}.ehfs .track{padding-left:16px;padding-right:16px;scroll-padding-left:16px}.ehfs h4{font-size:17px}}
</style>'''


def stars(n):
    return f'<div class="st">{"★" * n}<span>Hotel Bintang {n}</span></div>'


def img(pid, alt):
    src = IMG.format(w=800, h=416, id=pid)
    srcset = ', '.join(f'{IMG.format(w=w, h=round(w * 0.52), id=pid)} {w}w' for w in (480, 800, 1000))
    return (f'<img src="{src}" srcset="{srcset}" sizes="(max-width:760px) 90vw, 540px" '
            f'width="1000" height="520" loading="lazy" decoding="async" alt="{alt}">')


def hotel(slug, nama, bintang, jarak, paket, kota):
    cls = 'kota' if kota == 'Makkah' else 'kota mad'
    return (f'<figure class="slide">{img("fasilitas-hotel-" + slug, nama + " " + kota + " - hotel paket umroh Elharamain Wisata")}'
            f'<figcaption><span class="{cls}">Hotel {kota}</span>{stars(bintang)}<h4>{nama}</h4>'
            f'<p>{PIN}<span>{jarak}</span></p><p>{TAG}<span>Paket: <b>{paket}</b></span></p></figcaption></figure>')


BUS = (f'<figure class="slide">{img("fasilitas-bus", "Bus terbaru jamaah umroh Elharamain Wisata")}'
       '<figcaption><span class="kota bus">Transportasi</span><h4>Bus Terbaru Ber-AC</h4>'
       f'<p>{PIN}<span>Penjemputan bandara, perjalanan antar kota Makkah – Madinah – Jeddah, dan seluruh program ziarah &amp; city tour.</span></p>'
       f'<p>{TAG}<span>Madinah → Makkah naik <b>Kereta Cepat Haramain</b> (sesuai paket).</span></p></figcaption></figure>')

ARROW_L = '<svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg>'
ARROW_R = '<svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg>'
JS = """<script data-no-optimize="1" data-no-defer="1" data-cfasync="false">
(function(){
  function init(){
    var root=document.getElementById('ehfs'); if(!root||root.dataset.ok) return; root.dataset.ok=1;
    var track=root.querySelector('.track'), slides=track.children, dots=root.querySelector('.dots'), timer;
    function gap(){return parseFloat(getComputedStyle(track).columnGap)||22;}
    function step(){return slides[0].getBoundingClientRect().width+gap();}
    function perView(){return Math.max(1,Math.floor((track.clientWidth+gap()+1)/step()));}
    function pages(){return Math.max(1,slides.length-perView()+1);}
    function cur(){return Math.round(track.scrollLeft/step());}
    function go(i){var n=pages();i=(i+n)%n;track.scrollTo({left:i*step(),behavior:'smooth'});}
    function drawDots(){var n=pages(),h='';for(var i=0;i<n;i++)h+='<button type="button" aria-label="Slide '+(i+1)+'"></button>';dots.innerHTML=h;mark();}
    function mark(){var c=cur();[].forEach.call(dots.children,function(b,i){b.classList.toggle('on',i===c);});}
    function restart(){clearInterval(timer);timer=setInterval(function(){if(!document.hidden)go(cur()+1);},4000);}
    root.querySelector('.prev').addEventListener('click',function(){go(cur()-1);restart();});
    root.querySelector('.next').addEventListener('click',function(){go(cur()+1);restart();});
    dots.addEventListener('click',function(e){var i=[].indexOf.call(dots.children,e.target);if(i>-1){go(i);restart();}});
    track.addEventListener('scroll',function(){clearTimeout(track._t);track._t=setTimeout(mark,80);},{passive:true});
    root.addEventListener('mouseenter',function(){clearInterval(timer);});
    root.addEventListener('mouseleave',restart);
    track.addEventListener('touchstart',function(){clearInterval(timer);},{passive:true});
    window.addEventListener('resize',drawDots);
    drawDots();restart();
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
</script>"""


def build():
    slides = ([hotel(*h, 'Makkah') for h in MAKKAH] + [hotel(*h, 'Madinah') for h in MADINAH] + [BUS])
    return (CSS + '<div class="ehfs" id="ehfs" aria-roledescription="carousel" aria-label="Fasilitas hotel dan bus Elharamain Wisata">'
            f'<button type="button" class="nav prev" aria-label="Sebelumnya">{ARROW_L}</button>'
            '<div class="track">' + ''.join(slides) + '</div>'
            f'<button type="button" class="nav next" aria-label="Berikutnya">{ARROW_R}</button>'
            '<div class="dots"></div></div>'
            '<p class="ehfs-note">Hotel sesuai paket yang dipilih atau setaraf. Jarak perkiraan dari brosur resmi Elharamain Wisata.</p>'
            + JS)


# Carousel "Fasilitas Elharamain Wisata" lama: 7 slide 2025 (bus, Swissotel, Marwa Rotana, Anjum, Al-Aqeeq, Taiba Front,
# Taiba) dengan nama file 10 / 2-1 ... 7-1 (+ akhiran duplikat WordPress), dipakai di ketiga situs.
OLD_RE = re.compile(r'^(10|[2-7]-1)(-\d+)*(\.jpg)?(-\d+)*\.(jpg|webp)$')
SITES = {  # situs: (base REST, env user, env app password, halaman)
    'wisata': ('https://www.elharamainwisata.com/wp-json', 'WP_USER', 'WP_APP_PASSWORD',
               [9581, 7840, 8869, 8896, 8908, 8909, 8910, 9584, 9585, 9586, 9587, 9588, 9589]),
    'id': ('https://www.elharamain.id/wp-json', 'ELHARAMAINID_USER', 'ELHARAMAINID_WP_APP_PASSWORD',
           [309, 783, 496, 480, 476, 472, 468, 464, 439, 385, 351, 210]),
    'haji': ('https://www.elharamainhaji.com/wp-json', 'ELHARAMAINHAJI_USER', 'ELHARAMAINHAJI_WP_APP_PASSWORD',
             [230, 220, 210, 175]),
}


def requester(site):
    # Pakai curl: Cloudflare di elharamain.id / elharamainhaji.com kadang menolak urllib Python (403 / halaman challenge).
    import subprocess, tempfile
    base, u, pw, _ = SITES[site]

    def req(method, path, data=None):
        cmd = ['curl', '-sS', '--max-time', '120', '-X', method, '-u', f"{os.environ[u]}:{os.environ[pw]}",
               '-A', 'Mozilla/5.0 eh-admin', '-H', 'Content-Type: application/json', '-w', '\n%{http_code}']
        tmp = None
        if data is not None:
            tmp = tempfile.NamedTemporaryFile('w', suffix='.json', delete=False)
            json.dump(data, tmp)
            tmp.close()
            cmd += ['--data-binary', '@' + tmp.name]
        out = subprocess.run(cmd + [base + path], capture_output=True, text=True).stdout
        if tmp:
            os.unlink(tmp.name)
        body, _, code = out.rpartition('\n')
        try:
            return int(code), (json.loads(body) if body else None)
        except ValueError:
            # elharamain.id membocorkan <style id="elementor-post-N"> di depan JSON respons REST: lewati sampai awal JSON.
            for m in re.finditer(r'[\[{]"', body):
                try:
                    return int(code), json.JSONDecoder().raw_decode(body, m.start())[0]
                except ValueError:
                    continue
            return int(code or 0), body[:300]
    return req


def is_old_carousel(e):
    if e.get('widgetType') != 'image-carousel':
        return False
    c = e.get('settings', {}).get('carousel') or []
    if isinstance(c, str):
        c = json.loads(c)
    names = [os.path.basename(x.get('url', '')) for x in c if isinstance(x, dict)]
    return len(names) == 7 and sum(bool(OLD_RE.match(n)) for n in names) >= 6


def deploy(html, pid, req, site):
    for i in range(6):
        try:
            st, raw = req('GET', f'/wp/v2/pages/{pid}?context=edit')
            if st == 200 and isinstance(raw, dict):
                break
        except (json.JSONDecodeError, urllib.error.URLError, ValueError):
            pass
        time.sleep(20)
    else:
        raise SystemExit(f'gagal GET {site} {pid}')
    data = raw['meta']['_elementor_data']
    bdir = os.path.join(ROOT, 'backup', '2026-10-03')
    os.makedirs(bdir, exist_ok=True)
    prefix = '' if site == 'wisata' else site + '-'
    with open(os.path.join(bdir, f'{prefix}{pid}_sebelum_fasilitas_{time.strftime("%H%M")}.json'), 'w') as f:
        f.write(data)
    els = json.loads(data)
    n = 0

    def swap(es):
        nonlocal n
        for i, e in enumerate(es):
            st = e.get('settings', {})
            mine = e.get('widgetType') == 'html' and 'id="ehfs"' in st.get('html', '')
            if is_old_carousel(e) or mine:
                es[i] = {'id': e['id'] if mine else NEW_WIDGET, 'elType': 'widget', 'widgetType': 'html', 'elements': [],
                         'settings': {'html': html, '_margin': {'unit': 'px', 'top': '10', 'right': '0', 'bottom': '25', 'left': '0', 'isLinked': False}}}
                n += 1
            else:
                swap(e.get('elements', []))

    swap(els)
    assert n == 1, (site, pid, n)
    if os.environ.get('DRY') == '1':
        print('DRY', site, pid, 'OK')
        return
    st, r = req('POST', f'/wp/v2/pages/{pid}', {'meta': {'_elementor_data': json.dumps(els, ensure_ascii=False)}})
    print('POST', site, pid, st)
    assert st == 200, r


if __name__ == '__main__':
    html = build()
    assert '<!--' not in html
    with open(OUT, 'w') as f:
        f.write(html + '\n')
    print('tulis', OUT, len(html), 'byte')
    if os.environ.get('DEPLOY') == '1':
        site = os.environ.get('SITE', 'wisata')
        req = requester(site)
        for pid in [int(x) for x in os.environ.get('PAGES', '').split(',') if x] or SITES[site][3]:
            deploy(html, pid, req, site)
        if os.environ.get('DRY') != '1':
            print('hapus cache elementor:', req('DELETE', '/elementor/v1/cache')[0])
