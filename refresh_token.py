"""Exchange a short-lived user token for a ~60-day token, or refresh an existing long-lived one.
Usage: python refresh_token.py   (reads IG_ACCESS_TOKEN, FB_APP_ID, FB_APP_SECRET from .env)
Prints only expiry info; writes the new token back to .env so it never appears on screen."""
import os, re
from common import api
r = api("GET", "oauth/access_token", {"grant_type": "fb_exchange_token", "client_id": os.environ["FB_APP_ID"],
        "client_secret": os.environ["FB_APP_SECRET"], "fb_exchange_token": os.environ["IG_ACCESS_TOKEN"]})
txt = open(".env", encoding="utf-8").read()
txt = re.sub(r"^IG_ACCESS_TOKEN=.*$", "IG_ACCESS_TOKEN=" + r["access_token"], txt, flags=re.M)
open(".env", "w", encoding="utf-8").write(txt)
print("Token renewed. expires_in seconds:", r.get("expires_in"), "(update the GitHub secret too)")
