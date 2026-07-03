# Benchmarks & Indices (`TR.Index*` / RIC-addressed)

Index-level data for equity benchmarks (S&P 500, FTSE 100, Euro Stoxx 50, Nikkei, MSCI
composites, …): the **index level**, its **valuation multiples** (P/E, price-to-book, dividend
yield — trailing and forward), **market cap**, **pre-computed returns**, **reference metadata**,
and **constituents**. A separate `TR.Benchmark*` family covers **fixed-income** benchmarks
(yield-to-maturity, durations, spreads). Everything below was **enumerated and validated live
against the MCP field catalogue and `get_data` on 2026-07-02 / 2026-07-03**; the specific values
quoted are real prints kept as evidence the fields resolve on this account.

> **Two distinct benchmark families.** They do not mix, and they live under different parent
> categories in the field catalogue:
>
> | Family | Parent category | Prefix | Covers |
> |---|---|---|---|
> | **Equity Index Information** | `Equity Index Information` | `TR.Index*` | Equity benchmarks — the bulk of this doc |
> | **ICW Benchmark Master Dataset** | `ICW Benchmark Master Dataset` | `TR.Benchmark*` | Fixed-income benchmarks — separate section at the end |

## The single most important gotcha: `get_history` is DENIED for indices

On the account tested, **`ld.get_history()` on an index RIC returns a hard permission error**, not
data:

```
get_history(".SPX", start=..., end=...)
  -> LSEG API error: (TSCC.QS.UserNotPermission.92000, User has no permission)
get_history(".DJI", ...)  -> same denial
```

This is a blanket entitlement gap on the index time-series feed, confirmed on multiple index RICs.
**The workaround — which works fully — is `ld.get_data()` with the price field `TR.PriceClose`**
plus an `SDate`/`EDate`/`Frq` range. Index levels, and every analytic below, come through
`get_data`, never `get_history`. So unlike equities or FX (which use `get_history` for prices),
indices are a **`get_data`-only** family here.

## RIC anatomy

Index RICs are a **leading dot + code**: `.SPX`, `.FTSE`, `.GDAXI`. Validated live via `get_data`:

| RIC | Index | Calc ccy | Validated print |
|---|---|---|---|
| `.SPX` | S&P 500 (price return) | USD | close 6173.07 (2025-06-27); P/E 27.29 |
| `.DJI` | Dow Jones Industrial Average | USD | 30 constituents returned |
| `.FTSE` | FTSE 100 | GBP | "FTSE 100 Index", P/E 18.58 |
| `.GDAXI` | DAX (performance index) | EUR | P/E 18.82 |
| `.STOXX50E` | Euro Stoxx 50 (price) | EUR | P/E 18.49 |
| `.STOXX` | Stoxx Europe 600 | EUR | close 648.35 |
| `.N225` | Nikkei 225 | JPY | "Nikkei 225 Index", P/E 23.28 |
| `.TOPX` | TOPIX | JPY | close 4064.6 |
| `.SPXTR` | S&P 500 **Total Return** | USD | close 16739.26 |
| `.MIWO00000PUS` | MSCI World | USD | close 4832.1 |

Two things this table demonstrates:

- **Total-return / gross variants are their own RIC** (`.SPXTR` for the S&P total-return index),
  read the same way (`TR.PriceClose`). Not every guessed TR form resolves — `.SX5T` came back
  empty — so confirm the exact RIC rather than assuming a suffix convention.
- **MSCI composites resolve** (`.MIWO00000PUS` = MSCI World), so the family is not limited to
  single-country exchange indices.

**Finding an index RIC** — filter `search_instruments` to the Indices category (ETFs otherwise
flood the results and come back with a null RIC):

```python
ld.discovery.search(
    query="S&P 500",
    filter="SearchAllCategory eq 'Indices'",   # equivalently RCSAssetCategoryLeaf eq 'Equity Index'
    select="RIC,DocumentTitle,RCSAssetCategoryLeaf",
)
# -> .SPX | "S&P 500 Index - CBOE, Equity Index" | Equity Index
```

## Index level (price)

| Field Code | Title | Type | Notes |
|---|---|---|---|
| `TR.PriceClose` | Price Close | Money | The index level. Daily via `SDate`/`EDate`/`Frq`. **This is the get_history replacement.** |

**Historical depth (validated on `.SPX`):** the level reaches back to at least **January 1973**
(prints ~114–120, correct for the early-1973 S&P). This is much deeper than the valuation analytics
below. Append `TR.PriceClose.date` for the observation date — but see the `.date` caveat under
gotchas (companion dates only populate for the field that actually has data).

## Valuation analytics — the core (`TR.Index_*`, category "Analytics")

