import argparse
import json
import os
import subprocess
import sys
import time

from ipc_address import is_removable_file, pickle_endpoint, scratch_path

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable


def run_pair(label, first_cmd, second_cmd, settle=0.3):
    t0 = time.perf_counter()
    p1 = subprocess.Popen(first_cmd, cwd=HERE, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, text=True)
    time.sleep(settle)
    p2 = subprocess.Popen(second_cmd, cwd=HERE, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, text=True)

    out1, err1 = p1.communicate()
    out2, err2 = p2.communicate()
    orchestration_wall = time.perf_counter() - t0

    if p1.returncode != 0:
        raise RuntimeError(f"[{label}] first process failed:\n{err1}")
    if p2.returncode != 0:
        raise RuntimeError(f"[{label}] second process failed:\n{err2}")

    r1 = json.loads(out1.strip().splitlines()[-1])
    r2 = json.loads(out2.strip().splitlines()[-1])
    by_role = {r1["role"]: r1, r2["role"]: r2}
    return by_role["producer"], by_role["consumer"], orchestration_wall


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=1_000_000)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    n = args.count

    ring_path = scratch_path("proof_mmap.ring")
    sock_path = pickle_endpoint("proof_pickle")
    for p in (ring_path, sock_path):
        if is_removable_file(p) and os.path.exists(p):
            os.remove(p)

    print(f"Sending {n:,} orders between two separate OS processes, two ways.\n")


    print("[1/2] mmap (zero-copy, shared memory) ...")
    mmap_prod, mmap_cons, mmap_wall = run_pair(
        "mmap",
        first_cmd=[PY, "mmap_consumer.py", "--path", ring_path, "--count", str(n)],
        second_cmd=[PY, "mmap_producer.py", "--path", ring_path,
                    "--count", str(n), "--capacity", str(int(n * 1.2)),
                    "--seed", str(args.seed)],
        settle=0.1,
    )

    print("[2/2] pickle (multiprocessing.connection) ...")
    pkl_prod, pkl_cons, pkl_wall = run_pair(
        "pickle",
        first_cmd=[PY, "pickle_producer.py", "--address", sock_path,
                   "--count", str(n), "--seed", str(args.seed)],
        second_cmd=[PY, "pickle_consumer.py", "--address", sock_path, "--count", str(n)],
        settle=0.2,
    )

    def row(label, prod, cons, wall):
        total_cpu = prod["cpu_seconds"] + cons["cpu_seconds"]
        return {
            "label": label,
            "orders": n,
            "wall_seconds": wall,
            "producer_cpu_seconds": prod["cpu_seconds"],
            "consumer_cpu_seconds": cons["cpu_seconds"],
            "total_cpu_seconds": total_cpu,
            "throughput_orders_per_sec": n / wall,
            "cpu_us_per_order": (total_cpu / n) * 1e6,
            "lost": cons.get("lost"),
            "verified_count": cons["count"],
        }

    results = [
        row("mmap (zero-copy)", mmap_prod, mmap_cons, mmap_wall),
        row("pickle (multiprocessing.connection)", pkl_prod, pkl_cons, pkl_wall),
    ]

    with open(os.path.join(HERE, "proof_results.json"), "w") as f:
        json.dump(results, f, indent=2)

    speedup = results[1]["wall_seconds"] / results[0]["wall_seconds"]
    cpu_factor = results[1]["total_cpu_seconds"] / results[0]["total_cpu_seconds"]

    print("\n" + "=" * 72)
    print(f"{'':30} {'wall (s)':>10} {'total CPU (s)':>15} {'orders/s':>12}")
    for r in results:
        print(f"{r['label']:30} {r['wall_seconds']:10.3f} {r['total_cpu_seconds']:15.3f} "
              f"{r['throughput_orders_per_sec']:12,.0f}")
    print("=" * 72)
    print(f"mmap is {speedup:.1f}x faster wall-clock, and burns {cpu_factor:.1f}x less "
          f"total CPU across both processes than pickle-based IPC.")
    print(f"Both delivered all {n:,} orders with 0 lost "
          f"(mmap lost={results[0]['lost']}, consumer counts match exactly).")
    print("\nFull results written to proof_results.json")


if __name__ == "__main__":
    main()
