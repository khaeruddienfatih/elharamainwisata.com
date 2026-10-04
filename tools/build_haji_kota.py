"""Bangun isi halaman 'Paket Haji Plus <Kota>' untuk haji.biz dari data kantor nyata.

Sumber fakta: halaman 'Lokasi Kantor' haji.biz (alamat, WA) dan artikel haji.biz yang sudah terbit
(harga 4 paket, setoran awal 4.000 USD, SK Kemenag 846/2020). Tidak ada klaim masa tunggu dalam tahun:
ditautkan ke artikel estimasi keberangkatan agar angkanya satu sumber.

Output: build/haji-biz/kota/<slug>.html (isi post) dan build/haji-biz/kota/preview.html (semua kota).
Pakai: python3 tools/build_haji_kota.py
"""
import os, urllib.parse, html

OUT = os.path.join(os.path.dirname(__file__), '..', 'build', 'haji-biz', 'kota')

# id = ID post di haji.biz (WordPress.com blog 257739192)
KOTA = [
    dict(id=331, slug='paket-haji-plus-bekasi', kota='Bekasi', kantor='Kantor Pusat Bekasi',
         alamat='Ruko Emerald No.5 Blok EB 1, Jl. Harapan Indah Raya, Kec. Medan Satria, Kota Bekasi, Jawa Barat 17132',
         wa='6281287292422', tel='0812-8729-2422',
         area=['Kota Bekasi', 'Harapan Indah', 'Bekasi Utara', 'Cikarang', 'Tambun']),
    dict(id=336, slug='paket-haji-plus-depok', kota='Depok', kantor='Kantor Depok',
         alamat='Jl. Margonda No.252 D, Kemiri Muka, Kec. Beji, Kota Depok, Jawa Barat',
         wa='6285179988198', tel='0851-7998-8198',
         area=['Margonda', 'Beji', 'Pancoran Mas', 'Sawangan', 'Cinere']),
    dict(id=342, slug='paket-haji-plus-tangerang', kota='Tangerang', kantor='Kantor Tangerang (BSD)',
         alamat='Ruko Ps. Modern No.18 BSD, Rw. Mekar Jaya, Kec. Serpong, Kota Tangerang Selatan, Banten 15318',
         wa='6285693883208', tel='0856-9388-3208',
         area=['BSD', 'Serpong', 'Pamulang', 'Ciputat', 'Kota Tangerang']),
    dict(id=347, slug='paket-haji-plus-bandung', kota='Bandung', kantor='Kantor Bandung',
         alamat='Jl. Bulevar Utama Blok RC No.18, Ruby Commercial, Summarecon Bandung, Kota Bandung, Jawa Barat',
         wa='628132212344', tel='0813-2212-344',  # dikonfirmasi pemilik 4 Okt 2026
         area=['Summarecon Bandung', 'Gedebage', 'Kota Bandung', 'Cimahi', 'Bandung Raya']),
    dict(id=297, slug='paket-haji-plus-jakarta', kota='Jakarta', kantor='Kantor Jakarta (Tebet)',
         alamat='Jl. Tebet Raya No.39 B, Tebet Timur, Kec. Tebet, Kota Jakarta Selatan, DKI Jakarta 12820',
         wa='6281214178056', tel='0812-1417-8056',
         area=['Tebet', 'Jakarta Selatan', 'Jakarta Timur', 'Jakarta Pusat', 'Jakarta Barat']),
    dict(id=763, slug='paket-haji-plus-bogor', kota='Bogor', kantor='Kantor Bogor',
         alamat='Ruko Graha Boulevard, Jl. Summarecon Bogor GBVD No.10, Sukatani, Kec. Sukaraja, Kab. Bogor, Jawa Barat 16144',
         wa='6282260126394', tel='0822-6012-6394',
         area=['Sukaraja', 'Cibinong', 'Kota Bogor', 'Kabupaten Bogor', 'Sentul']),
]

PAKET = [
    ('Silver', '12.000 USD', 'Hotel Makkah Anjum, maktab 116',
     'https://haji.biz/paket-haji-plus-silver-1448h/'),
    ('Gold', '15.500 USD', 'Marwa Rotana, depan Masjidil Haram',
     'https://haji.biz/paket-haji-plus-gold-1448h/'),
    ('Gold Arbain', '17.000 USD', 'Gold plus program 40 waktu shalat di Masjid Nabawi',
     'https://haji.biz/program-arbain-haji-plus/'),
    ('Platinum', '20.000 USD', 'Fairmont Makkah, maktab 111',
     'https://haji.biz/paket-haji-plus-platinum-1448h/'),
]

