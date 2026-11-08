"""Bhai Dooj cinematic festive reel (8 Nov; user ref reel DfcvscghAvp). User-made AI images (tilak.png, thali.png).
Slow push-ins, diya glow flicker, rising golden embers, script title, soft dissolves, 2.6 s brand end card. Silent (user adds song)."""
import sys, math, random
sys.path.insert(0, '/home/claude/series')
from engine import *
from PIL import ImageFont, ImageFilter, ImageEnhance
OUT = sys.argv[1]
FD = '/home/claude/fonts/'
SCRIPT = lambda s: ImageFont.truetype(FD + 'GreatVibes-Regular.ttf', s)
def CIN(s, w=600):
    f = ImageFont.truetype(FD + 'Cinzel-VF.ttf', s)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f
MB = lambda s: ImageFont.truetype(FD + 'Mukta-Bold.ttf', s)
GOLD, CREAM = (255, 214, 140), (255, 246, 228)
D = '/home/claude/series/bhaidooj/'
TIL = Image.open(D + 'tilak.png').convert('RGB').resize((W, H), Image.LANCZOS)
THA = Image.open(D + 'thali.png').convert('RGB').resize((W, H), Image.LANCZOS)
sx = W / 941
DIYAS_TIL = [(550, 676), (395, 1302), (405, 1335), (475, 1295), (600, 1290), (915, 1300), (330, 1320), (1030, 1490), (290, 1500)]
DIYAS_THA = [(300 * sx, 470 * sx)]
S1, S2, S3, TOTAL, XF = 0.0, 6.2, 11.8, 14.6, 0.7
_L = Image.open('/home/claude/ruyan_automation/logo.png').convert('RGBA')
LOGO = Image.new('RGBA', _L.size, GOLD + (0,)); LOGO.putalpha(_L.getchannel('A'))
rng = random.Random(7)
EMBERS = [(rng.uniform(0, W), rng.uniform(0, H), rng.uniform(18, 60), rng.uniform(2, 5), rng.uniform(0, 6.28)) for _ in range(90)]

def push(img, t, t0, dur, z0, z1, fx=0.5, fy=0.5):
    q = min(1, max(0, (t - t0) / dur)); q = q * q * (3 - 2 * q)
    z = z0 + (z1 - z0) * q; cw, ch = W / z, H / z
    x0 = (W - cw) * fx; y0 = (H - ch) * fy
    return img.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.LANCZOS), z, x0, y0

def glows(im, t, pts, z, x0, y0, base=70):
    g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(g)
    for i, (px, py) in enumerate(pts):
        X = (px - x0) * z; Y = (py - y0) * z
        f = 0.75 + 0.25 * math.sin(t * 9 + i * 1.7) * math.sin(t * 5.3 + i)
        r = base * f
        d.ellipse((X - r, Y - r * 1.2, X + r, Y + r * 0.8), fill=(255, 170, 70, int(70 * f)))
    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(28)))

def embers(im, t, a=1.0):
    g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(g)
    for x, y, sp, s, ph in EMBERS:
        yy = (y - sp * t * 2.2) % H; xx = x + 18 * math.sin(t * 0.8 + ph)
        al = int(a * 150 * (0.5 + 0.5 * math.sin(t * 3 + ph)))
        d.ellipse((xx - s, yy - s, xx + s, yy + s), fill=(255, 200, 110, al))
    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(1.2)))

def gtext(im, cx, y, txt, f, col, a, glow=True):
    if a <= 0: return
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    tw = d.textlength(txt, font=f); x = cx - tw / 2
    if glow:
        gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(gl).text((x, y), txt, font=f, fill=(255, 160, 60, 200))
        lay.alpha_composite(gl.filter(ImageFilter.GaussianBlur(14)))
        sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).text((x + 3, y + 4), txt, font=f, fill=(40, 10, 0, 160))
        lay.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4)))
    ImageDraw.Draw(lay).text((x, y), txt, font=f, fill=col + (255,))
    lay.putalpha(lay.getchannel('A').point(lambda v: int(v * a)))
    im.alpha_composite(lay)

