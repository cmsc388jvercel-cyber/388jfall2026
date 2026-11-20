# origin_demo.py -- Week 11, Part 6: a connection from the wrong website is refused.
# Needs app.py running on port 5102.
import requests

url = "http://localhost:5102/socket.io/?EIO=4&transport=polling"

for label, origin in (
    ("our own page          ", "http://localhost:5102"),
    ("a page on evil.example", "http://evil.example"),
):
    r = requests.get(url, headers={"Origin": origin}, timeout=5)
    print(f"Origin: {origin:<24} ({label}) -> {r.status_code}")
