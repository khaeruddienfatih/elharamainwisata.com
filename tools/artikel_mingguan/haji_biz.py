"""35 artikel untuk haji.biz: 23 haji plus (brosur haji 1448 H) + 12 umroh (brosur umroh). Artikel boleh campur."""
from data import HAJI, HAJI_ANTRIAN, HAJI_ITIN, ITIN_9, PAKET
from render import e, fig, haji_table, hotel_line, ol, paket, rp, table, ul, usd

CAT_HAJI, CAT_PAKET_HAJI, CAT_KHUSUS, CAT_MIX = 3, 8, 40, 1
U = 'https://www.haji.biz/wp-content/uploads/2026/09/'
IMG = {751: U + 'jamaah-haji-kabah-malam-scaled.webp', 752: U + 'jamaah-haji-tenda-mina-scaled.webp',
       753: U + 'jamaah-haji-doa-bersama-scaled.webp', 755: U + 'jamaah-haji-mekkah-1-scaled.webp',
       756: U + 'jamaah-haji-mekkah-2-scaled.webp'}
ALT = {751: 'Jamaah haji di depan Ka\'bah pada malam hari', 752: 'Jamaah haji di tenda Mina',
       753: 'Jamaah haji berdoa bersama', 755: 'Jamaah haji di Makkah', 756: 'Jamaah haji di Makkah'}
LEGAL_H = ('PT Dhiyaa El Haramain El Mubarakah (Elharamain Wisata), Penyelenggara Ibadah Haji Khusus (PIHK) resmi '
           'Kementerian Agama RI No. 846/2020')
EST = 'Biaya di atas adalah estimasi keberangkatan 2027 (1448 H) dan diinformasikan final 1 tahun sebelum keberangkatan.'

A = []


def art(**k):
    k.setdefault('site', 'hajibiz')
    k.setdefault('cat', CAT_HAJI)
    if 'feat' in k:
        k.setdefault('cover', IMG[k['feat']])
        k.setdefault('cover_alt', ALT[k['feat']])
    A.append(k)


def h(name):
    return next(x for x in HAJI if x[0] == name)


def haji_card(name):
    n, a, b, c, mk, md, dur, mt, jt = h(name)
    return table(['Komponen', f'Paket {n}'], [['Setoran awal porsi', '4.000 USD'], ['Ber-4 / Ber-3 / Ber-2', f'{usd(a)} / {usd(b)} / {usd(c)}'],
                                             ['Durasi', dur], ['Hotel Makkah', mk], ['Hotel Madinah', md], ['Maktab VIP', f'{mt} (jarak tenda {jt})']])


# ============ HAJI (23) ============
art(slug='program-arbain-haji-plus', kw='program arbain', cat=CAT_PAKET_HAJI, feat=753,
    title='Program Arbain Haji Plus: 40 Waktu Shalat di Masjid Nabawi dengan Paket Gold Arbain',
    seo_title='Program Arbain Haji Plus: Paket Gold Arbain 1448 H',
    desc='Program Arbain haji plus: 40 waktu shalat fardhu berjamaah berturut-turut di Masjid Nabawi, tersedia di paket Gold Arbain Elharamain Wisata (27–28 hari).',
    intro='<b>Program Arbain</b> adalah melaksanakan 40 waktu shalat fardhu berjamaah berturut-turut di Masjid Nabawi, Madinah. Di Elharamain Wisata, program ini tersedia khusus pada paket <b>Gold Arbain</b>.',
    body=f'''<h2>Paket Gold Arbain 1448 H</h2>{haji_card('Gold Arbain')}<p>{EST}</p>
<h2>Kenapa Durasinya Lebih Panjang?</h2>
<p>Paket reguler Elharamain berdurasi 22–23 hari, sedangkan Gold Arbain <b>27–28 hari</b> untuk memberi waktu cukup di Madinah menunaikan 40 waktu shalat.</p>
<h2>Gold vs Gold Arbain</h2>
{table(['', 'Gold', 'Gold Arbain'], [['Durasi', '22–23 hari', '27–28 hari'], ['Hotel', 'Marwa Rotana & Al-Aqeeq', 'Marwa Rotana & Al-Aqeeq'],
       ['Ber-4', usd(15500), usd(17000)], ['Program Arbain', '–', 'Termasuk']])}''',
    faqs=[('Apa itu program Arbain?', 'Shalat fardhu berjamaah 40 waktu berturut-turut di Masjid Nabawi Madinah.'),
          ('Paket apa yang termasuk Arbain?', 'Paket Gold Arbain, durasi 27–28 hari.'),
          ('Berapa biaya Gold Arbain?', f'{usd(17000)} (ber-4), {usd(18500)} (ber-3), {usd(20000)} (ber-2), estimasi 2027.')],
    cta=('Tanya Paket Gold Arbain', "Assalamu'alaikum, saya mau info paket haji plus Gold Arbain."), rel=['perbandingan-paket-haji-plus-silver-gold-platinum'])

art(slug='apa-itu-tanazul-haji', kw='tanazul', feat=752,
    title='Apa Itu Tanazul dalam Haji Khusus? Pengertian dan Cara Kerjanya',
    seo_title='Apa Itu Tanazul Haji? Pengertian & Penjelasannya',
    desc='Tanazul adalah skema layanan haji ketika jamaah tidak bermalam di tenda Mina, tetapi di hotel sekitar Mina dan kembali ke Mina untuk lontar jumrah.',
    intro='Istilah <b>tanazul</b> sering muncul saat membahas haji khusus. Berikut penjelasannya sesuai materi Elharamain Wisata.',
    body=f'''<h2>Pengertian Tanazul</h2>
<p>Tanazul adalah skema layanan di mana jamaah <b>tidak bermalam di tenda Mina</b>, melainkan menginap di hotel sekitar Mina, lalu kembali ke Mina hanya untuk lontar jumrah pada hari-hari tasyrik.</p>
<h2>Kaitannya dengan Jadwal Armuzna</h2>
{table(['Tanggal', 'Kegiatan'], [r for r in HAJI_ITIN if 'Dzulhijjah' in r[0] and r[0][:2] in ('8 ', '9 ', '10', '11', '13')])}
<h2>Istilah Lain yang Perlu Diketahui</h2>
{ul(['<b>Nafar Tsani</b>: tetap di Mina hingga 13 Dzulhijjah.', '<b>Murur</b>: mabit di Muzdalifah dengan melintas tanpa turun dari kendaraan.', '<b>Arbain</b>: 40 waktu shalat di Masjid Nabawi.'])}''',
    faqs=[('Apa itu tanazul?', 'Skema jamaah tidak bermalam di tenda Mina, melainkan di hotel sekitar Mina, dan kembali ke Mina untuk lontar jumrah.'),
          ('Kapan tanazul berlaku?', 'Pada hari-hari tasyrik saat jamaah melontar jumrah.'),
          ('Apakah tenda Mina Elharamain kelas VIP?', 'Ya, tenda Mina & Arafah kelas VIP.')],
    cta=('Konsultasi Haji Plus', "Assalamu'alaikum, saya mau konsultasi haji plus."), rel=[])

art(slug='nafar-tsani-haji', kw='nafar tsani', feat=752,
    title='Nafar Tsani dalam Ibadah Haji: Tetap di Mina Hingga 13 Dzulhijjah',
    seo_title='Nafar Tsani Haji: Pengertian dan Jadwalnya',
    desc='Nafar Tsani adalah program bagi jamaah haji yang tetap tinggal di Mina hingga 13 Dzulhijjah untuk melontar jumrah terakhir sebelum meninggalkan Mina.',
    intro='Setelah wukuf dan hari nahar, jamaah memilih waktu meninggalkan Mina. <b>Nafar Tsani</b> adalah pilihan untuk tetap di Mina hingga 13 Dzulhijjah.',
    body=f'''<h2>Pengertian Nafar Tsani</h2>
<p>Program bagi jamaah yang memilih tetap tinggal di Mina hingga <b>13 Dzulhijjah</b>, melaksanakan lontar jumrah terakhir sebelum meninggalkan Mina.</p>
<h2>Posisinya dalam Rencana Perjalanan Haji</h2>
{table(['Tanggal', 'Kegiatan'], [r for r in HAJI_ITIN if r[0].startswith(('10', '11', '13', '15'))])}
<h2>Tenda Mina Paket Elharamain</h2>
{table(['Paket', 'Maktab VIP', 'Jarak tenda'], [[x[0], x[7], x[8]] for x in HAJI])}''',
    faqs=[('Apa itu nafar tsani?', 'Tetap di Mina hingga 13 Dzulhijjah dan melontar jumrah terakhir.'),
          ('Kapan jamaah kembali ke hotel Makkah?', 'Sesuai rencana perjalanan, 15 Dzulhijjah.'),
          ('Paket dengan tenda terdekat?', 'Platinum, maktab 111 dengan jarak tenda 200 meter.')],
    cta=('Tanya Program Haji', "Assalamu'alaikum, saya mau tanya program haji plus."), rel=['apa-itu-tanazul-haji'])

