"""
Summary
-------
Smoke test for LSEG Data Library connectivity: open a session, run one fundamentals
query and one pricing query, and report success or a diagnostic message.

Logic
-----
1. Import `lseg.data`; if it isn't installed, print an install hint and exit.
2. Open a session, fetch a validated fundamentals field, and a short price history.
3. Inspect the results are non-empty; close the session; return a success flag.

Usage
-----
    python scripts/test_connection.py
"""

import sys


def test_connection() -> bool:
    """Open a session and confirm basic data retrieval works."""
    try:
        import lseg.data as ld
    except ImportError:
        print("ERROR: lseg-data not installed")
        print("Install with: pip install lseg-data")
        return False

    try:
        print("Opening LSEG session...")
        ld.open_session()
        print("SUCCESS: session opened")

        print("\nTesting fundamentals retrieval...")
        df = ld.get_data(
            universe=["AAPL.O"],
            fields=["TR.CommonName", "TR.Revenue"],
            parameters={"Period": "FY0", "Scale": "6"},
        )
        if df is not None and not df.empty:
            print(f"SUCCESS: retrieved data for {df.iloc[0]['TR.CommonName']}")
        else:
            print("WARNING: empty fundamentals response")

        print("\nTesting pricing retrieval...")
        hist = ld.get_history(
            universe="AAPL.O",
            fields=["TRDPRC_1"],
            start="2024-01-02",
            end="2024-01-10",
            interval="daily",
        )
        if hist is not None and not hist.empty:
            print(f"SUCCESS: retrieved {len(hist)} price rows")
        else:
            print("WARNING: empty pricing response")

        ld.close_session()
        print("\nSession closed successfully")
        return True

    except Exception as e:
        print(f"ERROR: {e}")
        print("\nCheck:")
        print("  1. A lseg-data.config.json with valid credentials exists in your")
        print("     working directory (or the folder named by LD_LIB_CONFIG_PATH),")
        print("  2. or environment variables RDP_APP_KEY, RDP_USERNAME, RDP_PASSWORD are set,")
        print("  3. and you have network connectivity to LSEG servers.")
        try:
            import lseg.data as ld
            ld.close_session()
        except Exception:
            pass
        return False


if __name__ == "__main__":
    sys.exit(0 if test_connection() else 1)
