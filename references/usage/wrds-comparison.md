# LSEG vs WRDS

A bridge for researchers who know WRDS (CRSP / Compustat) and need to work with the
LSEG Data Library.

| Aspect | WRDS | LSEG Data Library |
|---|---|---|
| Access | SQL via the `wrds` package | Python API via `lseg.data` |
| Data model | Relational tables | Instruments + fields |
| Identifiers | PERMNO, GVKEY, CUSIP | RIC, ISIN, SEDOL |
| Coverage focus | US-centric, academic | Global, real-time capable |
| Update cadence | Batch (daily/monthly) | Real-time to daily |

## Identifier mapping

| WRDS | LSEG | Notes |
|---|---|---|
| PERMNO | RIC | CRSP permanent number vs Reuters Instrument Code |
| GVKEY | OrgId | Compustat company key vs LSEG Organization ID |
| CUSIP | CUSIP | Same standard — but LSEG returns 9 chars, CRSP often uses 8 |
| TICKER | Ticker | Exchange-specific |

```python
from lseg.data.content import symbol_conversion

# CUSIP -> RIC / ISIN
symbol_conversion.Definition(
    symbols=["037833100"],
    from_symbol_type="CUSIP",
    to_symbol_types=["RIC", "ISIN"],
).get_data()
```

## Field mapping (fundamentals)

| Concept | WRDS (Compustat) | LSEG (validated) |
|---|---|---|
| Revenue | `revt` | `TR.Revenue` |
| Net income | `ni` | `TR.NetIncome` |
| Total assets | `at` | `TR.TotalAssets` |
| Book equity | `ceq` | `TR.TotalEquity` |
| EPS (basic) | `epspx` | `TR.F.EPSBasicExclExordItemsComTot` |

## Field mapping (pricing)

| Concept | WRDS (CRSP) | LSEG |
|---|---|---|
| Close price | `prc` | `TRDPRC_1` (via `get_history`) |
| Volume | `vol` | `ACVOL_UNS` (via `get_history`) |
| Bid / Ask | `bid`, `ask` | `BID`, `ASK` |
| Market cap | `prc * shrout` | `TR.CompanyMarketCap` |
| Return | `ret` | compute from adjusted prices |

## Same task, both platforms

**Annual revenue — WRDS:**
```python
db.raw_sql("""
    SELECT gvkey, datadate, fyear, tic, revt, ni
    FROM comp.funda
    WHERE tic IN ('AAPL','MSFT') AND fyear >= 2020
      AND indfmt='INDL' AND datafmt='STD' AND popsrc='D' AND consol='C'
""")
```

**Annual revenue — LSEG:**
```python
ld.get_data(
    universe=["AAPL.O", "MSFT.O"],
    fields=["TR.Revenue", "TR.NetIncome", "TR.Revenue.fperiod"],
    parameters={"Period": "FY-4:FY0", "Scale": "6", "Curn": "USD"},
)
```

## Key differences

- **Dates:** WRDS carries `datadate`/`fyear` columns; LSEG uses the `Period`
  parameter (`FY0`, `FQ0`, ranges) — see [querying.md](querying.md).
- **Adjustments:** CRSP has separate adjusted fields (`ret`, `cfacpr`); LSEG takes
  `adjustments=["split","dividend"]` on `get_history`.
- **Universe:** WRDS queries index-constituent tables; LSEG uses chain RICs
  (`0#.SPX` for S&P 500 constituents).
- **Missing data:** SQL `NULL` vs pandas `NaN` — `df.dropna(subset=[...])`.

## When to prefer which

**WRDS** for long clean US history, established PERMNO-GVKEY links, reproducible
static datasets, and complex SQL joins. **LSEG** for global coverage, real-time and
intraday data, broad ESG, and quick API lookups.

## Migration tips

- **WRDS -> LSEG:** map identifiers first (PERMNO/GVKEY -> RIC), then validate a few
  overlapping periods before trusting the rest.
- **LSEG -> WRDS:** pull CUSIP from LSEG, truncate to 8 characters, link via CRSP
  `msenames`.
