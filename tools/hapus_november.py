"""Hapus paket keberangkatan November 2026 dari data Elementor halaman elharamainwisata.com.
Dipakai 2026-10-09 (permintaan pemilik: "paket november tidak ada"). Cadangan: backup/2026-10-09_hapus_november/."""
import json, re

CARD = re.compile(r'<a class="card"[^>]*>.*?</a>\s*', re.S)

def fix_ehpk(h):
    """Widget harga (.ehpk): buang tab November, grid November, dan kartu 26 Nov di grid lain."""
    if 'class="ehpk' not in h:
        return h
    h = h.replace('<label class="tab" for="ehpk-t1">November</label>', '')
    # grid g1 = tab November (sampai grid berikutnya)
    h = re.sub(r'<div class="grid g1">.*?(?=<div class="grid g2")', '', h, flags=re.S)
    h = CARD.sub(lambda m: '' if re.search(r'26 Nov(ember)? 2026|%2026%20Nov%202026', m.group(0)) else m.group(0), h)
    return h

def fix_common(h):
    h = h.replace('Bronze November \\u00b7 Bronze Plus', 'Bronze Plus').replace('Bronze November · Bronze Plus', 'Bronze Plus')
    return h

def walk(els, fn):
    for e in els:
        st = e.get('settings', {})
        for k in ('html', 'editor', 'title', 'text', 'description_text', 'tab_content'):
            if isinstance(st.get(k), str):
                st[k] = fn(st[k])
        for k, v in st.items():
            if isinstance(v, list):
                for it in v:
                    if isinstance(it, dict):
                        for kk in ('text', 'tab_title', 'tab_content', 'title', 'description', 'content', 'item_title', 'item_content'):
                            if isinstance(it.get(kk), str):
                                it[kk] = fn(it[kk])
        walk(e.get('elements', []), fn)

def process(data):
    walk(data, lambda s: fix_common(fix_ehpk(s)))
    return data

def fix_text(h):
    h = h.replace('November 2026 · Desember 2026 · Januari 2027', 'Desember 2026 · Januari 2027')
    h = h.replace('November 2026 – Januari 2027', 'Desember 2026 – Januari 2027')
    h = re.sub(r'November 2026: 26 November 2026(?: \(Bronze &(?:amp;)? Gold\))?; ', '', h)
    return h

def fix_ldjson(h):
    def one(m):
        try:
            j = json.loads(m.group(2))
        except Exception:
            return m.group(0)
        if isinstance(j, dict) and isinstance(j.get('@graph'), list):
            j['@graph'] = [x for x in j['@graph'] if not (isinstance(x, dict) and x.get('@type') == 'TouristTrip' and 'November' in str(x.get('name', '')))]
        return m.group(1) + json.dumps(j, ensure_ascii=False) + m.group(3)
    return re.sub(r'(<script type="application/ld\+json"[^>]*>)(.*?)(</script>)', one, h, flags=re.S)

def fix_ehp_tabs(h):
    """Halaman Musim Dingin: tab periode 'november-2026' (radio, label, panel) dibuang; tab berikutnya jadi default."""
    if 'id="ehp-t-november-2026"' not in h:
        return h
    h = re.sub(r'<input type="radio" class="ehp-tabs-r" name="ehp-tab" id="ehp-t-november-2026" value="november-2026" checked>', '', h)
    h = re.sub(r'(<input type="radio" class="ehp-tabs-r" name="ehp-tab" id="ehp-t-[a-z0-9-]+" value="[a-z0-9-]+")>', r'\1 checked>', h, count=1)
    h = re.sub(r'<label for="ehp-t-november-2026" role="tab">.*?</label>', '', h, flags=re.S)
    h = re.sub(r'<div class="ehp-panel" data-tab="november-2026">.*?(?=<div class="ehp-panel" data-tab=)', '', h, flags=re.S)
    return h

def process(data):  # noqa: F811 (versi lengkap)
    walk(data, lambda s: fix_text(fix_ldjson(fix_ehp_tabs(fix_common(fix_ehpk(s))))))
    return data
