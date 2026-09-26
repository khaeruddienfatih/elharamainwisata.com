"""Perlengkapan section: replaces the old Elementor slides widget (2025 images) with the
Canva design (exported to Cloudinary) split into Jamaah Pria / Jamaah Wanita."""

CLD = 'https://res.cloudinary.com/v6gwkqrb/image/upload/'
SRC = 'perlengkapan-umroh-eksklusif-elharamain-2026.jpg'  # 1588x2246, Canva DAHWEZG_LvE page 2
PARTS = [  # (label, crop) - pixel crops of the Canva page
    ('Perlengkapan Jamaah Pria', 'c_crop,x_0,y_195,w_1588,h_910'),
    ('Perlengkapan Jamaah Wanita', 'c_crop,x_0,y_1120,w_1588,h_1060'),
]


def html():
    cards = []
    for label, crop in PARTS:
        w, h = 1588, int(crop.split('h_')[1])
        src = f'{CLD}{crop}/w_800,f_auto,q_auto/{SRC}'
        srcset = ', '.join(f'{CLD}{crop}/w_{x},f_auto,q_auto/{SRC} {x}w' for x in (480, 800, 1200))
        full = f'{CLD}{crop}/f_auto,q_auto/{SRC}'
        cards.append(
            f'<figure class="ehpl-c"><figcaption>{label}</figcaption>'
            f'<a href="{full}" target="_blank" rel="noopener"><img src="{src}" srcset="{srcset}" '
            f'sizes="(max-width:760px) 100vw, 560px" width="{w}" height="{h}" loading="lazy" '
            f'alt="{label} Elharamain Wisata - paket umroh"></a></figure>')
    return ('<style>'
            '.ehpl{display:grid;grid-template-columns:1fr 1fr;gap:22px;max-width:1160px;margin:0 auto;font-family:Poppins,sans-serif}'
            '.ehpl-c{margin:0;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 8px 26px rgba(0,40,100,.14)}'
            '.ehpl-c figcaption{background:#004AAD;color:#fff;font-weight:700;font-size:17px;padding:12px 18px;text-align:center}'
            '.ehpl-c img{display:block;width:100%;height:auto}'
            '.ehpl-note{max-width:1160px;margin:14px auto 0;text-align:center;font:500 14px Poppins,sans-serif;color:#10213d}'
            '@media (max-width:760px){.ehpl{grid-template-columns:1fr}}'
            '</style>'
            '<div class="ehpl">' + ''.join(cards) + '</div>'
            '<p class="ehpl-note">Klik gambar untuk memperbesar.</p>')


def replace_slides(data):
    """Swap every Elementor 'slides' widget (the perlengkapan slider) for the new HTML block."""
    n = 0

    def walk(nodes):
        nonlocal n
        for i, e in enumerate(nodes):
            if e.get('widgetType') == 'slides':
                nodes[i] = {'id': e['id'], 'elType': 'widget', 'widgetType': 'html', 'isInner': False,
                            'settings': {'html': html()}, 'elements': []}
                n += 1
            else:
                walk(e.get('elements', []))
    walk(data)
    return n
