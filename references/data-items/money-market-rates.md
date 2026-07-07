# Money-Market, Reference & Policy Rates (RIC-addressed, `get_history`)

Overnight near-risk-free rates (RFRs), term interbank fixings, and central-bank **policy
rates** — the very front end of every yield curve. Like swaps and FX, these are **instruments
addressed by RIC and read as a time series with `get_history`**, not `TR.*` field codes. Coverage
below was enumerated live on **2026-07-03**: the major RFRs and policy rates across USD, EUR, GBP,
JPY, CHF, CAD, AUD, plus EURIBOR term rates, all at **daily** frequency, with history reaching from
the late 1990s (legacy term/overnight rates) to just 2018–2020 for the newest RFRs.

> **This family does NOT use `TR.*` fields.** A benchmark rate is *not* a `get_data` field code —
> it is an **instrument addressed by RIC**, read with `get_history`. You do not "select a field";
> you pick the right RIC and pull its value column. The **value column is not always the same** —
> it is `FIXING_1` for market fixings, `VALUE` for the economic-indicator policy series, and
> `TRDPRC_1` for the central-bank rate pages (see "Fields returned"). All are quoted **in percent**.

> **Entitlement / access caveat.** Central-bank and RFR pages sourced directly from official
> administrators (Federal Reserve, ECB, Bank of England, SIX, Bank of Japan, Bank of Canada) are
> broadly entitled and returned cleanly here. **ICE LIBOR fixings are denied on this account**
> (`User has no permission` / `The universe is not found`) — LIBOR RICs below are therefore
> documented but marked **unvalidated**. A denial is a licensing gap, not a bad query.

## RIC shapes you will meet

Unlike the tidy swap grammar (`{CCY}{conv}{tenor}=`), money-market benchmarks use **heterogeneous
RIC conventions** depending on who administers and distributes them. There is no single template —
discover the exact RIC with `search_instruments` (short queries work best; long phrases return
nothing), then reuse it. The shapes seen live:

| Shape | Example | What it is |
|---|---|---|
| bare `=` | `USDSOFR=`, `EUROSTR=`, `CORRA=`, `AUCASH=` | RFR / cash-rate fixing, REFINITIV composite |
| `=`+source | `SONIAOSR=` (BoE), `JPONMU=RR` (BoJ), `GBBASE=BOEL` (BoE), `AUCASHT=RBAA` (RBA) | fixing / policy page from a named administrator |
| `.`-prefix | `.SOFR`, `.TONA` | **compounded index** (an accruing level, base 100) |
| `.S` suffix | `SARON.S` | SIX Swiss Exchange domestic-rate page |
| `AVG=` | `SOFR1MAVG=`, `SOFR3MAVG=` | backward-looking compounded **average** rate |
| `{CCY}IBOR{tenor}D=` | `EURIBOR3MD=`, `EURIBOR1YD=` | term interbank offered rate fixing |
| `a`-prefix | `aXZECB`, `aJPMPRPB`, `aCAONTAR` | economic-indicator **policy-rate step series** (field `VALUE`) |

## 1. Overnight near-risk-free rates (RFR fixings)

The successor rates that replaced LIBOR/EONIA for discounting and floating-rate contracts. Each is
a **daily overnight fixing in percent**, carried in `FIXING_1`. All validated live:

