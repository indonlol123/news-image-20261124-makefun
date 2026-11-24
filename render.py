#!/usr/bin/env python3
"""Draw the front page of THE WORLD IN A DAY for Tuesday 24 November 2026.

A one-page newspaper front page, 1024x1024, drawn from scratch with Pillow.
No network, no randomness, no clock: the same run always writes the same
bytes. Run:  python3 render.py   (writes entry.png beside this file)
"""
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (248, 244, 233)      # warm newsprint
INK = (20, 20, 20)           # near-black type
FAINT = (107, 101, 90)       # grey for datelines and footers
RULE = (20, 20, 20)
BLUE = (29, 78, 137)
RED = (158, 27, 27)
DARKRED = (122, 31, 31)
OCHRE = (138, 90, 0)
GREEN = (46, 107, 52)
TEAL = (15, 107, 92)
PURPLE = (91, 45, 142)
NAVY = (39, 68, 114)
ORANGE = (179, 84, 30)
LEAD_BG = (238, 232, 214)    # slightly darker panel behind the lead story

# ---------------------------------------------------------------- stories
# Each story: (kicker, colour, headline, summary, icon key).
# All twelve are events of Tuesday 24 November 2026, lead first.
LEAD = (
    "TECHNOLOGY  ·  THE LEAD STORY",
    BLUE,
    "HUANG IS BACK AT NVIDIA",
    "Nvidia reinstates Jensen Huang as chief executive, just 11 days after "
    "he resigned in an espionage scandal. Shares jump 31% and lift the "
    "whole US market.",
    "chip",
    "Wall Street's best day since April 2024: the S&P 500 rose 4.7% "
    "and the Dow 3%.",
)

STORIES = [
    ("TECHNOLOGY", BLUE,
     "US BLACKLISTS CHIP FIRM MEGASPEED",
     "Washington bars US firms from dealing with the Singapore firm in "
     "the Nvidia spy case.",
     "ban"),
    ("MIDDLE EAST", RED,
     "IRAN STRIKES GULF SITES AS US SQUEEZES",
     "Tehran hits US bases and Gulf sites and sues for $290bn as a US "
     "naval blockade bites.",
     "burst"),
    ("ASIA", OCHRE,
     "RUSSIAN JETS ENTER KOREA'S AIR ZONE",
     "Seoul scrambles fighters and warns Ulleung Island after Russian "
     "jets enter its air zone.",
     "jet"),
    ("THE WAR", DARKRED,
     "UKRAINE SINKS RUSSIAN WARSHIP OFF LIBYA",
     "Kyiv says it sank a Russian warship off Libya; Moscow vows to "
     "answer the strike.",
     "ship"),
    ("THE WAR", DARKRED,
     "DRONE STRIKE ON KYIV TOWN KILLS 11",
     "A boy is pulled alive from the rubble after a Russian drone attack "
     "on a town near Kyiv.",
     "flame"),
    ("LAW", PURPLE,
     "STATES SUE SPACEX OVER GROK IMAGES",
     "Virginia and Oregon say Grok, the X chatbot, made sexual images of "
     "real people.",
     "gavel"),
    ("THE AMERICAS", GREEN,
     "MEXICO CAPTURES 'EL CHAPO ISIDRO'",
     "Mexico holds the alleged drug lord and says it will try him at "
     "home, not extradite him.",
     "badge"),
    ("CLIMATE", TEAL,
     "COP31 CLIMATE TALKS END WITH NO DEAL",
     "Talks in Antalya collapse without a pact; Pacific island nations "
     "call it a betrayal.",
     "globe"),
    ("EUROPE", NAVY,
     "SPAIN'S RIGHT SET TO OUST SANCHEZ",
     "Polls put the right on course to beat Pedro Sanchez in Sunday's "
     "general election.",
     "ballot"),
    ("HEALTH", GREEN,
     "BANGLADESH TO VACCINATE 50M CHILDREN",
     "A month-long drive targets drug-resistant typhoid in one of the "
     "world's biggest campaigns.",
     "syringe"),
    ("SPORT", ORANGE,
     "ALCARAZ WINS FIRST ATP FINALS CROWN",
     "The Spaniard beats Alexander Zverev in the final to take his first "
     "season-ending title.",
     "ball"),
]

