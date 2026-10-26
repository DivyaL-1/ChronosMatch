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

Technology                                      Purpose

Python 3.12                                     Main implementation and orchestration

asyncio                                         Asynchronous market order generation

Cython                                          Optimized order-book processing

NumPy                                           Numerical and array operations where applicable

mmap                                            Shared memory and IPC

struct                                          Binary order representation

Flask                                           Browser-based dashboard

HTML and CSS                                    Dashboard layout and styling

SQLite                                          Trade persistence support

PowerShell                                      Windows development and execution

Git and GitHub                                  Version control and collaboration