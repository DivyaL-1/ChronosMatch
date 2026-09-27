from ringBuffer import RingBuffer


ring = RingBuffer("orders.dat", create=False)

records, current, lost = ring.read_new(0)

print("Current sequence:", current)
print("Orders read:", len(records))
print("Orders lost:", lost)

print("\nLast 5 orders:")

for seq, order in records[-5:]:
    print(seq, order)

ring.close()
