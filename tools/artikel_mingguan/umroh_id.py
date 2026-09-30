"""35 artikel umroh untuk elharamain.id (fakta hanya dari brosur resmi, lihat data.py)."""
from data import HOTEL, ITIN_9, ITIN_12, ITIN_RIYADH, PAKET, PEMBIMBING, REKENING
from render import (batal_table, belum_ul, dokumen_ul, e, fasilitas_ul, fig, hotel_line, oleh_ul, ol, paket,
                    paket_list, pembimbing_ul, perlengkapan, rp, table, ul)

CAT_UMROH, CAT_PAKET = 1, 12
H = lambda n: str(n)  # noqa: E731  foto dokumentasi folder Cloudinary Elharamainwisata/Header
LIBURAN = '1._Desain_Paket_Umroh_Liburan_Akhir_Tahun_Musim_Dingin_By_Saudia_Airlines_Elharamain_Wisata_2026'
JAN = '1._Desain_3_Paket_Umroh_Januari_Musim_Dingin_By_Saudia_Airlines_Elharamain_Wisata_2027'
F = lambda n: 'fasilitas-' + n  # noqa: E731

def minq(fn):
    return rp(min(p['q'] for p in PAKET if fn(p)))

A = []


def art(**k):
    k.setdefault('site', 'elharamainid')
    k.setdefault('cat', CAT_UMROH)
    A.append(k)


# 1
art(slug='perbandingan-paket-umroh-bronze-silver-platinum', kw='perbandingan paket umroh',
    title='Perbandingan Paket Umroh Bronze, Silver, Platinum & Premium: Mana yang Cocok?',
    seo_title='Perbandingan Paket Umroh Bronze, Silver, Platinum & Premium',
    desc='Perbandingan paket umroh Elharamain Wisata: beda hotel, harga, bonus, dan rute Bronze, Silver, Platinum, Premium & Gold untuk musim dingin 2026/2027.',
    cat=CAT_PAKET, cover=H(3),
    intro='Bingung memilih kelas paket? <b>Perbandingan paket umroh</b> ini merangkum perbedaan Bronze, Silver, Platinum, Premium, dan Gold di Elharamain Wisata berdasarkan brosur resmi musim dingin November 2026 – Januari 2027.',
    body=f'''<h2>Perbedaan Utama Tiap Kelas</h2>
<p>Semua kelas memakai hotel bintang 5 dan program yang sama (Thaif, kereta cepat, fasilitasi umroh sampai 3x). Pembedanya ada pada <b>lokasi hotel</b>, <b>rute penerbangan</b>, dan <b>bonus</b>.</p>
{table(['Kelas', 'Hotel Makkah', 'Hotel Madinah', 'Ciri khas'], [
 ['<b>Bronze</b>', 'Anjum / Prestige', 'Peninsula Worth / Al-Aqeeq', 'Harga paling terjangkau; umumnya in Jeddah – out Jeddah'],
 ['<b>Silver</b>', 'Anjum', 'Al-Aqeeq / Peninsula Worth', 'Pilihan Makkah First atau Madinah First; tersedia 12 hari'],
 ['<b>Platinum</b>', 'Marwa Rotana / Movenpick', 'Al-Aqeeq / Al-Haram / Movenpick', 'Hotel Makkah di pelataran Zamzam Tower + bonus'],
 ['<b>Premium</b>', 'Fairmont', 'Movenpick', 'Kelas tertinggi Januari 2027 + bonus'],
 ['<b>Gold 12 Hari</b>', 'Marwa Rotana / Movenpick', 'Al-Aqeeq', 'Program 12 hari dengan hotel Makkah kelas Platinum']])}
<h2>Kisaran Harga per Kelas</h2>
<p>Harga terendah (sekamar ber-empat) per kelas di seluruh jadwal musim dingin:</p>
{ul([f"Bronze: mulai {minq(lambda p: p['tier'] == 'bronze')}", f"Silver: mulai {minq(lambda p: p['tier'] == 'silver')}",
     f"Platinum: mulai {minq(lambda p: p['tier'] == 'platinum')}", f"Gold 12 Hari: mulai {minq(lambda p: p['tier'] == 'gold')}",
     f"Premium: mulai {minq(lambda p: p['tier'] == 'premium')}"])}
<h2>Bonus yang Membedakan Platinum & Premium</h2>
<p>Paket Platinum dan Premium mendapat tambahan seperti gratis menginap di Hotel 101 pada H-1, golf car untuk sai, wahana Toboggan atau Jabal Khandama (tergantung jadwal), serta abaya/outer & jaket eksklusif. Paket 12 hari mendapat GMC tour malam Jabal Uhud.</p>
<h2>Cara Memilih</h2>
{ul(['Prioritas jarak ke Masjidil Haram → pilih Platinum/Premium (hotel di pelataran Zamzam Tower).',
     'Ingin waktu ibadah lebih lama → pilih program 12 hari (Silver 12 Hari atau Gold 12 Hari).',
     'Anggaran efisien tetap bintang 5 → Bronze atau Silver.'])}''',
    faqs=[('Apa beda paket umroh Silver dan Platinum?', 'Silver memakai Anjum Hotel (±350 m dari Masjidil Haram), sedangkan Platinum memakai Marwa Rotana/Movenpick yang berada di pelataran Zamzam Tower, ditambah bonus seperti menginap H-1 dan jaket eksklusif.'),
          ('Apakah semua paket memakai hotel bintang 5?', 'Ya. Menurut brosur, seluruh paket musim dingin Elharamain Wisata memakai hotel bintang 5 atau setaraf.'),
          ('Paket apa yang paling murah?', f"Paket Bronze Desember 2026 (9 hari) mulai {rp(36500000)} per jamaah sekamar ber-empat.")],
    cta=('Konsultasi Pilih Paket via WhatsApp', "Assalamu'alaikum, saya mau konsultasi memilih kelas paket umroh."),
    rel=['umroh-januari-2027'])

# 2
art(slug='umroh-riyadh-air-november-2026', kw='umroh riyadh air',
    title='Umroh Riyadh Air November 2026: Jadwal, Harga & Itinerary 10 Hari',
    seo_title='Umroh Riyadh Air November 2026: Harga & Itinerary',
    desc='Umroh Riyadh Air bersama Elharamain Wisata: berangkat 26 November 2026, program 10 hari + Thaif + kereta cepat, hotel bintang 5, mulai Rp 37 juta.',
    cat=CAT_PAKET, cover='10_Hari_Riyad_Air_1',
    intro='Ingin mencoba maskapai baru Arab Saudi? Program <b>umroh Riyadh Air</b> Elharamain Wisata berangkat <b>26 November 2026</b> dalam paket Musim Sejuk 10 hari, dengan harga mulai Rp 37.000.000.',
    body=f'''<h2>Harga Paket Umroh Riyadh Air</h2>
{paket(lambda p: p['maskapai'] == 'Riyadh Air', cols=('label', 'hari', 'berangkat', 'makkah', 'madinah', 'q', 't', 'd'))}
{fig('10_Hari_Riyad_Air_2', 'Brosur umroh Riyadh Air November 2026 Elharamain Wisata', 600)}
<h2>Rute Penerbangan</h2>
<p>Menurut itinerary brosur, keberangkatan melalui rute <b>Jakarta – Riyadh – Jeddah</b> dan kepulangan <b>Jeddah – Riyadh – Jakarta</b>. Brosur mencantumkan jadwal terbang dari Jeddah pukul 17.20 waktu setempat pada hari terakhir.</p>
<h2>Itinerary Umroh Riyadh Air</h2>
{ol(ITIN_RIYADH)}
<p>Hotel yang disiapkan: Prestige atau Anjum di Makkah dan Peninsula atau Al-Aqeeq di Madinah (atau setaraf).</p>''',
    faqs=[('Kapan umroh Riyadh Air Elharamain berangkat?', 'Tanggal 26 November 2026, program Musim Sejuk 10 hari.'),
          ('Berapa harga umroh Riyadh Air?', 'Rp 37.000.000 (ber-empat), Rp 40.000.000 (ber-tiga), dan Rp 43.000.000 (ber-dua) per jamaah.'),
          ('Apakah penerbangan Riyadh Air transit?', 'Sesuai itinerary brosur, rutenya Jakarta–Riyadh–Jeddah saat berangkat dan Jeddah–Riyadh–Jakarta saat pulang.')],
    cta=('Tanya Umroh Riyadh Air', "Assalamu'alaikum, saya mau info umroh Riyadh Air 26 November 2026."), rel=[])

# 3
art(slug='umroh-akhir-tahun-2026', kw='umroh akhir tahun 2026',
    title='Umroh Akhir Tahun 2026: Paket Eksklusif Liburan 21–27 Desember',
    seo_title='Umroh Akhir Tahun 2026: Paket Eksklusif Liburan',
    desc='Umroh akhir tahun 2026 bersama Elharamain Wisata: paket eksklusif Saudia 9 & 12 hari berangkat 21–27 Desember, Thaif + 2x kereta cepat, mulai Rp 47 juta.',
    cat=CAT_PAKET, cover=LIBURAN,
    intro='Libur sekolah dan cuti akhir tahun jadi momen pas untuk ibadah bersama keluarga. Program <b>umroh akhir tahun 2026</b> Elharamain Wisata berangkat 21, 22, 23, 26, dan 27 Desember dengan Saudia Airlines (Jeddah–Jeddah).',
    body=f'''<h2>Pilihan Paket Umroh Akhir Tahun</h2>
{paket(lambda p: p['label'].startswith('Eksklusif'), cols=('label', 'hari', 'berangkat', 'makkah', 'madinah', 'q', 't', 'd'))}
{fig('2._Desain_Paket_Umroh_Liburan_Akhir_Tahun_Musim_Dingin_By_Saudia_Airlines_Elharamain_Wisata_2026', 'Brosur umroh akhir tahun 2026 Elharamain Wisata', 600)}
<h2>Keistimewaan Program Liburan Akhir Tahun</h2>
{ul(['Ziarah Thaif dan <b>2x naik kereta cepat</b> Haramain.', 'GMC tour malam Jabal Uhud (tercantum di itinerary hari ke-2).',
     'Platinum: gratis menginap H-1 di Hotel 101, wahana Toboggan + golf car sai, outer & jaket eksklusif.',
     'Hotel Madinah Al-Aqeeq (±50 m dari Masjid Nabawi) untuk semua kelas; Platinum juga bisa Al-Haram.'])}
<h2>Kapan Harus Mendaftar?</h2>
<p>Pelunasan dilakukan 35 hari sebelum keberangkatan, sehingga untuk jadwal 21 Desember pelunasan jatuh sekitar pertengahan November. Kursi liburan akhir tahun biasanya cepat penuh, jadi amankan dengan DP Rp 6.000.000 lebih awal.</p>''',
    faqs=[('Tanggal berapa saja umroh akhir tahun 2026?', 'Paket 9 hari berangkat 21, 22, dan 26 Desember; paket 12 hari berangkat 23 dan 27 Desember 2026.'),
          ('Berapa harga umroh akhir tahun?', 'Mulai Rp 47.000.000 (Eksklusif Silver 9 hari, ber-empat) hingga Rp 75.000.000 (Gold 12 hari, ber-dua).'),
          ('Maskapai apa yang dipakai?', 'Saudia Airlines dengan rute Jeddah–Jeddah.')],
    cta=('Daftar Umroh Akhir Tahun', "Assalamu'alaikum, saya mau daftar umroh akhir tahun 2026."), rel=['perbandingan-paket-umroh-bronze-silver-platinum'])

