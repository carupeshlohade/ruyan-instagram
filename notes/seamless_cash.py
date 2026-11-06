"""'Traveling icon' seamless carousel (trend ref: yoursocialteam DepPeSVHZ7g, 4 Nov). One 5-slide panorama, a dashed path runs across
all slides and a cash bundle travels along it. Case: Vinod Kumar Gupta v. ITO, ITAT Allahabad, ITA 79/ALLD/2025, AY 2017-18, 15.10.2026."""
import math, os
from PIL import Image, ImageDraw, ImageFont
W, H, N = 1080, 1350, 5
FD = '/home/claude/fonts/'
F = lambda n, s: ImageFont.truetype(FD + n, s)
HX, HB, HR = (lambda s: F('Mukta-ExtraBold.ttf', s)), (lambda s: F('Mukta-Bold.ttf', s)), (lambda s: F('Mukta-Regular.ttf', s) if os.path.exists(FD + 'Mukta-Regular.ttf') else F('Mukta-Bold.ttf', s))
EMO = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', 109)
def emoji(ch, size):
    im = Image.new('RGBA', (150, 150), (0, 0, 0, 0)); ImageDraw.Draw(im).text((10, 10), ch, font=EMO, embedded_color=True)
    return im.crop(im.getbbox()).resize((size, size), Image.LANCZOS)
BG, INK, MUT, ACC, RED, GRN, LINE = (250, 238, 222), (52, 36, 30), (128, 104, 92), (214, 120, 60), (196, 64, 52), (52, 140, 92), (226, 170, 120)
pano = Image.new('RGBA', (W * N, H), BG + (255,)); d = ImageDraw.Draw(pano)
for i in range(N):  # soft alternating tint per slide so the swipe reads, path stays continuous
    if i % 2: d.rectangle((i * W, 0, (i + 1) * W, H), fill=(247, 232, 214, 255))
# continuous wavy path across all slides
pts = [(x, 860 + 150 * math.sin(x / 760)) for x in range(-20, W * N + 20, 6)]
for k in range(0, len(pts) - 1, 2):
    d.line((pts[k], pts[k + 1]), fill=LINE, width=14)
def y_at(x): return 860 + 150 * math.sin(x / 760)
STOPS = [(0.70, '💵'), (1.55, '🏦'), (2.55, '📩'), (3.55, '⚖️'), (4.50, '✅')]
for fx, ch in STOPS:
    x = int(fx * W); y = int(y_at(x)); r = 92
    d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 250, 244, 255), outline=ACC, width=8)
    e = emoji(ch, 112); pano.alpha_composite(e, (x - 56, y - 56)); d = ImageDraw.Draw(pano)
def wrap(txt, f, w):
    out, cur = [], ''
    for wd in txt.split():
        t = (cur + ' ' + wd).strip()
        if d.textlength(t, font=f) <= w: cur = t
        else: out.append(cur); cur = wd
    return out + [cur]
def block(i, y, lines, f, col, lh=1.2, x=80, w=W - 160):
    for ln in lines:
        for l2 in wrap(ln, f, w): d.text((i * W + x, y), l2, font=f, fill=col); y += int(f.size * lh)
    return y
def tag(i, txt):
    f = HB(30); tw = d.textlength(txt, font=f)
    d.rounded_rectangle((i * W + 80, 90, i * W + 80 + tw + 44, 146), 28, fill=INK); d.text((i * W + 102, 95), txt, font=f, fill=BG)
    d.text((i * W + W - 150, 100), f'{i + 1}/{N}', font=HB(32), fill=MUT)
# 1 cover
tag(0, 'REAL CASE  ·  INCOME TAX')
block(0, 200, ['Deposited your', 'own shop cash.'], HX(96), INK, 1.08)
block(0, 430, ['Got taxed for it.'], HX(96), RED, 1.08)
d.text((80, 1150), 'Follow the cash. Swipe >>', font=HB(46), fill=ACC)
# 2
tag(1, 'WHAT HAPPENED')
block(1, 200, ['₹2,49,998'], HX(120), INK)
block(1, 360, ['cash deposited in the bank.', 'Every rupee from his own sales.'], HB(48), MUT, 1.3)
block(1, 1080, ['Recorded in the books. Shown in VAT returns.'], HB(40), INK, 1.3)
# 3
tag(2, 'THE TAX OFFICER')
block(2, 200, ['"More than your', 'average daily turnover.', 'Unexplained!"'], HX(74), RED, 1.12)
block(2, 1080, ['Added to income under Section 69A, as unexplained money.'], HB(40), INK, 1.3)
# 4
tag(3, 'THE TRIBUNAL')
block(3, 200, ['Addition', 'deleted.'], HX(110), GRN, 1.05)
block(3, 460, ['Based on guesswork, not evidence.', 'The sales were already in his books.'], HB(44), MUT, 1.3)
block(3, 1080, ['ITAT Allahabad · AY 2017-18 · 15 Oct 2026'], HB(36), INK)
# 5 hint + CTA
tag(4, 'BEFORE IT HAPPENS TO YOU')
block(4, 200, ['Every cash business', 'needs one set of papers.'], HX(70), INK, 1.12)
block(4, 380, ['Most keep only half of it.'], HX(70), RED, 1.12)
bw = 620; x0 = 4 * W + (W - bw) // 2
d.rounded_rectangle((x0, 1060, x0 + bw, 1170), 55, fill=INK)
f = HX(64); t = 'Comment CASH'; tw = d.textlength(t, font=f); d.text((4 * W + (W - tw) / 2, 1072), t, font=f, fill=BG)
f = HB(32); t = "We'll tell you what to keep. Call 7020570215"; tw = d.textlength(t, font=f); d.text((4 * W + (W - tw) / 2, 1190), t, font=f, fill=MUT)
logo = Image.open('/home/claude/ruyan_automation/logo.png').convert('RGBA').resize((70, 70)); logo.putalpha(logo.getchannel('A').point(lambda a: int(a * 0.5)))
for i in range(N):
    pano.alpha_composite(logo, (i * W + W - 110, H - 110))
    d.text((i * W + 80, H - 90), '@ruyan_corporate_services', font=HB(28), fill=MUT)
out = '/home/claude/ruyan_automation/batch2/media12'; os.makedirs(out, exist_ok=True)
for i in range(N): pano.crop((i * W, 0, (i + 1) * W, H)).convert('RGB').save(f'{out}/case-cash-{i + 1}.jpg', quality=92)
pano.convert('RGB').resize((W * N // 4, H // 4)).save(f'{out}/preview-case-cash.jpg'); print('ok')
