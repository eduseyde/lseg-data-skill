# LSEG Time-Series Data Retrieval Guide

Comprehensive guide for retrieving time-series data from LSEG using `get_data()` and `get_history()`.

**Prerequisites**: Active LSEG session via `LsegSession` context manager. See [find-field-names.md](find-field-names.md) for field discovery and [discovered-fields.md](discovered-fields.md) for field reference.

```python
from toolkit.data.providers.lseg import LsegSession
import lseg.data as ld

with LsegSession():
    df = ld.get_data(...)
```

---

## Two retrieval functions

| Function | Use for | Time parameters |
|---|---|---|
| `ld.get_data()` | Fundamentals, estimates, ratios, ESG | `Period`, `SDate/EDate`, `Frq` |
| `ld.get_history()` | OHLCV pricing, intraday bars | `start`, `end`, `interval` |

Use `get_data()` for everything except raw price/volume data. Use `get_history()` for market pricing.

---

## Period parameter

The `Period` parameter selects fiscal or calendar periods using a compact syntax. This is the **recommended way** to retrieve multi-period fundamental data.

### Period prefixes

| Prefix | Meaning | Fiscal year end |
|---|---|---|
| `FY` | Fiscal Year | Company-specific (AAPL=Sept, MSFT=June) |
| `FQ` | Fiscal Quarter | Company-specific quarter boundaries |
| `CY` | Calendar Year | Always Jan–Dec |
| `LTM` | Last Twelve Months | Trailing 4 quarters summed |

### Offset syntax

| Syntax | Meaning | Example (AAPL, today) |
|---|---|---|
| `FY0` | Latest completed fiscal year | FY2025 (ended 2025-09-27) |
| `FQ0` | Latest completed fiscal quarter | FY2026Q1 (ended 2025-12-27) |
| `FY-1` | One year ago | FY2024 |
| `FY1` | Next fiscal year (forward) | FY2026 |
| `FY-4:FY0` | Range: 5 annual periods | FY2021 through FY2025 |
| `FQ-8:FQ0` | Range: 9 quarterly periods | FY2024Q1 through FY2026Q1 |
| `FY0:FY2` | Current + 2 forward periods | FY2025 through FY2027 |
| `CY-3:CY0` | Calendar year range | CY2022 through CY2024 |
| `LTM` | Trailing 12-month aggregate | Single row |

### Examples

**5 years of annual revenue:**
```python
df = ld.get_data("AAPL.O",
    ["TR.Revenue", "TR.Revenue.date", "TR.Revenue.fperiod"],
    {"Period": "FY-4:FY0", "Scale": "6"})
```
```
  Instrument  Revenue       Date Financial Period Absolute
0     AAPL.O   365817 2021-09-25                    FY2021
1     AAPL.O   394328 2022-09-24                    FY2022
2     AAPL.O   383285 2023-09-30                    FY2023
3     AAPL.O   391035 2024-09-28                    FY2024
4     AAPL.O   416161 2025-09-27                    FY2025
```

**9 quarters of revenue:**
```python
df = ld.get_data("AAPL.O",
    ["TR.Revenue", "TR.Revenue.date", "TR.Revenue.fperiod"],
    {"Period": "FQ-8:FQ0"})
```
```
  Instrument       Revenue       Date Financial Period Absolute
0     AAPL.O  119575000000 2023-12-30                  FY2024Q1
...
8     AAPL.O  143756000000 2025-12-27                  FY2026Q1
```

**Last twelve months:**
```python
df = ld.get_data("AAPL.O",
    ["TR.Revenue"],
    {"Period": "LTM", "Scale": "6"})
# → 435,617 (sum of trailing 4 quarters)
```

**11 years of history:**
```python
df = ld.get_data("AAPL.O",
    ["TR.Revenue", "TR.Revenue.fperiod"],
    {"Period": "FY-10:FY0", "Scale": "6"})
# → 11 rows from FY2015 to FY2025
```

### Forward periods and estimates

Forward periods (`FY1`, `FY2`, etc.) return `<NA>` for actual fields but work with estimate fields:

```python
# Actuals for past + estimates for future
df = ld.get_data("AAPL.O",
    ["TR.Revenue", "TR.RevenueMean", "TR.Revenue.fperiod"],
    {"Period": "FY-1:FY2"})
```
```
  Instrument       Revenue  Revenue - Mean Financial Period Absolute
0     AAPL.O  391035000000  390497710880                     FY2024  ← actual
1     AAPL.O  416161000000  415010194840                     FY2025  ← actual
2     AAPL.O          <NA>  465238502110                     FY2026  ← estimate only
3     AAPL.O          <NA>  496514863690                     FY2027  ← estimate only
```