art(slug='murur-muzdalifah-haji', kw='murur muzdalifah', feat=753,
    title='Murur Muzdalifah: Mabit dengan Melintas Tanpa Turun dari Kendaraan',
    seo_title='Murur Muzdalifah: Pengertian dalam Ibadah Haji',
    desc='Murur Muzdalifah adalah metode mabit dengan melintasi Muzdalifah setelah wukuf tanpa turun dari kendaraan, lalu langsung menuju Mina atau Masjidil Haram.',
    intro='<b>Murur Muzdalifah</b> menjadi istilah yang makin sering dibahas pada penyelenggaraan haji. Berikut penjelasannya.',
    body=f'''<h2>Pengertian Murur</h2>
<p>Metode mabit di Muzdalifah dengan <b>melintas</b> wilayah tersebut setelah wukuf <b>tanpa turun dari kendaraan</b>, langsung menuju Mina atau Masjidil Haram untuk tawaf ifadah.</p>
<h2>Urutan Setelah Wukuf</h2>
{ol(['9 Dzulhijjah: wukuf di Arafah.', '10 Dzulhijjah: Muzdalifah – Ifadah – Mina (lontar jumrah pertama).', '11–12 Dzulhijjah: lontar jumrah ke-2 & ke-3 di Mina.'])}
<h2>Bimbingan dari Masa Tunggu</h2><p>Elharamain Wisata membekali jamaah sejak masa tunggu lewat Manasik Camp 5 hari, termasuk program mabit Muzdalifah.</p>''',
    faqs=[('Apa itu murur?', 'Mabit di Muzdalifah dengan melintas tanpa turun dari kendaraan setelah wukuf.'),
          ('Ke mana setelah murur?', 'Langsung menuju Mina atau Masjidil Haram untuk tawaf ifadah.'),
          ('Apakah ada latihan mabit Muzdalifah?', 'Ya, termasuk program bimbingan Elharamain Wisata.')],
    cta=('Konsultasi Manasik', "Assalamu'alaikum, saya mau tanya manasik haji plus."), rel=['nafar-tsani-haji'])

art(slug='itinerary-haji-plus-1448h', kw='itinerary haji plus', cat=CAT_PAKET_HAJI, feat=751,
    title='Itinerary Haji Plus 1448 H: Rencana Perjalanan dari 2 hingga 26 Dzulhijjah',
    seo_title='Itinerary Haji Plus 1448 H: Jadwal Harian Lengkap',
    desc='Itinerary haji plus 1448 H Elharamain Wisata: berangkat 2 Dzulhijjah, wukuf 9 Dzulhijjah, Mina, tawaf wada, Madinah, tiba di Indonesia 26 Dzulhijjah.',
    intro='Berikut <b>itinerary haji plus</b> Elharamain Wisata untuk musim 1448 H (estimasi keberangkatan 2027), sesuai materi brosur.',
    body=f'''<h2>Rencana Perjalanan Haji Plus</h2>{table(['Tanggal', 'Kegiatan'], HAJI_ITIN)}
<h2>Durasi per Paket</h2>{table(['Paket', 'Durasi'], [[x[0], x[6]] for x in HAJI])}
<p>Paket Gold Arbain lebih panjang (27–28 hari) karena mencakup program Arbain di Madinah.</p>''',
    faqs=[('Kapan jamaah haji plus berangkat?', 'Sesuai rencana perjalanan, 2 Dzulhijjah.'),
          ('Kapan wukuf di Arafah?', '9 Dzulhijjah.'),
          ('Berapa lama di Madinah?', 'Sekitar 21–25 Dzulhijjah untuk ibadah, ziarah, dan city tour.')],
    cta=('Tanya Jadwal Haji Plus', "Assalamu'alaikum, saya mau tanya jadwal haji plus 1448 H."), rel=['nafar-tsani-haji'])

art(slug='maktab-vip-tenda-mina-haji-plus', kw='maktab haji plus', cat=CAT_PAKET_HAJI, feat=752,
    title='Maktab Haji Plus: Nomor Maktab VIP dan Jarak Tenda Mina per Paket',
    seo_title='Maktab Haji Plus: Maktab VIP & Jarak Tenda Mina',
    desc='Maktab haji plus Elharamain Wisata: Silver maktab 116 (900 m), Gold & Gold Arbain 113 (500 m), Platinum 111 (200 m). Tenda Mina & Arafah kelas VIP.',
    intro='Selama di Mina, jarak tenda ke Jamarat sangat berpengaruh pada kenyamanan. Berikut data <b>maktab haji plus</b> per paket Elharamain Wisata.',
    body=f'''<h2>Maktab & Jarak Tenda per Paket</h2>{table(['Paket', 'Maktab VIP', 'Jarak tenda', 'Ber-4'], [[x[0], x[7], x[8], usd(x[1])] for x in HAJI])}
<h2>Fasilitas Tenda</h2>{ul(['Tenda Mina & Arafah kelas VIP.', 'Setiap 1 bus haji didampingi 3 petugas profesional.', 'Layanan kesehatan oleh dokter profesional selama ibadah.'])}''',
    faqs=[('Maktab berapa untuk paket Platinum?', 'Maktab VIP 111 dengan jarak tenda 200 meter, paling dekat.'),
          ('Maktab paket Silver?', 'Maktab VIP 116, jarak tenda 900 meter.'),
          ('Apakah tenda Arafah juga VIP?', 'Ya, tenda Mina & Arafah kelas VIP.')],
    cta=('Tanya Maktab Haji', "Assalamu'alaikum, saya mau tanya maktab haji plus."), rel=['itinerary-haji-plus-1448h'])

art(slug='free-badal-haji', kw='badal haji gratis', feat=753,
    title='Badal Haji Gratis dari Elharamain Wisata: Perlindungan Jika Jamaah Wafat di Masa Tunggu',
    seo_title='Badal Haji Gratis Jika Wafat di Masa Tunggu',
    desc='Elharamain Wisata memberi fasilitas badal haji gratis bila calon jamaah haji plus wafat dalam masa tunggu sebelum berangkat, berlaku sejak brosur 1448 H.',
    intro='Masa tunggu haji plus bertahun-tahun. Untuk memberi ketenangan, Elharamain Wisata menyediakan <b>badal haji gratis</b> bagi calon jamaah yang wafat sebelum berangkat.',
    body=f'''<h2>Ketentuan Free Badal Haji</h2>
{ul(['Berlaku jika calon jamaah <b>wafat dalam masa tunggu</b> sebelum berangkat.', 'Fasilitas badal haji diberikan gratis oleh Elharamain Wisata.', 'Berlaku sejak brosur edisi 1448 H terbit.'])}
<h2>Keunggulan Lain</h2>{ul(['PIHK resmi', 'Bimbingan ibadah intensif sejak masa tunggu', 'DP haji 4.000 USD', 'Transparansi Dana Manfaat', 'Voucher umroh Rp 5.000.000 selama masa tunggu'])}''',
    faqs=[('Apa itu free badal haji?', 'Fasilitas badal haji gratis bila calon jamaah wafat dalam masa tunggu sebelum berangkat.'),
          ('Sejak kapan berlaku?', 'Sejak brosur edisi 1448 H terbit.'),
          ('Apakah perlu biaya tambahan?', 'Tidak, diberikan gratis oleh Elharamain Wisata.')],
    cta=('Tanya Free Badal Haji', "Assalamu'alaikum, saya mau tanya fasilitas free badal haji."), rel=[])

