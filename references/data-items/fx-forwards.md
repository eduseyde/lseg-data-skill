# FX Forwards & Forward Points (RIC-addressed, `get_history`)

Forward points, outright forward rates, and non-deliverable forwards (NDFs) across the standard
FX tenor ladder. Coverage was enumerated live from the MCP (`search_instruments` + `get_history`)
on **2026-07-02**: **majors + a broad EM set** (both deliverable and non-deliverable), a tenor grid
from **overnight to 10 years**, and **daily** history back to **~1990** for the majors' front end.

> **This family does NOT use `TR.*` fields.** Like spot and swap curves, a forward point or
> outright is an **instrument addressed by RIC** and read as a **rate/price time series with
> `get_history`**. There is one RIC per (currency × tenor), and — unlike the swap-curve family —
> a **second, separate RIC** for the outright rate. See below.

## RIC anatomy — points and outright are different RICs, not different fields

Unlike a swap page (one RIC gives you rate + risk analytics together), FX forwards split the
**forward points** and the **outright forward rate** into two separate instrument pages:

| Concept | RIC pattern | Example (EUR/USD, 1M) | Confirmed value scale |
|---|---|---|---|
| **Forward points** (pips, can be ±) | `{CCY}{tenor}=` | `EUR1M=` | BID 14.19 / ASK 14.79 (pips) |
| **Outright forward rate** (same scale as spot) | `{CCY}{tenor}V=` | `EUR1MV=` | BID 1.139749 / ASK 1.139951 |
| Spot, for comparison | `{CCY}=` | `EUR=` | BID 1.1383 / ASK 1.1385 |

Document titles confirm the split: `EUR1M=` = *"...FX Forward Swap, FX Forward Swap, 1 Month,
REFINITIV"*; `EUR1MV=` = *"...FX Forward Outright, FX Forward Outright, 1 Month, REFINITIV
CALCULATED"*.

**Non-deliverable forwards (NDF)** — for currencies without full capital-account convertibility —
use a distinct infix on both sides of the same split:

| Concept | RIC pattern | Example (KRW, 1M) |
|---|---|---|
| NDF points | `{CCY}{tenor}NDF=` | `KRW1MNDF=` |
| NDF outright | `{CCY}{tenor}NDFOR=` | `KRW1MNDFOR=` |

