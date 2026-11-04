# lb_sim.py -- Week 8, Part 2: round robin vs least connections, no network needed.
# Twelve requests arrive one per tick. Most are quick (1 tick) but some are slow (6 ticks).
import itertools

durations = [1, 6, 1, 1, 6, 1, 1, 1, 6, 1, 1, 1]
SERVERS = 3


def simulate(strategy):
    busy_until = [0] * SERVERS          # tick when each server finishes its current work
    queue_len = [0] * SERVERS           # requests assigned to each server in total
    waits = []
    rotation = itertools.cycle(range(SERVERS))
    for tick, work in enumerate(durations):
        if strategy == "round_robin":
            s = next(rotation)
        else:  # least connections: pick the server that is free soonest
            s = min(range(SERVERS), key=lambda i: busy_until[i])
        start = max(tick, busy_until[s])
        waits.append(start - tick)       # how long this request waited before anyone worked on it
        busy_until[s] = start + work
        queue_len[s] += 1
    return waits, queue_len


for strategy in ("round_robin", "least_connections"):
    waits, counts = simulate(strategy)
    print(f"{strategy:18} requests per server {counts}   longest wait {max(waits)} ticks   average wait {sum(waits) / len(waits):.2f}")
