# proxy.py -- Week 9: a tiny reverse proxy. It listens on 5009 and forwards each GET to the origin on 5091.
# Usage: python3 proxy.py          pass-through: forwards everything and remembers nothing (Part 1)
#        python3 proxy.py cache    caching: reuses replies for as long as Cache-Control: max-age allows (Part 5)
import re
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import requests

ORIGIN = "http://localhost:5091"
MODE = sys.argv[1] if len(sys.argv) > 1 else "pass"
cache = {}  # path -> {"status", "type", "body", "control", "expires"}


def max_age(cache_control):
    match = re.search(r"max-age=(\d+)", cache_control)
    return int(match.group(1)) if match else 0  # no max-age: do not keep it


class Proxy(BaseHTTPRequestHandler):
    def do_GET(self):
        if MODE == "cache":
            entry = cache.get(self.path)
            if entry and entry["expires"] > time.time():
                return self.reply(entry, "HIT")  # answered here: the origin never hears about this request

        try:
            # Forward the request, and say who really asked and that a proxy handled it.
            r = requests.get(ORIGIN + self.path, headers={
                "X-Forwarded-For": self.client_address[0],
                "Via": "1.1 week9-proxy",
            })
        except requests.RequestException:
            self.send_error(502, "origin down")
            return

        entry = {
            "status": r.status_code,
            "type": r.headers.get("Content-Type", "text/plain"),
            "body": r.content,
            "control": r.headers.get("Cache-Control", ""),
        }
        ttl = max_age(entry["control"])
        if MODE == "cache" and r.status_code == 200 and ttl > 0:
            entry["expires"] = time.time() + ttl
            cache[self.path] = entry  # remember it for next time
        self.reply(entry, "MISS" if MODE == "cache" else None)

    def reply(self, entry, x_cache):
        self.send_response(entry["status"])
        self.send_header("Content-Type", entry["type"])
        self.send_header("Content-Length", str(len(entry["body"])))
        if entry["control"]:
            self.send_header("Cache-Control", entry["control"])
        self.send_header("Via", "1.1 week9-proxy")
        if x_cache:
            self.send_header("X-Cache", x_cache)
        self.end_headers()
        self.wfile.write(entry["body"])

    def log_message(self, *args):  # keep the terminal quiet
        pass


if __name__ == "__main__":
    print(f"proxy on :5009 in '{MODE}' mode, origin {ORIGIN}")
    try:
        ThreadingHTTPServer(("localhost", 5009), Proxy).serve_forever()
    except KeyboardInterrupt:
        pass