# 4
art(slug='syarat-umroh-dokumen', kw='syarat umroh',
    title='Syarat Umroh 2026: Dokumen yang Wajib Disiapkan Jamaah',
    seo_title='Syarat Umroh 2026: Daftar Dokumen Wajib',
    desc='Syarat umroh 2026 di Elharamain Wisata: paspor minimal 10 bulan, nama 2 suku kata, pas foto 4x6, KTP, KK, buku nikah, sertifikat vaksin & BPJS.',
    cover=H(5),
    intro='Sebelum membayar DP, pastikan dokumen Anda lengkap. Berikut <b>syarat umroh</b> yang diminta Elharamain Wisata untuk keberangkatan musim dingin 2026/2027.',
    body=f'''<h2>Daftar Dokumen Syarat Umroh</h2>
{dokumen_ul()}
<h2>Catatan Penting Soal Paspor</h2>
<p>Paspor harus <b>berlaku minimal 10 bulan</b> dan nama di paspor minimal <b>2 suku kata</b>. Jika nama Anda hanya satu kata, urus penambahan nama di kantor imigrasi sebelum mendaftar. Biaya pembuatan paspor tidak termasuk dalam harga paket.</p>
<h2>Yang Belum Termasuk Biaya Paket</h2>
{belum_ul()}
<h2>Setelah Dokumen Siap</h2>
<p>Pendaftaran disertai DP Rp 6.000.000 per jamaah, lalu pelunasan 35 hari sebelum keberangkatan. Dokumen bisa dikirim ke kantor terdekat atau dikonsultasikan lewat WhatsApp.</p>''',
    faqs=[('Berapa lama masa berlaku paspor untuk umroh?', 'Minimal 10 bulan sesuai ketentuan brosur Elharamain Wisata.'),
          ('Apakah suami-istri perlu buku nikah?', 'Ya, fotokopi buku nikah diperlukan bagi jamaah suami-istri.'),
          ('Apakah suntik meningitis termasuk paket?', 'Belum. Suntik meningitis & polio termasuk biaya di luar paket.')],
    cta=('Cek Kelengkapan Dokumen', "Assalamu'alaikum, saya mau cek syarat dokumen umroh."), rel=[])

# 5
art(slug='cara-daftar-umroh-dp-6-juta', kw='cara daftar umroh',
    title='Cara Daftar Umroh di Elharamain Wisata: DP Rp 6 Juta, Pelunasan & Rekening Resmi',
    seo_title='Cara Daftar Umroh: DP Rp 6 Juta & Alur Pembayaran',
    desc='Cara daftar umroh di Elharamain Wisata: pilih jadwal, bayar DP Rp 6 juta ke rekening resmi PT Dhiyaa El Haramain El Mubarakah, lunasi 35 hari sebelum berangkat.',
    cover=H(6),
    intro='Mendaftar umroh tidak rumit asal urutannya jelas. Inilah <b>cara daftar umroh</b> di Elharamain Wisata, dari memilih jadwal hingga pelunasan.',
    body=f'''<h2>Langkah Pendaftaran</h2>
{ol(['Pilih paket dan tanggal keberangkatan (November 2026 – Januari 2027).', 'Siapkan dokumen: paspor, pas foto 4x6, KTP, KK, buku nikah (suami-istri), sertifikat vaksin, BPJS.',
     'Bayar <b>DP Rp 6.000.000 per jamaah</b> untuk mengamankan kursi.', 'Lunasi biaya paket paling lambat <b>35 hari sebelum keberangkatan</b>.',
     'Ikuti manasik umroh di hotel berbintang sebelum berangkat.'])}
<h2>Rekening Resmi</h2>
<div class="ea-box">Pembayaran hanya sah jika ditransfer ke rekening a.n. <b>PT Dhiyaa El Haramain El Mubarakah</b>: {REKENING.split(' a.n.')[0]}. Pembayaran ke rekening lain tidak dianggap sah.</div>
<h2>Ketentuan yang Perlu Diketahui</h2>
{ul(['Harga dapat menyesuaikan bila ada kebijakan baru Arab Saudi atau kenaikan kurs signifikan (asumsi kurs maksimal Rp 17.000).',
     'Bila hotel penuh, travel berhak mengganti dengan hotel setaraf.', 'Kamar quad (ber-empat) wajib memiliki teman sekamar; bila tidak, jamaah upgrade kamar.',
     'Dengan membayar DP, jamaah dianggap menyetujui seluruh ketentuan tertulis.'])}''',
    faqs=[('Berapa DP umroh di Elharamain Wisata?', 'Rp 6.000.000 per jamaah.'),
          ('Kapan batas pelunasan umroh?', '35 hari sebelum tanggal keberangkatan.'),
          ('Ke rekening mana pembayaran dilakukan?', 'Bank Mandiri 156.001.150.115.4 atau Bank BSI 710.857.755.4 a.n. PT Dhiyaa El Haramain El Mubarakah.')],
    cta=('Daftar Umroh Sekarang', "Assalamu'alaikum, saya mau daftar umroh."), rel=['syarat-umroh-dokumen'])

# 6
art(slug='harga-umroh-quad-triple-double', kw='harga umroh sekamar berdua',
    title='Harga Umroh Sekamar Berdua, Bertiga, atau Berempat: Mana yang Paling Hemat?',
    seo_title='Harga Umroh Sekamar Berdua vs Bertiga vs Berempat',
    desc='Bandingkan harga umroh sekamar berdua (double), bertiga (triple), dan berempat (quad) di Elharamain Wisata, plus selisih biaya tiap paket musim dingin.',
    cat=CAT_PAKET, cover=H(7),
    intro='Harga umroh ditentukan juga oleh tipe kamar. Artikel ini membahas <b>harga umroh sekamar berdua</b> (double) dibanding bertiga (triple) dan berempat (quad) pada paket Elharamain Wisata.',
    body=f'''<h2>Selisih Harga Quad, Triple, dan Double</h2>
<p>Pada brosur musim dingin, selisih kamar bertiga terhadap berempat berkisar Rp 2–6 juta, dan kamar berdua Rp 4–15 juta di atas harga berempat, tergantung paket.</p>
{table(['Paket', 'Ber-4 (Quad)', 'Ber-3 (Triple)', 'Ber-2 (Double)', 'Selisih Double vs Quad'],
       [[f"<b>{e(p['label'])}</b> ({p['bulan']})", rp(p['q']), rp(p['t']), rp(p['d']), rp(p['d'] - p['q'])] for p in PAKET])}
<h2>Tips Memilih Tipe Kamar</h2>
{ul(['<b>Quad</b> paling hemat, cocok untuk rombongan keluarga 4 orang. Jika tidak punya teman sekamar, jamaah wajib upgrade kamar.',
     '<b>Triple</b> jalan tengah untuk keluarga kecil atau 3 sahabat.', '<b>Double</b> memberi privasi terbaik, cocok untuk pasangan suami-istri.'])}''',
    faqs=[('Apa itu umroh quad, triple, double?', 'Quad = sekamar berempat, triple = bertiga, double = berdua. Makin sedikit penghuni kamar, makin tinggi harga per jamaah.'),
          ('Bagaimana jika daftar quad tapi tidak ada teman sekamar?', 'Sesuai ketentuan brosur, jamaah harus melakukan upgrade sesuai jenis kamar yang tersedia.'),
          ('Berapa harga umroh sekamar berdua termurah?', f"Paket Bronze Desember 2026: {rp(40500000)} per jamaah.")],
    cta=('Tanya Harga Kamar', "Assalamu'alaikum, saya mau tanya harga umroh per tipe kamar."), rel=['perbandingan-paket-umroh-bronze-silver-platinum'])

# 7
art(slug='itinerary-umroh-9-hari', kw='itinerary umroh 9 hari',
    title='Itinerary Umroh 9 Hari: Jadwal Kegiatan Harian Madinah, Makkah & Thaif',
    seo_title='Itinerary Umroh 9 Hari: Jadwal Harian Lengkap',
    desc='Itinerary umroh 9 hari Elharamain Wisata: ziarah Madinah, 3x umroh, Thaif, kereta cepat, hingga city tour Jeddah. Lihat jadwal kegiatan harinya di sini.',
    cover=H(8),
    intro='Program 9 hari adalah pilihan paling banyak di Elharamain Wisata. Berikut <b>itinerary umroh 9 hari</b> sesuai brosur Desember 2026, lengkap dengan kegiatan setiap harinya.',
    body=f'''<h2>Jadwal Harian Umroh 9 Hari</h2>
{table(['Hari', 'Kegiatan'], [[f'Hari {i + 1}', t] for i, t in enumerate(ITIN_9)])}
<h2>Sorotan Program</h2>
{ul(['<b>3x umroh</b>: dari Madinah, dari Qarnul Manazil (Thaif), dan dari Ji’ranah.', 'Perjalanan Madinah–Makkah memakai <b>kereta cepat</b>.',
     'Ziarah Thaif termasuk cable car Al-Hada dan kuliner Nasi Mandi.', 'Tahajjud bersama dan kajian di Madinah maupun Makkah.'])}
<h2>Paket yang Memakai Program 9 Hari</h2>
{paket(lambda p: p['hari'] == 9, cols=('label', 'bulan', 'berangkat', 'q'))}''',
    faqs=[('Berapa kali umroh dalam program 9 hari?', 'Tiga kali: umroh pertama saat dari Madinah, kedua dengan miqat Qarnul Manazil, ketiga dengan miqat Ji\'ranah.'),
          ('Apakah ada hari bebas?', 'Ya, hari ke-5 adalah acara bebas untuk i\'tikaf dan ibadah sunnah di Masjidil Haram.'),
          ('Apakah susunan itinerary bisa berubah?', 'Bisa, program menyesuaikan situasi dan kondisi terbaru sesuai ketentuan brosur.')],
    cta=('Tanya Jadwal 9 Hari', "Assalamu'alaikum, saya mau info umroh 9 hari."), rel=['perbandingan-paket-umroh-bronze-silver-platinum'])