art(slug='manasik-haji-plus-masa-tunggu', kw='manasik haji plus', feat=753,
    title='Manasik Haji Plus Selama Masa Tunggu: Manasik Camp, Kajian Rutin & Online',
    seo_title='Manasik Haji Plus Selama Masa Tunggu',
    desc='Manasik haji plus Elharamain Wisata sejak masa tunggu: manasik camp 5 hari, kajian rutin & bulanan online, hingga latihan tarwiyah dan mabit Muzdalifah.',
    intro='Persiapan haji dimulai jauh sebelum berangkat. Program <b>manasik haji plus</b> Elharamain Wisata mendampingi jamaah selama masa tunggu.',
    body=f'''<h2>Program Bimbingan</h2>{ul(['Manasik Camp 5 hari', 'Kajian rutin 5 waktu shalat', 'Kajian bulanan online (1 bulan sekali)', 'Program tarwiyah dan mabit Muzdalifah', 'Tahajjud bersama'])}
<h2>Saat di Tanah Suci</h2>{ul(['Tilawah & khatam Al-Qur’an selama 23–28 hari di Arab Saudi', 'Ziarah Raudhah dan Makam Nabi Muhammad ﷺ di Madinah'])}''',
    faqs=[('Apa itu Manasik Camp?', 'Program manasik 5 hari untuk jamaah haji plus Elharamain.'),
          ('Apakah ada kajian online?', 'Ya, kajian bulanan online sebulan sekali.'),
          ('Apa program selama di Arab Saudi?', 'Tahajjud bersama, tilawah & khatam Al-Qur\'an, ziarah Raudhah dan Makam Nabi.')],
    cta=('Tanya Program Manasik', "Assalamu'alaikum, saya mau tanya manasik haji plus."), rel=['murur-muzdalifah-haji'])

art(slug='paket-haji-plus-silver-1448h', kw='paket haji plus silver', cat=CAT_PAKET_HAJI, feat=755,
    title='Paket Haji Plus Silver 1448 H: Harga 12.000 USD, Hotel Anjum & Maktab 116',
    seo_title='Paket Haji Plus Silver 1448 H: Harga & Fasilitas',
    desc='Paket haji plus Silver 1448 H Elharamain Wisata: mulai 12.000 USD, Anjum Hotel Makkah, Concorde Dar Alkhair Madinah, maktab VIP 116, 22–23 hari.',
    intro='<b>Paket haji plus Silver</b> adalah pilihan paling terjangkau dari empat paket haji khusus Elharamain Wisata untuk musim 1448 H.',
    body=f'''<h2>Rincian Paket Silver</h2>{haji_card('Silver')}<p>{EST}</p>
<h2>Maskapai</h2><p>Saudia / Qatar / Emirates.</p>
<h2>Cocok untuk Siapa?</h2><p>Jamaah yang ingin haji khusus dengan anggaran paling efisien, tetap dengan hotel Makkah ±350 m dan Madinah ±200 m dari masjid.</p>''',
    faqs=[('Berapa harga paket haji plus Silver?', f'{usd(12000)} (ber-4), {usd(13500)} (ber-3), {usd(15000)} (ber-2), estimasi 2027.'),
          ('Hotel apa yang dipakai?', 'Anjum Hotel di Makkah dan Concorde Dar Alkhair di Madinah.'),
          ('Berapa setoran awalnya?', '4.000 USD untuk pengambilan porsi.')],
    cta=('Daftar Haji Plus Silver', "Assalamu'alaikum, saya mau daftar haji plus Silver."), rel=['maktab-vip-tenda-mina-haji-plus'])

art(slug='paket-haji-plus-gold-1448h', kw='paket haji plus gold', cat=CAT_PAKET_HAJI, feat=756,
    title='Paket Haji Plus Gold 1448 H: Marwa Rotana Depan Masjidil Haram, 15.500 USD',
    seo_title='Paket Haji Plus Gold 1448 H: Harga & Hotel',
    desc='Paket haji plus Gold 1448 H: Marwa Rotana tepat di depan Masjidil Haram, Al-Aqeeq ±50 m dari Nabawi, maktab 113, mulai 15.500 USD (estimasi 2027).',
    intro='<b>Paket haji plus Gold</b> menawarkan hotel Makkah tepat di depan Masjidil Haram dengan harga di tengah jajaran paket Elharamain Wisata.',
    body=f'''<h2>Rincian Paket Gold</h2>{haji_card('Gold')}<p>{EST}</p>
<h2>Gold atau Gold Arbain?</h2><p>Hotel dan maktab sama; Gold Arbain lebih panjang (27–28 hari) karena mencakup program Arbain.</p>''',
    faqs=[('Berapa harga haji plus Gold?', f'{usd(15500)} (ber-4), {usd(17000)} (ber-3), {usd(18500)} (ber-2).'),
          ('Seberapa dekat hotelnya?', 'Marwa Rotana tepat di depan Masjidil Haram; Al-Aqeeq ±50 m dari Masjid Nabawi.'),
          ('Maktab berapa?', 'Maktab VIP 113, jarak tenda 500 meter.')],
    cta=('Daftar Haji Plus Gold', "Assalamu'alaikum, saya mau daftar haji plus Gold."), rel=['program-arbain-haji-plus', 'paket-haji-plus-silver-1448h'])

art(slug='paket-haji-plus-platinum-1448h', kw='paket haji plus platinum', cat=CAT_PAKET_HAJI, feat=751,
    title='Paket Haji Plus Platinum 1448 H: Fairmont, Movenpick & Maktab 111',
    seo_title='Paket Haji Plus Platinum 1448 H: Harga & Fasilitas',
    desc='Paket haji plus Platinum 1448 H Elharamain Wisata: Fairmont Makkah & Movenpick Madinah (±50 m), maktab VIP 111 (tenda 200 m), mulai 20.000 USD.',
    intro='Untuk kenyamanan maksimal, <b>paket haji plus Platinum</b> menempatkan jamaah di hotel depan masjid dan tenda Mina terdekat.',
    body=f'''<h2>Rincian Paket Platinum</h2>{haji_card('Platinum')}<p>{EST}</p>
<h2>Maskapai</h2><p>Saudia / Garuda Indonesia.</p>''',
    faqs=[('Berapa harga haji plus Platinum?', f'{usd(20000)} (ber-4), {usd(22000)} (ber-3), {usd(24000)} (ber-2), estimasi 2027.'),
          ('Hotel apa yang dipakai?', 'Fairmont di Makkah dan Movenpick di Madinah, keduanya ±50 m dari masjid.'),
          ('Apa kelebihan maktab Platinum?', 'Maktab VIP 111 dengan jarak tenda 200 meter, paling dekat.')],
    cta=('Daftar Haji Plus Platinum', "Assalamu'alaikum, saya mau daftar haji plus Platinum."), rel=['paket-haji-plus-gold-1448h'])

art(slug='estimasi-keberangkatan-haji-plus', kw='estimasi keberangkatan haji plus', feat=755,
    title='Estimasi Keberangkatan Haji Plus Elharamain: Antrian Jamaah 2027–2032',
    seo_title='Estimasi Keberangkatan Haji Plus 2027–2032',
    desc='Estimasi keberangkatan haji plus Elharamain Wisata: perkiraan antrian jamaah per tahun 2027–2032 dan cara mengamankan porsi dengan setoran 4.000 USD.',
    intro='Kapan saya berangkat? Berikut data <b>estimasi keberangkatan haji plus</b> berdasarkan antrian jamaah Elharamain Wisata.',
    body=f'''<h2>Estimasi Antrian per Tahun</h2>{table(['Tahun', 'Estimasi antrian'], HAJI_ANTRIAN)}
<p>Angka di atas merupakan estimasi dari materi Elharamain Wisata dan dapat berubah mengikuti kuota resmi pemerintah.</p>
<h2>Nomor Antrian Terpisah</h2><p>Nomor antrian haji khusus di sistem Siskohat terpisah dari haji reguler, dan porsi reguler tidak dapat dipindahkan ke haji plus.</p>''',
    faqs=[('Berapa estimasi antrian 2027?', 'Sekitar 70 jamaah sesuai materi Elharamain Wisata.'),
          ('Apakah porsi reguler bisa pindah ke haji plus?', 'Tidak bisa, alur dan sistem antriannya berbeda.'),
          ('Bagaimana mengamankan porsi?', 'Dengan setoran awal 4.000 USD per jamaah.')],
    cta=('Cek Estimasi Keberangkatan', "Assalamu'alaikum, saya mau cek estimasi keberangkatan haji plus."), rel=[])

