"""Animated 1080x1920 Reels: staggered text reveals, drifting shapes, circular wipe transitions, music."""
import os, subprocess, math, numpy as np
from PIL import Image, ImageDraw, ImageFilter
import build_posts as bp, options as op, music
from reels import REELS
W, H, FPS, TR = 1080, 1920, 30, 0.6
def ease(x): x = max(0, min(1, x)); return 1 - (1 - x) ** 3
def snap(d): return max(3.75, math.ceil(d / 1.25) * 1.25)
LOGO = Image.open("logo.png").split()[3]
def blob(r, col, a):
    im = Image.new("RGBA", (r*2, r*2), col + (0,)); m = Image.new("L", (r*2, r*2), 0)
    ImageDraw.Draw(m).ellipse((r*0.4, r*0.4, r*1.6, r*1.6), fill=int(255*a)); m = m.filter(ImageFilter.GaussianBlur(r*0.16)); im.putalpha(m); return im
class Scene:
    def __init__(s, idx, total, tag, text, dur, pal):
        s.dur, s.idx, s.total = dur, idx, total
        bp.BG, bp.FG, bp.ACC, bp.MUT, bp.LINE = op.POOL[pal]; s.bg, s.fg, s.acc, s.line = bp.BG, bp.FG, bp.ACC, bp.LINE
        d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
        hook = tag == "Hook"
        f, L, sz = bp.fit(d, text, "Bold", W - 170, 800, 88 if hook else 70, 44)
        s.lines = []
        for ln in L:
            im = Image.new("RGBA", (W, int(sz*1.35)), (0,0,0,0)); ImageDraw.Draw(im).text((85, 0), ln, font=f, fill=s.fg + (255,)); s.lines.append(im)
        s.lh = int(sz * 1.28); s.top = 640 if hook else 700
        s.tag = None
        if not hook:
            tf = bp.font("Bold", 34); wd = int(d.textlength(tag.upper(), font=tf)) + 56
            im = Image.new("RGBA", (wd, 70), (0,0,0,0)); dd = ImageDraw.Draw(im)
            dd.rounded_rectangle((0, 0, wd-1, 69), 35, fill=s.acc + (255,)); dd.text((28, 35), tag.upper(), font=tf, fill=s.bg + (255,), anchor="lm"); s.tag = im
        s.num = None
        if not hook and tag != "Enquiries":
            im = Image.new("RGBA", (500, 360), (0,0,0,0)); ImageDraw.Draw(im).text((0, 0), f"{idx:02d}", font=bp.font("Bold", 300), fill=s.acc + (60,)); s.num = im
        hd = Image.new("RGBA", (W, 130), (0,0,0,0)); lg = Image.new("RGBA", (96, 96), s.fg + (255,)); lg.putalpha(LOGO.resize((96, 96), Image.LANCZOS)); hd.paste(lg, (85, 10), lg)
        ImageDraw.Draw(hd).text((205, 58), "RUYAN CORPORATE SERVICES", font=bp.font("Bold", 28), fill=s.fg + (255,), anchor="lm"); s.hd = hd
        wm = Image.new("RGBA", (900, 900), s.fg + (0,)); wm.putalpha(LOGO.resize((900, 900), Image.LANCZOS).point(lambda v: int(v * 0.10))); s.wm = wm
        s.b1, s.b2 = blob(380, s.acc, 0.22), blob(300, s.fg, 0.07)
    def frame(s, t, g):  # t local seconds, g global seconds
        im = Image.new("RGBA", (W, H), s.bg + (255,))
        im.alpha_composite(s.b1, (int(-120 + 90 * math.sin(t * 0.7 + s.idx)), int(1000 + 70 * math.cos(t * 0.5))))
        im.alpha_composite(s.b2, (int(560 + 80 * math.cos(t * 0.6 + s.idx)), int(150 + 60 * math.sin(t * 0.8))))
        w2 = s.wm.rotate(-4 + 3 * math.sin(t * 0.5), resample=Image.BICUBIC); sc = 1 + 0.04 * (t / s.dur)
        w2 = w2.resize((int(900*sc), int(900*sc))); im.alpha_composite(w2, (W - 600, H - 1100))
        im.alpha_composite(s.hd, (0, 230 + int(30 * (1 - ease(t / 0.5)))) if t < 0.5 else (0, 230))
        if s.num:
            a = ease((t - 0.1) / 0.6); im.alpha_composite(Image.eval(s.num, lambda v: v) if a >= 1 else fade(s.num, a), (W - 440, 430 - int(30 * (1 - a))))
        if s.tag:
            a = ease((t - 0.25) / 0.45); im.alpha_composite(fade(s.tag, a), (85, 580 + int(40 * (1 - a))))
        for i, ln in enumerate(s.lines):
            a = ease((t - 0.4 - 0.22 * i) / 0.6); 
            if a > 0: im.alpha_composite(fade(ln, a), (0, s.top + i * s.lh + int(70 * (1 - a))))
        d = ImageDraw.Draw(im); y = 1560; d.rounded_rectangle((85, y, W - 85, y + 8), 4, fill=s.line + (255,))
        d.rounded_rectangle((85, y, 85 + int((W - 170) * min(g / TOTAL[0], 1)), y + 8), 4, fill=s.acc + (255,))
        return im.convert("RGB")
def fade(im, a):
    if a >= 1: return im
    im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * a))); return im
TOTAL = [1]
def build(slot):
    pal, slides = REELS[slot]; os.makedirs("tmp_reel", exist_ok=True)
    sc, starts, acc = [], [], 0.0
    for i, (tag, text, dur) in enumerate(slides, 1):
        d = 5.0 if tag == "Hook" else snap(dur); sc.append(Scene(i, len(slides), tag, text, d, (pal + i) % len(op.POOL))); starts.append(acc); acc += d
    TOTAL[0] = acc; cuts = starts[1:]
    wav = f"tmp_reel/{slot}.wav"; music.make(acc, cuts, wav, seed=int(slot[-2:]) if slot[-2:].isdigit() else 7)
    out = f"media/{slot}-reel.mp4"
    p = subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i",wav,
        "-c:v","libx264","-preset","medium","-crf","20","-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-movflags","+faststart","-t",str(acc),out], stdin=subprocess.PIPE)
    for n in range(int(acc * FPS)):
        g = n / FPS; i = max(k for k, s0 in enumerate(starts) if s0 <= g); t = g - starts[i]
        fr = sc[i].frame(t, g)
        if i > 0 and t < TR:
            prev = sc[i-1].frame(sc[i-1].dur, g); r = int(ease(t / TR) * 2300)
            m = Image.new("L", (W, H), 0); cx, cy = int(W * 0.85), int(H * 0.82)
            ImageDraw.Draw(m).ellipse((cx - r, cy - r, cx + r, cy + r), fill=255); fr = Image.composite(fr, prev, m)
        p.stdin.write(fr.tobytes())
    p.stdin.close(); p.wait(); print(out, round(acc, 1), "s", os.path.getsize(out) // 1024, "KB")
if __name__ == "__main__":
    import sys
    for s in (sys.argv[1:] or REELS): build(s)
