# stack.py -- Week 9: start the origin (app.py) and the proxy (proxy.py) together. Ctrl-C stops both.
# Usage: python3 stack.py [pass|cache]
import subprocess
import sys
import time

mode = sys.argv[1] if len(sys.argv) > 1 else "pass"
procs = [subprocess.Popen([sys.executable, "app.py"])]
time.sleep(1.5)  # give the origin a moment to start listening
procs.append(subprocess.Popen([sys.executable, "proxy.py", mode]))
print(f"stack up: origin on 5091, proxy on 5009 ({mode} mode). Ctrl-C to stop.")
try:
    for p in procs:
        p.wait()
except KeyboardInterrupt:
    for p in procs:
        p.terminate()
