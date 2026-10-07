"""Builds silent text-on-screen Reels (1080x1920 mp4) for approved reel slots."""
import os, subprocess, sys
from PIL import Image, ImageDraw
import build_posts as bp
import options as op
W, H = 1080, 1920
REELS = {
 "2026-10-08": (3, [("Hook", "Starting a business in Pune? Here is everything you will need help with in year one.", 4.5),
   ("Accounting", "Books that are ready when the bank or the tax department asks.", 3.5),
   ("GST", "Registration and monthly returns, filed on time.", 3.5),
   ("Income tax", "Returns and planning, for you and for your business.", 3.5),
   ("Loans and subsidy", "Project reports and documents for loan and subsidy applications.", 3.8),
   ("ROC and incorporation", "Company or LLP setup and annual filings.", 3.5),
   ("Investment planning", "General guidance on what to do with your surplus.", 3.5),
   ("Enquiries", "Ruyan Corporate Services, Pune. Message us or call 7020570215.", 4.5)]),
 "2026-10-11": (5, [("Hook", "Which business structure suits you? Three questions will tell you.", 4.0),
   ("Proprietorship", "One owner. Simple to start. The owner is personally liable for business debts.", 4.5),
   ("LLP", "Two or more partners. Liability is limited to the agreed contribution. Annual filings with the ROC.", 5.0),
   ("Private Limited", "A company. Limited liability. Can issue shares to investors. Highest compliance load.", 5.0),
   ("The three questions", "How much liability can you carry? How much compliance can you manage? Will you raise funds?", 5.5),
   ("Enquiries", "Not sure which fits? Message us or call 7020570215.", 4.0)]),
 "2026-10-13": (6, [("Hook", "Your business made a profit but the bank is empty. Here is why.", 4.0),
   ("Example", "You sell goods worth Rs 1,00,000 on credit this month.", 4.0),
   ("The result", "Your books show the profit. Your bank balance has not moved.", 4.0),
   ("Reason 1", "Customers have not paid yet.", 3.0),
   ("Reason 2", "Cash is tied up in stock you bought.", 3.0),
   ("Reason 3", "Loan repayments reduce cash, even though they are not an expense.", 4.0),
   ("The habit", "Read a monthly profit statement and a cash statement together.", 4.0),
   ("Enquiries", "Want help with this? Message us or call 7020570215.", 4.0)]),
}
def frame(tag, text, pal, n, total):
    bp.BG, bp.FG, bp.ACC, bp.MUT, bp.LINE = op.POOL[pal]
    im = Image.new("RGB", (W, H), bp.BG); d = ImageDraw.Draw(im)
    wm = Image.open("logo.png").split()[3].resize((900, 900), Image.LANCZOS).point(lambda v: int(v * 0.10))
    im.paste(Image.new("RGB", (900, 900), bp.FG), (W - 650, H - 1050), wm)
    lg = Image.open("logo.png").split()[3].resize((96, 96), Image.LANCZOS)
    im.paste(Image.new("RGB", (96, 96), bp.FG), (80, 230), lg)
    d.text((200, 278), "RUYAN CORPORATE SERVICES", font=bp.font("Bold", 28), fill=bp.FG, anchor="lm")
    if tag != "Hook": d.text((80, 520), tag.upper(), font=bp.font("Bold", 32), fill=bp.ACC)
    f, L, s = bp.fit(d, text, "Bold", W - 160, 760, 84 if tag == "Hook" else 66, 40)
    y = 600 if tag != "Hook" else 520
    for ln in L: d.text((80, y), ln, font=f, fill=bp.FG); y += int(s * 1.28)
    # progress dots
    for i in range(total):
        x = W // 2 - (total * 28) // 2 + i * 28
        d.ellipse((x, 1500, x + 14, 1514), fill=bp.ACC if i < n else bp.LINE)
    return im
def build(slot):
    pal, slides = REELS[slot]; os.makedirs("tmp_reel", exist_ok=True); clips = []
    for i, (tag, text, dur) in enumerate(slides, 1):
        p = f"tmp_reel/{slot}-{i}.png"; frame(tag, text, (pal + i) % len(op.POOL), i, len(slides)).save(p)
        c = f"tmp_reel/{slot}-{i}.mp4"
        subprocess.run(["ffmpeg","-y","-loglevel","error","-loop","1","-t",str(dur),"-i",p,"-f","lavfi","-t",str(dur),"-i","anullsrc=r=44100:cl=stereo",
          "-vf",f"fade=t=in:st=0:d=0.3,fade=t=out:st={dur-0.3}:d=0.3,format=yuv420p","-r","30","-c:v","libx264","-c:a","aac","-shortest",c],check=True)
        clips.append(c)
    lst = f"tmp_reel/{slot}.txt"; open(lst,"w").write("".join(f"file '{os.path.basename(c)}'\n" for c in clips))
    out = f"media/{slot}-reel.mp4"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",lst,"-c","copy",out],check=True)
    print(out, round(sum(s[2] for s in slides),1), "s", os.path.getsize(out)//1024, "KB")
if __name__ == "__main__":
    for s in REELS: build(s)