art(slug='voucher-umroh-masa-tunggu-haji-plus', kw='voucher umroh', feat=753,
    title='Voucher Umroh Rp 5 Juta untuk Jamaah Haji Plus Selama Masa Tunggu',
    seo_title='Voucher Umroh Rp 5 Juta untuk Jamaah Haji Plus',
    desc='Jamaah haji plus Elharamain Wisata mendapat voucher umroh gratis Rp 5.000.000 selama masa tunggu, bisa dipakai untuk paket umroh musim dingin.',
    intro='Menunggu giliran haji bisa diisi dengan umroh. Jamaah haji plus Elharamain Wisata mendapat <b>voucher umroh</b> senilai Rp 5.000.000 selama masa tunggu.',
    body=f'''<h2>Ketentuan Voucher</h2>{ul(['Nilai voucher Rp 5.000.000.', 'Diberikan selama masa tunggu haji plus.'])}
<h2>Contoh Paket Umroh yang Bisa Dipilih</h2>{paket(lambda p: p['tier'] == 'bronze', cols=('label', 'bulan', 'hari', 'berangkat', 'q'))}''',
    faqs=[('Berapa nilai voucher umroh?', 'Rp 5.000.000.'),
          ('Kapan voucher bisa dipakai?', 'Selama masa tunggu haji plus.'),
          ('Paket umroh termurah saat ini?', f'Bronze Desember 2026 mulai {rp(36500000)}.')],
    cta=('Tanya Voucher Umroh', "Assalamu'alaikum, saya mau tanya voucher umroh jamaah haji plus."), rel=['free-badal-haji'])

art(slug='setoran-awal-haji-plus-4000-usd', kw='setoran awal haji plus', feat=755,
    title='Setoran Awal Haji Plus 4.000 USD: Untuk Apa dan Bagaimana Dikelola?',
    seo_title='Setoran Awal Haji Plus 4.000 USD: Penjelasannya',
    desc='Setoran awal haji plus 4.000 USD untuk pengambilan porsi dikelola BPKH dan menghasilkan Dana Manfaat ±120 USD/tahun sebagai pengurang biaya paket.',
    intro='Semua paket haji plus Elharamain Wisata memiliki <b>setoran awal haji plus</b> yang sama: 4.000 USD per jamaah.',
    body=f'''<h2>Fungsi Setoran Awal</h2><p>Setoran 4.000 USD dipakai untuk <b>pengambilan porsi</b> haji khusus. Dana ini dikelola BPKH melalui instrumen syariah dan bertumbuh sekitar 120 USD per tahun.</p>
<h2>Dana Manfaat Kembali ke Jamaah</h2><p>Di Elharamain Wisata, hasil pengembangan dana manfaat diberikan kembali sebagai pengurang biaya paket.</p>
<h2>Harga Paket Setelah Setoran</h2>{haji_table()}''',
    faqs=[('Berapa setoran awal haji plus?', '4.000 USD per jamaah untuk semua paket.'),
          ('Siapa yang mengelola dana setoran?', 'BPKH melalui instrumen syariah.'),
          ('Berapa dana manfaat per tahun?', 'Sekitar 120 USD per tahun.')],
    cta=('Tanya Setoran Haji Plus', "Assalamu'alaikum, saya mau tanya setoran awal haji plus."), rel=['apa-itu-haji-khusus-haji-plus-dana-manfaat'])

art(slug='kenaikan-biaya-haji-plus-per-tahun', kw='kenaikan biaya haji plus', feat=756,
    title='Kenaikan Biaya Haji Plus per Tahun: Estimasi 4–5% dan Cara Menyikapinya',
    seo_title='Kenaikan Biaya Haji Plus per Tahun: Estimasi 4–5%',
    desc='Kenaikan biaya haji plus diperkirakan 4–5% per tahun dari harga tahun sebelumnya; biaya final diinformasikan 1 tahun sebelum keberangkatan.',
    intro='Harga yang tertera saat mendaftar adalah estimasi. Pahami pola <b>kenaikan biaya haji plus</b> agar perencanaan keuangan lebih matang.',
    body=f'''<h2>Estimasi Kenaikan</h2><p>Menurut materi Elharamain Wisata, biaya paket diperkirakan naik <b>sekitar 4–5% per tahun</b> dari harga tahun sebelumnya, dan biaya final diinformasikan 1 tahun sebelum keberangkatan.</p>
<h2>Harga Estimasi 1448 H</h2>{haji_table()}
<h2>Pengurang Biaya: Dana Manfaat</h2><p>Dana manfaat dari setoran 4.000 USD (±120 USD/tahun) dapat mengurangi pelunasan.</p>''',
    faqs=[('Berapa kenaikan biaya haji plus per tahun?', 'Sekitar 4–5% per tahun dari harga tahun sebelumnya.'),
          ('Kapan biaya final diumumkan?', '1 tahun sebelum keberangkatan.'),
          ('Apa yang bisa mengurangi pelunasan?', 'Dana manfaat dari setoran awal.')],
    cta=('Konsultasi Biaya', "Assalamu'alaikum, saya mau konsultasi biaya haji plus."), rel=['setoran-awal-haji-plus-4000-usd'])

art(slug='pelunasan-haji-plus', kw='pelunasan haji plus', feat=755,
    title='Pelunasan Haji Plus: Waktu, Pengurangan Dana Manfaat & Opsi Pembiayaan Syariah',
    seo_title='Pelunasan Haji Plus: Waktu & Cara Pembayarannya',
    desc='Pelunasan haji plus di Elharamain Wisata dilakukan 6 bulan sebelum keberangkatan, dapat dikurangi Dana Manfaat, dengan opsi pembiayaan syariah Bank Muamalat.',
    intro='Setelah porsi aman, tahap berikutnya adalah <b>pelunasan haji plus</b>. Berikut ketentuannya di Elharamain Wisata.',
    body=f'''<h2>Kapan Pelunasan?</h2><p>Pelunasan dilakukan <b>6 bulan sebelum keberangkatan</b>.</p>
<h2>Dikurangi Dana Manfaat</h2><p>Hasil pengembangan setoran awal (±120 USD/tahun) diberikan kembali sebagai pengurang biaya paket.</p>
<h2>Opsi Pembiayaan Syariah</h2><p>Tersedia pembiayaan melalui Bank Muamalat: biaya admin/ujroh Rp 2.500.000 dan angsuran mulai Rp 1.545.833/bulan (simulasi 72 bulan untuk plafon Rp 77.000.000).</p>''',
    faqs=[('Kapan pelunasan haji plus?', '6 bulan sebelum keberangkatan.'),
          ('Apakah bisa dicicil?', 'Ada opsi pembiayaan syariah melalui Bank Muamalat.'),
          ('Berapa angsuran termurah?', 'Mulai Rp 1.545.833/bulan untuk simulasi 72 bulan plafon Rp 77 juta.')],
    cta=('Konsultasi Pelunasan', "Assalamu'alaikum, saya mau tanya pelunasan haji plus."), rel=['kenaikan-biaya-haji-plus-per-tahun', 'cicilan-haji-plus-simulasi-angsuran-pembiayaan'])

