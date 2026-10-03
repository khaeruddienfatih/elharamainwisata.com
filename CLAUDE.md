# CLAUDE.md — konteks proyek Elharamain Wisata

Baca file ini di awal sesi. Bahasa kerja: Indonesia. Jangan minta pemilik mengulang info yang sudah tertulis di sini.

## 4 domain (WordPress + Elementor + Rank Math)
| Domain | Peran |
|---|---|
| elharamainwisata.com | Web utama, hub brand (umroh + haji). **Sudah bagus — JANGAN diubah.** |
| elharamainhaji.com | Web haji utama (jualan/transaksional). 1.530 post spam sudah di-Trash (30 Sep); lihat README |
| elharamain.id | Info/edukasi umroh |
| haji.biz | Info/edukasi haji. **Auth REST rusak** — jangan pasang snippet WPCode lagi tanpa investigasi |

**Sumber kebenaran: `README.md` (branch `main`).** Baca itu dulu; berisi peran domain, tools, widget live, tracking GTM,
pelajaran teknis LiteSpeed, dan daftar "Pekerjaan berikutnya". Branch kerja utama = `main`; jangan mulai dari branch `claude/*` lama.
Kredensial: env var per domain (nama ada di README), jangan tulis di repo.

## Akses
- MCP WordPress tersambung: `elharamainwisata_com`, `haji_biz` (tool: elementor/*, rank-math/*, marketplace/*).
- `Elharamainhaji` & `Elharamain_id` **sudah tersambung** (30 Sep, kemampuan sama).
- REST API elharamainwisata.com: lihat `README.md` (snippet WPCode `wordpress/wpcode-bantu-login-api.php`, kredensial dari env `WP_USER` / `WP_APP_PASSWORD`, jangan pernah tulis kredensial di repo).
- Tool marketplace hanya memasang plugin dari URL download; plugin berbayar butuh file zip/lisensi dari pemilik.

## Aturan kerja
- **JANGAN ubah elharamainwisata.com** (situs utama sudah bagus, kata pemilik). Hanya boleh baca/audit. Perubahan hanya jika pemilik minta eksplisit.
- Istilah pemilik: "UAE" = plugin Ultimate Addons for Elementor. Kalau istilah ambigu, cek dulu di sini sebelum bertanya.
- Konfirmasi dulu sebelum aksi di situs live yang sulit dibatalkan (pasang/hapus plugin, publish halaman). Halaman baru dibuat sebagai Draft.
- Jangan buat PR kecuali diminta. Commit ke branch sesi, push di akhir.
- Simpan ringkasan tiap sesi di `catatan/AAAA-BB-HH-sesi.md` (keputusan, pekerjaan, temuan; tanpa kredensial). Lakukan otomatis di akhir sesi tanpa diminta, lalu commit & push. Transkrip mentah tidak bisa disimpan; hanya ringkasan.
- Di akhir sesi, perbarui bagian "Status & tugas" di bawah supaya sesi berikutnya tidak mengulang.

## Status & tugas
Lihat "Pekerjaan berikutnya" di `README.md`. Tambahan sesi 2026-09-30:
- Plugin UAE (= Ultimate Addons for Elementor gratis, slug `header-footer-elementor`) aktif di haji.biz, elharamain.id, elharamainhaji.com.
- Draf header/footer haji.biz: `wordpress/uae/haji-biz-*.html` (brand dari `tools/build_header.py`/`build_footer.py`). Belum dipasang: MCP haji.biz tak bisa membuat post type `elementor-hf`, REST haji.biz rusak → tempel manual di UAE.
- Konektor `Elharamainhaji` & `Elharamain_id` sudah tersambung; audit kedua situs ada di `catatan/2026-09-30-sesi.md`.
- Spam elharamainhaji.com: 1.530 post sudah di-Trash (30 Sep). Sisa: pemilik buat 1 redirect regex Rank Math (isian di README;
  per 3 Okt belum ada), lalu cek `rank-math/get-redirections`. Helper REST: `tools/wp_rest_elharamainhaji.py`. Jangan cari "generator" lagi (itu drip post terjadwal, sudah dibuang).
- Usulan (butuh izin): bahasa id_ID + timezone Asia/Jakarta di elharamain.id, LiteSpeed Cache di elharamain.id (elharamainhaji.com sudah aktif),
  update Elementor Pro di elharamain.id.
