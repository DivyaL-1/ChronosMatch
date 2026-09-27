import order_book

book = order_book.OrderBook("TEST")

print("Initial book:")
print("Best bid:", book.best_bid())
print("Best ask:", book.best_ask())
print("Spread:", book.spread())
print("Length:", len(book))

# Add a BUY order
fills = book.add_limit_order(1, 100.0, 10, 0)

print("\nAfter BUY order:")
print("Fills:", fills)
print("Best bid:", book.best_bid())
print("Best ask:", book.best_ask())
print("Spread:", book.spread())
print("Length:", len(book))

# Add a SELL order that crosses the BUY
fills = book.add_limit_order(2, 99.0, 5, 1)

print("\nAfter SELL order:")
print("Fills:", fills)
print("Best bid:", book.best_bid())
print("Best ask:", book.best_ask())
print("Spread:", book.spread())
print("Length:", len(book))
