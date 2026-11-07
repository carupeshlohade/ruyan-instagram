"""Trader reel (7 Nov, user: "highly relatable, share market graphs"). Text-led, soft piano bed, no SFX.
Case: ITAT Cuttack, Ratan Kumar Kejriwal, AY 2013-14 (Taxscan 06.11.2026; ET: Rs 21.6 lakh speculative loss, notice for no tax audit).
usage: reel_trader.py out.mp4 [sheet.jpg]"""
import sys, math, random
sys.path.insert(0, '/home/claude/series')
from engine import *
from PIL import ImageFont
OUT = sys.argv[1]
fX = lambda s: font('Mukta-ExtraBold.ttf', s)
fB = lambda s: font('Mukta-Bold.ttf', s)
fM = lambda s: font('SpaceMono-Bold.ttf', s)
BG, PANEL, GRID, RED, GRN, INK, MUT, GOLD = (12, 16, 24), (22, 28, 40), (36, 44, 60), (240, 72, 72), (46, 204, 130), (240, 242, 248), (140, 150, 170), (255, 196, 90)
EMO = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', 109)
def emoji(ch, size):
    im = Image.new('RGBA', (150, 150), (0, 0, 0, 0)); ImageDraw.Draw(im).text((10, 10), ch, font=EMO, embedded_color=True)
    return im.crop(im.getbbox()).resize((size, size), Image.LANCZOS)
LOGO = logo_badge(84)
S = [0, 5.2, 9.6, 13.2, 18.0, 22.4]; TOTAL = 27.0
# candles: drifting down with noise
rng = random.Random(11); C = []; p = 100.0
for i in range(46):
    o = p; p = p + rng.uniform(-3.2, 1.6) - (1.2 if i > 18 else 0.2); c = p
    hi = max(o, c) + rng.uniform(0.3, 1.8); lo = min(o, c) - rng.uniform(0.3, 1.8); C.append((o, hi, lo, c))
LO = min(x[2] for x in C); HI = max(x[1] for x in C)

def chart(im, t, x0, y0, w, h, n_show):
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((x0, y0, x0 + w, y0 + h), 28, fill=PANEL)
    for k in range(1, 5): d.line((x0 + 20, y0 + k * h / 5, x0 + w - 20, y0 + k * h / 5), fill=GRID, width=2)
    cw = (w - 60) / len(C)
    Y = lambda v: y0 + 30 + (HI - v) / (HI - LO) * (h - 60)
    for i in range(int(n_show)):
        o, hi, lo, c = C[i]; x = x0 + 30 + i * cw + cw / 2; col = GRN if c >= o else RED
        d.line((x, Y(hi), x, Y(lo)), fill=col, width=3)
        d.rectangle((x - cw * 0.32, min(Y(o), Y(c)), x + cw * 0.32, max(Y(o), Y(c)) + 2), fill=col)
    return d

