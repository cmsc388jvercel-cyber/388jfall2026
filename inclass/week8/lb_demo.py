# lb_demo.py -- Week 8, Part 2: talk to the three servers through the load balancer on port 5008.
import collections

import requests

LB = "http://localhost:5008"

# 1. Nine requests to one URL. Who answers?
print("--- 9 requests to the load balancer ---")
tally = collections.Counter()
for _ in range(9):
    who = requests.get(f"{LB}/").json()["served_by"]
    tally[who] += 1
    print(who)
print(dict(tally))

# 2. STATEFUL: the counter lives in each server's memory, so the count jumps around.
print("\n--- /counter, 6 requests (server memory) ---")
for _ in range(6):
    print(requests.get(f"{LB}/counter").json())

# 3. STATELESS: the count rides in the cookie, so every server agrees. Session keeps the cookie between requests.
print("\n--- /visit, 6 requests with a cookie (client holds the state) ---")
with requests.Session() as client:
    for _ in range(6):
        print(client.get(f"{LB}/visit").json())
