import asyncio

from order_generator import generate_orders
from ringBuffer import RingBuffer, Order, Side


async def main():
    ring = RingBuffer("orders.dat", capacity=1000, create=True)

    orders = await generate_orders(100_000)

    for order_data in orders:

        side = Side.BUY if order_data["side"] == "BUY" else Side.SELL

        order = Order(
            order_id=order_data["order_id"],
            price=order_data["price"],
            quantity=order_data["quantity"],
            side=side
        )

        ring.push(order)

    ring.flush()
    ring.close()

    print("All orders pushed into ring buffer.")


if __name__ == "__main__":
    asyncio.run(main())
