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
