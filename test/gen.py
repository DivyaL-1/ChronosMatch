import random


def make_orders(n: int, seed: int = 42):
    rnd = random.Random(seed)
    for order_id in range(1, n + 1):
        price = round(rnd.uniform(100, 200), 2)
        quantity = rnd.randint(1, 1000)
        side = rnd.choice(["BUY", "SELL"])
        yield order_id, price, quantity, side
