"""Shared drawing library for the Starlink Mobile explainer (v2).
All paths absolute. Frames are 1920x1080 rendered at 2x and box-reduced.
"""
import math, json, os, re
from functools import lru_cache
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = "/home/claude/v2"
SITE = "/home/claude/starlink-roadmap/index.html"
W, H, SS = 1920, 1080, 2
BG=(7,11,20); PANEL=(14,22,38); LINE=(30,42,62); TEXT=(230,237,247); DIM=(125,140,163)
AMBER=(232,178,58); GREEN=(47,191,113); BLUE=(91,168,255); RED=(214,69,69); PURPLE=(167,139,250)
F = f"{ROOT}/fonts/inter/extras/ttf/"; M = f"{ROOT}/fonts/jbm/fonts/ttf/"

@lru_cache(maxsize=64)
def fnt(s, b=False): return ImageFont.truetype(F + ("Inter-Bold.ttf" if b else "Inter-Regular.ttf"), int(s * SS))
@lru_cache(maxsize=64)
def mono(s, b=False): return ImageFont.truetype(M + ("JetBrainsMono-Bold.ttf" if b else "JetBrainsMono-Regular.ttf"), int(s * SS))

ease = lambda t: t * t * (3 - 2 * t)
clamp = lambda x, a=0.0, b=1.0: max(a, min(b, x))
def fade(t, a, b, d=0.45): return ease(clamp((t - a) / d)) * ease(clamp((b - t) / d))
def al(c, a): return (c[0], c[1], c[2], int(255 * clamp(a)))
def canvas():
    im = Image.new('RGB', (W * SS, H * SS), BG); return im, ImageDraw.Draw(im, 'RGBA')
def out(im): return im.reduce(SS)
def head(d, t, main, sub, t0=0.2, t1=1e9):
    a = fade(t, t0, t1, 0.5)
    d.text((90 * SS, 52 * SS), main, font=fnt(30, True), fill=al(TEXT, a))
    if sub: d.text((90 * SS, 94 * SS), sub, font=mono(15), fill=al(DIM, a))
def panel(d, x0, y0, x1, y1, a=1.0):
    d.rounded_rectangle([x0 * SS, y0 * SS, x1 * SS, y1 * SS], 10 * SS, fill=al(PANEL, a), outline=al(LINE, a), width=2 * SS)
def stat(d, x, y, label, value, vcol=TEXT, vsize=60, a=1.0, suffix=None, ssize=22):
    d.text((x * SS, y * SS), label, font=mono(15), fill=al(DIM, a))
    d.text((x * SS, (y + 30) * SS), value, font=fnt(vsize, True), fill=al(vcol, a))
    if suffix:
        w = d.textlength(value, font=fnt(vsize, True))
        d.text((x * SS + w + 12 * SS, (y + 30 + vsize * 0.72) * SS), suffix, font=mono(ssize), fill=al(DIM, a))
def count(v, fmt="{:,.0f}"): return fmt.format(v)
def pulse(t, period=1.1): return 0.5 + 0.5 * math.sin(2 * math.pi * t / period)
def sat_glyph(d, x, y, a=1.0, s=1.0):
    d.rounded_rectangle([x - 16 * s * SS, y - 10 * s * SS, x + 16 * s * SS, y + 10 * s * SS], 3 * SS, fill=al(TEXT, a))
    for k in (-1, 1):
        d.rectangle([x + k * 36 * s * SS - 14 * s * SS, y - 5 * s * SS, x + k * 36 * s * SS + 14 * s * SS, y + 5 * s * SS], fill=al((120, 150, 190), a))
        d.line([(x + k * 16 * s * SS, y), (x + k * 22 * s * SS, y)], fill=al((150, 170, 200), a), width=2 * SS)
def phone_glyph(d, x, y, a=1.0, s=1.0):
    d.rounded_rectangle([x - 18 * s * SS, y - 34 * s * SS, x + 18 * s * SS, y + 34 * s * SS], 6 * SS, fill=al(TEXT, a))

_MARKS = None
def beat(scene, i):
    global _MARKS
    if _MARKS is None: _MARKS = json.load(open(f"{ROOT}/marks.json"))
    b = _MARKS[scene]["beats"][i]; return b[0], b[1]
def dur(scene):
    global _MARKS
    if _MARKS is None: _MARKS = json.load(open(f"{ROOT}/marks.json"))
    return _MARKS[scene]["dur"]

# ---------- CONUS data embedded in the site ----------
@lru_cache(maxsize=1)
def site_src(): return open(SITE, encoding='utf-8', errors='replace').read()
@lru_cache(maxsize=1)
def conus():
    s = site_src()
    hexs = s.split('US_DENS = {')[1].split('hex: "')[1].split('"')[0]
    GW, GH, CELL = 129, 70, 40
    dens = np.full(GW * GH, -1.0)
    for i in range(GW * GH):
        v = int(hexs[i * 2:i * 2 + 2], 16)
        if v != 255: dens[i] = 10 ** (v / 254 * 6.5 - 2)
    dens = dens.reshape(GH, GW)
    MIDX = s.split('US_MIDX = "')[1].split('"')[0]
    midx = np.array([int(MIDX[i * 2:i * 2 + 2], 16) for i in range(GW * GH)]).reshape(GH, GW)
    states = json.loads(s.split('US_STATES = ')[1].split(';\n')[0])
    path = re.search(r'CONUS_PATH = "([^"]+)"', s).group(1)
    return dens, midx, states, path, GW, GH, CELL

def parse_path(dd, P):
    o = []
    for sub in dd.split('M')[1:]:
        pts = []
        for tok in sub.replace('Z', '').split('L'):
            tok = tok.strip()
            if tok:
                a, b = tok.split(','); pts.append(P(float(a), float(b)))
        if len(pts) > 2: o.append(pts)
    return o

def render_range(frame, scene, a, b):
    d = f"{ROOT}/frames/{scene}"; os.makedirs(d, exist_ok=True)
    for n in range(int(a * 30), int(b * 30)): frame(n / 30.0).save(f"{d}/f{n:05d}.png", compress_level=1)
    print(scene, int(a * 30), "→", int(b * 30))
