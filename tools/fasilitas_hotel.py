"""Widget "Fasilitas Elharamain Wisata": semua hotel paket + bus, menggantikan Image Carousel lama di 9581.

Foto: gabungan 3 foto per hotel dari brosur PDF (eksterior, kamar, lobi/restoran), Cloudinary folder
Elharamainwisata/Fasilitas (public_id fasilitas-hotel-<slug>, fasilitas-bus). Slider scroll-snap (bisa digeser tanpa JS);
panah, titik & autoplay pakai JS kecil yang dikecualikan dari optimasi LiteSpeed (pola sama dengan pembimbing-slider).

Jalankan: python3 tools/fasilitas_hotel.py              -> tulis landing-pages/widget/fasilitas-hotel-bus.html
          DEPLOY=1 python3 tools/fasilitas_hotel.py     -> juga pasang di halaman 9581 (ganti carousel 73bd261 / widget f4c1b05)
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(__file__))

ROOT = os.path.join(os.path.dirname(__file__), '..')
OUT = os.path.join(ROOT, 'landing-pages', 'widget', 'fasilitas-hotel-bus.html')
IMG = 'https://res.cloudinary.com/v6gwkqrb/image/upload/c_fill,w_{w},h_{h},q_auto,f_auto/{id}.jpg'
PAGE, OLD_WIDGET, NEW_WIDGET = 9581, '73bd261', 'f4c1b05'

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


def deploy(html):
    from wp_rest import req
    for i in range(6):
        try:
            st, raw = req('GET', f'/wp/v2/pages/{PAGE}?context=edit')
            if st == 200 and isinstance(raw, dict):
                break
        except json.JSONDecodeError:
            pass
        time.sleep(20)
    data = raw['meta']['_elementor_data']
    bdir = os.path.join(ROOT, 'backup', '2026-10-03')
    os.makedirs(bdir, exist_ok=True)
    with open(os.path.join(bdir, f'{PAGE}_sebelum_fasilitas_{time.strftime("%H%M")}.json'), 'w') as f:
        f.write(data)
    els = json.loads(data)

    def swap(es):
        for i, e in enumerate(es):
            if e.get('id') in (OLD_WIDGET, NEW_WIDGET):
                assert e.get('widgetType') in ('image-carousel', 'html'), e.get('widgetType')
                es[i] = {'id': NEW_WIDGET, 'elType': 'widget', 'widgetType': 'html', 'elements': [],
                         'settings': {'html': html, '_margin': {'unit': 'px', 'top': '10', 'right': '0', 'bottom': '25', 'left': '0', 'isLinked': False}}}
                return True
            if swap(e.get('elements', [])):
                return True
        return False

    assert swap(els), 'widget carousel tidak ditemukan'
    st, r = req('POST', f'/wp/v2/pages/{PAGE}', {'meta': {'_elementor_data': json.dumps(els, ensure_ascii=False)}})
    print('POST', PAGE, st)
    assert st == 200, r
    print('hapus cache elementor:', req('DELETE', '/elementor/v1/cache')[0])


if __name__ == '__main__':
    html = build()
    assert '<!--' not in html
    with open(OUT, 'w') as f:
        f.write(html + '\n')
    print('tulis', OUT, len(html), 'byte')
    if os.environ.get('DEPLOY') == '1':
        deploy(html)
