
import argparse
import sqlite3
import time
from pathlib import Path

from trade_buffer import TradeBuffer


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BUFFER = ROOT / "trades.dat"
DEFAULT_DATABASE = ROOT / "trades.db"


def create_database(connection):
    connection.execute("""
        CREATE TABLE IF NOT EXISTS trades (
            sequence INTEGER PRIMARY KEY,
            maker_order_id INTEGER NOT NULL,
            taker_order_id INTEGER NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            aggressor_side INTEGER NOT NULL
        )
    """)
    connection.commit()


def save_trades(connection, records):
    rows = [
        (
            seq,
            trade.maker_order_id,
            trade.taker_order_id,
            trade.price,
            trade.quantity,
            trade.aggressor_side
        )
        for seq, trade in records
    ]

    connection.executemany("""
        INSERT OR IGNORE INTO trades (
            sequence,
            maker_order_id,
            taker_order_id,
            price,
            quantity,
            aggressor_side
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, rows)

    connection.commit()


def run_writer(buffer_path, database_path):
    print("Starting ChronosMatch background trade writer...")

    with sqlite3.connect(database_path) as connection:
        create_database(connection)

        # WAL mode allows readers during writes.
        connection.execute("PRAGMA journal_mode=WAL")

        cursor = connection.execute(
            "SELECT COALESCE(MAX(sequence), -1) FROM trades"
        )
        last_sequence = cursor.fetchone()[0]
        next_sequence = last_sequence + 1

        print(f"Resuming from sequence: {next_sequence}")

        buffer = TradeBuffer(str(buffer_path), create=False)

        try:
            while True:
                records, current, lost = buffer.read_new(next_sequence)

                if lost:
                    raise RuntimeError(
                        f"Trade buffer overflow: {lost} records lost. "
                        "Audit history may be incomplete."
                    )

                if records:
                    save_trades(connection, records)
                    next_sequence = current
                    print(
                        f"Saved {len(records)} trades. "
                        f"Next sequence: {next_sequence}"
                    )
                else:
                    time.sleep(0.01)

        except KeyboardInterrupt:
            print("\nStopping trade writer...")

        finally:
            buffer.close()
            print("Trade writer stopped.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--buffer",
        type=Path,
        default=DEFAULT_BUFFER
    )
    parser.add_argument(
        "--database",
        type=Path,
        default=DEFAULT_DATABASE
    )

    args = parser.parse_args()
    run_writer(args.buffer, args.database)

