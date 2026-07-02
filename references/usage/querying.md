# Querying: Periods, Dates, and Pitfalls

How to retrieve fundamentals, estimates, ratios, and ESG with `ld.get_data()` —
choosing the right time parameters and avoiding the classic mistakes.

All examples assume an open session:

```python
import lseg.data as ld
ld.open_session()
# ... queries ...
ld.close_session()
```

## Period parameter (recommended for fundamentals)

`Period` selects fiscal or calendar periods with a compact syntax. This is the
best way to retrieve multi-period fundamental data.

### Prefixes

| Prefix | Meaning | Fiscal year end |
|---|---|---|
| `FY` | Fiscal Year | Company-specific (AAPL = Sept, MSFT = June) |
| `FQ` | Fiscal Quarter | Company-specific quarter boundaries |
| `CY` | Calendar Year | Always Jan-Dec |
| `LTM` | Last Twelve Months | Trailing 4 quarters summed |

### Offsets and ranges

| Syntax | Meaning |
|---|---|
| `FY0` | Latest completed fiscal year |
| `FQ0` | Latest completed fiscal quarter |
| `FY-1` | One year ago |
| `FY1` | Next fiscal year (forward — estimates only) |
| `FY-4:FY0` | Range: 5 annual periods |
| `FQ-8:FQ0` | Range: 9 quarterly periods |
| `FY0:FY2` | Current + 2 forward periods |
| `CY-3:CY0` | Calendar-year range |
| `LTM` | Trailing 12-month aggregate (single row) |

```python
# 5 years of annual revenue
df = ld.get_data(
    "AAPL.O",
    ["TR.Revenue", "TR.Revenue.date", "TR.Revenue.fperiod"],
    {"Period": "FY-4:FY0", "Scale": "6"},
)

# 9 quarters of revenue
df = ld.get_data(
    "AAPL.O",
    ["TR.Revenue", "TR.Revenue.fperiod"],
    {"Period": "FQ-8:FQ0"},
)
```

### Forward periods and estimates

Forward periods (`FY1`, `FY2`, ...) return `<NA>` for actual fields but work with
estimate fields (see [../data-items/estimates.md](../data-items/estimates.md)):

```python
# Actuals for the past, consensus for the future
df = ld.get_data(
    "AAPL.O",
    ["TR.Revenue", "TR.RevenueMean", "TR.Revenue.fperiod"],
    {"Period": "FY-1:FY2"},
)
```

For estimate fields, `.date` returns the date the estimate was retrieved, not the
fiscal period end. Use `.fperiod` to label each period.

## SDate / EDate / Frq (for date ranges and daily fields)

These three parameters define a date range and sampling frequency. They are best
for **daily time-series fields** — valuation ratios, market cap, enterprise value.

### Frq values

| Frq | Meaning | Best for |
|---|---|---|
| `D` | Daily | Valuation ratios, market cap, EV |
| `W` | Weekly | Weekly snapshots |
| `M` | Monthly | Monthly snapshots |
| `FQ` / `FY` | Fiscal Quarter / Year | Fundamental fields (see gotcha 1) |
| `CQ` / `CY` | Calendar Quarter / Year | Fundamental fields |

**Spelled-out names do NOT work.** `"Monthly"`, `"Daily"` throw errors — use the
abbreviations.

```python
# Daily enterprise value over a month
df = ld.get_data(
    "AAPL.O",
    ["TR.EV", "TR.EV.date"],
    {"SDate": "2025-01-01", "EDate": "2025-02-01", "Frq": "D"},
)
```

### SDate as an "as of" date

Combined with `Period`, `SDate` shifts the reference point for relative offsets —
useful for point-in-time analysis:

| Parameters | Result |
|---|---|
| `Period=FY0` | Latest completed FY |
| `Period=FY0, SDate=2022-01-01` | Latest FY as of Jan 2022 |

## Critical gotchas

**1. `Frq` does not change data resolution.** Using `Frq=FQ` with `SDate/EDate` on
an *annual* field repeats the annual value each quarter. To get real quarterly
data, use `Period="FQ-N:FQ0"` instead.

**2. Never combine a `Period` range with an `SDate/EDate` range.** It creates a
confusing cross-product (one offset per year). Use one or the other.

**3. `Frq` alone (no `SDate/EDate`) is ignored** — you get only the latest period.

**4. Fiscal years are company-specific.** `FY0` maps to different calendar dates
per company (AAPL = Sept, MSFT = June, WMT = Jan). All report "FY2025" at different
dates. Use `CY` periods for calendar-aligned comparisons.

**5. `CY` periods re-aggregate to calendar boundaries.** For non-December fiscal
year ends, CY values differ from FY (they sum quarters to Jan-Dec).

**6. Some fields are entitlement-gated.** A valid field name can still return
access-denied depending on your subscription (P/E and a plain EPS field are common
examples). If so, compute alternatives — e.g. P/E from
`TR.CompanyMarketCap / TR.NetIncome`, or use `TR.F.EPSBasicExclExordItemsComTot` /
`TR.EPSMean` for EPS.

## Scale and Curn

```python
df = ld.get_data(
    "AAPL.O",
    ["TR.Revenue", "TR.Revenue.currency"],
    {"Period": "FY0", "Curn": "EUR", "Scale": "6"},
)
```

- `Scale`: `"6"` = millions, `"9"` = billions. Pass as a string. Works on `TR.*`
  and `TR.F.*`.
- `Curn`: converts to the given currency. Without it, values are in the company's
  native reporting currency. Combine freely with `Scale`.

## Companion suffixes

Append to any field for per-row metadata: `.date` (period end), `.fperiod` (label
like `FY2025`), `.currency`. Each field gets its own companion column. **Always
include `.fperiod`** in multi-period queries so you can tell which period each row
is.

## Multiple instruments and mixed field types

```python
# Multiple instruments
df = ld.get_data(
    ["AAPL.O", "MSFT.O", "GOOGL.O"],
    ["TR.Revenue", "TR.Revenue.fperiod", "TR.EBITDA", "TR.NetIncome"],
    {"Period": "FY-1:FY0", "Scale": "6", "Curn": "USD"},
)

# Fundamentals + valuation + identifiers in one call
df = ld.get_data(
    "AAPL.O",
    ["TR.CommonName", "TR.Revenue", "TR.EVToEBITDA", "TR.CompanyMarketCap"],
    {"Period": "FY0", "Scale": "6"},
)
```

## Decision tree

```
Need pricing (OHLCV)?              -> get_history() (see pricing.md)
Fundamentals at specific periods?  -> get_data() with Period="FY-N:FY0" / "FQ-N:FQ0"
Forward analyst estimates?         -> get_data() with Period="FY1:FYN" (estimates only)
Trailing twelve months?            -> get_data() with Period="LTM"
Daily valuation ratios (EV, MCap)? -> get_data() with SDate/EDate + Frq="D"/"W"/"M"
Point-in-time historical value?    -> get_data() with Period="FY0" + SDate="YYYY-MM-DD"
Calendar-aligned comparison?       -> get_data() with Period="CY-N:CY0"
```
