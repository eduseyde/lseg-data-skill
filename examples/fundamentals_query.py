"""
Summary
-------
Retrieve multi-period company fundamentals and a valuation snapshot from the LSEG
Data Library, using field codes validated against the live API.

Logic
-----
1. Open an LSEG session.
2. Pull several years of annual fundamentals via a Period range (`FY-N:FY0`),
   including the `.fperiod` companion so each row is labelled.
3. Pull a current valuation snapshot (enterprise value, EV/EBITDA, market cap).
4. Print samples and close the session.

Usage
-----
    python examples/fundamentals_query.py
"""

import lseg.data as ld
import pandas as pd


def get_annual_fundamentals(tickers: list[str], years: int = 5) -> pd.DataFrame:
    """Annual revenue, EBITDA, and net income for the last `years` fiscal years."""
    return ld.get_data(
        universe=tickers,
        fields=[
            "TR.CommonName",
            "TR.Revenue",
            "TR.EBITDA",
            "TR.NetIncome",
            "TR.Revenue.fperiod",
        ],
        parameters={"Period": f"FY-{years - 1}:FY0", "Scale": "6", "Curn": "USD"},
    )


def get_valuation_snapshot(tickers: list[str]) -> pd.DataFrame:
    """Current enterprise value, EV/EBITDA, and market cap."""
    return ld.get_data(
        universe=tickers,
        fields=[
            "TR.CommonName",
            "TR.CompanyMarketCap",
            "TR.EV",
            "TR.EVToEBITDA",
            "TR.PriceToBVPerShare",
        ],
        parameters={"Period": "FY0", "Scale": "6"},
    )


def main() -> None:
    tickers = ["AAPL.O", "MSFT.O", "GOOGL.O"]

    ld.open_session()
    try:
        print("Annual fundamentals (last 5 fiscal years)")
        print("=" * 60)
        print(get_annual_fundamentals(tickers).to_string())

        print("\n\nCurrent valuation snapshot")
        print("=" * 60)
        print(get_valuation_snapshot(tickers).to_string())
    finally:
        ld.close_session()


if __name__ == "__main__":
    main()
