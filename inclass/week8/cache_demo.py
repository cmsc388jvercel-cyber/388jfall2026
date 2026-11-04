# cache_demo.py -- Week 8, Part 4: the cache-aside pattern with a time-to-live (TTL).
import time

database = {"movie:1": "Inception", "movie:2": "Arrival"}
cache = {}      # key -> (value, expires_at)
TTL = 2.0       # seconds before a cached value is thrown away
db_reads = 0


def slow_db_read(key):
    global db_reads
    db_reads += 1
    time.sleep(0.3)  # a pretend slow query
    return database[key]


def get(key):
    entry = cache.get(key)
    if entry is not None and entry[1] > time.time():
        return entry[0], "HIT"
    value = slow_db_read(key)                  # miss: ask the database...
    cache[key] = (value, time.time() + TTL)    # ...and remember the answer for next time
    return value, "MISS"


def timed(key):
    start = time.perf_counter()
    value, result = get(key)
    print(f"{key:8} {value:12} {result:5} {time.perf_counter() - start:.3f}s")


print("--- five reads of the same key ---")
for _ in range(5):
    timed("movie:1")

print("\n--- the data changes, but the cache does not know ---")
database["movie:1"] = "Interstellar"
timed("movie:1")  # still the old answer: stale

print("\n--- wait for the TTL to run out ---")
time.sleep(TTL)
timed("movie:1")  # expired, so we read the new value
print("database reads in total:", db_reads)