def topshade(im, a=150, h=620):
    g = Image.new('RGBA', (W, h), (0, 0, 0, 0)); d = ImageDraw.Draw(g)
    for y in range(h): d.line((0, y, W, y), fill=(25, 8, 2, int(a * (1 - y / h) ** 1.6)))
    im.alpha_composite(g, (0, 0))

def scene1(t):
    img, z, x0, y0 = push(TIL, t, 0, S2 + XF, 1.0, 1.10, 0.45, 0.2)
    im = img.convert('RGBA'); glows(im, t, DIYAS_TIL, z, x0, y0, 55); embers(im, t, 0.8); topshade(im)
    a = ease_out(prog(t, 0.6, 1.2)); b = ease_out(prog(t, 1.4, 1.2))
    gtext(im, W / 2, 60 + (1 - a) * 20, 'Happy', SCRIPT(100), GOLD, a)
    gtext(im, W / 2, 140 + (1 - b) * 20, 'Bhai Dooj', SCRIPT(160), GOLD, b)
    return im

def scene2(t):
    img, z, x0, y0 = push(THA, t, S2 - XF, S3 - S2 + 2 * XF, 1.12, 1.0, 0.4, 0.4)
    im = img.convert('RGBA'); glows(im, t, DIYAS_THA, z, x0, y0, 120); embers(im, t, 0.6); topshade(im, 170, 560)
    a = ease_out(prog(t, S2 + 0.5, 1.2)); b = ease_out(prog(t, S2 + 1.3, 1.2))
    gtext(im, W / 2, 150 + (1 - a) * 20, 'A tilak of love,', CIN(56), CREAM, a)
    gtext(im, W / 2, 230 + (1 - b) * 20, 'a lifetime of protection.', CIN(56), CREAM, b)
    return im

def scene3(t):
    bg = THA.filter(ImageFilter.GaussianBlur(26)); bg = ImageEnhance.Brightness(bg).enhance(0.38).convert('RGBA')
    embers(bg, t, 0.7); d = ImageDraw.Draw(bg)
    a = ease_out(prog(t, S3 + 0.2, 0.8))
    lg = LOGO.resize((170, 170)); lg.putalpha(lg.getchannel('A').point(lambda v: int(v * a))); bg.alpha_composite(lg, (W // 2 - 85, 620))
    gtext(bg, W / 2, 830, 'Happy Bhai Dooj', SCRIPT(120), GOLD, a)
    b = ease_out(prog(t, S3 + 0.6, 0.8))
    gtext(bg, W / 2, 1010, 'RUYAN CORPORATE SERVICES', CIN(46, 700), CREAM, b, glow=False)
    gtext(bg, W / 2, 1090, 'Pune · Mumbai · Chhatrapati Sambhajinagar · Dhule', MB(32), (235, 215, 190), b, glow=False)
    gtext(bg, W / 2, 1150, '7020570215  ·  www.ruyangroup.org', MB(34), GOLD, b, glow=False)
    return bg

def frame(t):
    if t < S2 - XF: im = scene1(t)
    elif t < S2: im = Image.blend(scene1(t), scene2(t), ease_out((t - (S2 - XF)) / XF))
    elif t < S3 - XF: im = scene2(t)
    elif t < S3: im = Image.blend(scene2(t), scene3(t), ease_out((t - (S3 - XF)) / XF))
    else: im = scene3(t)
    if t < 0.5: im = Image.blend(Image.new('RGBA', (W, H), (0, 0, 0, 255)), im, t / 0.5)
    return im.convert('RGB')

if __name__ == '__main__':
    if len(sys.argv) > 2:
        ts = [0.3, 3.0, 5.9, 8.5, 11.5, 13.8]
        sh = Image.new('RGB', (216 * 6, 384), 'white')
        for i, x in enumerate(ts): sh.paste(frame(x).resize((216, 384)), (i * 216, 0))
        sh.save(sys.argv[2]); print('sheet')
    else:
        render(OUT, '/home/claude/series/gift/silent.wav', TOTAL, frame); print('done', OUT)
