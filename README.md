# elharamainwisata.com — catatan kerja & tools

Situs: WordPress + Elementor (tema LandingPress, Rank Math), di belakang Cloudflare + LiteSpeed Cache.
Konten halaman dibangun di repo ini lalu dikirim lewat WP REST API (`meta._elementor_data`).

## 4 domain Elharamain Wisata — peran masing-masing (ditentukan 30 Sep 2026)
| Domain | Peran | Kredensial (env var Windows) |
|---|---|---|
| **elharamainwisata.com** | Web utama (hub brand, umroh + haji) | `WP_USER` / `WP_APP_PASSWORD` |
| **elharamainhaji.com** | Web haji **utama** (situs jualan/transaksional haji #1) | `ELHARAMAINHAJI_WP_USER` / `ELHARAMAINHAJI_WP_APP_PASSWORD` |
| **elharamain.id** | Info-info seputar **umroh** (konten/edukasi) | `ELHARAMAINID_WP_USER` / `ELHARAMAINID_WP_APP_PASSWORD` |
| **haji.biz** | Info-info seputar **haji** (konten/edukasi) | `HAJIBIZ_WP_USER` / `HAJIBIZ_WP_APP_PASSWORD` — **auth REST rusak**, lihat catatan di bawah |

Sebelum bikin/pindah konten baru: sales & paket → elharamainwisata.com & elharamainhaji.com. Artikel edukasi/SEO
long-tail → elharamain.id (umroh) & haji.biz (haji). **Belum ditindaklanjuti:** elharamainhaji.com (situs jualan)
saat ini juga berisi banyak artikel edukasi haji (cara daftar, biaya, perbandingan paket dll) yang menurut strategi
ini semestinya lebih cocok dipindah ke haji.biz — tunggu arahan sebelum memindahkan.

### Rank Math Pro + WordPress Abilities API (jauh lebih reliable dari REST lama)
Aktif di elharamainwisata.com, elharamainhaji.com, elharamain.id: `GET/POST /wp-json/wp-abilities/v1/abilities/rank-math/<nama>/run`
(readonly = GET dengan `?input[field]=value`, write = POST dengan body `{"input": {...}}`). Ability yang berguna:
`get-settings`, `set-post-type-seo-settings` (noindex/sitemap per post type), `set-sitemap-settings`,
`audit-site-seo` (skor + temuan fail/warning), `fix-site-seo` (auto-fix test_id: `focus_keywords`, `post_titles`, dll),
`get-post-schema`, `get-post-seo-meta`. Endpoint REST lama `rankmath/v1/updateMeta` (`{"objectType":"post","objectID":N,"meta":{"rank_math_title":...,"rank_math_description":...,"rank_math_robots":[...]}}`)
masih jalan untuk meta per-post kalau ability belum cukup; `rankmath/v1/updateSettings` **selalu 403** lewat Application Password (butuh sesi login).

### Status akses otomatis (tes 30 Sep 2026)
| Situs | Login REST | Template UAE via REST |
|---|---|---|
| elharamainwisata.com | OK | OK (snippet lama) |
| elharamainhaji.com | OK (env `ELHARAMAINHAJI_USER`) | perlu snippet `wordpress/wpcode-uae-rest.php` |
| elharamain.id | 401: env `ELHARAMAINID_WP_USER` kosong | perlu snippet |
| haji.biz | **OK tanpa snippet** (sekarang jalan) | perlu snippet |

Hosting kadang membalas halaman HTML "reload 5 detik" (anti-bot) untuk request ber-login; cukup ulangi
beberapa detik kemudian (`tools/deploy_uae.py` sudah otomatis mengulang). Setelah snippet terpasang:
`python3 tools/deploy_uae.py hajibiz header wordpress/uae/haji-biz-header.html`.

### haji.biz — auth REST bermasalah (catatan lama), JANGAN pasang snippet penambal LOGIN lagi
Snippet `wpcode-uae-rest.php` aman karena tidak menyentuh proses login.
Server haji.biz meneruskan header `Authorization` tapi PHP tidak memecahnya jadi `PHP_AUTH_USER`/`PHP_AUTH_PW` (beda
dari elharamainwisata.com). Snippet WPCode penambal sempat dipasang (urai manual dari `HTTP_AUTHORIZATION`), tapi
begitu berhasil mengisi `PHP_AUTH_USER`, malah memicu proses lain di situs mencoba login normal dengan nilai itu
sebagai password biasa (error "Nama pengguna tidak dikenal") — kemungkinan ada plugin Basic-Auth-to-login yang tidak
terduga. Snippet sudah dicabut. Perlu investigasi hosting/plugin dulu sebelum coba lagi.

### Draft artikel SEO (30 Sep 2026) — landing page Elementor, siap direview
Dibuat dari materi brosur PDF asli (bukan konten template), style pakai token yang sama dengan `widget/kartu-harga-live.html`
(`.eh-art`: navy `#1f3553`, biru `#004AAD`, font Raleway/Mulish/Poppins, checklist ikon centang, badge tier gradient, CTA WA pil hijau).
Template halaman: `elementor_canvas` (landing page, tanpa header/footer tema).

| Domain | Post ID | Judul | Status |
|---|---|---|---|
| elharamainwisata.com | 9733 | Paket Umroh Musim Dingin Desember 2026 | draft |
| elharamainwisata.com | 9735 | Panduan Lengkap Haji Plus 1448H | draft |
| elharamainhaji.com | 3509 | Panduan Lengkap Haji Plus 1448H | draft, robots di-override `index` (post type "post" di-noindex massal, lihat bawah) |
| elharamain.id | 801 | Paket Umroh Musim Dingin Desember 2026 | draft |

### elharamainhaji.com — 1.376 post spam terdeteksi & di-noindex (30 Sep 2026)
Post type "post" berisi 1.376 halaman auto-generate 1/kabupaten-kota se-Indonesia (judul diawali nomor WA,
isi cuma daftar keyword diulang, pola "Scaled Content Abuse"). Sumber generator **belum ditemukan** — bukan plugin,
bukan mu-plugin, bukan Application Password, bukan XML-RPC (diblokir 403); hanya ada 1 user di situs. Sudah di-mitigasi:
seluruh post type "post" di-set noindex + dikeluarkan dari sitemap lewat `rank-math/set-post-type-seo-settings` +
`set-sitemap-settings`. Artikel baru yang genuine (id 3509 di atas) di-override manual jadi `index` per-post.
**Perlu:** cari sumber generator (cek Cron Job cPanel hosting), ganti password login akun `elharamainhaji`.

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
Nomor admin lain (bukan cabang): 6282320722940, 6285199381590.

Rotasi tombol WA melayang (Click to Chat Pro, diatur di WP Admin karena endpoint REST plugin butuh nonce sesi login):
6281287292422, 6285179988198, 6285693883208, 6282320722940, 6281214178056, 6285843372026, 628132212344, 6285199381590,
6282260126394. Di 6 halaman cabang rotasi dikunci ke nomor cabang oleh `widget/wa-cabang-template.html`.

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
   gambar 404 `Assets-Elaramin-Umroh.webp`. (Bahasa situs → id_ID **sudah selesai** 29 Sep.)
4. Konfirmasi nomor WA Bandung dan nomor rotasi 6285843372026 di plugin Click to Chat.
5. Cek plugin mencurigakan "Block Widget" (Auto generated plugin, by Admin).
6. Setelah selesai: hapus snippet WPCode bantu-login dan cabut Application Password.
7. **Baru (30 Sep):** review & publish 4 draft artikel SEO di atas; putuskan auto-fix `post_titles` (7 artikel
   elharamainwisata.com, lihat ability `rank-math/audit-site-seo`); cari sumber generator spam kabupaten di
   elharamainhaji.com; investigasi ulang auth REST haji.biz sebelum pasang snippet lagi; pertimbangkan pindah
   artikel edukasi haji dari elharamainhaji.com ke haji.biz sesuai peran domain baru.
