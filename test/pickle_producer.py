import argparse
import json
import os
import time
from multiprocessing.connection import Listener

from cpu_timing import cpu_time
from gen import make_orders
from ipc_address import is_removable_file


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--address", required=True)
    ap.add_argument("--count", type=int, required=True)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    if is_removable_file(args.address) and os.path.exists(args.address):
        os.remove(args.address)

    listener = Listener(args.address)  # family inferred from the address's shape
    conn = listener.accept()  # blocks until the consumer connects

    cpu0 = cpu_time()
    wall0 = time.perf_counter()

    for order_id, price, quantity, side in make_orders(args.count, args.seed):
        order = {"order_id": order_id, "price": price, "quantity": quantity, "side": side}
        conn.send(order)  # pickle.dumps() under the hood

    conn.send(None)  # end-of-stream sentinel

    wall1 = time.perf_counter()
    cpu1 = cpu_time()
    conn.close()
    listener.close()

    print(json.dumps({
        "role": "producer",
        "channel": "pickle",
        "count": args.count,
        "wall_seconds": wall1 - wall0,
        "cpu_seconds": cpu1 - cpu0,
    }))


if __name__ == "__main__":
    main()