**Contributor suffixes** mirror the swap-curve family: bare `=` (Refinitiv), `=R` (Refinitiv
Calculated), `=RFB` (Refinitiv Blended Composite), `=X` (Refinitiv Snapshot), `=FMD` (Fenics),
`=ICAP`, `=TTKL`/`=PYNY`/`=TPBR` (Tullett Prebon), `=D3` (Dealing 3000 Traded), plus dozens of
single-bank pages (`=COBA`, `=BARL`, `=BAFX`, `=LBWX`, `=LOYL`, …). Fenics-contributed outright
pages use `OR=` instead of `V=` (e.g. `EUR1MOR=FMD`). Reciprocal RICs also exist (`USDEUR1M=R`
quotes the same swap from the other currency's side) — check which currency's pips you're reading.

## Tenor grid (confirmed live for EUR/USD)

| Tenor | RIC token | Status |
|---|---|---|
| Overnight | `ON` | ✅ `EURON=` |
| Tomorrow-next | `TN` | ✅ `EURTN=` |
| **Spot week (~7 days)** | `SW` | ✅ `EURSW=` — **not** `1W` |
| 1 week (literal) | `1W` | ❌ `EUR1W=` fails on the composite (only some bank-contributor pages use "1W", e.g. `EUR1W=NXIP`) |
| 2 / 3 weeks | `2W`, `3W` | ✅ both resolve |
| 1–9 months | `1M`,`2M`,`3M`,`4M`,`5M`,`6M`,`9M` | ✅ all resolve |
| 1, 2, 3, 5, 7, 10 years | `1Y`,`2Y`,`3Y`,`5Y`,`7Y`,`10Y` | ✅ all resolve |

4Y/6Y/8Y/9Y and beyond-10Y were **not tested live** — don't assume they exist; probe before
building a panel that needs them.

**Gotcha, analogous to the swap-curve "chain root" problem:** a literal `1W` token fails on the
REFINITIV composite. Use `SW` for the shortest (~7-day) tenor.

## Currency coverage

**Majors — all deliverable, standard `{CCY}{tenor}=` pattern vs. USD:** EUR, GBP, JPY, CHF, AUD,
NZD, CAD — all confirmed resolving at 1M.

**EM — deliverable forwards** (contrary to the folk assumption that "EM = NDF"):

| Currency | Points RIC | Outright RIC |
|---|---|---|
| MXN | `MXN1M=` | `MXN1MV=` |
| ZAR | `ZAR1M=` | `ZAR1MV=` |
| TRY | `TRY1M=` | `TRY1MV=` |
| CNH (offshore yuan) | `CNH1M=` | — |

**EM — non-deliverable forwards** (distinct `NDF`/`NDFOR` infix):

| Currency | Points RIC | Outright RIC |
|---|---|---|
| KRW | `KRW1MNDF=` | `KRW1MNDFOR=` |
| INR | `INR1MNDF=` | `INR1MNDFOR=` |
| BRL | `BRL1MNDF=` | `BRL1MNDFOR=` |
| CNY (onshore) | `CNY1MNDF=` | `CNY1MNDFOR=` |
| IDR | `IDR1MNDF=` | `IDR1MNDFOR=` |

Document titles confirm the classification (e.g. `KRW1MNDF=` = *"US Dollar/Korean Won 1 Month FX
Non-Deliverable Forward, ... REFINITIV"*), and the search-property catalog carries a dedicated
`RCSAssetCategoryLeaf = "FX Non-Deliverable Forward"` facet.

## Fields returned by `get_history`

**Deliverable forward-points page** (e.g. `EUR1M=`) — **25 columns**:

| Field | Meaning |
|---|---|
| `MID_PRICE` / `BID` / `ASK` | Forward points (pips) — can be negative |
| `OPEN_BID` / `OPEN_ASK` | Session-open bid/ask points |
| `BID_HIGH_1` / `BID_LOW_1` / `ASK_HIGH_1` / `ASK_LOW_1` | Intraday high/low |
| `NUM_BIDS` | Bid-tick count |
| `ASIAOP_BID`/`ASIAHI_BID`/`ASIALO_BID`/`ASIACL_BID`, `EUROP_BID`/…, `AMEROP_BID`/… | Session-level (Asia/Europe/Americas) bid OHLC |
| `DAYS_MAT` | Days to maturity |
| `MATUR_DATE` | Settlement/maturity date |
| `START_DT` | Value date |

**Deliverable outright page** (e.g. `EUR1MV=`) — only **10 columns**, a stripped-down subset:
`BID, ASK, BID_HIGH_1, BID_LOW_1, OPEN_BID, MID_PRICE, ASK_LOW_1, ASK_HIGH_1, OPEN_ASK` — **no**
session breakdown, **no** `DAYS_MAT`/`MATUR_DATE`/`START_DT`. If you need maturity metadata
alongside an outright price, pull it from the points RIC and join.

**NDF points page** (e.g. `KRW1MNDF=`) — same 25-field set **plus `FIX_DATE`** (the NDF fixing
date), 26 columns.

**NDF outright page** (e.g. `KRW1MNDFOR=`) — **keeps the full 26-column set including
`FIX_DATE`** — unlike the deliverable-outright page, which is thin. This asymmetry (NDF outright
rich, deliverable outright thin) is easy to miss.

## Historical depth (verified via yearly-interval probes)

| Instrument | First data observed | Notes |
|---|---|---|
| `EUR1M=` (points) | **1990** | Empty for 1970–1985 queries (clean empty, not an error) |
| `EUR1MV=` (outright) | **1990** | Tracks true EUR/USD spot history pre-1999 via synthetic backfill, same D-mark stitching noted for spot and swap curves |
| `GBP1M=` (points) | **1982**, but **bid-only until ~1990** | `ASK`/`OPEN_ASK` null 1982–1989; two-sided quoting starts ~1990 |
| `EURON=` (overnight points) | **~1992**, two-sided | Front end has deep history — unlike swap OIS curves, which are structurally short |
| `EUR10Y=` (points) | `DAYS_MAT` from 2000, real BID/ASK/MID from **2002** | Long end starts materially later than the front end — same "wings fill in later" pattern as the swap-curve tenor grid |
| `TRY1M=` (deliverable points) | present by **1995** | |
| `INR1MNDF=` | usable from **2006** | **Scale jump ~2012**: points run ~0.05–0.5 in 2006–2011, then jump to ~20–40 from 2012 — a quoting-convention change, not a data error; inspect before comparing magnitudes across the full history |
| `KRW1MNDF=` | data only from **2011** | A 1995–2010 yearly query returns completely empty despite the RIC resolving fine for current dates |

**Frequency:** daily (business days); `interval` also accepts weekly/monthly/quarterly/yearly
(yearly aggregation adds `MID_OPEN`/`MID_HIGH`/`MID_LOW` columns).

## Access patterns

**One tenor point, points and outright together:**

```python
import lseg.data as ld
ld.open_session()
points   = ld.get_history("EUR1M=",  fields=["MID_PRICE"], start="2000-01-01", end="2026-07-01")
outright = ld.get_history("EUR1MV=", fields=["MID_PRICE"], start="2000-01-01", end="2026-07-01")
ld.close_session()
```

**A whole forward curve** — hold the currency, iterate the tenor, one RIC per call:

```python
tenors = ["ON","TN","SW","2W","3W","1M","2M","3M","6M","9M","1Y","2Y","3Y","5Y","10Y"]
curve = {t: ld.get_history(f"EUR{t}=", fields=["MID_PRICE"],
                            start="2024-06-28", end="2024-06-28")
         for t in tenors}
```

> **Multi-RIC bug (same as spot and swap curves).** Passing several forward RICs in one
> `get_history` `universe` list errors (`keys must be str, int, float, bool or None, not tuple`).
> Query one RIC at a time.

**An EM currency, choosing deliverable vs. NDF correctly:**

```python
# MXN is deliverable — use the plain forward
mxn_pts = ld.get_history("MXN1M=", fields=["MID_PRICE"], start="2020-01-01", end="2026-07-01")

# KRW is non-deliverable — use the NDF family, not the plain forward
krw_pts = ld.get_history("KRW1MNDF=", fields=["MID_PRICE"], start="2020-01-01", end="2026-07-01")
```

## Notes / gotchas

- **Points ≠ outright is a different RIC**, not a field choice on one RIC — `{CCY}{tenor}=`
  (points) vs. `{CCY}{tenor}V=` (outright); NDF equivalents are `{CCY}{tenor}NDF=` /
  `{CCY}{tenor}NDFOR=`.
- **`1W` fails on the composite; use `SW`** for the shortest weekly tenor.
- **EM currencies aren't uniformly NDF.** MXN, ZAR, TRY, and offshore CNH are carried as
  deliverable; only KRW, INR, BRL, onshore CNY, IDR (and similar capital-controlled currencies) use
  the dedicated NDF family. Check `RCSAssetCategoryLeaf` if unsure which applies to a new currency.
- **Deliverable-outright pages are field-poor** (no maturity/session data); NDF-outright pages are
  field-rich (keep `FIX_DATE` and the full session breakdown) — an asymmetry across the two
  families worth remembering.
- **Silent scale shifts within one RIC's own history** occur (e.g. INR NDF ~2012) — eyeball the
  full time series before comparing magnitudes across years.
- **Bid-only early history** on some majors (`GBP1M=` pre-1990) — spread/ask-side analysis isn't
  possible before two-sided quoting began.
- **Contributor proliferation** mirrors the swap-curve family — pick one composite consistently and
  expect the same entitlement-denial pattern on named-contributor pages.
- **Long-end forward-point magnitudes get large** (e.g. EUR 10Y points ~1600–1715, i.e. 0.16–0.17
  added to spot) — correct given a decade of compounded rate differential, not a data error.
- **Related family:** spot is documented in [fx-spot.md](fx-spot.md); implied-volatility surfaces
  in [fx-options.md](fx-options.md).