**Forward quarterly estimates:**
```python
df = ld.get_data("AAPL.O",
    ["TR.EPSMean", "TR.EPSMean.date", "TR.EPSMean.fperiod"],
    {"Period": "FQ1:FQ4"})
```
```
  Instrument  Earnings Per Share - Mean       Date Financial Period Absolute
0     AAPL.O                    1.94056 2026-02-10                  FY2026Q2
1     AAPL.O                    1.72517 2026-02-10                  FY2026Q3
2     AAPL.O                    1.98038 2026-02-10                  FY2026Q4
3     AAPL.O                    2.98077 2026-02-03                  FY2027Q1
```

Note: For estimate fields, the `.date` suffix returns the date the estimate was retrieved, not the fiscal period end date.

---

## SDate, EDate, and Frq parameters

These three parameters work together to define a date range and sampling frequency. They are best suited for **daily time-series fields** (valuation ratios, market cap, enterprise value).

### Frq (Frequency) values

| Frq | Meaning | Best for |
|---|---|---|
| `D` | Daily | Valuation ratios, market cap, EV |
| `W` | Weekly | Weekly snapshots |
| `M` | Monthly | Monthly snapshots |
| `FQ` | Fiscal Quarter | Fundamental fields (see warning) |
| `FY` | Fiscal Year | Fundamental fields |
| `CQ` | Calendar Quarter | Fundamental fields |
| `CY` | Calendar Year | Fundamental fields |

**Spelled-out names do NOT work.** `"Monthly"`, `"Weekly"`, `"Daily"` all throw unrecognized errors. Use only the abbreviations above.

### Daily time-series valuation ratios

These fields support `SDate/EDate` + `Frq=D/W/M`:

| Field | Works with Frq=D |
|---|---|
| `TR.EV` | Yes |
| `TR.EVToEBITDA` | Yes |
| `TR.CompanyMarketCap` | Yes |
| `TR.DividendYield` | Yes |
| `TR.BookValuePerShare` | Yes |
| `TR.CurrentRatio` | Yes |
| `TR.PriceToBVPerShare` | Yes |
| `TR.PriceToSalesPerShare` | Yes |
| `TR.PERatio` | **Blocked** (access denied) |
| `TR.EPS` | **Blocked** (access denied) |

**Daily enterprise value over 1 month:**
```python
df = ld.get_data("AAPL.O",
    ["TR.EV", "TR.EV.date"],
    {"SDate": "2025-01-01", "EDate": "2025-02-01", "Frq": "D"})
```

**Weekly market cap:**
```python
df = ld.get_data("AAPL.O",
    ["TR.CompanyMarketCap", "TR.CompanyMarketCap.date"],
    {"SDate": "2025-01-01", "EDate": "2025-02-01", "Frq": "W"})
```

**Monthly EV/EBITDA over 1 year:**
```python
df = ld.get_data("AAPL.O",
    ["TR.EVToEBITDA", "TR.EVToEBITDA.date"],
    {"SDate": "2024-01-01", "EDate": "2025-01-01", "Frq": "M"})
```

### SDate/EDate with fundamental fields

When used with fundamental fields (like `TR.Revenue`) and `Frq=FY`, SDate/EDate selects fiscal periods whose end dates fall within the range:

```python
df = ld.get_data("AAPL.O",
    ["TR.Revenue", "TR.Revenue.fperiod"],
    {"SDate": "2020-01-01", "EDate": "2025-01-01", "Frq": "FY"})
# → FY2020, FY2021, FY2022, FY2023, FY2024 (fiscal years ending within the date range)
```

Without `Frq`, `SDate/EDate` defaults to annual frequency.

### SDate as "as of" date with Period

When `SDate` is combined with `Period`, it shifts the reference point for relative period offsets:

| Parameters | Result |
|---|---|
| `Period=FY0` (no SDate) | Latest completed FY → FY2025 |
| `Period=FY0, SDate=2024-01-01` | Latest FY as of Jan 2024 → FY2023 |
| `Period=FY0, SDate=2022-01-01` | Latest FY as of Jan 2022 → FY2021 |
| `Period=FY0, SDate=2020-01-01` | Latest FY as of Jan 2020 → FY2019 |

