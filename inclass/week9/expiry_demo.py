# expiry_demo.py -- Week 9, Part 4: what happens when the data changes? Three ways to keep a cache honest.
import time

TTL = 2.0


def show(step, value, result):
    print(f"  {step:<22} {value:<26} {result}")


# 1. TTL: every entry expires on its own. Simple, but readers can see old data until then.
print("--- 1. TTL: expire after 2 seconds ---")
database = {"article": "v1"}
cache = {}  # key -> (value, expires_at)


def read_ttl(key):
    entry = cache.get(key)
    if entry and entry[1] > time.time():
        return entry[0], "HIT"
    cache[key] = (database[key], time.time() + TTL)
    return cache[key][0], "MISS"


show("read", *read_ttl("article"))
database["article"] = "v2"
show("edit -> v2, read", *read_ttl("article"))   # stale
time.sleep(TTL + 0.1)
show("after the TTL, read", *read_ttl("article"))

# 2. Coherent cache: whoever edits the data also tells the cache to forget it.
print("\n--- 2. Coherent: the writer invalidates ---")
database = {"article": "v1"}
cache = {}


def read_coherent(key):
    if key in cache:
        return cache[key], "HIT"
    cache[key] = database[key]
    return cache[key], "MISS"


def write_coherent(key, value):
    database[key] = value
    cache.pop(key, None)  # send the invalidation message


show("read", *read_coherent("article"))
write_coherent("article", "v2")
show("edit -> v2, read", *read_coherent("article"))  # fresh at once
show("read again", *read_coherent("article"))

# 3. Versioned data: never change a file, make a new one with a new name.
print("\n--- 3. Versioned: new data gets a new key ---")
database = {"article:v1": "first draft", "latest": 1}
cache = {}


def read_versioned():
    key = f"article:v{database['latest']}"
    if key in cache:
        return f"{key} = {cache[key]}", "HIT"
    cache[key] = database[key]
    return f"{key} = {cache[key]}", "MISS"


show("read", *read_versioned())
database["article:v2"] = "second draft"
database["latest"] = 2                               # point readers at the new name
show("edit -> v2, read", *read_versioned())
show("read again", *read_versioned())
print("  article:v1 is still in the cache, still correct:", "article:v1" in cache)
