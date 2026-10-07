"""Weekly performance pull -> insights_log.csv (feeds the Weekly Tracker sheet)."""
import os, csv, datetime as dt
from common import api
IG = os.environ["IG_USER_ID"]
prof = api("GET", IG, {"fields": "username,followers_count,media_count"})
media = api("GET", f"{IG}/media", {"fields": "id,caption,media_type,permalink,timestamp,like_count,comments_count", "limit": 30})["data"]
rows = []
for m in media:
    try:
        ins = api("GET", f"{m['id']}/insights", {"metric": "reach,saved,shares"})["data"]
        v = {i["name"]: i["values"][0]["value"] for i in ins}
    except Exception:
        v = {}
    rows.append([dt.date.today().isoformat(), m["timestamp"][:10], m["media_type"], m["permalink"],
                 v.get("reach"), v.get("saved"), v.get("shares"), m.get("comments_count"), m.get("like_count")])
new = not os.path.exists("insights_log.csv")
with open("insights_log.csv", "a", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    if new: w.writerow(["pulled_on","posted_on","type","link","reach","saves","shares","comments","likes"])
    w.writerows(rows)
print(prof["username"], "followers:", prof["followers_count"], "posts:", prof["media_count"], "rows:", len(rows))