| Rate | Ccy | RIC | Administrator | Recent fixing | Extra columns |
|---|---|---|---|---|---|
| **SOFR** (Secured Overnight Financing Rate) | USD | `USDSOFR=` | NY Fed | 3.66 | `ACVOL_UNS` (≈$3.3tn daily volume) |
| **€STR / ESTER** (Euro Short-Term Rate) | EUR | `EUROSTR=` | ECB | 2.183 | `ACVOL_UNS`, `TP_MP_AVPC`, `NO_MPANT`, `NUM_MOVES` (panel-transparency stats) |
| **SONIA** (Sterling Overnight Index Average) | GBP | `SONIAOSR=` | Bank of England | 3.731 | `ACVOL_UNS` (≈£50bn); `HIGH_1`/`LOW_1` present but null |
| **SARON** (Swiss Average Rate Overnight) | CHF | `SARON.S` | SIX | −0.037 | `HIGH_1`, `LOW_1`, `OPEN_PRC`, `REF_PRICE`, `REF_PRC_2` |
| **CORRA** (Canadian Overnight Repo Rate Average) | CAD | `CORRA=` | Bank of Canada | 2.34 | `ACVOL_UNS` |
| **TONA / TONAR** (Tokyo Overnight Average Rate) | JPY | `JPONMU=RR` | Bank of Japan | 0.977 | `HIGH_1`, `LOW_1` (intraday call-rate range) |
| **AONIA** (AUD Overnight Cash Rate) | AUD | `AUCASH=` | RBA (REFINITIV composite) | 4.35 | value in `TRDPRC_1`, not `FIXING_1` |

- **SOFR, €STR and SONIA are secured/unsecured near-risk-free benchmarks** underpinning the modern
  OIS discount curves; SARON is repo-based; CORRA is repo-based; TONA is the uncollateralised
  overnight call rate. AONIA sits essentially **on** the RBA cash-rate target (hence the flat 4.35).
- **Rates can be negative** — SARON printed around −0.04 to −0.75 across 2015–2022, TONA around
  −0.10 through the BoJ's negative-rate era (2016 to March 2024). This is expected, not an error.

## 2. Compounded indices and averages

For calculating realised compounded interest over a period without re-compounding daily fixings
yourself. Two flavours, both carried in `FIXING_1`:

| Instrument | Ccy | RIC | What `FIXING_1` is | Validated |
|---|---|---|---|---|
| **SOFR Index** | USD | `.SOFR` | An **accruing index level** (base 100), not a rate (≈100.70) | Yes — but starts ~2020, not 2018 (see depth) |
| **SOFR 30-day Average** | USD | `SOFR1MAVG=` | Backward compounded **rate %** (≈3.632) | Yes |
| **SOFR 90-day Average** | USD | `SOFR3MAVG=` | Backward compounded **rate %** (≈3.635) | Yes |
| **SOFR 180-day Average** | USD | `SOFR6MAVG=` | Backward compounded **rate %** | Listed by search (same NY Fed family) |
| **TONA Index** | JPY | `.TONA` | Compounded index level | **Caution** — inconsistent scaling (see gotchas) |

- **Index vs rate.** `.SOFR` returns a *level* (~100.7), not a percent — divide successive levels to
  recover the compounded rate over any window. `SOFR{1M,3M,6M}AVG=` already give the *rate*.
- Compounded **indices/averages for €STR and SONIA** are published by the ECB/BoE and exposed as
  "realised risk-free rate" chains (`0#SONIAOSRRR=R`, and the €STR equivalent). These are chain
  roots; the MCP-style harness cannot expand chains, so a single directly-pullable index RIC for
  €STR/SONIA was **not resolved this session** — build the compound yourself from the daily fixing.

## 3. Term reference rates (EURIBOR, Term SOFR, TIBOR, legacy LIBOR)

Forward-looking term fixings. EURIBOR validated across the full tenor set (value in `FIXING_1`, %):

| Tenor | EURIBOR RIC | Recent fixing |
|---|---|---|
| 1 Month | `EURIBOR1MD=` | 2.179 |
| 3 Month | `EURIBOR3MD=` | (workhorse) |
| 6 Month | `EURIBOR6MD=` | 2.596 |
| 12 Month | `EURIBOR1YD=` | 2.764 |

- **EURIBOR never ceased** and remains the euro term benchmark (reformed to a hybrid methodology in
  2019–2022). History runs continuously from **early 1999** (a few stitched points in late 1998).