art(slug='rekening-resmi-pembayaran-haji-plus', kw='rekening resmi haji plus', feat=751,
    title='Rekening Resmi Haji Plus Elharamain: Cara Bayar Aman dan Hindari Penipuan',
    seo_title='Rekening Resmi Haji Plus Elharamain Wisata',
    desc='Rekening resmi haji plus Elharamain Wisata: Bank Danamon Syariah IDR & USD a.n. PT Dhiyaa El Haramain El Mubarakah. Transfer ke rekening lain tidak sah.',
    intro='Waspadai penipuan yang mengatasnamakan travel. Berikut <b>rekening resmi haji plus</b> Elharamain Wisata.',
    body=f'''<h2>Rekening Resmi</h2>{table(['Mata uang', 'Bank', 'Nomor rekening'], [['IDR', 'Bank Danamon Syariah', '0037.0716.7775'], ['USD', 'Bank Danamon Syariah', '0037.0716.8161']])}
<p>Atas nama <b>PT Dhiyaa El Haramain El Mubarakah</b>. Pembayaran ke rekening lain tidak sah.</p>
<h2>Tips Aman</h2>{ul(['Konfirmasi nomor rekening ke kantor resmi sebelum transfer.', 'Simpan bukti transfer dan minta kuitansi resmi.', 'Cek legalitas PIHK di situs Kementerian Agama.'])}''',
    faqs=[('Ke rekening mana membayar haji plus?', 'Bank Danamon Syariah a.n. PT Dhiyaa El Haramain El Mubarakah: IDR 0037.0716.7775 atau USD 0037.0716.8161.'),
          ('Apakah boleh transfer ke rekening pribadi?', 'Tidak, hanya rekening resmi atas nama perusahaan yang sah.'),
          ('Bagaimana cek legalitas travel?', 'Melalui situs Kementerian Agama RI; Elharamain terdaftar PIHK No. 846/2020.')],
    cta=('Konfirmasi Rekening', "Assalamu'alaikum, saya mau konfirmasi rekening resmi haji plus."), rel=['pelunasan-haji-plus'])

art(slug='hotel-haji-plus-makkah', kw='hotel haji plus makkah', cat=CAT_PAKET_HAJI, feat=756,
    title='Hotel Haji Plus Makkah: Anjum, Marwa Rotana, dan Fairmont',
    seo_title='Hotel Haji Plus Makkah: Jarak & Paketnya',
    desc='Hotel haji plus Makkah Elharamain Wisata: Anjum (±350 m, Silver), Marwa Rotana (depan Masjidil Haram, Gold), Fairmont (depan masjid, Platinum).',
    intro='Lokasi hotel di Makkah menentukan seberapa mudah jamaah ke Masjidil Haram. Berikut <b>hotel haji plus Makkah</b> per paket.',
    body=f'''<h2>Hotel Makkah per Paket</h2>{table(['Paket', 'Hotel Makkah', 'Ber-4'], [[x[0], x[4], usd(x[1])] for x in HAJI])}
<h2>Dari Makkah ke Madinah</h2><p>Setelah rangkaian haji dan tawaf wada (20 Dzulhijjah), jamaah menuju Madinah sekitar 21–25 Dzulhijjah.</p>''',
    faqs=[('Hotel Makkah paket Silver?', 'Anjum Hotel, ±350 m dari Masjidil Haram.'),
          ('Hotel Makkah paket Gold?', 'Marwa Rotana, tepat di depan Masjidil Haram.'),
          ('Hotel Makkah paket Platinum?', 'Fairmont Hotel, di depan masjid.')],
    cta=('Tanya Hotel Haji Plus', "Assalamu'alaikum, saya mau tanya hotel haji plus."), rel=['paket-haji-plus-platinum-1448h'])

art(slug='hotel-haji-plus-madinah', kw='hotel haji plus madinah', cat=CAT_PAKET_HAJI, feat=755,
    title='Hotel Haji Plus Madinah: Concorde Dar Alkhair, Al-Aqeeq & Movenpick',
    seo_title='Hotel Haji Plus Madinah: Jarak & Paketnya',
    desc='Hotel haji plus Madinah Elharamain Wisata: Concorde Dar Alkhair (±200 m, Silver), Al-Aqeeq (±50 m, Gold), Movenpick (±50 m, Platinum).',
    intro='Fase Madinah diisi ibadah, ziarah Raudhah, dan city tour. Berikut <b>hotel haji plus Madinah</b> di tiap paket Elharamain Wisata.',
    body=f'''<h2>Hotel Madinah per Paket</h2>{table(['Paket', 'Hotel Madinah', 'Durasi'], [[x[0], x[5], x[6]] for x in HAJI])}
<h2>Program di Madinah</h2>{ul(['Ibadah di Masjid Nabawi', 'Ziarah Raudhah & Makam Nabi Muhammad ﷺ', 'City tour Madinah', 'Program Arbain (paket Gold Arbain)'])}''',
    faqs=[('Hotel Madinah paket Silver?', 'Concorde Dar Alkhair, ±200 m dari Masjid Nabawi.'),
          ('Hotel Madinah paket Gold?', 'Al-Aqeeq Hotel, ±50 m.'),
          ('Hotel Madinah paket Platinum?', 'Movenpick Hotel, ±50 m.')],
    cta=('Tanya Hotel Madinah', "Assalamu'alaikum, saya mau tanya hotel Madinah haji plus."), rel=['hotel-haji-plus-makkah'])

art(slug='maskapai-haji-plus', kw='maskapai haji plus', feat=751,
    title='Maskapai Haji Plus Elharamain: Saudia, Qatar, Emirates & Garuda Indonesia',
    seo_title='Maskapai Haji Plus: Saudia, Qatar, Emirates, Garuda',
    desc='Maskapai haji plus Elharamain Wisata: paket Silver memakai Saudia/Qatar/Emirates, paket Platinum memakai Saudia/Garuda Indonesia.',
    intro='Selain hotel, jamaah sering menanyakan <b>maskapai haji plus</b>. Berikut ketentuan per paket sesuai materi Elharamain Wisata.',
    body=f'''<h2>Maskapai per Paket</h2>{table(['Paket', 'Maskapai'], [['Silver', 'Saudia / Qatar / Emirates'], ['Platinum', 'Saudia / Garuda Indonesia'], ['Gold & Gold Arbain', 'Dikonfirmasi saat pendaftaran']])}
<h2>Jadwal Terbang</h2><p>Rencana keberangkatan 2 Dzulhijjah dan kepulangan dari Madinah/Jeddah pada 25 Dzulhijjah, tiba di Indonesia 26 Dzulhijjah.</p>''',
    faqs=[('Maskapai apa untuk paket Silver?', 'Saudia, Qatar, atau Emirates.'),
          ('Maskapai apa untuk paket Platinum?', 'Saudia atau Garuda Indonesia.'),
          ('Kapan pulang ke Indonesia?', 'Tiba 26 Dzulhijjah sesuai rencana perjalanan.')],
    cta=('Tanya Maskapai', "Assalamu'alaikum, saya mau tanya maskapai haji plus."), rel=['itinerary-haji-plus-1448h'])

art(slug='haji-plus-ramah-lansia', kw='haji plus ramah lansia', feat=753,
    title='Haji Plus Ramah Lansia: Pendampingan, Layanan Dokter, dan Pilihan Paket',
    seo_title='Haji Plus Ramah Lansia: Layanan & Tips Memilih',
    desc='Haji plus ramah lansia bersama Elharamain Wisata: 3 petugas per bus, dokter profesional, fasilitas lansia-friendly, dan hotel dekat masjid.',
    intro='Banyak calon jamaah berangkat di usia lanjut. Elharamain Wisata menyiapkan layanan <b>haji plus ramah lansia</b> agar ibadah tetap nyaman.',
    body=f'''<h2>Layanan untuk Lansia</h2>{ul(['Setiap 1 bus haji didampingi 3 petugas profesional.', 'Layanan kesehatan oleh dokter profesional selama ibadah.', 'Fasilitas tambahan untuk jamaah lansia (lansia-friendly).', 'Tenda Mina & Arafah kelas VIP.'])}
<h2>Pilih Hotel dan Tenda Terdekat</h2>{table(['Paket', 'Hotel Makkah', 'Jarak tenda Mina'], [[x[0], x[4], x[8]] for x in HAJI])}''',
    faqs=[('Apakah ada pendamping untuk lansia?', 'Setiap bus didampingi 3 petugas profesional.'),
          ('Apakah ada dokter?', 'Ya, layanan kesehatan oleh dokter profesional selama ibadah.'),
          ('Paket paling nyaman untuk lansia?', 'Platinum: hotel depan masjid dan tenda Mina paling dekat (200 m).')],
    cta=('Konsultasi Haji Lansia', "Assalamu'alaikum, saya mau konsultasi haji plus untuk orang tua."), rel=['maktab-vip-tenda-mina-haji-plus'])

