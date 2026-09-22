import asyncio
import random


async def generate_orders(number_of_orders=10):
    for order_id in range(1, number_of_orders + 1):

        price = round(random.uniform(100, 200), 2)
        quantity = random.randint(1, 1000)
        side = random.choice(["BUY", "SELL"])

        print(
            f"Order ID: {order_id} | "
            f"Price: {price} | "
            f"Quantity: {quantity} | "
            f"Side: {side}"
        )

        await asyncio.sleep(0)


async def main():
    await generate_orders(10)


if __name__ == "__main__":
    asyncio.run(main())