These are LSEG's own index-level multiples, rebuilt from the constituents. **Each measure exists in
two flavours** — exactly like the FX/swap composite-vs-contributor split:

- **`_RTRS`** = Refinitiv/LSEG-**calculated**. Broadly populated. **Use this.**
- **`_VENDOR`** = the number as the **index provider** reports it. On this account it came back
  **null for `.SPX`, `.FTSE`, `.GDAXI`, `.STOXX50E`, `.N225`** — treat VENDOR as MSCI-/entitlement-
  specific and not a reliable default.

| Concept | `_RTRS` (use this) | `_VENDOR` |
|---|---|---|
| Trailing P/E | `TR.Index_PE_RTRS` | `TR.Index_PE_VENDOR` |
| Price-to-book | `TR.Index_PRICE_TO_BOOK_RTRS` | `TR.Index_PRICE_TO_BOOK_VENDOR` |
| Gross dividend yield (%) | `TR.Index_DIV_YLD_RTRS` | `TR.Index_DIV_YLD_VENDOR` |
| Forward P/E, year 1 | `TR.Index_EST_PE_Y1_RTRS` | `TR.Index_EST_PE_Y1_VENDOR` |
| Forward P/E, year 2 | `TR.Index_EST_PE_Y2_RTRS` | `TR.Index_EST_PE_Y2_VENDOR` |
| Forward div yield, year 1 | `TR.Index_EST_DIV_YLD_Y1_RTRS` | `TR.Index_EST_DIV_YLD_Y1_VENDOR` |
| Forward div yield, year 2 | `TR.Index_EST_DIV_YLD_Y2_RTRS` | `TR.Index_EST_DIV_YLD_Y2_VENDOR` |
| Market cap, local ccy | `TR.Index_MKT_CAP_RTRS` | `TR.Index_MKT_CAP_VENDOR` |
| Market cap, USD | `TR.Index_MKT_CAP_USD_RTRS` | `TR.Index_MKT_CAP_USD_VENDOR` |
| Observation date | `TR.Index_CalcDate` (often null — prefer `TR.Index_PE_RTRS.date`) | |

**Validated cross-section** (latest, `_RTRS`):

| RIC | P/E | Div yld % | P/B | Fwd P/E Y1 / Y2 | Mkt cap |
|---|---|---|---|---|---|
| `.SPX` | 27.29 | 1.32 | 5.23 | 21.97 / 19.06 | null |
| `.FTSE` | 18.58 | — | — | — | null |
| `.GDAXI` | 18.82 | — | — | — | null |
| `.STOXX50E` | 18.49 | — | — | — | null |
| `.N225` | 23.28 | — | — | — | 1,042.3tn JPY / \$6.41tn |

Note P/E populates for **all** indices; market cap only for some (`.N225` yes, `.SPX` no). Coverage
of any one analytic is provider-dependent — always inspect for nulls.

**Two behaviours that will trip you up:**

1. **`Frq` is ignored — these fields return a value for every trading day.** Ask for `Frq="M"`
   and you still get the full daily series (a 2010–2025 pull on two indices is ~8,000 rows /
   ~1.4 MB). Pull it, then **down-sample yourself** (e.g. last obs per month/year). For big pulls,
   export straight to a file (see access patterns) rather than into memory.
2. **Analytics history is shallow — roughly 2003 onward.** Validated on `.SPX`: the P/E, dividend
   yield and price-to-book series are **null in 1990 and 1995**, **populated from 2003** (e.g.
   2003-06-02: P/E 19.44, div yld 1.95, P/B 2.94). So the multiples cover the last ~20+ years,
   while the raw price level (`TR.PriceClose`) goes back to the 1970s. Do not expect a 1990s
   valuation panel from these fields.

## Pre-computed returns (`TR.IndexTotalReturn*`, category "Index Returns")

Ready-made total-return figures over standard windows, drawn from the linked total-return variant
(so they exist where a TR index is linked — populated for `.SPX`, `.GDAXI`, `.STOXX50E`; null for
`.FTSE`, `.N225` on this account):

| Field Code | Window |
|---|---|
| `TR.IndexTotalReturnWTD` / `MTD` / `QTD` / `YTD` | Week / month / quarter / year to date |
| `TR.IndexTotalReturn1Wk` / `1Mo` / `3Mo` / `6Mo` | Trailing 1w / 1m / 3m / 6m |
| `TR.IndexTotalReturn1Yr` / `3Yr` / `5Yr` | Trailing 1 / 3 / 5 years |

Validated: `.SPX` 1-year 21.62%, 5-year 84.79%; `.STOXX50E` 1-year 23.07%.

