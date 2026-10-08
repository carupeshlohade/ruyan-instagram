"""Publishes approved, due rows of queue.csv to Instagram via the official Graph API.
Run every 15 min (GitHub Actions). Only rows with status == 'approved' are posted."""
import os, sys, time, datetime as dt
from common import api, read_queue, write_queue

IST = dt.timezone(dt.timedelta(hours=5, minutes=30))
DRY = "--dry-run" in sys.argv
IG = os.environ.get("IG_USER_ID", "")
BASEURL = os.environ.get("MEDIA_BASE_URL", "")

def wait_ready(cid, tries=30):
    for _ in range(tries):
        s = api("GET", cid, {"fields": "status_code,status"})
        if s.get("status_code") == "FINISHED": return
        if s.get("status_code") in ("ERROR", "EXPIRED"): raise RuntimeError(f"container {s}")
        time.sleep(10)
    raise RuntimeError("container not ready in time")

def publish(row):
    files = [m.strip() for m in row["media"].split(";") if m.strip()]
    urls = [BASEURL + f for f in files]
    cap, fmt = row["caption"], row["format"]
    if fmt == "Static":
        c = api("POST", f"{IG}/media", {"image_url": urls[0], "caption": cap})["id"]
    elif fmt == "Carousel":
        kids = [api("POST", f"{IG}/media", {"image_url": u, "is_carousel_item": "true"})["id"] for u in urls]
        c = api("POST", f"{IG}/media", {"media_type": "CAROUSEL", "children": ",".join(kids), "caption": cap})["id"]
    elif fmt == "Reel":
        c = api("POST", f"{IG}/media", {"media_type": "REELS", "video_url": urls[0], "caption": cap, "share_to_feed": "true"})["id"]
    elif fmt == "Story":
        key = "video_url" if urls[0].lower().endswith(".mp4") else "image_url"
        c = api("POST", f"{IG}/media", {"media_type": "STORIES", key: urls[0]})["id"]
    else:
        raise RuntimeError(f"unknown format {fmt}")
    wait_ready(c)
    return api("POST", f"{IG}/media_publish", {"creation_id": c})["id"]

def main():
    now = dt.datetime.now(IST)
    rows = read_queue(); changed = False; done = 0
    for r in rows:
        if r["status"] != "approved": continue
        due = dt.datetime.fromisoformat(f"{r['date']}T{r['time']}").replace(tzinfo=IST)
        if due > now: continue
        if (now - due) > dt.timedelta(hours=12):
            r["status"], r["error"] = "missed", "more than 12h late, not auto-posted"; changed = True; continue
        if done >= 1: break          # max one post per run
        if DRY: print("DRY:", r["id"], r["format"], r["media"]); continue
        try:
            r["posted_media_id"] = publish(r); r["status"] = "posted"
            r["posted_at"] = now.isoformat(timespec="minutes"); r["error"] = ""; done += 1
        except Exception as e:
            r["status"], r["error"] = "failed", str(e)[:300]
        changed = True
    if changed and not DRY: write_queue(rows)
    print("posted:", done)

if __name__ == "__main__": main()
