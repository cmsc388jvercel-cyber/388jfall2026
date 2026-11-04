# lru_demo.py -- Week 9, Part 2: least recently used (LRU) eviction.
import time
from collections import OrderedDict
from functools import lru_cache


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = OrderedDict()  # oldest first, most recently used last

    def get(self, key):
        if key not in self.items:
            return None                  # miss
        self.items.move_to_end(key)      # we just used it, so it is now the newest
        return self.items[key]

    def put(self, key, value):
        self.items[key] = value
        self.items.move_to_end(key)
        if len(self.items) > self.capacity:
            evicted, _ = self.items.popitem(last=False)  # drop the oldest: the least recently used
            return evicted
        return None


cache = LRUCache(capacity=3)
print("--- a cache that holds 3 pages ---")
for page in ["A", "B", "C", "A", "D", "B", "A"]:
    if cache.get(page) is not None:
        result, evicted = "HIT ", None
    else:
        result, evicted = "MISS", cache.put(page, f"contents of {page}")
    note = f"evicted {evicted}" if evicted else ""
    print(f"request {page}  {result}  cache = {list(cache.items)}  {note}")

print("\n--- the same idea is built into Python ---")


@lru_cache(maxsize=2)
def slow_square(n):
    time.sleep(0.2)
    return n * n


for n in [3, 3, 4, 5, 3]:
    slow_square(n)
print(slow_square.cache_info())
