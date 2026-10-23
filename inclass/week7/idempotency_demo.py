# idempotency_demo.py -- Week 7, Part 4: what happens when a client retries.
import requests

BASE = "http://localhost:5007"
AUTH = {"Authorization": "Bearer demo-token"}

# Start from a clean list of orders.
requests.delete(f"{BASE}/orders", headers=AUTH)

# 1. POST is NOT idempotent: send the same request twice and you get two orders.
print("--- POST /orders, twice ---")
order = {"part_id": "00345", "quantity": 5}
for attempt in (1, 2):
    r = requests.post(f"{BASE}/orders", json=order, headers=AUTH)
    print(f"attempt {attempt}: {r.status_code}  Location: {r.headers['Location']}")
print("orders on the server:", requests.get(f"{BASE}/orders", headers=AUTH).json()["count"])

# 2. PUT IS idempotent: same request twice, same state as sending it once.
print("\n--- PUT /parts/00345, twice ---")
new_part = {"name": "Hex bolt (zinc)", "price": 0.30}
for attempt in (1, 2):
    r = requests.put(f"{BASE}/parts/00345", json=new_part, headers=AUTH)
    print(f"attempt {attempt}: {r.status_code}  {r.json()['name']}  ${r.json()['price']:.2f}")

# 3. DELETE is idempotent too: the part is gone after the first call and stays gone.
print("\n--- DELETE /parts/00348, twice ---")
for attempt in (1, 2):
    r = requests.delete(f"{BASE}/parts/00348", headers=AUTH)
    print(f"attempt {attempt}: {r.status_code}")
print("is it still there?", requests.get(f"{BASE}/parts/00348").status_code)

# 4. Put the deleted part back with PUT, which can create a resource at a URL we choose.
r = requests.put(f"{BASE}/parts/00348", json={"name": "Lock washer", "price": 0.12}, headers=AUTH)
print("restored with PUT:", r.status_code)
