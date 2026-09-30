# CLAUDE.md — konteks proyek Elharamain Wisata

Baca file ini di awal sesi. Bahasa kerja: Indonesia. Jangan minta pemilik mengulang info yang sudah tertulis di sini.

## 4 domain (WordPress + Elementor + Rank Math)
| Domain | Peran |
|---|---|
| elharamainwisata.com | Web utama, hub brand (umroh + haji). **Sudah bagus — JANGAN diubah.** |
| elharamainhaji.com | Web haji utama (jualan/transaksional). Ada 1.376 post spam di-noindex; lihat README |
| elharamain.id | Info/edukasi umroh |
| haji.biz | Info/edukasi haji. **Auth REST rusak** — jangan pasang snippet WPCode lagi tanpa investigasi |

**Sumber kebenaran: `README.md` (branch `main`).** Baca itu dulu; berisi peran domain, tools, widget live, tracking GTM,
pelajaran teknis LiteSpeed, dan daftar "Pekerjaan berikutnya". Branch kerja utama = `main`; jangan mulai dari branch `claude/*` lama.
Kredensial: env var per domain (nama ada di README), jangan tulis di repo.

## Akses
- MCP WordPress tersambung: `elharamainwisata_com`, `haji_biz` (tool: elementor/*, rank-math/*, marketplace/*).
- `Elharamainhaji` & `Elharamain_id` **sudah tersambung** (30 Sep 2026), tool sama (elementor/*, rank-math/*, marketplace/*).
- REST API elharamainwisata.com: lihat `README.md` (snippet WPCode `wordpress/wpcode-bantu-login-api.php`, kredensial dari env `WP_USER` / `WP_APP_PASSWORD`, jangan pernah tulis kredensial di repo).
- Tool marketplace hanya memasang plugin dari URL download; plugin berbayar butuh file zip/lisensi dari pemilik.

## Aturan kerja
- **JANGAN ubah elharamainwisata.com** (situs utama sudah bagus, kata pemilik). Hanya boleh baca/audit. Perubahan hanya jika pemilik minta eksplisit.
- **haji.biz = khusus haji**: jangan tautkan/buat halaman umroh di menu, header, footer, atau halaman haji.biz. **Artikel/blog boleh campur** haji & umroh (keputusan pemilik 30 Sep 2026).
- Istilah pemilik: "UAE" = plugin Ultimate Addons for Elementor. Kalau istilah ambigu, cek dulu di sini sebelum bertanya.
- Konfirmasi dulu sebelum aksi di situs live yang sulit dibatalkan (pasang/hapus plugin, publish halaman). Halaman baru dibuat sebagai Draft.
- Jangan buat PR kecuali diminta. Commit ke branch sesi, push di akhir.
- Simpan ringkasan tiap sesi di `catatan/AAAA-BB-HH-sesi.md` (keputusan, pekerjaan, temuan; tanpa kredensial). Lakukan otomatis di akhir sesi tanpa diminta, lalu commit & push. Transkrip mentah tidak bisa disimpan; hanya ringkasan.
- Di akhir sesi, perbarui bagian "Status & tugas" di bawah supaya sesi berikutnya tidak mengulang.

## Status & tugas
Lihat "Pekerjaan berikutnya" di `README.md`. Tambahan sesi 2026-09-30:
- Plugin UAE (= Ultimate Addons for Elementor gratis, slug `header-footer-elementor`) aktif di haji.biz, elharamain.id, elharamainhaji.com.
- Akses otomatis: snippet `wordpress/wpcode-uae-rest.php` aktif di haji.biz, elharamainhaji.com, elharamain.id. Login REST semua situs OK (helper `tools/deploy_uae.py` → fungsi `rest()`, pakai curl).
- Header/footer UAE **LIVE** di 3 situs (menu: Home, Paket, Tentang Kami, Lokasi Kantor, Blog). Ubah lewat `tools/build_uae_sites.py` lalu `tools/deploy_uae.py`; halaman Lokasi Kantor/Tentang Kami lewat `tools/build_info_pages.py --publish`. Detail: catatan/2026-09-30-sesi.md.
- Paket di beranda elharamain.id & elharamainhaji.com sudah sesuai brosur PDF (`tools/update_home_paket.py`).
- Menunggu keputusan pemilik: di haji.biz masih terbit 2 **halaman** umroh (ID 778, 135) → draft/redirect? (Artikel umroh ID 293, 263 & kategori "Haji & Umroh" dibiarkan: artikel boleh campur.)
- Audit Rank Math 30 Sep: elharamainhaji.com skor 78 (59 post + 12 halaman tanpa focus keyword, GSC belum ditautkan); elharamain.id skor 80 (meta deskripsi beranda 170 kar., 42 gambar tanpa alt, og:image kosong, GSC belum ditautkan).
