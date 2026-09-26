#!/usr/bin/env node
// Membangun landing-pages/section-harga-paket-umroh.html dari data/paket-umroh.json.
// Jalankan: node landing-pages/build-section-harga.js
//
// Output berupa HTML statis (kartu sudah jadi) + tab bulan berbasis CSS (radio button), tanpa JavaScript.
// Alasannya: LiteSpeed di situs menunda semua script sampai pengunjung berinteraksi, sehingga kartu
// yang dibuat lewat JS akan kosong saat halaman dibuka. Jangan tulis tag HTML di dalam komentar HTML
// output — pengoptimal LiteSpeed membacanya sebagai tag sungguhan dan halaman terpotong.
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const { paket: PAKET } = JSON.parse(fs.readFileSync(path.join(ROOT, 'data/paket-umroh.json'), 'utf8'));
const OUT = path.join(__dirname, 'section-harga-paket-umroh.html');

const WA = '6281287292422';
const IMG = 'https://res.cloudinary.com/v6gwkqrb/image/upload/c_fill,g_auto,w_700,h_500,q_auto,f_auto/';
const MIN = 3, MAX = 6, KOLOM = 3;

const IC = {
  durasi: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
  maskapai: '<svg viewBox="0 0 24 24"><path d="M10.5 3.5 13 10h5.5a2 2 0 0 1 0 4H13l-2.5 6.5H8.5L10 14H6l-1.5 2H3l1-4-1-4h1.5L6 10h4L8.5 3.5z"/></svg>',
  tanggal: '<svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>',
  hotel: '<svg viewBox="0 0 24 24"><rect x="4" y="3" width="16" height="18" rx="1"/><path d="M8 7h2M14 7h2M8 11h2M14 11h2M10 21v-4h4v4"/></svg>',
  wa: '<svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.4.1-.2 0-.3 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .1-1.3c0-.1-.2-.2-.4-.3z"/></svg>'
};

const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const rp = n => 'Rp ' + n.toLocaleString('de-DE');
const jt = n => 'Rp ' + String(n / 1e6).replace('.', ',') + ' jt';
const waUrl = teks => 'https://api.whatsapp.com/send?phone=' + WA + '&amp;text=' + encodeURIComponent(teks);
const row = (k, label, v) => '<li><span class="k">' + IC[k] + label + '</span><span class="v">' + esc(v) + '</span></li>';

function card(p) {
  const href = p.detail
    ? esc(p.detail) + '"'
    : waUrl('Assalamualaikum, saya mau info paket umroh ' + p.label + ' ' + p.hari + ' hari, keberangkatan ' + p.berangkat) + '" target="_blank" rel="noopener"';
  return '<a class="card" href="' + href + '>' +
    '<div class="img"><img loading="lazy" src="' + IMG + esc(p.img) + '.jpg" alt="Paket umroh ' + esc(p.label) + ' ' + esc(p.bulan) + '"></div>' +
    '<div class="body">' +
      '<span class="tag ' + esc(p.tier) + '">' + esc(p.label) + '</span>' +
      '<p class="desc">' + esc(p.desc) + '</p>' +
      '<ul class="rows">' +
        row('durasi', 'Durasi', p.hari + ' hari') +
        row('maskapai', 'Maskapai', p.maskapai) +
        row('hotel', 'Hotel Makkah', p.makkah + ' ★5') +
        row('tanggal', 'Berangkat', p.berangkat) +
      '</ul>' +
      '<div class="foot"><small>Mulai dari</small><b>' + rp(p.q) + '</b></div>' +
      '<p class="kamar">Triple ' + jt(p.t) + ' · Double ' + jt(p.d) + '</p>' +
    '</div></a>';
}

// Kartu pengisi agar baris tetap rapi.
function moreCard(bulan) {
  const teks = 'Assalamualaikum, saya mau konsultasi jadwal & paket umroh' + (bulan ? ' bulan ' + bulan : '') + ' lainnya';
  return '<a class="card more" href="' + waUrl(teks) + '" target="_blank" rel="noopener">' +
    '<div class="ic">' + IC.wa + '</div>' +
    '<h3>Paket Lainnya</h3>' +
    '<p>Cari jadwal, durasi, atau tipe kamar lain? Tim kami bantu pilihkan yang paling pas.</p>' +
    '<span>Konsultasi Gratis</span></a>';
}

