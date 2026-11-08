"""Diwali gift 'Bill X-ray' reel (7 Nov, user: "Nice idea. Make it and post it"). Text-led, soft piano (music.py siemens), no SFX.
Law: s.17(5)(h) CGST Act (ITC blocked on gifts); TDS on business benefits > Rs 20,000/yr (s.194R, carried into IT Act 2025);
employer gifts to employees up to Rs 50,000/yr not a supply (CBIC clarification 2017)."""
import sys, math, random
sys.path.insert(0, '/home/claude/series')
from engine import *
from PIL import ImageFont, ImageFilter
OUT = sys.argv[1]
fX = lambda s: font('Mukta-ExtraBold.ttf', s)
fB = lambda s: font('Mukta-Bold.ttf', s)
fM = lambda s: font('SpaceMono-Regular.ttf', s)
fMB = lambda s: font('SpaceMono-Bold.ttf', s)
BG, GOLD, CREAM, INK, MUT, RED, SCAN = (16, 28, 64), (246, 196, 92), (255, 248, 236), (40, 30, 30), (130, 110, 104), (214, 48, 48), (80, 255, 200)
EMO = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', 109)
def emoji(ch, size):
    im = Image.new('RGBA', (150, 150), (0, 0, 0, 0)); ImageDraw.Draw(im).text((10, 10), ch, font=EMO, embedded_color=True)
    return im.crop(im.getbbox()).resize((size, size), Image.LANCZOS)
LOGO = logo_badge(84)
GIFT, DIYA = emoji('🎁', 300), emoji('🪔', 90)
S = [0, 3.75, 11.35, 15.95, 22.3, 28.9]; TOTAL = 36.4; T_INTRO = 5.75
rng = random.Random(4); SPARK = [(rng.randint(0, W), rng.randint(0, H), rng.random() * 6) for _ in range(70)]
# bill canvas
BW, BH = 900, 820
bill = Image.new('RGBA', (BW, BH), CREAM + (255,)); b = ImageDraw.Draw(bill)
for k in range(0, BW, 30): b.polygon([(k, BH - 1), (k + 15, BH - 18), (k + 30, BH - 1)], fill=BG + (255,))
def ct(dr, y, t, f, c, w=BW):
    dr.text(((w - dr.textlength(t, font=f)) / 2, y), t, font=f, fill=c)
ct(b, 40, 'SHUBH DRY FRUITS & GIFTS', fMB(40), INK); ct(b, 96, 'TAX INVOICE  ·  06-11-2026', fM(28), MUT)
b.line((40, 150, BW - 40, 150), fill=(200, 190, 180), width=3)
ROWS = [('Dry fruit hampers x 40', '1,80,000.00'), ('  for dealers & clients', ''), ('Sweet boxes x 60', '36,000.00'), ('  for staff', ''),
        ('Taxable value', '2,16,000.00'), ('GST @ 5%', '10,800.00'), ('TOTAL', '2,26,800.00')]
ROWY = {}
y = 190
for a, v in ROWS:
    f = fMB(36) if a in ('TOTAL',) else fM(34)
    b.text((50, y), a, font=f, fill=INK if not a.startswith('  ') else MUT)
    if v: b.text((BW - 50 - b.textlength(v, font=f), y), v, font=f, fill=INK)
    ROWY[a.strip()] = y; y += 70 if not a.startswith('  ') else 80
    if a in ('  for staff',): b.line((40, y - 20, BW - 40, y - 20), fill=(200, 190, 180), width=3)
ct(b, BH - 100, 'Thank you! Happy Diwali', fMB(34), INK)
BX, BY = (W - BW) // 2, 470
TRAPS = [  # (bill row, scene start, title, line1, line2)
    ('GST @ 5%', S[2], 'TRAP 1', "This GST? You can't", 'claim it back.'),
    ('Dry fruit hampers x 40', S[3], 'TRAP 2', 'Gift to a dealer above', '₹20,000 a year? TDS angle.'),
    ('Sweet boxes x 60', S[4], 'TRAP 3', 'Staff gifts above ₹50,000', 'a year? Different tax story.')]

def sparkle(d, t):
    for x, y, ph in SPARK:
        a = (math.sin(t * 2.4 + ph) + 1) / 2; s = 2 + 4 * a
        d.line((x - s, y, x + s, y), fill=GOLD, width=2); d.line((x, y - s, x, y + s), fill=GOLD, width=2)

