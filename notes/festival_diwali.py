"""Diwali 2026 festival posts (user 6 Nov: festival posts were missed). Dhanteras 6 Nov, Diwali/Lakshmi Puja 8 Nov, Padwa 10 Nov, Bhai Dooj 11 Nov.
Each festival gets its own layout + pastel-warm palette. Outputs feed post 1080x1350 + story 1080x1920. Brand block: name, branches, phone, website."""
import os, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
FD = '/home/claude/fonts/'
HX = lambda s: ImageFont.truetype(FD + 'Mukta-ExtraBold.ttf', s)
HB = lambda s: ImageFont.truetype(FD + 'Mukta-Bold.ttf', s)
EMO = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', 109)
OUT = '/home/claude/ruyan_automation/batch2/fest'; os.makedirs(OUT, exist_ok=True)
LOGO = Image.open('/home/claude/ruyan_automation/logo.png').convert('RGBA')
def emoji(ch, size):
    im = Image.new('RGBA', (150, 150), (0, 0, 0, 0)); ImageDraw.Draw(im).text((10, 10), ch, font=EMO, embedded_color=True)
    return im.crop(im.getbbox()).resize((size, size), Image.LANCZOS)
def ctext(d, W, y, t, f, col):
    tw = d.textlength(t, font=f); d.text(((W - tw) / 2, y), t, font=f, fill=col)
def glow(im, x, y, r, col):
    g = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse((x - r, y - r, x + r, y + r), fill=col + (110,))
    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(r * 0.6)))