# 8
art(slug='umroh-12-hari', kw='umroh 12 hari',
    title='Umroh 12 Hari: Jadwal Desember 2026 & Januari 2027, Harga, dan Keunggulannya',
    seo_title='Umroh 12 Hari: Jadwal, Harga & Keunggulan',
    desc='Umroh 12 hari bersama Elharamain Wisata: Silver 12 Hari & Gold 12 Hari berangkat Desember 2026 dan Januari 2027, in Madinah–out Jeddah, mulai Rp 41,5 juta.',
    cat=CAT_PAKET, cover='12_hari_januari_1',
    intro='Butuh waktu ibadah lebih panjang? <b>Umroh 12 hari</b> memberi tambahan hari untuk tahajjud bersama dan ibadah di Masjidil Haram dibanding program 9 hari.',
    body=f'''<h2>Jadwal & Harga Umroh 12 Hari</h2>
{paket(lambda p: p['hari'] == 12, cols=('label', 'bulan', 'berangkat', 'makkah', 'madinah', 'q', 't', 'd'))}
{fig('12_hari_januari_2', 'Brosur umroh 12 hari Januari 2027 Elharamain Wisata', 600)}
<h2>Itinerary Umroh 12 Hari</h2>
{ol(ITIN_12)}
<h2>Kelebihan Dibanding 9 Hari</h2>
{ul(['Tambahan hari tahajjud bersama dan thawaf sunnah di Makkah.', 'Hari khusus tahajjud dan kajian di Madinah.', 'Bonus GMC tour malam Jabal Uhud (Silver 12 Hari & Gold 12 Hari).'])}''',
    faqs=[('Kapan jadwal umroh 12 hari?', '9 Desember 2026 (Silver 12 Hari), 23 & 27 Desember (Eksklusif), serta 13, 14, 20, dan 24 Januari 2027.'),
          ('Berapa harga umroh 12 hari termurah?', f"Silver 12 Hari Desember 2026 mulai {rp(41500000)} (ber-empat)."),
          ('Rute umroh 12 hari?', 'Paket 12 hari Desember awal & Januari: in Madinah – out Jeddah; paket Eksklusif akhir Desember: Jeddah–Jeddah.')],
    cta=('Tanya Umroh 12 Hari', "Assalamu'alaikum, saya mau info umroh 12 hari."), rel=['itinerary-umroh-9-hari', 'umroh-januari-2027'])

# 9
art(slug='ziarah-madinah-saat-umroh', kw='ziarah madinah',
    title='Ziarah Madinah Saat Umroh: Tempat yang Dikunjungi Bersama Elharamain Wisata',
    seo_title='Ziarah Madinah: Daftar Tempat Ziarah Saat Umroh',
    desc='Ziarah Madinah saat umroh: Raudhah, makam Nabi ﷺ, Baqi, Masjid Quba, Jabal Uhud, Masjid Qiblatain, Khandaq, kebun kurma & Jabal Magnet.',
    cover=H(9),
    intro='Madinah adalah kota yang dirindukan setiap jamaah. Program <b>ziarah Madinah</b> di Elharamain Wisata dibagi menjadi ziarah dalam (area Masjid Nabawi) dan ziarah kota.',
    body=f'''<h2>Ziarah Dalam (Area Masjid Nabawi)</h2>
{ul(['Raudhah', 'Makam Nabi Muhammad ﷺ', 'Makam Baqi', 'Tsaqifah Bani Saidah'])}
<h2>Ziarah Kota Madinah</h2>
{ul(['Masjid Quba', 'Kebun kurma', 'Jabal Uhud', 'Masjid Qiblatain', 'Masjid Khandaq', 'Jabal Magnet'])}
<p>Pada hari ziarah kota, jamaah juga mengikuti <b>pemantapan manasik</b> sebelum berangkat ke Makkah untuk umroh pertama.</p>
<h2>Bonus di Madinah</h2>
{ul(['Free ATV & naik unta di Madinah (termasuk fasilitas paket).', 'GMC tour malam Jabal Uhud untuk paket 12 hari, Platinum & Premium Januari, serta program akhir tahun.'])}
{fig(F('free-unta-atv'), 'Fasilitas ziarah Madinah: naik unta dan ATV', 330)}
<h2>Hotel Dekat Masjid Nabawi</h2>
{ul([hotel_line('Al-Aqeeq'), hotel_line('Movenpick Madinah'), hotel_line('Peninsula Worth')])}''',
    faqs=[('Apa saja tempat ziarah Madinah?', 'Raudhah, makam Nabi ﷺ, Baqi, Tsaqifah Bani Saidah, Masjid Quba, kebun kurma, Jabal Uhud, Masjid Qiblatain, Masjid Khandaq, dan Jabal Magnet.'),
          ('Apakah ziarah Raudhah termasuk program?', 'Ya, termasuk ziarah dalam di hari kedua.'),
          ('Berapa jarak hotel Madinah ke Masjid Nabawi?', 'Al-Aqeeq dan Movenpick ±50 meter, Peninsula Worth ±150 meter.')],
    cta=('Tanya Program Ziarah', "Assalamu'alaikum, saya mau tanya program ziarah Madinah."), rel=['itinerary-umroh-9-hari'])

# 10
art(slug='ziarah-makkah-saat-umroh', kw='ziarah makkah',
    title='Ziarah Makkah: Jabal Tsur, Arafah, Mina, hingga Jabal Nur dalam Program Umroh',
    seo_title='Ziarah Makkah: Daftar Tempat Ziarah Saat Umroh',
    desc='Ziarah Makkah bersama Elharamain Wisata: Jabal Tsur, Arafah, Muzdalifah, Mina, Jamarat, miqat Ji\'ranah, dan melewati Jabal Nur.',
    cover=H(10),
    intro='Selain beribadah di Masjidil Haram, jamaah juga diajak mengenal tempat bersejarah. Berikut rute <b>ziarah Makkah</b> di program umroh Elharamain Wisata.',
    body=f'''<h2>Tempat yang Dikunjungi</h2>
{ul(['Jabal Tsur', 'Padang Arafah', 'Muzdalifah', 'Mina', 'Jamarat', 'Melewati Jabal Nur'])}
<h2>Sekaligus Umroh dari Ji'ranah</h2>
<p>Ziarah kota Makkah digabung dengan <b>umroh kedua/ketiga</b> yang mengambil miqat di Ji'ranah, sehingga perjalanan ziarah juga menjadi kesempatan menambah ibadah umroh.</p>
<h2>Hotel Makkah Pilihan</h2>
{ul([hotel_line('Anjum'), hotel_line('Marwa Rotana'), hotel_line('Fairmont')])}
<h2>Ibadah di Masjidil Haram</h2>
<p>Hari-hari di Makkah juga diisi tahajjud bersama, i'tikaf, dan thawaf sunnah, sebelum ditutup dengan thawaf wada.</p>''',
    faqs=[('Apa saja tempat ziarah Makkah?', 'Jabal Tsur, Arafah, Muzdalifah, Mina, Jamarat, dan melewati Jabal Nur.'),
          ('Apakah ada umroh saat ziarah Makkah?', 'Ya, umroh dengan miqat di Ji\'ranah dilakukan pada hari ziarah kota Makkah.'),
          ('Hotel Makkah terdekat di paket apa?', 'Marwa Rotana dan Fairmont yang berada di pelataran Zamzam Tower (paket Platinum, Premium, Gold).')],
    cta=('Tanya Program Makkah', "Assalamu'alaikum, saya mau tanya program ziarah Makkah."), rel=['ziarah-madinah-saat-umroh'])

# 11
art(slug='umroh-plus-thaif', kw='umroh plus thaif',
    title='Umroh Plus Thaif: Ziarah Kota Thaif, Cable Car Al-Hada & Miqat Qarnul Manazil',
    seo_title='Umroh Plus Thaif: Ziarah, Cable Car & Miqat',
    desc='Umroh plus Thaif gratis di semua paket Elharamain: Masjid Abdullah bin Abbas, Masjid Kuq, penyulingan mawar, cable car Al-Hada & miqat Qarnul Manazil.',
    cover=F('ziarah-thaif'),
    intro='Semua paket musim dingin Elharamain Wisata sudah termasuk <b>umroh plus Thaif</b>, kota sejuk di pegunungan yang sarat sejarah dakwah Rasulullah ﷺ.',
    body=f'''<h2>Rute Ziarah Thaif</h2>
{ul(['Masjid Abdullah bin Abbas', 'Masjid Kuq', 'Penyulingan parfum & mawar', 'Kuliner Nasi Mandi', 'Area bukit wisata Al-Hada', 'Cable car Al-Hada'])}
{fig(F('ziarah-thaif'), 'Program umroh plus Thaif Elharamain Wisata', 295)}
<h2>Umroh dari Miqat Qarnul Manazil</h2>
<p>Dalam perjalanan pulang dari Thaif, jamaah mengambil miqat di <b>Masjid Qarnul Manazil</b> untuk melaksanakan umroh berikutnya di Masjidil Haram.</p>
<h2>Sudah Termasuk Paket</h2>
<p>Brosur mencantumkan <b>free city tour Kota Thaif</b> sebagai fasilitas di seluruh paket, termasuk Bronze.</p>''',
    faqs=[('Apakah Thaif termasuk semua paket?', 'Ya, free city tour Thaif tercantum sebagai fasilitas semua paket musim dingin.'),
          ('Apa saja yang dikunjungi di Thaif?', 'Masjid Abdullah bin Abbas, Masjid Kuq, penyulingan parfum & mawar, bukit Al-Hada, dan cable car Al-Hada.'),
          ('Di mana miqat saat dari Thaif?', 'Di Masjid Qarnul Manazil.')],
    cta=('Tanya Umroh Plus Thaif', "Assalamu'alaikum, saya mau info umroh plus Thaif."), rel=['ziarah-makkah-saat-umroh', 'itinerary-umroh-9-hari'])

