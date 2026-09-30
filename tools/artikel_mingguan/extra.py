"""Bagian penjelasan unik per artikel (tanpa fakta baru di luar brosur) + blok pendukung per jenis artikel."""
from data import FASILITAS, HAJI, ITIN_9
from render import haji_table, ol, ul, usd

X = {
# ---------------- elharamain.id ----------------
'perbandingan-paket-umroh-bronze-silver-platinum': ('Tips Membandingkan Paket Secara Adil', '''<p>Saat membandingkan paket, jangan hanya melihat angka termurah. Perhatikan tiga hal: jarak hotel ke masjid, durasi program, dan fasilitas tambahan. Selisih harga antar kelas biasanya mencerminkan lokasi hotel di Makkah, karena di sanalah jamaah paling sering bolak-balik untuk shalat lima waktu dan thawaf.</p>
<p>Bagi jamaah lansia atau keluarga dengan anak, hotel yang lebih dekat bisa menghemat tenaga untuk ibadah. Sebaliknya, jamaah muda yang terbiasa berjalan kaki bisa memilih kelas Bronze atau Silver dan mengalokasikan anggaran untuk kamar yang lebih lega. Apa pun kelasnya, program inti seperti ziarah Thaif, kereta cepat, dan bimbingan umroh tetap sama.</p>'''),
'umroh-riyadh-air-november-2026': ('Mengapa Memilih Umroh di Bulan November?', '''<p>November berada di awal musim sejuk, sebelum puncak keramaian liburan akhir tahun. Bagi jamaah yang fleksibel soal cuti, jadwal ini memberi kesempatan beribadah dengan suasana yang relatif lebih lapang dibanding pekan-pekan liburan sekolah.</p>
<p>Program Riyadh Air juga menjadi pilihan bagi jamaah yang ingin merasakan maskapai baru Arab Saudi. Karena rutenya melalui Riyadh, siapkan barang bawaan kabin yang ringkas dan patuhi arahan tour leader saat transit. Kuota satu tanggal keberangkatan terbatas, sehingga pendaftaran lebih awal sangat disarankan.</p>'''),
'umroh-akhir-tahun-2026': ('Persiapan Umroh Bersama Keluarga di Akhir Tahun', '''<p>Umroh akhir tahun sering diikuti keluarga dengan anak usia sekolah. Pastikan paspor seluruh anggota keluarga masih berlaku minimal 10 bulan dan nama di paspor minimal dua suku kata. Urus dokumen sejak jauh hari karena antrean kantor imigrasi biasanya meningkat menjelang musim liburan.</p>
<p>Untuk rombongan empat orang, kamar quad menjadi pilihan paling hemat. Jika jumlah anggota ganjil, pertimbangkan kamar triple atau double agar tidak perlu upgrade mendadak. Diskusikan juga pilihan program 9 atau 12 hari dengan jadwal masuk sekolah anak.</p>'''),
'syarat-umroh-dokumen': ('Kesalahan Umum Saat Menyiapkan Dokumen', '''<p>Kesalahan paling sering adalah paspor yang masa berlakunya mepet atau nama yang hanya satu kata. Keduanya bisa menghambat proses visa. Periksa juga kesesuaian ejaan nama di paspor, KTP, dan KK, karena data yang tidak konsisten memperlambat verifikasi.</p>
<p>Simpan salinan digital seluruh dokumen di ponsel dan bawa fotokopi cadangan saat berangkat. Untuk pasangan suami-istri, jangan lupa fotokopi buku nikah. Bila ragu, kirim foto dokumen ke kantor Elharamain Wisata terdekat untuk dicek sebelum membayar DP.</p>'''),
'cara-daftar-umroh-dp-6-juta': ('Tips Agar Pendaftaran Lancar', '''<p>Tentukan dulu jadwal keberangkatan yang realistis dengan cuti kerja atau libur sekolah, lalu hitung mundur 35 hari untuk batas pelunasan. Dengan begitu Anda tahu kapan dana harus siap. Simpan bukti transfer DP dan pelunasan dengan rapi.</p>
<p>Selalu pastikan rekening tujuan atas nama PT Dhiyaa El Haramain El Mubarakah. Penipuan yang mengatasnamakan travel umroh kerap memakai rekening pribadi. Jika menerima nomor rekening berbeda, konfirmasi langsung ke kantor resmi sebelum mentransfer.</p>'''),
'harga-umroh-quad-triple-double': ('Menghitung Anggaran Keluarga', '''<p>Untuk keluarga, total biaya dihitung dari harga per jamaah dikali jumlah anggota. Rombongan empat orang yang memilih kamar quad akan membayar harga terendah per orang. Jika pasangan suami-istri ingin privasi, kamar double memberi ruang lebih walau biaya per orang lebih tinggi.</p>
<p>Ingat pula biaya di luar paket seperti paspor, vaksin meningitis, dan keperluan pribadi. Menyiapkan dana cadangan membuat perjalanan lebih tenang. Konsultasikan kombinasi kamar terbaik dengan tim Elharamain Wisata sebelum membayar DP.</p>'''),
'itinerary-umroh-9-hari': ('Cara Memaksimalkan Program 9 Hari', '''<p>Program 9 hari cukup padat, sehingga manajemen energi penting. Manfaatkan hari bebas di Makkah untuk i'tikaf dan beristirahat di sela ibadah. Tidur lebih awal pada malam sebelum jadwal tahajjud bersama agar tubuh tetap bugar.</p>
<p>Bawa tas kecil berisi air minum, sajadah traveling, dan obat pribadi saat ziarah. Ikuti arahan pembimbing melalui Audio Hajj agar tidak tertinggal rombongan, terutama ketika umroh dan ziarah kota berlangsung di tempat yang ramai.</p>'''),
'umroh-12-hari': ('Siapa yang Cocok dengan Umroh 12 Hari?', '''<p>Program 12 hari cocok untuk jamaah yang ingin ritme lebih santai, misalnya lansia, jamaah yang baru pertama kali umroh, atau mereka yang ingin memperbanyak i'tikaf di Masjidil Haram. Tambahan hari memberi jeda istirahat di antara kegiatan ziarah.</p>
<p>Walau durasinya lebih panjang, selisih harga dibanding program 9 hari tidak terlalu jauh untuk kelas yang sama. Pertimbangkan pula ketersediaan cuti, karena program 12 hari membutuhkan waktu libur lebih lama.</p>'''),
'ziarah-madinah-saat-umroh': ('Adab Selama Ziarah di Madinah', '''<p>Madinah adalah kota Rasulullah ﷺ, sehingga jamaah dianjurkan menjaga adab: berbicara pelan, tidak berdesakan, dan mengikuti arahan petugas masjid. Saat berziarah ke makam Nabi, ucapkan salam dengan tenang lalu lanjutkan perjalanan agar jamaah lain juga mendapat kesempatan.</p>
<p>Gunakan pakaian yang nyaman dan alas kaki yang mudah dilepas. Ziarah kota berlangsung cukup lama, jadi bawa air minum dan jaga stamina sebelum berangkat ke Makkah untuk umroh pertama.</p>'''),
'ziarah-makkah-saat-umroh': ('Mengambil Pelajaran dari Tempat Bersejarah', '''<p>Jabal Tsur mengingatkan kisah hijrah Rasulullah ﷺ, sementara Arafah, Muzdalifah, dan Mina adalah lokasi puncak ibadah haji. Mengunjungi tempat-tempat ini saat umroh membantu jamaah memahami sejarah Islam dan menjadi bekal bila kelak berangkat haji.</p>
<p>Pembimbing biasanya menjelaskan sejarah setiap lokasi selama perjalanan. Dengarkan melalui Audio Hajj agar penjelasan tetap jelas meski berada di dalam bus atau area terbuka yang ramai.</p>'''),
'umroh-plus-thaif': ('Mengapa Thaif Istimewa?', '''<p>Thaif dikenal sebagai kota pegunungan dengan udara lebih sejuk dibanding Makkah. Kota ini juga terkait dengan perjalanan dakwah Rasulullah ﷺ, sehingga kunjungan ke Thaif menjadi momen tadabbur sejarah sekaligus rekreasi ringan.</p>
<p>Siapkan jaket tipis karena udara di area perbukitan bisa terasa dingin, terutama pada musim dingin. Karena rangkaian hari ini juga ditutup dengan umroh, tetap jaga energi dan kebersihan pakaian ihram yang dibawa.</p>'''),
'kereta-cepat-haramain-umroh': ('Keuntungan Naik Kereta Cepat', '''<p>Dibanding perjalanan darat panjang dengan bus, kereta cepat membuat waktu tempuh Madinah–Makkah lebih singkat sehingga jamaah tiba di hotel dengan kondisi lebih segar. Ini penting karena jamaah biasanya langsung bersiap untuk rangkaian umroh.</p>
<p>Atur barang bawaan agar koper besar sudah ditangani sesuai arahan petugas, dan bawa tas kecil berisi keperluan ibadah. Ikuti instruksi tour leader saat naik dan turun kereta agar rombongan tetap bersama.</p>'''),
'umroh-3-kali-satu-perjalanan': ('Menjaga Kondisi Tubuh untuk 3 Kali Umroh', '''<p>Tiga kali umroh dalam satu perjalanan adalah kesempatan berharga, namun membutuhkan stamina. Atur waktu tidur, minum air cukup, dan gunakan alas kaki yang nyaman saat sai. Jamaah lansia bisa berkonsultasi dengan pembimbing mengenai kemampuan fisik sebelum umroh tambahan.</p>
<p>Niatkan setiap umroh dengan tenang dan ikuti bacaan pembimbing. Umroh tambahan sering diniatkan untuk orang tua atau keluarga yang telah wafat, sesuai pendapat ulama yang membolehkannya; tanyakan kepada pembimbing untuk penjelasan lebih lengkap.</p>'''),
'hotel-anjum-makkah': ('Tips Menginap di Hotel yang Berjarak ±350 Meter', '''<p>Jarak sekitar 350 meter umumnya dapat ditempuh berjalan kaki. Berangkat lebih awal sebelum waktu shalat membantu mendapatkan tempat di dalam masjid, terutama menjelang shalat Jumat dan Maghrib yang ramai.</p>
<p>Kenali rute dari hotel ke pintu masjid pada hari pertama bersama tour leader, lalu catat nomor kamar dan nama hotel di ponsel. Kebiasaan kecil ini mencegah jamaah tersesat saat kembali dari masjid.</p>'''),
'hotel-marwa-rotana-makkah': ('Keuntungan Hotel di Pelataran Zamzam Tower', '''<p>Hotel di kawasan Zamzam Tower memudahkan jamaah bolak-balik ke Masjidil Haram, sehingga waktu dapat dimaksimalkan untuk ibadah. Keunggulan ini paling terasa bagi jamaah lansia dan keluarga yang ingin sering kembali ke kamar untuk beristirahat.</p>
<p>Karena lokasinya strategis, kamar di kawasan ini sering penuh. Sesuai ketentuan brosur, bila hotel yang ditetapkan tidak tersedia, jamaah akan ditempatkan di hotel setaraf.</p>'''),
'hotel-fairmont-makkah-umroh': ('Siapa yang Cocok dengan Paket Premium?', '''<p>Paket Premium cocok untuk jamaah yang memprioritaskan kenyamanan maksimal: hotel di kawasan Zamzam Tower di Makkah dan hotel dekat Masjid Nabawi di Madinah, ditambah berbagai bonus. Pilihan ini banyak diminati keluarga yang mengajak orang tua.</p>
<p>Kuota paket Premium hanya tersedia pada dua tanggal keberangkatan, sehingga pendaftaran lebih awal sangat disarankan.</p>'''),
'hotel-movenpick-madinah': ('Memanfaatkan Waktu di Madinah', '''<p>Dengan hotel yang dekat, jamaah bisa mengikuti shalat berjamaah di Masjid Nabawi tanpa terburu-buru. Gunakan waktu luang untuk membaca Al-Qur'an dan berdzikir di masjid, serta mengikuti kajian yang dijadwalkan pembimbing.</p>
<p>Musim dingin membuat pagi dan malam di Madinah terasa sejuk; siapkan pakaian hangat dari perlengkapan yang dibagikan travel.</p>'''),
'hotel-al-aqeeq-madinah': ('Kenapa Al-Aqeeq Banyak Dipilih?', '''<p>Kombinasi jarak dekat dan harga paket yang beragam menjadikan Al-Aqeeq pilihan fleksibel: tersedia di kelas Bronze hingga Gold. Jamaah dengan anggaran berbeda tetap bisa menginap dekat Masjid Nabawi.</p>
<p>Untuk kenyamanan, simpan kartu hotel dan catat jalur tercepat ke pintu masjid terdekat pada hari pertama.</p>'''),
'hotel-peninsula-worth-madinah': ('Tips Memilih Paket Desember yang Hemat', '''<p>Paket dengan Peninsula Worth umumnya berada di kelas harga terjangkau bulan Desember. Bila ingin lebih dekat, bandingkan dengan paket yang memakai Al-Aqeeq dan hitung selisih harganya.</p>
<p>Berjalan kaki sekitar 150 meter tetap nyaman bagi sebagian besar jamaah, apalagi di musim dingin. Pastikan membawa alas kaki yang nyaman dan tas kecil untuk sajadah.</p>'''),
'perlengkapan-umroh-pria': ('Tips Packing untuk Jamaah Pria', '''<p>Manfaatkan koper kabin untuk barang yang dibutuhkan di perjalanan, seperti ihram cadangan, obat, dan pakaian ganti. Koper bagasi dipakai untuk pakaian harian dan perlengkapan lain. Ingat batas bagasi 35 kg termasuk oleh-oleh saat pulang.</p>
<p>Latih cara memakai ihram dan sabuk ihram sebelum berangkat, terutama bagi yang baru pertama kali umroh. Pembimbing akan menjelaskan tata caranya saat manasik.</p>'''),
'perlengkapan-umroh-wanita': ('Tips Packing untuk Jamaah Wanita', '''<p>Siapkan satu set mukena dan scarf di tas kecil agar mudah dipakai saat tiba di masjid. Knitwear dan outer berguna saat udara sejuk, terutama pagi hari di Madinah dan saat ziarah ke Thaif.</p>
<p>Pisahkan pakaian untuk ziarah dan untuk ibadah di masjid agar tidak repot. Perhatikan pula batas bagasi 35 kg ketika menambah oleh-oleh pribadi.</p>'''),
'oleh-oleh-umroh': ('Belanja Oleh-oleh Tambahan dengan Bijak', '''<p>Karena oleh-oleh utama sudah disiapkan, jamaah tidak perlu menghabiskan banyak waktu berbelanja dan bisa fokus beribadah. Jika ingin membeli tambahan, lakukan di sela waktu bebas dan perhatikan berat bagasi.</p>
<p>Air zamzam 5 liter dibagikan di bandara kepulangan, jadi tidak perlu dimasukkan ke koper sendiri.</p>'''),
'ketentuan-pembatalan-reschedule-umroh': ('Cara Menghindari Biaya Pembatalan', '''<p>Pilih tanggal keberangkatan yang benar-benar pasti sebelum membayar DP. Jika ada kemungkinan perubahan, sampaikan permintaan reschedule sedini mungkin, minimal 40 hari sebelum keberangkatan, agar masih dapat dilayani.</p>
<p>Simpan salinan ketentuan pendaftaran dan bukti pembayaran. Bila ragu, konsultasikan kondisi Anda dengan kantor Elharamain Wisata sebelum mengambil keputusan.</p>'''),
'umroh-saudia-airlines-direct-flight': ('Keuntungan Penerbangan Langsung', '''<p>Penerbangan langsung mengurangi waktu tunggu transit sehingga jamaah tiba dalam kondisi lebih segar. Ini penting karena setibanya di Tanah Suci jamaah segera memulai rangkaian ibadah.</p>
<p>Patuhi batas bagasi 35 kg dan simpan dokumen penting di tas kabin. Tour leader akan mendampingi proses check-in rombongan di bandara.</p>'''),
'umroh-madinah-first-atau-makkah-first': ('Pertimbangan Memilih Rute', '''<p>Madinah First memberi waktu adaptasi di kota yang lebih tenang sebelum rangkaian umroh. Makkah First cocok bagi yang ingin segera menunaikan umroh begitu tiba. Keduanya sama baiknya; pilih sesuai kondisi fisik, tanggal yang tersedia, dan anggaran.</p>
<p>Perhatikan pula hotel dan harga masing-masing paket, karena rute berbeda biasanya dipasangkan dengan hotel yang berbeda.</p>'''),
'city-tour-jeddah-umroh': ('Tips di Hari Terakhir', '''<p>Hari terakhir biasanya diisi thawaf wada, city tour, lalu ke bandara. Pastikan koper sudah dikemas malam sebelumnya dan barang penting ada di tas kabin agar tidak terburu-buru.</p>
<p>Gunakan city tour sebagai momen santai bersama rombongan setelah rangkaian ibadah yang padat.</p>'''),
'program-tahajjud-dan-kajian-umroh': ('Manfaat Ibadah Berjamaah', '''<p>Tahajjud dan kajian bersama membantu jamaah menjaga semangat ibadah selama di Tanah Suci. Suasana berjamaah juga memudahkan jamaah yang baru pertama kali umroh untuk belajar dari pembimbing dan sesama jamaah.</p>
<p>Siapkan diri dengan tidur lebih awal dan bawa mushaf atau aplikasi Al-Qur'an untuk memanfaatkan waktu sebelum Subuh.</p>'''),
'audio-hajj-umroh': ('Tips Menggunakan Audio Hajj', '''<p>Pastikan perangkat terisi daya sebelum berangkat ke masjid dan simpan di saku yang mudah dijangkau. Uji suara sebelum rangkaian umroh dimulai agar tidak tertinggal bacaan.</p>
<p>Bila terpisah dari rombongan, tetap ikuti arahan melalui audio dan menuju titik kumpul yang telah disepakati.</p>'''),
'bonus-paket-umroh-platinum': ('Apakah Bonus Sepadan dengan Selisih Harga?', '''<p>Selisih harga Platinum dibanding Silver mencakup hotel di kawasan Zamzam Tower dan sejumlah bonus. Bagi jamaah yang mengutamakan kenyamanan dan kedekatan ke Masjidil Haram, paket ini sering menjadi pilihan paling masuk akal.</p>
<p>Bonus dapat berbeda antar jadwal, jadi selalu cek tabel di atas sesuai tanggal keberangkatan yang Anda pilih.</p>'''),
'tips-umroh-musim-dingin': ('Menjaga Kesehatan Selama Perjalanan', '''<p>Perubahan suhu antara ruangan ber-AC dan udara luar bisa memicu flu. Minum air cukup, istirahat teratur, dan bawa obat pribadi. Konsultasikan kondisi kesehatan dengan dokter sebelum berangkat, terutama bagi jamaah lansia.</p>
<p>Jangan lupa suntik meningitis dan polio yang menjadi biaya di luar paket.</p>'''),
'umroh-bronze-plus-jumat-di-masjidil-haram': ('Keutamaan Shalat Jumat di Masjidil Haram', '''<p>Shalat Jumat di Masjidil Haram menjadi pengalaman yang dirindukan banyak jamaah. Datang lebih awal karena masjid sangat penuh menjelang waktu Jumat. Bawa sajadah dan air minum.</p>
<p>Paket ini cocok bagi yang ingin pengalaman tersebut dengan anggaran kelas Bronze.</p>'''),
'fasilitas-paket-umroh': ('Membaca Fasilitas Sebelum Membandingkan Harga', '''<p>Dua paket dengan harga mirip bisa berbeda jauh isinya. Periksa apakah visa, asuransi, perlengkapan, city tour, kuliner, dan bagasi sudah termasuk. Fasilitas yang lengkap mengurangi biaya tak terduga di perjalanan.</p>
<p>Simpan daftar ini dan cocokkan dengan brosur saat berkonsultasi dengan tim Elharamain Wisata.</p>'''),
'kuliner-arab-saudi-saat-umroh': ('Tips Makan Selama di Tanah Suci', '''<p>Nikmati kuliner khas secukupnya dan tetap jaga pola makan agar stamina terjaga. Minum air cukup, terutama setelah ziarah dan umroh.</p>
<p>Bagi jamaah dengan kebutuhan diet khusus, sampaikan kepada tour leader sejak awal.</p>'''),
'pembimbing-umroh-elharamain-wisata': ('Mengapa Pembimbing Itu Penting?', '''<p>Pembimbing memastikan tata cara ibadah sesuai tuntunan dan membantu jamaah memahami makna setiap rangkaian. Bimbingan yang baik membuat ibadah lebih tenang dan khusyuk.</p>
<p>Jangan ragu bertanya kepada pembimbing selama manasik maupun di Tanah Suci.</p>'''),
'gmc-tour-malam-jabal-uhud': ('Mengenang Sejarah Uhud', '''<p>Jabal Uhud adalah lokasi Perang Uhud yang sarat pelajaran tentang ketaatan dan kesabaran. Kunjungan malam memberi suasana berbeda dan kesempatan merenungkan sejarah bersama rombongan.</p>
<p>Kenakan pakaian hangat karena udara malam di musim dingin terasa sejuk.</p>'''),
# ---------------- haji.biz ----------------
'program-arbain-haji-plus': ('Mempersiapkan Diri untuk Program Arbain', '''<p>Menjaga 40 waktu shalat berjamaah berturut-turut membutuhkan disiplin dan stamina. Atur waktu istirahat di antara shalat dan manfaatkan kedekatan hotel dengan Masjid Nabawi.</p>
<p>Program ini cocok bagi jamaah yang ingin memperpanjang waktu di Madinah setelah rangkaian haji selesai.</p>'''),
'apa-itu-tanazul-haji': ('Hal yang Perlu Ditanyakan ke Penyelenggara', '''<p>Sebelum mendaftar, tanyakan skema layanan selama hari-hari tasyrik, termasuk lokasi menginap dan jadwal lontar jumrah. Informasi ini membantu jamaah menyiapkan fisik dan barang bawaan.</p>
<p>Ikuti manasik dengan saksama agar memahami setiap istilah dan alur ibadah haji.</p>'''),
'nafar-tsani-haji': ('Nafar Tsani dan Persiapan Fisik', '''<p>Tinggal lebih lama di Mina berarti jamaah perlu menjaga kondisi tubuh. Pembimbing akan menjelaskan pilihan yang sesuai dengan kondisi masing-masing jamaah.</p>
<p>Pelajari istilah-istilah ini sejak masa tunggu melalui program bimbingan Elharamain Wisata.</p>'''),
'murur-muzdalifah-haji': ('Memahami Istilah Sejak Masa Tunggu', '''<p>Istilah seperti murur, tanazul, dan nafar tsani lebih mudah dipahami bila dipelajari jauh hari. Program manasik dan kajian selama masa tunggu membantu jamaah siap secara ilmu dan mental.</p>'''),
'itinerary-haji-plus-1448h': ('Menyiapkan Diri Mengikuti Jadwal', '''<p>Jadwal haji sangat terikat tanggal Dzulhijjah, sehingga jamaah perlu siap sejak awal keberangkatan. Latih stamina dengan berjalan kaki rutin selama masa tunggu dan ikuti manasik camp.</p>
<p>Detail teknis dapat menyesuaikan kebijakan resmi pemerintah Arab Saudi dan Indonesia pada tahun berjalan.</p>'''),
'maktab-vip-tenda-mina-haji-plus': ('Pertimbangan Memilih Paket Berdasarkan Maktab', '''<p>Semakin dekat tenda ke Jamarat, semakin ringan perjalanan saat lontar jumrah. Bagi jamaah lansia, faktor ini sering menjadi pertimbangan utama selain hotel.</p>'''),
'free-badal-haji': ('Ketenangan Selama Masa Tunggu', '''<p>Masa tunggu yang panjang membuat banyak keluarga khawatir. Fasilitas badal haji gratis memberi ketenangan bahwa niat ibadah tetap tertunaikan. Tanyakan detail syaratnya saat pendaftaran.</p>'''),
'manasik-haji-plus-masa-tunggu': ('Mengapa Bimbingan Sejak Masa Tunggu?', '''<p>Ibadah haji memiliki banyak rukun dan wajib yang perlu dipahami. Belajar bertahap selama masa tunggu membuat jamaah lebih siap dan tenang saat berangkat.</p>'''),
'paket-haji-plus-silver-1448h': ('Tips Memilih Paket Silver', '''<p>Paket Silver tepat bagi yang ingin kepastian keberangkatan haji khusus dengan anggaran paling efisien. Pertimbangkan jarak tenda 900 meter bila ada anggota keluarga lansia.</p>'''),
'paket-haji-plus-gold-1448h': ('Siapa yang Cocok dengan Paket Gold?', '''<p>Paket Gold menyeimbangkan kenyamanan hotel depan Masjidil Haram dengan harga di bawah Platinum. Pilihan ini banyak diminati pasangan dan keluarga.</p>'''),
'paket-haji-plus-platinum-1448h': ('Kenyamanan Maksimal untuk Lansia', '''<p>Hotel depan masjid dan tenda terdekat membuat paket Platinum ideal bagi jamaah lansia atau yang memiliki keterbatasan fisik.</p>'''),
'estimasi-keberangkatan-haji-plus': ('Mendaftar Lebih Awal', '''<p>Semakin awal mendaftar, semakin cepat mendapatkan nomor porsi. Konsultasikan estimasi keberangkatan terbaru dengan kantor Elharamain Wisata.</p>'''),
'voucher-umroh-masa-tunggu-haji-plus': ('Memanfaatkan Masa Tunggu', '''<p>Umroh selama masa tunggu dapat menjadi latihan fisik dan mental sebelum haji, sekaligus mengenal suasana Makkah dan Madinah.</p>'''),
'setoran-awal-haji-plus-4000-usd': ('Tips Menyiapkan Setoran', '''<p>Siapkan setoran dalam USD atau IDR sesuai ketentuan dan transfer hanya ke rekening resmi. Simpan bukti setoran dengan baik.</p>'''),
'kenaikan-biaya-haji-plus-per-tahun': ('Merencanakan Tabungan Haji', '''<p>Sisihkan dana secara rutin selama masa tunggu dengan memperhitungkan estimasi kenaikan. Dana manfaat dapat menjadi pengurang biaya saat pelunasan.</p>'''),
'pelunasan-haji-plus': ('Persiapan Menjelang Pelunasan', '''<p>Siapkan dana sejak jauh hari dan pantau informasi biaya final yang diumumkan 1 tahun sebelum keberangkatan. Konsultasikan opsi pembiayaan bila diperlukan.</p>'''),
'rekening-resmi-pembayaran-haji-plus': ('Modus Penipuan yang Perlu Diwaspadai', '''<p>Waspadai tawaran porsi cepat dengan harga tidak wajar atau permintaan transfer ke rekening pribadi. Selalu verifikasi melalui kantor resmi.</p>'''),
'hotel-haji-plus-makkah': ('Memilih Hotel Sesuai Kebutuhan', '''<p>Pertimbangkan kondisi fisik dan kebutuhan keluarga. Hotel depan masjid menghemat tenaga, sementara hotel sedikit lebih jauh menawarkan harga lebih terjangkau.</p>'''),
'hotel-haji-plus-madinah': ('Fase Madinah yang Lebih Tenang', '''<p>Setelah puncak haji, fase Madinah menjadi waktu pemulihan dan memperbanyak ibadah di Masjid Nabawi.</p>'''),
'maskapai-haji-plus': ('Persiapan Penerbangan', '''<p>Ikuti arahan petugas terkait bagasi dan dokumen. Maskapai final dikonfirmasi sesuai ketersediaan dan ketentuan penerbangan haji.</p>'''),
'haji-plus-ramah-lansia': ('Tips untuk Keluarga Jamaah Lansia', '''<p>Lakukan pemeriksaan kesehatan rutin selama masa tunggu, latih berjalan kaki, dan pastikan obat-obatan pribadi tercatat.</p>'''),
'wukuf-arafah-haji-plus': ('Memaknai Wukuf', '''<p>Wukuf adalah momen doa dan muhasabah. Persiapkan daftar doa dan dzikir sejak di tanah air agar waktu di Arafah dimanfaatkan maksimal.</p>'''),
'program-ibadah-haji-plus': ('Menjaga Konsistensi Ibadah', '''<p>Target khatam Al-Qur'an membantu jamaah mengisi waktu luang dengan ibadah. Buat jadwal harian sederhana dan ikuti program bersama rombongan.</p>'''),
'jadwal-umroh-november-2026': ('Kenapa Memilih November?', '''<p>November berada sebelum musim liburan akhir tahun, sehingga cocok bagi jamaah yang fleksibel soal cuti. Daftar lebih awal karena kuota satu tanggal terbatas.</p>'''),
'jadwal-umroh-desember-2026': ('Tips Memilih Tanggal Desember', '''<p>Sesuaikan tanggal dengan cuti dan libur sekolah. Paket awal Desember lebih hemat, sedangkan akhir Desember cocok untuk liburan keluarga.</p>'''),
'biaya-umroh-2027': ('Menyiapkan Anggaran', '''<p>Hitung total biaya keluarga, tambahkan biaya paspor dan vaksin, lalu siapkan DP. Pelunasan dilakukan 35 hari sebelum keberangkatan.</p>'''),
'paket-umroh-gold-12-hari': ('Siapa yang Cocok?', '''<p>Paket Gold 12 hari cocok bagi jamaah yang ingin waktu ibadah panjang sekaligus hotel Makkah di kawasan Zamzam Tower.</p>'''),
'paket-umroh-silver-12-hari': ('Nilai Lebih Program 12 Hari', '''<p>Tambahan hari memberi ritme lebih santai, cocok untuk lansia dan jamaah pertama kali.</p>'''),
'umroh-hotel-bintang-5': ('Bintang 5 Bukan Satu-satunya Ukuran', '''<p>Selain bintang hotel, perhatikan jarak ke masjid, program ibadah, dan kualitas pembimbing ketika memilih paket umroh.</p>'''),
'miqat-qarnul-manazil': ('Persiapan Ihram dari Thaif', '''<p>Bawa pakaian ihram di tas kecil saat ziarah Thaif agar dapat berganti di miqat sesuai arahan pembimbing.</p>'''),
'miqat-jiranah': ('Persiapan Umroh dari Ji’ranah', '''<p>Siapkan ihram sebelum berangkat ziarah kota Makkah dan ikuti bacaan niat bersama pembimbing.</p>'''),
'paket-umroh-premium-januari-2027': ('Kenyamanan untuk Keluarga', '''<p>Paket Premium banyak dipilih keluarga yang mengajak orang tua karena lokasi hotel yang dekat dan bonus lengkap.</p>'''),
'paket-umroh-bronze': ('Hemat Tanpa Mengurangi Ibadah', '''<p>Program ibadah pada paket Bronze sama lengkapnya dengan kelas lain; perbedaannya terutama pada hotel dan bonus.</p>'''),
'vip-lounge-umroh-soekarno-hatta': ('Tips di Hari Keberangkatan', '''<p>Datang tepat waktu ke titik kumpul, bawa paspor di tas kabin, dan ikuti arahan tour leader saat check-in rombongan.</p>'''),
'manasik-umroh': ('Manfaat Mengikuti Manasik', '''<p>Manasik membantu jamaah memahami rukun dan wajib umroh sehingga ibadah lebih tenang dan sesuai tuntunan.</p>'''),
}