VIG = Image.new('L', (W, H), 0)
_vd = ImageDraw.Draw(VIG)
for i in range(60):
    a = int(110 * (i / 60) ** 0.6); _vd.rectangle((i * 9, i * 15, W - i * 9, H - i * 15), outline=110 - a, width=16)
VIG = VIG.filter(ImageFilter.GaussianBlur(60)); VIGL = Image.new('RGBA', (W, H), (2, 6, 20, 255)); VIGL.putalpha(VIG)

def cam(im, z, fy, ty=None):  # zoom z; point fy lands at ty (default: centre)
    if z <= 1.001 and ty is None: return im
    ty = H / 2 if ty is None else ty
    cw, ch = W / z, H / z; y0 = min(max(fy - ty / z, 0), H - ch); x0 = (W - cw) / 2
    return im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.LANCZOS)

def ease(a, b, q): return a + (b - a) * q
FOCUS = [None, None] + [BY + ROWY[r] + 30 for r, *_ in TRAPS]
Z = [1.0, 1.0, 1.12, 1.12, 1.12]

def bill_scene(t):
    k = scene_at(t, S)
    lay = Image.new('RGBA', (W, H), BG + (255,)); d = ImageDraw.Draw(lay); sparkle(d, t)
    lay.alpha_composite(bill, (BX, BY)); d = ImageDraw.Draw(lay)
    if k == 1:
        sy = BY + 160 + (BH - 250) * ease_out(min(1, (t - S[1]) / (S[2] - S[1] - 0.3)))
        glow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(glow).rectangle((BX - 20, sy - 16, BX + BW + 20, sy + 16), fill=SCAN + (150,))
        lay.alpha_composite(glow.filter(ImageFilter.GaussianBlur(12))); d = ImageDraw.Draw(lay); d.line((BX - 20, sy, BX + BW + 20, sy), fill=SCAN, width=4)
    for i, (row, t0, *_r) in enumerate(TRAPS):
        if t >= t0:
            ry = BY + ROWY[row] - 12; q = ease_out(prog(t, t0, 0.35))
            d.rounded_rectangle((BX + 30, ry, BX + BW - 30, ry + 62), 12, outline=RED, width=max(1, int(6 * q)))
    # camera: glide between focus rows
    if k >= 2:
        q = ease_out(prog(t, S[k], 0.9)); prevf = FOCUS[k - 1] if k > 2 else BY + BH / 2; prevz = Z[k - 1]
        if k == 2: z = ease(1.0, 1.06, q); ty = ease(BY, 440, q)
        else: z = 1.06; ty = 440
        z *= 1 + 0.004 * (t - S[2]); lay = cam(lay, z, BY, ty)
    else:
        lay = cam(lay, 1 + 0.012 * (t - S[1]), H / 2)
    lay.alpha_composite(VIGL); d = ImageDraw.Draw(lay)
    # fixed overlays: title + trap card
    band = Image.new('RGBA', (W, 420), (0, 0, 0, 0)); bd = ImageDraw.Draw(band)
    for yy in range(420): bd.line((0, yy, W, yy), fill=BG + (255 if yy < 340 else int(255 * (420 - yy) / 80),))
    lay.alpha_composite(band); d = ImageDraw.Draw(lay)
    text_c(d, 175, 'DIWALI GIFT BILL', fB(44), GOLD); text_c(d, 232, 'X-RAY', fX(104), CREAM)
    if k == 1 and t >= T_INTRO:
        pq = ease_out(prog(t, T_INTRO, 0.5)); py = int(1500 + (1 - pq) * 60)
        card = Image.new('RGBA', (W - 120, 270), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
        cd.rounded_rectangle((0, 0, W - 121, 269), 36, fill=GOLD + (255,))
        cd.text((44, 40), '3 tax traps are hiding', font=fX(62), fill=BG); cd.text((44, 128), 'in this one bill.', font=fX(62), fill=BG)
        card.putalpha(card.getchannel('A').point(lambda v: int(v * pq))); lay.alpha_composite(card, (60, py))
    if k >= 2:
        _, t0, ttl, l1, l2 = TRAPS[k - 2]; pq = ease_out(prog(t, t0 + 0.25, 0.5))
        py = int(1500 + (1 - pq) * 60)
        card = Image.new('RGBA', (W - 120, 270), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
        cd.rounded_rectangle((0, 0, W - 121, 269), 36, fill=(255, 255, 255, 255))
        cd.text((44, 26), ttl, font=fX(44), fill=RED); cd.text((44, 88), l1, font=fX(58), fill=INK); cd.text((44, 162), l2, font=fX(58), fill=INK)
        card.putalpha(card.getchannel('A').point(lambda v: int(v * pq)))
        lay.alpha_composite(card, (60, py))
    return lay

def raw(t):
    k = scene_at(t, S)
    if k == 0:
        im = Image.new('RGBA', (W, H), BG + (255,)); d = ImageDraw.Draw(im); sparkle(d, t)
        q = back_out(prog(t, 0.1, 0.7)); g = GIFT.resize((max(1, int(320 * q)),) * 2)
        im.alpha_composite(g, (W // 2 - g.width // 2, 980 - g.height // 2)); d = ImageDraw.Draw(im)
        a = ease_out(prog(t, 0.5, 0.6))
        if a: text_c(d, 560 + (1 - a) * 40, 'Bought Diwali gifts', fX(92), CREAM); text_c(d, 672 + (1 - a) * 40, 'for clients & staff?', fX(92), GOLD)
        c = ease_out(prog(t, 1.6, 0.6))
        if c: text_c(d, 1250 + (1 - c) * 30, 'Look at the bill again.', fB(58), CREAM)
        im = cam(im, 1 + 0.05 * t / S[1], H / 2); im.alpha_composite(VIGL); return im
    if k <= 4: return bill_scene(t)
    im = Image.new('RGBA', (W, H), BG + (255,)); d = ImageDraw.Draw(im); sparkle(d, t)
    a = ease_out(prog(t, S[5] + 0.2, 0.6)); text_c(d, 560 + (1 - a) * 40, 'One festival.', fX(100), CREAM)
    a = ease_out(prog(t, S[5] + 0.7, 0.6))
    if a: text_c(d, 690 + (1 - a) * 40, 'Three tax traps.', fX(110), GOLD)
    c = back_out(prog(t, S[5] + 2.8, 0.5))
    if c > 0:
        bw = int(820 * min(c, 1.05)); bh = int(160 * min(c, 1.05)); x0 = (W - bw) // 2
        d.rounded_rectangle((x0, 900, x0 + bw, 900 + bh), bh // 2, fill=GOLD)
        if c > 0.6: text_c(d, 926, 'Comment GIFT', fX(90), BG)
    e = ease_out(prog(t, S[5] + 3.6, 0.6))
    if e:
        text_c(d, 1110, 'before you book the next order.', fB(50), CREAM)
        text_c(d, 1240, 'Call 7020570215', fX(70), GOLD)
        text_c(d, 1370, '@ruyan_corporate_services', fB(44), CREAM); text_c(d, 1440, 'www.ruyangroup.org', fB(44), GOLD)
        for i in range(5): im.alpha_composite(DIYA, (W // 2 - 445 + i * 190, 1600))
    im = cam(im, 1.04 - 0.04 * ease_out(prog(t, S[5], 1.2)), H / 2); im.alpha_composite(VIGL); return im

XF = 0.45
def frame(t):
    im = raw(t)
    for b_ in (S[1], S[5]):  # cinematic dissolve with light bloom
        if b_ - XF < t < b_:
            q = (t - (b_ - XF)) / XF; nxt = raw(b_ + 0.001)
            im = Image.blend(im, nxt, ease_out(q))
            fl = Image.new('RGBA', (W, H), (255, 226, 160, int(90 * math.sin(math.pi * q)))); im.alpha_composite(fl)
    im.alpha_composite(LOGO, (W - 130, 50))
    return im.convert('RGB')

if __name__ == '__main__':
    if len(sys.argv) > 2:
        ts = [2.0, 8.0, 13.0, 18.0, 25.0, 34.0]
        sh = Image.new('RGB', (216 * 6, 384), 'white')
        for i, x in enumerate(ts): sh.paste(frame(x).resize((216, 384)), (i * 216, 0))
        sh.save(sys.argv[2]); print('sheet')
    else:
        render(OUT, '/home/claude/series/gift/mix.wav', TOTAL, frame); print('done', OUT)
