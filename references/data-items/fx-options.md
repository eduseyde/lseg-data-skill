# FX Options & Implied Volatility (RIC-addressed, `get_history`)

Implied-volatility surfaces for the OTC FX options market — ATM vol, risk reversals, butterflies,
and a full delta/strike smile — plus a pointer to exchange-listed FX option chains. Coverage was
enumerated live from the MCP (`search_instruments` + `get_history`) on **2026-07-02**:
**G10 + a broad EM set**, deltas from **10 to 45** (calculated family) or **10/25** (market
convention), tenors from **overnight to 10 years**, and **daily** history back to **1995** for the
deepest pairs.

> **This family does NOT use `TR.*` fields.** As with spot, forwards, and swap curves, an FX
> volatility quote is an **instrument addressed by RIC** and read as a **time series with
> `get_history`**. There is no separate "FX Options" search category — everything here sits under
> `SearchAllCategory = 'FX & Money'`; free-text search is the reliable discovery path.

## Two parallel RIC families

LSEG carries FX options data in two genuinely different families — pick the one that matches what
you need, they are not interchangeable:

| Family | What it gives you | Contributor |
|---|---|---|
| **A — market-convention broker composite** | ATM vol, 25-delta and 10-delta **risk reversal (RR)** and **butterfly (BF)** — the way vol traders actually quote | bare `=` (REFINITIV composite) |
| **B — calculated smile surface** | A full call/put **delta grid (10–45)** with **strike and premium**, not just a spread convention | `=R` (REFINITIV CALCULATED) |

Family A is the market-quoted spread convention (RR/BF are not themselves tradeable instruments).
Family B is what you'd use to reconstruct an actual executable smile with strikes and premiums.

## RIC anatomy

**Family A:** `{CCY}{TENOR}{TYPE}[DELTA]=`

| Chunk | Meaning | Observed values |
|---|---|---|
| `CCY` | Currency-pair stem (base/quote convention below) | `EUR`, `GBP`, `JPY`, `CHF`, `AUD`, `BRL`, `MXN`, `ZAR`, `TRY`, `CNH`, `CNY`, `INR`, plus crosses (`EUAU`, `EUCH`, `EUBR`, `EUTR`, `GBPAUD`, `GBPNZD`) |
| `TENOR` | `ON`, `SW`, `1M`,`2M`,`3M`,`6M`,`9M`,`1Y`,`2Y`,`3Y`,`5Y`,`10Y` | confirmed for EUR; **4Y, 7Y, 8Y absent**, nothing past 10Y |
| `TYPE` | `O` = ATM option; `RR` = 25-delta risk reversal; `BF` = 25-delta butterfly; `R10`/`B10` = 10-delta RR/BF | `EUR1MO=`, `EUR1MRR=`, `EUR1MBF=`, `EUR1MR10=`, `EUR1MB10=` |

Worked examples (all observed live, 2026-06-25 to 07-01):

| RIC | Decodes as | Sample MID_PRICE |
|---|---|---|
| `EUR1MO=` | EUR/USD 1-month ATM implied vol | 5.81% |
| `EUR10YO=` | EUR/USD 10-year ATM implied vol | 7.55% |
| `EUR1MRR=` | EUR/USD 1-month 25-delta risk reversal | −0.663 (vol pts) |
| `EUR1MBF=` | EUR/USD 1-month 25-delta butterfly | 0.143 (vol pts) |
| `JPY1MRR=` | **USD/JPY** 1-month 25-delta risk reversal | — |
| `CHF1MRR=` | **USD/CHF** 1-month 25-delta risk reversal | — |
| `EURONO=` | EUR/USD overnight ATM vol | 5.5–10.5% (noisy, expected for O/N) |

**Family B:** `{CCY}{DELTA}{C|P}{TENOR}=R`

| Chunk | Meaning | Observed values |
|---|---|---|
| `DELTA` | Put/call delta, whole numbers | **10, 15, 20, 25, 30, 35, 40, 45** — no 5-delta, no ATM/50-delta point (ATM lives in Family A) |
| `C`/`P` | Call or put | |
| `TENOR` | Same tokens as Family A | confirmed at 1M, 5M, 5Y, 10Y |

Examples: `EUR25C1M=R` (EUR/USD 1M 25-delta call), `EUR10P5Y=R` (5Y 10-delta put),
`EUR10C10Y=R` (10Y 10-delta call, MID_PRICE 8.15–8.4%).

