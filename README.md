# elharamainwisata.com — catatan kerja

Situs: WordPress + Elementor (tema LandingPress), di belakang Cloudflare + LiteSpeed.

## Status akses WordPress (REST API)
- `.htaccess` sudah berisi `RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]`.
- Snippet WPCode `wordpress/wpcode-bantu-login-api.php` aktif: ada plugin yang menentukan user terlalu awal,
  snippet ini memvalidasi ulang Application Password saat request REST. Diagnosa: `GET /wp-json/eh-diag/v1/auth`.
- Kredensial dibaca dari environment `WP_USER` (username login, bukan nama Application Password) dan `WP_APP_PASSWORD`.
- Tes login: `curl -u "$WP_USER:$WP_APP_PASSWORD" https://www.elharamainwisata.com/wp-json/wp/v2/users/me`

## Perubahan live
- 2026-09-26 — Beranda (page 7840): slider atas (widget image-carousel `5e65f052`) diganti 25 foto dari Cloudinary
  folder `Elharamainwisata/Header` (`c_fill,g_auto,w_1600,h_900,q_auto,f_auto`). Backup `_elementor_data` sebelum perubahan:
  `wordpress/backup-beranda-7840-elementor-data-2026-09-26.json` (kembalikan lewat `POST /wp/v2/pages/7840` field `meta._elementor_data`).

- 2026-09-26 — Halaman Paket Umroh Musim Dingin (page 9581): section harga baru dipasang sebagai widget HTML `e7a4c21`
  (isi = `landing-pages/section-harga-paket-umroh.html` + CSS kecil: judul bawaan disembunyikan, tab rata tengah).
  Widget harga lama `ba05577` TIDAK dihapus, hanya disembunyikan (hide desktop/tablet/mobile) karena CSS-nya dipakai
  section "Fasilitas & Ketentuan". Backup sebelum perubahan: `wordpress/backup-paket-umroh-musim-dingin-9581-2026-09-26.json`.

## Pelajaran teknis (LiteSpeed)
- Jangan tulis tag HTML (mis. teks `<script>`) di dalam komentar HTML pada widget: pengoptimal LiteSpeed membacanya sebagai
  tag sungguhan dan sebagian besar halaman hilang dari output.
- LiteSpeed menunda semua JavaScript sampai pengunjung berinteraksi → konten penting harus HTML statis, bukan dibuat JS.
- Setelah mengubah `_elementor_data` via REST, bersihkan cache: `DELETE /wp-json/elementor/v1/cache`.

## Pekerjaan berikutnya
1. Pasang `landing-pages/umroh-riyadh-air-10-hari.html` sebagai halaman **Draft** (Umroh Premium Musim Sejuk 10 Hari by Riyadh Air,
   berangkat 26 Nov 2026, mulai 37 jt). Nomor WhatsApp di LP sementara nomor pusat 6281287292422 — konfirmasi dulu (Fifi atau pusat).
2. Perbaikan beranda hasil audit: link telepon `http://0812-8729-2422` → `tel:081287292422`, "ZIN UMRAH" → "IZIN UMRAH",
   "WIsata" → "Wisata", "Kuliner Khas Nusantara" → "Kuliner Khas Arab Saudi", "Ibadah Haji Anda" → "Ibadah Umroh & Haji Anda",
   bahasa situs → id_ID, header/footer tema dobel, gambar 404 `Assets-Elaramin-Umroh.webp`, tag GA lama `UA-98624123-1`.
3. Cek plugin mencurigakan "Block Widget" (Auto generated plugin, by Admin).
4. Setelah selesai: hapus snippet WPCode dan cabut Application Password.
