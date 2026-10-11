"""Keyword comment -> DM. Watches posted lead posts (queue ids containing 'lead-<keyword>') for 7 days.
When a comment contains the keyword, sends one private reply (Instagram private replies API) with the
checklist link and a short public reply. Every handled comment is logged in dm_log.csv (never DMs twice).
Run:  python dm_keywords.py          (process)
      python dm_keywords.py --check  (print permission diagnostics only)"""
import os, sys, re, csv, json, random, datetime as dt
from common import api, read_queue

IG = os.environ.get("IG_USER_ID", "")
LINKS = json.load(open("checklist_links.json"))
NAMES = {"GST": "GST Registration Checklist", "ITR": "Income Tax Return Checklist", "ROC": "ROC Annual Compliance Checklist",
         "LOAN": "Business Loan Document Checklist", "SUBSIDY": "Subsidy Claim Checklist"}
DM = ("Hi! Here's your free {name}:\n{link}\n\n"
      "Any questions? Reply here or call/WhatsApp 7020570215.\n\n- Ruyan Corporate Services")
PUBLIC = ["Sent to your DM, check your inbox!", "Done! Check your DMs.", "Just sent it to your inbox.", "Check your DMs, it's there!"]
LOG = "dm_log.csv"; FIELDS = ["comment_id", "media_id", "keyword", "username", "comment", "dm", "public", "at", "error"]
IST = dt.timezone(dt.timedelta(hours=5, minutes=30))

def page_token():
    """Private replies go through the linked Facebook Page. Find it and its token."""
    pid, ptok = os.environ.get("PAGE_ID"), os.environ.get("PAGE_ACCESS_TOKEN")
    if pid and ptok: return pid, ptok
    r = api("GET", "me/accounts", {"fields": "id,name,access_token,instagram_business_account"})
    for p in r.get("data", []):
        if (p.get("instagram_business_account") or {}).get("id") == IG: return p["id"], p["access_token"]
    raise RuntimeError("linked Facebook Page not found in me/accounts")

def private_reply(comment_id, text):
    pid, ptok = page_token(); saved = os.environ["IG_ACCESS_TOKEN"]
    try:
        os.environ["IG_ACCESS_TOKEN"] = ptok
        return api("POST", f"{pid}/messages", {"recipient": json.dumps({"comment_id": comment_id}), "message": json.dumps({"text": text})})
    finally:
        os.environ["IG_ACCESS_TOKEN"] = saved

def check():
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): _check()
    out = buf.getvalue(); print(out); open("dm_check.txt", "w").write(out)

def _check():
    for path, params in (("me/permissions", {}), ("me/accounts", {"fields": "id,name,instagram_business_account,tasks"}),
                         (IG, {"fields": "username,followers_count"})):
        try:
            r = api("GET", path, params)
            if "data" in r: r = [{k: v for k, v in x.items() if k != "access_token"} for x in r["data"]]
            print(path, "->", json.dumps(r)[:1500])
        except Exception as e: print(path, "ERROR", e)
    try: print("page:", page_token()[0])
    except Exception as e: print("page ERROR", e)

def main():
    if "--check" in sys.argv: return check()
    done = {}
    if os.path.exists(LOG):
        for r in csv.DictReader(open(LOG, newline="", encoding="utf-8")): done[r["comment_id"]] = r
    me = api("GET", IG, {"fields": "username"}).get("username", "")
    now = dt.datetime.now(IST); new = []
    for row in read_queue():
        m = re.search(r"lead-([a-z]+)", row["id"])
        if not m or row["status"] != "posted" or not row["posted_media_id"]: continue
        kw = m.group(1).upper()
        if kw not in LINKS: continue
        try:
            if now - dt.datetime.fromisoformat(row["posted_at"]) > dt.timedelta(days=7): continue
        except Exception: pass
        res = api("GET", f"{row['posted_media_id']}/comments", {"fields": "id,text,username,timestamp", "limit": "100"})
        for c in res.get("data", []):
            if c["id"] in done or c.get("username") == me: continue
            if not re.search(rf"\b{kw}\b", c.get("text", ""), re.I): continue
            rec = dict(comment_id=c["id"], media_id=row["posted_media_id"], keyword=kw, username=c.get("username", ""),
                       comment=c.get("text", "")[:100], dm="", public="", at=now.isoformat(timespec="minutes"), error="")
            try: private_reply(c["id"], DM.format(name=NAMES[kw], link=LINKS[kw])); rec["dm"] = "sent"
            except Exception as e: rec["dm"] = "failed"; rec["error"] = str(e)[:250]
            if rec["dm"] == "sent":
                try: api("POST", f"{c['id']}/replies", {"message": random.choice(PUBLIC)}); rec["public"] = "sent"
                except Exception as e: rec["public"] = "failed"; rec["error"] = str(e)[:250]
            done[c["id"]] = rec; new.append(rec)
    if new:
        with open(LOG, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); w.writerows(done.values())
    print("handled:", len(new), [(r["username"], r["dm"]) for r in new])

if __name__ == "__main__": main()