art(slug='wukuf-arafah-haji-plus', kw='wukuf di arafah', feat=752,
    title='Wukuf di Arafah Bersama Haji Plus: Jadwal 9 Dzulhijjah & Tenda VIP',
    seo_title='Wukuf di Arafah: Jadwal & Fasilitas Haji Plus',
    desc='Wukuf di Arafah pada 9 Dzulhijjah adalah puncak ibadah haji. Jamaah haji plus Elharamain Wisata menempati tenda Arafah kelas VIP dengan pendampingan petugas.',
    intro='<b>Wukuf di Arafah</b> pada 9 Dzulhijjah adalah puncak ibadah haji. Berikut posisinya dalam program haji plus Elharamain Wisata.',
    body=f'''<h2>Rangkaian Menuju Wukuf</h2>{table(['Tanggal', 'Kegiatan'], [r for r in HAJI_ITIN if r[0][:2] in ('3–', '8 ', '9 ', '10')])}
<h2>Fasilitas Selama di Arafah</h2>{ul(['Tenda Arafah kelas VIP', 'Pendampingan petugas profesional', 'Layanan kesehatan dokter'])}''',
    faqs=[('Kapan wukuf di Arafah?', '9 Dzulhijjah.'),
          ('Apa yang dilakukan sebelum wukuf?', '8 Dzulhijjah jamaah menuju Mina (Tarwiyah).'),
          ('Ke mana setelah wukuf?', 'Muzdalifah – Ifadah – Mina pada 10 Dzulhijjah.')],
    cta=('Tanya Program Haji', "Assalamu'alaikum, saya mau tanya program haji plus."), rel=['itinerary-haji-plus-1448h', 'murur-muzdalifah-haji'])

art(slug='program-ibadah-haji-plus', kw='program ibadah haji plus', feat=753,
    title='Program Ibadah Haji Plus: Tahajjud, Tilawah & Khatam Al-Qur\'an di Tanah Suci',
    seo_title='Program Ibadah Haji Plus: Tahajjud & Khatam Quran',
    desc='Program ibadah haji plus Elharamain Wisata: tahajjud bersama, tilawah & khatam Al-Qur\'an 23–28 hari, tarwiyah, mabit Muzdalifah, ziarah Raudhah.',
    intro='Selain manasik, Elharamain Wisata menyusun <b>program ibadah haji plus</b> agar waktu di Tanah Suci terisi maksimal.',
    body=f'''<h2>Program Selama di Arab Saudi</h2>{ul(['Tahajjud bersama', 'Tilawah & khatam Al-Qur’an selama 23–28 hari', 'Program tarwiyah', 'Mabit Muzdalifah', 'Ziarah Raudhah dan Makam Nabi Muhammad ﷺ'])}
<h2>Sebelum Berangkat</h2>{ul(['Manasik Camp 5 hari', 'Kajian rutin 5 waktu shalat', 'Kajian bulanan online'])}''',
    faqs=[('Apakah ada target khatam Al-Qur\'an?', 'Ya, program tilawah & khatam selama 23–28 hari di Arab Saudi.'),
          ('Apakah ada tahajjud bersama?', 'Ya, termasuk program ibadah.'),
          ('Kapan ziarah Raudhah?', 'Saat fase Madinah.')],
    cta=('Tanya Program Ibadah', "Assalamu'alaikum, saya mau tanya program ibadah haji plus."), rel=['manasik-haji-plus-masa-tunggu'])

# ============ UMROH di haji.biz (12) ============
def um(**k):
    k.setdefault('cat', CAT_MIX)
    art(**k)


um(slug='jadwal-umroh-november-2026', kw='jadwal umroh november 2026', cover='10_Hari_Riyad_Air_3', cover_alt='Jadwal umroh November 2026 Elharamain Wisata',
   title='Jadwal Umroh November 2026: Musim Sejuk 10 Hari, Berangkat 26 November',
   seo_title='Jadwal Umroh November 2026: Berangkat 26 November',
   desc='Jadwal umroh November 2026 Elharamain Wisata: berangkat 26 November, program Musim Sejuk 10 hari dengan Riyadh Air, Thaif & kereta cepat, mulai Rp 37 juta.',
   intro='Mencari <b>jadwal umroh November 2026</b>? Elharamain Wisata membuka keberangkatan <b>26 November 2026</b> untuk program Musim Sejuk 10 hari.',
   body=f'''<h2>Jadwal dan Harga</h2>{paket(lambda p: p['bulan'] == 'November', cols=('label', 'hari', 'berangkat', 'maskapai', 'q', 't', 'd'))}
<h2>Program Utama</h2>{ul(['Ziarah Madinah dan Makkah', 'Ziarah Thaif dan umroh dari Qarnul Manazil', 'Kereta cepat Madinah–Makkah', 'City tour Jeddah'])}''',
   faqs=[('Kapan umroh November 2026?', '26 November 2026.'), ('Berapa lama programnya?', '10 hari.'), ('Berapa harganya?', 'Mulai Rp 37.000.000 per jamaah (ber-empat).')],
   cta=('Tanya Umroh November', "Assalamu'alaikum, saya mau info umroh November 2026."), rel=[])

um(slug='jadwal-umroh-desember-2026', kw='jadwal umroh desember 2026', cover='3._Desain_Paket_Umroh_Liburan_Akhir_Tahun_Musim_Dingin_By_Saudia_Airlines_Elharamain_Wisata_2026',
   cover_alt='Jadwal umroh Desember 2026 Elharamain Wisata',
   title='Jadwal Umroh Desember 2026: 10 Pilihan Keberangkatan dari 1 hingga 27 Desember',
   seo_title='Jadwal Umroh Desember 2026: 10 Pilihan Paket',
   desc='Jadwal umroh Desember 2026 Elharamain Wisata: 10 paket berangkat 1–27 Desember, Saudia Airlines, program 9 & 12 hari, mulai Rp 36,5 juta.',
   intro='Desember adalah bulan tersibuk. Berikut <b>jadwal umroh Desember 2026</b> Elharamain Wisata, dari awal bulan hingga liburan akhir tahun.',
   body=f'''<h2>Semua Keberangkatan Desember</h2>{paket(lambda p: p['bulan'] == 'Desember', cols=('label', 'hari', 'berangkat', 'makkah', 'q'))}
<h2>Awal vs Akhir Desember</h2><p>Paket awal–pertengahan Desember (1–12 Des) lebih terjangkau; paket eksklusif akhir Desember (21–27 Des) bertepatan dengan libur akhir tahun dan mendapat 2x kereta cepat.</p>''',
   faqs=[('Kapan umroh Desember 2026?', 'Tanggal 1, 7, 8, 9, 11, 12, 21, 22, 23, 26, dan 27 Desember 2026, tergantung paket.'),
         ('Paket Desember termurah?', f'Bronze 8 Desember mulai {rp(36500000)}.'), ('Maskapai apa?', 'Saudia Airlines.')],
   cta=('Tanya Umroh Desember', "Assalamu'alaikum, saya mau info umroh Desember 2026."), rel=['jadwal-umroh-november-2026'])

