
import mmap
import os
import struct
from dataclasses import dataclass


@dataclass
class Trade:
    maker_order_id: int
    taker_order_id: int
    price: float
    quantity: int
    aggressor_side: int


class TradeBuffer:
    MAGIC = b"TRAD"
    HEADER_FMT = "<4sIQQ"
    HEADER_SIZE = struct.calcsize(HEADER_FMT)

    RECORD_FMT = "<QQdQB7x"
    RECORD_SIZE = struct.calcsize(RECORD_FMT)
    SEQ_OFFSET = struct.calcsize("<4sIQ")

    def __init__(self, path, capacity=100_000, create=False):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")

        self.path = path

        if create:
            self.capacity = capacity
            size = self.HEADER_SIZE + capacity * self.RECORD_SIZE
            self.fd = os.open(
                path, os.O_RDWR | os.O_CREAT | os.O_TRUNC, 0o644
            )
            os.ftruncate(self.fd, size)
            self.mm = mmap.mmap(self.fd, size)
            struct.pack_into(
                self.HEADER_FMT, self.mm, 0,
                self.MAGIC, self.RECORD_SIZE, capacity, 0
            )
        else:
            self.fd = os.open(path, os.O_RDWR)
            try:
                header = os.read(self.fd, self.HEADER_SIZE)
                magic, record_size, capacity, _ = struct.unpack(
                    self.HEADER_FMT, header
                )
                if magic != self.MAGIC or record_size != self.RECORD_SIZE:
                    raise ValueError("Invalid trade buffer format")
                if capacity <= 0:
                    raise ValueError("Invalid capacity")

                self.capacity = capacity
                size = self.HEADER_SIZE + capacity * self.RECORD_SIZE
                self.mm = mmap.mmap(self.fd, size)
            except Exception:
                os.close(self.fd)
                raise

    @property
    def write_seq(self):
        return struct.unpack_from(
            "<Q", self.mm, self.SEQ_OFFSET
        )[0]

    def push(self, trade):
        seq = self.write_seq
        offset = self.HEADER_SIZE + (
            seq % self.capacity
        ) * self.RECORD_SIZE

        struct.pack_into(
            self.RECORD_FMT, self.mm, offset,
            trade.maker_order_id,
            trade.taker_order_id,
            trade.price,
            trade.quantity,
            trade.aggressor_side
        )
        struct.pack_into(
            "<Q", self.mm, self.SEQ_OFFSET, seq + 1
        )

    def read_new(self, from_seq):
        current = self.write_seq
        lost = 0

        if current - from_seq > self.capacity:
            lost = current - from_seq - self.capacity
            from_seq = current - self.capacity

        records = []
        for seq in range(from_seq, current):
            offset = self.HEADER_SIZE + (
                seq % self.capacity
            ) * self.RECORD_SIZE
            values = struct.unpack_from(
                self.RECORD_FMT, self.mm, offset
            )
            records.append((seq, Trade(*values)))

        return records, current, lost

    def flush(self):
        self.mm.flush()

    def close(self):
        self.mm.close()
        os.close(self.fd)

