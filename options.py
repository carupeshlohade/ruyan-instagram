"""Renders 3 design/hook options (A/B/C) per slot for the chosen weeks, plus a single option A for others.
Writes options.json (slot -> options) and media/ images. Warm pastel palettes only."""
import json, re, os, sys, datetime as dt, openpyxl
import build_posts as bp
from PIL import Image

POOL = [  # bg, text, accent, muted, line  (all warm pastels)
 ((251,227,211),(59,42,34),(196,112,82),(125,96,82),(225,190,170)),   # peach
 ((255,241,201),(58,50,34),(190,134,30),(122,108,74),(234,214,150)),  # butter
 ((247,217,217),(64,43,46),(183,95,90),(128,94,96),(232,188,188)),    # blush
 ((253,224,196),(66,44,28),(204,115,50),(132,98,70),(236,196,158)),   # apricot
 ((244,230,212),(60,46,34),(168,116,74),(125,104,84),(220,200,174)),  # sand
 ((250,218,224),(66,40,48),(194,90,110),(132,92,100),(236,190,200)),  # rose
 ((255,230,205),(62,42,30),(214,120,80),(130,98,76),(240,200,165)),   # melon
 ((253,236,214),(60,46,32),(176,124,52),(124,104,78),(232,208,172)),  # honey cream
]
PAL = {}
HOOKS = {  # extra hooks for week 1 (B and C); A comes from the calendar
 "2026-10-08": ["Starting a business in Pune? Here is everything you will need help with in year one.",
                "One consultancy for GST, tax, loans, subsidy and company setup. Here is how we help."],
 "2026-10-09": ["Do you need GST registration? Check these four cases before you decide.",
                "Turnover under the limit and still need GST? Yes, in some cases."],
 "2026-10-10": ["GSTR-1 is due 11 October. Have your sales data ready today.",
                "Two GST dates this month. Save them before you forget."],
 "2026-10-11": ["Which business structure suits you? Three questions will tell you.",
                "Private Limited, LLP or proprietorship: what changes for you, in 30 seconds."],
 "2026-10-12": ["Old or new tax regime? Run this five-question check before you file.",
                "Most people pick their tax regime without calculating. Do this instead."],
 "2026-10-13": ["Your business made a profit but the bank is empty. Here is why.",
                "Profit and cash are different things. Here is a simple example."],
 "2026-10-14": ["Applying for a business loan? Keep these eight documents ready.",
                "Why banks delay business loans, and the eight documents that prevent it."],
}
WEEK1 = set(HOOKS)

def setpal(k):
    bp.BG, bp.FG, bp.ACC, bp.MUT, bp.LINE = POOL[PAL[k]]

def render(slot, fmt, pillar, hook, pts, cta, tags, opt):
    setpal(opt + slot); files = []
    if fmt == "Static":
        im, d = bp.frame(pillar); y = bp.body(d, hook, "Bold", 70, bottom=700); yy = y + 50
        for p in pts[:4]:
            fp, Lp, sp = bp.fit(d, "- " + p, "Regular", bp.W - 140, 120, 36)
            for ln in Lp:
                if yy < bp.H - 190: d.text((70, yy), ln, font=fp, fill=bp.MUT); yy += int(sp * 1.3)
            yy += 14
        fn = f"{slot}-static-{opt}.png"; im.save("media/" + fn); files = [fn]
    elif fmt == "Carousel":
        slides = [("Swipe", hook)] + [(f"Point {i+1}", p) for i, p in enumerate(pts[:8])] + [("Next step", cta + "  Call 7020570215")]
        for i, (tag, txt) in enumerate(slides, 1):
            im, d = bp.frame(pillar if i == 1 else tag, i, len(slides))
            bp.body(d, txt, "Bold" if i in (1, len(slides)) else "Bold", 66 if i == 1 else 56)
            fn = f"{slot}-carousel-{opt}-{i}.png"; im.save("media/" + fn); files.append(fn)
    return files

def main(xlsx):
    for f in os.listdir("media"): os.remove("media/" + f)
    wb = openpyxl.load_workbook(xlsx, data_only=True); ws = wb["Oct 2026 Calendar"]
    hdr = [c.value for c in ws[4]]; out = {}
    for raw in ws.iter_rows(min_row=5, values_only=True):
        if not raw[0]: continue
        r = dict(zip(hdr, raw)); slot = r["Date"].date().isoformat(); fmt = r["Format"]
        pts = [re.sub(r"^(one date card|checklist frame):\s*", "", p.strip(), flags=re.I) for p in str(r["Key points / on-screen text"]).split("|") if p.strip()]
        pts = [p for p in pts if not re.match(r"^(slide \d+|cta slide|close:?)\b", p, re.I)]
        hooks = [r["Hook (spoken / headline)"]] + HOOKS.get(slot, [])
        t = r["Post time (IST)"]; t = t.strftime("%H:%M") if hasattr(t, "strftime") else "19:30"
        opts = {}
        di = r["Date"].date().toordinal()
        for j, kk in enumerate("ABC"): PAL[kk + slot] = (di * 3 + j * 3) % len(POOL)
        for k, h in zip("ABC", hooks):
            files = render(slot, fmt, r["Pillar"], h, pts, r["CTA"], r["Hashtags"], k) if fmt != "Reel" else []
            opts[k] = {"hook": h, "files": files, "caption": bp.caption(r, h, pts, r["CTA"], r["Hashtags"]),
                       "palette": PAL[k + slot] if fmt != "Reel" else ""}
        out[slot] = {"date": slot, "time": t, "format": fmt, "pillar": r["Pillar"], "topic": r["Topic"],
                     "points": pts, "verify": r.get("Verify before posting"), "options": opts}
    json.dump(out, open("options.json", "w"), indent=1, ensure_ascii=False)
    print(len(out), "slots,", len(os.listdir("media")), "images")
if __name__ == "__main__": main(sys.argv[1])