This is useful for point-in-time analysis (e.g., "what was the latest available revenue on this date?").

---

## Critical gotchas

### 1. Frq does NOT change data resolution

When using `Frq=FQ` with `SDate/EDate` on an annual fundamental field, the annual value is **repeated** for each quarter:

```python
# BAD — repeats annual values at quarterly cadence
df = ld.get_data("AAPL.O",
    ["TR.Revenue", "TR.Revenue.fperiod"],
    {"SDate": "2023-01-01", "EDate": "2025-01-01", "Frq": "FQ"})
```
```
  FY2022: 394B (repeated 3x)
  FY2023: 383B (repeated 4x)
  FY2024: 391B (repeated 1x)
```

**To get actual quarterly data, use `Period=FQ-N:FQ0` instead.**

### 2. Never combine Period with SDate/EDate ranges

Combining `Period` range with `SDate/EDate` range creates a **cross product** — one Period offset applied per SDate/EDate year:

```python
# BAD — produces 15 confusing rows instead of 3
df = ld.get_data("AAPL.O",
    ["TR.Revenue"],
    {"Period": "FY-2:FY0", "SDate": "2020-01-01", "EDate": "2025-01-01"})
```

Use either `Period` ranges OR `SDate/EDate` + `Frq`, not both.

### 3. Frq alone (without SDate/EDate) is ignored

```python
# Returns only the latest period — Frq has no effect
df = ld.get_data("AAPL.O",
    ["TR.Revenue"],
    {"Frq": "FQ"})
# → 1 row: FY2025 (latest annual)
```

### 4. FY periods are company-specific

`FY0` maps to different calendar dates for different companies:

| Company | FY End | FY0 = FY2025 end date |
|---|---|---|
| AAPL.O | September | 2025-09-27 |
| MSFT.O | June | 2025-06-30 |
| WMT | January | 2025-01-31 |

All three report "FY2025" but at different calendar dates. Use `CY` periods for calendar-aligned comparisons.

### 5. CY periods re-aggregate to calendar boundaries

For companies with non-December fiscal year ends, CY values differ from FY:
- AAPL FY2024 Revenue: $391B (Oct 2023 – Sep 2024)
- AAPL CY2024 Revenue: $397B (Jan 2024 – Dec 2024)

CY aggregation sums quarterly data to January–December boundaries.

### 6. TR.PERatio and TR.EPS are access-denied

Despite appearing in field discovery, `TR.PERatio` and `TR.EPS` are blocked for our API scope. Use alternatives:
- For P/E: compute from `TR.CompanyMarketCap / TR.NetIncome`
- For EPS: use `TR.F.EPSBasicExclExordItemsComTot` (standardized) or `TR.EPSMean` (consensus estimate)

---

## Scale and Curn parameters

### Scale — numeric scaling

| Scale | Divisor | Example (AAPL Revenue) |
|---|---|---|
| None | 1 | 416,161,000,000 |
| `"6"` | 10^6 (millions) | 416,161 |
| `"9"` | 10^9 (billions) | 416.161 |

Works on both `TR.*` and `TR.F.*` fields. Pass as string.

### Curn — currency conversion

```python
# Convert to EUR
df = ld.get_data("AAPL.O",
    ["TR.Revenue", "TR.Revenue.currency"],
    {"Period": "FY0", "Curn": "EUR", "Scale": "6"})
# → Revenue: 355,664  Currency: EUR
```

- Without `Curn`, values are in the company's native reporting currency
- Use `.currency` suffix to confirm which currency is used
- `Scale` and `Curn` can be combined freely

---

## Companion field suffixes

Append these suffixes to any field code for metadata about each row:

| Suffix | Returns | Example |
|---|---|---|
| `.date` | Fiscal period end date | `TR.Revenue.date` → `2025-09-27` |
| `.fperiod` | Fiscal period label | `TR.Revenue.fperiod` → `FY2025` |
| `.currency` | Reporting currency | `TR.Revenue.currency` → `USD` |

- Work on both `TR.*` and `TR.F.*` fields
- Each field gets its own companion column: `TR.Revenue.fperiod` and `TR.EBITDA.fperiod` are separate columns
- For estimate fields, `.date` returns the estimate retrieval date (not fiscal period end)
- **Always include `.fperiod`** in multi-period queries to identify which period each row belongs to

