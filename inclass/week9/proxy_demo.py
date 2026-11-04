# proxy_demo.py -- Week 9, Part 1: what changes when a proxy sits in front of the origin.
# Needs: python3 stack.py   (pass-through mode)
import requests

ORIGIN = "http://localhost:5091"
PROXY = "http://localhost:5009"

print("--- straight to the origin (port 5091) ---")
print(requests.get(f"{ORIGIN}/").json())

print("\n--- through the proxy (port 5009) ---")
r = requests.get(f"{PROXY}/")
print(r.json())
print("Via header on the reply:", r.headers.get("Via"))

# On one laptop every address is 127.0.0.1, so remote_addr looks the same both times.
# In production remote_addr would be the PROXY's address and X-Forwarded-For would be the real user.
print("\nThe origin only knew a proxy was involved because the proxy told it.")
