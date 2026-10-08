"""Original warm lo-fi bed (no third-party music): chords + pluck arp + soft kick + shaker + whooshes on cuts."""
import numpy as np, wave
SR = 44100
def note(f): return 440.0 * 2 ** ((f - 69) / 12)
def make(total, cuts, path, bpm=96, seed=1, prog=None, bell=False, kick=(0, 2)):
    rng = np.random.default_rng(seed); n = int(total * SR); out = np.zeros(n)
    beat = 60 / bpm; t = np.arange(n) / SR
    prog = prog or [[48,52,55,59],[45,48,52,55],[41,45,48,52],[43,47,50,53]]
    bar = beat * 4
    for b in range(int(total / bar) + 1):
        ch = prog[b % 4]; s = int(b * bar * SR); L = int(bar * SR * 1.05)
        if s >= n: break
        tt = np.arange(min(L, n - s)) / SR
        env = np.minimum(tt / 0.35, 1) * np.exp(-tt / 3.2)
        pad = sum(np.sin(2*np.pi*note(m)*tt) + 0.5*np.sin(2*np.pi*note(m)*1.004*tt) + 0.25*np.sin(2*np.pi*note(m+12)*tt) for m in ch)
        out[s:s+len(tt)] += 0.05 * pad * env
        arp = [ch[0]+12, ch[1]+12, ch[2]+12, ch[3]+12, ch[2]+12, ch[1]+12, ch[3]+12, ch[2]+12]
        for k, m in enumerate(arp):
            a = int((b * bar + k * beat / 2) * SR)
            if a >= n: break
            tt2 = np.arange(min(int(0.6*SR), n - a)) / SR
            p = np.sin(2*np.pi*note(m)*tt2) + 0.3*np.sin(2*np.pi*note(m)*2*tt2) + (0.35*np.sin(2*np.pi*note(m)*2.76*tt2) if bell else 0)
            out[a:a+len(tt2)] += 0.07 * p * np.exp(-tt2 * (4 if bell else 7)) * np.minimum(tt2 / 0.004, 1)
        for k in kick:
            a = int((b * bar + k * beat) * SR)
            if a >= n: break
            tt3 = np.arange(min(int(0.35*SR), n - a)) / SR
            f = 45 + 70 * np.exp(-tt3 * 25); ph = 2*np.pi*np.cumsum(f) / SR
            out[a:a+len(tt3)] += 0.32 * np.sin(ph) * np.exp(-tt3 * 9)
        for k in range(8):  # shaker on off-beats, quiet
            if k % 2 == 0: continue
            a = int((b * bar + k * beat / 2) * SR)
            if a >= n: break
            m = min(int(0.08*SR), n - a); nz = rng.normal(size=m); nz = np.diff(nz, prepend=0)
            out[a:a+m] += 0.05 * nz * np.exp(-np.arange(m) / SR * 45)
    for c in cuts:  # whoosh at each transition
        a = int(max(c - 0.25, 0) * SR); m = min(int(0.6*SR), n - a)
        if m <= 0: continue
        tt4 = np.arange(m) / SR; nz = rng.normal(size=m)
        k = np.ones(40) / 40; lp = np.convolve(nz, k, 'same')
        out[a:a+m] += 0.5 * lp * np.sin(np.pi * tt4 / 0.6) ** 2
    d = int(0.2 * SR); dl = np.zeros(n); dl[d:] = out[:-d]; out = out + 0.3 * dl  # simple echo
    out *= np.minimum(t / 0.5, 1) * np.minimum((total - t) / 1.2, 1)
    out = np.tanh(out * 1.6) * 0.55
    st = np.stack([out, np.roll(out, 90)], 1)
    w = wave.open(path, "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(st, -1, 1) * 32767).astype("<i2").tobytes()); w.close()
