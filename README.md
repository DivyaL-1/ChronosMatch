ChronosMatch — Low-Latency Order Matching Engine

ChronosMatch is a low-latency order matching engine prototype built to explore high-performance order processing, inter-process communication (IPC), memory-mapped shared memory, and optimized order matching using Python and Cython.

The project combines an asynchronous market order generator, a memory-mapped ring buffer, a Cython-based order book, performance measurements, and a real-time dashboard.

Project Overview

ChronosMatch simulates a simplified financial market in which generated buy and sell orders are transferred between processes, processed by an order book, and matched according to price-time priority.

The project focuses on:

Efficient order generation and processing

Inter-process communication using memory-mapped shared memory

Order-book matching and trade generation

Latency and throughput measurement

IPC performance comparison

Market visualization through a dashboard

Architecture

        Async Market Firehose
                 |
                 v
       Generated Market Orders
                 |
                 v
       Memory-Mapped Ring Buffer
                 |
                 v
        Order Book Consumer
                 |
                 v
       Cython Matching Engine
                 |
          Price-Time Priority
                 |
                 v
          Trade Generation
                 |
        +--------+--------+
        |                 |
        v                 v
  Trade Buffer       SQLite Writer
        |                 |
        +--------+--------+
                 |
                 v
      Market Dashboard / Metrics

The exact data path depends on the script being executed. The separate IPC proof benchmark compares mmap and pickle-based IPC and does not run the Cython matching engine.

Technology Stack

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Core programming language |
| asyncio | Asynchronous order generation |
| Cython | Optimized order-book processing |
| NumPy | Numerical and array operations, where applicable |
| mmap | Memory-mapped shared memory for IPC |
| struct | Binary order data representation |
| Flask | Web-based dashboard |
| HTML | Dashboard structure |
| CSS | Dashboard styling |
| SQLite | Trade storage and persistence |
| Git | Version control |
| GitHub | Source code hosting and collaboration |
| PowerShell | Windows development and execution |


Main Components

1. Market Firehose

The market firehose generates synthetic market orders asynchronously.

Each order includes fields such as:

order_id — unique order identifier

price — order price

quantity — number of units

side — BUY or SELL

The generator can be benchmarked independently to measure order-generation performance.

2. Memory-Mapped Ring Buffer

The ring buffer transfers order data between processes through a memory-mapped file.

Its purpose is to reduce the overhead associated with repeatedly serializing and transferring Python objects between processes.

The implementation uses binary records and shared-memory access to support high-volume order delivery.

3. Cython Order Book

The order book processes incoming orders and matches compatible buy and sell orders.

The matching engine is implemented in Cython to reduce Python-level overhead in performance-sensitive operations.

The project explores price-time priority, where better-priced orders take precedence and orders at the same price are handled according to arrival order.

4. Trade Buffer and SQLite

The trade buffer provides storage for generated trade records. The project also includes SQLite-based trade-writing support.

Trade buffering and successful persistence to SQLite are separate concerns; the database record count should be verified independently when validating persistence.

5. Dashboard

The browser-based dashboard presents market information and engine metrics, including:

Bid and ask market depth

Best bid and best ask

Bid-ask spread

Order-book information

Latency and throughput metrics where supplied by the running engine

Market status and alert indicators

The dashboard is intended to make the matching engine's activity easier to inspect during demonstrations.

