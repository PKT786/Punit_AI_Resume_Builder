"""
generate_assets.py
-------------------
Creates the app's brand assets:
  logo.png  — a wax-seal style monogram (deep navy + brass gold, embossed rim)
  hero.png  — an editorial hero graphic: two stacked, gently tilted resume
              cards on an ink-navy ground with a brass foil corner accent
              and soft film-grain texture

Design language: "ink & brass" — deep navy/charcoal grounds, warm brass-gold
accents, a serif display face (Lora) for anything text-like. Chosen because
the product is a resume/document tool: paper, foil-stamped stationery, and
letterpress typography are the natural vocabulary for "premium" here rather
than a generic tech-gradient look.

Run once (or whenever you want to regenerate placeholders):
    python3 generate_assets.py

Replace logo.png / hero.png with your own files at any time — same
filenames, any reasonable resolution.
"""

import math
import random

from PIL import Image, ImageDraw, ImageFont, ImageFilter

random.seed(11)

INK = (11, 15, 26)          # near-black navy ground
NAVY = (18, 32, 61)         # deep navy
NAVY_2 = (27, 45, 82)       # lighter navy for gradient
BRASS = (196, 155, 74)      # warm brass gold
BRASS_LIGHT = (224, 191, 118)
PAPER = (247, 243, 234)     # ivory/paper
INK_TEXT = (35, 38, 43)


def _font(path_options, size):
    for p in path_options:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()


SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
LORA = "/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf"


def _radial_gradient(size, inner, outer, center=None, radius=None):
    w, h = size
    if center is None:
        center = (w / 2, h / 2)
    if radius is None:
        radius = max(w, h) / 2
    img = Image.new("RGB", size, outer)
    px = img.load()
    cx, cy = center
    for y in range(h):
        for x in range(0, w, 2):  # step 2 for speed, fine for our sizes
            d = math.hypot(x - cx, y - cy) / radius
            d = min(d, 1)
            r = int(inner[0] + (outer[0] - inner[0]) * d)
            g = int(inner[1] + (outer[1] - inner[1]) * d)
            b = int(inner[2] + (outer[2] - inner[2]) * d)
            px[x, y] = (r, g, b)
            if x + 1 < w:
                px[x + 1, y] = (r, g, b)
    return img


def _add_grain(img, amount=10):
    w, h = img.size
    noise = Image.effect_noise((w, h), amount).convert("L")
    noise_rgb = Image.merge("RGB", (noise, noise, noise))
    return Image.blend(img, noise_rgb, 0.04)


# ------------------------------------------------------------------- logo --
def make_logo(path="logo.png", size=320):
    S = 4  # supersample for crisp edges
    big = size * S
    img = _radial_gradient((big, big), NAVY_2, INK, radius=big * 0.62)
    d = ImageDraw.Draw(img)

    cx, cy = big / 2, big / 2
    outer_r = big * 0.46

    # outer brass ring (double line, like a wax seal / medallion edge)
    d.ellipse([cx - outer_r, cy - outer_r, cx + outer_r, cy + outer_r],
              outline=BRASS, width=int(6 * S))
    inner_r = outer_r - 14 * S
    d.ellipse([cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r],
              outline=BRASS, width=int(2 * S))

    # small tick marks around the rim (coin/medallion detail)
    tick_r_outer = outer_r + 9 * S
    tick_r_inner = outer_r + 2 * S
    for i in range(48):
        ang = (i / 48) * 2 * math.pi
        x1 = cx + tick_r_inner * math.cos(ang)
        y1 = cy + tick_r_inner * math.sin(ang)
        x2 = cx + tick_r_outer * math.cos(ang)
        y2 = cy + tick_r_outer * math.sin(ang)
        d.line([x1, y1, x2, y2], fill=BRASS, width=int(2 * S))

    # monogram
    font = _font([LORA, SERIF_BOLD], int(outer_r * 1.05))
    text = "PK"
    bbox = d.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text((cx - tw / 2 - bbox[0], cy - th / 2 - bbox[1] - big * 0.02),
            text, font=font, fill=PAPER)

    # thin gold rule beneath monogram
    rule_w = outer_r * 0.9
    ry = cy + th * 0.55
    d.line([cx - rule_w / 2, ry, cx + rule_w / 2, ry], fill=BRASS, width=int(3 * S))

    # tiny caption under the rule
    cap_font = _font([LORA, SERIF], int(outer_r * 0.16))
    cap = "RESUME STUDIO"
    cbbox = d.textbbox((0, 0), cap, font=cap_font)
    cw = cbbox[2] - cbbox[0]
    d.text((cx - cw / 2 - cbbox[0], ry + 10 * S), cap, font=cap_font, fill=BRASS_LIGHT)

    img = img.resize((size, size), Image.LANCZOS)

    # soft drop shadow on transparent canvas
    pad = 24
    canvas = Image.new("RGBA", (size + pad * 2, size + pad * 2), (0, 0, 0, 0))
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse([pad + 6, pad + 10, pad + size - 6, pad + size + 6], fill=(0, 0, 0, 130))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    canvas.paste(shadow, (0, 0), shadow)

    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, size, size], fill=255)
    canvas.paste(img, (pad, pad), mask)

    canvas.save(path)
    print(f"wrote {path}  ({canvas.size[0]}x{canvas.size[1]})")


