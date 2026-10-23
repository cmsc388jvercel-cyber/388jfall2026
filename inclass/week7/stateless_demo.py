# stateless_demo.py -- Week 7, Part 5: every request has to carry everything the server needs.
import requests

BASE = "http://localhost:5007"
order = {"part_id": "00346", "quantity": 2}

# 1. The server does not remember us. No Authorization header, no order.
r = requests.post(f"{BASE}/orders", json=order)
print("no token:      ", r.status_code, r.json())

# 2. Send the token with the request and it works. Send it with EVERY request.
r = requests.post(f"{BASE}/orders", json=order, headers={"Authorization": "Bearer demo-token"})
print("with token:    ", r.status_code, r.json())

# 3. The next request is a stranger again unless it brings the token too.
r = requests.get(f"{BASE}/orders")
print("token forgotten:", r.status_code, r.json())

# 4. The opposite design: /visit remembers us, but only because a cookie comes back each time.
print("\n--- /visit, three separate requests (no cookie kept) ---")
for _ in range(3):
    print(requests.get(f"{BASE}/visit").json())

print("--- /visit, three requests with a Session (cookie kept) ---")
with requests.Session() as client:
    for _ in range(3):
        print(client.get(f"{BASE}/visit").json())
