#!/usr/bin/env python3
"""Render the 24 November 2026 world-news front page.

Fresh implementation: a newspaper front page drawn with Pillow.
Deterministic: fixed fonts, fixed colours, no timestamps, no randomness,
so every run writes byte-identical PNG output.
"""
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (247, 243, 232)
INK = (18, 18, 18)
GREY = (92, 88, 80)
RED = (176, 30, 36)
NAVY = (29, 78, 137)
GREEN = (31, 122, 66)
GOLD = (184, 134, 11)
CARD_BG = (255, 253, 246)
RULE = (200, 192, 172)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to the given pixel width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, color, width, leading):
    lines = wrap(draw, text, fnt, width)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=color)
        y += leading
    return y


# (number, kicker, headline, summary, accent colour)
STORIES = [
    ("02", "CHIPS / SANCTIONS",
     "US blacklists Singapore chip firm Megaspeed",
     "The Nvidia spy scandal's centre joins the Entity List with six others.",
     NAVY),
    ("03", "WAR AT SEA",
     "Ukraine sinks Russian warship off Libya",
     "Seven sea drones sink corvette Merkury off Benghazi; a Ka-27 destroyed.",
     NAVY),
    ("04", "UKRAINE",
     "Russian strike kills at least 15 near Kyiv",
     "Eleven die in a Dymer apartment block; a drone hits a Kyiv tower block.",
     RED),
    ("05", "DIPLOMACY",
     "Zelensky urges four-party peace talks",
     "Kyiv wants Ukraine, Russia, the US and Europe to meet ASAP — from Tuesday.",
     GREEN),
    ("06", "ASIA",
     "Russian warplanes enter South Korea's air zone",
     "Jets fly through the air zone over waters between Korea and Japan.",
     NAVY),
    ("07", "CLIMATE",
     "COP31 collapses in Antalya",
     "No pact after the longest COP ever — the first major failure since 2009.",
     GREEN),
    ("08", "TECH / LAW",
     "Oregon and Virginia sue SpaceX over Grok deepfakes",
     "First state lawsuits over Grok's non-consensual sexual imagery.",
     RED),
    ("09", "MEXICO",
     "Mexico will try 'El Chapo Isidro' at home",
     "The cartel boss faces trial in Mexico despite a US extradition request.",
     GOLD),
    ("10", "INDONESIA",
     "Candy-factory fire kills 24, 30 missing",
     "A Saturday-night blaze at PT Fonusa Agung Mulia in Cikande, Serang.",
     RED),
    ("11", "HEALTH",
     "Bangladesh vaccinates 50 million children",
     "A one-month mass typhoid drive against a drug-resistant strain begins.",
     GREEN),
    ("12", "SPORT",
     "Alcaraz wins his first ATP Finals",
     "The Spaniard beats world No. 1 Zverev 6-2, 7-6 in Turin on Sunday.",
     GOLD),
]