function view(b) {
  let list;
  const cards = [];
  if (b === 'Semua') {
    list = PAKET.filter(p => p.unggulan);
    if (!list.length) list = PAKET;
    list = list.slice(0, MAX);
    cards.push(...list.map(card));
    // Genapkan ke kelipatan 3, minimal 3 dan maksimal 6 kartu.
    const target = Math.min(MAX, Math.max(MIN, Math.ceil(list.length / KOLOM) * KOLOM));
    while (cards.length < target) cards.push(moreCard(''));
  } else {
    // Tab bulan: semua paket bulan itu + 1 kartu konsultasi, baris terakhir rata tengah.
    cards.push(...PAKET.filter(p => p.bulan === b).map(card), moreCard(b));
  }
  return cards.join('\n');
}

const bulanList = ['Semua'];
PAKET.forEach(p => { if (!bulanList.includes(p.bulan)) bulanList.push(p.bulan); });

// Tab CSS: radio tersembunyi + label; tiap radio menampilkan grid pasangannya.
const radios = bulanList.map((b, i) => '<input type="radio" class="rb" name="ehpk-tab" id="ehpk-t' + i + '"' + (i ? '' : ' checked') + '>').join('');
const labels = bulanList.map((b, i) => '<label class="tab" for="ehpk-t' + i + '">' + esc(b) + '</label>').join('');
const grids = bulanList.map((b, i) => '<div class="grid g' + i + '">\n' + view(b) + '\n</div>').join('\n');
const tabCss = bulanList.map((b, i) =>
  '#ehpk-t' + i + ':checked~.tabs label[for=ehpk-t' + i + ']{background:var(--navy);border-color:var(--navy);color:#fff}' +
  '#ehpk-t' + i + ':checked~.g' + i + '{display:flex}').join('\n');

