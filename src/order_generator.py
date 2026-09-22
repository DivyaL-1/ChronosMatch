import asyncio
import random
import time


def create_order(order_id):
    price = round(random.uniform(100, 200), 2)
    quantity = random.randint(1, 1000)
    side = random.choice(["BUY", "SELL"])

    return {
        "order_id": order_id,
        "price": price,
        "quantity": quantity,
        "side": side
    }


async def generate_orders(number_of_orders=100_000):
    start_time = time.perf_counter()

    orders = []

    for order_id in range(1, number_of_orders + 1):
        order = create_order(order_id)
        orders.append(order)

        if order_id % 1000 == 0:
            await asyncio.sleep(0)

    end_time = time.perf_counter()

    elapsed_time = end_time - start_time
    orders_per_second = number_of_orders / elapsed_time

    print(f"Orders generated: {number_of_orders}")
    print(f"Time taken: {elapsed_time:.6f} seconds")
    print(f"Order rate: {orders_per_second:,.0f} orders/second")

    return orders


async def main():
    orders = await generate_orders(100_000)

    print("\nFirst 5 orders:")
    for order in orders[:5]:
        print(order)


if __name__ == "__main__":
    asyncio.run(main())