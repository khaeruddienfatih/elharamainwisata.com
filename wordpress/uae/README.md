# Header & footer UAE (Ultimate Addons for Elementor)

Kenapa manual: tool MCP tidak bisa membuat post type `elementor-hf`, `elementor/build-composition`
butuh Atomic Editor (mati di haji.biz), dan REST haji.biz rusak. Pemasangan ±5 menit lewat wp-admin.

## Pasang di haji.biz
1. wp-admin → **Appearance → Elementor Header & Footer Builder → Add New**.
2. Judul `Header Haji.biz`, **Type of Template: Header**, **Display On: Entire Website** → Publish.
3. **Edit with Elementor** → seret widget **HTML** → tempel seluruh isi `haji-biz-header.html` → Update.
4. Ulangi untuk footer: judul `Footer Haji.biz`, Type **Footer**, Display **Entire Website**,
   tempel `haji-biz-footer.html`.
5. Jika header lama tema masih muncul: pastikan UAE → Settings → Theme Support = opsi 1 (Recommended);
   bila tetap dobel, pilih opsi 2.
6. LiteSpeed Cache → **Purge All**, lalu cek di HP (menu hamburger) dan desktop.

## Catatan
- Menu HP memakai checkbox tanpa JavaScript (aman untuk delay JS LiteSpeed).
- Logo di-hotlink dari elharamainwisata.com (hanya dibaca). Lebih baik unggah logo ke media haji.biz
  lalu ganti `src`.
- elharamain.id & elharamainhaji.com sudah punya 2 template `elementor-hf` masing-masing (terlihat di
  audit Rank Math 30 Sep) — belum ditinjau isinya.
