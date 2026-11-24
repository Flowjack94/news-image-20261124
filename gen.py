#!/usr/bin/env python3
"""news-image-20261124 — draw a newspaper front page summing up the world's
news of Tuesday 24 November 2026. Deterministic: fixed text, fixed layout,
fixed palette, no network, no time, no randomness. Writes entry.png (1024x1024).
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 241, 230)
INK = (20, 20, 20)
RED = (164, 31, 31)
NAVY = (29, 42, 74)
TAN = (236, 227, 205)
DARK = (38, 34, 30)
GRAY = (90, 86, 78)
ORANGE = (226, 88, 34)
YELLOW = (242, 160, 7)
FLAME = (255, 207, 63)

FD = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FD + name, size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap measured with the real font."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, fill=INK, leading=None):
    """Draw wrapped paragraph; return y after last line."""
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hrule(draw, x0, x1, y, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_flame(draw, cx, base_y, s):
    """Layered flame polygons, s = scale."""
    # outer flame
    draw.polygon([
        (cx, base_y - 3.4 * s),
        (cx + 1.1 * s, base_y - 1.6 * s),
        (cx + 1.5 * s, base_y - 0.4 * s),
        (cx + 0.7 * s, base_y),
        (cx - 0.7 * s, base_y),
        (cx - 1.5 * s, base_y - 0.4 * s),
        (cx - 1.1 * s, base_y - 1.6 * s),
    ], fill=ORANGE)
    # inner flame
    draw.polygon([
        (cx, base_y - 2.3 * s),
        (cx + 0.7 * s, base_y - 1.1 * s),
        (cx + 0.9 * s, base_y - 0.2 * s),
        (cx - 0.9 * s, base_y - 0.2 * s),
        (cx - 0.7 * s, base_y - 1.1 * s),
    ], fill=YELLOW)
    # core
    draw.polygon([
        (cx, base_y - 1.4 * s),
        (cx + 0.45 * s, base_y - 0.5 * s),
        (cx - 0.45 * s, base_y - 0.5 * s),
    ], fill=FLAME)


def draw_factory(draw, x0, y0, x1, y1):
    """Burning factory silhouette inside box (x0,y0)-(x1,y1)."""
    draw.rectangle([x0, y0, x1, y1], fill=DARK)
    # buildings
    draw.rectangle([x0 + 18, y1 - 78, x0 + 118, y1 - 8], fill=(12, 11, 10))
    draw.rectangle([x0 + 128, y1 - 108, x0 + 218, y1 - 8], fill=(12, 11, 10))
    draw.rectangle([x0 + 228, y1 - 62, x0 + 300, y1 - 8], fill=(12, 11, 10))
    # chimneys
    draw.rectangle([x0 + 48, y1 - 128, x0 + 66, y1 - 78], fill=(12, 11, 10))
    draw.rectangle([x0 + 168, y1 - 158, x0 + 186, y1 - 108], fill=(12, 11, 10))
    # smoke
    for cx, cy, r in [(x0 + 57, y1 - 142, 12), (x0 + 70, y1 - 158, 16),
                      (x0 + 177, y1 - 172, 12), (x0 + 190, y1 - 190, 16),
                      (x0 + 205, y1 - 206, 11)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 116, 108))
    # flames on roofs
    draw_flame(draw, x0 + 68, y1 - 76, 13)
    draw_flame(draw, x0 + 173, y1 - 106, 17)
    draw_flame(draw, x0 + 264, y1 - 60, 11)
    # windows (lit)
    for wx in (x0 + 34, x0 + 62, x0 + 90):
        draw.rectangle([wx, y1 - 56, wx + 12, y1 - 40], fill=YELLOW)
    for wx in (x0 + 144, x0 + 172, x0 + 200):
        draw.rectangle([wx, y1 - 84, wx + 12, y1 - 68], fill=YELLOW)


def draw_ship(draw, cx, cy, s):
    """Small cargo ship with a flame, centred near (cx, cy)."""
    # flame above
    draw_flame(draw, cx + 0.6 * s, cy - 1.1 * s, 0.45 * s)
    # hull
    draw.polygon([(cx - 1.6 * s, cy - 0.2 * s), (cx + 1.6 * s, cy - 0.2 * s),
                  (cx + 1.1 * s, cy + 0.5 * s), (cx - 1.1 * s, cy + 0.5 * s)],
                 fill=NAVY)
    # containers
    draw.rectangle([cx - 1.1 * s, cy - 0.9 * s, cx - 0.2 * s, cy - 0.2 * s], fill=RED)
    draw.rectangle([cx - 0.1 * s, cy - 0.9 * s, cx + 0.8 * s, cy - 0.2 * s], fill=ORANGE)
    # mast
    draw.line([(cx + 1.1 * s, cy - 0.2 * s), (cx + 1.1 * s, cy - 1.2 * s)],
              fill=INK, width=3)
    # waves
    for wy in (cy + 0.75 * s, cy + 1.05 * s):
        draw.arc([cx - 1.7 * s, wy - 0.25 * s, cx - 0.5 * s, wy + 0.25 * s],
                 200, 340, fill=(70, 110, 150), width=3)
        draw.arc([cx - 0.2 * s, wy - 0.25 * s, cx + 1.0 * s, wy + 0.25 * s],
                 200, 340, fill=(70, 110, 150), width=3)
        draw.arc([cx + 1.0 * s, wy - 0.25 * s, cx + 1.8 * s, wy + 0.25 * s],
                 200, 340, fill=(70, 110, 150), width=3)


def draw_globe(draw, cx, cy, r):
    """Small globe: blue circle, green land blobs, white meridian arcs."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(52, 110, 165))
    draw.ellipse([cx - 0.55 * r, cy - 0.75 * r, cx + 0.15 * r, cy - 0.05 * r],
                 fill=(74, 140, 74))
    draw.ellipse([cx - 0.1 * r, cy + 0.1 * r, cx + 0.6 * r, cy + 0.7 * r],
                 fill=(74, 140, 74))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=2)
    draw.arc([cx - r, cy - r, cx + r, cy + r], 90, 270, fill=(255, 255, 255), width=2)
    draw.ellipse([cx - 0.35 * r, cy - r, cx + 0.35 * r, cy + r],
                 outline=(255, 255, 255), width=2)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=(255, 255, 255), width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 30
    R = W - M  # right edge 994

    # ---------- masthead ----------
    title = "THE WORLD TODAY"
    tf = font(SERIF_B, 82)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 14), title, font=tf, fill=INK)
    hrule(d, M, R, 116, 3)
    hrule(d, M, R, 122, 1)
    date = "TUESDAY  24 NOVEMBER 2026"
    df = font(SANS_B, 32)
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 130), date, font=df, fill=RED)
    hrule(d, M, R, 172, 3)

    # ---------- lead: Indonesia factory fire ----------
    y = 188
    kf = font(SANS_B, 23)
    d.text((M, y), "INDONESIA  —  BANTEN", font=kf, fill=RED)
    hf = font(SERIF_B, 50)
    d.text((M, y + 34), "FACTORY FIRE KILLS", font=hf, fill=INK)
    d.text((M, y + 92), "AT LEAST 24", font=hf, fill=INK)
    bf = font(SANS, 23)
    para(d, M, y + 158,
         "A candy factory blaze leaves about 30 people missing as rescuers "
         "search the ruins.", bf, 600)
    # illustration + stat panel, right
    px0, py0, px1, py1 = 668, 188, R, 400
    draw_factory(d, px0, py0, px1, py1 - 44)
    d.rectangle([px0, py1 - 44, px1, py1], fill=RED)
    stat = "24 DEAD  ·  ~30 MISSING"
    ssize = 24
    while ssize > 14:
        sf = font(SANS_B, ssize)
        if d.textlength(stat, font=sf) <= (px1 - px0) - 16:
            break
        ssize -= 1
    sw = d.textlength(stat, font=sf)
    d.text((px0 + (px1 - px0 - sw) / 2, py1 - 38), stat, font=sf, fill=(255, 255, 255))
    hrule(d, M, R, 416, 2)

    # ---------- row 2: war at sea / COP31 ----------
    y = 430
    col_w = 464
    # left: Ukraine war
    d.text((M, y), "UKRAINE WAR", font=kf, fill=RED)
    d.text((M, y + 30), "WAR SPREADS", font=font(SERIF_B, 38), fill=INK)
    d.text((M, y + 74), "TO THE SEAS", font=font(SERIF_B, 38), fill=INK)
    para(d, M, y + 118,
         "Sparta II burns in the Gulf of Finland after a drone strike. "
         "Corvette Merkury destroyed at Benghazi, Libya. Kyiv region hit; "
         "several missing.",
         font(SANS, 19), col_w)
    draw_ship(d, 430, y + 52, 26)
    # divider
    d.line([(512, 430), (512, 642)], fill=GRAY, width=1)
    # right: COP31
    x2 = 534
    d.text((x2, y), "CLIMATE  —  COP31 ANTALYA", font=kf, fill=RED)
    d.text((x2, y + 30), "NO DEAL IN", font=font(SERIF_B, 38), fill=INK)
    d.text((x2, y + 74), "ANTALYA", font=font(SERIF_B, 38), fill=INK)
    para(d, x2, y + 118,
         "The climate summit ends with no fossil-fuel phase-out language, "
         "as nations split over the final text.",
         font(SANS, 19), col_w)
    draw_globe(d, 920, y + 52, 34)
    hrule(d, M, R, 642, 2)

    # ---------- row 3: three columns ----------
    y = 656
    cols = [
        ("MARKETS", "NVIDIA ADDS NEARLY $1 TRILLION",
         "Jensen Huang's chipmaker surges; tech stocks rally."),
        ("UNITED STATES", "COURT CLEARS WAY TO ERASE TRUMP VERDICT",
         "Court clears the way to erase the Trump verdict."),
        ("PORTUGAL", "THOUSANDS MARCH IN LISBON",
         "Protesters rally against the rising cost of living."),
    ]
    cw = 306
    xs = [M, 359, 688]
    kf3 = font(SANS_B, 19)
    hf3 = font(SERIF_B, 27)
    bf3 = font(SANS, 18)
    for (kicker, head, body), x in zip(cols, xs):
        d.text((x, y), kicker, font=kf3, fill=RED)
        yy = y + 28
        for line in wrap(d, head, hf3, cw):
            d.text((x, yy), line, font=hf3, fill=INK)
            yy += 33
        para(d, x, yy + 4, body, bf3, cw, leading=23)
    hrule(d, M, R, 846, 2)

    # ---------- also today ----------
    y = 858
    d.rectangle([M, y, R, y + 36], fill=INK)
    af = font(SANS_B, 20)
    d.text((M + 12, y + 6), "ALSO TODAY", font=af, fill=(255, 255, 255))
    y = 906
    half = 470
    sf2 = font(SANS_B, 19)
    bf2 = font(SANS, 18)
    d.text((M, y), "SPORT", font=sf2, fill=RED)
    para(d, M, y + 26,
         "Verstappen wins the Las Vegas GP. Alcaraz beats Zverev for the ATP "
         "Finals crown. Pant hits 128 vs New Zealand. World Chess: Gukesh v "
         "Sindarov opens in Geneva.",
         bf2, half, leading=23)
    d.text((534, y), "WORLD", font=sf2, fill=RED)
    para(d, 534, y + 26,
         "Modi and Nepal PM Shah open the Saryu–Kamala Express. BepiColombo "
         "enters Mercury orbit. Denmark's top court backs the 'ghetto law'. "
         "Myanmar criticises ASEAN.",
         bf2, half, leading=23)

    img.save("entry.png", "PNG", optimize=True)


if __name__ == "__main__":
    main()