def brand(im, d, W, H, ink, soft, acc):
    y = H - 250
    d.line((120, y, W - 120, y), fill=acc, width=3)
    lg = LOGO.resize((78, 78)); im.alpha_composite(lg, (W // 2 - 39, y + 22)); d = ImageDraw.Draw(im)
    ctext(d, W, y + 108, 'RUYAN CORPORATE SERVICES', HX(40), ink)
    ctext(d, W, y + 160, 'Pune  ·  Mumbai  ·  Chhatrapati Sambhajinagar  ·  Dhule', HB(28), soft)
    ctext(d, W, y + 200, 'Call / WhatsApp 7020570215  ·  www.ruyangroup.org', HB(28), soft)
    return d
def sparkles(d, W, H, col, n, seed):
    r = random.Random(seed)
    for _ in range(n):
        x, y, s = r.randint(30, W - 30), r.randint(30, H - 300), r.randint(3, 8)
        d.line((x - s, y, x + s, y), fill=col, width=2); d.line((x, y - s, x, y + s), fill=col, width=2)

def dhanteras(W, H):   # gold coins rising, cream + gold
    BG, INK, SOFT, ACC = (252, 244, 228), (92, 52, 24), (150, 112, 80), (214, 160, 60)
    im = Image.new('RGBA', (W, H), BG + (255,)); d = ImageDraw.Draw(im)
    glow(im, W // 2, int(H * 0.36), 300, (255, 214, 120)); d = ImageDraw.Draw(im); sparkles(d, W, H, ACC, 40, 1)
    coin = emoji('🪙', 120)
    for i, (x, y) in enumerate([(W // 2 - 60, int(H * 0.30)), (W // 2 - 190, int(H * 0.36)), (W // 2 + 70, int(H * 0.36)), (W // 2 - 60, int(H * 0.42))]):
        im.alpha_composite(coin, (x, y))
    pot = emoji('🏺', 170); im.alpha_composite(pot, (W // 2 - 85, int(H * 0.47))); d = ImageDraw.Draw(im)
    ctext(d, W, int(H * 0.08), 'Happy', HB(70), SOFT); ctext(d, W, int(H * 0.08) + 70, 'Dhanteras', HX(150), INK)
    y = int(H * 0.62)
    ctext(d, W, y, 'May your wealth grow', HB(50), INK); ctext(d, W, y + 64, 'and your books stay balanced.', HB(50), INK)
    return im, brand(im, d, W, H, INK, SOFT, ACC)

def diwali(W, H):      # row of diyas at the bottom, deep-peach night sky
    BG, INK, SOFT, ACC = (255, 232, 214), (110, 40, 40), (160, 96, 84), (232, 120, 70)
    im = Image.new('RGBA', (W, H), BG + (255,)); d = ImageDraw.Draw(im)
    for k in range(6):  # soft arches
        d.arc((W // 2 - 380 - k * 40, int(H * 0.05) - k * 40, W // 2 + 380 + k * 40, int(H * 0.75) + k * 40), 200, 340, fill=(250, 210, 190), width=4)
    sparkles(d, W, H, ACC, 30, 2)
    diya = emoji('🪔', 120); yb = int(H * 0.52)
    for i in range(5):
        x = W // 2 - 300 + i * 150 - 60; glow(im, x + 60, yb + 20, 90, (255, 190, 90)); im.alpha_composite(diya, (x, yb))
    d = ImageDraw.Draw(im)
    ctext(d, W, int(H * 0.12), 'Shubh', HB(76), SOFT); ctext(d, W, int(H * 0.12) + 78, 'Deepavali', HX(160), INK)
    ctext(d, W, int(H * 0.36), 'May every lamp light up', HB(48), INK); ctext(d, W, int(H * 0.36) + 62, 'a new opportunity for your business.', HB(44), INK)
    ctext(d, W, int(H * 0.66), 'Wishing you and your family a bright,', HB(40), SOFT); ctext(d, W, int(H * 0.66) + 52, 'prosperous Diwali.', HB(40), SOFT)
    return im, brand(im, d, W, H, INK, SOFT, ACC)

def padwa(W, H):       # new account book (vahi) — the traders' new year in Maharashtra
    BG, INK, SOFT, ACC = (244, 238, 250), (70, 40, 100), (128, 104, 150), (190, 120, 60)
    im = Image.new('RGBA', (W, H), BG + (255,)); d = ImageDraw.Draw(im); sparkles(d, W, H, (200, 170, 220), 30, 3)
    bx, by, bw, bh = W // 2 - 260, int(H * 0.30), 520, 360
    d.rounded_rectangle((bx, by, bx + bw, by + bh), 22, fill=(176, 40, 48)); d.rounded_rectangle((bx + 20, by + 20, bx + bw - 20, by + bh - 20), 16, outline=(240, 200, 110), width=6)
    ctext(d, W, by + 90, 'शुभ लाभ', HX(70), (250, 220, 140)) if False else None
    sw = emoji('🪷', 110); im.alpha_composite(sw, (W // 2 - 55, by + 60)); d = ImageDraw.Draw(im)
    ctext(d, W, by + 200, 'NEW BOOKS', HX(60), (250, 220, 140)); ctext(d, W, by + 270, 'SHUBH LABH', HB(36), (250, 220, 140))
    ctext(d, W, int(H * 0.08), 'Happy', HB(70), SOFT); ctext(d, W, int(H * 0.08) + 72, 'Diwali Padwa', HX(130), INK)
    y = by + bh + 60
    ctext(d, W, y, 'New year, new books.', HB(52), INK); ctext(d, W, y + 66, 'Start them clean. We keep them that way.', HB(40), SOFT)
    return im, brand(im, d, W, H, INK, SOFT, ACC)

def bhaidooj(W, H):    # tilak + thali, two-tone split
    BG, INK, SOFT, ACC = (255, 238, 236), (120, 40, 70), (170, 100, 120), (220, 110, 120)
    im = Image.new('RGBA', (W, H), BG + (255,)); d = ImageDraw.Draw(im)
    d.ellipse((W // 2 - 330, int(H * 0.22), W // 2 + 330, int(H * 0.22) + 660), fill=(255, 224, 220)); sparkles(d, W, H, ACC, 30, 4)
    thali = emoji('🪔', 130); sweet = emoji('🍬', 110); gift = emoji('🎁', 110)
    im.alpha_composite(thali, (W // 2 - 65, int(H * 0.36))); im.alpha_composite(sweet, (W // 2 - 230, int(H * 0.40))); im.alpha_composite(gift, (W // 2 + 120, int(H * 0.40)))
    d = ImageDraw.Draw(im)
    ctext(d, W, int(H * 0.08), 'Happy', HB(70), SOFT); ctext(d, W, int(H * 0.08) + 72, 'Bhai Dooj', HX(150), INK)
    y = int(H * 0.58)
    ctext(d, W, y, 'To the ones who always have your back', HB(44), INK); ctext(d, W, y + 60, 'in family, and in business.', HB(44), INK)
    return im, brand(im, d, W, H, INK, SOFT, ACC)

for name, fn in [('dhanteras', dhanteras), ('diwali', diwali), ('padwa', padwa), ('bhaidooj', bhaidooj)]:
    for tag, (W, H) in [('post', (1080, 1350)), ('story', (1080, 1920))]:
        im, d = fn(W, H); im.convert('RGB').save(f'{OUT}/{name}-{tag}.jpg', quality=93)
pv = Image.new('RGB', (4 * 270 + 50, 338 + 20), (50, 50, 50))
for i, n in enumerate(['dhanteras', 'diwali', 'padwa', 'bhaidooj']):
    pv.paste(Image.open(f'{OUT}/{n}-post.jpg').resize((270, 338)), (10 + i * 280, 10))
pv.save(f'{OUT}/preview.jpg'); print('ok')
