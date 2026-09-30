"""Data fakta dari brosur resmi (data/brosur/*.pdf) + draft artikel haji 1448 H. Satu-satunya sumber fakta artikel."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAKET = json.load(open(os.path.join(ROOT, 'data', 'paket-umroh.json')))['paket']

HOTEL = {  # jarak sesuai halaman "Fasilitas Hotel" brosur; None = brosur tidak menyebut jarak
    'Anjum': ('Makkah', '±350 meter dari Masjidil Haram'),
    'Marwa Rotana': ('Makkah', 'di pelataran Zamzam Tower'),
    'Fairmont': ('Makkah', 'di pelataran Zamzam Tower'),
    'Movenpick Madinah': ('Madinah', '±50 meter dari Masjid Nabawi'),
    'Al-Aqeeq': ('Madinah', '±50 meter dari Masjid Nabawi'),
    'Peninsula Worth': ('Madinah', '±150 meter dari Masjid Nabawi'),
    'Prestige': ('Makkah', None),
}

ITIN_9 = [  # brosur Desember 2026 (awal & akhir), program 9 hari
    'Berkumpul di VIP Lounge Umroh Soekarno-Hatta, terbang ke Jeddah/Madinah, lalu check-in hotel Madinah.',
    'Tahajjud bersama, ziarah Raudhah, makam Nabi Muhammad ﷺ, Baqi, Tsaqifah Bani Saidah, dan kajian.',
    'Ziarah kota Madinah (Masjid Quba, kebun kurma, Jabal Uhud, Masjid Qiblatain, Masjid Khandaq, Jabal Magnet) dan pemantapan manasik.',
    'Umroh pertama (miqat, thawaf, sai, tahallul), lalu ke Makkah dengan kereta cepat dan check-in hotel.',
    'Acara bebas: i\'tikaf dan amalan sunnah di Masjidil Haram.',
    'Ziarah Thaif: Masjid Abdullah bin Abbas, Masjid Kuq, penyulingan parfum & mawar, kuliner Nasi Mandi, bukit Al-Hada & cable car; umroh kedua dengan miqat di Qarnul Manazil.',
    'Ziarah kota Makkah: Jabal Tsur, Arafah, Muzdalifah, Mina, Jamarat; umroh ketiga dengan miqat di Ji\'ranah, melewati Jabal Nur.',
    'Tahajjud bersama, kajian keislaman, dan thawaf wada; Museum Wahyu dan city tour Jeddah (melewati Masjid Qisash, Corniche bila memungkinkan).',
    'Tiba di Soekarno-Hatta; pembagian air zamzam dan oleh-oleh (album foto, sertifikat umroh, kurma, parfum).',
]
ITIN_12 = [  # brosur Januari 2027, program 12 hari in Madinah – out Jeddah
    'Berkumpul di VIP Lounge Umroh Soekarno-Hatta, terbang ke Madinah, check-in hotel.',
    'Ziarah dalam: Raudhah, makam Nabi Muhammad ﷺ, Baqi, Tsaqifah Bani Saidah.',
    'Tahajjud bersama, kajian Islami, memperbanyak amalan sunnah di Masjid Nabawi.',
    'Ziarah kota Madinah dan pemantapan manasik.',
    'Umroh pertama; ke Makkah dengan kereta cepat, check-in hotel.',
    'Acara bebas: i\'tikaf dan amalan sunnah di Masjidil Haram.',
    'Ziarah kota Makkah; umroh kedua dengan miqat di Ji\'ranah.',
    'Tahajjud bersama dan ibadah di Masjidil Haram.',
    'Ziarah Thaif; umroh ketiga dengan miqat di Qarnul Manazil.',
    'Tahajjud bersama, thawaf sunnah, ibadah di Masjidil Haram.',
    'Thawaf wada, Museum Wahyu, city tour Jeddah.',
    'Tiba di Jakarta; pembagian air zamzam dan oleh-oleh.',
]
ITIN_RIYADH = [  # brosur November 2026 Riyadh Air
    'Berkumpul di VIP Lounge Umroh Soekarno-Hatta pagi hari, terbang Jakarta–Riyadh–Jeddah, lalu bus ke hotel Madinah.',
    'Tahajjud bersama, ziarah Raudhah, makam Nabi ﷺ, Baqi, Tsaqifah Bani Saidah, kajian.',
    'Ziarah kota Madinah dan pemantapan manasik.',
    'Umroh pertama, lalu ke Makkah dengan kereta cepat.',
    'Acara bebas: i\'tikaf dan amalan sunnah di Masjidil Haram.',
    'Ziarah Thaif dan umroh kedua dengan miqat di Qarnul Manazil.',
    'Ziarah kota Makkah dan umroh ketiga dengan miqat di Ji\'ranah.',
    'Tahajjud bersama, kajian, thawaf wada, Museum Wahyu, lalu menginap di hotel Jeddah.',
    'City tour Jeddah, terbang Jeddah–Riyadh–Jakarta (jadwal brosur: pukul 17.20 waktu setempat).',
]

FASILITAS = ['Tiket pesawat PP kelas ekonomi', 'Visa umroh', 'Asuransi perjalanan', 'Perlengkapan umroh eksklusif',
             'Manasik umroh di hotel berbintang', 'VIP Lounge Umroh Soekarno-Hatta', 'Airport tax & handling bandara',
             'Hotel sesuai paket', 'Makan fullboard 3x sehari', 'Transportasi bus terbaru',
             'Pembimbing & mutawwif berpengalaman', 'Program & city tour sesuai itinerary',
             'Kajian dan umroh dengan aplikasi Audio Hajj', 'Fasilitasi umroh sampai 3x', 'Free city tour Thaif',
             'Free ATV & naik unta di Madinah', 'Kuliner Nasi Mandhi + Kunafa', 'Bagasi 35 kg/jamaah',
             'Air zamzam 5 liter/jamaah', 'Album foto perjalanan', 'Sertifikat umroh', 'Gift Elharamain Wisata']
BELUM = ['Paspor', 'Suntik meningitis & polio', 'Keperluan pribadi', 'Kelebihan bagasi',
         'Penyesuaian biaya bila ada kebijakan baru kedua negara (kesehatan, tiket, hotel, visa)']
DOKUMEN = ['Paspor RI berlaku minimal 10 bulan', 'Nama di paspor minimal 2 suku kata', 'Pas foto 4x6 (cetak/digital)',
           'Fotokopi KTP dan KK', 'Fotokopi buku nikah bagi suami-istri', 'Sertifikat vaksin', 'BPJS']
PERLENGKAPAN_PRIA = ['Batik Elharamain', 'Koper bagasi 24 inci', 'Koper kabin 18 inci', 'Cover koper', 'Koko navy ziarah',
                     'Kemeja hitam ziarah', 'Kemeja kepulangan', 'Knitwear pria', 'Ihram eksklusif', 'Sabuk ihram',
                     'Tas pinggang', 'Tas sandal', 'Sajadah traveling', 'Totebag Elharamain', 'Payung lipat',
                     'Buku panduan umroh', 'Buku doa', 'Topi pria', 'Ransel eksklusif', 'Travel bag organizer']
PERLENGKAPAN_WANITA = ['Batik Elharamain', 'Koper bagasi 24 inci', 'Koper kabin 18 inci', 'Cover koper', 'Set mukena abu',
                       'Set mukena hitam', 'Knitwear wanita', 'Scarf abu', 'Scarf hitam', 'Scarf putih biru',
                       'Tas serbaguna', 'Tas sandal', 'Sajadah traveling', 'Totebag Elharamain', 'Payung lipat',
                       'Buku panduan umroh', 'Buku doa', 'Outer ziarah Madinah', 'Sling bag eksklusif',
                       'Travel organizer bag']
OLEH = ['Album foto perjalanan', 'Kurma Ajwa', 'Kurma Sukkari', 'Cokelat', 'Parfum eksklusif', 'Sertifikat umroh',
        'Tumbler', 'Air zamzam 5 liter']
PEMBIMBING = ['Ustadz Dr. Muhammad Tahir Lc MA', 'Ustadz Dr. Abdul Kadir Abu Lc MA', 'Ustadz Ahmad Taqy Hafiedz Lc MPd',
              'Ustadz Ahmad Shobirin Lc MA', 'Ustadz Didi Wibawa Lc MA', 'Ustadz Furqon Abdurrohman Lc MA',
              'Ustadz Sansan Susandi Lc MH', 'Ustadz Idrus Abidin Lc MA', 'Ustadz M. Nur Fathoni Lc MA',
              'Ustadz Zulfahmi Yusuf MPd', 'Ustadz Ahmad Husain Lc MPd', 'Ustadz Samhudi Ahmad Lc MH']
BATAL = [('Setelah booking seat / DP', 'Rp 1.000.000'), ('45 hari sebelum berangkat', '10% biaya paket'),
         ('44–31 hari sebelum berangkat', '25% biaya paket'), ('30–20 hari sebelum berangkat', '50% biaya paket'),
         ('19–10 hari sebelum berangkat', '70% biaya paket'), ('9–0 hari sebelum berangkat', '90% biaya paket')]
REKENING = 'Bank Mandiri 156.001.150.115.4 atau Bank BSI 710.857.755.4 a.n. PT Dhiyaa El Haramain El Mubarakah'

# Haji Plus 1448 H (estimasi berangkat 2027) — sumber: brosur haji via draft artikel "Panduan Lengkap Haji Plus 1448H"
HAJI = [  # nama, ber4, ber3, ber2, makkah, madinah, durasi, maktab, jarak tenda
    ('Silver', 12000, 13500, 15000, 'Anjum Hotel (±350 m)', 'Concorde Dar Alkhair (±200 m)', '22–23 hari', '116', '900 m'),
    ('Gold', 15500, 17000, 18500, 'Marwa Rotana (depan Masjidil Haram)', 'Al-Aqeeq Hotel (±50 m)', '22–23 hari', '113', '500 m'),
    ('Gold Arbain', 17000, 18500, 20000, 'Marwa Rotana (depan Masjidil Haram)', 'Al-Aqeeq Hotel (±50 m)', '27–28 hari', '113', '500 m'),
    ('Platinum', 20000, 22000, 24000, 'Fairmont Hotel (depan masjid, ±50 m)', 'Movenpick Hotel (±50 m)', '22–23 hari', '111', '200 m'),
]
HAJI_ITIN = [('2 Dzulhijjah', 'Keberangkatan dari Indonesia'),
             ('3–7 Dzulhijjah', 'Tiba di Makkah, ibadah umroh & pemantapan manasik haji'),
             ('8 Dzulhijjah', 'Menuju Mina (Tarwiyah)'), ('9 Dzulhijjah', 'Wukuf di Arafah'),
             ('10 Dzulhijjah', 'Muzdalifah – Ifadah – Mina (lontar jumrah pertama)'),
             ('11–12 Dzulhijjah', 'Mina, lontar jumrah ke-2 & ke-3'),
             ('13 Dzulhijjah', 'Nafar Tsani (bagi yang memilih), lontar jumrah ke-4'),
             ('15 Dzulhijjah', 'Kembali ke hotel Makkah'), ('20 Dzulhijjah', 'Tawaf Wada'),
             ('21–25 Dzulhijjah', 'Madinah: ibadah, ziarah, city tour'),
             ('25 Dzulhijjah', 'Kepulangan Madinah/Jeddah – Jakarta'), ('26 Dzulhijjah', 'Tiba kembali di Indonesia')]
HAJI_ANTRIAN = [('2027', '70 jamaah'), ('2028', '120 jamaah'), ('2029', '240 jamaah'), ('2030', '450 jamaah'),
                ('2031', '550 jamaah'), ('2032', '700 jamaah')]
