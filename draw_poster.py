"""Draw AURMARA - The Harbour of Golden Stairs (poster v2).

Warm golden-hour coastal town cascading down a cliff to the sea:
grand staircase, harbour boats, cafe terrace with two people at sunset.
Drawn with Pillow at build time; main.py only copies the PNG.
"""
import math
import random

from PIL import Image, ImageDraw, ImageFont, ImageFilter

W = H = 1024
OUT = "/home/hatch/workspace/poster-v2-build/poster.png"
random.seed(20261121)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(img, y0, y1, stops):
    """Vertical gradient between (pos 0..1, rgb) stops over y0..y1."""
    d = ImageDraw.Draw(img)
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0 - 1)
        for i in range(len(stops) - 1):
            p0, c0 = stops[i]
            p1, c1 = stops[i + 1]
            if p0 <= t <= p1:
                tt = (t - p0) / max(1e-6, p1 - p0)
                d.line([(0, y), (W, y)], fill=lerp(c0, c1, tt))
                break


def text_spaced(d, cx, y, s, font, fill, spacing=6, shadow=None):
    widths = [d.textlength(ch, font=font) for ch in s]
    total = sum(widths) + spacing * (len(s) - 1)
    x = cx - total / 2
    for ch, wch in zip(s, widths):
        if shadow:
            d.text((x + shadow[0], y + shadow[1]), ch, font=font, fill=shadow[2])
        d.text((x, y), ch, font=font, fill=fill)
        x += wch + spacing


img = Image.new("RGB", (W, H), (24, 48, 84))
d = ImageDraw.Draw(img, "RGBA")

# ---- sky: deep blue -> orange -> gold, horizon ~y560 ----
vgrad(img, 0, 560, [
    (0.0, (22, 46, 88)),
    (0.35, (64, 84, 130)),
    (0.55, (226, 122, 62)),
    (0.75, (248, 178, 92)),
    (1.0, (252, 214, 150)),
])
# ---- sea: teal gradient 560..800 ----
vgrad(img, 560, 800, [
    (0.0, (250, 196, 120)),
    (0.15, (56, 138, 150)),
    (0.6, (30, 104, 122)),
    (1.0, (22, 82, 100)),
])
# ---- terrace stone 800..1024 ----
vgrad(img, 800, 1024, [
    (0.0, (232, 196, 148)),
    (1.0, (198, 152, 104)),
])

# ---- sun + halo (low, left of centre) ----
sun_c = (400, 520)
for r, a in [(190, 40), (150, 60), (115, 90)]:
    d.ellipse([sun_c[0] - r, sun_c[1] - r, sun_c[0] + r, sun_c[1] + r],
              fill=(255, 214, 130, a))
d.ellipse([sun_c[0] - 78, sun_c[1] - 78, sun_c[0] + 78, sun_c[1] + 78],
          fill=(255, 233, 168, 255))
# sun reflection path on the sea
for i in range(26):
    y = 566 + i * 9
    wdt = 26 + i * 4 + random.randint(-8, 8)
    x0 = sun_c[0] - wdt // 2 + random.randint(-14, 14)
    alpha = max(30, 200 - i * 6)
    d.rectangle([x0, y, x0 + wdt, y + 4], fill=(255, 214, 130, alpha))

# ---- distant headland (right, hazy) ----
d.polygon([(700, 560), (1024, 470), (1024, 560)], fill=(122, 74, 88, 200))
d.polygon([(820, 560), (1024, 500), (1024, 560)], fill=(96, 58, 74, 220))

# ---- cliff + town (right side, stacked houses) ----
d.polygon([(640, 800), (700, 470), (1024, 400), (1024, 800)],
          fill=(146, 84, 62, 255))
d.polygon([(640, 800), (700, 470), (760, 470), (720, 800)],
          fill=(120, 66, 50, 255))
