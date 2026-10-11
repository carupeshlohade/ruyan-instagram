"""Daily follower log + weekly (Sunday) per-post insights. Writes followers_log.csv and insights_log.csv."""
import os, csv, datetime as dt
from common import api
IG = os.environ["IG_USER_ID"]; today = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
p = api("GET", IG, {"fields": "username,followers_count,follows_count,media_count"})
new = not os.path.exists("followers_log.csv")
with open("followers_log.csv", "a", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    if new: w.writerow(["date", "followers", "following", "posts"])
    w.writerow([today.date().isoformat(), p.get("followers_count"), p.get("follows_count"), p.get("media_count")])
print("followers", p.get("followers_count"))
if today.weekday() == 6 or os.environ.get("FULL") == "1":
    media = api("GET", f"{IG}/media", {"fields": "id,caption,media_type,media_product_type,permalink,timestamp,like_count,comments_count", "limit": 30})["data"]
    rows = []
    for m in media:
        v = {}
        for metric in ("reach,saved,shares,total_interactions", "reach,saved"):
            try:
                v = {i["name"]: i["values"][0]["value"] for i in api("GET", f"{m['id']}/insights", {"metric": metric})["data"]}; break
            except Exception: pass
        rows.append([today.date().isoformat(), m["timestamp"][:10], m.get("media_product_type") or m["media_type"], m["permalink"],
                     v.get("reach"), v.get("saved"), v.get("shares"), v.get("total_interactions"), m.get("comments_count"), m.get("like_count"),
                     (m.get("caption") or "").split("\n")[0][:80]])
    new = not os.path.exists("insights_log.csv")
    with open("insights_log.csv", "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new: w.writerow(["pulled_on", "posted_on", "type", "link", "reach", "saves", "shares", "interactions", "comments", "likes", "hook"])
        w.writerows(rows)
    print("insight rows", len(rows))