# 12
art(slug='kereta-cepat-haramain-umroh', kw='kereta cepat haramain',
    title='Naik Kereta Cepat Haramain Saat Umroh: Madinah ke Makkah Lebih Nyaman',
    seo_title='Kereta Cepat Haramain untuk Jamaah Umroh',
    desc='Semua paket umroh Elharamain Wisata memakai kereta cepat Haramain dari Madinah ke Makkah; program akhir tahun 2026 bahkan 2x naik kereta cepat.',
    cover=H(11),
    intro='Perjalanan Madinah–Makkah kini bisa ditempuh dengan <b>kereta cepat Haramain</b>. Di Elharamain Wisata, kereta cepat sudah menjadi bagian standar program umroh.',
    body=f'''<h2>Kapan Jamaah Naik Kereta Cepat?</h2>
<p>Sesuai itinerary, setelah umroh pertama (miqat dari Madinah), jamaah menuju Makkah menggunakan kereta cepat lalu check-in hotel Makkah.</p>
<h2>Program dengan 2x Kereta Cepat</h2>
<p>Paket eksklusif <b>akhir Desember 2026</b> mencantumkan <b>2x kereta cepat</b> dalam programnya.</p>
{paket(lambda p: p['label'].startswith('Eksklusif'), cols=('label', 'hari', 'berangkat', 'q'))}
<h2>Paket Lain yang Termasuk Kereta Cepat</h2>
<p>Program November (Riyadh Air), awal Desember, dan Januari seluruhnya bertajuk "Thaif + kereta cepat".</p>''',
    faqs=[('Apakah kereta cepat termasuk harga paket?', 'Ya, tercantum dalam program semua paket musim dingin.'),
          ('Rute kereta cepat saat umroh?', 'Dari Madinah menuju Makkah setelah umroh pertama.'),
          ('Paket mana yang 2x naik kereta cepat?', 'Paket eksklusif akhir Desember 2026 (Silver, Platinum, Silver 12 Hari, Gold 12 Hari).')],
    cta=('Tanya Paket Kereta Cepat', "Assalamu'alaikum, saya mau info umroh dengan kereta cepat."), rel=['umroh-akhir-tahun-2026'])

# 13
art(slug='umroh-3-kali-satu-perjalanan', kw='umroh 3 kali',
    title='Umroh 3 Kali dalam Satu Perjalanan: Miqat Madinah, Qarnul Manazil & Ji\'ranah',
    seo_title='Umroh 3 Kali dalam Satu Perjalanan: Caranya',
    desc='Paket Elharamain Wisata memfasilitasi umroh 3 kali: dari Madinah, miqat Qarnul Manazil di Thaif, dan miqat Ji\'ranah, dibimbing dengan Audio Hajj.',
    cover=F('umroh-3x'),
    intro='Salah satu keunggulan paket Elharamain Wisata adalah <b>umroh 3 kali</b> yang difasilitasi dan dibimbing dalam satu perjalanan.',
    body=f'''<h2>Tiga Kesempatan Umroh</h2>
{table(['Umroh', 'Miqat', 'Waktu dalam program'], [['Pertama', 'Dari Madinah', 'Saat berangkat ke Makkah'],
       ['Kedua/ketiga', 'Masjid Qarnul Manazil (Thaif)', 'Hari ziarah Thaif'], ['Kedua/ketiga', "Ji'ranah", 'Hari ziarah kota Makkah']])}
{fig(F('umroh-3x'), 'Fasilitasi umroh 3 kali Elharamain Wisata', 295)}
<h2>Dibimbing dengan Audio Hajj</h2>
<p>Setiap umroh dibimbing pembimbing dan dapat diikuti melalui <b>aplikasi/receiver Audio Hajj</b>, sehingga bacaan dan arahan tetap terdengar jelas di tengah keramaian.</p>''',
    faqs=[('Berapa kali umroh dalam paket Elharamain?', 'Difasilitasi sampai 3 kali umroh.'),
          ('Di mana saja miqatnya?', 'Dari Madinah, Qarnul Manazil (Thaif), dan Ji\'ranah.'),
          ('Apakah wajib mengikuti ketiganya?', 'Umroh tambahan difasilitasi dan dibimbing; konsultasikan kondisi fisik Anda dengan pembimbing.')],
    cta=('Tanya Program 3x Umroh', "Assalamu'alaikum, saya mau tanya program umroh 3 kali."), rel=['umroh-plus-thaif', 'ziarah-makkah-saat-umroh'])

# 14
art(slug='hotel-anjum-makkah', kw='hotel anjum makkah',
    title='Hotel Anjum Makkah: Jarak ke Masjidil Haram & Paket Umroh yang Memakainya',
    seo_title='Hotel Anjum Makkah: Jarak & Paket Umroh',
    desc='Hotel Anjum Makkah bintang 5 berjarak ±350 meter dari Masjidil Haram. Lihat paket umroh Elharamain Wisata yang menginap di Anjum beserta harganya.',
    cat=CAT_PAKET, cover=F('hotel-bintang-5'),
    intro='<b>Hotel Anjum Makkah</b> adalah hotel bintang 5 yang paling sering dipakai di paket Bronze dan Silver Elharamain Wisata.',
    body=f'''<h2>Lokasi Hotel Anjum</h2>
<p>Menurut brosur, Anjum Hotel berjarak <b>±350 meter dari Masjidil Haram</b>.</p>
<h2>Paket yang Menginap di Anjum</h2>
{paket(lambda p: 'Anjum' in p['makkah'], cols=('label', 'bulan', 'hari', 'berangkat', 'madinah', 'q'))}
<h2>Kombinasi Hotel Madinah</h2>
<p>Paket Anjum dipasangkan dengan Al-Aqeeq (±50 m dari Masjid Nabawi) atau Peninsula Worth (±150 m), tergantung jadwal.</p>''',
    faqs=[('Berapa jarak Hotel Anjum ke Masjidil Haram?', '±350 meter sesuai brosur Elharamain Wisata.'),
          ('Paket apa yang memakai Hotel Anjum?', 'Umumnya Bronze dan Silver, termasuk Silver 12 Hari.'),
          ('Apakah Anjum bintang 5?', 'Ya, tercantum sebagai hotel bintang 5 di brosur.')],
    cta=('Tanya Paket Hotel Anjum', "Assalamu'alaikum, saya mau info paket umroh hotel Anjum."), rel=['perbandingan-paket-umroh-bronze-silver-platinum'])

# 15
art(slug='hotel-marwa-rotana-makkah', kw='hotel marwa rotana makkah',
    title='Hotel Marwa Rotana Makkah: Di Pelataran Zamzam Tower, Paket Platinum & Gold',
    seo_title='Hotel Marwa Rotana Makkah untuk Umroh',
    desc='Hotel Marwa Rotana Makkah berada di pelataran Zamzam Tower. Dipakai paket umroh Platinum & Gold 12 Hari Elharamain Wisata, mulai Rp 46,5 juta.',
    cat=CAT_PAKET, cover=H(12),
    intro='Ingin hotel yang dekat pelataran Masjidil Haram? <b>Hotel Marwa Rotana Makkah</b> berada di <b>pelataran Zamzam Tower</b> dan menjadi hotel utama paket Platinum Elharamain Wisata.',
    body=f'''<h2>Paket yang Menginap di Marwa Rotana</h2>
{paket(lambda p: 'Marwa' in p['makkah'], cols=('label', 'bulan', 'hari', 'berangkat', 'madinah', 'q', 'd'))}
<h2>Bonus Paket Platinum</h2>
{ul(['Gratis menginap di Hotel 101 pada H-1', 'Golf car untuk sai', 'Wahana Toboggan (Desember) atau Jabal Khandama (Januari)', 'Abaya/outer & jaket eksklusif'])}
<p>Brosur mencantumkan "Marwa Rotana / Movenpick" sehingga hotel final dapat salah satunya atau setaraf.</p>''',
    faqs=[('Di mana lokasi Marwa Rotana Makkah?', 'Di pelataran Zamzam Tower, sesuai brosur.'),
          ('Paket apa yang memakai Marwa Rotana?', 'Platinum (Desember & Januari), Eksklusif Platinum, dan Gold 12 Hari.'),
          ('Berapa harga paket Marwa Rotana termurah?', f"Platinum Desember 2026 mulai {rp(46500000)} (ber-empat).")],
    cta=('Tanya Paket Platinum', "Assalamu'alaikum, saya mau info paket umroh Platinum Marwa Rotana."), rel=['hotel-anjum-makkah'])

