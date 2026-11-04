# longtail_demo.py -- Week 9, Part 3: why a small cache can absorb most of the traffic.
import random
from collections import OrderedDict

random.seed(388)
PAGES = 1000
REQUESTS = 100_000

# Page 1 is the most popular, page 1000 the least. Popularity falls off like 1/rank (a long tail).
weights = [1 / rank for rank in range(1, PAGES + 1)]
traffic = random.choices(range(1, PAGES + 1), weights=weights, k=REQUESTS)

print(f"--- {REQUESTS:,} requests spread over {PAGES} pages ---")
for top in (10, 100, 500):
    share = sum(1 for page in traffic if page <= top) / REQUESTS
    print(f"the {top:>3} most popular pages get {share:5.1%} of the traffic")


def hit_rate(size):
    cache, hits = OrderedDict(), 0
    for page in traffic:
        if page in cache:
            hits += 1
            cache.move_to_end(page)
        else:
            cache[page] = True
            if len(cache) > size:
                cache.popitem(last=False)  # LRU eviction
    return hits / REQUESTS


print("\n--- LRU cache hit rate by cache size ---")
for size in (1, 10, 50, 100, 250, 500):
    print(f"cache holds {size:>3} pages ({size / PAGES:5.1%} of all pages): hit rate {hit_rate(size):5.1%}")
