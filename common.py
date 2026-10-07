import os, csv, json, urllib.request, urllib.parse, urllib.error

def load_env(path=".env"):
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

load_env()
GV = os.environ.get("GRAPH_VERSION", "v23.0")
BASE = f"https://graph.facebook.com/{GV}"

def api(method, path, params=None):
    params = dict(params or {})
    params["access_token"] = os.environ["IG_ACCESS_TOKEN"]
    data = urllib.parse.urlencode(params).encode()
    url = f"{BASE}/{path}"
    req = urllib.request.Request(url + ("?" + data.decode() if method == "GET" else ""),
                                 data=None if method == "GET" else data, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Graph API {e.code}: {e.read().decode()[:400]}")

QUEUE_FIELDS = ["id","date","time","format","media","caption","status","posted_media_id","posted_at","error"]

def read_queue(path="queue.csv"):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_queue(rows, path="queue.csv"):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=QUEUE_FIELDS); w.writeheader(); w.writerows(rows)
