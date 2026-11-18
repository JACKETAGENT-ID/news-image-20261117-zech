#!/usr/bin/env python3
"""Generate entry.png for make.fun news-image-20261117 (zech).

One cinematic hero scene: the Kerch Bridge at dusk, smoke and drones in the
sky, the Kyiv skyline far away, and a caption strip naming the day plus the
day's headlines. Drawn entirely with PIL primitives - no photos, no fonts
beyond DejaVu shipped with the system.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1024, 1024
BAND_TOP = 760  # caption strip starts here
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def draw_sky(img):
    """Dusk gradient sky, 0..BAND_TOP, with a low sun and glow."""
    d = ImageDraw.Draw(img)
    top = (38, 24, 66)      # deep violet
    mid = (122, 52, 88)     # mauve
    low = (226, 110, 58)    # burnt orange at horizon
    for y in range(BAND_TOP):
        t = y / BAND_TOP
        if t < 0.55:
            c = lerp(top, mid, t / 0.55)
        else:
            c = lerp(mid, low, (t - 0.55) / 0.45)
        d.line([(0, y), (W, y)], fill=c)
    # sun glow + sun, low on the right
    glow = Image.new("RGBA", (W, BAND_TOP), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([640, 300, 940, 600], fill=(255, 190, 90, 70))
    gd.ellipse([690, 350, 890, 550], fill=(255, 220, 140, 120))
    glow = glow.filter(ImageFilter.GaussianBlur(40))
    img.alpha_composite(glow)
    d = ImageDraw.Draw(img)
    d.ellipse([728, 388, 852, 512], fill=(255, 226, 150))
    d.ellipse([742, 402, 838, 498], fill=(255, 240, 190))


def draw_clouds(img):
    """Flat dusk clouds, darker violet bands."""
    d = ImageDraw.Draw(img)
    for cx, cy, rx, ry, shade in [
        (150, 150, 190, 26, (52, 34, 84)),
        (330, 120, 150, 20, (64, 40, 92)),
        (620, 90, 170, 22, (58, 36, 88)),
        (880, 170, 170, 24, (66, 42, 94)),
        (90, 260, 160, 20, (70, 44, 96)),
        (520, 230, 180, 20, (60, 38, 90)),
    ]:
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=shade)


def draw_drones(img):
    """Small drone silhouettes in the sky."""
    d = ImageDraw.Draw(img)
    for cx, cy, s in [(180, 210, 16), (300, 150, 12), (700, 180, 14),
                      (860, 300, 18), (430, 90, 11)]:
        # body + four rotor arms
        d.rectangle([cx - s, cy - s // 3, cx + s, cy + s // 3], fill=(16, 10, 26))
        d.line([(cx - s, cy), (cx - s - 8, cy - 6)], fill=(16, 10, 26), width=3)
        d.line([(cx + s, cy), (cx + s + 8, cy - 6)], fill=(16, 10, 26), width=3)
        d.line([(cx - s, cy), (cx - s - 8, cy + 6)], fill=(16, 10, 26), width=3)
        d.line([(cx + s, cy), (cx + s + 8, cy + 6)], fill=(16, 10, 26), width=3)
        for px, py in [(cx - s - 10, cy - 8), (cx + s + 10, cy - 8),
                       (cx - s - 10, cy + 8), (cx + s + 10, cy + 8)]:
            d.ellipse([px - 5, py - 2, px + 5, py + 2], fill=(16, 10, 26))
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 120, 60))


def draw_smoke(img):
    """Smoke columns rising from the bridge, translucent grey."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for cx, base, hgt, wdt in [(300, 620, 280, 34), (600, 620, 340, 44)]:
        for i in range(5):
            t = i / 4
            y = base - t * hgt
            r = wdt * (0.55 + t * 0.6)
            alpha = int(100 * (1 - t * 0.5))
            d.ellipse([cx - r, y - r * 0.6, cx + r, y + r * 0.6],
                      fill=(120, 110, 130, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(8))
    img.alpha_composite(layer)


def draw_skyline(img):
    """Distant Kyiv skyline silhouette on the horizon, left of centre."""
    d = ImageDraw.Draw(img)
    base = 640
    col = (30, 18, 48)
    buildings = [
        (60, 560, 110, base), (115, 520, 160, base), (165, 575, 205, base),
        (210, 500, 250, base), (255, 565, 300, base), (305, 540, 330, base),
        (335, 585, 380, base), (385, 555, 415, base),
    ]
    for x0, y0, x1, y1 in buildings:
        d.rectangle([x0, y0, x1, y1], fill=col)
    # a domed tower
    d.rectangle([225, 470, 245, 500], fill=col)
    d.ellipse([220, 450, 250, 478], fill=col)
    # tiny lit windows
    for wx in range(70, 410, 18):
        for wy in range(530, 635, 22):
            if (wx * 7 + wy * 3) % 11 < 3:
                d.rectangle([wx, wy, wx + 4, wy + 6], fill=(255, 190, 90))
    d.text((60, 492), "KYIV", font=font("DejaVuSans-Bold.ttf", 22),
           fill=(255, 220, 160))


def draw_bridge(img):
    """Kerch Bridge silhouette across the strait, with a damaged gap."""
    d = ImageDraw.Draw(img)
    col = (18, 12, 30)
    deck_y = 600
    # arch spans
    for x0, x1 in [(0, 260), (300, 560), (600, 860), (900, 1024)]:
        d.arc([x0, deck_y - 90, x1, deck_y + 90], start=180, end=360,
              fill=col, width=14)
    # deck
    d.rectangle([0, deck_y, W, deck_y + 22], fill=col)
    # rail posts
    for x in range(10, W, 34):
        d.rectangle([x, deck_y - 16, x + 5, deck_y], fill=col)
    # piers
    for x in [130, 430, 730, 960]:
        d.rectangle([x - 14, deck_y + 22, x + 14, 700], fill=col)
    # damaged gap: deck broken open, sky showing through, small flames
    d.rectangle([560, deck_y, 640, deck_y + 22], fill=(226, 110, 58))
    d.polygon([(560, deck_y), (575, deck_y + 22), (560, deck_y + 22)],
              fill=col)
    d.polygon([(640, deck_y), (625, deck_y + 22), (640, deck_y + 22)],
              fill=col)
    d.polygon([(592, 600), (600, 566), (608, 600)], fill=(255, 150, 60))
    d.polygon([(596, 600), (600, 582), (604, 600)], fill=(255, 220, 120))
    d.text((665, 545), "KERCH BRIDGE", font=font("DejaVuSans-Bold.ttf", 22),
           fill=(255, 220, 160))


def draw_sea(img):
    """Dark strait water under the bridge with orange reflections."""
    d = ImageDraw.Draw(img)
    for y in range(700, BAND_TOP):
        t = (y - 700) / (BAND_TOP - 700)
        d.line([(0, y), (W, y)], fill=lerp((52, 34, 66), (24, 16, 40), t))
    for i, (x0, x1, y) in enumerate([
        (700, 880, 712), (640, 900, 726), (560, 820, 740),
        (120, 300, 718), (60, 240, 736), (300, 480, 748),
    ]):
        d.line([(x0, y), (x1, y)], fill=(255, 160, 80), width=3)


def draw_caption(img):
    """Bottom strip: the day, then five short headline lines."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, BAND_TOP, W, H], fill=(12, 16, 38))
    d.line([(0, BAND_TOP), (W, BAND_TOP)], fill=(255, 150, 60), width=5)
    d.text((40, BAND_TOP + 18), "TUESDAY, 17 NOVEMBER 2026",
           font=font("DejaVuSans-Bold.ttf", 46), fill=(255, 255, 255))
    d.text((40, BAND_TOP + 72), "THE WORLD IN ONE DAY",
           font=font("DejaVuSans-Bold.ttf", 24), fill=(255, 170, 90))
    lines = [
        "KERCH BRIDGE HIT — DAY 2  ·  KYIV BRIDGES STRUCK",
        "IRAN DRONE HITS U.S. RADAR BASE IN BAHRAIN  ·  TANKER MINED OFF HORMUZ",
        "XI–TRUMP–PUTIN TO MEET IN SHENZHEN, THU 19 NOV",
        "ESTONIA TO SHUT RUSSIA BORDER 1 DEC  ·  UK SANCTIONS 8 ISRAELI FIRMS",
        "JAPAN SCRAMBLES JETS  ·  HOUTHI ADVANCE ON ADEN",
    ]
    y = BAND_TOP + 116
    for line in lines:
        # auto-fit: shrink until the line fits inside the 944 px margin
        size = 24
        while size > 16 and d.textlength(
                line, font=font("DejaVuSans-Bold.ttf", size)) > W - 80:
            size -= 1
        d.text((40, y), line, font=font("DejaVuSans-Bold.ttf", size),
               fill=(235, 235, 245))
        y += 29


def main():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    draw_sky(img)
    draw_clouds(img)
    draw_drones(img)
    draw_smoke(img)
    draw_skyline(img)
    draw_bridge(img)
    draw_sea(img)
    draw_caption(img)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.convert("RGB").save(out, "PNG", optimize=True)
    print(out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
