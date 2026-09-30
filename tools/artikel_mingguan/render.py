"""Blok HTML artikel (gaya .ea, tanpa JS; aman dengan LiteSpeed) + helper SEO."""
import html
import json
import urllib.parse

from data import (BATAL, BELUM, DOKUMEN, FASILITAS, HAJI, HOTEL, OLEH, PAKET, PEMBIMBING, PERLENGKAPAN_PRIA,
                  PERLENGKAPAN_WANITA, REKENING)

CLD = 'https://res.cloudinary.com/v6gwkqrb/image/upload/'
WA = 'https://api.whatsapp.com/send?phone=6281287292422&text='
KEMENAG = 'https://kemenag.go.id/'

CSS = '''<style>
.ea{--b:#004AAD;--n:#0a2e6b;font-family:Poppins,sans-serif;color:#26364d;line-height:1.8;font-size:16.5px;max-width:820px;margin:0 auto}
.ea *{box-sizing:border-box}
.ea h2{font-family:Poppins,sans-serif!important;font-weight:700!important;color:var(--n);font-size:24px;line-height:1.3;margin:34px 0 12px}
.ea h3{font-family:Poppins,sans-serif!important;font-weight:700!important;color:var(--n);font-size:18.5px;margin:22px 0 8px}
.ea a{color:var(--b)}
.ea-fig{margin:20px 0}.ea-fig img{max-width:100%;height:auto;border-radius:14px;display:block;margin:0 auto}
.ea-fig figcaption{font-size:13px;color:#6b7a90;text-align:center;margin-top:6px}
.ea-box{background:#f5f8fd;border-left:4px solid var(--b);border-radius:10px;padding:16px 18px;margin:18px 0}
.ea-toc{background:#f8fafd;border:1px solid #e1e8f3;border-radius:12px;padding:14px 18px;margin:18px 0}
.ea-toc b{color:var(--n)}.ea-toc ol{margin:6px 0 0}
.ea-tw{overflow-x:auto;margin:14px 0;border:1px solid #e1e8f3;border-radius:12px}
.ea table{width:100%;border-collapse:collapse;font-size:14.5px;min-width:560px}
.ea th{background:var(--n);color:#fff;text-align:left;padding:10px 12px;font-weight:600}
.ea td{padding:10px 12px;border-top:1px solid #e1e8f3;vertical-align:top}
.ea tr:nth-child(even) td{background:#f8fafd}
.ea ul,.ea ol{padding-left:22px}.ea li{margin:5px 0}
.ea-cta{text-align:center;margin:30px 0}
.ea-cta a{display:inline-block;background:#25D366;color:#fff!important;font-weight:700;padding:14px 26px;border-radius:12px;text-decoration:none}
.ea details{border:1px solid #e1e8f3;border-radius:10px;padding:12px 16px;margin:10px 0}
.ea summary{font-weight:600;color:var(--n);cursor:pointer}
.ea-rel{border-top:1px solid #e1e8f3;margin-top:28px;padding-top:14px}
@media(max-width:640px){.ea{font-size:15.5px}.ea h2{font-size:21px}}
</style>'''


def e(s):
    return html.escape(str(s), quote=True)


def rp(n):
    return 'Rp ' + f'{n:,}'.replace(',', '.')


def usd(n):
    return f'{n:,}'.replace(',', '.') + ' USD'


def wa(text):
    return WA + urllib.parse.quote(text)


def img_url(pid, w=1200, h=None):
    t = f'c_fill,g_auto,w_{w},h_{h},q_auto,f_auto' if h else f'c_limit,w_{w},q_auto,f_auto'
    return f'{CLD}{t}/{pid}.jpg' if not pid.startswith('http') else pid


def fig(pid, alt, w=1200, h=None, cap=None):
    hattr = f' height="{h}"' if h else ''
    return (f'<figure class="ea-fig"><img src="{img_url(pid, w, h)}" alt="{e(alt)}" loading="lazy" width="{w}"{hattr}>'
            + (f'<figcaption>{cap}</figcaption>' if cap else '') + '</figure>')


def ul(items):
    return '<ul>' + ''.join(f'<li>{x}</li>' for x in items) + '</ul>'


