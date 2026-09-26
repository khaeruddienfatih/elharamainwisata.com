# elharamainwisata.com — catatan kerja & tools

Situs: WordPress + Elementor (tema LandingPress, Rank Math), di belakang Cloudflare + LiteSpeed Cache.
Konten halaman dibangun di repo ini lalu dikirim lewat WP REST API (`meta._elementor_data`).

## Sinkron Windows ↔ Mac
- Branch kerja utama: **`main`** (gabungan semua branch `claude/*` per 2026-09-26).
- Sebelum mulai kerja: `git pull`. Setelah selesai: commit lalu `git push`.
- Kredensial **tidak** disimpan di repo. Set di tiap perangkat:
  - Windows: environment variable user `WP_USER` dan `WP_APP_PASSWORD`.
  - Mac: tambahkan `export WP_USER=...` dan `export WP_APP_PASSWORD="..."` di `~/.zshrc`.
  - `WP_USER` = username login WordPress (bukan nama Application Password). Sebaiknya 1 Application Password per perangkat.

## Akses WordPress (REST API)
- `.htaccess` sudah berisi `RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]`.
- Snippet WPCode `wordpress/wpcode-bantu-login-api.php` aktif: ada plugin yang menentukan user terlalu awal,
  snippet ini memvalidasi ulang Application Password saat request REST. Diagnosa: `GET /wp-json/eh-diag/v1/auth`.
- Tes login: `curl -u "$WP_USER:$WP_APP_PASSWORD" https://www.elharamainwisata.com/wp-json/wp/v2/users/me`
- Helper Python lintas OS: `tools/wp_rest.py` (`req()`, `find()`, `get_public()`), membaca kredensial dari environment
  (di Windows juga dari registry user).

## Isi repo
| Path | Isi |
|---|---|
| `tools/build_musim_dingin.py`, `tools/build_pages.py` | Builder data paket, kartu/tab, Elementor data + SEO Rank Math untuk 9581, 8869, 8896, 8908, 8909, 8910, 9099. Jalankan: `OUT=build python3 tools/build_pages.py` |
| `tools/build_header.py`, `build_footer.py`, `deploy.py`, `warm.py`, … | Tools header/footer, deploy, isi ulang cache (sesi 24–25 Sep) |
| `data/paket-umroh.json`, `landing-pages/build-section-harga.js` | Data 17 paket & builder section harga (versi statis tab CSS) |
| `data/harga-paket-umroh.md`, `data/brosur/*.pdf` | Harga dari brosur Nov 2026–Jan 2027 |
| `landing-pages/widget/` | Widget HTML yang **sedang live** (lihat tabel di bawah) |
| `gtm/IMPORT-GTM-elharamain.json` | File import container GTM (tag yang dipindah dari situs) |
| `backup/pages/` | Data halaman sebelum redesign 24 Sep |
| `backup/2026-09-26/<id>_sebelum_<tahap>.json` | `_elementor_data` tiap halaman sebelum tiap tahap perubahan 26 Sep |

### Widget live (26 Sep 2026)
| File | Dipasang di | Keterangan |
|---|---|---|
| `widget/hero-slider.html` | 13 halaman* (menggantikan Image Carousel Elementor) | Slider header ringan: 25 foto Cloudinary `Elharamainwisata/Header`, foto 1 prioritas tinggi, srcset 480/800/1200, tanpa jQuery/Swiper |
| `widget/kartu-harga-live.html` | 9581 + 6 cabang; varian urutan per tier di 8869/8896/8908/8909/8910 | 17 paket, foto `Elharamainwisata/Kartu Paket` (kartu-paket-01…17, dari Canva tanpa logo), baris Hotel Madinah |
| `widget/perlengkapan.html` | 13 halaman* | Foto 2560px dari Canva: `perlengkapan-pria-2026`, `perlengkapan-wanita-2026-a` (ada juga `-b`) |
| `widget/fasilitas-ketentuan-tab.html` | 12 halaman (tanpa beranda) | Tab CSS: Sudah Termasuk / Belum Termasuk / Dokumen / Pendaftaran & Pembayaran |
| `widget/wa-cabang-template.html` | 6 halaman cabang (ditempel di akhir widget fasilitas) | Semua klik WA ke nomor pusat → nomor cabang, termasuk tombol melayang Click to Chat |
| `widget/pembimbing-slider.html` | 13 halaman* | Slider 8 ustadz, 4/3/2/1,3 per tampilan, autoplay 4 dtk |