CSS = """.ehk{--b:#004AAD;--n:#0a2e6b;--g:#DBC033;font-family:Poppins,sans-serif;color:#26364d;line-height:1.75}
.ehk h2{font-size:24px;color:var(--n);margin:34px 0 12px;font-weight:700}
.ehk .ans{background:#f5f8fd;border-left:4px solid var(--b);border-radius:10px;padding:18px 20px;margin:0 0 24px}
.ehk .toc{background:#fff;border:1px solid #e1e8f3;border-radius:12px;padding:16px 20px;margin:0 0 26px}
.ehk .toc b{display:block;margin-bottom:6px;color:var(--n)}.ehk .toc ul{margin:0;padding-left:20px}
.ehk .kantor{background:#fff;border:1px solid #e1e8f3;border-radius:14px;padding:20px;box-shadow:0 8px 24px rgba(0,74,173,.06)}
.ehk .kantor h3{margin:0 0 6px;font-size:18px;color:var(--n)}
.ehk .btn{display:inline-block;padding:10px 16px;border-radius:10px;font-weight:600;font-size:14px;text-decoration:none;margin:8px 8px 0 0}
.ehk .wa{background:#25D366;color:#fff!important}.ehk .mp{background:#eef4fc;color:var(--b)!important}
.ehk table{width:100%;border-collapse:collapse;margin:10px 0}
.ehk th,.ehk td{border:1px solid #e1e8f3;padding:10px 12px;text-align:left;font-size:15px}
.ehk th{background:#f5f8fd;color:var(--n)}
.ehk .cta{background:#fffbe6;border:1px solid #f0e3a0;border-radius:14px;padding:22px;text-align:center;margin:30px 0}
.ehk details{border:1px solid #e1e8f3;border-radius:10px;padding:12px 16px;margin:10px 0}
.ehk summary{cursor:pointer;font-weight:600}
.ehk .legal{font-size:14px;color:#5a6b85;border-top:1px solid #e1e8f3;margin-top:28px;padding-top:12px}"""


def wa_link(c, teks):
    return 'https://wa.me/%s?text=%s' % (c['wa'], urllib.parse.quote(teks))


def maps_link(c):
    q = 'Elharamain Wisata ' + c['alamat']
    return 'https://www.google.com/maps/search/?api=1&query=' + urllib.parse.quote(q)


