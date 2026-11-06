"""9:16 story from a feed post (user 6 Nov: stories go out automatically, no music needed).
usage: story_from_post.py post.jpg out.jpg"""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
src, out = sys.argv[1], sys.argv[2]
W, H = 1080, 1920; FD = '/home/claude/fonts/'
MB, MX = (lambda s: ImageFont.truetype(FD + 'Mukta-Bold.ttf', s)), (lambda s: ImageFont.truetype(FD + 'Mukta-ExtraBold.ttf', s))
p = Image.open(src).convert('RGB')
bg = p.resize((W, int(p.height * W / p.width))).resize((W, H)).filter(ImageFilter.GaussianBlur(40))
bg = Image.blend(bg, Image.new('RGB', (W, H), (20, 20, 24)), 0.45).convert('RGBA')
cw = 920; card = p.resize((cw, int(p.height * cw / p.width)), Image.LANCZOS); ch = card.height
y = (H - ch) // 2 + 20
sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((80, y + 16, 80 + cw, y + ch + 16), 28, fill=(0, 0, 0, 140))
bg.alpha_composite(sh.filter(ImageFilter.GaussianBlur(20)))
m = Image.new('L', card.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, cw, ch), 28, fill=255)
bg.paste(card, (80, y), m); d = ImageDraw.Draw(bg)
t = 'NEW POST'; f = MX(44); tw = d.textlength(t, font=f); d.rounded_rectangle(((W - tw) / 2 - 34, y - 120, (W + tw) / 2 + 34, y - 44), 38, fill=(255, 255, 255)); d.text(((W - tw) / 2, y - 114), t, font=f, fill=(20, 20, 24))
for i, (t, f) in enumerate([('Full post on our profile', MB(42)), ('@ruyan_corporate_services', MB(36))]):
    tw = d.textlength(t, font=f); d.text(((W - tw) / 2, y + ch + 50 + i * 58), t, font=f, fill=(255, 255, 255))
bg.convert('RGB').save(out, quality=92); print('ok')