def draw_chip(draw, x, y, w, h):
    """A small chip-and-chart illustration for the lead story."""
    # chart panel
    draw.rectangle([x, y, x + w, y + h], fill=(16, 34, 56), outline=INK, width=2)
    # grid lines
    for i in range(1, 4):
        gy = y + h * i // 4
        draw.line([x + 8, gy, x + w - 8, gy], fill=(48, 84, 120), width=1)
    # rising line chart
    pts = [(x + 14, y + h - 26), (x + w * 0.30, y + h - 52),
           (x + w * 0.52, y + h - 40), (x + w * 0.74, y + h - 78),
           (x + w - 16, y + h - 96)]
    draw.line(pts, fill=(74, 222, 128), width=5, joint="curve")
    # arrowhead
    draw.polygon([(x + w - 16, y + h - 96), (x + w - 34, y + h - 92),
                  (x + w - 22, y + h - 78)], fill=(74, 222, 128))
    # chip body
    cx, cy, cw, chh = x + w // 2 - 52, y + h - 74, 104, 52
    for k in range(4):
        px = cx + 12 + k * 26
        draw.line([px, cy - 8, px, cy], fill=(212, 175, 55), width=4)
        draw.line([px, cy + chh, px, cy + chh + 8], fill=(212, 175, 55), width=4)
    draw.rectangle([cx, cy, cx + cw, cy + chh], fill=(10, 22, 38),
                   outline=(212, 175, 55), width=3)
    draw.rectangle([cx + 30, cy + 14, cx + cw - 30, cy + chh - 14],
                   outline=(212, 175, 55), width=2)
    f = font(SANS_B, 20)
    draw.text((cx + cw // 2, cy + chh // 2), "NVDA", font=f,
              fill=(212, 175, 55), anchor="mm")
    # +31% badge
    bf = font(SANS_B, 30)
    draw.text((x + 16, y + 12), "+31%", font=bf, fill=(74, 222, 128))


def draw_card(draw, x, y, w, h, num, kicker, headline, summary, accent):
    draw.rectangle([x, y, x + w, y + h], fill=CARD_BG, outline=RULE, width=1)
    draw.rectangle([x, y, x + w, y + 4], fill=accent)
    kx = x + 12
    ky = y + 14
    kf = font(SANS_B, 13)
    draw.text((kx, ky), kicker, font=kf, fill=accent)
    nf = font(SERIF, 26)
    draw.text((x + w - 12, ky - 2), num, font=nf, fill=(176, 168, 148),
              anchor="ra")
    hf = font(SERIF, 20)
    hy = para(draw, kx, ky + 22, headline, hf, INK, w - 24, 23)
    sf = font(SANS, 14)
    # never let the summary spill past the card: cap at two lines
    lines = wrap(draw, summary, sf, w - 24)[:2]
    sy = hy + 4
    for ln in lines:
        draw.text((kx, sy), ln, font=sf, fill=GREY)
        sy += 18


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 24  # margin

    # ---- masthead ----
    d.text((W // 2, m + 4), "THE WORLD IN A DAY", font=font(SERIF, 56),
           fill=INK, anchor="ma")
    d.text((W // 2, m + 72), "TUESDAY, 24 NOVEMBER 2026  •  THE DAY IN TWELVE STORIES",
           font=font(SANS_B, 17), fill=RED, anchor="ma")
    d.line([m, m + 106, W - m, m + 106], fill=INK, width=4)
    d.line([m, m + 112, W - m, m + 112], fill=RED, width=2)

    # ---- lead story ----
    ly = m + 126
    lw = 620
    d.text((m, ly), "LEAD  •  MARKETS  •  No. 01", font=font(SANS_B, 15),
           fill=RED)
    d.text((m, ly + 22), "HUANG IS BACK", font=font(SERIF, 62), fill=INK)
    para(d, m, ly + 92,
         "Nvidia reinstates Jensen Huang as chief executive, just 11 days "
         "after he resigned — and its shares surge about 31% in Wall "
         "Street's third-best day ever.",
         font(SERIF_REG, 21), INK, lw, 27)
    d.text((m, ly + 182), "Resigned 12 November  •  Reinstated 24 November  •  +~31%",
           font=font(SANS_B, 15), fill=GREY)
    draw_chip(d, m + lw + 24, ly + 4, W - m * 2 - lw - 24, 186)

    # ---- grid of the other eleven stories ----
    gx, gy = m, ly + 206
    cw = (W - m * 2 - 2 * 12) // 3
    chh = 150
    for i, (num, kicker, headline, summary, accent) in enumerate(STORIES):
        row, col = divmod(i, 3)
        x = gx + col * (cw + 12)
        y = gy + row * (chh + 10)
        draw_card(d, x, y, cw, chh, num, kicker, headline, summary, accent)

    # ---- footer ----
    fy = H - 26
    d.line([m, fy - 10, W - m, fy - 10], fill=INK, width=2)
    d.text((W // 2, fy), "TWELVE STORIES  •  ONE DAY  •  24 NOVEMBER 2026",
           font=font(SANS_B, 14), fill=GREY, anchor="ma")

    img.save(OUT, format="PNG")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
