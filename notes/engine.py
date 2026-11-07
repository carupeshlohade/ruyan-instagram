"""Shared helpers for the graphic reels (no subtitles)."""
import re, subprocess, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance

W, H, FPS = 1080, 1920, 30
FD = '/home/claude/fonts/'
LOGO = '/home/claude/ruyan_automation/logo.png'
_fc = {}

def font(name, size, var=None):
    k = (name, size, var)
    if k not in _fc:
        f = ImageFont.truetype(FD + name, size, layout_engine=ImageFont.Layout.RAQM)
        if var:
            try: f.set_variation_by_name(var)
            except Exception: pass
        _fc[k] = f
    return _fc[k]

# ---------- easing ----------
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, t0, d): return clamp((t - t0) / d) if d > 0 else (1.0 if t >= t0 else 0.0)
def ease_out(p): return 1 - (1 - p) ** 3
def ease_io(p): return 3 * p * p - 2 * p * p * p
def back_out(p, s=1.7): p -= 1; return p * p * ((s + 1) * p + s) + 1

# ---------- timing from audio ----------
def sentences(lines):
    out = []
    for l in lines:
        for s in re.split(r'(?<=[।.?])\s+', l.strip()):
            if s.strip(): out.append(s.strip())
    return out

def sentence_times(audio, sents):
    dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', audio]))
    log = subprocess.run(['ffmpeg', '-i', audio, '-af', 'silencedetect=noise=-38dB:d=0.12', '-f', 'null', '-'], capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', log)]
    en = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', log)]
    gaps = list(zip(st, en))
    s0 = gaps[0][1] if gaps and gaps[0][0] < 0.05 else 0.0
    s1 = gaps[-1][0] if gaps and gaps[-1][1] > dur - 0.05 else dur
    inner = [g for g in gaps if g[0] > s0 + 0.1 and g[1] < s1 - 0.1]
    L = [len(s) for s in sents]; tot = sum(L); acc = 0; exp = []
    for x in L[:-1]:
        acc += x; exp.append(s0 + (s1 - s0) * acc / tot)
    chosen, used = [], set()
    for e in exp:
        best = None
        for i, g in enumerate(inner):
            if i in used or (chosen and g[0] <= chosen[-1][0]): continue
            sc = abs((g[0] + g[1]) / 2 - e) - 0.8 * (g[1] - g[0])
            if best is None or sc < best[0]: best = (sc, i)
        if best and abs((inner[best[1]][0] + inner[best[1]][1]) / 2 - e) < 3.0:
            used.add(best[1]); chosen.append(inner[best[1]])
        else:
            chosen.append((e, e))
    b = [s0] + [x for g in chosen for x in g] + [s1]
    return dur, [(b[2 * i], b[2 * i + 1]) for i in range(len(sents))]

# ---------- images ----------
_ic = {}
def load(path, w=W, h=H):
    k = (path, w, h)
    if k not in _ic:
        im = Image.open(path).convert('RGB')
        r = max(w / im.width, h / im.height) * 1.15
        im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
        _ic[k] = im
    return _ic[k]

def kb(path, p, w=W, h=H, z0=1.0, z1=1.12, dx=0, dy=0):
    """Ken Burns crop: p in 0..1"""
    big = load(path, w, h)
    base = max(w / big.width, h / big.height)
    z = (z0 + (z1 - z0) * p)
    s = base * 1.15 * z / 1.15
    cw, ch = w / (s / base * 1.0) , h / (s / base * 1.0)
    # crop window in big-image pixels
    scale = big.width / (w / base * 1.0) if False else 1.0
    cw = big.width / (z * 1.15 / 1.15) / (big.width / w * base / base) if False else None
    # simpler: scale big so that it covers w*z x h*z
    tw, th = int(w * z), int(h * z)
    r = max(tw / big.width, th / big.height)
    im = big.resize((max(tw, int(big.width * r)), max(th, int(big.height * r))), Image.BILINEAR)
    ox = (im.width - w) // 2 + int(dx * p); oy = (im.height - h) // 2 + int(dy * p)
    ox = int(clamp(ox, 0, im.width - w)); oy = int(clamp(oy, 0, im.height - h))
    return im.crop((ox, oy, ox + w, oy + h))

def sepia(im, amt):
    if amt <= 0: return im
    g = ImageOps.grayscale(im)
    sp = ImageOps.colorize(g, (40, 26, 12), (240, 214, 170))
    return Image.blend(im, sp, amt)

def grade(im, sat=1.0, bright=1.0, contrast=1.0):
    if sat != 1: im = ImageEnhance.Color(im).enhance(sat)
    if bright != 1: im = ImageEnhance.Brightness(im).enhance(bright)
    if contrast != 1: im = ImageEnhance.Contrast(im).enhance(contrast)
    return im

def rounded(im, r):
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), r, fill=255)
    out = Image.new('RGBA', im.size); out.paste(im, (0, 0), m); return out