def ol(items):
    return '<ol>' + ''.join(f'<li>{x}</li>' for x in items) + '</ol>'


def table(head, rows):
    return ('<div class="ea-tw"><table><thead><tr>' + ''.join(f'<th>{h}</th>' for h in head) + '</tr></thead><tbody>'
            + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows) + '</tbody></table></div>')


def paket(filter_fn, cols=('label', 'bulan', 'hari', 'berangkat', 'makkah', 'madinah', 'q', 't', 'd')):
    names = {'label': 'Paket', 'bulan': 'Bulan', 'hari': 'Durasi', 'berangkat': 'Berangkat', 'makkah': 'Hotel Makkah',
             'madinah': 'Hotel Madinah', 'maskapai': 'Maskapai', 'q': 'Ber-4', 't': 'Ber-3', 'd': 'Ber-2'}
    rows = []
    for p in PAKET:
        if not filter_fn(p):
            continue
        r = []
        for c in cols:
            v = p[c]
            r.append(rp(v) if c in 'qtd' else (f'{v} hari' if c == 'hari' else (f'<b>{e(v)}</b>' if c == 'label' else e(v))))
        rows.append(r)
    return table([names[c] for c in cols], rows)


def paket_list(filter_fn):
    return [p for p in PAKET if filter_fn(p)]


def haji_table():
    return table(['Paket', 'Ber-4', 'Ber-3', 'Ber-2', 'Durasi', 'Maktab VIP'],
                 [[f'<b>{n}</b>', usd(a), usd(b), usd(c), dur, f'{mk} (tenda {jt})'] for n, a, b, c, mh, md, dur, mk, jt in HAJI])


def hotel_line(name):
    kota, jarak = HOTEL[name]
    return f'<b>{e(name)}</b> ({kota})' + (f' — {jarak}' if jarak else '')


def faq_block(faqs):
    items = ''.join(f'<details><summary>{e(q)}</summary><p>{a}</p></details>' for q, a in faqs)
    ld = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': html.unescape(
            __import__('re').sub('<[^>]+>', '', a))}} for q, a in faqs]}
    return ('<h2>Pertanyaan yang Sering Diajukan</h2>' + items
            + '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>')


def legal(umroh=True):
    izin = ('<b>Izin Umrah SK Kemenag No. 63 Tahun 2020</b> dan <b>Izin Haji Plus (PIHK) SK Kemenag No. 846 Tahun 2020</b>'
            if umroh else '<b>Penyelenggara Ibadah Haji Khusus (PIHK) resmi, SK Kemenag No. 846 Tahun 2020</b>')
    return (f'<div class="ea-box">Elharamain Wisata (PT Dhiyaa El Haramain El Mubarakah) terdaftar resmi: {izin}. '
            f'Legalitas penyelenggara dapat dicek di situs <a href="{KEMENAG}" target="_blank" rel="noopener">Kementerian Agama RI</a>. '
            'Konsultasi langsung tersedia di <a href="/lokasi-kantor/">6 kantor kami</a> (Bekasi, Jakarta, Depok, '
            'Tangerang, Bandung, Bogor).</div>')


def cta(label, text):
    return f'<div class="ea-cta"><a href="{wa(text)}" target="_blank" rel="noopener">{e(label)}</a></div>'


def toc(heads):
    return '<div class="ea-toc"><b>Daftar isi</b>' + ol(heads) + '</div>'


def related(links):
    if not links:
        return ''
    return '<div class="ea-rel"><b>Baca juga:</b>' + ul(f'<a href="{u}">{e(t)}</a>' for u, t in links) + '</div>'


def fasilitas_ul():
    return ul(FASILITAS)


def belum_ul():
    return ul(BELUM)


def dokumen_ul():
    return ul(DOKUMEN)


def batal_table():
    return table(['Waktu pembatalan', 'Biaya pembatalan'], BATAL)


def perlengkapan(g):
    return ol(PERLENGKAPAN_PRIA if g == 'pria' else PERLENGKAPAN_WANITA)


def oleh_ul():
    return ul(OLEH)


def pembimbing_ul(n=12):
    return ul(PEMBIMBING[:n])


REKENING_TXT = REKENING