# 16
art(slug='hotel-fairmont-makkah-umroh', kw='hotel fairmont makkah',
    title='Hotel Fairmont Makkah: Paket Umroh Premium Januari 2027 di Zamzam Tower',
    seo_title='Hotel Fairmont Makkah: Paket Umroh Premium 2027',
    desc='Menginap di Hotel Fairmont Makkah (pelataran Zamzam Tower) lewat paket umroh Premium Januari 2027 Elharamain Wisata: 11 & 31 Januari, mulai Rp 52 juta.',
    cat=CAT_PAKET, cover=H(13),
    intro='<b>Hotel Fairmont Makkah</b> berada di pelataran Zamzam Tower dan menjadi hotel utama paket <b>Premium</b>, kelas tertinggi program Januari 2027 Elharamain Wisata.',
    body=f'''<h2>Jadwal & Harga Paket Premium Fairmont</h2>
{paket(lambda p: 'Fairmont' in p['makkah'], cols=('label', 'hari', 'berangkat', 'makkah', 'madinah', 'q', 't', 'd'))}
<h2>Pasangan Hotel Madinah</h2>
<p>Paket Premium menginap di {hotel_line('Movenpick Madinah')}.</p>
<h2>Bonus Paket Premium</h2>
{ul(['Gratis menginap di Hotel 101 pada H-1', 'Jabal Khandama + golf car sai', 'Abaya & jaket eksklusif', 'GMC tour malam Jabal Uhud'])}
<h2>Rute</h2><p>In Madinah – out Jeddah dengan Saudia Airlines, program 9 hari + Thaif + kereta cepat.</p>''',
    faqs=[('Paket apa yang menginap di Fairmont Makkah?', 'Paket Premium Januari 2027.'),
          ('Kapan paket Premium berangkat?', '11 dan 31 Januari 2027.'),
          ('Berapa harga paket Premium?', 'Rp 52.000.000 (ber-empat), Rp 56.000.000 (ber-tiga), Rp 61.000.000 (ber-dua).')],
    cta=('Tanya Paket Premium Fairmont', "Assalamu'alaikum, saya mau info paket umroh Premium Fairmont."), rel=['hotel-marwa-rotana-makkah', 'umroh-januari-2027'])

# 17
art(slug='hotel-movenpick-madinah', kw='hotel movenpick madinah',
    title='Hotel Movenpick Madinah: ±50 Meter dari Masjid Nabawi, Paket Platinum & Premium',
    seo_title='Hotel Movenpick Madinah: Jarak & Paket Umroh',
    desc='Hotel Movenpick Madinah berjarak ±50 meter dari Masjid Nabawi. Dipakai paket umroh Platinum & Premium Januari 2027 Elharamain Wisata.',
    cat=CAT_PAKET, cover=H(14),
    intro='<b>Hotel Movenpick Madinah</b> berjarak sekitar <b>50 meter dari Masjid Nabawi</b>, sehingga jamaah mudah bolak-balik untuk shalat berjamaah dan ziarah Raudhah.',
    body=f'''<h2>Paket yang Menginap di Movenpick Madinah</h2>
{paket(lambda p: p['madinah'] == 'Movenpick', cols=('label', 'bulan', 'berangkat', 'makkah', 'q', 'd'))}
<h2>Kenapa Dekat Masjid Itu Penting?</h2>
<p>Program Madinah diisi tahajjud bersama, ziarah dalam, dan kajian. Hotel yang dekat membuat jamaah lansia maupun keluarga dengan anak tidak cepat lelah.</p>
<h2>Hotel Madinah Lain di Paket Elharamain</h2>
{ul([hotel_line('Al-Aqeeq'), hotel_line('Peninsula Worth')])}''',
    faqs=[('Berapa jarak Movenpick Madinah ke Masjid Nabawi?', '±50 meter sesuai brosur.'),
          ('Paket apa yang memakai Movenpick Madinah?', 'Platinum dan Premium Januari 2027.'),
          ('Hotel Makkah pasangannya?', 'Platinum: Marwa Rotana/Movenpick; Premium: Fairmont.')],
    cta=('Tanya Paket Movenpick', "Assalamu'alaikum, saya mau info paket umroh hotel Movenpick Madinah."), rel=['ziarah-madinah-saat-umroh', 'hotel-fairmont-makkah-umroh'])

# 18
art(slug='hotel-al-aqeeq-madinah', kw='hotel al-aqeeq madinah',
    title='Hotel Al-Aqeeq Madinah: Hotel Bintang 5 Dekat Masjid Nabawi untuk Umroh',
    seo_title='Hotel Al-Aqeeq Madinah: Jarak & Paket Umroh',
    desc='Hotel Al-Aqeeq Madinah (±50 m dari Masjid Nabawi) dipakai banyak paket umroh Elharamain Wisata: Silver, Platinum, 12 hari, hingga paket akhir tahun.',
    cat=CAT_PAKET, cover=H(15),
    intro='<b>Hotel Al-Aqeeq Madinah</b> adalah hotel bintang 5 yang paling banyak dipakai di paket Elharamain Wisata, dengan jarak ±50 meter dari Masjid Nabawi.',
    body=f'''<h2>Paket dengan Hotel Al-Aqeeq</h2>
{paket(lambda p: 'Al-Aqeeq' in p['madinah'], cols=('label', 'bulan', 'hari', 'berangkat', 'makkah', 'q'))}
<h2>Catatan "Setaraf"</h2>
<p>Beberapa paket mencantumkan "Al-Aqeeq / Al-Haram" atau "Peninsula / Al-Aqeeq". Jika hotel penuh, brosur memberi hak mengganti dengan hotel setaraf.</p>''',
    faqs=[('Berapa jarak Al-Aqeeq ke Masjid Nabawi?', '±50 meter sesuai brosur.'),
          ('Paket termurah dengan Al-Aqeeq?', f"Bronze November (Riyadh Air) atau Bronze Januari mulai {rp(37000000)}–{rp(37900000)}, tergantung hotel yang ditetapkan."),
          ('Apakah paket akhir tahun memakai Al-Aqeeq?', 'Ya, semua paket eksklusif akhir Desember 2026 memakai Al-Aqeeq (Platinum juga bisa Al-Haram).')],
    cta=('Tanya Paket Al-Aqeeq', "Assalamu'alaikum, saya mau info paket umroh hotel Al-Aqeeq."), rel=['hotel-movenpick-madinah'])

# 19
art(slug='hotel-peninsula-worth-madinah', kw='hotel peninsula worth madinah',
    title='Hotel Peninsula Worth Madinah: Pilihan Paket Umroh Bronze & Silver Desember',
    seo_title='Hotel Peninsula Worth Madinah untuk Umroh',
    desc='Hotel Peninsula Worth Madinah berjarak ±150 meter dari Masjid Nabawi, dipakai paket umroh Bronze, Bronze Plus & Silver Desember 2026 Elharamain Wisata.',
    cat=CAT_PAKET, cover=H(16),
    intro='Untuk paket ekonomis bintang 5 di bulan Desember, Elharamain Wisata memakai <b>Hotel Peninsula Worth Madinah</b> yang berjarak ±150 meter dari Masjid Nabawi.',
    body=f'''<h2>Paket dengan Peninsula Worth</h2>
{paket(lambda p: 'Peninsula' in p['madinah'], cols=('label', 'bulan', 'hari', 'berangkat', 'makkah', 'q', 't', 'd'))}
<h2>Pilihan Hemat Tetap Nyaman</h2>
<p>Dengan jarak ±150 meter, jamaah tetap bisa berjalan kaki ke Masjid Nabawi untuk shalat berjamaah, sambil menikmati harga paket yang lebih terjangkau.</p>''',
    faqs=[('Berapa jarak Peninsula Worth ke Masjid Nabawi?', '±150 meter sesuai brosur Desember 2026.'),
          ('Paket apa saja yang memakai Peninsula Worth?', 'Bronze, Bronze Plus, Silver Makkah First, dan Silver 12 Hari Desember 2026.'),
          ('Harga paket termurahnya?', f"Bronze 8 Desember 2026 mulai {rp(36500000)}.")],
    cta=('Tanya Paket Desember', "Assalamu'alaikum, saya mau info paket umroh Desember hotel Peninsula."), rel=['hotel-al-aqeeq-madinah'])

# 20
art(slug='perlengkapan-umroh-pria', kw='perlengkapan umroh pria',
    title='Perlengkapan Umroh Pria: 20 Item yang Didapat Jamaah Elharamain Wisata',
    seo_title='Perlengkapan Umroh Pria: Daftar 20 Item Lengkap',
    desc='Daftar perlengkapan umroh pria dari Elharamain Wisata: koper 24 & 18 inci, ihram eksklusif, sabuk ihram, koko ziarah, knitwear, ransel, hingga buku doa.',
    cover='perlengkapan-pria-2026',
    intro='Jamaah tidak perlu repot belanja. Berikut daftar <b>perlengkapan umroh pria</b> yang dibagikan Elharamain Wisata sesuai brosur 2026/2027.',
    body=f'''{fig('perlengkapan-pria-2026', 'Perlengkapan umroh pria Elharamain Wisata', 1200, 675)}
<h2>Daftar Lengkap Perlengkapan Pria</h2>
{perlengkapan('pria')}
<h2>Tambahan untuk Paket Tertentu</h2>
<p>Paket Platinum & Premium mendapat tambahan jaket eksklusif (item no. 21 di brosur).</p>
<h2>Yang Perlu Dibawa Sendiri</h2>
{ul(['Obat-obatan pribadi', 'Pakaian harian secukupnya', 'Dokumen perjalanan (paspor dan salinannya)'])}''',
    faqs=[('Apakah ihram sudah disediakan?', 'Ya, ihram eksklusif dan sabuk ihram termasuk perlengkapan pria.'),
          ('Berapa ukuran koper yang didapat?', 'Koper bagasi 24 inci dan koper kabin 18 inci.'),
          ('Berapa kg bagasi yang diizinkan?', 'Bagasi 35 kg per jamaah sesuai fasilitas paket.')],
    cta=('Tanya Perlengkapan', "Assalamu'alaikum, saya mau tanya perlengkapan umroh."), rel=['syarat-umroh-dokumen'])

# 21
art(slug='perlengkapan-umroh-wanita', kw='perlengkapan umroh wanita',
    title='Perlengkapan Umroh Wanita: Mukena, Scarf, Outer & 20 Item dari Elharamain',
    seo_title='Perlengkapan Umroh Wanita: Daftar 20 Item',
    desc='Daftar perlengkapan umroh wanita dari Elharamain Wisata: set mukena abu & hitam, 3 scarf, knitwear, outer ziarah Madinah, koper, sling bag, dan buku doa.',
    cover='perlengkapan-wanita-2026-a',
    intro='Jamaah wanita mendapat paket perlengkapan tersendiri. Inilah daftar <b>perlengkapan umroh wanita</b> dari brosur Elharamain Wisata musim dingin 2026/2027.',
    body=f'''{fig('perlengkapan-wanita-2026-a', 'Perlengkapan umroh wanita Elharamain Wisata', 1200, 675)}
<h2>Daftar Lengkap Perlengkapan Wanita</h2>
{perlengkapan('wanita')}
<h2>Tambahan Abaya untuk Platinum & Premium</h2>
<p>Paket Platinum dan Premium mendapat tambahan <b>abaya & jaket eksklusif</b>; paket Platinum akhir Desember mendapat outer & jaket.</p>
{fig('perlengkapan-wanita-2026-b', 'Contoh perlengkapan umroh wanita Elharamain Wisata', 1200, 675)}''',
    faqs=[('Berapa set mukena yang didapat?', 'Dua set: mukena abu dan mukena hitam.'),
          ('Apakah ada pakaian hangat?', 'Ya, knitwear wanita dan outer ziarah Madinah; Platinum & Premium juga mendapat jaket.'),
          ('Apakah koper termasuk?', 'Ya, koper bagasi 24 inci, koper kabin 18 inci, dan cover koper.')],
    cta=('Tanya Perlengkapan Wanita', "Assalamu'alaikum, saya mau tanya perlengkapan umroh wanita."), rel=['perlengkapan-umroh-pria'])

