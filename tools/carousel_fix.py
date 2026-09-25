"""CSS that pins each Elementor image-carousel slide to its real image ratio.

LiteSpeed lazy-load shows a placeholder until an image loads; a slide whose image is
still a placeholder can end up much taller than the loaded ones, and Swiper stretches
every slide to the tallest, leaving a big empty gap under the carousel."""
import json, os, struct, subprocess

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'image_dims.json')


def _dims(b):
    if b[:4] == b'RIFF' and b[8:12] == b'WEBP':
        c = b[12:16]
        if c == b'VP8X':
            return 1 + int.from_bytes(b[24:27], 'little'), 1 + int.from_bytes(b[27:30], 'little')
        if c == b'VP8 ':
            w, h = struct.unpack('<HH', b[26:30]); return w & 0x3fff, h & 0x3fff
        if c == b'VP8L':
            v = int.from_bytes(b[21:25], 'little'); return (v & 0x3fff) + 1, ((v >> 14) & 0x3fff) + 1
    if b[:2] == b'\xff\xd8':
        i = 2
        while i < len(b) - 9:
            m, L = b[i + 1], int.from_bytes(b[i + 2:i + 4], 'big')
            if m in (0xC0, 0xC1, 0xC2):
                return int.from_bytes(b[i + 7:i + 9], 'big'), int.from_bytes(b[i + 5:i + 7], 'big')
            i += 2 + L
    if b[:4] == b'\x89PNG':
        return struct.unpack('>II', b[16:24])
    return None


def image_dims(url, _cache={}):
    if not _cache:
        _cache.update(json.load(open(CACHE)) if os.path.exists(CACHE) else {})
    if url not in _cache:
        b = subprocess.run(['curl', '-sS', '--max-time', '60', url], capture_output=True).stdout
        _cache[url] = _dims(b)
        json.dump(_cache, open(CACHE, 'w'), indent=0, sort_keys=True)
    return _cache[url]


def carousel_css(data):
    rules = []

    def walk(nodes):
        for e in nodes:
            if e.get('widgetType') == 'image-carousel' and e['settings'].get('carousel'):
                d = image_dims(e['settings']['carousel'][0]['url'])
                if d:
                    sel = f".elementor-element-{e['id']}"
                    rules.append(f"{sel} .swiper-wrapper{{align-items:flex-start}}"
                                 f"{sel} .swiper-slide{{height:auto!important}}"
                                 f"{sel} .swiper-slide-image{{width:min(100%,{d[0]}px);height:auto!important;aspect-ratio:{d[0]}/{d[1]};object-fit:cover}}")
            walk(e.get('elements', []))
    walk(data)
    return '<style>' + ''.join(rules) + '</style>' if rules else ''
