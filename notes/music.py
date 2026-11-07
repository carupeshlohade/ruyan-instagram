"""Very light background bed: soft pad + gentle plucked notes. usage: music.py mood seconds out.wav"""
import sys, numpy as np, soundfile as sf
mood, secs, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
SR = 44100
N = int(SR * secs)
t = np.arange(N) / SR
rng = np.random.default_rng(7)

def hz(m): return 440 * 2 ** ((m - 69) / 12)
# chord progressions (midi roots + triad type), bpm
MOODS = {
    'kini':    dict(bpm=78, prog=[(57, 'm'), (53, 'M'), (48, 'M'), (55, 'M')], arp=True),   # Am F C G - curious
    'siemens': dict(bpm=84, prog=[(50, 'M'), (57, 'M'), (59, 'm'), (55, 'M')], arp=True),   # D A Bm G - clean, hopeful
    'srh':     dict(bpm=96, prog=[(48, 'M'), (55, 'M'), (57, 'm'), (53, 'M')], arp=True),   # C G Am F - light
    'jav':     dict(bpm=66, prog=[(53, 'm'), (49, 'M'), (56, 'M'), (51, 'M')], arp=True),   # Fm Db Ab Eb - nostalgic
}
M = MOODS[mood]
beat = 60 / M['bpm']; bar = beat * 4
def triad(r, q): return [r, r + (3 if q == 'm' else 4), r + 7]

pad = np.zeros(N); pl = np.zeros(N)
nb = int(secs / bar) + 2
for b in range(nb):
    r, q = M['prog'][b % len(M['prog'])]
    notes = triad(r, q)
    s0 = int(b * bar * SR); s1 = min(N, int((b + 1) * bar * SR + 0.6 * SR))
    if s0 >= N: break
    tt = np.arange(s1 - s0) / SR
    env = np.minimum(1, tt / 0.8) * np.minimum(1, np.maximum(0, (bar + 0.6 - tt) / 0.9))
    for n in notes + [r - 12]:
        f = hz(n)
        w = (np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 1.003 * tt) + 0.25 * np.sin(2 * np.pi * f * 2 * tt))
        pad[s0:s1] += w * env * (0.6 if n == r - 12 else 0.35)
    # gentle pluck arpeggio (8th notes), soft, one octave up
    if M['arp']:
        seq = [notes[0] + 12, notes[1] + 12, notes[2] + 12, notes[1] + 12]
        for k in range(8):
            ps = int((b * bar + k * beat / 2) * SR)
            if ps >= N: break
            if rng.random() < 0.25: continue
            f = hz(seq[k % 4])
            L = min(N - ps, int(1.6 * SR)); tt = np.arange(L) / SR
            e = np.exp(-tt * 3.2) * np.minimum(1, tt / 0.004)
            w = np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * 2 * f * tt) * np.exp(-tt * 6) + 0.1 * np.sin(2 * np.pi * 3 * f * tt) * np.exp(-tt * 9)
            pl[ps:ps + L] += w * e * 0.22

# soften pad with simple one-pole lowpass
def lp(x, a):
    y = np.zeros_like(x); acc = 0.0
    for i in range(0, len(x), 1):
        acc += a * (x[i] - acc); y[i] = acc
    return y
pad = np.convolve(pad, np.ones(24) / 24, mode='same')
mix = pad * 0.5 + pl
# simple stereo + tiny reverb (feedback delays)
L = mix.copy(); R = mix.copy()
for d, g in [(0.083, 0.35), (0.127, 0.28), (0.191, 0.2)]:
    k = int(d * SR)
    L[k:] += g * mix[:-k]; R[int(k * 1.13):] += g * mix[:-int(k * 1.13)]
st = np.stack([L, R], 1)
fi, fo = int(1.5 * SR), int(2.2 * SR)
st[:fi] *= np.linspace(0, 1, fi)[:, None]
st[-fo:] *= np.linspace(1, 0, fo)[:, None]
st /= np.max(np.abs(st)) + 1e-9
sf.write(out, st * 0.8, SR)
print('ok', out)