- **Term SOFR** (CME forward-looking SOFR): the candidate RIC `USDTSFR3M=` did **not resolve** on
  this account — **unvalidated** (likely a different RIC convention or a CME entitlement).
- **TIBOR** (Japanese Yen / Euroyen): the fixing panel `DIBJP=` ("TIBOR Fixing 1100 JST") and the
  chain `0#TIBORJPYZ=R` exist in search, but neither the bare page nor a `DIBJP3M=`-style tenor RIC
  returned a series — **tenor RIC unvalidated** this session.
- **LIBOR (ceased).** `USDLIBOR=`, `USD3MFSR=` and the ICE fixing chain `0#USDFSR=` are **entitlement-
  denied here** (`User has no permission`), so they are **unvalidated**. Even where entitled, LIBOR
  has **stopped fixing** (cessation dates in gotchas) — use the successor RFRs instead.

## 4. Central-bank policy rates

Two access routes. Most policy rates are exposed as **economic-indicator step series** with an
`a`-prefix RIC and their value in a `VALUE` column; a few have clean central-bank "domestic interest
rate" pages carrying `TRDPRC_1`. **All below validated live.**

| Central bank / rate | RIC | Value field | Behaviour |
|---|---|---|---|
| **Fed funds target** (upper bound of range) | `aUSFEDFUNDT` | `VALUE` | prints on FOMC dates (3.75) |
| **ECB Main Refinancing (MRO)** | `aXZECB` | `VALUE` | prints on ECB dates (2.40) |
| **ECB Deposit Facility** | `aXZDEPF` | `VALUE` | step series (2.25) |
| **ECB Marginal Lending Facility** | `aXZMLENF` | `VALUE` | step series (2.65) |
| **Bank of England — Bank Rate** | `GBBASE=BOEL` | `TRDPRC_1` | carried daily (3.75) |
| **Bank of Japan — Policy Rate Balance** | `aJPMPRPB` | `VALUE` | prints on BoJ meetings (−0.1 → +1.0 across NIRP exit) |
| **SNB — Policy Rate** | `aCH3LIMBORM` | `VALUE` | prints on SNB meetings (1.5 → 0.0) |
| **Bank of Canada — Overnight Target** | `aCAONTAR` | `VALUE` | step series (5.0 → 2.25) |
| **RBA — Target Cash Rate** | `AUCASHT=RBAA` | `TRDPRC_1` | prints on RBA changes (4.10 → 4.35) |

- The `a`-prefixed series and `AUCASHT=RBAA` are **step series: they only print on meeting / change
  dates**, so a narrow window can return *nothing*. Pull a **wide window and forward-fill** to get a
  daily level. (`GBBASE=BOEL` and `AUCASH=` are carried on every business day.)
- The ECB corridor is internally consistent in the data: on the same day, Deposit 2.25 / MRO 2.40 /
  Marginal Lending 2.65 (MRO = deposit + 15bp; lending = deposit + 40bp).
- **Fed lower bound** was not resolved to its own RIC; derive it as `aUSFEDFUNDT − 0.25`, or discover
  via `search_instruments("Federal Funds Target Rate")` (returns the Datastream `aUS...` family).
- **Discover any other country's policy rate** the same way: `search_instruments("<Country> policy
  rate")` surfaces its `a`-prefixed "Policy Rates … Interest Rates, Daily" RIC.

## Fields returned by `get_history`

The **value lives in a different column per family** — this is the single most important gotcha:

