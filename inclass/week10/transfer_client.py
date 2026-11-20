# transfer_client.py -- Week 10, Part 5: drives the bank in app.py. Needs: python3 app.py running in another terminal.
import requests

BANK = "http://localhost:5101"


def balances():
    people = {a["name"]: a["balance"] for a in requests.get(f"{BANK}/accounts").json()}
    total = requests.get(f"{BANK}/total").json()["total"]
    return f"Alice={people['Alice']:<3} Bob={people['Bob']:<3} total={total}"


def post(path):
    r = requests.post(BANK + path)
    print(f"POST {path} -> {r.status_code} {r.json()}")


requests.post(f"{BANK}/reset")
print("start".ljust(30), balances())

post("/transfer/10")
print("after a good transfer".ljust(30), balances())

post("/transfer/25")
print("after one Alice cannot afford".ljust(30), balances())

post("/transfer/5?crash=1")
print("after crash (transaction)".ljust(30), balances())

post("/transfer_unsafe/5?crash=1")
print("after crash (NO transaction)".ljust(30), balances())