There is also a chain root `0#EURVOLSURF` ("Euro FX Volatility Surfaces") that aggregates the
whole Family-B grid on the terminal — not directly usable with `get_history` (no chain-expansion
in this MCP, same limitation as the swap-curve family's chain roots).

## Delta / strike grid

- **Family A:** only **10-delta and 25-delta** RR/BF are quoted. No 5-delta.
- **Family B:** a genuinely granular smile — **10, 15, 20, 25, 30, 35, 40, 45** delta, both call
  and put (16 points per tenor), plus the ATM point from Family A. A targeted search for 5-delta
  instruments returned zero results — 10 is the wing limit.

## Tenor grid (confirmed live for EUR/USD ATM)

| Works | Fails (`The universe is not found`) |
|---|---|
| ON, SW(1W), 1M, 2M, 3M, 6M, 9M, 1Y, 2Y, 3Y, 5Y, **10Y** | **4Y, 7Y, 8Y**, and anything past 10Y (15Y/20Y/30Y all failed) |

This is a genuinely irregular grid, not "annual to 10Y then longer" — confirm any tenor you need
with a direct probe before building a panel. RR/BF share the same tenor tokens (`EUR1MRR=`,
`EUR5YRR=`, `EUR5YR10=` all confirmed).

## Currency-pair coverage and RIC-stem convention

The single-currency stem follows **real FX quoting convention**, same split as spot:

| Stem | Actual pair | Base |
|---|---|---|
| `EUR`, `GBP`, `AUD` | EUR/USD, GBP/USD, AUD/USD | foreign currency |
| `JPY`, `CHF` | **USD/JPY**, **USD/CHF** | USD |
| `BRL`, `MXN`, `ZAR`, `TRY`, `CNH`, `CNY`, `INR` | USD/XXX | USD |

**Crosses** (non-USD pairs) mostly use 2-letter+2-letter concatenation (`EUAU=` = EUR/AUD,
`EUCH=` = EUR/CHF, `EUBR=` = EUR/BRL, `EUTR=` = EUR/TRY), **but GBP crosses break the pattern** and
use full 3-letter+3-letter (`GBPAUD1MO=`, `GBPNZD1MO=`). Don't assume the abbreviation length —
resolve via `search_instruments`.

**EM coverage is real, not token.** BRL, MXN, ZAR, TRY, CNH, CNY (onshore, at least 1M), and INR
all have a **full tenor ladder with both 10-delta and 25-delta RR** confirmed live (ON through
1Y, and BRL/ZAR/CHF/JPY out to 2Y–5Y) — this is not a G10-only surface.

## Fields returned by `get_history`

**Family A (ATM/RR/BF, bare `=`) — 10 columns:**

| Field | Meaning |
|---|---|
| `MID_PRICE` | **The vol number itself, in %** (or the RR/BF spread, in vol points) |
| `BID` / `ASK` | Two-way quoted vol |
| `OPEN_BID` / `OPEN_ASK` | Session-open bid/ask |
| `BID_HIGH_1` / `BID_LOW_1` / `ASK_HIGH_1` / `ASK_LOW_1` | Intraday high/low of bid/ask vol |
| `MATUR_DATE` | The expiry date this tenor point corresponds to |

**Family B (calculated surface, `=R`) — 11 columns, richer:**

| Field | Meaning |
|---|---|
| `MID_PRICE`, `BID`, `ASK` | Vol, same as Family A |
| `MID_STRIKE` / `BID_STRIKE` / `ASK_STRIKE` | **The actual strike** implied by that delta point |
| `MID_PREM` / `BID_PREM` / `ASK_PREM` | **Option premium** (e.g. 0.0028 = 28 pips for EUR/USD 1M 25-delta call) |
| `MATUR_DATE`, `DELIV_DATE` | Expiry and settlement/delivery date |

The strike/premium fields are the practical reason to reach for Family B over Family A whenever
you need an executable smile rather than a market-convention quote.

**Sign convention (observed):** `EUR1MRR=` printed negative (−0.66 to −0.40 across
2026-06-25/07-01), `EUR1MBF=` printed positive (0.11–0.14) — consistent with standard convention
(a butterfly is always a positive convexity charge; RR sign encodes put-vs-call skew direction and
can flip).

## Historical depth (verified live, 1-month ATM point unless noted)

| Currency | Start date | Notes |
|---|---|---|
| GBP/USD, USD/JPY | **1995-01-06** | Deepest coverage found; both start the same week |
| EUR/USD | **1999-01-04** | Cannot predate this — the euro didn't exist before 1999; pre-1999 queries return a clean empty result, not an error |
| USD/ZAR | **2002-02-07** | |
| USD/MXN | **2003-05-21** | |
| USD/TRY | **2004-06-08** | |
| USD/CNH (offshore) | **2012-11-01** | Tracks the actual emergence of the offshore CNH market |

**Frequency:** daily (business days); `interval` also accepts weekly/monthly/quarterly/yearly.

## Other FX-options instruments (noted, not the primary recommendation)

- **Exchange-listed (CME) FX options** exist as separate chains from the OTC vol surface above:
  `0#EUUN26+` (CME premium-quoted European-style EUR/USD monthly chain), `0#EUUQ26+`, `0#EUUZ26+`
  (other expiry months), weekly variants (`0#MO1WN26+`, `0#WE4WH24+`), and cross-currency listed
  options (`0#RF+` = EUR/CHF, `0#RY+` = EUR/JPY). These are genuine exchange-traded futures
  options, distinct from everything above. The MCP has no chain-expansion tool, so individual
  contract RICs would need to be resolved separately — out of scope for a discount-curve/vol-surface
  workflow, flagged here for completeness only.
- **Legacy/OPRA vol proxies** (`GBPATMIV.U`, `BPATMIV`, `LPATMIV`) surfaced in search but belong to
  an older, separate product line — not recommended over the two families above.
- `TR.IMPLIEDVOLATILITY` / `IMP_VOLT` in the general field catalog are **generic equity/listed-
  option fields for `get_data`**, not applicable to this RIC family.

## Access patterns

**ATM vol term structure for one pair:**

```python
import lseg.data as ld
ld.open_session()
tenors = ["ON","SW","1M","2M","3M","6M","9M","1Y","2Y","3Y","5Y","10Y"]
atm = {t: ld.get_history(f"EUR{t}O=", fields=["MID_PRICE"],
                          start="2024-06-28", end="2024-06-28")
       for t in tenors}
ld.close_session()
```

**Market-convention smile inputs (ATM + RR + BF) at one tenor:**

```python
atm_1m = ld.get_history("EUR1MO=",  fields=["MID_PRICE"])
rr_1m  = ld.get_history("EUR1MRR=", fields=["MID_PRICE"])
bf_1m  = ld.get_history("EUR1MBF=", fields=["MID_PRICE"])
```

**An executable delta point with strike and premium:**

```python
call_25d_1m = ld.get_history("EUR25C1M=R",
                              fields=["MID_PRICE", "MID_STRIKE", "MID_PREM"])
```

> **Multi-RIC bug (same as spot, forwards, swap curves).** Passing several vol RICs in one
> `get_history` `universe` list errors. Query one RIC at a time and assemble the surface yourself.

## Notes / gotchas

- **Tenor-less root fails outright** (`EURVOL=` → `The universe is not found`) — always give a
  tenor token, same failure mode as swap curves.
- **Missing tenors fail loudly, not silently** — `EUR4YO=`/`EUR7YO=`/`EUR8YO=` and anything past
  10Y return an explicit error, which makes gaps easy to detect but means you cannot assume a
  regular annual grid; verify each tenor.
- **Pre-instrument-existence dates return a clean empty result, not an error** (e.g. `EUR1MO=`
  before 1999) — don't mistake this for a broken RIC.
- **Currency-stem convention is not "always USD-quote."** `JPY`/`CHF` stems mean USD is the base;
  `EUR`/`GBP`/`AUD` stems mean the foreign currency is the base — mirrors spot exactly, and will
  silently produce an inverted series if assumed wrong.
- **Cross-pair abbreviation length is inconsistent** (2+2 for most, 3+3 for GBP crosses) — resolve
  via `search_instruments`, don't guess the stem.
- **Two families, easy to conflate.** Family A gives a market-convention RR/BF *spread*; Family B
  gives an actual call/put point with strike and premium. Different field sets, not interchangeable.
- **Related family:** spot is documented in [fx-spot.md](fx-spot.md); forward points and outrights
  in [fx-forwards.md](fx-forwards.md).
