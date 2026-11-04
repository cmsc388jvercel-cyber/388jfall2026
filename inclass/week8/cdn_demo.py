# cdn_demo.py -- Week 8, Part 6: edge servers that keep copies of static files near the user.
# Latencies are made-up round-trip times in milliseconds.
ORIGIN_MS = {"Maryland": 20, "London": 90, "Tokyo": 170}   # distance from each user to the one origin server
EDGE_MS = 10                                                # distance from a user to the nearest edge server

edge_cache = {city: set() for city in ORIGIN_MS}            # which files each edge server has stored


def fetch(city, path, use_cdn):
    if not use_cdn:
        return ORIGIN_MS[city], "origin"
    if path in edge_cache[city]:
        return EDGE_MS, "edge HIT"
    edge_cache[city].add(path)                              # miss: edge asks the origin, then keeps a copy
    return EDGE_MS + ORIGIN_MS[city], "edge MISS -> origin"


requests = [("Maryland", "/logo.png"), ("London", "/logo.png"), ("London", "/logo.png"),
            ("London", "/logo.png"), ("Tokyo", "/logo.png"), ("Tokyo", "/logo.png"), ("Tokyo", "/app.css")]

for use_cdn in (False, True):
    print(f"\n--- {'with' if use_cdn else 'without'} a CDN ---")
    total = 0
    for city, path in requests:
        ms, how = fetch(city, path, use_cdn)
        total += ms
        print(f"{city:9} {path:10} {ms:4} ms  {how}")
    print(f"total {total} ms")