FAS_RINGKAS = FASILITAS[:12]


def blok_umroh(slug, i):
    """Blok pendukung bergilir untuk artikel umroh (hindari duplikasi seragam)."""
    daftar = ('<h2>Cara Daftar Singkat</h2>' + ol(['Pilih paket dan tanggal keberangkatan.', 'Siapkan paspor (berlaku minimal 10 bulan) dan dokumen pendukung.',
                                                   'Bayar DP Rp 6.000.000 per jamaah ke rekening resmi PT Dhiyaa El Haramain El Mubarakah.',
                                                   'Lunasi 35 hari sebelum keberangkatan dan ikuti manasik.']))
    fas = '<h2>Fasilitas Utama yang Sudah Termasuk</h2>' + ul(FAS_RINGKAS) + '<p>Daftar lengkap ada di halaman fasilitas paket.</p>'
    itin = '<h2>Gambaran Program 9 Hari</h2>' + ol(ITIN_9)
    pilihan = [(fas, daftar), (itin, daftar), (fas, itin), (daftar, fas), (itin, fas)]
    skip = {'fasilitas-paket-umroh': fas, 'cara-daftar-umroh-dp-6-juta': daftar, 'itinerary-umroh-9-hari': itin}
    return ''.join(b for b in pilihan[i % len(pilihan)] if b != skip.get(slug))


