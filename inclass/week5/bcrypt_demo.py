# bcrypt_demo.py -- Week 5, Part 3: BCrypt in Flask
import time

from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

password = "hunter2"

# 1. Same password, two hashes: bcrypt picks a new random salt every time.
hash1 = bcrypt.generate_password_hash(password).decode("utf-8")
hash2 = bcrypt.generate_password_hash(password).decode("utf-8")
print(hash1)
print(hash2)
print("same string?", hash1 == hash2)

# 2. Checking still works, because the salt is stored inside the hash.
print("right password:", bcrypt.check_password_hash(hash1, "hunter2"))
print("wrong password:", bcrypt.check_password_hash(hash1, "hunter3"))

# 3. How slow is "slow"? Ten guesses, on purpose.
start = time.perf_counter()
for i in range(10):
    bcrypt.generate_password_hash(f"guess{i}")
elapsed = time.perf_counter() - start
print(f"10 bcrypt guesses took {elapsed:.2f} seconds")