| Column | Appears on | Meaning |
|---|---|---|
| **`FIXING_1`** | RFR fixings, EURIBOR, SOFR averages, `.SOFR`/`.TONA` indices | **The rate, in %** (or the index level for `.`-prefixed indices). The value you want. |
| **`VALUE`** | `a`-prefixed policy-rate series | The policy rate, in %. Step series. |
| **`TRDPRC_1`** | `GBBASE=BOEL`, `AUCASH=`, `AUCASHT=RBAA` | The rate, in %, on central-bank "domestic interest rate" pages. |
| `ACVOL_UNS` | SOFR, €STR, SONIA, CORRA | Underlying **transaction volume** for the fixing (in local ccy notional). |
| `HIGH_1` / `LOW_1` | SARON, TONA | Intraday high/low of the overnight rate. |
| `OPEN_PRC`, `REF_PRICE`, `REF_PRC_2` | SARON | Session open / reference prints. |
| `TP_MP_AVPC`, `NO_MPANT`, `NUM_MOVES` | €STR | ECB panel-transparency stats (share of volume, active banks, transactions). |

- **Always inspect the returned columns.** An invalid/unentitled field is **silently dropped**, and
  requesting `fields="FIXING_1"` on a `VALUE`/`TRDPRC_1` page returns the value under a differently
  named column (or, for multi-RIC calls, under the RIC name — see access patterns).
- **Fixing vs publication.** The date on each row is the **fixing (reference) date**; the number is
  **published the next business day** (SOFR ~08:00 ET T+1; €STR 08:00 CET T+1; SONIA ~09:00 London
  T+1; CORRA late-morning ET T+1; TONA next BoJ business day; SARON is published intraday same day by
  SIX). A query up to "today" typically **misses the latest fixing until T+1**.

## Historical depth (by tier)

All starts below were **verified live** by pulling early windows:

| Tier | Series | Starts around | Notes |
|---|---|---|---|
| **Deepest (legacy term/overnight)** | SONIA `SONIAOSR=` **1997**; EURIBOR `EURIBOR3MD=` **1999** (stitched late-1998); SARON `SARON.S` **1999**; CORRA `CORRA=` **2000** | **late 1990s** | These benchmarks pre-date their "reform": SONIA/SARON/CORRA levels are back-cast to the late 1990s; EURIBOR runs from EMU launch. |
| **New RFR fixings** | SOFR `USDSOFR=` **2018-04-02**; €STR `EUROSTR=` **2019-10-02** | **2018–2019** | Structurally short — each starts at the benchmark's launch. |
| **Compounded indices** | SOFR Index `.SOFR` **~2020** | **2020** | The *index* starts later than the *fixing*: `.SOFR` is **empty in April 2018** (NY Fed first published the SOFR Index in 2020). |
| **Policy rates** | `a`-prefixed step series | decades (sparse) | Only change dates print; the effective history is long but the row count is small. Forward-fill. |

**Frequency:** daily (business days). `interval` also accepts `weekly`/`monthly`/`quarterly`/`yearly`.
Intraday bars are shallow (fine for the front end of a curve, a limit only for intraday studies).

## Relationship to OIS / swap curves

These overnight fixings are **the anchor of the modern discount curve**. The OIS/RFR swap family
documented in [swap-rates.md](swap-rates.md) is built *on top of* the rates here: `USDSROIS10Y=`
(SOFR OIS), `GBP10YOIS=` (SONIA OIS), `EUREST10Y=` (€STR OIS), `JPY10YOIS=` (TONA OIS) and
`CHF10YOIS=` (SARON OIS) all price the market's expected average of the corresponding overnight
fixing over their tenor. The very front point of any OIS curve **is** the overnight fixing in this
file. For the swap grid, tenor conventions, and cross-currency basis, see swap-rates.md — this file
covers only the underlying reference and policy fixings, not the derivatives layered on them.

## Access patterns

**1. One fixing, as a time series:**

```python
import lseg.data as ld
ld.open_session()
sofr = ld.get_history(
    universe="USDSOFR=",
    fields=["FIXING_1"],           # the overnight rate, in %
    start="2018-01-01", end="2026-07-01",
    interval="daily",
)
ld.close_session()
```