## Reference metadata (`TR.Index*`, category "Index Details")

Descriptive attributes. **Coverage is sparse and uneven** — the same field is populated for one
index and null for another, and several are null even where the name resolves. The reliably useful
ones are `TR.IndexCalculationCurrency` (populated for all five test indices) and, for many indices,
`TR.IndexName` / `TR.IndexIssuerName` / `TR.IndexGeography` / `TR.IndexAveragingMethod`.

| Field Code | Title | Populated example |
|---|---|---|
| `TR.IndexName` | Index name | `.FTSE` → "FTSE 100 Index" (null for `.SPX`, `.GDAXI`, `.STOXX50E`) |
| `TR.IndexIssuerName` | Issuer/administrator | `.FTSE` → "FTSE International Ltd" |
| `TR.IndexGeography` | Country | `.FTSE` → "United Kingdom" |
| `TR.IndexCalculationCurrency` | Calc currency | all five: USD/GBP/EUR/EUR/JPY |
| `TR.IndexAveragingMethod` | Arithmetic vs geometric | `.FTSE`, `.N225` → "Arithmetic" |
| `TR.IndexBaseDate` / `TR.IndexBaseValue` | Base date & level | often null (null even for `.FTSE`) |
| `TR.IndexBeginDate` / `TR.Index_EndDate` | Data start / termination date | often null |
| `TR.IndexShareNumberType` | Free-float / listed / issued | often null |
| `TR.IndexDivisor` | Price-index divisor | often null |
| `TR.IndexSeriesName` / `TR.Index_Name` | Series name | — |
| `TR.IndexHoldingsDate` | Date of held constituent data | — |

## Constituents

**Current membership works** via two fields (validated on `.DJI` → all 30 members with correct
RICs and names, e.g. `AAPL.OQ` "Apple Inc.", `NVDA.OQ` "Nvidia Corp"):

| Field Code | Title | Notes |
|---|---|---|
| `TR.IndexConstituentRIC` | Constituent RIC | ✅ current membership |
| `TR.IndexConstituentName` | Constituent name | ✅ current membership |
| `TR.IndexConstituentWeightPercent` | Weight (%) | **null for S&P/Dow** — see below |

**Official weights are entitlement-split by provider.** `TR.IndexConstituentWeightPercent` came
back **null for `.DJI`** (an S&P/Dow index). Prior work found MSCI indices *do* populate weights but
without clean identifiers. **Workaround:** rebuild weights yourself from each constituent's
free-float market cap (`TR.CompanyMarketCap` × free-float) and normalise — a mcap×free-float
reconstruction. There are also **MSCI-only** constituent fields: `TR.Index_ConstituentPrice`,
`TR.Index_ConstituentPriceCurr`, `TR.Index_ConstituentMarketCapNextDay` (descriptions explicitly say
"for MSCI only").

**Point-in-time / historical membership.** Passing a plain historical date range to the constituent
fields (`SDate=EDate=2008-06-30` on `.DJI`) **returned null** — the simple date-range form does not
back-date membership here. For the historical change record, use the **joiners-and-leavers** family
(category "Index Joiners and Leavers"), which is the audit trail of additions/removals:

| Field Code | Title |
|---|---|
| `TR.IndexJLConstituentRIC` | RIC that joined/left |
| `TR.IndexJLConstituentName` / `...ComName` | Name / common name |
| `TR.IndexJLConstituentChange` | "Joiner" vs "Leaver" |
| `TR.IndexJLConstituentChangeDate` | Date of the change |

Reconstruct any past constituent set by taking today's membership and rolling the joiner/leaver log
backwards. (Point-in-time membership with no survivorship bias is available in the LSEG platform
generally, but through a parameterised field form / chain expansion rather than the plain MCP
date-range tested here.)

## Fixed-income benchmarks (`TR.Benchmark*`, "ICW Benchmark Master Dataset")

A separate family for **bond** benchmarks, at both index-group and constituent level. Enumerated live
(fields resolve in the catalogue); it requires **fixed-income benchmark identifiers** and likely a
separate entitlement, so validate access with your own benchmark IDs before relying on it.

Index-group analytics (`TR.Benchmark*`):

| Field Code | Meaning |
|---|---|
| `TR.BenchmarkYieldToMaturityRate` | Yield to maturity |
| `TR.BenchmarkYieldToWorstRate` | Yield to worst |
| `TR.BenchmarkZeroCouponYieldRate` | Zero-coupon yield |
| `TR.BenchmarkGrossSpreadRate` | Spread to the pricing curve |
| `TR.BenchmarkEffectiveDurationYears` | Effective duration (option-adjusted) |
| `TR.BenchmarkMacaulayDurationYears` | Macaulay duration |
| `TR.BenchmarkSpreadDurationYears` | Spread duration |
| `TR.BenchmarkRealYieldDurationYears` | Real-yield duration |
| `TR.BenchmarkAverageLifeYears` | Average life |
| `TR.BenchmarkCouponPaidAmount` | Coupon paid |

