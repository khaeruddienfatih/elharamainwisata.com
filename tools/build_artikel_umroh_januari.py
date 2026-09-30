"""Artikel "Umroh Januari 2027" untuk elharamain.id — sumber: brosur resmi data/brosur/paket-umroh-januari-2027.pdf
(update 10/09/2026) + data/paket-umroh.json. Gambar dari Cloudinary. Disimpan sebagai DRAFT.
Usage: python3 tools/build_artikel_umroh_januari.py [--save]"""
import html
import json
import os
import sys
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from deploy_uae import rest  # noqa: E402

CLD = 'https://res.cloudinary.com/v6gwkqrb/image/upload/'
WA = 'https://api.whatsapp.com/send?phone=6281287292422&text='
SLUG = 'umroh-januari-2027'
TITLE = 'Umroh Januari 2027: Jadwal, Harga & Pilihan Paket Musim Dingin'
DESC = ('Jadwal & harga umroh Januari 2027 Elharamain Wisata: 6 paket musim dingin Saudia Airlines, '
        'hotel bintang 5, Thaif + kereta cepat, mulai Rp 37,9 juta.')

PAKET = [p for p in json.load(open(os.path.join(ROOT, 'data', 'paket-umroh.json')))['paket'] if p['bulan'] == 'Januari']


def img(pid, alt, w=1200, h=None, cap=None):
    t = f'c_fill,g_auto,w_{w},h_{h},q_auto,f_auto' if h else f'c_limit,w_{w},q_auto,f_auto'
    fig = (f'<figure class="ea-fig"><img src="{CLD}{t}/{pid}.jpg" alt="{html.escape(alt)}" loading="lazy" '
           f'width="{w}"{f" height={chr(34)}{h}{chr(34)}" if h else ""}>')
    return fig + (f'<figcaption>{cap}</figcaption>' if cap else '') + '</figure>'


def rp(n):
    return 'Rp ' + f'{n:,}'.replace(',', '.')


def wa(text):
    return WA + urllib.parse.quote(text)


CSS = '''<style>
.ea{--b:#004AAD;--n:#0a2e6b;font-family:Poppins,sans-serif;color:#26364d;line-height:1.8;font-size:16.5px;max-width:820px;margin:0 auto}
.ea *{box-sizing:border-box}
.ea h2{font-family:Poppins,sans-serif!important;font-weight:700!important;color:var(--n);font-size:24px;line-height:1.3;margin:36px 0 12px}
.ea h3{font-family:Poppins,sans-serif!important;font-weight:700!important;color:var(--n);font-size:18.5px;margin:24px 0 8px}
.ea a{color:var(--b)}
.ea-fig{margin:20px 0}.ea-fig img{width:100%;height:auto;border-radius:14px;display:block}
.ea-fig figcaption{font-size:13px;color:#6b7a90;text-align:center;margin-top:6px}
.ea-box{background:#f5f8fd;border-left:4px solid var(--b);border-radius:10px;padding:16px 18px;margin:18px 0}
.ea-tw{overflow-x:auto;margin:14px 0;border:1px solid #e1e8f3;border-radius:12px}
.ea table{width:100%;border-collapse:collapse;font-size:14.5px;min-width:640px}
.ea th{background:var(--n);color:#fff;text-align:left;padding:10px 12px;font-weight:600}
.ea td{padding:10px 12px;border-top:1px solid #e1e8f3;vertical-align:top}
.ea tr:nth-child(even) td{background:#f8fafd}
.ea ul,.ea ol{padding-left:22px}.ea li{margin:5px 0}
.ea-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.ea-cta{text-align:center;margin:30px 0}
.ea-cta a{display:inline-block;background:#25D366;color:#fff!important;font-weight:700;padding:14px 26px;border-radius:12px;text-decoration:none}
.ea details{border:1px solid #e1e8f3;border-radius:10px;padding:12px 16px;margin:10px 0}
.ea summary{font-weight:600;color:var(--n);cursor:pointer}
@media(max-width:640px){.ea{font-size:15.5px}.ea h2{font-size:21px}.ea-grid{grid-template-columns:1fr}}
</style>'''


