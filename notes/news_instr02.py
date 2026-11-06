"""Static news post (6 Nov) — CBIC Instruction 02/2026-GST dt 30.10.2026: no arrests, truck checks limited, no SCN below Rs 10,000.
New format: newspaper front page (masthead, headline, 3 'columns'), owner problem first, hint + Comment GST."""
import os
from PIL import Image, ImageDraw, ImageFont
W, H = 1080, 1350
FD = '/home/claude/fonts/'
F = lambda n, s: ImageFont.truetype(FD + n, s)
SER, MB, MX = (lambda s: F('Gloock-Regular.ttf', s)), (lambda s: F('Mukta-Bold.ttf', s)), (lambda s: F('Mukta-ExtraBold.ttf', s))
EMO = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', 109)
PAPER, INK, MUT, RED, RULE = (245, 240, 228), (24, 22, 20), (104, 96, 86), (190, 40, 36), (60, 56, 50)
def emoji(ch, size):
    im = Image.new('RGBA', (150, 150), (0, 0, 0, 0)); ImageDraw.Draw(im).text((10, 10), ch, font=EMO, embedded_color=True)
    return im.crop(im.getbbox()).resize((size, size), Image.LANCZOS)
def ct(d, y, t, f, c):
    d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=c)
im = Image.new('RGBA', (W, H), PAPER + (255,)); d = ImageDraw.Draw(im)
# masthead
d.line((60, 60, W - 60, 60), fill=RULE, width=3)
ct(d, 72, 'THE OWNER\'S DAILY', SER(58), INK)
d.line((60, 150, W - 60, 150), fill=RULE, width=2); d.line((60, 156, W - 60, 156), fill=RULE, width=1)
d.text((60, 162), 'GST  ·  BREAKING', font=MB(26), fill=RED)
t = 'Friday, 6 November 2026'; d.text((W - 60 - d.textlength(t, font=MB(26)), 162), t, font=MB(26), fill=MUT)
d.line((60, 200, W - 60, 200), fill=RULE, width=1)
# problem-first lead
y = 228
for ln in ['Truck stopped on the highway.', 'A GST notice for ₹4,000.', 'An officer who says "arrest".']:
    d.text((60, y), ln, font=MB(40), fill=MUT); y += 52
y += 14
for ln in ['From 30 October,', 'all three changed.']:
    d.text((60, y), ln, font=SER(92), fill=INK); y += 100
y += 18
d.rounded_rectangle((60, y, 470, y + 46), 8, fill=RED); d.text((76, y + 4), 'IN FORCE NOW, NOT 2027', font=MX(30), fill=PAPER)
y += 80
# three columns
cols = [('🚫', 'Arrests', ['No further GST', 'arrests till the', 'law is amended']),
        ('🚚', 'Truck checks', ['Only on specific', 'intelligence, with', 'written reasons']),
        ('📩', 'Small notices', ['No SCN where tax', 'involved is below', '₹10,000 in total'])]
cw = (W - 120 - 2 * 30) // 3
d.line((60, y - 14, W - 60, y - 14), fill=RULE, width=2)
for i, (e, h, ls) in enumerate(cols):
    x = 60 + i * (cw + 30)
    if i: d.line((x - 15, y, x - 15, y + 330), fill=(200, 192, 178), width=2)
    im.alpha_composite(emoji(e, 70), (x, y + 6)); d = ImageDraw.Draw(im)
    d.text((x, y + 92), h, font=SER(44), fill=INK)
    yy = y + 160
    for l in ls: d.text((x, yy), l, font=MB(31), fill=INK); yy += 42
y += 350
d.line((60, y, W - 60, y), fill=RULE, width=2)
# hint + CTA
y += 22
d.text((60, y), 'But there are exceptions. And a notice already', font=MB(36), fill=INK); y += 46
d.text((60, y), 'in your hand is a different story.', font=MB(36), fill=RED); y += 74
bw = 560; x0 = 60
d.rounded_rectangle((x0, y, x0 + bw, y + 96), 48, fill=INK)
t = 'Comment GST'; f = MX(56); d.text((x0 + (bw - d.textlength(t, font=f)) / 2, y + 12), t, font=f, fill=PAPER)
d.text((x0 + bw + 30, y + 8), 'Stuck with one?', font=MB(30), fill=MUT)
d.text((x0 + bw + 30, y + 46), 'Call 7020570215', font=MX(34), fill=INK)
# footer
d.text((60, H - 70), 'Source: CBIC Instruction No. 02/2026-GST, 30.10.2026', font=MB(24), fill=MUT)
lg = Image.open('/home/claude/ruyan_automation/logo.png').convert('RGBA').resize((56, 56)); lg.putalpha(lg.getchannel('A').point(lambda a: int(a * 0.5)))
im.alpha_composite(lg, (W - 116, H - 92)); d = ImageDraw.Draw(im)
t = '@ruyan_corporate_services'; d.text((W - 130 - d.textlength(t, font=MB(24)), H - 70), t, font=MB(24), fill=MUT)
out = '/home/claude/ruyan_automation/batch2/media16'; os.makedirs(out, exist_ok=True)
im.convert('RGB').save(f'{out}/news-instr02.jpg', quality=93); print('ok', y)