**2. Several fixings at once — multi-RIC WORKS here** (unlike the swap-curve RICs, which error on
multi-RIC calls). Pass a single value field and the columns come back **one per RIC** (wide format):

```python
df = ld.get_history(
    universe="USDSOFR=,SONIAOSR=,CORRA=",
    fields=["FIXING_1"],
    start="2020-01-01", end="2026-07-01",
)
# columns: Date, USDSOFR=, SONIAOSR=, CORRA=
```

**3. A policy rate — pull WIDE and forward-fill** (step series only print on change/meeting dates):

```python
ecb_depo = ld.get_history(
    universe="aXZDEPF",            # ECB Deposit Facility
    fields=["VALUE"],              # note: VALUE, not FIXING_1
    start="2000-01-01", end="2026-07-01",
)
ecb_depo = ecb_depo.asfreq("D").ffill()   # carry the level forward between meetings
```

**4. Discovery first.** RIC conventions here are irregular. Resolve with **short** `search_instruments`
queries (a benchmark name or a country + "policy rate"); long descriptive phrases return zero rows.

## Notes / gotchas

- **The value column differs by family** — `FIXING_1` (fixings/benchmarks), `VALUE` (`a`-prefixed
  policy series), `TRDPRC_1` (central-bank pages). Requesting the wrong one silently returns nothing
  useful. When in doubt, call with **no `fields`** first and read the columns.
- **Policy rates are step series.** The `a`-prefixed RICs and `AUCASHT=RBAA` print only on
  meeting/change dates — a narrow window can be empty. Always pull a wide window and forward-fill.
- **`.SOFR`/`.TONA` are index *levels*, not rates.** Divide successive levels to recover a compounded
  rate. Don't mix them with the `FIXING_1` *rate* of `USDSOFR=`.
- **`.TONA` scaling is inconsistent** in this feed — it returned an index level (~99.7 in 2024) but
  an anomalous ~1.25 in 2026 for the same RIC. Treat `.TONA` with caution; for the JPY overnight
  fixing use **`JPONMU=RR`** (the raw TONA/uncollateralised call rate), which is clean.
- **LIBOR cessation** (why these rates stop, and what replaced them):
  - GBP, EUR, CHF, JPY LIBOR (all tenors) and 1-week/2-month USD LIBOR: **ceased 31 Dec 2021**.
  - Overnight, 1M, 3M, 6M, 12M **USD LIBOR ceased 30 June 2023** (synthetic USD 1M/3M/6M ran to
    30 Sep 2024). Synthetic GBP 3M ran to end-March 2024. **EONIA ceased 3 Jan 2022.**
  - Successors: USD → **SOFR**, GBP → **SONIA**, CHF → **SARON**, JPY → **TONA**, EONIA → **€STR**.
    **EURIBOR is the exception — it continues** (reformed, not discontinued).
- **Simple vs compounded.** RFR-linked contracts use the *compounded* overnight rate in arrears (use
  the index/average RICs), whereas LIBOR/EURIBOR are *term* rates set in advance. Do not treat an
  overnight fixing as if it were a term rate.
- **Holidays return null.** CORRA does not fix on Canadian holidays (e.g. `CORRA=` is null on 1 July,
  Canada Day); each fixing follows its own currency's calendar, so multi-RIC panels have staggered
  gaps. Reindex to a common business-day calendar and handle nulls explicitly.
- **All values are percent** (e.g. `3.66` = 3.66%), never decimals — except the `.`-prefixed indices,
  which are levels (~100).
- **Entitlement drops are silent-ish.** LIBOR here returns an explicit `User has no permission`;
  other unentitled pages return `The universe is not found`. Either is a licensing/RIC issue, not a
  code bug — confirm the RIC with `search_instruments`.
- **Related families:** OIS/RFR swap curves and cross-currency basis → [swap-rates.md](swap-rates.md);
  government benchmark **bond** yields (`=RR` RICs, `MID_YLD_1`) → the benchmark-yield notes.
