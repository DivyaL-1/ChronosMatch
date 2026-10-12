import argparse
import json
import time
from multiprocessing.connection import Client

from cpu_timing import cpu_time


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--address", required=True)
    ap.add_argument("--count", type=int, required=True)
    args = ap.parse_args()

    conn = None
    deadline = time.time() + 15.0
    while conn is None:
        try:
            conn = Client(args.address)  # family inferred from the address's shape
        except OSError:
            if time.time() > deadline:
                raise TimeoutError("producer listener never came up")
            time.sleep(0.01)

    cpu0 = cpu_time()
    wall0 = time.perf_counter()

    received = 0
    last_order = None
    while True:
        obj = conn.recv()  # pickle.loads() under the hood
        if obj is None:
            break
        received += 1
        last_order = obj

    wall1 = time.perf_counter()
    cpu1 = cpu_time()
    conn.close()

    print(json.dumps({
        "role": "consumer",
        "channel": "pickle",
        "count": received,
        "wall_seconds": wall1 - wall0,
        "cpu_seconds": cpu1 - cpu0,
        "last_order_id": last_order["order_id"] if last_order else None,
    }))


if __name__ == "__main__":
    main()
