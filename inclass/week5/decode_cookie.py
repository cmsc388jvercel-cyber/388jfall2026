# decode_cookie.py -- paste a Flask session cookie value to see what is inside it.
# Usage: python3 decode_cookie.py "<cookie value>"
import base64
import json
import sys
import zlib

value = sys.argv[1]
compressed = value.startswith(".")       # a leading dot means Flask compressed the data
payload = value.lstrip(".").split(".")[0]  # first chunk is the data; the rest is timestamp + signature
payload += "=" * (-len(payload) % 4)     # restore the base64 padding
data = base64.urlsafe_b64decode(payload)
if compressed:
    data = zlib.decompress(data)
print(json.loads(data))