# ------------------------------------------------------------------- hero --
def _document_card(w, h, accent=BRASS, lines=8, header=True):
    """A single resume-card graphic used inside the hero scene."""
    card = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(card)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=16, fill=PAPER + (255,))

    if header:
        d.rounded_rectangle([0, 0, w - 1, 78], radius=16, fill=NAVY + (255,))
        d.rectangle([0, 56, w - 1, 78], fill=NAVY + (255,))
        # name / title placeholder bars
        d.rounded_rectangle([28, 26, 190, 38], radius=4, fill=PAPER + (255,))
        d.rounded_rectangle([28, 48, 140, 58], radius=3, fill=(BRASS_LIGHT[0], BRASS_LIGHT[1], BRASS_LIGHT[2], 255))
        # accent rule
        d.rectangle([24, 92, w - 24, 96], fill=accent + (255,))

    y = 112 if header else 24
    for i in range(lines):
        lw = (w - 48) - random.randint(0, 70)
        d.rounded_rectangle([24, y, 24 + lw, y + 9], radius=4, fill=(210, 214, 224, 255))
        y += 22
        if i in (2, 5) and header:
            y += 10  # section gap

    return card


def make_hero(path="hero.png", w=1000, h=680):
    base = _radial_gradient((w, h), NAVY_2, INK, center=(w * 0.32, h * 0.38), radius=w * 0.85)
    d = ImageDraw.Draw(base, "RGBA")

    # faint concentric arcs (medallion echo, ties to the logo)
    for i, radius in enumerate([520, 400, 300, 210]):
        alpha = 26 - i * 4
        bbox = [w - radius * 0.4, -radius * 0.5, w - radius * 0.4 + radius * 2, -radius * 0.5 + radius * 2]
        d.ellipse(bbox, outline=BRASS + (max(alpha, 6),), width=2)

    # brass foil corner accent (top-left)
    fold = 130
    d.polygon([(0, 0), (fold, 0), (0, fold)], fill=BRASS + (40,))
    d.line([(0, fold), (fold, 0)], fill=BRASS + (160,), width=3)

    base = base.convert("RGBA")

    # back card (slightly behind/right, muted)
    back = _document_card(300, 400, accent=(154, 165, 177), lines=7)
    back = back.rotate(-8, expand=True, resample=Image.BICUBIC)
    shadow = Image.new("RGBA", back.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rectangle([0, 0, back.size[0], back.size[1]], fill=(0, 0, 0, 0))
    base.paste(back, (int(w * 0.50), int(h * 0.16)), back)

    # front card (main, sharper, on top)
    front = _document_card(320, 430, accent=BRASS, lines=8)
    front = front.rotate(-3, expand=True, resample=Image.BICUBIC)

    # drop shadow for front card
    shadow_layer = Image.new("RGBA", (front.size[0] + 60, front.size[1] + 60), (0, 0, 0, 0))
    shalpha = Image.new("L", front.size, 0)
    ImageDraw.Draw(shalpha).rounded_rectangle([0, 0, front.size[0], front.size[1]], radius=16, fill=140)
    shadow_layer.paste((0, 0, 0, 255), (30, 34), shalpha)
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(18))

    fx, fy = int(w * 0.40), int(h * 0.12)
    base.alpha_composite(shadow_layer, (fx - 30, fy - 20))
    base.alpha_composite(front, (fx, fy))

    # small brass seal badge on the front card corner (echo of the logo)
    seal_d = ImageDraw.Draw(base)
    seal_cx, seal_cy = fx + front.size[0] - 46, fy + 40
    seal_r = 30
    seal_d.ellipse([seal_cx - seal_r, seal_cy - seal_r, seal_cx + seal_r, seal_cy + seal_r],
                   fill=BRASS + (255,), outline=PAPER + (255,), width=3)
    seal_font = _font([LORA, SERIF_BOLD], 26)
    seal_bbox = seal_d.textbbox((0, 0), "PK", font=seal_font)
    sw, sh = seal_bbox[2] - seal_bbox[0], seal_bbox[3] - seal_bbox[1]
    seal_d.text((seal_cx - sw / 2 - seal_bbox[0], seal_cy - sh / 2 - seal_bbox[1]),
                "PK", font=seal_font, fill=INK)

    # floating brass dust / particles for depth
    for _ in range(26):
        rx = random.uniform(w * 0.05, w * 0.95)
        ry = random.uniform(h * 0.05, h * 0.95)
        s = random.uniform(2, 6)
        alpha = random.randint(40, 140)
        seal_d.ellipse([rx, ry, rx + s, ry + s], fill=BRASS + (alpha,))

    out = base.convert("RGB")
    out = _add_grain(out, amount=8)
    out.save(path, quality=95)
    print(f"wrote {path}  ({out.size[0]}x{out.size[1]})")


if __name__ == "__main__":
    make_logo()
    make_hero()
