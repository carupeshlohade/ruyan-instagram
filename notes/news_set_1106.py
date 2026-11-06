"""News set from 6 Nov routine (user: cover all 5). Each in a new visual format.
 A delivery  - static 'food-app receipt' (Notf 09/2026-CT(Rate), 18% -> 5% on ECO delivery, w.e.f. 1.11.2026; CBIC: 'no new tax')
 B register  - 'follow the line' carousel, 5 slides (Circular 257/03/2026-GST, 26.10.2026)
 C notice    - static 'red-pen notice' (Circular 258/04/2026-GST, 26.10.2026)
 D cra4      - static 'desk calendar' (MCA General Circular 06/2026, CRA-4 FY 2025-26 without additional fee till 31.12.2026)"""
import os, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H = 1080, 1350
FD = '/home/claude/fonts/'
F = lambda n, s: ImageFont.truetype(FD + n, s)
MB, MX = (lambda s: F('Mukta-Bold.ttf', s)), (lambda s: F('Mukta-ExtraBold.ttf', s))
MONO, MONOB = (lambda s: F('SpaceMono-Regular.ttf', s)), (lambda s: F('SpaceMono-Bold.ttf', s))
KAL = lambda s: F('Kalam-Bold.ttf', s)
EMO = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', 109)
OUT = '/home/claude/ruyan_automation/batch2/media16'; os.makedirs(OUT, exist_ok=True)
LOGO = Image.open('/home/claude/ruyan_automation/logo.png').convert('RGBA')
def emoji(ch, size):
    im = Image.new('RGBA', (150, 150), (0, 0, 0, 0)); ImageDraw.Draw(im).text((10, 10), ch, font=EMO, embedded_color=True)
    return im.crop(im.getbbox()).resize((size, size), Image.LANCZOS)
def ctx(d, y, t, f, c, cx=W / 2):
    d.text((cx - d.textlength(t, font=f) / 2, y), t, font=f, fill=c)
def foot(im, src, col):
    d = ImageDraw.Draw(im)
    lg = LOGO.resize((56, 56)); lg.putalpha(lg.getchannel('A').point(lambda a: int(a * 0.5))); im.alpha_composite(lg, (W - 116, H - 82))
    d = ImageDraw.Draw(im); d.text((60, H - 58), src, font=MB(24), fill=col)
    t = '@ruyan_corporate_services'; d.text((W - 130 - d.textlength(t, font=MB(24)), H - 58), t, font=MB(24), fill=col)
