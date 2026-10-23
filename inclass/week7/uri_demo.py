# uri_demo.py -- Week 7, Part 6: a million URLs, zero files.
import os

import requests

BASE = "http://localhost:5007"

for number in (1, 345, 999_999):
    print(requests.get(f"{BASE}/catalog/{number}").json())

print("past the end:", requests.get(f"{BASE}/catalog/1000000").status_code)

# Is there a file or folder called catalog anywhere in this project? No. The URL is logical.
print("\nfiles next to app.py:", sorted(f for f in os.listdir(".") if not f.startswith(".")))
