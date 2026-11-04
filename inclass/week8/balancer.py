# balancer.py -- Week 8: a tiny load balancer. It listens on 5008 and forwards each GET to one backend.
# Usage: python3 balancer.py round_robin      (default)
#        python3 balancer.py least_connections
import itertools
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import requests

BACKENDS = ["http://localhost:5081", "http://localhost:5082", "http://localhost:5083"]
STRATEGY = sys.argv[1] if len(sys.argv) > 1 else "round_robin"

lock = threading.Lock()
rotation = itertools.cycle(BACKENDS)
active = {b: 0 for b in BACKENDS}  # how many requests each backend is working on right now


def choose():
    with lock:
        if STRATEGY == "least_connections":
            backend = min(BACKENDS, key=lambda b: active[b])
        else:
            backend = next(rotation)
        active[backend] += 1
        return backend


class Balancer(BaseHTTPRequestHandler):
    def do_GET(self):
        backend = choose()
        try:
            # Forward the request, cookies included, then hand the reply back unchanged.
            reply = requests.get(backend + self.path, headers={"Cookie": self.headers.get("Cookie", "")})
            self.send_response(reply.status_code)
            self.send_header("Content-Type", reply.headers.get("Content-Type", "text/plain"))
            if "Set-Cookie" in reply.headers:
                self.send_header("Set-Cookie", reply.headers["Set-Cookie"])
            self.end_headers()
            self.wfile.write(reply.content)
        except requests.RequestException:
            self.send_error(502, "backend down")
        finally:
            with lock:
                active[backend] -= 1

    def log_message(self, *args):  # keep the terminal quiet
        pass


if __name__ == "__main__":
    print(f"load balancer on :5008 using {STRATEGY}, backends {BACKENDS}")
    try:
        ThreadingHTTPServer(("localhost", 5008), Balancer).serve_forever()
    except KeyboardInterrupt:
        pass  # Ctrl-C: stop quietly instead of printing a traceback