def pill(d, x0, y, w, h, txt, f, bg, fg):
    d.rounded_rectangle((x0, y, x0 + w, y + h), h // 2, fill=bg); d.text((x0 + (w - d.textlength(txt, font=f)) / 2, y + (h - f.size * 1.25) / 2 + 2), txt, font=f, fill=fg)

# ---------------- A: receipt ----------------
def A():
    BG, INK, MUT, GRN, RED = (255, 236, 222), (34, 30, 28), (120, 104, 96), (24, 128, 80), (206, 58, 48)
    im = Image.new('RGBA', (W, H), BG + (255,)); d = ImageDraw.Draw(im)
    d.text((60, 60), 'Saw the viral post', font=MX(70), fill=INK)
    d.text((60, 140), 'about a "new GST on delivery"?', font=MX(56), fill=RED)
    # receipt
    rx, ry, rw, rh = 170, 260, 740, 720
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((rx + 12, ry + 18, rx + rw + 12, ry + rh + 18), fill=(120, 60, 30, 70))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16))); d = ImageDraw.Draw(im)
    d.rectangle((rx, ry, rx + rw, ry + rh), fill=(255, 255, 252))
    for k in range(0, rw, 40):  # zig-zag bottom
        d.polygon([(rx + k, ry + rh), (rx + k + 20, ry + rh + 20), (rx + k + 40, ry + rh)], fill=(255, 255, 252))
    y = ry + 36; ctx(d, y, 'ORDER SUMMARY', MONOB(38), INK, rx + rw / 2); y += 60
    d.line((rx + 40, y, rx + rw - 40, y), fill=(200, 200, 200), width=2); y += 26
    def row(a, b, f=MONO(32), c=INK):
        nonlocal y; d.text((rx + 50, y), a, font=f, fill=c); d.text((rx + rw - 50 - d.textlength(b, font=f), y), b, font=f, fill=c); y += 54
    row('Food items', 'Rs 640.00'); row('Delivery fee', 'Rs  40.00')
    yo = y; row('GST on delivery @18%', 'Rs   7.20', c=MUT)
    d.line((rx + 40, yo + 22, rx + rw - 40, yo + 22), fill=RED, width=5)
    row('GST on delivery @5%', 'Rs   2.00', MONOB(32), GRN)
    d.line((rx + 40, y, rx + rw - 40, y), fill=(200, 200, 200), width=2); y += 24
    d.text((rx + 50, y), 'Illustrative bill. Food GST not shown.', font=MONO(22), fill=MUT); y += 60
    st = Image.new('RGBA', (560, 190), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
    sd.rounded_rectangle((8, 8, 552, 182), 24, outline=GRN, width=10); ctx(sd, 22, 'NOT A NEW TAX', MX(64), GRN, 280); ctx(sd, 104, 'A CUT: 18% to 5%', MB(46), GRN, 280)
    st = st.rotate(-7, expand=True, resample=Image.BICUBIC); im.alpha_composite(st, (rx + 70, y - 10)); d = ImageDraw.Draw(im)
    y = 1050
    d.text((60, y), 'From 1 Nov, delivery through apps is taxed at 5%.', font=MB(36), fill=INK); y += 48
    d.text((60, y), 'Sell or deliver through one? Your invoice may change.', font=MB(36), fill=RED); y += 72
    pill(d, 60, y, 520, 92, 'Comment DELIVERY', MX(50), INK, BG)
    d.text((610, y + 6), 'Not sure how it hits you?', font=MB(30), fill=MUT); d.text((610, y + 44), 'Call 7020570215', font=MX(34), fill=INK)
    foot(im, 'Source: Notification 09/2026-CT (Rate); CBIC, Nov 2026', MUT)
    im.convert('RGB').save(f'{OUT}/news-delivery.jpg', quality=93)

# ---------------- B: follow the line carousel ----------------
def B():
    N = 5; BG, INK, MUT, LINE, ACC, RED = (232, 238, 250), (26, 34, 64), (96, 106, 140), (66, 96, 220), (255, 170, 60), (200, 56, 60)
    pano = Image.new('RGBA', (W * N, H), BG + (255,)); d = ImageDraw.Draw(pano)
    # one continuous line: enters each slide, makes a loop/turn, exits
    pts = []
    for x in range(-10, W * N + 10, 4):
        i = x // W; lx = x - i * W
        base = 1000 + 60 * math.sin(x / 300)
        pts.append((x, base))
    for k in range(len(pts) - 1): d.line((pts[k], pts[k + 1]), fill=LINE, width=12)
    stops = [(0.5, '📄'), (1.5, '🏠'), (2.5, '🙅'), (3.5, '⏱️'), (4.5, '✅')]
    for fx, ch in stops:
        x = int(fx * W); y = int(1000 + 60 * math.sin(x / 300))
        d.ellipse((x - 70, y - 70, x + 70, y + 70), fill=(255, 255, 255), outline=LINE, width=10)
        pano.alpha_composite(emoji(ch, 80), (x - 40, y - 40)); d = ImageDraw.Draw(pano)
    def wrap(t, f, w):
        out, cur = [], ''
        for wd in t.split():
            s = (cur + ' ' + wd).strip()
            if d.textlength(s, font=f) <= w: cur = s
            else: out.append(cur); cur = wd
        return out + [cur]
    def blk(i, y, lines, f, c, lh=1.15):
        for ln in lines:
            for l2 in wrap(ln, f, W - 140): d.text((i * W + 70, y), l2, font=f, fill=c); y += int(f.size * lh)
        return y
    def tag(i, t):
        f = MB(28); tw = d.textlength(t, font=f); d.rounded_rectangle((i * W + 70, 80, i * W + 70 + tw + 40, 130), 25, fill=INK); d.text((i * W + 90, 84), t, font=f, fill=BG)
        d.text((i * W + W - 140, 88), f'{i + 1}/{N}', font=MB(30), fill=MUT)
    tag(0, 'GST REGISTRATION · NEW RULES')
    blk(0, 180, ['Applied for GST.', 'Officer wants', 'one more document.'], MX(88), INK, 1.05)
    blk(0, 520, ['Again. And again.'], MX(64), RED)
    blk(0, 640, ['CBIC has now drawn the line. Follow it.'], MB(42), MUT)
    tag(1, 'STEP 1 · ONE LIST')
    blk(1, 180, ['One fixed list', 'of documents.'], MX(84), INK, 1.05)
    blk(1, 420, ['Owned, rented, family-owned or co-working: each premises type now has its own set list.', 'Nothing outside it.'], MB(40), MUT, 1.3)
    tag(2, 'STEP 2 · WHAT THEY CANNOT ASK')
    blk(2, 180, ['Not allowed', 'any more:'], MX(84), INK, 1.05)
    y = 420
    for t in ['Udyam / MSME certificate', 'Your home address in another city', '"Is this electricity connection commercial?"', '"Residential place cannot be a business"']:
        d.text((2 * W + 70, y), 'x', font=MX(40), fill=RED); d.text((2 * W + 120, y), t, font=MB(38), fill=INK); y += 64
    tag(3, 'STEP 3 · THE CLOCK')
    blk(3, 180, ['7 working', 'days.'], MX(110), INK, 1.0)
    blk(3, 440, ['With Aadhaar authentication. Queries only for missing, unclear or mismatched documents.', 'If the officer sits on it, approval can be deemed.'], MB(40), MUT, 1.3)
    tag(4, 'BEFORE YOU APPLY')
    blk(4, 180, ['The list is fixed.', 'Getting it right the', 'first time is not.'], MX(72), INK, 1.08)
    blk(4, 470, ['One wrong rent paper, one address mismatch, and the clock starts again.'], MB(40), RED, 1.3)
    x0 = 4 * W + (W - 620) // 2; pill(d, x0, 1150, 620, 100, 'Comment REGISTER', MX(54), INK, BG)
    ctx(d, 1262, "We'll check your papers first. Call 7020570215", MB(30), MUT, 4 * W + W / 2)
    for i in range(N):
        lg = LOGO.resize((56, 56)); lg.putalpha(lg.getchannel('A').point(lambda a: int(a * 0.45))); pano.alpha_composite(lg, (i * W + W - 116, H - 82))
        d = ImageDraw.Draw(pano)
        d.text((i * W + 70, H - 58), 'Source: CBIC Circular 257/03/2026-GST, 26.10.2026' if i in (0, 4) else '@ruyan_corporate_services', font=MB(24), fill=MUT)
    for i in range(N): pano.crop((i * W, 0, (i + 1) * W, H)).convert('RGB').save(f'{OUT}/news-register-{i + 1}.jpg', quality=92)
    pv = Image.new('RGB', (N * 270 + 60, 358), (40, 40, 40))
    for i in range(N): pv.paste(pano.crop((i * W, 0, (i + 1) * W, H)).convert('RGB').resize((270, 338)), (10 + i * 280, 10))
    pv.save(f'{OUT}/preview-register.jpg')

# ---------------- C: red-pen notice ----------------
def C():
    BG, INK, MUT, RED, PAP = (58, 62, 70), (30, 30, 34), (110, 110, 118), (214, 40, 40), (250, 249, 244)
    im = Image.new('RGBA', (W, H), BG + (255,)); d = ImageDraw.Draw(im)
    d.text((60, 56), 'GST notice says "fraud"', font=MX(64), fill=(255, 255, 255))
    d.text((60, 132), 'just because you paid late?', font=MX(56), fill=(255, 196, 120))
    px, py, pw, ph = 80, 240, 920, 760
    paper = Image.new('RGBA', (pw, ph), PAP + (255,)); pd = ImageDraw.Draw(paper)
    ctx(pd, 30, 'SHOW CAUSE NOTICE', MONOB(40), INK, pw / 2); ctx(pd, 84, 'under Section 74 of the CGST Act, 2017', MONO(26), MUT, pw / 2)
    pd.line((40, 130, pw - 40, 130), fill=(200, 200, 200), width=2)
    lines = ['The noticee has not paid tax of', 'Rs 3,48,600 for the period', 'Apr 2023 to Mar 2024.', '', 'Therefore, the noticee has', 'suppressed facts with intent', 'to evade tax, and penalty', 'equal to the tax is proposed.']
    y = 160
    for l in lines: pd.text((50, y), l, font=MONO(34), fill=INK); y += 52
    paper = paper.rotate(2, expand=True, resample=Image.BICUBIC, fillcolor=(0, 0, 0, 0))
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((px + 14, py + 20, px + pw + 14, py + ph + 20), fill=(0, 0, 0, 110))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18))); im.alpha_composite(paper, (px, py)); d = ImageDraw.Draw(im)
    # red pen marks
    d.line((px + 40, py + 470, px + 560, py + 466), fill=RED, width=6); d.line((px + 40, py + 520, px + 520, py + 516), fill=RED, width=6)
    d.ellipse((px + 470, py + 400, px + 900, py + 560), outline=RED, width=6)
    d.text((px + 520, py + 590), 'Where is the', font=KAL(52), fill=RED); d.text((px + 520, py + 650), 'evidence?', font=KAL(60), fill=RED)
    y = 1040
    d.text((60, y), 'CBIC (26 Oct): not paying tax alone is not fraud.', font=MB(36), fill=(255, 255, 255)); y += 48
    d.text((60, y), 'The notice must show the facts behind "intent".', font=MB(36), fill=(255, 255, 255)); y += 50
    d.text((60, y), 'Most replies never ask for them.', font=MB(36), fill=(255, 196, 120)); y += 70
    pill(d, 60, y, 500, 92, 'Comment SCN', MX(54), (255, 196, 120), INK)
    d.text((590, y + 6), 'Got a Section 74 notice?', font=MB(30), fill=(200, 204, 214)); d.text((590, y + 44), 'Call 7020570215', font=MX(34), fill=(255, 255, 255))
    foot(im, 'Source: CBIC Circular 258/04/2026-GST, 26.10.2026', (190, 194, 204))
    im.convert('RGB').save(f'{OUT}/news-scn.jpg', quality=93)

