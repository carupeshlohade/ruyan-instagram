# Ruyan Instagram: working rules (rebuilt 06-Nov-2026 after the cloud workspace was reset)

Brand: Ruyan Corporate Services (consultancy, NOT shown as a CA firm). @ruyan_corporate_services · 7020570215 · www.ruyangroup.org · contact.ruyan@gmail.com
Branches: Pune · Mumbai · Chhatrapati Sambhajinagar · Dhule

## MASTER STRATEGY (user 1 Nov: "This is the strategy for everything we do")
Real relatable owner problem first → only a HINT that Ruyan can solve it (never the full fix) → reason to contact (Comment KEYWORD / DM / call). Goal: attract clients.
- Relatable/brand reels: no "Comment" needed; CTA = "Call 7020570215 and hire us so you can focus on your business and family".
- Pick the MOST relatable case (shopkeeper / everyday owner pain) and lead with it.

## FORMAT ROTATION (user 5 Nov: "Dont copy same style for post. Everytime it should be new.")
Viral reference: instagram.com/p/DepPeSVHZ7g (yoursocialteam).
Used: traveling icon (cash), swipe to reveal (UPI), fake client on blast (accountant reel), swipe to zoom (MSME), follow the line (GST registration 9 Nov), newspaper front page, food receipt + stamp, red-pen notice, desk calendar.
Unused: walking through slides, hold the dots & slide.

## DASHBOARD AUTO-ACTION (user 2 Nov)
Ruyan Approvals https://claude.ai/artifact/XrHSMDUz87RCDDdSViavD2 (ArtifactData: items, decisions/<id>). Act on Approve / Reject / note automatically. A note with no choice counts as a decision. Chained check every 2 h; no checks 00:30–08:00 IST (next at 08:15). For revisions, use new media filenames and bump rev.

## POSTING
- Queue: GitHub carupeshlohade/ruyan-instagram queue.csv (id,date,time,format,media,caption,status,posted_media_id,posted_at,error,ai). DictWriter lineterminator '\r\n'. status=approved posts via publish.yml every 15 min (may be late; manual Run workflow if needed). Formats: Static, Carousel (media ;-separated), Reel, Story.
- Uploads only via Chrome on github.com upload pages (media → /upload/main/media, queue.csv → /upload/main), ≤10 MB per call, JS-wait until no "Uploading N of M" before Commit, verify md5 against origin/main, check queue diff before uploading queue.csv. No direct git push. Close the tabs Claude opens. If a browser dialog appears, stop and ask the user to click OK.
- AUTO STORIES (user 6 Nov 09:04): "U can post... Story without music is ok. You can keep posting and uploading automatically." Every feed post gets a Story row 10 min after it (batch2/story_from_post.py). The user may still add music himself.
- Captions: source line; disclaimer "General information based on ...; not legal advice. For any query or consultation, contact us on 7020570215 or visit www.ruyangroup.org"; closing "Share with your Friends and Follow us for more such updates."; 3 hashtags. No em dashes.
- AI-image reels: ai=yes.
- Voice: all numbers, dates and form names spoken in English. ElevenLabs v4, stability 0.15, whispered CTA with the [whispers] tag. The key lived in /home/claude/.secrets/elevenlabs_key; it was LOST in the reset and the user must paste it again. Never store it in memory.
- Music: gentle piano + pad, NO sound effects (the lo-fi beat and SFX were rejected). The piano_bed.py generator was lost in the reset and must be rebuilt (Am-F-C-G, 72 bpm, piano + pad, echo, ducking under the whisper).
- Instagram commenting on other creators' posts: STOPPED (28 Oct).

## FESTIVALS (user 6 Nov: posts were missed)
Check the festival calendar daily. The user posts festival posts himself with music; Claude sends post + story + caption with hashtags on the morning of each festival. Each festival needs a new layout with name, branches, phone and website.
Scheduled 07:30 IST: Diwali 8 Nov, Padwa 10 Nov, Bhai Dooj 11 Nov (files in batch2/fest/, rebuilt 6 Nov; backup in repo notes/fest/). Next to verify: Guru Nanak Jayanti / Dev Deepawali (~24 Nov), Christmas, New Year.

## PENDING
- Shop-interior and LLP-capital reels: scripts approved, waiting for the user's 4 photos each. The voice mp3s were lost in the reset and need re-voicing (requires the key).
- MSME swipe-to-zoom v2 (lavender): on the dashboard awaiting approval, proposed Tue 10 Nov 11:00.
- Loan-file X-ray reel idea: no reply yet.
- Phone Link highlights: swap the Nov due-dates card, the ROC LLP card, re-bump Ask Us. Waiting for the user's "ready".
- Case pool numbering 189–203 (picked: 189, 190, 193/164, 194, 195, 198, 199). The full case_pool.md was lost.

## Idea log (rebuilt; older entries from memory of the session)
- Lock-screen panic: APPROVED (reel queued 9 Nov). Sunday reel: APPROVED. Accountant on blast: APPROVED 05-Nov. Bill X-ray, Red flags, Truck, Widow, PMEGP, Penalty, Brand, Payment: made earlier.
- 05-Nov Loan file X-ray: discussed, no reply.
- 06-Nov "Same GST notice, 3 owners" (multi-character debate trend; Panicker / Ignorer / Calm one; Comment NOTICE; option A animated / B acted): discussed.
- 06-Nov 16:28 user: "Dhanteras still not posted" → festival greetings are now POSTED BY CLAUDE via the queue (post 08:00 + story 08:10 on the day) unless the user says he will post one himself. Queued: Dhanteras 6 Nov 16:40, Diwali 8, Padwa 10, Bhai Dooj 11.

## 07-Nov user decisions
- Daily case round: PERMANENT ("regular and not to be stopped"); chained send_later 07:46 IST daily.
- Picked case 2 (Mohan Clothing refund) → hold-the-dots carousel (batch2/dots_refund.py) queued Sat 14 Nov 11:00 + story. "hold the dots" now USED; only "walking through slides" left unused.
- Trader reel (ET/Taxscan ITAT Cuttack Rs 21.6 lakh speculative loss, s.271B, Ratan Kumar Kejriwal AY 2013-14) — series/reel_trader.py, text + music.py 'kini' bed, no VO (key lost) → queued Wed 11 Nov 19:30 + story. Comment TRADE.
- User asked for a reach/growth strategy. Insights (62 posts): followers flat ~621-624; median reach reels 76, feed 23; late Oct median halved; best = practical how-to & timely deadlines; worst = court stories & festival wishes. Proposed: 1 feed post/day, 40/25/20/15 mix, face reels 2/wk, share CTAs, trial reels, collabs, boost Rs 300-500/day, auto-DM checks, Monday review. Awaiting his yes/no on 4 points.
- 07-Nov 10:29 user: ONE FEED POST PER DAY (queue re-planned to 2 Dec; 16/23/30 Nov kept free for his face reels, which start 16 Nov). No interactive/daily stories until organic engagement exists (likes/shares currently mostly from his and staff accounts); auto "new post" stories stay. Paid promotion from DECEMBER. Case slots Tue/Fri 11:00; newly picked cases take the next Tue/Fri slot and push older case carousels later. Padwa & Bhai Dooj = story only; delivery-5% news dropped.
- ElevenLabs key was lost when the cloud workspace was replaced (it lived only in /home/claude/.secrets by design); user must paste again. Settings: eleven_v4, stability 0.15, voices Niraj (Calm Intense News Anchor) / Monika Sogam (Calm and Natural), [whispers] CTA.
