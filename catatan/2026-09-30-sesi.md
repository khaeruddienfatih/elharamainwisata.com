# Catatan sesi 2026-09-30

## Yang dibahas
- Claude tidak ingat sesi VS Code; konteks dibaca ulang dari README dan commit terakhir (24 Sep).
- Struktur 4 domain ditetapkan (lihat CLAUDE.md).
- "UAE" = Ultimate Addons for Elementor (gratis, slug `header-footer-elementor`).

## Yang dikerjakan
- Plugin UAE diaktifkan di haji.biz (sudah terpasang, belum aktif). Sudah ada di elharamain.id dan elharamainhaji.com.
- Dibuat `CLAUDE.md` + PR #1 ke `main`.

## Temuan
- Konektor MCP `Elharamainhaji` dan `Elharamain_id` belum diotorisasi.
- Default branch repo adalah `claude/admiring-curie-k3qpc9`, bukan `main` (perlu diubah di Settings → Branches).
- Tool MCP tidak menjangkau post type `elementor-hf` (header/footer UAE).

## Lanjutan
Lihat bagian "Status & tugas" di CLAUDE.md.

## Header/footer haji.biz
- Draf HTML di `wordpress/uae/haji-biz-header.html` & `-footer.html`, memakai token brand dari tools/build_header.py (belum dipasang).
- Akses web ke haji.biz & elharamain.id diblokir egress; info brand ternyata sudah ada di branch main (README + tools/). Pelajaran: selalu `git merge origin/main` di awal sesi.

## Lanjutan sesi ("lanjut") — konektor Elharamainhaji & Elharamain_id sudah tersambung
Kemampuan sama dengan haji.biz (elementor/*, rank-math/*, marketplace/*). Hanya audit baca-saja; tidak ada perubahan di situs live.

### elharamainhaji.com
- Sumber spam kabupaten ketemu: bukan proses aktif, tapi post terjadwal massal (drip) yang diterbitkan WP-Cron.
  Detail + langkah stop di README (bagian spam). **153 post masih `future`** s.d. 20 Nov 2026. Menunggu keputusan pemilik.
- Rank Math SEO score 80. Gagal: 13 gambar beranda tanpa alt, OpenGraph tanpa `og:image`, Search Console belum terhubung,
  777 post + 12 halaman tanpa focus keyword (sebagian besar post spam).
- Bahasa situs `en_US` (og:locale en_US) → sebaiknya `id_ID` seperti elharamainwisata.com.
- **Tidak ada plugin cache** aktif (WP_CACHE off) padahal server LiteSpeed → pertimbangkan pasang LiteSpeed Cache.
- Modul Rank Math Redirections & 404 Monitor tidak aktif (tabel tidak ada) — perlu jika post spam di-trash + redirect.
- Plugin aktif: Classic Editor, Click to Chat (+PRO), Elementor 4.3.2, Rank Math (+PRO), UAE 2.9.5, WebP Express,
  Widgets for Google Reviews. Tema LandingPress WP 3.4.7.2. 1 user saja.

### elharamain.id
- Rank Math score 78 (tes remote tidak tersedia, hanya 8 tes). Search Console belum terhubung.
- Bahasa `en_US`, **timezone +00:00** (harus Asia/Jakarta agar jadwal post benar).
- Elementor Pro 3.28.3 vs Elementor 4.3.2 → versi Pro tertinggal (ada update 4.3.0); risiko tidak kompatibel.
- Tidak ada plugin cache aktif.

### Kedua server (hosting sama)
- Drop-in `maintenance.php` ada di kedua situs (umum dari hosting/plugin; cek isinya di File Manager).
- OPcache penuh (128 MB, interned strings 100%) → minta hosting menaikkan `opcache.memory_consumption`.

## Keputusan pemilik: "trash redirect saja"
- 1.530 post spam elharamainhaji.com → Trash via REST (`/?rest_route=/wp/v2/posts/<id>` DELETE, tanpa force). Cadangan daftar:
  `backup/elharamainhaji-spam-posts-2026-09-30.csv`. Draf asli 3509 dikecualikan.
- Modul Rank Math Redirections diaktifkan (MCP `set-module-status`). REST `updateRedirection` tidak menyimpan redirect
  (balasan "created", ID kosong, tabel 0 baris) → pemilik membuat 1 redirect regex di wp-admin (isian di README).
- Koreksi audit pagi: LiteSpeed Cache 7.9.1 **sudah aktif** di elharamainhaji.com (terpasang di tengah sesi, WP_CACHE on).
- Hasil trash: 1.530/1.530 post spam di Trash (1.529 via skrip + ID 1978 saat uji). Log: `backup/elharamainhaji-trash-log-2026-09-30.json`.
  Sisa post di situs: hanya 3509 (artikel Haji Plus 1448H, sudah dipublish pemilik 30 Sep 05:28).
- Helper REST tersimpan: `tools/wp_rest_elharamainhaji.py` (retry anti-bot + jalur `?rest_route=`).
- Cek 3 Okt: redirect regex **belum dibuat** (`rank-math/get-redirections` = 0). URL spam lama sekarang 404 sampai redirect dibuat.
