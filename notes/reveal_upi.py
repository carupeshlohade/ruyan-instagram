"""'Swipe to reveal' (blurred) carousel — UPI fraud case (5 Nov). Each slide shows the next card BLURRED at the bottom; the next slide
shows it sharp. The final answer (reporting deadline) stays blurred: Comment UPI to unblur. Case: Raja Sachdeva v. Axis Bank, DCDRC Chandigarh."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H = 1080, 1350
FD = '/home/claude/fonts/'
HX = lambda s: ImageFont.truetype(FD + 'Mukta-ExtraBold.ttf', s)
HB = lambda s: ImageFont.truetype(FD + 'Mukta-Bold.ttf', s)
BG, INK, MUT, ACC, RED, GRN, CARD = (18, 38, 44), (245, 240, 230), (160, 184, 186), (255, 196, 110), (255, 110, 100), (110, 220, 160), (250, 248, 242)
DARK = (30, 34, 40)
def wrap(d, txt, f, w):
    out, cur = [], ''
    for wd in txt.split():
        t = (cur + ' ' + wd).strip()
        if d.textlength(t, font=f) <= w: cur = t
        else: out.append(cur); cur = wd
    return out + [cur]
def card(kind):
    c = Image.new('RGBA', (900, 420), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rounded_rectangle((0, 0, 899, 419), 40, fill=CARD + (255,))
    if kind == 'sms':
        d.rounded_rectangle((40, 40, 120, 120), 20, fill=(40, 110, 200)); d.text((58, 52), 'UPI', font=HX(30), fill='white')
        d.text((145, 45), 'BANK ALERT  ·  11 Sep, 4:12 PM', font=HB(30), fill=(110, 110, 120))
        d.text((145, 90), 'Rs 97,000.00 debited', font=HX(58), fill=DARK)
        d.text((40, 190), 'from A/c XX4821 via UPI to an unknown VPA.', font=HB(36), fill=(70, 70, 80))
        d.text((40, 245), 'Not you? Call customer care.', font=HB(36), fill=(70, 70, 80))
        d.rounded_rectangle((40, 320, 400, 380), 30, fill=(255, 225, 220)); d.text((66, 326), 'He never paid this', font=HB(34), fill=(190, 50, 40))
    elif kind == 'bank':
        d.text((40, 40), 'Reply from the bank', font=HB(30), fill=(110, 110, 120))
        y = 95
        for ln in wrap(d, '"The transaction was authorised with OTP and PIN. Since the OTP was shared, the refund cannot be processed."', HB(40), 820):
            d.text((40, y), ln, font=HB(40), fill=DARK); y += 54
        d.rounded_rectangle((40, 335, 330, 390), 28, fill=(255, 225, 220)); d.text((64, 340), 'REFUND REFUSED', font=HX(32), fill=(190, 50, 40))
    elif kind == 'order':
        d.text((40, 40), 'Consumer Commission, Chandigarh', font=HB(30), fill=(110, 110, 120))
        d.text((40, 85), 'Bank must refund', font=HX(62), fill=(30, 130, 80))
        for i, ln in enumerate(['₹97,000 + 6% interest', '+ ₹20,000 compensation', 'No OTP record. No device ID. No IP logs.']):
            d.text((40, 180 + i * 56), ln, font=HB(40), fill=DARK)
    elif kind == 'deadline':
        d.text((40, 40), 'Report UPI fraud within', font=HB(40), fill=(110, 110, 120))
        d.text((40, 110), '3 working days', font=HX(110), fill=(190, 50, 40))   # stays blurred on purpose
        d.text((40, 290), 'to keep your loss at zero', font=HB(40), fill=DARK)
    return c
CARDS = {k: card(k) for k in ('sms', 'bank', 'order', 'deadline')}
def blurred(c, r=26):
    b = c.filter(ImageFilter.GaussianBlur(r)); return b
def base(i, n=5):
    im = Image.new('RGBA', (W, H), BG + (255,)); d = ImageDraw.Draw(im)
    for k in range(n):  # dots
        x = W // 2 - (n - 1) * 18 + k * 36; d.ellipse((x - 7, 70, x + 7, 84), fill=ACC if k == i else (70, 92, 98))
    d.text((70, H - 80), '@ruyan_corporate_services', font=HB(28), fill=MUT)
    lg = Image.open('/home/claude/ruyan_automation/logo.png').convert('RGBA').resize((64, 64)); lg.putalpha(lg.getchannel('A').point(lambda a: int(a * 0.45)))
    im.alpha_composite(lg, (W - 120, H - 100))
    return im, d
def text(d, y, lines, f, col, lh=1.12):
    for ln in lines:
        for l2 in wrap(d, ln, f, W - 140): d.text((70, y), l2, font=f, fill=col); y += int(f.size * lh)
    return y
def peek(im, d, c, label):  # next card, blurred, at the bottom
    im.alpha_composite(blurred(c, 30), (90, 830)); d = ImageDraw.Draw(im)
    tw = d.textlength(label, font=HB(36)); d.rounded_rectangle(((W - tw) / 2 - 30, 1000, (W + tw) / 2 + 30, 1060), 30, fill=(18, 38, 44))
    d.text(((W - tw) / 2, 1006), label, font=HB(36), fill=ACC)
slides = []
im, d = base(0); text(d, 170, ['A notification', 'he never expected.'], HX(92), INK); text(d, 420, ['Swipe to reveal what happened to his account.'], HB(44), MUT)
peek(im, d, CARDS['sms'], 'Swipe to reveal  >>'); slides.append(im)
im, d = base(1); text(d, 125, ['REAL CASE · UPI FRAUD'], HB(34), ACC); im.alpha_composite(CARDS['sms'], (90, 195)); d = ImageDraw.Draw(im)
text(d, 655, ['Random Google Pay requests 2 days earlier.', 'He ignored them.'], HB(42), MUT, 1.3)
d.text((70, 775), 'Illustration based on the reported case', font=HB(26), fill=(110, 134, 138))
peek(im, d, CARDS['bank'], 'What did the bank say?  >>'); slides.append(im)
im, d = base(2); text(d, 125, ['THE BANK'], HB(34), ACC); im.alpha_composite(CARDS['bank'], (90, 195)); d = ImageDraw.Draw(im)
text(d, 655, ['"Your fault."', 'Customer care: no help.'], HX(60), RED, 1.15)
peek(im, d, CARDS['order'], 'He went to the Consumer Commission  >>'); slides.append(im)
im, d = base(3); text(d, 125, ['THE ORDER'], HB(34), ACC); im.alpha_composite(CARDS['order'], (90, 195)); d = ImageDraw.Draw(im)
text(d, 655, ['"Mere receipt of SMS does not', 'establish the customer authorised it."'], HB(44), GRN, 1.25)
peek(im, d, CARDS['deadline'], 'But there is a catch  >>'); slides.append(im)
im, d = base(4); text(d, 150, ['THE CATCH'], HB(34), ACC)
text(d, 230, ['There is a deadline', 'to report UPI fraud.'], HX(76), INK)
text(d, 430, ['Miss it, and the loss can become yours.'], HB(46), RED)
im.alpha_composite(blurred(CARDS['deadline'], 42), (90, 560)); d = ImageDraw.Draw(im)
bw = 640; x0 = (W - bw) // 2
d.rounded_rectangle((x0, 1050, x0 + bw, 1160), 55, fill=ACC)
f = HX(62); t = 'Comment UPI'; tw = d.textlength(t, font=f); d.text(((W - tw) / 2, 1062), t, font=f, fill=BG)
f = HB(32); t = 'to unblur it. Or call 7020570215'; tw = d.textlength(t, font=f); d.text(((W - tw) / 2, 1180), t, font=f, fill=MUT)
slides.append(im)
out = '/home/claude/ruyan_automation/batch2/media14'; os.makedirs(out, exist_ok=True)
for i, s in enumerate(slides, 1): s.convert('RGB').save(f'{out}/case-upi-{i}.jpg', quality=92)
pv = Image.new('RGB', (5 * 270 + 60, 338 + 20), (40, 40, 40))
for i, s in enumerate(slides): pv.paste(s.convert('RGB').resize((270, 338)), (10 + i * 280, 10))
pv.save(f'{out}/preview-case-upi.jpg'); print('ok')
