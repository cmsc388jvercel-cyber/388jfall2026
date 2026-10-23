# hash_demo.py -- Week 5, Part 2: fast hashes and why they are not enough
import hashlib
import time

password = "hunter2"

# 1. A fast hash is deterministic: same input, same output, every time.
print("sha256:", hashlib.sha256(password.encode()).hexdigest())
print("sha256:", hashlib.sha256(password.encode()).hexdigest())

# 2. How fast is "fast"?
start = time.perf_counter()
for i in range(100_000):
    hashlib.sha256(f"guess{i}".encode()).hexdigest()
elapsed = time.perf_counter() - start
print(f"100,000 sha256 guesses took {elapsed:.3f} seconds")

# 3. A tiny rainbow table: precomputed hash -> password.
print("\n")
common_passwords = ["123456", "password", "qwerty", "letmein", "hunter2"]
table = {hashlib.sha256(p.encode()).hexdigest(): p for p in common_passwords}

stolen_hash = hashlib.sha256(password.encode()).hexdigest()
print("stolen hash:", stolen_hash)
print("cracked with one dictionary lookup:", table.get(stolen_hash))
