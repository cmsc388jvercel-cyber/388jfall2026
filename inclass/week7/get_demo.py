# get_demo.py -- Week 7, Part 3: GET the list, follow the links, ask for XML.
import requests

BASE = "http://localhost:5007"

# 1. GET the collection. Every part comes back with an href to itself.
response = requests.get(f"{BASE}/parts")
print(response.status_code, response.headers["Content-Type"])
parts = response.json()["parts"]
for part in parts:
    print("  ", part["id"], "->", part["href"])

# 2. Follow a link. We never built that URL ourselves; the server handed it to us.
first = requests.get(parts[0]["href"]).json()
print("\nfollowed the first link:", first)

# 3. The response carries a link onward, too.
print("link back to the list:", first["all_parts"])

# 4. Same resource, different representation: only the Accept header changed.
xml = requests.get(f"{BASE}/parts", headers={"Accept": "application/xml"})
print("\n", xml.headers["Content-Type"])
print(xml.text)