def body():
    rows = ''.join(
        f'<tr><td><b>{html.escape(p["label"])}</b></td><td>{p["hari"]} hari</td><td>{html.escape(p["berangkat"])}</td>'
        f'<td>{html.escape(p["makkah"])}</td><td>{html.escape(p["madinah"])}</td>'
        f'<td>{rp(p["q"])}</td><td>{rp(p["t"])}</td><td>{rp(p["d"])}</td></tr>' for p in PAKET)
    termurah = min(p['q'] for p in PAKET)
    termasuk = ['Tiket pesawat PP kelas ekonomi (Saudia Airlines)', 'Visa umroh', 'Asuransi perjalanan',
                'Perlengkapan umroh eksklusif', 'Manasik umroh di hotel berbintang', 'VIP Lounge Umroh Soekarno-Hatta',
                'Airport tax & handling bandara', 'Hotel sesuai paket', 'Makan fullboard 3x sehari di hotel',
                'Transportasi bus terbaru', 'Pembimbing & mutawwif berpengalaman', 'Program & city tour sesuai itinerary',
                'Kajian dan umroh dengan aplikasi Audio Hajj', 'Fasilitasi umroh sampai 3x', 'Free city tour Thaif',
                'Free ATV & naik unta di Madinah', 'Kuliner Nasi Mandhi + Kunafa', 'Bagasi 35 kg/jamaah',
                'Air zamzam 5 liter/jamaah', 'Album foto perjalanan', 'Sertifikat umroh', 'Gift Elharamain Wisata']
    belum = ['Paspor', 'Suntik meningitis & polio', 'Keperluan pribadi', 'Kelebihan bagasi',
             'Penyesuaian biaya bila ada kebijakan baru kedua negara (kesehatan, tiket, hotel, visa)']
    itin = [('Hari 1', 'Berkumpul di VIP Lounge Umroh Soekarno-Hatta, terbang ke Madinah, check-in hotel.'),
            ('Hari 2', 'Ziarah dalam: Raudhah, makam Nabi Muhammad ﷺ, Baqi, Tsaqifah Bani Saidah.'),
            ('Hari 3', 'Tahajjud bersama, kajian Islami, memperbanyak amalan sunnah di Masjid Nabawi.'),
            ('Hari 4', 'Ziarah kota Madinah: Masjid Quba, kebun kurma, Jabal Uhud, Masjid Qiblatain, Masjid Khandaq, Jabal Magnet; pemantapan manasik.'),
            ('Hari 5', 'Umroh pertama (miqat, thawaf, sai, tahallul); ke Makkah dengan kereta cepat, check-in hotel.'),
            ('Hari 6', 'Acara bebas: i\'tikaf dan amalan sunnah di Masjidil Haram.'),
            ('Hari 7', 'Ziarah kota Makkah: Jabal Tsur, Arafah, Muzdalifah, Mina, Jamarat; umroh kedua dengan miqat di Ji\'ranah.'),
            ('Hari 8', 'Tahajjud bersama dan ibadah di Masjidil Haram.'),
            ('Hari 9', 'Ziarah Thaif: Masjid Abdullah bin Abbas, penyulingan parfum & mawar, kuliner Nasi Mandi, bukit Al-Hada; umroh ketiga dengan miqat di Qarnul Manazil.'),
            ('Hari 10', 'Tahajjud bersama, thawaf sunnah dan ibadah di Masjidil Haram.'),
            ('Hari 11', 'Thawaf wada, Museum Wahyu, city tour Jeddah.'),
            ('Hari 12', 'Tiba di Jakarta; pembagian air zamzam dan oleh-oleh (album foto, sertifikat umroh, kurma, parfum).')]
    faq = [('Berapa biaya umroh Januari 2027 di Elharamain Wisata?',
            f'Mulai {rp(termurah)} per jamaah (Paket Bronze 9 hari, sekamar ber-empat) hingga {rp(61000000)} '
            '(Premium sekamar ber-dua atau Gold 12 hari sekamar ber-dua).'),
           ('Kapan jadwal keberangkatan umroh Januari 2027?',
            'Tanggal 3, 4, 9, 11, 13, 14, 17, 18, 20, 24, 25, dan 31 Januari 2027, tergantung paket yang dipilih.'),
           ('Berapa DP dan kapan pelunasan?',
            'DP Rp 6.000.000 per jamaah saat pendaftaran; pelunasan paling lambat 35 hari sebelum keberangkatan.'),
           ('Dokumen apa saja yang disiapkan?',
            'Paspor RI berlaku minimal 10 bulan (minimal 2 suku kata), pas foto 4x6, fotokopi KTP & KK, '
            'fotokopi buku nikah (suami-istri), sertifikat vaksin, dan BPJS.')]
    return f'''{CSS}<div class="ea">
<p>Januari termasuk salah satu waktu favorit untuk berumroh: musim dingin di Arab Saudi membuat ibadah di Makkah dan Madinah terasa lebih nyaman. Untuk <b>umroh Januari 2027</b>, Elharamain Wisata membuka <b>6 pilihan paket musim dingin</b> dengan maskapai <b>Saudia Airlines</b>, hotel bintang 5, program Thaif, dan perjalanan Makkah–Madinah dengan kereta cepat. Harga mulai <b>{rp(termurah)}</b>.</p>
{img('12', 'Umroh Januari 2027 bersama Elharamain Wisata di Tanah Suci', 1200, 675)}
<p>Seluruh jadwal dan harga di artikel ini diambil dari brosur resmi Elharamain Wisata <i>Paket Umroh Musim Dingin High Season Januari 2027</i> (update 10 September 2026).</p>

<h2>Jadwal & Harga Paket Umroh Januari 2027</h2>
<p>Harga per jamaah, sekamar ber-empat / ber-tiga / ber-dua. Semua hotel bintang 5 (atau setaraf). Detail program bisa dilihat juga di halaman <a href="/paket-umroh-silver/">Paket Umroh Silver</a> dan <a href="/paket-umroh-platinum/">Paket Umroh Platinum</a>.</p>
<div class="ea-tw"><table><thead><tr><th>Paket</th><th>Durasi</th><th>Keberangkatan</th><th>Hotel Makkah</th><th>Hotel Madinah</th><th>Ber-4</th><th>Ber-3</th><th>Ber-2</th></tr></thead><tbody>{rows}</tbody></table></div>
<div class="ea-box"><b>Rute penerbangan:</b> Bronze in Jeddah – out Jeddah; Silver 3, 4 & 31 Jan Madinah–Jeddah (25 Jan Jeddah–Madinah); Platinum, Premium, Silver 12 Hari & Gold 12 Hari in Madinah – out Jeddah.</div>
<div class="ea-grid">{img('1._Desain_3_Paket_Umroh_Januari_Musim_Dingin_By_Saudia_Airlines_Elharamain_Wisata_2027', 'Brosur paket umroh Januari 2027 Saudia Airlines Elharamain Wisata', 600, None)}{img('12_hari_januari_1', 'Brosur paket umroh 12 hari Januari 2027 Elharamain Wisata', 600, None)}</div>

<h2>Bonus di Paket Platinum, Premium & 12 Hari</h2>
<ul><li><b>Platinum & Premium:</b> H-1 free menginap di Hotel 101, free Jabal Khandama + golf car sai, free abaya & jaket eksklusif, free GMC tour night Jabal Uhud.</li>
<li><b>Silver 12 Hari & Gold 12 Hari:</b> free GMC tour night Jabal Uhud.</li></ul>

<h2>Hotel Bintang 5 Dekat Masjid</h2>
<ul><li><b>Anjum Hotel</b> (Makkah) — ±350 meter dari Masjidil Haram.</li>
<li><b>Marwa Rotana</b> & <b>Fairmont</b> (Makkah) — di pelataran Zamzam Tower.</li>
<li><b>Movenpick</b> & <b>Al-Aqeeq Hotel</b> (Madinah) — ±50 meter dari Masjid Nabawi.</li></ul>

<h2>Contoh Itinerary Umroh 12 Hari (In Madinah – Out Jeddah)</h2>
<ol>{''.join(f'<li><b>{d}:</b> {t}</li>' for d, t in itin)}</ol>
<p>Program 9 hari mengikuti pola yang sama dengan waktu lebih ringkas. Susunan acara dapat menyesuaikan kondisi terbaru.</p>

<h2>Fasilitas yang Termasuk</h2>
<ul>{''.join(f'<li>{x}</li>' for x in termasuk)}</ul>
<h3>Belum termasuk</h3>
<ul>{''.join(f'<li>{x}</li>' for x in belum)}</ul>

<h2>Perlengkapan Umroh Eksklusif</h2>
<p>Jamaah mendapat perlengkapan lengkap, antara lain koper bagasi 24 inci & kabin 18 inci, batik Elharamain, ihram eksklusif (pria) atau set mukena & scarf (wanita), knitwear untuk musim dingin, sajadah traveling, payung lipat, buku panduan umroh & buku doa, hingga travel organizer bag. Paket Platinum & Premium mendapat tambahan abaya & jaket.</p>
<div class="ea-grid">{img('perlengkapan-pria-2026', 'Perlengkapan umroh eksklusif Elharamain Wisata untuk jamaah pria', 600, 338)}{img('perlengkapan-wanita-2026-a', 'Perlengkapan umroh eksklusif Elharamain Wisata untuk jamaah wanita', 600, 338)}</div>

<h2>Dibimbing Asatidz Lulusan Timur Tengah</h2>
<p>Ibadah dibimbing secara intensif dan sesuai sunnah oleh para pembimbing, di antaranya Ustadz Dr. Muhammad Tahir Lc MA, Ustadz Dr. Abdul Kadir Abu Lc MA, Ustadz Ahmad Shobirin Lc MA, Ustadz Didi Wibawa Lc MA, dan Ustadz Furqon Abdurrohman Lc MA.</p>

<h2>Syarat & Cara Daftar</h2>
<ul><li>DP <b>Rp 6.000.000/jamaah</b>; pelunasan 35 hari sebelum keberangkatan.</li>
<li>Dokumen: paspor RI berlaku minimal 10 bulan (minimal 2 suku kata), pas foto 4x6, fotokopi KTP & KK, fotokopi buku nikah (suami-istri), sertifikat vaksin, BPJS.</li>
<li>Pembayaran hanya sah ke rekening a.n. <b>PT Dhiyaa El Haramain El Mubarakah</b>: Bank Mandiri 156.001.150.115.4 atau Bank BSI 710.857.755.4.</li>
<li>Kamar ber-empat (quad) wajib memiliki teman sekamar; bila tidak, jamaah melakukan upgrade kamar.</li></ul>
<div class="ea-box">Elharamain Wisata adalah penyelenggara resmi: <b>Izin Umrah SK Kemenag No. 63 Tahun 2020</b> dan <b>Izin Haji Plus SK Kemenag No. 846 Tahun 2020</b> — izin travel umroh dapat dicek di situs resmi <a href="https://kemenag.go.id/" target="_blank" rel="noopener">Kementerian Agama RI</a>. Konsultasi langsung bisa di <a href="/lokasi-kantor/">6 kantor kami</a> (Bekasi, Jakarta, Depok, Tangerang, Bandung, Bogor).</div>
<div class="ea-cta"><a href="{wa("Assalamu'alaikum Elharamain Wisata, saya mau info paket umroh Januari 2027.")}" target="_blank" rel="noopener">Tanya Paket Umroh Januari 2027 via WhatsApp</a></div>

<h2>Pertanyaan yang Sering Diajukan</h2>
{''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faq)}
<p style="font-size:13.5px;color:#6b7a90">Harga & jadwal dapat berubah mengikuti kebijakan Arab Saudi, maskapai, dan kurs (asumsi kurs maksimal Rp 17.000), sesuai ketentuan brosur.</p>
</div>'''