NUMBERS = [
    ("NASDAQ", "+6.5%"),
    ("NVIDIA", "+31%"),
    ("CROWDSTRIKE BUYS ZSCALER", "$44BN"),
    ("SOFTBANK TO INVEST IN INTEL", "$2BN"),
]

# ------------------------------------------------------------------ fonts
def _font(name, size):
    """First matching font file wins; falls back to Pillow's built-in."""
    candidates = [
        f"/usr/share/fonts/truetype/noto/{name}.ttf",
        f"/usr/share/fonts/truetype/dejavu/{name}.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def fonts():
    return {
        "masthead": _font("NotoSerif-Bold", 58),
        "dateline": _font("NotoSans-Bold", 19),
        "kicker": _font("NotoSans-Bold", 16),
        "lead_head": _font("NotoSerif-Bold", 40),
        "lead_body": _font("NotoSans", 18),
        "head": _font("NotoSerif-Bold", 19),
        "body": _font("NotoSans", 15),
        "num_label": _font("NotoSans-Bold", 14),
        "num_value": _font("NotoSans-Bold", 17),
        "footer": _font("NotoSans", 13),
    }


def wrap(draw, text, font, width):
    """Greedy word wrap measured in pixels; returns a list of lines."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        line = words[0]
        for word in words[1:]:
            trial = line + " " + word
            if draw.textlength(trial, font=font) <= width:
                line = trial
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


def text_height(draw, lines, font, leading):
    if not lines:
        return 0
    ascent, descent = font.getmetrics()
    return len(lines) * leading - (leading - (ascent + descent))

# ------------------------------------------------------------------ icons
# Small 34x34 pictograms, drawn with plain lines and shapes in one colour.
# Each takes the draw context, the top-left corner and the colour.
def _icon_chip(d, x, y, c):
    d.rectangle([x + 8, y + 8, x + 26, y + 26], outline=c, width=3)
    d.rectangle([x + 14, y + 14, x + 20, y + 20], fill=c)
    for i in (12, 17, 22):
        d.line([x + i, y + 2, x + i, y + 8], fill=c, width=2)
        d.line([x + i, y + 26, x + i, y + 32], fill=c, width=2)
        d.line([x + 2, y + i, x + 8, y + i], fill=c, width=2)
        d.line([x + 26, y + i, x + 32, y + i], fill=c, width=2)


def _icon_ban(d, x, y, c):
    d.ellipse([x + 3, y + 3, x + 31, y + 31], outline=c, width=3)
    d.line([x + 7, y + 27, x + 27, y + 7], fill=c, width=3)


def _icon_burst(d, x, y, c):
    cx, cy = x + 17, y + 17
    for k in range(8):
        ang = k * 3.14159 / 4
        dx, dy = int(13 * _cos(ang)), int(13 * _sin(ang))
        d.line([cx, cy, cx + dx, cy + dy], fill=c, width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=c)


def _cos(a):
    import math
    return math.cos(a)


def _sin(a):
    import math
    return math.sin(a)


def _icon_jet(d, x, y, c):
    d.polygon([(x + 17, y + 3), (x + 22, y + 20), (x + 17, y + 16),
               (x + 12, y + 20)], fill=c)
    d.polygon([(x + 12, y + 20), (x + 4, y + 30), (x + 12, y + 24)], fill=c)
    d.polygon([(x + 22, y + 20), (x + 30, y + 30), (x + 22, y + 24)], fill=c)
    d.polygon([(x + 15, y + 24), (x + 19, y + 24), (x + 17, y + 31)], fill=c)


def _icon_ship(d, x, y, c):
    d.polygon([(x + 4, y + 20), (x + 30, y + 20), (x + 25, y + 29),
               (x + 9, y + 29)], fill=c)
    d.line([x + 17, y + 4, x + 17, y + 20], fill=c, width=3)
    d.polygon([(x + 17, y + 6), (x + 27, y + 14), (x + 17, y + 14)], fill=c)


def _icon_flame(d, x, y, c):
    d.polygon([(x + 17, y + 3), (x + 26, y + 16), (x + 22, y + 16),
               (x + 28, y + 24), (x + 17, y + 31), (x + 6, y + 24),
               (x + 12, y + 16), (x + 8, y + 16)], fill=c)


def _icon_gavel(d, x, y, c):
    d.line([x + 8, y + 27, x + 26, y + 9], fill=c, width=4)
    d.rectangle([x + 4, y + 6, x + 14, y + 12], fill=c)
    d.rectangle([x + 20, y + 18, x + 30, y + 24], fill=c)
    d.line([x + 4, y + 30, x + 16, y + 30], fill=c, width=3)


def _icon_badge(d, x, y, c):
    cx, cy = x + 17, y + 16
    pts = []
    for k in range(10):
        r = 13 if k % 2 == 0 else 6
        ang = -1.5708 + k * 0.6283
        pts.append((cx + r * _cos(ang), cy + r * _sin(ang)))
    d.polygon(pts, outline=c, width=2)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=c)
    d.polygon([(cx - 2, cy + 12), (cx + 2, cy + 12), (cx + 5, cy + 22),
               (cx - 5, cy + 22)], fill=c)


def _icon_globe(d, x, y, c):
    d.ellipse([x + 3, y + 3, x + 31, y + 31], outline=c, width=3)
    d.ellipse([x + 11, y + 3, x + 23, y + 31], outline=c, width=2)
    d.line([x + 3, y + 17, x + 31, y + 17], fill=c, width=2)
    d.arc([x + 3, y + 8, x + 31, y + 26], 200, 340, fill=c, width=2)


def _icon_ballot(d, x, y, c):
    d.rectangle([x + 5, y + 12, x + 29, y + 30], outline=c, width=3)
    d.line([x + 5, y + 12, x + 17, y + 5], fill=c, width=2)
    d.line([x + 29, y + 12, x + 17, y + 5], fill=c, width=2)
    d.line([x + 11, y + 21, x + 15, y + 25], fill=c, width=3)
    d.line([x + 15, y + 25, x + 24, y + 15], fill=c, width=3)


def _icon_syringe(d, x, y, c):
    d.line([x + 6, y + 28, x + 22, y + 12], fill=c, width=4)
    d.rectangle([x + 18, y + 8, x + 28, y + 18], outline=c, width=2)
    d.line([x + 26, y + 4, x + 30, y + 8], fill=c, width=3)
    d.line([x + 4, y + 26, x + 8, y + 30], fill=c, width=3)
    d.line([x + 10, y + 20, x + 14, y + 24], fill=c, width=2)
    d.line([x + 14, y + 16, x + 18, y + 20], fill=c, width=2)


def _icon_ball(d, x, y, c):
    d.ellipse([x + 3, y + 3, x + 31, y + 31], outline=c, width=3)
    d.arc([x + 3, y + 3, x + 31, y + 31], 300, 60, fill=c, width=2)
    d.arc([x + 3, y + 3, x + 31, y + 31], 120, 240, fill=c, width=2)


ICONS = {
    "chip": _icon_chip, "ban": _icon_ban, "burst": _icon_burst,
    "jet": _icon_jet, "ship": _icon_ship, "flame": _icon_flame,
    "gavel": _icon_gavel, "badge": _icon_badge, "globe": _icon_globe,
    "ballot": _icon_ballot, "syringe": _icon_syringe, "ball": _icon_ball,
}


def draw_icon(d, key, x, y, colour):
    fn = ICONS.get(key)
    if fn:
        fn(d, x, y, colour)

# ----------------------------------------------------------------- layout
MARGIN = 26
COL_W = 312
COL_GAP = 12
ROW_H = 140
ROW_GAP = 10
GRID_TOP = 372


def draw_masthead(d, f):
    title = "THE WORLD IN A DAY"
    tw = d.textlength(title, font=f["masthead"])
    d.text(((W - tw) / 2, 28), title, font=f["masthead"], fill=INK)
    dateline = "TUESDAY, 24 NOVEMBER 2026   ·   ONE DAY, ONE PAGE, TWELVE STORIES"
    tw = d.textlength(dateline, font=f["dateline"])
    d.text(((W - tw) / 2, 102), dateline, font=f["dateline"], fill=FAINT)
    d.line([MARGIN, 130, W - MARGIN, 130], fill=RULE, width=3)
    d.line([MARGIN, 136, W - MARGIN, 136], fill=RULE, width=1)


def draw_lead_chip(d, x0, y0, x1, y1):
    """The lead illustration: a microchip with a rising market arrow."""
    # chip body
    d.rectangle([x0 + 30, y0 + 25, x0 + 130, y0 + 125], outline=BLUE, width=5)
    d.rectangle([x0 + 62, y0 + 57, x0 + 98, y0 + 93], fill=BLUE)
    for i in (48, 80, 112):
        d.line([x0 + i, y0 + 8, x0 + i, y0 + 25], fill=BLUE, width=3)
        d.line([x0 + i, y0 + 125, x0 + i, y0 + 142], fill=BLUE, width=3)
        d.line([x0 + 13, y0 + i, x0 + 30, y0 + i], fill=BLUE, width=3)
        d.line([x0 + 130, y0 + i, x0 + 147, y0 + i], fill=BLUE, width=3)
    # rising arrow across the chip's right side
    pts = [(x0 + 150, y0 + 128), (x0 + 185, y0 + 95), (x0 + 205, y0 + 108),
           (x0 + 255, y0 + 45)]
    d.line(pts, fill=GREEN, width=6, joint="curve")
    d.polygon([(x0 + 255, y0 + 45), (x0 + 232, y0 + 48), (x0 + 250, y0 + 68)],
              fill=GREEN)
    f_big = _font("NotoSans-Bold", 30)
    d.text((x0 + 185, y0 + 128), "+31%", font=f_big, fill=GREEN)


def draw_lead(d, f):
    d.rectangle([MARGIN, 146, W - MARGIN, 354], fill=LEAD_BG)
    kicker, colour, head, body, _icon, note = LEAD
    d.text((MARGIN + 18, 160), kicker, font=f["kicker"], fill=colour)
    d.text((MARGIN + 18, 186), head, font=f["lead_head"], fill=INK)
    lines = wrap(d, body, f["lead_body"], 600)
    y = 244
    for line in lines:
        d.text((MARGIN + 18, y), line, font=f["lead_body"], fill=INK)
        y += 24
    note_lines = wrap(d, note, f["body"], 600)
    y += 10
    for line in note_lines:
        d.text((MARGIN + 18, y), line, font=f["body"], fill=FAINT)
        y += 19
    draw_lead_chip(d, 668, 168, 998, 354)
    d.line([MARGIN, 364, W - MARGIN, 364], fill=RULE, width=1)


def draw_cell(d, f, x, y, story):
    kicker, colour, head, body, icon = story
    d.line([x, y, x + COL_W, y], fill=colour, width=2)
    d.text((x, y + 8), kicker, font=f["kicker"], fill=colour)
    draw_icon(d, icon, x + COL_W - 34, y + 6, colour)
    head_lines = wrap(d, head, f["head"], COL_W - 42)
    yy = y + 32
    for line in head_lines[:2]:
        d.text((x, yy), line, font=f["head"], fill=INK)
        yy += 24
    body_lines = wrap(d, body, f["body"], COL_W)
    for line in body_lines[:2]:
        d.text((x, yy), line, font=f["body"], fill=INK)
        yy += 19


def draw_numbers(d, f, x, y):
    d.line([x, y, x + COL_W, y], fill=INK, width=2)
    d.text((x, y + 8), "BY THE NUMBERS", font=f["kicker"], fill=INK)
    yy = y + 34
    for label, value in NUMBERS:
        d.text((x, yy), label, font=f["num_label"], fill=INK)
        vw = d.textlength(value, font=f["num_value"])
        d.text((x + COL_W - vw, yy - 2), value, font=f["num_value"],
               fill=GREEN)
        yy += 26


def draw_footer(d, f):
    note = ("THE WORLD IN A DAY  ·  TUESDAY 24 NOVEMBER 2026  ·  "
            "DRAWN FROM THE DAY'S REPORTING")
    tw = d.textlength(note, font=f["footer"])
    d.text(((W - tw) / 2, 978), note, font=f["footer"], fill=FAINT)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    f = fonts()
    draw_masthead(d, f)
    draw_lead(d, f)
    cols = [MARGIN, MARGIN + COL_W + COL_GAP, MARGIN + 2 * (COL_W + COL_GAP)]
    rows = [GRID_TOP + i * (ROW_H + ROW_GAP) for i in range(4)]
    for i, story in enumerate(STORIES):
        row, col = divmod(i, 3)
        draw_cell(d, f, cols[col], rows[row], story)
    draw_numbers(d, f, cols[2], rows[3])
    draw_footer(d, f)
    img.save(OUT, format="PNG")
    return OUT


if __name__ == "__main__":
    print(build())
