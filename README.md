# elharamainwisata.com – page tooling

WordPress (Elementor + Rank Math) content for www.elharamainwisata.com is built here and pushed through the WP REST API.

- `tools/build_musim_dingin.py` – package data (prices, dates, hotels from the Nov 2026–Jan 2027 PDFs), card/tab markup and styles.
- `tools/build_pages.py` – builds Elementor data + Rank Math SEO for:
  `/paket-umroh-musim-dingin/` (9581), `/umroh-bronze/` (8869), `/paket-umroh-silver/` (8896),
  `/umroh-platinum/` (8908), `/umroh-premium/` (8909), `/umroh-silver-12-hari/` (8910), `/kantor-cabang/` (9099).
  Run: `OUT=build python3 tools/build_pages.py` → `build/<page_id>.json`, `build/seo.json`, `build/preview-*.html`.
- `backup/pages/` – page JSON (incl. `_elementor_data`) as it was **before** the 2026-09-24 redesign; `backup/seo-before.jsonl` – previous titles/descriptions.

To change a price: edit `PERIODS` in `tools/build_musim_dingin.py`, rebuild, then POST `meta._elementor_data` to `/wp-json/wp/v2/pages/<id>` and clear the Elementor cache (`DELETE /wp-json/elementor/v1/cache`).
