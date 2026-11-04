# proxy_cache_demo.py -- Week 9, Part 5: a caching proxy honouring Cache-Control.
# Needs: python3 stack.py cache
import time

import requests

PROXY = "http://localhost:5009"
ORIGIN = "http://localhost:5091"

requests.get(f"{ORIGIN}/reset")  # start the "built" counters at zero (straight to the origin)


def get(path):
    start = time.perf_counter()
    r = requests.get(PROXY + path)
    took = time.perf_counter() - start
    return r.headers.get("X-Cache", "-"), took, r.json()


print("--- /slow: max-age=5 ---")
for _ in range(3):
    x_cache, took, _ = get("/slow")
    print(f"/slow   {x_cache:<5} {took:.3f}s")

print("\n--- /clock: max-age=5 (built = how often the origin really ran it) ---")
for _ in range(3):
    x_cache, _, body = get("/clock")
    print(f"/clock  {x_cache:<5} {body}")
time.sleep(5.1)
x_cache, _, body = get("/clock")
print(f"/clock  {x_cache:<5} {body}   <- after 5 seconds")

print("\n--- /live: no-store ---")
for _ in range(2):
    x_cache, _, body = get("/live")
    print(f"/live   {x_cache:<5} {body}")