def build(c):
    k = c['kota']
    esc = html.escape
    area = ', '.join(c['area'])
    wa1 = wa_link(c, "Assalamu'alaikum Elharamain Wisata %s, saya mau konsultasi Haji Plus." % k)
    rows = ''.join('<tr><td><a href="%s">Paket %s</a></td><td>mulai %s</td><td>%s</td></tr>' % (u, n, h, d)
                   for n, h, d, u in PAKET)
    faq = [
        ('Di mana alamat kantor Elharamain Wisata di %s?' % k, c['alamat'] + '.'),
        ('Apakah saya harus ber-KTP %s untuk mendaftar?' % k,
         'Tidak. Pendaftaran Haji Plus bisa dilakukan dari kota mana saja, secara online maupun datang ke kantor kami. '
         'Kantor %s hanya memudahkan konsultasi tatap muka bagi jamaah di %s dan sekitarnya.' % (k, area)),
        ('Berapa setoran awal Haji Plus?',
         'Setoran awal 4.000 USD per jamaah, sama untuk semua paket dan semua kantor. Pembayaran hanya ke rekening resmi '
         'PT Dhiyaa El Haramain El Mubarakah.'),
        ('Apakah harga paket di %s berbeda dengan kota lain?' % k,
         'Tidak. Harga paket sama di semua kantor Elharamain Wisata.'),
        ('Kapan perkiraan keberangkatan saya?',
         'Estimasi keberangkatan bergantung pada antrean dan kebijakan pemerintah. Lihat penjelasan terbarunya di artikel '
         '<a href="https://haji.biz/estimasi-keberangkatan-haji-plus/">Estimasi Keberangkatan Haji Plus</a>.'),
        ('Dokumen apa yang perlu disiapkan?',
         'KTP, Kartu Keluarga, pas foto 4x6, buku nikah (bagi suami-istri), dan akte lahir.'),
    ]
    faq_html = ''.join('<details><summary>%s</summary><div>%s</div></details>' % (esc(q), a) for q, a in faq)
    return f"""<!-- wp:html -->
<style>{CSS}</style>
<div class="ehk">
<div class="ans"><b>Ringkasan:</b> Paket Haji Plus {k} dari Elharamain Wisata tersedia mulai 12.000 USD dengan setoran awal 4.000 USD. Elharamain Wisata adalah PIHK resmi Kemenag RI (SK No. 846 Tahun 2020) dan melayani konsultasi tatap muka di {esc(c['kantor'])}. Daftar bisa dari mana saja, termasuk online.</div>
<p>Bagi calon jamaah di {area}, bisa berkonsultasi langsung dengan petugas yang paham proses pendaftaran Haji Plus adalah nilai penting. Elharamain Wisata melayani konsultasi paket, pendaftaran, dan pendampingan dokumen untuk jamaah dari {k} dan sekitarnya.</p>
<div class="toc"><b>Daftar isi</b><ul>
<li><a href="#kantor-{k.lower()}">Kantor Haji Plus di {k}</a></li>
<li><a href="#paket-{k.lower()}">Pilihan paket dan harga</a></li>
<li><a href="#daftar-{k.lower()}">Langkah mendaftar dari {k}</a></li>
<li><a href="#faq-{k.lower()}">Pertanyaan umum</a></li></ul></div>
<h2 id="kantor-{k.lower()}">Kantor Haji Plus Elharamain Wisata di {k}</h2>
<div class="kantor"><h3>{esc(c['kantor'])}</h3><div>{esc(c['alamat'])}</div><div>Telepon / WhatsApp: {c['tel']}</div>
<a class="btn wa" href="{wa1}" target="_blank" rel="noopener">Konsultasi via WhatsApp</a><a class="btn mp" href="{maps_link(c)}" target="_blank" rel="noopener">Lihat peta</a></div>
<p>Kantor ini melayani jamaah dari {area}. Tidak bisa datang? Konsultasi dan pendaftaran juga bisa dilakukan secara online lewat WhatsApp.</p>
<h2 id="paket-{k.lower()}">Pilihan Paket Haji Plus untuk Jamaah {k}</h2>
<p>Jamaah dari {k} dapat memilih empat paket Haji Plus 1448 H. Harga di bawah adalah harga mulai untuk kamar berempat.</p>
<table><thead><tr><th>Paket</th><th>Harga</th><th>Keunggulan</th></tr></thead><tbody>{rows}</tbody></table>
<p>Bandingkan lengkap hotel, jarak, dan fasilitas di <a href="https://haji.biz/perbandingan-paket-haji-plus-silver-gold-platinum/">Perbandingan 4 Paket Haji Plus</a>. Ingin mencicil? Lihat <a href="https://haji.biz/cicilan-haji-plus-simulasi-angsuran-pembiayaan/">simulasi cicilan Haji Plus</a>.</p>
<h2 id="daftar-{k.lower()}">Langkah Mendaftar Haji Plus dari {k}</h2>
<ol>
<li>Konsultasi dengan {esc(c['kantor'])} atau lewat WhatsApp untuk memilih paket.</li>
<li>Siapkan dokumen: KTP, KK, pas foto 4x6, buku nikah (bagi suami-istri), dan akte lahir.</li>
<li>Bayar setoran awal 4.000 USD per jamaah, hanya ke rekening resmi PT Dhiyaa El Haramain El Mubarakah.</li>
<li>Nomor porsi diterbitkan dan tercatat resmi di sistem Kemenag.</li>
<li>Lunasi biaya paket 6 bulan sebelum jadwal keberangkatan.</li></ol>
<p>Pelajari dulu perbedaannya di <a href="https://haji.biz/perbedaan-haji-khusus-dan-reguler/">Perbedaan Haji Khusus dan Reguler</a> dan <a href="https://haji.biz/syarat-daftar-haji-khusus/">syarat daftar haji khusus</a>.</p>
<div class="cta"><b>Ingin konsultasi dari {k}?</b><br>Gratis, tanpa biaya apa pun.<br><a class="btn wa" href="{wa1}" target="_blank" rel="noopener">Chat WhatsApp {esc(c['kantor'])}</a></div>
<h2 id="faq-{k.lower()}">Pertanyaan Umum Haji Plus {k}</h2>
{faq_html}
<p class="legal">PT Dhiyaa El Haramain El Mubarakah, Penyelenggara Ibadah Haji Khusus (PIHK) resmi, SK Kemenag RI No. 846 Tahun 2020. Verifikasi di <a href="https://kemenag.go.id/" target="_blank" rel="noopener">kemenag.go.id</a>.</p>
</div>
<!-- /wp:html -->
"""


def main():
    os.makedirs(OUT, exist_ok=True)
    prev = ['<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>Preview halaman kota haji.biz</title><body style="margin:0;background:#eef2f8">']
    for c in KOTA:
        body = build(c)
        open(os.path.join(OUT, c['slug'] + '.html'), 'w').write(body)
        prev.append('<section style="max-width:900px;margin:24px auto;background:#fff;padding:24px;border-radius:12px"><h1 style="font-family:Poppins,sans-serif">Paket Haji Plus %s <small style="font-size:13px;color:#888">(post %d)</small></h1>%s</section>' % (c['kota'], c['id'], body))
    open(os.path.join(OUT, 'preview.html'), 'w').write(''.join(prev))
    print('ok', len(KOTA), 'halaman ->', os.path.abspath(OUT))


if __name__ == '__main__':
    main()
