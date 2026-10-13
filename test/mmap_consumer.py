import argparse
import json
import time

from cpu_timing import cpu_time
from ringBuffer import RingBuffer


def wait_for_ring(path: str, timeout: float = 15.0) -> RingBuffer:
    deadline = time.time() + timeout
    while True:
        try:
            return RingBuffer(path, create=False)
        except (FileNotFoundError, ValueError):
            if time.time() > deadline:
                raise TimeoutError(f"no ring buffer at {path} after {timeout}s")
            time.sleep(0.005)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", required=True)
    ap.add_argument("--count", type=int, required=True)
    args = ap.parse_args()

    ring = wait_for_ring(args.path)

    cpu0 = cpu_time()
    wall0 = time.perf_counter()

    received = 0
    read_seq = 0
    total_lost = 0
    last_order = None
    while received < args.count:
        records, read_seq, lost = ring.read_new(read_seq)
        total_lost += lost
        received += len(records)
        if records:
            last_order = records[-1][1]
        else:
            time.sleep(0.0002)

    wall1 = time.perf_counter()
    cpu1 = cpu_time()
    ring.close()

    print(json.dumps({
        "role": "consumer",
        "channel": "mmap",
        "count": received,
        "lost": total_lost,
        "wall_seconds": wall1 - wall0,
        "cpu_seconds": cpu1 - cpu0,
        "last_order_id": last_order.order_id if last_order else None,
    }))


if __name__ == "__main__":
    main()
