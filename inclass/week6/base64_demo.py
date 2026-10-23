# base64_demo.py -- Week 6, Part 5: what a data: URI actually is.
# Runs on its own: python3 base64_demo.py
import base64

raw = b"\x89PNG\r\n\x1a\n"  # the first 8 bytes of every PNG file
encoded = base64.b64encode(raw)

print("raw bytes:   ", raw)
print("base64 bytes:", encoded)
print("as a string: ", encoded.decode("utf-8"))
print('<img src="data:image/png;base64,' + encoded.decode("utf-8") + '">')