um(slug='biaya-umroh-2027', kw='biaya umroh 2027', cover='januari_1', cover_alt='Biaya umroh 2027 Elharamain Wisata',
   title='Biaya Umroh 2027: Harga Paket Januari Mulai Rp 37,9 Juta',
   seo_title='Biaya Umroh 2027: Harga Paket Januari Terbaru',
   desc='Biaya umroh 2027 di Elharamain Wisata untuk keberangkatan Januari: Bronze, Silver, Platinum, Premium, Silver & Gold 12 hari, mulai Rp 37,9 juta.',
   intro='Merencanakan umroh awal tahun? Berikut <b>biaya umroh 2027</b> untuk keberangkatan Januari dari brosur Elharamain Wisata.',
   body=f'''<h2>Daftar Harga Januari 2027</h2>{paket(lambda p: p['bulan'] == 'Januari', cols=('label', 'hari', 'berangkat', 'q', 't', 'd'))}
<h2>Asumsi Harga</h2><p>Harga memakai asumsi kurs maksimal Rp 17.000 dan dapat menyesuaikan jika ada kebijakan baru Arab Saudi atau kenaikan kurs signifikan.</p>''',
   faqs=[('Berapa biaya umroh 2027 termurah?', 'Bronze 9 hari Januari mulai Rp 37.900.000 (ber-empat).'),
         ('Paket termahal?', 'Premium dan Gold 12 Hari sekamar berdua, Rp 61.000.000.'), ('Berapa DP-nya?', 'Rp 6.000.000 per jamaah.')],
   cta=('Tanya Biaya Umroh 2027', "Assalamu'alaikum, saya mau info biaya umroh 2027."), rel=['jadwal-umroh-desember-2026'])

um(slug='paket-umroh-gold-12-hari', kw='paket umroh gold', cover='12_hari_januari_3', cover_alt='Paket umroh Gold 12 hari Elharamain Wisata',
   title='Paket Umroh Gold 12 Hari: Marwa Rotana & Al-Aqeeq, Desember & Januari',
   seo_title='Paket Umroh Gold 12 Hari: Jadwal & Harga',
   desc='Paket umroh Gold 12 hari Elharamain Wisata: hotel Marwa Rotana/Movenpick Makkah dan Al-Aqeeq Madinah, berangkat 23 & 27 Des 2026 serta 14, 20, 24 Jan 2027.',
   intro='<b>Paket umroh Gold</b> memadukan program 12 hari dengan hotel Makkah kelas Platinum di pelataran Zamzam Tower.',
   body=f'''<h2>Jadwal & Harga Gold 12 Hari</h2>{paket(lambda p: p['tier'] == 'gold', cols=('label', 'bulan', 'berangkat', 'makkah', 'madinah', 'q', 't', 'd'))}
<h2>Bonus</h2><p>GMC tour malam Jabal Uhud; paket akhir Desember juga 2x kereta cepat.</p>''',
   faqs=[('Kapan paket Gold berangkat?', '23 & 27 Desember 2026 serta 14, 20 & 24 Januari 2027.'),
         ('Hotel paket Gold?', 'Marwa Rotana/Movenpick Makkah dan Al-Aqeeq Madinah.'), ('Harga termurah?', f'Gold 12 Hari Januari mulai {rp(54000000)}.')],
   cta=('Tanya Paket Gold', "Assalamu'alaikum, saya mau info paket umroh Gold 12 hari."), rel=['biaya-umroh-2027'])

um(slug='paket-umroh-silver-12-hari', kw='paket umroh silver 12 hari', cover='12_hari_januari_4', cover_alt='Paket umroh Silver 12 hari Elharamain Wisata',
   title='Paket Umroh Silver 12 Hari: Program Lebih Lama dengan Harga Terjangkau',
   seo_title='Paket Umroh Silver 12 Hari: Jadwal & Harga',
   desc='Paket umroh Silver 12 hari Elharamain Wisata: Anjum Makkah, Al-Aqeeq/Peninsula Madinah, berangkat Desember 2026 & Januari 2027, mulai Rp 41,5 juta.',
   intro='Ingin program 12 hari tanpa biaya setinggi Gold? <b>Paket umroh Silver 12 hari</b> adalah jawabannya.',
   body=f'''<h2>Jadwal & Harga</h2>{paket(lambda p: p['tier'] == 'silver' and p['hari'] == 12, cols=('label', 'bulan', 'berangkat', 'madinah', 'q', 't', 'd'))}
<h2>Hotel</h2>{ul([hotel_line('Anjum'), hotel_line('Al-Aqeeq'), hotel_line('Peninsula Worth')])}''',
   faqs=[('Kapan Silver 12 hari berangkat?', '9 & 27 Desember 2026 serta 13, 14 & 20 Januari 2027.'),
         ('Harga termurah?', f'Silver 12 Hari 9 Desember mulai {rp(41500000)}.'), ('Apa bonusnya?', 'GMC tour malam Jabal Uhud.')],
   cta=('Tanya Silver 12 Hari', "Assalamu'alaikum, saya mau info umroh Silver 12 hari."), rel=['paket-umroh-gold-12-hari'])

um(slug='umroh-hotel-bintang-5', kw='umroh bintang 5', cover=IMG[756], cover_alt='Umroh bintang 5 bersama Elharamain Wisata',
   title='Umroh Bintang 5: Daftar Hotel dan Jaraknya ke Masjidil Haram & Nabawi',
   seo_title='Umroh Bintang 5: Daftar Hotel & Jaraknya',
   desc='Umroh bintang 5 bersama Elharamain Wisata: Anjum, Marwa Rotana, Fairmont, Al-Aqeeq, Movenpick, dan Peninsula Worth. Cek jarak hotel ke masjid.',
   intro='Elharamain Wisata memakai hotel bintang 5 di seluruh paket. Berikut daftar hotel <b>umroh bintang 5</b> beserta jaraknya.',
   body=f'''<h2>Hotel di Makkah</h2>{ul([hotel_line('Anjum'), hotel_line('Marwa Rotana'), hotel_line('Fairmont'), hotel_line('Prestige')])}
<h2>Hotel di Madinah</h2>{ul([hotel_line('Al-Aqeeq'), hotel_line('Movenpick Madinah'), hotel_line('Peninsula Worth')])}
<p>Bila hotel yang ditetapkan penuh, travel berhak mengganti dengan hotel setaraf.</p>''',
   faqs=[('Apakah semua paket bintang 5?', 'Ya, sesuai brosur musim dingin 2026/2027.'),
         ('Hotel Makkah terdekat?', 'Marwa Rotana dan Fairmont di pelataran Zamzam Tower.'), ('Hotel Madinah terdekat?', 'Al-Aqeeq dan Movenpick, ±50 m.')],
   cta=('Tanya Hotel Umroh', "Assalamu'alaikum, saya mau tanya hotel umroh bintang 5."), rel=['biaya-umroh-2027'])

um(slug='miqat-qarnul-manazil', kw='miqat qarnul manazil', cover='fasilitas-ziarah-thaif', cover_alt='Miqat Qarnul Manazil saat ziarah Thaif',
   title='Miqat Qarnul Manazil: Umroh dari Thaif dalam Program Elharamain Wisata',
   seo_title='Miqat Qarnul Manazil: Umroh dari Thaif',
   desc='Miqat Qarnul Manazil di Thaif menjadi titik niat umroh kedua pada program Elharamain Wisata, setelah ziarah Masjid Abdullah bin Abbas dan bukit Al-Hada.',
   intro='Dalam program ziarah Thaif, jamaah mengambil <b>miqat Qarnul Manazil</b> untuk umroh berikutnya.',
   body=f'''<h2>Rangkaian Hari Thaif</h2>{ol(['Ziarah Masjid Abdullah bin Abbas dan Masjid Kuq', 'Penyulingan parfum & mawar', 'Kuliner Nasi Mandi', 'Bukit Al-Hada & cable car', 'Miqat di Masjid Qarnul Manazil, lalu umroh di Masjidil Haram'])}
<h2>Paket yang Termasuk</h2><p>Free city tour Thaif termasuk fasilitas semua paket musim dingin.</p>''',
   faqs=[('Di mana miqat Qarnul Manazil?', 'Di Thaif, pada Masjid Qarnul Manazil.'), ('Umroh ke berapa dari Qarnul Manazil?', 'Umroh tambahan dalam fasilitasi 3x umroh.'), ('Apakah semua paket ke Thaif?', 'Ya, free city tour Thaif termasuk semua paket.')],
   cta=('Tanya Program Thaif', "Assalamu'alaikum, saya mau tanya program Thaif."), rel=[])

