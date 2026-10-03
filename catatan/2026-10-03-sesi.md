# Catatan sesi 2026-10-03

## Keputusan pemilik
- "kerjakan" = jalankan usulan untuk elharamain.id (bahasa + timezone, LiteSpeed Cache, update Elementor Pro).

## Yang dikerjakan (elharamain.id)
- Timezone: kosong (UTC+0) → **Asia/Jakarta** via REST `/wp/v2/settings` (kredensial env `ELHARAMAINID_USER` /
  `ELHARAMAINID_WP_APP_PASSWORD`, REST situs ini normal, tanpa WAF/anti-bot). Cadangan pengaturan awal:
  `backup/elharamain-id-settings-sebelum-2026-10-03.json`.
- **LiteSpeed Cache 7.9.1** dipasang + diaktifkan via MCP `marketplace/install-plugin` (URL wordpress.org) dan
  `activate-plugin`. Dicek: beranda 200, judul utuh, header `x-litespeed-cache: miss` lalu `hit`. Pengaturan default
  (belum ada UCSS/optimasi lanjutan).

## Belum bisa (perlu pemilik di wp-admin)
- Bahasa `id_ID`: REST menerima tapi diabaikan karena paket bahasa Indonesia belum terpasang.
  → Settings → General → Site Language → Bahasa Indonesia → Save (paket terunduh otomatis).
- Update Elementor Pro 3.28.3 → 4.3.0: plugin berbayar, unduhan butuh lisensi; REST/MCP tak bisa update plugin.
  → Plugins → Elementor Pro → Update now (lisensi aktif, karena WP mendeteksi versi baru).
- Redirect regex elharamainhaji.com (isian di README) masih belum dibuat per 3 Okt.

## Temuan
- elharamain.id punya plugin `code-snippets` (nonaktif) dan WPCode (`insert-headers-and-footers`, aktif).