```python
df = ld.get_data("AAPL.O",
    ["TR.F.EBITDA", "TR.F.EBITDA.date", "TR.F.EBITDA.fperiod", "TR.F.EBITDA.currency"],
    {"Period": "FQ-3:FQ0"})
```

---

## Multiple instruments

All time-series parameters work with multiple instruments:

```python
df = ld.get_data(
    ["AAPL.O", "MSFT.O", "GOOGL.O"],
    ["TR.Revenue", "TR.Revenue.fperiod", "TR.EBITDA", "TR.NetIncome"],
    {"Period": "FY-1:FY0", "Scale": "6", "Curn": "USD"})
```
```
  Instrument  Revenue Financial Period Absolute  EBITDA  Net Income
0     AAPL.O   391035                    FY2024  134661       93736
1     AAPL.O   416161                    FY2025  144748      112010
2     MSFT.O   245122                    FY2024  129433       88136
3     MSFT.O   281724                    FY2025  156528      101832
```

Rows are grouped by instrument, then sorted by period.

---

## Mixing field types in one query

You can combine fundamentals, valuation ratios, estimates, and identifiers in a single call:

```python
df = ld.get_data("AAPL.O",
    ["TR.CommonName", "TR.Revenue", "TR.EVToEBITDA", "TR.CompanyMarketCap"],
    {"Period": "FY0", "Scale": "6"})
```
```
  Instrument Company Common Name  Revenue  EV/EBITDA  Company Market Cap
0     AAPL.O           Apple Inc   416161   26.6456       4,050,595
```

---

## ESG fields with time-series

ESG scores support `SDate/EDate` with `Frq=FY` for annual time series:

```python
df = ld.get_data("AAPL.O",
    ["TR.TRESGScore", "TR.EnvironmentPillarScore", "TR.TRESGScore.date"],
    {"SDate": "2020-01-01", "EDate": "2025-01-01", "Frq": "FY"})
```
```
  Instrument  ESG Score  Environmental Pillar Score       Date
0     AAPL.O      67.78                       61.01 2019-09-28
1     AAPL.O      77.46                       65.10 2020-09-26
2     AAPL.O      82.37                       66.23 2021-09-25
3     AAPL.O      77.62                       67.00 2022-09-24
4     AAPL.O      74.71                       66.60 2023-09-30
```

---

## get_history() — pricing time series

For OHLCV pricing data, use `get_history()` instead of `get_data()`:

### Intervals

| Interval | Description |
|---|---|
| `"daily"` | Daily bars |
| `"weekly"` | Weekly bars (end-of-week) |
| `"monthly"` | Monthly bars |
| `"1min"`, `"5min"`, `"15min"`, `"30min"`, `"60min"` | Intraday bars |

### Default fields

Without specifying fields, `get_history()` returns ~17 columns including prices, volume, VWAP, bid/ask, and block trade data:

`TRDPRC_1` (close), `HIGH_1`, `LOW_1`, `OPEN_PRC`, `ACVOL_UNS` (volume), `VWAP`, `BID`, `ASK`, `TRNOVR_UNS` (turnover), `BLKCOUNT`, `BLKVOLUM`, `NUM_MOVES`, `TRD_STATUS`, `SALTIM`, `NAVALUE`, `VWAP_VOL`

### Clean OHLCV

For standard OHLCV data, specify fields explicitly:

```python
df = ld.get_history("AAPL.O",
    fields=["OPEN_PRC", "HIGH_1", "LOW_1", "TRDPRC_1", "ACVOL_UNS"],
    start="2025-01-02", end="2025-01-10", interval="daily")
```
```
AAPL.O      OPEN_PRC   HIGH_1    LOW_1  TRDPRC_1  ACVOL_UNS
Date
2025-01-03    243.36   244.18   241.89    243.36   40244114
2025-01-06    244.31   247.33    243.2     245.0   45045571
2025-01-07    242.98   245.55   241.35    242.21   40855960
2025-01-08    241.92  243.71    240.05     242.7   37628940
2025-01-10    240.01   240.16    233.0    236.85   61710856
```

### Multiple instruments

Multi-instrument queries return MultiIndex columns `(instrument, field)`:

```python
df = ld.get_history(["AAPL.O", "MSFT.O"],
    fields=["TRDPRC_1", "ACVOL_UNS"],
    start="2025-01-02", end="2025-01-10", interval="daily")
```
```
             AAPL.O             MSFT.O
           TRDPRC_1 ACVOL_UNS TRDPRC_1 ACVOL_UNS
2025-01-03   243.36  40244114   423.35  16662943
2025-01-06    245.0  45045571   427.85  20573648
```