um(slug='miqat-jiranah', kw="miqat ji'ranah", cover=IMG[751], cover_alt='Umroh dengan miqat Ji\'ranah',
   title='Miqat Ji\'ranah: Umroh Tambahan Saat Ziarah Kota Makkah',
   seo_title='Miqat Ji\'ranah: Umroh Saat Ziarah Makkah',
   desc='Miqat Ji\'ranah dipakai untuk umroh tambahan saat ziarah kota Makkah (Jabal Tsur, Arafah, Mina) dalam program umroh Elharamain Wisata.',
   intro='Saat ziarah kota Makkah, jamaah Elharamain Wisata mengambil <b>miqat Ji\'ranah</b> untuk umroh tambahan.',
   body=f'''<h2>Rute Ziarah Kota Makkah</h2>{ul(['Jabal Tsur', 'Arafah', 'Muzdalifah', 'Mina', 'Jamarat', 'Miqat di Ji’ranah, melewati Jabal Nur'])}
<h2>Bagian dari Fasilitasi 3x Umroh</h2><p>Umroh dari Ji\'ranah dibimbing dan dapat diikuti dengan Audio Hajj.</p>''',
   faqs=[('Kapan ke Ji\'ranah?', 'Saat hari ziarah kota Makkah.'), ('Apakah dibimbing?', 'Ya, oleh pembimbing dengan Audio Hajj.'), ('Tempat apa lagi yang dikunjungi?', 'Jabal Tsur, Arafah, Muzdalifah, Mina, Jamarat, dan melewati Jabal Nur.')],
   cta=('Tanya Program Makkah', "Assalamu'alaikum, saya mau tanya program ziarah Makkah."), rel=['miqat-qarnul-manazil'])

um(slug='paket-umroh-premium-januari-2027', kw='paket umroh premium', cover='januari_4', cover_alt='Paket umroh Premium Januari 2027 Elharamain Wisata',
   title='Paket Umroh Premium Januari 2027: Fairmont Makkah & Movenpick Madinah',
   seo_title='Paket Umroh Premium Januari 2027: Harga & Bonus',
   desc='Paket umroh Premium Elharamain Wisata: Fairmont Makkah & Movenpick Madinah, berangkat 11 & 31 Januari 2027, bonus Hotel 101 H-1, mulai Rp 52 juta.',
   intro='<b>Paket umroh Premium</b> adalah kelas tertinggi pada jadwal Januari 2027 Elharamain Wisata.',
   body=f'''<h2>Jadwal & Harga</h2>{paket(lambda p: p['tier'] == 'premium', cols=('label', 'berangkat', 'makkah', 'madinah', 'q', 't', 'd'))}
<h2>Bonus</h2>{ul(['H-1 free menginap di Hotel 101', 'Jabal Khandama + golf car sai', 'Abaya & jaket eksklusif', 'GMC tour malam Jabal Uhud'])}''',
   faqs=[('Kapan paket Premium berangkat?', '11 dan 31 Januari 2027.'), ('Hotel paket Premium?', 'Fairmont Makkah dan Movenpick Madinah.'), ('Harga?', 'Rp 52 juta (ber-4), Rp 56 juta (ber-3), Rp 61 juta (ber-2).')],
   cta=('Tanya Paket Premium', "Assalamu'alaikum, saya mau info paket umroh Premium."), rel=['umroh-hotel-bintang-5'])

um(slug='paket-umroh-bronze', kw='paket umroh bronze', cover='januari_2', cover_alt='Paket umroh Bronze Elharamain Wisata',
   title='Paket Umroh Bronze: Pilihan Hemat Hotel Bintang 5, November–Januari',
   seo_title='Paket Umroh Bronze: Jadwal & Harga Terbaru',
   desc='Paket umroh Bronze Elharamain Wisata: pilihan paling hemat dengan hotel bintang 5, berangkat November 2026 – Januari 2027, mulai Rp 36,5 juta.',
   intro='<b>Paket umroh Bronze</b> adalah kelas paling terjangkau di Elharamain Wisata, namun tetap memakai hotel bintang 5 dan program lengkap.',
   body=f'''<h2>Jadwal & Harga Bronze</h2>{paket(lambda p: p['tier'] == 'bronze', cols=('label', 'bulan', 'hari', 'berangkat', 'makkah', 'madinah', 'q'))}
<h2>Tetap Dapat Fasilitas Lengkap</h2>{ul(['Thaif + kereta cepat', 'Fasilitasi umroh sampai 3x', 'Perlengkapan & oleh-oleh eksklusif'])}''',
   faqs=[('Harga paket Bronze termurah?', f'Bronze 8 Desember 2026 mulai {rp(36500000)}.'), ('Apakah Bronze bintang 5?', 'Ya, semua paket bintang 5.'), ('Apa beda Bronze dan Bronze Plus?', 'Bronze Plus memakai hotel Prestige dan jadwal Jumat di Masjidil Haram.')],
   cta=('Tanya Paket Bronze', "Assalamu'alaikum, saya mau info paket umroh Bronze."), rel=['biaya-umroh-2027'])

um(slug='vip-lounge-umroh-soekarno-hatta', kw='vip lounge umroh', cover='fasilitas-vip-lounge', cover_alt='VIP lounge umroh Soekarno-Hatta Elharamain Wisata',
   title='VIP Lounge Umroh Soekarno-Hatta: Titik Kumpul Jamaah Elharamain Wisata',
   seo_title='VIP Lounge Umroh Soekarno-Hatta: Fasilitas Jamaah',
   desc='Jamaah Elharamain Wisata berkumpul di VIP Lounge Umroh Soekarno-Hatta sebelum terbang; airport tax dan handling bandara sudah termasuk paket.',
   intro='Perjalanan dimulai dengan nyaman. Jamaah Elharamain Wisata berkumpul di <b>VIP lounge umroh</b> Bandara Soekarno-Hatta.',
   body=f'''<h2>Fasilitas Bandara yang Termasuk</h2>{ul(['VIP Lounge Umroh Soekarno-Hatta', 'Airport tax & handling bandara', 'Bagasi 35 kg per jamaah'])}
<h2>Hari Pertama</h2><p>{ITIN_9[0]}</p>''',
   faqs=[('Di mana titik kumpul jamaah?', 'VIP Lounge Umroh Bandara Soekarno-Hatta.'), ('Apakah airport tax termasuk?', 'Ya, termasuk handling bandara.'), ('Berapa bagasi?', '35 kg per jamaah.')],
   cta=('Tanya Keberangkatan', "Assalamu'alaikum, saya mau tanya keberangkatan umroh."), rel=['paket-umroh-bronze'])

um(slug='manasik-umroh', kw='manasik umroh', cover='fasilitas-manasik-eksklusif', cover_alt='Manasik umroh eksklusif Elharamain Wisata',
   title='Manasik Umroh Elharamain Wisata: Di Hotel Berbintang dan Dimantapkan di Madinah',
   seo_title='Manasik Umroh: Jadwal & Materi Bimbingan',
   desc='Manasik umroh Elharamain Wisata digelar di hotel berbintang sebelum berangkat, lalu dimantapkan di Madinah; dibimbing asatidz dengan Audio Hajj.',
   intro='Ibadah yang benar dimulai dari ilmu. <b>Manasik umroh</b> Elharamain Wisata dilakukan dua tahap: sebelum berangkat dan di Madinah.',
   body=f'''<h2>Tahap Manasik</h2>{ol(['Manasik umroh di hotel berbintang sebelum keberangkatan.', 'Pemantapan manasik & kajian singkat di Madinah sebelum umroh pertama.'])}
<h2>Pembimbing</h2><p>Dibimbing asatidz seperti Ustadz Dr. Muhammad Tahir Lc MA dan Ustadz Didi Wibawa Lc MA.</p>''',
   faqs=[('Di mana manasik umroh?', 'Di hotel berbintang sebelum berangkat.'), ('Apakah ada manasik di Tanah Suci?', 'Ya, pemantapan manasik di Madinah.'), ('Apakah manasik berbayar?', 'Tidak, termasuk fasilitas paket.')],
   cta=('Tanya Jadwal Manasik', "Assalamu'alaikum, saya mau tanya jadwal manasik umroh."), rel=['vip-lounge-umroh-soekarno-hatta'])