houses = [
    # x, y, w, h, wall, roof
    (760, 430, 90, 70, (250, 240, 214), (178, 84, 52)),
    (860, 415, 80, 78, (246, 230, 198), (168, 76, 48)),
    (945, 430, 79, 64, (250, 238, 210), (178, 84, 52)),
    (720, 520, 100, 76, (248, 236, 208), (172, 80, 50)),
    (830, 505, 86, 84, (252, 242, 218), (180, 86, 54)),
    (925, 520, 99, 70, (246, 232, 200), (170, 78, 48)),
    (690, 620, 110, 80, (250, 238, 212), (176, 82, 52)),
    (810, 610, 96, 88, (248, 234, 204), (172, 80, 50)),
    (915, 625, 109, 74, (252, 240, 216), (178, 84, 52)),
]
for (x, y, w, h, wall, roof) in houses:
    d.rectangle([x, y, x + w, y + h], fill=wall)
    d.polygon([(x - 4, y), (x + w + 4, y), (x + w - 8, y - 16), (x + 8, y - 16)],
              fill=roof)
    # lit windows
    for wx in range(x + 12, x + w - 12, 26):
        for wy in (y + 14, y + 42):
            if wy + 16 <= y + h:
                lit = random.random() < 0.55
                d.rectangle([wx, wy, wx + 12, wy + 16],
                            fill=(255, 214, 120, 255) if lit else (52, 44, 66, 255))
    # tiny arch door
    d.rectangle([x + w // 2 - 8, y + h - 22, x + w // 2 + 8, y + h],
                fill=(72, 52, 60, 255))
# cypress trees
for (x, y, s) in [(735, 470, 46), (905, 455, 52), (985, 470, 44), (700, 600, 40)]:
    d.ellipse([x - s * 0.22, y - s, x + s * 0.22, y], fill=(34, 74, 52, 255))
    d.rectangle([x - 2, y - 4, x + 2, y + 6], fill=(74, 52, 38, 255))
# bougainvillea clusters on the cliff
for (x, y, r) in [(700, 500, 26), (880, 470, 30), (990, 560, 28), (745, 640, 24)]:
    for _ in range(26):
        px = x + random.randint(-r, r)
        py = y + random.randint(-r // 2, r // 2)
        d.ellipse([px - 4, py - 4, px + 4, py + 4],
                  fill=random.choice([(214, 62, 110), (226, 92, 128), (198, 48, 96)]))

# ---- grand staircase (centre-right, descending to the harbour) ----
for i in range(12):
    y = 560 + i * 18
    x0 = 520 - i * 3
    x1 = 620 + i * 2
    d.rectangle([x0, y, x1, y + 11], fill=(240, 214, 164, 255))
    d.rectangle([x0, y + 11, x1, y + 14], fill=(176, 128, 84, 255))
# stair side walls
d.polygon([(520, 560), (500, 776), (520, 776), (538, 560)], fill=(214, 178, 128, 255))
d.polygon([(620, 560), (640, 776), (620, 776), (604, 560)], fill=(214, 178, 128, 255))
# lanterns on the stair walls
for (x, y) in [(506, 600), (520, 680), (634, 620), (624, 700)]:
    d.rectangle([x - 3, y - 12, x + 3, y + 12], fill=(52, 44, 58, 255))
    d.ellipse([x - 8, y - 24, x + 8, y - 8], fill=(255, 214, 120, 255))

# ---- sailboats on the sea ----
def sailboat(cx, cy, s):
    d.polygon([(cx - 34 * s, cy), (cx + 34 * s, cy), (cx + 22 * s, cy + 14 * s),
               (cx - 22 * s, cy + 14 * s)], fill=(72, 44, 40, 255))
    d.rectangle([cx - 2 * s, cy - 62 * s, cx + 2 * s, cy], fill=(52, 40, 36, 255))
    d.polygon([(cx + 4 * s, cy - 58 * s), (cx + 4 * s, cy - 4 * s),
               (cx + 40 * s, cy - 4 * s)], fill=(255, 246, 224, 255))
    d.polygon([(cx - 4 * s, cy - 48 * s), (cx - 4 * s, cy - 4 * s),
               (cx - 30 * s, cy - 4 * s)], fill=(250, 226, 188, 255))
    # reflection
    for i in range(4):
        d.rectangle([cx - 26 * s, cy + 18 * s + i * 6, cx + 26 * s,
                     cy + 21 * s + i * 6], fill=(255, 220, 150, 90 - i * 18))

sailboat(250, 640, 1.0)
sailboat(180, 720, 0.65)

# ---- cafe terrace foreground ----
# balustrade
d.rectangle([0, 800, W, 818], fill=(226, 188, 138, 255))
for x in range(30, W, 46):
    d.rectangle([x, 818, x + 14, 872], fill=(240, 214, 164, 255))
    d.ellipse([x - 2, 812, x + 16, 826], fill=(244, 222, 176, 255))
d.rectangle([0, 872, W, 884], fill=(214, 172, 118, 255))
# round table + two people (left)
d.ellipse([140, 912, 350, 940], fill=(255, 250, 236, 255))
d.rectangle([236, 935, 244, 1000], fill=(120, 88, 60, 255))
# person 1 (straw hat, rust dress)
d.ellipse([176, 872, 212, 908], fill=(52, 40, 36, 255))
d.ellipse([158, 884, 230, 902], fill=(232, 196, 120, 255))
d.polygon([(168, 908), (220, 908), (232, 985), (156, 985)], fill=(178, 84, 52, 255))
# person 2 (dark hair, white shirt)
d.ellipse([262, 874, 296, 908], fill=(40, 32, 30, 255))
d.polygon([(256, 908), (302, 908), (312, 985), (246, 985)], fill=(250, 244, 230, 255))
# wine glasses on the table
for gx in (196, 282):
    d.rectangle([gx, 890, gx + 10, 906], fill=(255, 240, 190, 230))
    d.rectangle([gx + 4, 906, gx + 6, 912], fill=(255, 240, 190, 230))
# potted bougainvillea (right foreground)
d.polygon([(880, 930), (950, 930), (940, 1000), (890, 1000)], fill=(172, 84, 52, 255))
for _ in range(40):
    px = 915 + random.randint(-46, 46)
    py = 900 + random.randint(-34, 10)
    d.ellipse([px - 5, py - 5, px + 5, py + 5],
              fill=random.choice([(214, 62, 110), (226, 92, 128), (198, 48, 96)]))
d.polygon([(60, 930), (130, 930), (122, 1000), (68, 1000)], fill=(172, 84, 52, 255))
for _ in range(26):
    px = 95 + random.randint(-34, 34)
    py = 905 + random.randint(-28, 8)
    d.ellipse([px - 5, py - 5, px + 5, py + 5],
              fill=random.choice([(214, 62, 110), (226, 92, 128)]))

# ---- soft vignette ----
vig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
vd = ImageDraw.Draw(vig)
vd.rectangle([0, 0, W, H], outline=(60, 30, 20, 70), width=26)
img = Image.alpha_composite(img.convert("RGBA"), vig).convert("RGB")
d = ImageDraw.Draw(img, "RGBA")

# ---- cream border + inner rule ----
d.rectangle([0, 0, W - 1, H - 1], outline=(250, 240, 214, 255), width=26)
d.rectangle([34, 34, W - 35, H - 35], outline=(250, 240, 214, 160), width=2)

# ---- title block ----
f_title = ImageFont.truetype(SERIF_B, 118)
f_sub = ImageFont.truetype(SERIF, 36)
text_spaced(d, W // 2, 72, "AURMARA", f_title, (255, 246, 224, 255),
            spacing=10, shadow=(4, 5, (90, 40, 20, 160)))
text_spaced(d, W // 2, 228, "THE HARBOUR OF GOLDEN STAIRS", f_sub,
            (255, 238, 205, 255), spacing=5, shadow=(2, 2, (90, 40, 20, 140)))

img.save(OUT, optimize=True)
print("saved", OUT, img.size)
import os
print("bytes:", os.path.getsize(OUT))
