import curses
import time


def dashboard(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)

    while True:
        stdscr.clear()

        # Mock order book data
        height, width = stdscr.getmaxyx()
        bids = [150.20, 150.10, 150.00]
        asks = [150.30, 150.40, 150.50]

        best_bid = bids[0]
        best_ask = asks[0]
        spread = best_ask - best_bid

        stdscr.addstr(1, 5, "========================================")
        stdscr.addstr(2, 5, "       CHRONOSMATCH - MARKET")
        stdscr.addstr(3, 5, "========================================")

        stdscr.addstr(5, 10, "ORDER BOOK")

        stdscr.addstr(7, 10, "BID")
        stdscr.addstr(7, 30, "ASK")

        stdscr.addstr(8, 10, "--------------------")
        stdscr.addstr(8, 30, "--------------------")

        for i in range(3):
            stdscr.addstr(9 + i, 10, f"{bids[i]:.2f}")
            stdscr.addstr(9 + i, 30, f"{asks[i]:.2f}")

        stdscr.addstr(14, 10, f"Best Bid: {best_bid:.2f}")
        stdscr.addstr(15, 10, f"Best Ask: {best_ask:.2f}")
        stdscr.addstr(16, 10, f"Spread:   {spread:.2f}")

        stdscr.addstr(18, 10, "----------------------------------------")
        stdscr.addstr(19, 10, "Status: LIVE")
        stdscr.addstr(20, 10, "Press Q to quit")

        stdscr.refresh()

        key = stdscr.getch()

        if key in (ord("q"), ord("Q")):
            break

        time.sleep(0.5)


if __name__ == "__main__":
    curses.wrapper(dashboard)