# 22
art(slug='oleh-oleh-umroh', kw='oleh-oleh umroh',
    title='Oleh-oleh Umroh dari Elharamain Wisata: Kurma Ajwa, Zamzam 5 Liter & Album Foto',
    seo_title='Oleh-oleh Umroh: Kurma Ajwa, Zamzam & Album Foto',
    desc='Oleh-oleh umroh dari Elharamain Wisata untuk jamaah: album foto, kurma Ajwa & Sukkari, cokelat, parfum eksklusif, sertifikat umroh, tumbler & zamzam 5 liter.',
    cover=F('oleh-oleh'),
    intro='Pulang umroh tanpa pusing mencari buah tangan. Elharamain Wisata menyiapkan <b>oleh-oleh umroh</b> yang dibagikan saat jamaah tiba di Soekarno-Hatta.',
    body=f'''<h2>Isi Paket Oleh-oleh</h2>
{oleh_ul()}
{fig(F('oleh-oleh'), 'Oleh-oleh umroh Elharamain Wisata', 296)}
<h2>Kapan Dibagikan?</h2>
<p>Sesuai itinerary, air zamzam dan gift oleh-oleh dibagikan di hari terakhir saat jamaah tiba di Bandara Soekarno-Hatta.</p>
<h2>Bagasi</h2>
<p>Fasilitas bagasi 35 kg per jamaah; kelebihan bagasi menjadi biaya pribadi.</p>''',
    faqs=[('Apa saja oleh-oleh dari Elharamain?', 'Album foto, kurma Ajwa, kurma Sukkari, cokelat, parfum eksklusif, sertifikat umroh, tumbler, dan air zamzam.'),
          ('Berapa liter air zamzam?', '5 liter per jamaah.'),
          ('Apakah album foto termasuk paket?', 'Ya, album foto perjalanan termasuk fasilitas.')],
    cta=('Tanya Fasilitas Paket', "Assalamu'alaikum, saya mau tanya fasilitas paket umroh."), rel=['perlengkapan-umroh-wanita'])

# 23
art(slug='ketentuan-pembatalan-reschedule-umroh', kw='pembatalan umroh',
    title='Ketentuan Pembatalan Umroh & Reschedule: Biaya dan Batas Waktunya',
    seo_title='Pembatalan Umroh & Reschedule: Biaya dan Aturan',
    desc='Ketentuan pembatalan umroh Elharamain Wisata: biaya Rp 1 juta hingga 90% sesuai waktu, serta syarat reschedule minimal 40 hari sebelum keberangkatan.',
    cover=H(17),
    intro='Rencana bisa berubah. Pahami <b>pembatalan umroh</b> dan aturan reschedule di Elharamain Wisata sebelum membayar DP agar tidak ada kejutan.',
    body=f'''<h2>Biaya Pembatalan</h2>
{batal_table()}
<h2>Ketentuan Reschedule</h2>
{ul(['Pergantian tanggal & program diperbolehkan bila diinformasikan <b>minimal 40 hari</b> sebelum keberangkatan.',
     'Permintaan kurang dari 40 hari sebelum keberangkatan tidak dapat dilayani.'])}
<h2>Force Majeure</h2>
<p>Dalam keadaan kahar (bencana alam, kerusuhan, wabah, dan sebagainya), susunan maupun tanggal perjalanan dapat berubah demi keamanan rombongan, dan biaya layanan yang sudah dibayar namun tidak terpakai tidak dikembalikan, sesuai ketentuan brosur.</p>''',
    faqs=[('Berapa biaya batal setelah DP?', 'Rp 1.000.000 setelah booking seat atau DP.'),
          ('Berapa biaya batal H-10?', '70% dari biaya paket untuk pembatalan 19–10 hari sebelum berangkat.'),
          ('Kapan batas reschedule?', 'Minimal 40 hari sebelum tanggal keberangkatan.')],
    cta=('Konsultasi Jadwal', "Assalamu'alaikum, saya mau konsultasi jadwal umroh."), rel=['cara-daftar-umroh-dp-6-juta'])

# 24
art(slug='umroh-saudia-airlines-direct-flight', kw='umroh saudia airlines',
    title='Umroh Saudia Airlines Direct Flight: Jadwal Desember 2026 & Januari 2027',
    seo_title='Umroh Saudia Airlines Direct Flight 2026/2027',
    desc='Umroh Saudia Airlines direct flight bersama Elharamain Wisata: jadwal Desember 2026 & Januari 2027, rute Jeddah atau Madinah, mulai Rp 36,5 juta.',
    cat=CAT_PAKET, cover=F('maskapai-saudia-direct-flight'),
    intro='Mayoritas paket musim dingin Elharamain Wisata menggunakan <b>umroh Saudia Airlines</b> dengan penerbangan langsung (direct flight) dari Soekarno-Hatta.',
    body=f'''<h2>Jadwal Paket Saudia Airlines</h2>
{paket(lambda p: p['maskapai'] == 'Saudia Airlines', cols=('label', 'bulan', 'hari', 'berangkat', 'q'))}
{fig(F('maskapai-saudia-direct-flight'), 'Umroh Saudia Airlines direct flight Elharamain Wisata', 254)}
<h2>Rute yang Tersedia</h2>
{ul(['Jeddah – Jeddah (Bronze, paket akhir tahun)', 'Madinah – Jeddah (Silver Madinah First, Platinum, Premium, 12 hari)', 'Jeddah – Madinah (Silver Makkah First, Silver 25 Januari)'])}
<h2>Tiket Termasuk Paket</h2><p>Tiket pesawat PP kelas ekonomi, airport tax, handling bandara, dan bagasi 35 kg sudah termasuk.</p>''',
    faqs=[('Apakah umroh Saudia Airlines direct?', 'Brosur menyebut maskapai direct flight Saudia Airlines untuk paket Desember dan Januari.'),
          ('Berapa bagasi Saudia di paket ini?', '35 kg per jamaah sesuai fasilitas paket.'),
          ('Paket Saudia termurah?', f"Bronze 8 Desember 2026 mulai {rp(36500000)}.")],
    cta=('Tanya Umroh Saudia', "Assalamu'alaikum, saya mau info umroh Saudia Airlines."), rel=['umroh-riyadh-air-november-2026'])

# 25
art(slug='umroh-madinah-first-atau-makkah-first', kw='umroh madinah first',
    title='Umroh Madinah First atau Makkah First? Beda Rute dan Cara Memilihnya',
    seo_title='Umroh Madinah First vs Makkah First: Pilih Mana?',
    desc='Umroh Madinah first (in Madinah–out Jeddah) atau Makkah first (in Jeddah–out Madinah)? Simak bedanya dan paket Elharamain Wisata untuk tiap rute.',
    cover=H(18),
    intro='Di brosur Anda akan menemukan istilah <b>umroh Madinah first</b> dan Makkah first. Keduanya sama-sama umroh, bedanya pada kota yang dikunjungi lebih dulu.',
    body=f'''<h2>Pengertian</h2>
{table(['Istilah', 'Rute', 'Urutan'], [['Madinah First', 'In Madinah – out Jeddah', 'Ziarah Madinah dulu, lalu umroh dan ibadah di Makkah'],
       ['Makkah First', 'In Jeddah – out Madinah', 'Umroh di Makkah dulu, ditutup di Madinah']])}
<h2>Paket per Rute</h2>
<h3>Madinah First</h3>{paket(lambda p: 'Madinah First' in p['label'] or p['label'] in ('Platinum', 'Premium') or (p['hari'] == 12 and not p['label'].startswith('Eksklusif')), cols=('label', 'bulan', 'berangkat', 'q'))}
<h3>Makkah First</h3>{paket(lambda p: 'Makkah First' in p['label'], cols=('label', 'bulan', 'berangkat', 'q'))}
<h2>Mana yang Cocok?</h2>
{ul(['Madinah First: adaptasi lebih santai sebelum rangkaian umroh; umroh pertama diambil dari miqat saat menuju Makkah.', 'Makkah First: langsung umroh, lalu penutupan perjalanan di Madinah yang tenang.'])}''',
    faqs=[('Apa itu umroh Madinah first?', 'Rute in Madinah – out Jeddah: jamaah ke Madinah dulu, baru ke Makkah.'),
          ('Paket apa yang Makkah first?', 'Silver Makkah First 8 Desember 2026 (in Jeddah – out Madinah).'),
          ('Apakah harganya berbeda?', f"Di Desember 2026, Silver Makkah First {rp(37500000)} dan Silver Madinah First {rp(38000000)} (ber-empat).")],
    cta=('Tanya Rute Umroh', "Assalamu'alaikum, saya mau tanya rute umroh Madinah first atau Makkah first."), rel=['umroh-saudia-airlines-direct-flight'])

