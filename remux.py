"""Replace each video's audio with a post-specific music style (video stream untouched)."""
import subprocess, math, os, music
from reels import REELS
snap = lambda d: max(3.75, math.ceil(d / 1.25) * 1.25)
STYLES = {  # day -> (bpm, progression, bell, kick)
 "09": (96,  [[48,52,55,59],[45,48,52,55],[41,45,48,52],[43,47,50,53]], False, (0, 2)),
 "10": (112, [[43,47,50,54],[40,43,47,50],[48,52,55,59],[50,54,57,59]], False, (0, 1, 2, 3)),
 "11": (84,  [[50,53,57,60],[43,47,50,53],[48,52,55,62],[45,48,52,55]], False, (0, 2)),
 "12": (120, [[41,45,48,52],[50,53,57,60],[46,50,53,57],[48,52,55,57]], False, (0, 1, 2, 3)),
 "13": (76,  [[39,43,46,50],[48,51,55,58],[44,48,51,55],[46,50,53,55]], True,  (0,)),
 "14": (100, [[45,48,52,55],[41,45,48,52],[48,52,55,59],[43,47,50,55]], False, (0, 2)),
}
def durs(slot, kind):
    if kind == "reel": return [5.0 if t == "Hook" else snap(d) for t, _, d in REELS[slot][1]]
    return [5.0, 3.75]
for slot in ["2026-10-09","2026-10-10","2026-10-11","2026-10-12","2026-10-13","2026-10-14"]:
    bpm, prog, bell, kick = STYLES[slot[-2:]]
    for kind, f in (("reel", f"media/{slot}-reel.mp4"), ("story", f"media/{slot}-story-pre.mp4"), ("story", f"media/{slot}-story-live.mp4")):
        if not os.path.exists(f) or (kind == "reel" and slot not in REELS): continue
        ds = durs(slot, kind); tot = sum(ds); cuts = [sum(ds[:i]) for i in range(1, len(ds))]
        wav = f"tmp_reel/{os.path.basename(f)}.wav"; music.make(tot, cuts, wav, bpm=bpm, seed=int(slot[-2:]), prog=prog, bell=bell, kick=kick)
        tmp = f + ".tmp.mp4"
        subprocess.run(["ffmpeg","-y","-loglevel","error","-i",f,"-i",wav,"-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-b:a","160k","-shortest","-movflags","+faststart",tmp],check=True)
        os.replace(tmp, f); print("remuxed", f, bpm)
