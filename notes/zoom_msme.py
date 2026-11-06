"""'Swipe to zoom' carousel — MSME late-payment interest (6 Nov). One big invoice; each slide zooms closer into a detail.
Case: SRK Metals and Plastics v. State of Assam, Gauhati HC, WP(C) 8288/2019 (LiveLawBiz 14.08.2026)."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H = 1080, 1350
FD = '/home/claude/fonts/'
HX = lambda s: ImageFont.truetype(FD + 'Mukta-ExtraBold.ttf', s)
HB = lambda s: ImageFont.truetype(FD + 'Mukta-Bold.ttf', s)
BG, INK, MUT, ACC, RED, GRN = (241, 236, 252), (40, 32, 78), (112, 102, 142), (124, 82, 222), (200, 60, 60), (30, 130, 90)
# --- the invoice (big canvas) ---
IW, IH = 2000, 2600
inv = Image.new('RGB', (IW, IH), (253, 252, 247)); d = ImageDraw.Draw(inv)
d.rectangle((0, 0, IW, 220), fill=(70, 52, 140)); d.text((80, 60), 'TAX INVOICE', font=HX(110), fill='white')
d.text((80, 300), 'Supplier: MSME manufacturer (Udyam registered)', font=HB(56), fill=INK)
d.text((80, 380), 'Buyer: Government department', font=HB(56), fill=INK)
d.rounded_rectangle((80, 520, 1000, 760), 20, outline=(200, 210, 205), width=4)
d.text((120, 550), 'Invoice date', font=HB(48), fill=MUT); d.text((120, 620), '05 Jan 2018', font=HX(80), fill=INK)
d.rounded_rectangle((1040, 520, 1920, 760), 20, outline=ACC, width=8)
d.text((1080, 550), 'Payment due', font=HB(48), fill=MUT); d.text((1080, 620), 'within 45 days', font=HX(80), fill=ACC)
for i, (a, b) in enumerate([('Item', 'Amount'), ('MS pipes & fittings', '₹ 18,40,000'), ('GST', '₹ 3,31,200'), ('TOTAL', '₹ 21,71,200')]):
    y = 880 + i * 120; d.line((80, y + 100, 1920, y + 100), fill=(220, 225, 222), width=3)
    d.text((100, y), a, font=HX(58) if i in (0, 3) else HB(56), fill=INK); tw = d.textlength(b, font=HB(56)); d.text((1900 - tw, y), b, font=HX(58) if i in (0, 3) else HB(56), fill=INK)
# paid-late stamp
st = Image.new('RGBA', (900, 300), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
sd.rounded_rectangle((10, 10, 890, 290), 30, outline=RED, width=14); sd.text((70, 40), 'PAID', font=HX(130), fill=RED); sd.text((70, 190), '8 months late', font=HB(64), fill=RED)
st = st.rotate(-10, expand=True, resample=Image.BICUBIC); inv.paste(st, (950, 1430), st)
d = ImageDraw.Draw(inv)
d.text((80, 1850), 'Interest on delayed payment:', font=HB(64), fill=INK)
d.rounded_rectangle((80, 1950, 1920, 2200), 26, fill=(250, 236, 220)); d.text((140, 2010), '₹ ________   (never claimed)', font=HX(96), fill=(160, 120, 90))
d.text((80, 2350), 'Signature', font=HB(48), fill=MUT)
def zoom(cx, cy, cw, h=760):  # crop width cw (invoice px) around (cx,cy), scaled to a 940xh window
    ch = cw * h / 940; x0 = max(0, min(IW - cw, cx - cw / 2)); y0 = max(0, min(IH - ch, cy - ch / 2))
    return inv.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((940, h), Image.LANCZOS)
def frame(i, crop, top, sub, hint=None, n=5):
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    d.text((70, 60), 'SWIPE TO ZOOM IN', font=HB(30), fill=MUT); d.text((W - 150, 60), f'{i}/{n}', font=HB(30), fill=MUT)
    for k in range(i):  # zoom-level bars
        d.rounded_rectangle((70 + k * 46, 110, 106 + k * 46, 122), 6, fill=ACC)
    y = 160
    for ln in top: d.text((70, y), ln[0], font=HX(ln[1]), fill=ln[2]); y += int(ln[1] * 1.12)
    y += 30; ch = crop.size[1]
    sh = Image.new('RGBA', (980, 800), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((20, 20, 960, 20 + ch), 24, fill=(0, 0, 0, 60))
    im.paste(sh.filter(ImageFilter.GaussianBlur(12)), (50, y + 10), sh.filter(ImageFilter.GaussianBlur(12)))
    im.paste(crop, (70, y)); d.rounded_rectangle((70, y, 1010, y + ch), 22, outline=(208, 200, 230), width=4)
    y += ch + 30
    for ln in sub: d.text((70, y), ln, font=HB(38), fill=INK); y += 50
    if hint: hint(d, im)
    lg = Image.open('/home/claude/ruyan_automation/logo.png').convert('RGBA').resize((60, 60)); lg.putalpha(lg.getchannel('A').point(lambda a: int(a * 0.45)))
    im.paste(lg, (W - 110, H - 90), lg); d.text((70, H - 75), '@ruyan_corporate_services', font=HB(26), fill=MUT)
    return im
S = []
full = Image.new('RGB', (940, 700), (244, 248, 246)); full.paste(inv.resize((538, 700), Image.LANCZOS), (201, 0))
S.append(frame(1, full, [('Your customer paid.', 74, INK), ('8 months late.', 74, RED)], ['Swipe and zoom in. Something on this invoice', 'is still unpaid. (Illustrative invoice)']))
S.append(frame(2, zoom(1300, 620, 1300, 700), [('Zoom 1', 40, ACC), ('Due in 45 days.', 74, INK)], ['The law gives MSME suppliers a fixed payment limit.', 'This buyer crossed it by months.']))
S.append(frame(3, zoom(1380, 1620, 1250, 700), [('Zoom 2', 40, ACC), ('Paid. Finally.', 74, INK)], ['The buyer then said: "Principal is paid.', 'Your interest claim is over."']))
def court(d, im):
    d.rounded_rectangle((70, 1000, 1010, 1160), 22, fill=(220, 242, 230)); d.text((100, 1020), 'Gauhati High Court: the interest claim', font=HB(36), fill=GRN)
    d.text((100, 1070), 'survives, even after principal is paid.', font=HB(36), fill=GRN)
S.append(frame(4, zoom(900, 2060, 1250, 560), [('Zoom 3', 40, ACC), ('This line is still open.', 70, INK)], [], court))
def cta(d, im):
    d.rounded_rectangle((170, 1080, 910, 1175), 50, fill=INK); t = 'Comment MSME'; tw = d.textlength(t, font=HX(60)); d.text(((W - tw) / 2, 1086), t, font=HX(60), fill=BG)
    t = "We'll tell you how much is yours. Call 7020570215"; tw = d.textlength(t, font=HB(30)); d.text(((W - tw) / 2, 1190), t, font=HB(30), fill=MUT)
blank = zoom(700, 2075, 1100, 520).filter(ImageFilter.GaussianBlur(3))
S.append(frame(5, blank, [('Most suppliers never', 64, INK), ('fill this line.', 64, RED)], ['There is one registration you need first,', 'and one rate the law fixes for you.'], cta))
out = '/home/claude/ruyan_automation/batch2/media15'; os.makedirs(out, exist_ok=True)
for i, s in enumerate(S, 1): s.save(f'{out}/case-msme-{i}.jpg', quality=92)
pv = Image.new('RGB', (5 * 270 + 60, 338 + 20), (40, 40, 40))
for i, s in enumerate(S): pv.paste(s.resize((270, 338)), (10 + i * 280, 10))
pv.save(f'{out}/preview-case-msme.jpg'); print('ok')