# 26
art(slug='city-tour-jeddah-umroh', kw='city tour jeddah',
    title='City Tour Jeddah Saat Umroh: Museum Wahyu, Masjid Qisash & Corniche',
    seo_title='City Tour Jeddah Saat Umroh: Rute & Tempatnya',
    desc='City tour Jeddah di akhir program umroh Elharamain Wisata: Museum Wahyu, melewati Masjid Qisash dan Corniche (bila memungkinkan) sebelum pulang.',
    cover=H(19),
    intro='Sebelum terbang pulang, jamaah diajak <b>city tour Jeddah</b>, kota pelabuhan yang menjadi gerbang utama jamaah umroh.',
    body=f'''<h2>Rute City Tour Jeddah</h2>
{ul(['Museum Wahyu', 'Melewati Masjid Qisash', 'Corniche Jeddah (bila memungkinkan)'])}
<p>Rangkaian ini dilakukan setelah thawaf wada di Makkah. Pada program Riyadh Air November, jamaah juga menginap semalam di hotel Jeddah sebelum city tour.</p>
<h2>Paket yang Berakhir di Jeddah</h2>
{paket(lambda p: p['hari'] == 12 or 'Madinah First' in p['label'] or p['label'] in ('Bronze', 'Platinum', 'Premium'), cols=('label', 'bulan', 'berangkat'))}''',
    faqs=[('Apa saja yang dikunjungi saat city tour Jeddah?', 'Museum Wahyu, melewati Masjid Qisash, dan Corniche bila memungkinkan.'),
          ('Kapan city tour Jeddah dilakukan?', 'Di hari terakhir setelah thawaf wada, sebelum ke bandara.'),
          ('Apakah city tour termasuk biaya paket?', 'Ya, program & city tour sesuai itinerary termasuk fasilitas.')],
    cta=('Tanya Itinerary', "Assalamu'alaikum, saya mau tanya itinerary umroh."), rel=['itinerary-umroh-9-hari'])

# 27
art(slug='program-tahajjud-dan-kajian-umroh', kw='tahajjud bersama saat umroh',
    title='Tahajjud Bersama Saat Umroh: Program Ibadah & Kajian Elharamain Wisata',
    seo_title='Tahajjud Bersama Saat Umroh & Kajian Islami',
    desc='Program tahajjud bersama saat umroh di Masjid Nabawi dan Masjidil Haram, kajian tsuruq & kajian keislaman, dibimbing asatidz lulusan Timur Tengah.',
    cover=F('program-bersama'),
    intro='Umroh bukan hanya perjalanan, tapi juga pembinaan. Elharamain Wisata menjadwalkan <b>tahajjud bersama saat umroh</b> dan kajian di Madinah maupun Makkah.',
    body=f'''<h2>Jadwal Tahajjud & Kajian</h2>
{ul(['Madinah: tahajjud bersama, ziarah Raudhah, dan kajian tsuruq (hari ke-2).', 'Madinah: pemantapan manasik & kajian singkat (hari ke-3).',
     'Makkah: tahajjud bersama dan kajian keislaman sebelum thawaf wada.', 'Program 12 hari: tambahan hari khusus tahajjud di Madinah dan Makkah.'])}
{fig(F('program-bersama'), 'Program tahajjud bersama dan kajian Elharamain Wisata', 295)}
<h2>Dibimbing Asatidz</h2>
<p>Program dipandu tim pembimbing, di antaranya {', '.join(PEMBIMBING[:4])}.</p>''',
    faqs=[('Apakah tahajjud bersama wajib?', 'Program dijadwalkan bersama, tetap menyesuaikan kondisi jamaah.'),
          ('Kajian apa saja?', 'Kajian tsuruq, kajian singkat manasik, dan kajian keislaman.'),
          ('Siapa pembimbingnya?', 'Asatidz lulusan Timur Tengah seperti Ustadz Dr. Muhammad Tahir Lc MA dan Ustadz Ahmad Shobirin Lc MA.')],
    cta=('Tanya Program Ibadah', "Assalamu'alaikum, saya mau tanya program ibadah umroh."), rel=['ziarah-madinah-saat-umroh'])

# 28
art(slug='audio-hajj-umroh', kw='audio hajj',
    title='Audio Hajj: Umroh dan Kajian Lebih Khusyuk dengan Audio Receiver',
    seo_title='Audio Hajj untuk Umroh: Fungsi & Manfaatnya',
    desc='Elharamain Wisata memakai aplikasi/receiver Audio Hajj agar bimbingan umroh dan kajian terdengar jelas di tengah keramaian Masjidil Haram.',
    cover=F('audio-haji'),
    intro='Di tengah jutaan jamaah, suara pembimbing sering tak terdengar. Karena itu Elharamain Wisata memakai <b>Audio Hajj</b> untuk umroh dan kajian.',
    body=f'''<h2>Apa Fungsi Audio Hajj?</h2>
<p>Jamaah mendengarkan arahan dan bacaan pembimbing melalui perangkat/aplikasi Audio Hajj, sehingga tetap bisa mengikuti bimbingan meski berjarak dari pembimbing.</p>
{fig(F('audio-haji'), 'Audio Hajj Elharamain Wisata untuk umroh', 295)}
<h2>Dipakai Kapan Saja?</h2>
{ul(['Saat umroh (fasilitasi sampai 3x umroh).', 'Saat kajian dan ziarah.'])}
<h2>Termasuk Fasilitas</h2><p>Brosur mencantumkan "Kajian dan Umroh menggunakan Aplikasi Audio Hajj" sebagai fasilitas semua paket.</p>''',
    faqs=[('Apakah Audio Hajj berbayar?', 'Tidak, termasuk fasilitas paket.'),
          ('Kapan Audio Hajj digunakan?', 'Saat umroh dan kajian.'),
          ('Berapa kali umroh yang difasilitasi?', 'Sampai 3 kali umroh.')],
    cta=('Tanya Fasilitas', "Assalamu'alaikum, saya mau tanya fasilitas Audio Hajj."), rel=['umroh-3-kali-satu-perjalanan'])

# 29
art(slug='bonus-paket-umroh-platinum', kw='bonus paket umroh platinum',
    title='Bonus Paket Umroh Platinum: Hotel 101, Golf Car Sai, Jaket & Abaya Eksklusif',
    seo_title='Bonus Paket Umroh Platinum & Premium Elharamain',
    desc='Bonus paket umroh Platinum & Premium Elharamain Wisata: free menginap H-1 Hotel 101, golf car sai, Toboggan/Jabal Khandama, abaya & jaket, GMC tour Uhud.',
    cat=CAT_PAKET, cover=H(20),
    intro='Selain hotel di pelataran Zamzam Tower, paket Platinum dan Premium membawa sejumlah hadiah. Berikut rincian <b>bonus paket umroh Platinum</b> per jadwal.',
    body=f'''<h2>Rincian Bonus per Jadwal</h2>
{table(['Paket', 'Bonus'], [['Platinum 7 Des 2026', 'H-1 free Hotel 101, wahana Toboggan + golf car sai, abaya & jaket eksklusif, GMC tour night Jabal Uhud'],
       ['Eksklusif Platinum akhir Des 2026', 'H-1 free Hotel 101, wahana Toboggan + golf car sai, outer & jaket eksklusif'],
       ['Platinum & Premium Jan 2027', 'H-1 free Hotel 101, Jabal Khandama + golf car sai, abaya & jaket eksklusif, GMC tour night Jabal Uhud']])}
<h2>Harga Paket Platinum & Premium</h2>
{paket(lambda p: p['tier'] in ('platinum', 'premium'), cols=('label', 'bulan', 'berangkat', 'makkah', 'q', 'd'))}''',
    faqs=[('Apa itu H-1 free Hotel 101?', 'Jamaah Platinum/Premium mendapat gratis menginap di Hotel 101 sehari sebelum keberangkatan, sesuai brosur.'),
          ('Apakah golf car sai termasuk?', 'Ya, untuk paket Platinum dan Premium.'),
          ('Apa bonus pakaian yang didapat?', 'Abaya & jaket eksklusif (Desember awal & Januari) atau outer & jaket (akhir Desember).')],
    cta=('Tanya Paket Platinum', "Assalamu'alaikum, saya mau info bonus paket Platinum."), rel=['hotel-marwa-rotana-makkah', 'hotel-fairmont-makkah-umroh'])

# 30
art(slug='tips-umroh-musim-dingin', kw='tips umroh musim dingin',
    title='Tips Umroh Musim Dingin: Pakaian, Perlengkapan, dan Persiapan Ibadah',
    seo_title='Tips Umroh Musim Dingin: Persiapan & Pakaian',
    desc='Tips umroh musim dingin (November–Januari): siapkan pakaian berlapis, manfaatkan knitwear & jaket dari travel, jaga stamina untuk 3x umroh dan ziarah.',
    cover=H(21),
    intro='Musim dingin adalah waktu favorit berumroh karena cuaca lebih sejuk. Agar ibadah tetap nyaman, simak <b>tips umroh musim dingin</b> berikut.',
    body=f'''<h2>1. Siapkan Pakaian Berlapis</h2>
<p>Pagi dan malam terasa lebih dingin dibanding siang, terutama di Madinah dan saat ziarah ke daerah perbukitan seperti Thaif. Gunakan pakaian berlapis yang mudah dilepas.</p>
<h2>2. Manfaatkan Perlengkapan dari Travel</h2>
<p>Jamaah Elharamain Wisata mendapat <b>knitwear</b> (pria & wanita) dan <b>outer ziarah Madinah</b> (wanita); paket Platinum & Premium mendapat jaket eksklusif.</p>
<h2>3. Jaga Stamina untuk Program Padat</h2>
<p>Program musim dingin mencakup sampai 3x umroh, ziarah Thaif, dan ziarah kota. Tidur cukup dan manfaatkan hari bebas untuk ibadah dengan ritme sendiri.</p>
<h2>4. Pilih Jadwal yang Tepat</h2>
{paket(lambda p: p['label'] in ('Bronze',), cols=('label', 'bulan', 'hari', 'berangkat', 'q'))}
<h2>5. Lengkapi Dokumen Lebih Awal</h2><p>Musim liburan akhir tahun ramai peminat. Siapkan paspor (berlaku minimal 10 bulan) sebelum mendaftar.</p>''',
    faqs=[('Kapan musim dingin untuk umroh?', 'Paket musim dingin Elharamain Wisata dijadwalkan Desember 2026 – Januari 2027, dengan program musim sejuk di November.'),
          ('Apakah travel menyediakan jaket?', 'Knitwear untuk semua jamaah; jaket eksklusif untuk paket Platinum & Premium.'),
          ('Apa paket musim dingin termurah?', f"Bronze Desember 2026 mulai {rp(36500000)}.")],
    cta=('Tanya Paket Musim Dingin', "Assalamu'alaikum, saya mau info umroh musim dingin."), rel=['perlengkapan-umroh-pria', 'perlengkapan-umroh-wanita'])

