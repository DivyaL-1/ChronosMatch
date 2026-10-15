
import sys
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from ringBuffer import RingBuffer
import order_book

EXPECTED_ORDERS = 100_000


def main():
    ring = RingBuffer("orders.dat", create=False)
    book = order_book.OrderBook("TEST")

    current_seq = 0
    orders_processed = 0
    orders_with_fills = 0
    total_fills = 0
    total_lost = 0

    start = time.perf_counter()

    print("Starting ChronosMatch engine audit...")

    try:
        while orders_processed < EXPECTED_ORDERS:
            records, current, lost = ring.read_new(current_seq)
            total_lost += lost

            if records:
                for seq, order in records:
                    fills = book.add_limit_order(
                        order.order_id,
                        order.price,
                        order.quantity,
                        order.side
                    )

                    orders_processed += 1

                    if fills:
                        orders_with_fills += 1
                        total_fills += len(fills)

                current_seq = current

            else:
                time.sleep(0.01)

        elapsed = time.perf_counter() - start

        snapshot = {
            "best_bid": book.best_bid(),
            "best_ask": book.best_ask(),
            "spread": book.spread(),
            "depth": book.depth(5),
            "orders_processed": orders_processed,
            "orders_with_fills": orders_with_fills,
            "total_fills": total_fills,
            "orders_lost": total_lost,
            "elapsed_seconds": elapsed,
            "throughput_orders_per_sec": (
                orders_processed / elapsed if elapsed > 0 else 0
            )
        }

        with open("book_snapshot.json", "w") as f:
            json.dump(snapshot, f, indent=2)

        print("\n--- ChronosMatch Engine Audit ---")
        print(f"Expected orders:     {EXPECTED_ORDERS:,}")
        print(f"Orders processed:    {orders_processed:,}")
        print(f"Orders lost:         {total_lost:,}")
        print(f"Orders with fills:   {orders_with_fills:,}")
        print(f"Total fills:         {total_fills:,}")
        print(f"Elapsed seconds:     {elapsed:.4f}")
        print(f"Throughput:          {snapshot['throughput_orders_per_sec']:,.0f} orders/sec")
        print("Snapshot saved to book_snapshot.json")

        if orders_processed != EXPECTED_ORDERS or total_lost:
            print("AUDIT FAILED: order count mismatch or records lost.")
            sys.exit(1)

        print("AUDIT PASSED: all expected orders were processed.")

    finally:
        ring.close()


if __name__ == "__main__":
    main()
