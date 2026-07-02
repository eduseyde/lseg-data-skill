"""
Summary
-------
Screen the LSEG equity universe with the `Screener` object, then pull details for
the matching instruments with `get_data()`.

Logic
-----
1. Open an LSEG session.
2. Build a screening expression (active public primary equities, market cap and
   performance filters) and evaluate it to a list of RICs.
3. Retrieve descriptive fields for the matches.
4. Print results and close the session.

Usage
-----
    python examples/stock_screener.py
"""

import lseg.data as ld
from lseg.data.discovery import Screener


def large_cap_energy_momentum() -> Screener:
    """Large-cap US energy names with strong 3-month total return."""
    return Screener(
        "U(IN(Equity(active,public,primary))), "
        "TR.CompanyMarketCap(Scale=6)>=5000, "
        'IN(TR.ExchangeMarketIdCode,"XNYS"), '
        'IN(TR.TRBCBusinessSectorCode,"5010","5020","5030"), '
        "TR.TotalReturn3Mo>=15, "
        "CURN=USD"
    )


def main() -> None:
    ld.open_session()
    try:
        rics = large_cap_energy_momentum()
        matches = list(rics)
        print(f"Matched {len(matches)} instruments: {matches}")

        if matches:
            df = ld.get_data(
                matches,
                [
                    "TR.CommonName",
                    "TR.CompanyMarketCap(Scale=6)",
                    "TR.ExchangeName",
                    "TR.TRBCBusinessSector",
                    "TR.TotalReturn3Mo",
                ],
            )
            print(df.to_string())
    finally:
        ld.close_session()


if __name__ == "__main__":
    main()