def blok_haji(slug, i):
    keunggulan = ('<h2>Keunggulan Haji Plus Elharamain Wisata</h2>' + ul(['PIHK resmi Kementerian Agama RI No. 846/2020', 'Bimbingan ibadah intensif sejak masa tunggu',
                  'Setoran awal 4.000 USD dengan proses cepat', 'Free badal haji bila wafat di masa tunggu', 'Transparansi Dana Manfaat',
                  'Voucher umroh Rp 5.000.000 selama masa tunggu']))
    daftar = ('<h2>Syarat & Cara Daftar Haji Plus</h2>' + ul(['Setoran awal 4.000 USD per jamaah; pelunasan 6 bulan sebelum keberangkatan.',
              'Dokumen: KTP, KK, pas foto 4x6, fotokopi buku nikah (suami-istri), fotokopi akte lahir.', 'Pembayaran hanya ke rekening resmi PT Dhiyaa El Haramain El Mubarakah (Bank Danamon Syariah).']))
    tabel = '<h2>Ringkasan 4 Paket Haji Plus 1448 H</h2>' + haji_table()
    pilihan = [(keunggulan, daftar), (tabel, daftar), (keunggulan, tabel), (daftar, keunggulan), (tabel, keunggulan)]
    return ''.join(pilihan[i % len(pilihan)])
