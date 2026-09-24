# elharamainwisata.com — catatan kerja

Situs: WordPress + Elementor (tema LandingPress), di belakang Cloudflare + LiteSpeed.

## Status akses WordPress (REST API)
- `.htaccess` sudah berisi `RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]`.
- Snippet WPCode `wordpress/wpcode-bantu-login-api.php` aktif: ada plugin yang menentukan user terlalu awal,
  snippet ini memvalidasi ulang Application Password saat request REST. Diagnosa: `GET /wp-json/eh-diag/v1/auth`.
- Kredensial dibaca dari environment `WP_USER` (username login, bukan nama Application Password) dan `WP_APP_PASSWORD`.
- Tes login: `curl -u "$WP_USER:$WP_APP_PASSWORD" https://www.elharamainwisata.com/wp-json/wp/v2/users/me`

## Pekerjaan berikutnya
1. Pasang `landing-pages/umroh-riyadh-air-10-hari.html` sebagai halaman **Draft** (Umroh Premium Musim Sejuk 10 Hari by Riyadh Air,
   berangkat 26 Nov 2026, mulai 37 jt). Nomor WhatsApp di LP sementara nomor pusat 6281287292422 — konfirmasi dulu (Fifi atau pusat).
2. Perbaikan beranda hasil audit: link telepon `http://0812-8729-2422` → `tel:081287292422`, "ZIN UMRAH" → "IZIN UMRAH",
   "WIsata" → "Wisata", "Kuliner Khas Nusantara" → "Kuliner Khas Arab Saudi", "Ibadah Haji Anda" → "Ibadah Umroh & Haji Anda",
   bahasa situs → id_ID, header/footer tema dobel, gambar 404 `Assets-Elaramin-Umroh.webp`, tag GA lama `UA-98624123-1`.
3. Cek plugin mencurigakan "Block Widget" (Auto generated plugin, by Admin).
4. Setelah selesai: hapus snippet WPCode dan cabut Application Password.