### Wrapper function

Our toolkit wrapper (`toolkit.data.providers.lseg.get_history`) adds:
- Automatic yearly chunking for large date ranges (>3000 estimated trading days)
- T-1 lag warning when `end` is today
- Empty result validation

```python
from toolkit.data.providers.lseg import get_history, LsegSession

with LsegSession():
    df = get_history("AAPL.O",
        fields=["OPEN_PRC", "HIGH_1", "LOW_1", "TRDPRC_1", "ACVOL_UNS"],
        start="2020-01-01", end="2025-01-01", interval="daily")
```

---

## Quick reference: common use cases

### Get 5 years of annual revenue
```python
df = ld.get_data("AAPL.O",
    ["TR.Revenue", "TR.Revenue.fperiod"],
    {"Period": "FY-4:FY0", "Scale": "6"})
```

### Get quarterly EPS (last 8 quarters)
```python
df = ld.get_data("AAPL.O",
    ["TR.F.EPSBasicExclExordItemsComTot", "TR.F.EPSBasicExclExordItemsComTot.fperiod"],
    {"Period": "FQ-7:FQ0"})
```

### Get forward analyst estimates
```python
df = ld.get_data("AAPL.O",
    ["TR.RevenueMean", "TR.EPSMean", "TR.RevenueMean.fperiod"],
    {"Period": "FY1:FY3"})
```

### Get daily enterprise value over 1 year
```python
df = ld.get_data("AAPL.O",
    ["TR.EV", "TR.EV.date"],
    {"SDate": "2024-01-01", "EDate": "2025-01-01", "Frq": "D"})
```

### Compare companies across different fiscal years
```python
df = ld.get_data(["AAPL.O", "MSFT.O", "WMT"],
    ["TR.Revenue", "TR.Revenue.fperiod", "TR.Revenue.date"],
    {"Period": "FY-2:FY0", "Scale": "6", "Curn": "USD"})
```

### Get trailing 12-month metrics
```python
df = ld.get_data("AAPL.O",
    ["TR.Revenue", "TR.EBITDA", "TR.NetIncome"],
    {"Period": "LTM", "Scale": "6"})
```

### Get annual ESG scores over time
```python
df = ld.get_data("AAPL.O",
    ["TR.TRESGScore", "TR.EnvironmentPillarScore", "TR.SocialPillarScore",
     "TR.GovernancePillarScore", "TR.TRESGScore.date"],
    {"SDate": "2018-01-01", "EDate": "2025-01-01", "Frq": "FY"})
```

### Get 1 year of daily OHLCV prices
```python
from toolkit.data.providers.lseg import get_history, LsegSession

with LsegSession():
    df = get_history("AAPL.O",
        fields=["OPEN_PRC", "HIGH_1", "LOW_1", "TRDPRC_1", "ACVOL_UNS"],
        start="2024-01-01", end="2025-01-01", interval="daily")
```

### Get quarterly income statement items
```python
df = ld.get_data("AAPL.O",
    ["TR.F.TotRevenue", "TR.F.EBITDA", "TR.F.NetIncAfterTax",
     "TR.F.TotRevenue.fperiod"],
    {"Period": "FQ-7:FQ0", "Scale": "6"})
```

### Non-US company with currency conversion
```python
df = ld.get_data("BMWG.DE",
    ["TR.Revenue", "TR.EBITDA", "TR.Revenue.fperiod", "TR.Revenue.currency"],
    {"Period": "FY-2:FY0", "Scale": "6", "Curn": "USD"})
```

---

## Decision tree: which approach to use?

```
Need pricing data (OHLCV)?
  → get_history() with start/end/interval

Need fundamental data at specific periods?
  → get_data() with Period parameter
    Annual:    Period="FY-N:FY0"
    Quarterly: Period="FQ-N:FQ0"
    Forward:   Period="FY1:FYN" (estimates only)
    LTM:       Period="LTM"

Need daily valuation ratios (EV, EV/EBITDA, market cap)?
  → get_data() with SDate/EDate + Frq="D" (or "W" / "M")

Need point-in-time historical data?
  → get_data() with Period="FY0" + SDate="YYYY-MM-DD"

Need calendar-aligned cross-company comparison?
  → get_data() with Period="CY-N:CY0"
```