def save():
    content = f'<!-- wp:html -->\n{body()}\n<!-- /wp:html -->'
    cats = rest('elharamainid', 'GET', '/wp/v2/categories?per_page=100&_fields=id,name,slug')
    cat = [c['id'] for c in cats if 'umroh' in c['slug'].lower()][:1]
    data = {'title': TITLE, 'slug': SLUG, 'status': 'draft', 'content': content, 'excerpt': DESC}
    if cat:
        data['categories'] = cat
    found = rest('elharamainid', 'GET', f'/wp/v2/posts?slug={SLUG}&status=draft,publish&_fields=id')
    path = f'/wp/v2/posts/{found[0]["id"]}' if found else '/wp/v2/posts'
    r = rest('elharamainid', 'POST', path + '?_fields=id,status,link', data)
    print('artikel:', r, '| kategori:', [c['name'] for c in cats if c['id'] in cat])
    return r['id']


if __name__ == '__main__':
    os.makedirs(os.path.join(ROOT, 'build'), exist_ok=True)
    p = os.path.join(ROOT, 'build', 'artikel-umroh-januari-2027.html')
    open(p, 'w').write('<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width">'
                       f'<h1 style="font-family:Poppins;max-width:820px;margin:30px auto 10px">{TITLE}</h1>' + body())
    print('preview', os.path.relpath(p, ROOT))
    if '--save' in sys.argv:
        save()
