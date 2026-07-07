---
name: lseg-data
version: 2.0
description: This skill should be used when the user asks to "access LSEG data", "query Refinitiv", "get market data from Refinitiv", "download fundamentals from LSEG", "access ESG scores", "convert RIC to ISIN", or needs the LSEG Data Library Python API (lseg.data).
---

# LSEG Data Library

Access financial data from LSEG (London Stock Exchange Group, formerly Refinitiv)
via the `lseg.data` Python library. This skill covers the pure Python API and
requires an entitled LSEG account.

New here? Start with [references/usage/getting-started.md](references/usage/getting-started.md).

## Query discipline: no data claim without inspection

LSEG **silently drops invalid field names** and returns empty cells instead of
errors, so a query can look successful and still be wrong. Before claiming any
query worked:

1. **Validate** field names against the [field catalog](references/data-items/README.md)
   (check prefixes: `TR.`, `TR.F.`, `CF_`).
2. **Validate** RIC symbology (correct exchange suffix: `.O`, `.N`, `.L`, `.T`).
3. **Execute** the query.
4. **Inspect** a sample (`.head()` / `.sample()`).
5. **Verify** critical columns are not all null.
6. **Verify** the date range and periods match expectations.
7. **Claim** success only after all checks pass.

| Excuse | Reality | Do instead |
|---|---|---|
| "It returned data, so it worked" | Returned ≠ correct | Inspect for nulls, wrong dates, bad values |
| "The user gave me the RIC" | Wrong suffixes are common | Verify symbology |
| "Field names look right" | Typos resolve to nothing | Validate against the catalog first |
| "Market data is current" | T-1 lag | Account for next-day availability |

## Quick start

```python
import lseg.data as ld

ld.open_session()

df = ld.get_data(
    universe=["AAPL.O", "MSFT.O"],
    fields=["TR.CommonName", "TR.Revenue", "TR.EPSMean"],
    parameters={"Period": "FY0", "Scale": "6"},
)
print(df.head())

prices = ld.get_history(
    universe="AAPL.O",
    fields=["OPEN_PRC", "HIGH_1", "LOW_1", "TRDPRC_1", "ACVOL_UNS"],
    start="2024-01-01", end="2024-12-31", interval="daily",
)
print(prices.head())

ld.close_session()
```

## Authentication

Provide credentials via a `lseg-data.config.json` in your working directory (or the
folder named by the `LD_LIB_CONFIG_PATH` environment variable), or via environment
variables. See [references/usage/getting-started.md](references/usage/getting-started.md)
for the full setup. **Never commit credentials.**

## Core APIs

| API | Use case |
|---|---|
| `ld.get_data()` | Point-in-time and periodic data: fundamentals, estimates, ratios, ESG, identifiers |
| `ld.get_history()` | Time series: OHLCV pricing, intraday bars |
| `symbol_conversion.Definition()` | ID mapping: RIC ↔ ISIN ↔ CUSIP ↔ SEDOL |

## Field prefixes

| Prefix | Type | Example |
|---|---|---|
| `TR.F.` | Standardized financial statement line items | `TR.F.TotRevenue` |
| `TR.` | LSEG-calculated values, estimates, ratios, ESG | `TR.Revenue`, `TR.EPSMean` |
| `CF_` | Composite real-time fields | `CF_LAST`, `CF_BID` |

## RIC symbology

| Suffix | Exchange | Suffix | Exchange |
|---|---|---|---|
| `.O` | NASDAQ | `.L` | London |
| `.N` | NYSE | `.DE` | Frankfurt |
| `.P` | NYSE Arca | `.T` | Tokyo |

See [references/usage/symbology.md](references/usage/symbology.md) for the full list
and identifier conversion.

## Rate limits

Requests are throttled and each response is capped (roughly a few thousand rows).
Batch instruments into chunks and chunk long date ranges. See
[references/usage/troubleshooting.md](references/usage/troubleshooting.md).

## Date awareness (T-1)

End-of-day market data is typically available only the next day. When querying up
to "today", expect the latest bar to be missing until T+1; adjust date ranges
accordingly.

## Reference material

**Usage guides** — how to query:

- [usage/getting-started.md](references/usage/getting-started.md) — install, auth, first query
- [usage/field-discovery.md](references/usage/field-discovery.md) — how to find field codes
- [usage/querying.md](references/usage/querying.md) — periods, date ranges, and pitfalls
- [usage/pricing.md](references/usage/pricing.md) — historical and real-time prices
- [usage/symbology.md](references/usage/symbology.md) — identifier conversion
- [usage/screening.md](references/usage/screening.md) — dynamic stock screening
- [usage/esg.md](references/usage/esg.md) — ESG scores and emissions
- [usage/troubleshooting.md](references/usage/troubleshooting.md) — common issues
- [usage/wrds-comparison.md](references/usage/wrds-comparison.md) — for WRDS/CRSP/Compustat users

**Data items** — validated field catalog, by category:

- [data-items/README.md](references/data-items/README.md) — catalog index and the two field families
- Balance sheet, income statement, cash flow, fundamentals, estimates,
  valuation & ratios, ESG, identifiers, pricing fields, funds, interest-rate
  swaps, FX spot, FX forwards, FX options, benchmarks, sovereign yields,
  and money-market & policy rates.

**Examples & scripts:**

- `examples/fundamentals_query.py`, `examples/historical_pricing.py`,
  `examples/stock_screener.py`
- `scripts/test_connection.py` — validate connectivity