# 31
art(slug='umroh-bronze-plus-jumat-di-masjidil-haram', kw='umroh bronze plus',
    title='Umroh Bronze Plus Desember 2026: Hotel Prestige & Shalat Jumat di Masjidil Haram',
    seo_title='Umroh Bronze Plus: Jumat di Masjidil Haram',
    desc='Paket umroh Bronze Plus Elharamain Wisata berangkat 11 & 12 Desember 2026: hotel Prestige Makkah, Peninsula Worth Madinah, dan shalat Jumat di Masjidil Haram.',
    cat=CAT_PAKET, cover=H(22),
    intro='<b>Umroh Bronze Plus</b> adalah varian hemat bulan Desember dengan keistimewaan jadwal: jamaah mendapatkan <b>shalat Jumat di Masjidil Haram</b>.',
    body=f'''<h2>Detail Paket Bronze Plus</h2>
{paket(lambda p: p['label'] == 'Bronze Plus', cols=('label', 'hari', 'berangkat', 'makkah', 'madinah', 'q', 't', 'd'))}
<h2>Beda dengan Bronze Biasa</h2>
{table(['', 'Bronze (8 Des)', 'Bronze Plus (11 & 12 Des)'], [['Hotel Makkah', 'Anjum', 'Prestige'], ['Hotel Madinah', 'Peninsula Worth', 'Peninsula Worth'],
       ['Keistimewaan', 'Harga termurah', 'Jumat di Masjidil Haram'], ['Harga ber-4', rp(36500000), rp(37500000)]])}
<h2>Rute</h2><p>In Jeddah – out Jeddah dengan Saudia Airlines, program 9 hari + Thaif + kereta cepat.</p>''',
    faqs=[('Kapan umroh Bronze Plus berangkat?', '11 dan 12 Desember 2026.'),
          ('Apa keistimewaan Bronze Plus?', 'Jadwal yang memungkinkan shalat Jumat di Masjidil Haram, dengan hotel Prestige di Makkah.'),
          ('Berapa harganya?', 'Rp 37.500.000 (ber-empat), Rp 39.500.000 (ber-tiga), Rp 41.500.000 (ber-dua).')],
    cta=('Daftar Bronze Plus', "Assalamu'alaikum, saya mau daftar umroh Bronze Plus Desember."), rel=['perbandingan-paket-umroh-bronze-silver-platinum'])

# 32
art(slug='fasilitas-paket-umroh', kw='fasilitas paket umroh',
    title='Fasilitas Paket Umroh Elharamain Wisata: 22 Layanan yang Sudah Termasuk',
    seo_title='Fasilitas Paket Umroh: 22 Layanan Sudah Termasuk',
    desc='Rincian fasilitas paket umroh Elharamain Wisata: tiket, visa, asuransi, VIP lounge, hotel bintang 5, makan 3x, Audio Hajj, Thaif, zamzam 5 liter, dan lainnya.',
    cover=F('vip-lounge'),
    intro='Sebelum membandingkan harga, cek dulu isinya. Berikut daftar <b>fasilitas paket umroh</b> Elharamain Wisata sesuai brosur musim dingin 2026/2027.',
    body=f'''<h2>Fasilitas yang Termasuk</h2>
{fasilitas_ul()}
{fig(F('vip-lounge'), 'Fasilitas VIP Lounge Umroh Elharamain Wisata', 295)}
<h2>Biaya yang Belum Termasuk</h2>
{belum_ul()}
<h2>Kuliner Selama Perjalanan</h2><p>Selain makan fullboard 3x sehari di hotel, brosur mencantumkan kuliner Nasi Mandhi, Kunafa, dan Albaik 3x + snack meal.</p>''',
    faqs=[('Apakah visa dan asuransi termasuk?', 'Ya, visa umroh dan asuransi perjalanan termasuk.'),
          ('Berapa kali makan per hari?', 'Fullboard 3x sehari di hotel.'),
          ('Apa yang tidak termasuk?', 'Paspor, suntik meningitis & polio, keperluan pribadi, kelebihan bagasi, dan penyesuaian biaya akibat kebijakan baru.')],
    cta=('Tanya Fasilitas Paket', "Assalamu'alaikum, saya mau tanya fasilitas paket umroh."), rel=['syarat-umroh-dokumen', 'oleh-oleh-umroh'])

# 33
art(slug='kuliner-arab-saudi-saat-umroh', kw='kuliner arab saudi',
    title='Kuliner Arab Saudi Saat Umroh: Nasi Mandi, Kunafa & Albaik Bersama Elharamain',
    seo_title='Kuliner Arab Saudi Saat Umroh: Mandi, Kunafa, Albaik',
    desc='Cicipi kuliner Arab Saudi saat umroh bersama Elharamain Wisata: Nasi Mandi di Thaif, Kunafa, dan Albaik 3x + snack meal, sudah termasuk paket.',
    cover=F('kuliner-arab-saudi'),
    intro='Umroh juga momen mengenal budaya setempat. Paket Elharamain Wisata sudah memasukkan pengalaman <b>kuliner Arab Saudi</b> dalam programnya.',
    body=f'''<h2>Menu yang Termasuk Paket</h2>
{ul(['<b>Nasi Mandi</b> — dinikmati saat ziarah Thaif', '<b>Kunafa</b>', '<b>Albaik</b> 3x + snack meal'])}
{fig(F('kuliner-arab-saudi'), 'Kuliner Arab Saudi Nasi Mandi Kunafa Albaik Elharamain Wisata', 296)}
<h2>Makan Harian di Hotel</h2><p>Di luar kuliner khas, jamaah mendapat makan fullboard 3x sehari di hotel sesuai paket.</p>''',
    faqs=[('Apakah kuliner khas termasuk biaya?', 'Ya, Nasi Mandhi, Kunafa, dan Albaik tercantum sebagai fasilitas.'),
          ('Kapan makan Nasi Mandi?', 'Saat program ziarah Thaif.'),
          ('Berapa kali makan di hotel?', 'Fullboard 3x sehari.')],
    cta=('Tanya Program', "Assalamu'alaikum, saya mau tanya program umroh."), rel=['umroh-plus-thaif', 'fasilitas-paket-umroh'])

# 34
art(slug='pembimbing-umroh-elharamain-wisata', kw='pembimbing umroh',
    title='Pembimbing Umroh Elharamain Wisata: Asatidz Lulusan Timur Tengah',
    seo_title='Pembimbing Umroh: Asatidz Lulusan Timur Tengah',
    desc='Kenali pembimbing umroh Elharamain Wisata: 12 asatidz bergelar Lc, MA, MH, dan MPd yang membimbing ibadah sesuai sunnah dari manasik hingga pulang.',
    cover=F('full-bimbingan'),
    intro='Kualitas umroh sangat ditentukan pembimbingnya. Elharamain Wisata menugaskan <b>pembimbing umroh</b> dari kalangan asatidz lulusan Timur Tengah.',
    body=f'''<h2>Daftar Pembimbing Ibadah</h2>
{pembimbing_ul()}
{fig(F('full-bimbingan'), 'Full bimbingan umroh sesuai sunnah Elharamain Wisata', 295)}
<h2>Peran Pembimbing</h2>
{ul(['Manasik umroh di hotel berbintang sebelum berangkat.', 'Pemantapan manasik di Madinah.', 'Membimbing 3x umroh dengan Audio Hajj.', 'Mengisi kajian dan tahajjud bersama.'])}''',
    faqs=[('Siapa saja pembimbing umroh Elharamain?', 'Di antaranya Ustadz Dr. Muhammad Tahir Lc MA, Ustadz Dr. Abdul Kadir Abu Lc MA, dan Ustadz Ahmad Shobirin Lc MA.'),
          ('Apakah ada manasik sebelum berangkat?', 'Ya, manasik umroh di hotel berbintang termasuk fasilitas.'),
          ('Apakah bimbingan sesuai sunnah?', 'Ya, brosur menegaskan program ibadah dibimbing secara intensif dan sesuai sunnah.')],
    cta=('Tanya Jadwal Manasik', "Assalamu'alaikum, saya mau tanya jadwal manasik umroh."), rel=['program-tahajjud-dan-kajian-umroh'])

# 35
art(slug='gmc-tour-malam-jabal-uhud', kw='tour malam jabal uhud',
    title='Tour Malam Jabal Uhud dengan GMC: Bonus Paket 12 Hari & Platinum',
    seo_title='Tour Malam Jabal Uhud (GMC): Paket yang Dapat',
    desc='Tour malam Jabal Uhud menggunakan GMC jadi bonus paket umroh 12 hari, Platinum, Premium, dan program akhir tahun 2026 Elharamain Wisata.',
    cover=H(23),
    intro='Jabal Uhud menyimpan sejarah besar perjuangan Rasulullah ﷺ. Beberapa paket Elharamain Wisata memberi bonus <b>tour malam Jabal Uhud</b> dengan kendaraan GMC.',
    body=f'''<h2>Paket yang Mendapat GMC Tour Jabal Uhud</h2>
{paket(lambda p: 'GMC' in p['desc'] or p['label'] in ('Platinum', 'Premium'), cols=('label', 'bulan', 'berangkat', 'q'))}
<h2>Selain Tour Malam</h2>
<p>Semua jamaah tetap mengunjungi Jabal Uhud pada ziarah kota Madinah di siang hari, bersama Masjid Quba, Masjid Qiblatain, dan Masjid Khandaq.</p>''',
    faqs=[('Apa itu GMC tour night Jabal Uhud?', 'Tour malam ke Jabal Uhud menggunakan kendaraan GMC, bonus untuk paket tertentu.'),
          ('Paket apa yang mendapat bonus ini?', 'Silver 12 Hari, Gold 12 Hari, Platinum Desember, Platinum & Premium Januari, serta program akhir tahun.'),
          ('Apakah paket lain ke Jabal Uhud?', 'Ya, lewat ziarah kota Madinah di siang hari.')],
    cta=('Tanya Paket 12 Hari', "Assalamu'alaikum, saya mau info paket dengan tour Jabal Uhud."), rel=['ziarah-madinah-saat-umroh', 'umroh-12-hari'])