_vig = {}
def vignette(strength=170):
    if strength not in _vig:
        m = Image.new('L', (W // 4, H // 4), 0); d = ImageDraw.Draw(m)
        for i in range(60):
            a = int(strength * (1 - i / 60) ** 2)
            d.rectangle((i * 2, i * 3, W // 4 - i * 2, H // 4 - i * 3), outline=a)
        _vig[strength] = m.resize((W, H), Image.BILINEAR).filter(ImageFilter.GaussianBlur(30))
    return _vig[strength]

def logo_badge(size=130, ring=(255, 255, 255)):
    lg = Image.open(LOGO).convert('RGBA').resize((size, size), Image.LANCZOS)
    b = Image.new('RGBA', (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.ellipse((0, 0, size - 1, size - 1), fill=ring + (240,))
    m = Image.new('L', (size, size), 0); ImageDraw.Draw(m).ellipse((0, 0, size - 1, size - 1), fill=255)
    b.paste(lg, (0, 0), Image.composite(lg.split()[3], Image.new('L', (size, size), 0), m))
    return b

# ---------- drawing ----------
def text_c(d, xy_center_y, txt, f, fill, W_=W, stroke=0, sf=(0, 0, 0), x0=0):
    tw = d.textlength(txt, font=f)
    d.text((x0 + (W_ - tw) / 2, xy_center_y), txt, font=f, fill=fill, stroke_width=stroke, stroke_fill=sf)
    return tw

def tick(d, x, y, s, col, w=8, p=1.0):
    pts = [(x, y + s * 0.5), (x + s * 0.38, y + s * 0.88), (x + s, y + s * 0.1)]
    if p <= 0: return
    l1 = 0.4
    if p < l1:
        q = p / l1; d.line([pts[0], (pts[0][0] + (pts[1][0] - pts[0][0]) * q, pts[0][1] + (pts[1][1] - pts[0][1]) * q)], fill=col, width=w)
    else:
        q = (p - l1) / (1 - l1)
        d.line([pts[0], pts[1], (pts[1][0] + (pts[2][0] - pts[1][0]) * q, pts[1][1] + (pts[2][1] - pts[1][1]) * q)], fill=col, width=w, joint='curve')

def cross(d, x, y, s, col, w=8):
    d.line([(x, y), (x + s, y + s)], fill=col, width=w); d.line([(x + s, y), (x, y + s)], fill=col, width=w)

def stamp(base, txt, f, col, center, angle, p, pad=(36, 18), border=8):
    """rubber-stamp slam: p 0..1"""
    if p <= 0: return base
    d0 = ImageDraw.Draw(base)
    tw = int(d0.textlength(txt, font=f)); asc, desc = f.getmetrics()
    w, h = tw + pad[0] * 2, asc + desc + pad[1] * 2
    s = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(s)
    d.rounded_rectangle((border // 2, border // 2, w - border // 2, h - border // 2), 14, outline=col + (255,), width=border)
    d.text((pad[0], pad[1]), txt, font=f, fill=col + (255,))
    sc = 1.8 - 0.8 * ease_out(clamp(p * 1.4))
    s = s.resize((max(1, int(w * sc)), max(1, int(h * sc))), Image.BILINEAR).rotate(angle, expand=True, resample=Image.BICUBIC)
    a = clamp(p * 3)
    if a < 1:
        al = s.split()[3].point(lambda v: int(v * a)); s.putalpha(al)
    base.paste(s, (int(center[0] - s.width / 2), int(center[1] - s.height / 2)), s)
    return base

def inr(n):
    s = str(int(n)); last = s[-3:]; rest = s[:-3]
    parts = []
    while len(rest) > 2: parts.insert(0, rest[-2:]); rest = rest[:-2]
    if rest: parts.insert(0, rest)
    return ','.join(parts + [last]) if parts else last

def render(path_out, audio, total, frame_fn, pad_audio=True):
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-i', audio, '-filter_complex', f'[1:a]apad=whole_dur={total:.2f},loudnorm=I=-14:TP=-1.5[a]', '-map', '0:v', '-map', '[a]',
                           '-c:v', 'libx264', '-preset', 'medium', '-crf', '21', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k',
                           '-t', f'{total:.2f}', '-movflags', '+faststart', path_out], stdin=subprocess.PIPE)
    N = int(total * FPS)
    for n in range(N):
        im = frame_fn(n / FPS)
        ff.stdin.write(im.convert('RGB').tobytes())
    ff.stdin.close(); ff.wait()

def scene_at(t, starts):
    k = 0
    for i, s in enumerate(starts):
        if t >= s: k = i
    return k