def frame(t):
    im = Image.new('RGBA', (W, H), BG + (255,)); d = ImageDraw.Draw(im)
    k = scene_at(t, S)
    if k <= 1:
        # trading app
        d.text((70, 150), 'NIFTY  ·  INTRADAY  ·  F&O', font=fM(34), fill=MUT)
        n = min(len(C), 4 + (t / 4.6) * len(C)); chart(im, t, 50, 260, W - 100, 720, n); d = ImageDraw.Draw(im)
        q = ease_out(prog(t, 0.3, 4.3)); v = int(2160000 * q)
        d.text((70, 1020), 'Total P&L', font=fB(40), fill=MUT)
        d.text((70, 1070), f'-₹{inr(v)}', font=fM(110), fill=RED)
        a = ease_out(prog(t, 0.6, 0.6))
        if a: text_c(d, 1330 + (1 - a) * 30, 'Lost ₹21.6 lakh', fX(104), INK); text_c(d, 1450 + (1 - a) * 30, 'in the share market.', fX(80), INK)
        if k == 1:
            b = ease_out(prog(t, S[1], 0.5)); y = int(1960 - b * 1180)
            sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((0, 0, W, H), fill=(0, 0, 0, int(150 * b))); im.alpha_composite(sh); d = ImageDraw.Draw(im)
            d.rounded_rectangle((60, y, W - 60, y + 560), 36, fill=(250, 248, 242))
            d.rounded_rectangle((100, y + 40, 190, y + 130), 20, fill=(30, 70, 140)); d.text((116, y + 56), 'IT', font=fX(48), fill='white')
            d.text((220, y + 44), 'INCOME TAX DEPARTMENT', font=fB(34), fill=(90, 90, 100)); d.text((220, y + 88), 'Notice', font=fB(32), fill=(140, 140, 150))
            d.text((100, y + 180), 'Why were your accounts', font=fX(62), fill=(20, 20, 28)); d.text((100, y + 255), 'not audited?', font=fX(62), fill=(20, 20, 28))
            d.rounded_rectangle((100, y + 370, 650, y + 440), 35, fill=(255, 225, 220)); d.text((128, y + 378), 'Penalty: Section 271B', font=fB(40), fill=(190, 40, 40))
            tw = d.textlength('Then came this.', font=fX(76)); d.rounded_rectangle(((W - tw) / 2 - 40, y - 140, (W + tw) / 2 + 40, y - 30), 55, fill=BG); text_c(d, y - 130, 'Then came this.', fX(76), GOLD)
    elif k == 2:
        a = ease_out(prog(t, S[2], 0.5))
        im.alpha_composite(emoji('🤯', 200), (W // 2 - 100, 560))
        d = ImageDraw.Draw(im)
        text_c(d, 840 + (1 - a) * 30, 'He made a LOSS.', fX(104), INK)
        b = ease_out(prog(t, S[2] + 1.0, 0.5))
        if b: text_c(d, 990 + (1 - b) * 30, 'And still got a', fX(84), MUT); text_c(d, 1095 + (1 - b) * 30, 'penalty notice?', fX(100), RED)
    elif k == 3:
        a = ease_out(prog(t, S[3], 0.5))
        d.rounded_rectangle((70, 520, W - 70, 1250), 40, fill=PANEL)
        im.alpha_composite(emoji('⚖️', 130), (W // 2 - 65, 570)); d = ImageDraw.Draw(im)
        text_c(d, 730, 'ITAT Cuttack', fB(54), MUT)
        text_c(d, 810, 'Penalty deleted.', fX(110), GRN)
        b = ease_out(prog(t, S[3] + 1.2, 0.5))
        if b:
            text_c(d, 980, "The department's own record", fB(48), INK); text_c(d, 1045, 'said he ran no business.', fB(48), INK)
        text_c(d, 1170, 'AY 2013-14  ·  reported 6 Nov 2026', fB(32), MUT)
    elif k == 4:
        rows = [('Intraday', 'taxed one way'), ('F&O', 'taxed another'), ('Delivery', 'taxed a third way')]
        for i, (a_, b_) in enumerate(rows):
            q = ease_out(prog(t, S[4] + i * 0.55, 0.45))
            if q:
                y = 420 + i * 200; x = 70 - (1 - q) * 120
                d.rounded_rectangle((x, y, x + W - 140, y + 160), 30, fill=PANEL)
                d.text((x + 40, y + 36), a_, font=fX(66), fill=GOLD); d.text((x + 420, y + 54), b_, font=fB(46), fill=INK)
        b = ease_out(prog(t, S[4] + 2.0, 0.5))
        if b:
            text_c(d, 1100, 'And the audit rule depends', fB(54), INK); text_c(d, 1170, 'on which one you do.', fB(54), INK)
            text_c(d, 1310, 'Most traders file it wrong.', fX(78), RED)
    else:
        text_c(d, 600, 'Trading this year?', fX(88), INK)
        c = back_out(prog(t, S[5] + 0.3, 0.5))
        if c > 0:
            bw = int(800 * min(c, 1.05)); bh = int(160 * min(c, 1.05)); x0 = (W - bw) // 2
            d.rounded_rectangle((x0, 780, x0 + bw, 780 + bh), bh // 2, fill=GOLD)
            if c > 0.6: text_c(d, 806, 'Comment TRADE', fX(88), (20, 20, 30))
        e = ease_out(prog(t, S[5] + 1.2, 0.6))
        if e:
            text_c(d, 1010, "We'll check before the notice does.", fB(50), INK)
            text_c(d, 1150, 'Call 7020570215', fX(70), GOLD)
            text_c(d, 1290, '@ruyan_corporate_services', fB(44), MUT); text_c(d, 1360, 'www.ruyangroup.org', fB(44), INK)
    im.alpha_composite(LOGO, (W - 130, 50))
    return im.convert('RGB')

if __name__ == '__main__':
    if len(sys.argv) > 2:
        ts = [3.5, 7.5, 11.5, 16.5, 21.5, 25.5]
        sh = Image.new('RGB', (216 * 6, 384), 'white')
        for i, x in enumerate(ts): sh.paste(frame(x).resize((216, 384)), (i * 216, 0))
        sh.save(sys.argv[2]); print('sheet')
    else:
        render(OUT, '/home/claude/series/trade/bed.wav', TOTAL, frame); print('done', OUT)
