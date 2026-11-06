"""'Accountant on blast' reel (5 Nov, trend adapt). WhatsApp-style chat, soft piano (no SFX), whispered CTA.
usage: reel_blast.py out.mp4 [sheet.jpg]   (audio: piano_bed.py -> lock/blast_mix.wav)"""
import sys, os, math
sys.path.insert(0, '/home/claude/series')
from engine import *
from PIL import ImageFilter, ImageFont
OUT = sys.argv[1]
fX = lambda s: font('Mukta-ExtraBold.ttf', s)
fB = lambda s: font('Mukta-Bold.ttf', s)
CHAT_BG, HEAD, ME, THEM, INK, MUT, TICK = (236, 229, 221), (0, 128, 105), (217, 253, 211), (255, 255, 255), (17, 27, 33), (102, 119, 129), (83, 189, 235)
# (day, time, who, text)  who: me / acc / seen / sms
MSGS = [('MONDAY', '9:02 AM', 'me', 'GSTR-3B file ho gaya?'),
        (None, '9:41 AM', 'acc', 'Kal pakka sir 👍'),
        ('TUESDAY', '11:40 AM', 'me', 'Ho gaya?'),
        (None, '1:15 PM', 'acc', 'Portal slow hai sir'),
        ('WEDNESDAY', '6:15 PM', 'me', '??'),
        (None, '8:50 PM', 'acc', 'Bas data bhej do ek baar phirse'),
        ('THURSDAY', '10:05 PM', 'me', 'Bhai aaj last date hai'),
        (None, '10:05 PM', 'seen', ''),
        ('FRIDAY', '8:30 AM', 'sms', 'GST: Return not filed by due date. Late fee and interest applicable.')]
T0, DT = 1.0, 1.35
T_MSG = [T0 + i * DT for i in range(len(MSGS))]
T_CUT = T_MSG[-1] + 2.2
T_HINT = T_CUT + 3.0
T_CTA = T_HINT + 3.2
TOTAL = T_CTA + 5.6
LOGO = logo_badge(80)
EMO = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', 109)
def emoji(ch, size):
    im = Image.new('RGBA', (150, 150), (0, 0, 0, 0)); ImageDraw.Draw(im).text((10, 10), ch, font=EMO, embedded_color=True)
    return im.crop(im.getbbox()).resize((size, size), Image.LANCZOS)
THUMB = emoji('👍', 44)

def wrap(d, txt, f, w):
    out, cur = [], ''
    for wd in txt.split():
        t = (cur + ' ' + wd).strip()
        if d.textlength(t, font=f) <= w: cur = t
        else: out.append(cur); cur = wd
    return out + [cur]

def bubble(d, im, y, who, text, tm, q):
    f = fB(44); ft = fB(26)
    if who == 'seen':
        s = 'Seen ✓✓'; s = 'Seen  10:05 PM'
        tw = d.textlength(s, font=ft); d.text((W - 60 - tw, y), s, font=ft, fill=TICK); return y + 50
    if who == 'sms':
        x0, x1 = 60, W - 60
        lines = wrap(d, text, fB(40), x1 - x0 - 60); h = 90 + len(lines) * 52
        d.rounded_rectangle((x0, y, x1, y + h), 26, fill=(255, 240, 238), outline=(220, 70, 60), width=4)
        d.text((x0 + 30, y + 18), 'SMS · GST PORTAL', font=fB(28), fill=(200, 60, 50))
        yy = y + 60
        for ln in lines: d.text((x0 + 30, yy), ln, font=fB(40), fill=INK); yy += 52
        return y + h + 24
    txt = text.replace('👍', '').strip()
    lines = wrap(d, txt, f, 620); w = max(d.textlength(l, font=f) for l in lines) + (60 if '👍' in text else 0)
    w = max(w, 200) + 150; h = 30 + len(lines) * 56 + 30
    if who == 'me': x1 = W - 50; x0 = x1 - w; col = ME
    else: x0 = 50; x1 = x0 + w; col = THEM
    off = int((1 - q) * 30)
    d.rounded_rectangle((x0, y + off, x1, y + h + off), 24, fill=col)
    yy = y + 22 + off
    for ln in lines: d.text((x0 + 26, yy), ln, font=f, fill=INK); yy += 56
    if '👍' in text: im.alpha_composite(THUMB, (int(x0 + 26 + d.textlength(lines[-1], font=f) + 10), y + 26 + off))
    st = tm + ('  ✓✓' if who == 'me' else ''); st = tm
    tw = d.textlength(st, font=ft); d.text((x1 - 20 - tw, y + h - 34 + off), st, font=ft, fill=MUT)
    if who == 'me':
        tx = x1 - 20 - tw - 46; d.line((tx, y + h - 20 + off, tx + 8, y + h - 12 + off, tx + 22, y + h - 28 + off), fill=TICK, width=3)
        d.line((tx + 12, y + h - 12 + off, tx + 26, y + h - 28 + off), fill=TICK, width=3)
    return y + h + 20