\* 13 halaman = Beranda 7840, Musim Dingin 9581, Bronze 8869, Silver 8896, Platinum 8908, Premium 8909, Silver 12 Hari 8910,
cabang Bekasi 9584, Jakarta 9585, Depok 9586, Tangerang 9587, Bogor 9588, Bandung 9589. Umroh Plus (8914–8917) & Haji **tidak** diubah.

**Penting:** kartu harga live sudah diedit langsung (foto `kartu-paket-XX`, Hotel Madinah, urutan per tier). Kalau section harga
di-build ulang dari `data/paket-umroh.json` / `build-section-harga.js` / `build_musim_dingin.py`, perubahan itu harus ikut dimasukkan
ke builder dulu, kalau tidak akan hilang.

Nomor WA cabang: Bekasi (pusat) 6281287292422 · Jakarta 6281214178056 · Depok 6285179988198 · Tangerang 6285693883208 ·
Bogor 6282260126394 · Bandung 628132212344 (11 digit — belum dikonfirmasi).

## Tracking (semua lewat GTM-PJVND2F9, versi 15 per 26 Sep)
- Di situs hanya tersisa snippet GTM. Kode lama (UA-98624123-1, gtag AW-11511018347, Facebook Pixel tema LandingPress,
  TikTok 2x) sudah dihapus.
- Tag di GTM: Google tag AW-11512602371 (+ konversi Ads, Conversion Linker), Google tag AW-11511018347, GA4 G-N0SHQ6D2QL,
  Facebook Pixel 1313353029656348 / 989315122296585 / 2017127175571851 (PageView), TikTok D7LBT4RC77UDI5AAHHAG,
  Helper `gtag()` (untuk `data-awdata` tombol LandingPress & Click to Chat), AddToCart FB & TikTok + GA4 `klik_whatsapp`
  pada setiap klik link WhatsApp dan event `Click to Chat`.
- Catatan: trigger konversi Ads lama (label `adEmCOr05NIbEIO-0fEq`) hanya aktif di `umroh.elharamainwisata.com`.

## Pelajaran teknis
- **Jangan tulis tag HTML (mis. teks `<script>`) di dalam komentar HTML pada widget**: pengoptimal LiteSpeed membacanya sebagai
  tag sungguhan dan sebagian besar halaman hilang dari output.
- LiteSpeed menunda semua JavaScript sampai pengunjung berinteraksi → konten penting harus HTML statis. Script yang harus
  langsung jalan diberi `data-no-optimize="1" data-no-defer="1" data-cfasync="false"`.
- Foto yang harus langsung tampil diberi `class="skip-lazy" data-no-lazy="1"` agar tidak di-lazyload LiteSpeed.
- Setelah mengubah `_elementor_data` via REST: `DELETE /wp-json/elementor/v1/cache`, lalu isi ulang cache
  (cache miss = respon server 4–7 dtk, cache hit = 0,3–0,6 dtk).
- Saat memotong HTML widget dengan regex, jangan pakai `.*?</div>` (berhenti di `</div>` pertama di dalam kartu).

## Pekerjaan berikutnya
1. Kecepatan (Lighthouse HP 26 Sep: beranda 16, Jakarta 39): LiteSpeed → Page Optimization → UCSS + Load CSS Async,
   Crawler aktif; cek CLS 0,9 di beranda (hanya muncul di Lighthouse).
2. Pasang `landing-pages/umroh-riyadh-air-10-hari.html` sebagai halaman **Draft** (konfirmasi nomor WA dulu).
3. Sisa audit beranda: link telepon `http://0812-8729-2422` → `tel:081287292422`, "ZIN UMRAH" → "IZIN UMRAH",
   bahasa situs → id_ID, gambar 404 `Assets-Elaramin-Umroh.webp`.
4. Konfirmasi nomor WA Bandung dan nomor rotasi 6285843372026 di plugin Click to Chat.
5. Cek plugin mencurigakan "Block Widget" (Auto generated plugin, by Admin).
6. Setelah selesai: hapus snippet WPCode bantu-login dan cabut Application Password.
