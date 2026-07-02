# Getting Started

How to authenticate, open a session, and run your first query with the
`lseg.data` Python library.

## Install

```bash
pip install lseg-data
```

You need an **entitled LSEG account** (LSEG Workspace / Refinitiv, or a Data
Platform machine account). The library itself is free; the data is not.

## Authenticate

The library supports two session types:

| Session | When to use | Requires |
|---|---|---|
| `desktop.workspace` | LSEG Workspace or Eikon is running on the same machine | The desktop app open and logged in |
| `platform.ldp` | Headless / server use | Machine ID, password, and app key |

### Option A: config file (recommended)

Create `lseg-data.config.json` in your working directory (or point the
`LD_LIB_CONFIG_PATH` environment variable at its folder):

```json
{
  "sessions": {
    "default": "platform.ldp",
    "platform": {
      "ldp": {
        "app-key": "YOUR_APP_KEY",
        "username": "YOUR_MACHINE_ID",
        "password": "YOUR_PASSWORD"
      }
    }
  }
}
```

> Keep this file out of version control. Never commit credentials.

### Option B: environment variables

```bash
export RDP_APP_KEY="YOUR_APP_KEY"
export RDP_USERNAME="YOUR_MACHINE_ID"
export RDP_PASSWORD="YOUR_PASSWORD"
```

Machine IDs look like `GE-A-01234567-8-9012` — that is not your email address.

## First query

```python
import lseg.data as ld

ld.open_session()

# Fundamentals (point-in-time)
df = ld.get_data(
    universe=["AAPL.O", "MSFT.O"],
    fields=["TR.CommonName", "TR.Revenue", "TR.EPSMean"],
    parameters={"Period": "FY0", "Scale": "6"},
)
print(df.head())   # always inspect the sample

# Historical prices
prices = ld.get_history(
    universe="AAPL.O",
    fields=["OPEN_PRC", "HIGH_1", "LOW_1", "TRDPRC_1", "ACVOL_UNS"],
    start="2024-01-01",
    end="2024-12-31",
    interval="daily",
)
print(prices.head())

ld.close_session()
```

## The two core functions

| Function | Use for | Time parameters |
|---|---|---|
| `ld.get_data()` | Fundamentals, estimates, ratios, ESG, identifiers | `Period`, `SDate/EDate`, `Frq` |
| `ld.get_history()` | OHLCV pricing, intraday bars | `start`, `end`, `interval` |

## Good habits (read before trusting a result)

LSEG silently drops invalid field names and returns empty cells rather than
raising errors. Before you rely on any result:

1. Confirm field names against the [field catalog](../data-items/README.md).
2. Confirm the instrument code (RIC) has the right exchange suffix.
3. Inspect a sample (`.head()`), and check critical columns are not all null.
4. Confirm the date range and periods match what you asked for.
5. Remember **T-1**: end-of-day market data is usually available only the next day.

## Where to go next

- [field-discovery.md](field-discovery.md) — how to find field codes.
- [querying.md](querying.md) — periods, date ranges, and the common pitfalls.
- [pricing.md](pricing.md) — historical and real-time prices.
- [symbology.md](symbology.md) — converting between RIC / ISIN / CUSIP / SEDOL.
- [screening.md](screening.md) — dynamic stock screening.
- [esg.md](esg.md) — ESG scores and emissions.
- [troubleshooting.md](troubleshooting.md) — when something goes wrong.
