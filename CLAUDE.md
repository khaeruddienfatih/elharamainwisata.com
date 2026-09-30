# CLAUDE.md — konteks proyek Elharamain Wisata

Baca file ini di awal sesi. Bahasa kerja: Indonesia. Jangan minta pemilik mengulang info yang sudah tertulis di sini.

## 4 domain (semua WordPress + Elementor + Rank Math)
| Domain | Peran |
|---|---|
| elharamainwisata.com | Domain utama & branding (travel umroh) |
| elharamainhaji.com | Khusus haji |
| elharamain.id | News/berita umroh |
| haji.biz | News/berita haji |

Stack elharamainwisata.com: tema LandingPress, Cloudflare + LiteSpeed.

## Akses
- MCP WordPress tersambung: `elharamainwisata_com`, `haji_biz` (tool: elementor/*, rank-math/*, marketplace/*).
- Belum diotorisasi (perlu dilakukan pemilik di pengaturan konektor claude.ai): `Elharamainhaji`, `Elharamain_id`.
- REST API elharamainwisata.com: lihat `README.md` (snippet WPCode `wordpress/wpcode-bantu-login-api.php`, kredensial dari env `WP_USER` / `WP_APP_PASSWORD`, jangan pernah tulis kredensial di repo).
- Tool marketplace hanya memasang plugin dari URL download; plugin berbayar butuh file zip/lisensi dari pemilik.

## Aturan kerja
- Istilah pemilik: "UAE" = plugin Ultimate Addons for Elementor. Kalau istilah ambigu, cek dulu di sini sebelum bertanya.
- Konfirmasi dulu sebelum aksi di situs live yang sulit dibatalkan (pasang/hapus plugin, publish halaman). Halaman baru dibuat sebagai Draft.
- Jangan buat PR kecuali diminta. Commit ke branch sesi, push di akhir.
- Di akhir sesi, perbarui bagian "Status & tugas" di bawah supaya sesi berikutnya tidak mengulang.

## Status & tugas (perbarui tiap sesi)
Selesai:
- Akses REST API WordPress elharamainwisata.com (.htaccess + snippet WPCode).
- Draft landing page `landing-pages/umroh-riyadh-air-10-hari.html` (26 Nov 2026, mulai 37 jt).

- Plugin UAE (= Ultimate Addons for Elementor versi gratis, slug `header-footer-elementor`) aktif di haji.biz, elharamain.id, elharamainhaji.com. "UAE" TIDAK berarti Uni Emirat Arab.

Belum:
1. Pasang LP Riyadh Air sebagai halaman Draft; konfirmasi nomor WhatsApp (Fifi atau pusat 6281287292422).
2. Rapikan isi elharamainhaji.com & elharamain.id (plugin UAE sudah dipasang pemilik, isinya belum bagus) → audit setelah konektornya diotorisasi. Buat header/footer UAE di haji.biz meniru elharamain.id (template post type `elementor-hf` tidak terjangkau tool MCP; pakai Import/Export Elementor).
3. Perbaikan beranda elharamainwisata.com: link `http://0812-8729-2422` → `tel:081287292422`; "ZIN UMRAH" → "IZIN UMRAH"; "WIsata" → "Wisata"; "Kuliner Khas Nusantara" → "Kuliner Khas Arab Saudi"; "Ibadah Haji Anda" → "Ibadah Umroh & Haji Anda"; bahasa situs id_ID; header/footer tema dobel; gambar 404 `Assets-Elaramin-Umroh.webp`; tag GA lama `UA-98624123-1`.
4. Cek plugin mencurigakan "Block Widget".
5. Setelah selesai: hapus snippet WPCode & cabut Application Password.