# ---------------- D: calendar ----------------
def D():
    BG, INK, MUT, ACC, RED = (236, 246, 240), (24, 48, 40), (96, 122, 112), (40, 140, 100), (210, 70, 60)
    im = Image.new('RGBA', (W, H), BG + (255,)); d = ImageDraw.Draw(im)
    d.text((60, 60), 'Cost audit report', font=MX(76), fill=INK); d.text((60, 146), 'still not filed?', font=MX(76), fill=RED)
    cx, cy, cw, ch = 140, 290, 800, 620
    d.rounded_rectangle((cx, cy, cx + cw, cy + ch), 30, fill=(255, 255, 255)); d.rounded_rectangle((cx, cy, cx + cw, cy + 110), 30, fill=ACC); d.rectangle((cx, cy + 80, cx + cw, cy + 110), fill=ACC)
    ctx(d, cy + 22, 'DECEMBER 2026', MX(54), (255, 255, 255), cx + cw / 2)
    days = ['M', 'T', 'W', 'T', 'F', 'S', 'S']; gw = cw / 7
    for i, t in enumerate(days): ctx(d, cy + 130, t, MB(30), MUT, cx + gw * i + gw / 2)
    start = 1  # 1 Dec 2026 is a Tuesday
    for n in range(1, 32):
        k = n - 1 + start; r, c = divmod(k, 7); x = cx + gw * c + gw / 2; y = cy + 190 + r * 78
        if n == 31:
            d.ellipse((x - 44, y - 12, x + 44, y + 70), outline=RED, width=7); ctx(d, y, '31', MX(44), RED, x)
        else: ctx(d, y, str(n), MB(36), INK if c < 5 else MUT, x)
    y = 950
    d.text((60, y), 'Form CRA-4 for FY 2025-26: MCA allows filing', font=MB(38), fill=INK); y += 50
    d.text((60, y), 'without additional fee till 31 December 2026.', font=MB(38), fill=INK); y += 62
    d.text((60, y), 'Many companies cross the cost audit limit and never notice.', font=MB(32), fill=RED); y += 66
    pill(d, 60, y, 470, 92, 'Comment COST', MX(54), INK, BG)
    d.text((560, y + 6), 'Not sure if it applies?', font=MB(30), fill=MUT); d.text((560, y + 44), 'Call 7020570215', font=MX(34), fill=INK)
    foot(im, 'Source: MCA General Circular 06/2026', MUT)
    im.convert('RGB').save(f'{OUT}/news-cra4.jpg', quality=93)

A(); B(); C(); D()
pv = Image.new('RGB', (4 * 270 + 50, 358), (40, 40, 40))
for i, n in enumerate(['news-delivery', 'news-register-1', 'news-scn', 'news-cra4']):
    pv.paste(Image.open(f'{OUT}/{n}.jpg').resize((270, 338)), (10 + i * 280, 10))
pv.save(f'{OUT}/preview-set.jpg'); print('ok')