const BASE_CSS = `.ehpk{--ink:#1d2433;--muted:#5b6474;--line:#e6e8ee;--navy:#1f3553;--merah:linear-gradient(90deg,#8e1b1b,#c0504d);--biru:linear-gradient(90deg,#1f3553,#5b7494);font-family:Mulish,system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:var(--ink);line-height:1.5;max-width:1000px;margin:0 auto;padding:48px 16px}
.ehpk *{box-sizing:border-box}
.ehpk .hd{margin-bottom:24px}
.ehpk .hd h2{font-family:Literata,Georgia,serif;font-weight:600;font-size:clamp(28px,4.5vw,40px);line-height:1.15;margin:0 0 8px;color:var(--ink)}
.ehpk .hd p{margin:0;color:var(--muted);font-size:17px}
.ehpk .rb{position:absolute;opacity:0;pointer-events:none}
.ehpk .tabs{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 28px}
.ehpk .tab{border:1px solid var(--line);background:#fff;color:var(--muted);border-radius:999px;padding:8px 18px;font-weight:700;font-size:14px;line-height:1;cursor:pointer;transition:.2s;user-select:none}
.ehpk .tab:hover{border-color:var(--navy);color:var(--navy)}
.ehpk .grid{--gap:32px;--col:3;display:none;flex-wrap:wrap;justify-content:center;gap:var(--gap)}
.ehpk .grid>.card{width:calc((100% - (var(--col) - 1) * var(--gap)) / var(--col))}
.ehpk .card{display:flex;flex-direction:column;background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden;text-decoration:none;color:inherit;transition:box-shadow .2s,transform .2s}
.ehpk .card:hover{box-shadow:0 12px 28px rgba(29,36,51,.12);transform:translateY(-3px)}
.ehpk .img{aspect-ratio:7/5;background:#eef1f6}
.ehpk .img img{width:100%;height:100%;object-fit:cover;display:block}
.ehpk .body{padding:16px 16px 18px;display:flex;flex-direction:column;flex:1}
.ehpk .tag{align-self:flex-start;color:#fff;font-weight:800;font-size:14px;padding:3px 26px 3px 12px;border-radius:4px 999px 999px 4px;background:var(--biru)}
.ehpk .tag.bronze{background:linear-gradient(90deg,#7a4a22,#b98150)}
.ehpk .tag.silver{background:linear-gradient(90deg,#4f5d70,#95a3b5)}
.ehpk .tag.gold{background:linear-gradient(90deg,#8c6812,#d0a534)}
.ehpk .tag.platinum{background:var(--biru)}
.ehpk .tag.premium{background:var(--merah)}
.ehpk .desc{margin:14px 0 16px;font-size:14px;color:var(--muted)}
.ehpk .rows{margin:0;padding:0;list-style:none;display:grid;gap:8px;font-size:14px;color:var(--muted)}
.ehpk .rows li{display:flex;justify-content:space-between;align-items:center;gap:12px;margin:0}
.ehpk .rows .k{display:flex;align-items:center;gap:8px;flex:none}
.ehpk .rows svg{width:16px;height:16px;stroke:currentColor;fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.ehpk .rows .v{text-align:right}
.ehpk .foot{display:flex;justify-content:space-between;align-items:baseline;gap:8px;margin-top:auto;padding-top:28px}
.ehpk .foot small{font-size:12px;color:var(--muted)}
.ehpk .foot b{font-size:16px;font-weight:800;color:var(--ink)}
.ehpk .kamar{margin:6px 0 0;font-size:12px;color:var(--muted);text-align:right}
.ehpk .more{justify-content:center;align-items:center;text-align:center;padding:32px 24px;background:linear-gradient(160deg,#1f3553,#3b5578);color:#fff;border:0}
.ehpk .more .ic{width:56px;height:56px;border-radius:50%;background:rgba(255,255,255,.14);display:grid;place-items:center;margin:0 auto 16px}
.ehpk .more .ic svg{width:26px;height:26px;fill:#fff}
.ehpk .more h3{font-family:Literata,Georgia,serif;font-weight:600;font-size:22px;margin:0 0 8px;color:#fff}
.ehpk .more p{margin:0 0 20px;font-size:14px;opacity:.85}
.ehpk .more span{display:inline-block;background:#fff;color:var(--navy);font-weight:800;font-size:14px;padding:10px 20px;border-radius:999px}
@media (max-width:900px){.ehpk .grid{--col:2;--gap:20px}}
@media (max-width:600px){.ehpk{padding:36px 16px}.ehpk .grid{--col:1}.ehpk .tabs{flex-wrap:nowrap;overflow-x:auto;padding-bottom:4px}.ehpk .tab{flex:none}}`;

const html = `<!-- Section Harga Paket Umroh (gaya kartu ala jejakimani.com/umroh). FILE HASIL BUILD, jangan diedit manual:
     ubah data/paket-umroh.json lalu jalankan node landing-pages/build-section-harga.js.
     Tempel ke widget HTML Elementor. Gambar dari Cloudinary folder Elharamainwisata/Header. -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Mulish:wght@400;600;700;800&family=Literata:wght@600&display=swap" rel="stylesheet">
<style>
${BASE_CSS}
${tabCss}
</style>

<div class="ehpk" id="paket-umroh">
<div class="hd">
<h2>Umroh Lebih Nyaman</h2>
<p>Pilih jadwal keberangkatan yang paling pas untuk ibadah Anda.</p>
</div>
${radios}
<div class="tabs" role="tablist">${labels}</div>
${grids}
</div>
`;

// Pengaman: komentar HTML tidak boleh berisi tanda kurung sudut (lihat catatan di atas).
for (const m of html.matchAll(/<!--([\s\S]*?)-->/g)) {
  if (/[<>]/.test(m[1])) throw new Error('Komentar HTML output berisi tanda kurung sudut');
}
fs.writeFileSync(OUT, html);
console.log('OK', path.relative(ROOT, OUT), PAKET.length + ' paket,', 'tab: ' + bulanList.join(', '));
