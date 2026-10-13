import argparse
import json
import time

from cpu_timing import cpu_time
from gen import make_orders
from ringBuffer import Order, RingBuffer, Side

SIDE_MAP = {"BUY": Side.BUY, "SELL": Side.SELL}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", required=True)
    ap.add_argument("--count", type=int, required=True)
    ap.add_argument("--capacity", type=int, required=True)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    ring = RingBuffer(args.path, capacity=args.capacity, create=True)

    cpu0 = cpu_time()
    wall0 = time.perf_counter()

    for order_id, price, quantity, side in make_orders(args.count, args.seed):
        ring.push(Order(order_id, price, quantity, SIDE_MAP[side]))

    ring.flush()
    wall1 = time.perf_counter()
    cpu1 = cpu_time()
    ring.close()

    print(json.dumps({
        "role": "producer",
        "channel": "mmap",
        "count": args.count,
        "wall_seconds": wall1 - wall0,
        "cpu_seconds": cpu1 - cpu0,
    }))


if __name__ == "__main__":
    main()
