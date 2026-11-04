# cluster.py -- Week 8: start three copies of app.py and the load balancer in one go. Ctrl-C stops all four.
# Usage: python3 cluster.py [round_robin|least_connections]
import subprocess
import sys
import time

strategy = sys.argv[1] if len(sys.argv) > 1 else "round_robin"
procs = [subprocess.Popen([sys.executable, "app.py", str(port)]) for port in (5081, 5082, 5083)]
time.sleep(1.5)  # give the servers a moment to start listening
procs.append(subprocess.Popen([sys.executable, "balancer.py", strategy]))
print("cluster up: servers on 5081-5083, load balancer on 5008. Ctrl-C to stop.")
try:
    for p in procs:
        p.wait()
except KeyboardInterrupt:
    for p in procs:
        p.terminate()