Every one has a **constituent-level analogue** (`TR.BenchmarkConstituent…`: `…YieldToMaturityRate`,
`…EffectiveDurationYears`, `…GrossSpreadRate`, `…OutstandingAmount`, `…MembershipJoinDate`,
`…MembershipLeaveDate`, etc.), so a bond benchmark can be decomposed security by security.

## Access patterns

**1. A valuation time series for one benchmark** — pull daily (the analytics ignore `Frq`), then
down-sample:

```python
import lseg.data as ld
ld.open_session()
df = ld.get_data(
    universe=[".SPX"],
    fields=["TR.Index_PE_RTRS", "TR.Index_PRICE_TO_BOOK_RTRS",
            "TR.Index_DIV_YLD_RTRS", "TR.Index_PE_RTRS.date"],
    parameters={"SDate": "2003-01-01", "EDate": "2026-06-30", "Frq": "D"},
)
# down-sample to year-end yourself:
df["year"] = pd.to_datetime(df["Date"]).dt.year
year_end = df.dropna(subset=["Date"]).sort_values("Date").groupby("year").tail(1)
ld.close_session()
```

**2. A cross-section snapshot across many benchmarks** (latest value, one row each):

```python
df = ld.get_data(
    universe=[".SPX", ".STOXX50E", ".FTSE", ".N225", ".GDAXI"],
    fields=["TR.Index_PE_RTRS", "TR.Index_PRICE_TO_BOOK_RTRS",
            "TR.Index_DIV_YLD_RTRS", "TR.IndexCalculationCurrency"],
)
```

**3. The index level itself** (the `get_history` replacement):

```python
df = ld.get_data(
    universe=[".SPX"],
    fields=["TR.PriceClose", "TR.PriceClose.date"],
    parameters={"SDate": "1990-01-01", "EDate": "2026-06-30", "Frq": "D"},
)
```

**4. Current constituents:**

```python
df = ld.get_data(
    universe=[".DJI"],
    fields=["TR.IndexConstituentRIC", "TR.IndexConstituentName"],
)   # -> 30 rows
```

**Large pulls: write to disk, then process.** A daily multi-index analytics pull runs to thousands
of rows. Persist it (`df.to_parquet(...)`) and post-process from the file rather than holding and
re-inspecting the whole frame in memory.

## Notes / gotchas

- **`get_history` is permission-denied for indices** on this account — use `get_data` +
  `TR.PriceClose` for levels, and `get_data` for all analytics. Indices are a `get_data`-only family.
- **`Frq` is ignored by the index analytics** — they return one value per trading day regardless.
  Down-sample after the fact. Expect large payloads.
- **Analytics history ≈ 2003+, price level ≈ 1973+** on `.SPX`. The multiples are null in the 1990s;
  only the raw level goes deep.
- **`_RTRS` vs `_VENDOR`.** Prefer `_RTRS` (LSEG-calculated, broadly populated). `_VENDOR` was null
  for every major test index — do not default to it.
- **Companion `.date` follows the field that has data.** `TR.Index_PE_RTRS.date` returns `NaT` in a
  period where P/E is null; `TR.PriceClose.date` populates where the price exists. Attach `.date` to
  a field you expect to be non-null, and `TR.Index_CalcDate` is frequently null — don't rely on it.
- **Metadata is sparse and uneven** — `TR.IndexName` is null for `.SPX`/`.GDAXI`/`.STOXX50E` but set
  for `.FTSE`/`.N225`. Always inspect; only `TR.IndexCalculationCurrency` was universally populated.
- **Constituent weights are provider-gated** — null for S&P/Dow; reconstruct from free-float market
  cap. Historical point-in-time membership needs the joiners/leavers log, not a plain date range.
- **Silent field drops.** Invalid field codes (e.g. `TR.IndexConstituentWeight`, `TR.CLOSE`) are
  omitted from the result with only an all-null warning, not an error. Always inspect returned
  columns. Unknown index RICs (`.SX5T`) come back as a null-value row rather than an error.
- **T-1 availability**, as with every LSEG series — the latest close may post only the next day.
- **Two families don't mix:** equity `TR.Index*` vs fixed-income `TR.Benchmark*` (ICW). Related
  index-level valuation for single stocks lives in [valuation-ratios.md](valuation-ratios.md);
  identifiers/classification in [identifiers.md](identifiers.md).
