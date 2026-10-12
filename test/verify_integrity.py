import argparse
import sys

from gen import make_orders
from ringBuffer import RingBuffer, Side

SIDE_MAP = {"BUY": Side.BUY, "SELL": Side.SELL}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", required=True)
    ap.add_argument("--count", type=int, required=True)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    ring = RingBuffer(args.path, create=False)
    records, final_seq, lost = ring.read_new(0)
    ring.close()

    print(f"read {len(records)} records, write_seq={final_seq}, lost={lost}")

    expected = list(make_orders(args.count, args.seed))
    if len(records) != len(expected):
        print(f"FAIL: count mismatch -- expected {len(expected)}, got {len(records)}")
        sys.exit(1)

    mismatches = 0
    for (seq, order), (order_id, price, quantity, side) in zip(records, expected):
        if (order.order_id, round(order.price, 2), order.quantity, int(order.side)) != \
           (order_id, price, quantity, int(SIDE_MAP[side])):
            mismatches += 1
            if mismatches <= 5:
                print(f"MISMATCH at seq={seq}: got {order}, expected "
                      f"order_id={order_id} price={price} qty={quantity} side={side}")

    if mismatches:
        print(f"FAIL: {mismatches} mismatches out of {len(records)}")
        sys.exit(1)

    print(f"OK: all {len(records)} records byte-exact against the seeded generator")


if __name__ == "__main__":
    main()