def chat(t):
    im = Image.new('RGBA', (W, H), CHAT_BG + (255,)); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W, 200), fill=HEAD)
    d.ellipse((50, 70, 150, 170), fill=(200, 210, 215)); text_c  # avatar
    d.text((175, 72), 'Accountant', font=fX(54), fill='white')
    typing = any(T_MSG[i] - 0.8 < t < T_MSG[i] for i, m in enumerate(MSGS) if m[2] == 'acc')
    d.text((175, 136), 'typing…' if typing else 'online', font=fB(32), fill=(220, 245, 238))
    shown = [i for i in range(len(MSGS)) if t >= T_MSG[i]]
    # layout from top, then scroll so the newest stays in view
    items = []
    for i in shown:
        day, tm, who, txt = MSGS[i]
        items.append((i, day, tm, who, txt))
    ys, y = [], 240
    tmp = Image.new('RGBA', (W, 6000), (0, 0, 0, 0)); td = ImageDraw.Draw(tmp)
    for i, day, tm, who, txt in items:
        if day:
            f = fB(30); tw = td.textlength(day, font=f)
            td.rounded_rectangle(((W - tw) / 2 - 24, y, (W + tw) / 2 + 24, y + 52), 14, fill=(225, 243, 251)); td.text(((W - tw) / 2, y + 6), day, font=f, fill=MUT); y += 76
        q = ease_out(prog(t, T_MSG[i], 0.3))
        y = bubble(td, tmp, y, who, txt, tm, q)
    scroll = max(0, y - (H - 200) + 80)
    im.alpha_composite(tmp.crop((0, scroll, W, scroll + H - 200)), (0, 200))
    d = ImageDraw.Draw(im); d.rectangle((0, 0, W, 200), fill=HEAD)
    d.ellipse((50, 70, 150, 170), fill=(200, 210, 215)); d.text((175, 72), 'Accountant', font=fX(54), fill='white')
    d.text((175, 136), 'typing…' if typing else 'online', font=fB(32), fill=(220, 245, 238))
    return im

def frame(t):
    if t < T_CUT:
        im = chat(t)
    else:
        im = Image.new('RGBA', (W, H), (16, 18, 26, 255)); d = ImageDraw.Draw(im)
        if t < T_CTA:
            a = ease_out(prog(t, T_CUT, 0.3))
            text_c(d, 660, 'Paying someone', fX(96), (255, 255, 255))
            text_c(d, 780, 'to make YOU', fX(96), (255, 255, 255))
            text_c(d, 900, 'chase THEM?', fX(110), (255, 196, 90))
            b = ease_out(prog(t, T_HINT, 0.5))
            if b > 0:
                text_c(d, 1130 + (1 - b) * 20, "There's a way your phone stays quiet,", fB(48), (220, 222, 235))
                text_c(d, 1200 + (1 - b) * 20, 'and the work still gets done.', fB(48), (220, 222, 235))
        else:
            text_c(d, 640, 'Psst…', fB(64), (170, 175, 195))
            c = back_out(prog(t, T_CTA, 0.5))
            if c > 0:
                bw = int(780 * min(c, 1.05)); bh = int(150 * min(c, 1.05)); x0 = (W - bw) // 2
                d.rounded_rectangle((x0, 760, x0 + bw, 760 + bh), bh // 2, fill=(255, 196, 90))
                if c > 0.6: text_c(d, 786, 'Call 7020570215', fX(80), (20, 20, 30))
            e = ease_out(prog(t, T_CTA + 1.2, 0.6))
            if e > 0:
                text_c(d, 1000, 'Stop chasing. Hire us.', fB(58), (230, 230, 240))
                text_c(d, 1260, '@ruyan_corporate_services', fB(44), (255, 196, 90))
                text_c(d, 1330, 'www.ruyangroup.org', fB(48), (255, 255, 255))
    im = im.convert('RGBA'); im.alpha_composite(LOGO, (W - 120, 230 if t < T_CUT else 40))
    return im.convert('RGB')

if __name__ == '__main__':
    if len(sys.argv) > 2:
        ts = [T_MSG[2] + 0.5, T_MSG[7] + 0.5, T_MSG[8] + 1, T_HINT + 1.5, T_CTA + 3]
        sh = Image.new('RGB', (216 * 5, 384), 'white')
        for i, x in enumerate(ts): sh.paste(frame(x).resize((216, 384)), (i * 216, 0))
        sh.save(sys.argv[2]); print('sheet', TOTAL)
    else:
        render(OUT, '/home/claude/series/lock/blast_mix.wav', TOTAL, frame); print('done', OUT, round(TOTAL, 2))
