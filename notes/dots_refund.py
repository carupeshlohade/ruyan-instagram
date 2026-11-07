"""'Hold the dots & slide' carousel (7 Nov, user picked case 2). One dotted trail runs through all slides; each slide lights the next dot.
Case: Mohan Clothing Co. Pvt. Ltd. v. DCIT, Delhi HC, WP(C) 16193/2024, 28.10.2026 (LiveLawBiz 28.10.2026)."""
import os
from PIL import Image, ImageDraw, ImageFont
W, H, N = 1080, 1350, 6
FD = '/home/claude/fonts/'
MX = lambda s: ImageFont.truetype(FD + 'Mukta-ExtraBold.ttf', s)
MB = lambda s: ImageFont.truetype(FD + 'Mukta-Bold.ttf', s)
BG, INK, MUT, ACC, GRN, DIM = (255, 248, 226), (28, 36, 72), (110, 112, 140), (236, 94, 70), (34, 140, 92), (214, 206, 186)
pano = Image.new('RGB', (W * N, H), BG); d = ImageDraw.Draw(pano)
YD = 1010
for x in range(40, W * N - 40, 26): d.ellipse((x - 5, YD - 5, x + 5, YD + 5), fill=DIM)
DOTS = [(1.5, '1'), (2.5, '2'), (3.5, '3'), (4.5, '4')]
def wrap(t, f, w):
    out, cur = [], ''
    for wd in t.split():
        s = (cur + ' ' + wd).strip()
        if d.textlength(s, font=f) <= w: cur = s
        else: out.append(cur); cur = wd
    return out + [cur]
def blk(i, y, lines, f, c, lh=1.14):
    for ln in lines:
        for l2 in wrap(ln, f, W - 150): d.text((i * W + 75, y), l2, font=f, fill=c); y += int(f.size * lh)
    return y
def top(i, t):
    d.text((i * W + 75, 80), t, font=MB(30), fill=ACC); d.text((i * W + W - 150, 80), f'{i + 1}/{N}', font=MB(30), fill=MUT)
for k, (fx, lab) in enumerate(DOTS):
    x = int(fx * W); d.ellipse((x - 46, YD - 46, x + 46, YD + 46), fill=INK); tw = d.textlength(lab, font=MX(52)); d.text((x - tw / 2, YD - 38), lab, font=MX(52), fill=BG)
    hx = x + 80; d.text((hx, YD - 20), 'hold', font=MB(30), fill=MUT)
# 1 cover
top(0, 'REAL CASE  ·  INCOME TAX REFUND')
blk(0, 170, ['Your refund', 'was due.'], MX(104), INK, 1.02)
blk(0, 420, ['Then it vanished.'], MX(104), ACC)
blk(0, 600, ['Follow the dots to see where it went.'], MB(44), MUT)
d.text((75, 1100), 'Hold the dots & slide  >>', font=MB(44), fill=INK)
# 2
top(1, 'DOT 1  ·  THE DEMAND')
blk(1, 170, ['About ₹7.54 crore'], MX(96), INK)
blk(1, 320, ['Tax demand for AY 2020-21.', 'The company disagreed and filed an appeal in October 2022.'], MB(44), MUT, 1.3)
# 3
top(2, 'DOT 2  ·  THE REFUND')
blk(2, 170, ['₹6.20 crore refund'], MX(96), INK)
blk(2, 320, ['Due for AY 2022-23. It never reached the bank.', 'The department adjusted it against the demand still under appeal.'], MB(44), MUT, 1.3)
# 4
top(3, 'DOT 3  ·  MORE RECOVERY')
blk(3, 170, ['₹1,93,15,522 more'], MX(96), ACC)
blk(3, 320, ['Recovered in February 2025, while the stay application was still pending.'], MB(44), MUT, 1.3)
# 5
top(4, 'DOT 4  ·  THE HIGH COURT')
blk(4, 170, ['Delhi High Court:'], MX(70), INK)
blk(4, 260, ['Return ₹1,93,15,522', 'with interest.'], MX(80), GRN, 1.05)
blk(4, 470, ['But the ₹6.20 crore? Not returned. No stay had been asked for back then.'], MB(44), ACC, 1.3)
d.text((4 * W + 75, 1110), 'WP(C) 16193/2024  ·  28 Oct 2026', font=MB(30), fill=MUT)
# 6 hint + CTA
top(5, 'BEFORE IT HAPPENS TO YOU')
blk(5, 170, ['One application,', 'filed on time,', 'decided whose', 'money it was.'], MX(84), INK, 1.04)
blk(5, 560, ['Most people file the appeal and forget it.'], MB(44), ACC)
bw = 640; x0 = 5 * W + (W - bw) // 2
d.rounded_rectangle((x0, 1120, x0 + bw, 1220), 50, fill=INK)
t = 'Comment REFUND'; f = MX(56); d.text((5 * W + (W - d.textlength(t, font=f)) / 2, 1132), t, font=f, fill=BG)
f = MB(30); t = "Refund stuck or adjusted? Call 7020570215"; d.text((5 * W + (W - d.textlength(t, font=f)) / 2, 1236), t, font=f, fill=MUT)
logo = Image.open('/home/claude/ruyan_automation/logo.png').convert('RGBA').resize((56, 56)); logo.putalpha(logo.getchannel('A').point(lambda a: int(a * 0.5)))
pano = pano.convert('RGBA'); d = ImageDraw.Draw(pano)
for i in range(N):
    pano.alpha_composite(logo, (i * W + W - 116, H - 82)); d = ImageDraw.Draw(pano)
    d.text((i * W + 75, H - 58), '@ruyan_corporate_services' if i not in (0, 4) else 'Source: Mohan Clothing Co. v. DCIT, Delhi HC', font=MB(24), fill=MUT)
out = '/home/claude/ruyan_automation/batch2/media17'; os.makedirs(out, exist_ok=True)
for i in range(N): pano.crop((i * W, 0, (i + 1) * W, H)).convert('RGB').save(f'{out}/case-refund-{i + 1}.jpg', quality=92)
pv = Image.new('RGB', (N * 220 + 70, 295), (40, 40, 40))
for i in range(N): pv.paste(pano.crop((i * W, 0, (i + 1) * W, H)).convert('RGB').resize((216, 270)), (10 + i * 226, 12))
pv.save(f'{out}/preview.jpg'); print('ok')
