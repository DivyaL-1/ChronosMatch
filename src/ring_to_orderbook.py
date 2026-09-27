import sys
sys.path.append(".")

from ringBuffer import RingBuffer
import order_book


from ringBuffer import RingBuffer
import order_book

ring = RingBuffer("orders.dat", create=False)
book = order_book.OrderBook("TEST")

records, current, lost = ring.read_new(0)

print("Orders read:", len(records))
print("Orders lost:", lost)

orders_with_fills = 0
total_fills = 0

for seq, order in records:
    fills = book.add_limit_order(
        order.order_id,
        order.price,
        order.quantity,
        order.side
    )

    if fills:
        orders_with_fills += 1
        total_fills += len(fills)

print("Orders processed:", len(records))
print("Orders with fills:", orders_with_fills)
print("Total fills:", total_fills)