"""Animated 9:16 Stories that point followers to the post: a same-day pre-teaser and a 'now live' teaser."""
import os, sys, json, subprocess
import reels2 as r2, music, options as op
from PIL import ImageDraw
CHOSEN = {'2026-10-08':'B','2026-10-09':'B','2026-10-10':'C','2026-10-11':'B','2026-10-12':'C','2026-10-13':'B','2026-10-14':'B'}
KIND = {"Reel": "New Reel", "Carousel": "New Carousel", "Static": "New Post"}
def build(slot, kind, tag, text, cta, pal, out):
    scenes = [(tag, text, 5.0), (cta[0], cta[1], 3.75)]
    r2.REELS["_s"] = (pal, scenes)
    # reuse engine, but drop the numbered watermark and the music beat count is fine
    orig = r2.Scene.__init__
    def init(self, *a, **k): orig(self, *a, **k); self.num = None
    r2.Scene.__init__ = init
    r2.build.__globals__["REELS"] = r2.REELS
    r2.build("_s"); r2.Scene.__init__ = orig
    os.replace("media/_s-reel.mp4", out)
if __name__ == "__main__":
    d = json.load(open("options.json")); only = sys.argv[1:]
    for slot, c in CHOSEN.items():
        if only and slot not in only: continue
        s = d[slot]; hook = s["options"][c]["hook"]; pal = int(slot[-2:]) % 8
        build(slot, "pre", f"Tonight 7:30 pm", hook, ("Stay tuned", "Follow us so you do not miss it."), pal, f"media/{slot}-story-pre.mp4")
        build(slot, "live", f"{KIND[s['format']]} is live", hook, ("See it now", "Tap our latest post on our profile."), (pal + 3) % 8, f"media/{slot}-story-live.mp4")
