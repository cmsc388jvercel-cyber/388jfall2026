# shard_demo.py -- Week 8, Part 3: sharding with a hash, and what happens when you add a shard.
import hashlib
from collections import Counter


def h(key):
    # Python's built-in hash() changes every run for strings, so use md5 for a stable number.
    return int(hashlib.md5(key.encode()).hexdigest(), 16)


users = [f"user{i}" for i in range(1000)]

# 1. Pick the shard from the hash of the key. Same key, same shard, every time.
def shard_for(key, num_shards):
    return h(key) % num_shards


print("--- 1000 users on 3 shards ---")
print(sorted(Counter(shard_for(u, 3) for u in users).items()))
print("user42 lives on shard", shard_for("user42", 3))

# 2. Add a fourth shard. How many users now map somewhere else?
moved = sum(shard_for(u, 3) != shard_for(u, 4) for u in users)
print(f"\n--- add a 4th shard with hash % N ---\n{moved} of 1000 users moved ({moved / 10:.0f}%)")


# 3. Consistent hashing: put shards AND keys on the same ring, each key goes to the next shard clockwise.
def ring(shards, copies=100):
    points = sorted((h(f"{s}#{i}"), s) for s in shards for i in range(copies))
    return points


def ring_shard(key, points):
    k = h(key)
    for point, shard in points:
        if point >= k:
            return shard
    return points[0][1]  # wrapped around the ring


before, after = ring(["A", "B", "C"]), ring(["A", "B", "C", "D"])
moved = sum(ring_shard(u, before) != ring_shard(u, after) for u in users)
print(f"\n--- add a 4th shard with a hash ring ---\n{moved} of 1000 users moved ({moved / 10:.0f}%)")

# 4. Replication: every write goes to a primary and is copied to replicas.
print("\n--- replication ---")
primary, replicas = {}, [{}, {}]


def write(key, value):
    primary[key] = value
    for r in replicas:
        r[key] = value


write("user42", {"name": "Ada"})
print("primary has it:", "user42" in primary)
print("replica 1 has it:", "user42" in replicas[0])
primary.clear()  # the primary dies
print("primary dead, read from a replica:", replicas[0]["user42"])
