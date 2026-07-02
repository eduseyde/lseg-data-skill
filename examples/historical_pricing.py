"""
Summary
-------
Retrieve historical OHLCV pricing from the LSEG Data Library with `get_history()`,
for a single instrument and for several instruments at once.

Logic
-----
1. Open an LSEG session.
2. Request clean daily OHLCV for one instrument by naming the five core price
   fields explicitly.
3. Request close and volume for several instruments (returns MultiIndex columns).
4. Print samples and close the session.

Usage
-----
    python examples/historical_pricing.py
"""

import lseg.data as ld

CORE_OHLCV = ["OPEN_PRC", "HIGH_1", "LOW_1", "TRDPRC_1", "ACVOL_UNS"]


def daily_ohlcv(ric: str, start: str, end: str):
    """Clean daily OHLCV for one instrument."""
    return ld.get_history(
        universe=ric, fields=CORE_OHLCV, start=start, end=end, interval="daily"
    )


def multi_close(rics: list[str], start: str, end: str):
    """Close price and volume for several instruments (MultiIndex columns)."""
    return ld.get_history(
        universe=rics,
        fields=["TRDPRC_1", "ACVOL_UNS"],
        start=start,
        end=end,
        interval="daily",
    )


def main() -> None:
    ld.open_session()
    try:
        print("Daily OHLCV for AAPL.O")
        print("=" * 60)
        print(daily_ohlcv("AAPL.O", "2024-01-01", "2024-03-31").head().to_string())

        print("\n\nClose + volume for AAPL.O, MSFT.O")
        print("=" * 60)
        print(multi_close(["AAPL.O", "MSFT.O"], "2024-01-01", "2024-03-31").head().to_string())
    finally:
        ld.close_session()


if __name__ == "__main__":
    main()
