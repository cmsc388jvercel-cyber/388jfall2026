# http_cache_demo.py -- Week 9, Part 5: the headers that control caching, and conditional requests.
# Needs: python3 app.py   (or python3 stack.py)
import requests

ORIGIN = "http://localhost:5091"

print("--- Cache-Control headers the origin sends ---")
for path in ["/clock", "/live", "/article", "/assets/v1/style.css"]:
    r = requests.get(ORIGIN + path)
    print(f"{path:<22} Cache-Control: {r.headers['Cache-Control']}")

print("\n--- a conditional request with ETag ---")
first = requests.get(f"{ORIGIN}/article")
etag = first.headers["ETag"]
print(f"first GET           {first.status_code}  ETag {etag}  body {len(first.content)} bytes")

again = requests.get(f"{ORIGIN}/article", headers={"If-None-Match": etag})
print(f"asking again        {again.status_code}  body {len(again.content)} bytes   (nothing changed)")

requests.post(f"{ORIGIN}/article", json={"text": "A thief steals ideas from dreams."})
changed = requests.get(f"{ORIGIN}/article", headers={"If-None-Match": etag})
print(f"after an edit       {changed.status_code}  ETag {changed.headers['ETag']}  body {len(changed.content)} bytes")
