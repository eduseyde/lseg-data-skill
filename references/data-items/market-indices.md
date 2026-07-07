# Market Indices & Barometers (RIC-addressed, `get_history`)

Cross-asset **market barometers and headline indices** — the dollar index, volatility gauges,
commodity indices, and equity benchmarks you use as risk-state variables and market context. This is
the `DXY / VIX / MOVE` family: a single number per market that summarises price, stress, or breadth.

The RICs below are **standard LSEG/Refinitiv index codes**. Each was probed live via `get_history` on
2026-07-07 (data through 2026-07-06) and carries an entitlement marker:

- **✅ live** — returned data on the reference account; a live level snapshot is shown as evidence.
- **◑ gated** — a genuine, widely-used LSEG index RIC that did **not** resolve on the reference
  account. LSEG data is **entitlement-based**, so these are expected to resolve on a subscription that
  licenses the relevant index (S&P DJI, CBOE, Nikkei, etc.). They are catalogued here because the code
  is real and useful — the `◑` is an account fact, not a statement that the series does not exist.

> **This family does NOT use `TR.*` fields.** Like the swap, FX, and sovereign-yield families, a
> market index is an **instrument addressed by RIC** and read as a **time series with `get_history`**.
> You do not "select a `TR.` field"; you pick the RIC and pull the level. The value lives in
> **`TRDPRC_1`** (the close/last). This is the single most important field in this file.

## How to address an index (RIC anatomy)

Index RICs are **dot-prefixed** mnemonics: `.DXY`, `.VIX`, `.MOVE`, `.FTSE`. There is no country/tenor
grammar as with `=RR` yields — each index is its own code, so the practical task is **knowing the
code**, which is what the tables below give you. To confirm a code (or find one not listed), search
rather than guess:

```python
ld.discovery.search(query="VSTOXX volatility index", view="SearchAll",
                    select="RIC, DocumentTitle")
```

### The value field: `TRDPRC_1`

A single-RIC `get_history` with no `fields` returns `TRDPRC_1` (level/close) plus `OPEN_PRC`,
`HIGH_1`, `LOW_1` where the index publishes them. **`TRDPRC_1` is the index level** — the number you
almost always want. Validated on `.DXY`: a bare call returns `TRDPRC_1` 100.85 with `OPEN_PRC` /
`HIGH_1` / `LOW_1` alongside.

> **Wide-frame quirk (identical to the sovereign-yields family).** When you pass **several RICs with
> one field**, LSEG returns a tidy **wide frame, one column per RIC**, but (i) relabels the columns by
> RIC and (ii) emits a harmless `"Requested fields not found: ['TRDPRC_1']"` warning — **the values
> ARE `TRDPRC_1`**, the label just moves to the RIC. Ask for **one field only** in the multi-RIC form;
> a single-RIC call can take a field list. Unentitled RICs come back as an **all-null column** (listed
> in a second warning), so a mixed batch never fails — you read off which codes populated.

## 1. Cross-asset volatility & risk gauges (the `DXY / VIX / MOVE` cluster)

The barometer set proper. On the reference account the dollar (`.DXY`), the Treasury-vol index
(`.MOVE`), and the European/Asian equity-vol indices resolve, while the **CBOE US volatility suite is
gated** — so on an unentitled account the VIX-equivalent you can pull from LSEG is **VSTOXX**. On a
CBOE-licensed account, `.VIX` and its relatives below resolve exactly the same way.

### Equity volatility

| Index | RIC | Measures | Status / live (2026-07-06) | History from |
|---|---|---|---|---|
| **CBOE VIX** | `.VIX` | S&P 500 30-day implied vol — the fear gauge | ◑ gated | — |
| CBOE VXN / RVX / VXD | `.VXN` · `.RVX` · `.VXD` | Nasdaq-100 / Russell-2000 / Dow implied vol | ◑ gated | — |
| CBOE VVIX | `.VVIX` | Vol-of-vol (VIX options) | ◑ gated | — |
| **CBOE SKEW** | `.SKEWX` | Tail/crash-risk pricing (OTM-put demand) | ◑ gated | — |
| VIX term structure | `.VIX9D` · `.VXV`/`.VIX3M` · `.VXMT` | 9-day / 3-month / 6-month VIX | ◑ gated | — |
| **VSTOXX (main)** | `.V2TX` | Euro Stoxx 50 30-day implied vol — Europe's VIX | ✅ 15.87 | **1999** |
| **VSTOXX term structure** | `.V6I1` … `.V6I8` | VSTOXX constant-maturity sub-indices (1m → ~24m) | ✅ V6I1 14.35 · V6I8 22.10 | **1999** |
| **Hang Seng Vol (VHSI)** | `.VHSI` | Hang Seng 30-day implied vol — HK/China | ✅ 23.02 | **2001** |
| **India NIFTY VIX** | `.NIFVIX` | NIFTY 50 implied vol (NSE India VIX) | ✅ 11.65 | **2008** |
| VDAX-NEW / VFTSE / VCAC | `.VDAXNEW` · `.VFTSE` · `.VCAC` | DAX / FTSE 100 / CAC 40 implied vol | ◑ gated | — |
| VSMI / VAEX | `.VSMI` · `.VAEX` | Swiss SMI / Dutch AEX implied vol | ◑ gated | — |
| Nikkei Vol / VKOSPI | `.JNIV` · `.VKOSPI` | Nikkei 225 / KOSPI 200 implied vol | ◑ gated | — |

**VSTOXX gives you a whole vol curve for free.** `.V2TX` is the rolling 30-day index; `.V6I1..V6I8` are
the maturity sub-indices, so the **VSTOXX term structure** (contango/backwardation — a clean
risk-appetite signal) is directly readable. Validated points on 2026-07-06: 1m 14.35, 2m 16.14,
3m 17.31, 4m 19.54, 6m 22.04, 8m 22.10 — a textbook upward-sloping (calm-regime) vol curve.

### Rate & commodity volatility

| Index | RIC | Measures | Status / live (2026-07-06) | History from |
|---|---|---|---|---|
| **ICE BofA MOVE** | `.MOVE` | US Treasury implied vol — the "bond VIX" | ✅ 65.76 | **2002** |
| CBOE Swap-Rate Vol (SRVIX) | `.SRVIX` | 1y10y swaption implied vol | ◑ gated | — |
| CBOE Treasury Vol (TYVIX) | `.TYVIX` | 10Y Treasury-future vol (discontinued 2020) | ◑ gated | — |
| CBOE TLT ETF Vol | `.VXTLT` | 20y+ Treasury-ETF implied vol | ◑ gated | — |
| CBOE Oil / Gold Vol | `.OVX` · `.GVZ` | Crude-oil / gold implied vol | ◑ gated | — |

For **currency-specific implied vol** (FX ATM / risk-reversal / butterfly surfaces — the FX analogue of
these indices) use the FX options family in [fx-options.md](fx-options.md), not an index RIC.

## 2. Currency indices

| Index | RIC | Notes | Status / live (2026-07-06) | History from |
|---|---|---|---|---|
| **ICE US Dollar Index (DXY)** | `.DXY` | USD vs 6 majors (EUR ~58%) — the dollar gauge | ✅ 100.85 | **1985** |
| Bloomberg Dollar Spot | `.BBDXY` | Trade-weighted, **EM-inclusive** (CNY, MXN) | ◑ gated | — |
| Bloomberg-JPM Asia Dollar | `.ADXY` | EM-Asia FX basket | ◑ gated | — |

For an EM-weighted or custom dollar index, you can also build one from FX spot
([fx-spot.md](fx-spot.md)); the Fed Broad Dollar and BIS effective exchange rates are the standard
non-LSEG alternatives.

## 3. Commodity indices

| Index | RIC | Notes | Status / live (2026-07-06) | History from |
|---|---|---|---|---|
| **Bloomberg Commodity (spot/ER)** | `.BCOM` | Diversified, capped-weight basket | ✅ 125.63 | **1991** |
| **Bloomberg Commodity Total Return** | `.BCOMTR` | Same basket, total return (roll + collateral) | ✅ 322.38 | **1991** |
| **CoreCommodity CRB (Refinitiv)** | `.TRCCRB` | The classic CRB index (current code) | ✅ 362.31 | **1994** |
| **Baltic Dry Index** | `.BADI` | Dry-bulk shipping — real-activity / China-demand proxy | ✅ 2797 | **1985** |
| S&P GSCI (spot / TR) | `.SPGSCI` · `.SPGSCITR` | Energy-heavy, production-weighted | ◑ gated | — |
| Thomson Reuters/Jefferies CRB | `.TRJCRB` | Legacy CRB code (superseded by `.TRCCRB`) | ◑ gated | — |
| LME Metals Index | `.LMEX` | London Metal Exchange base-metals basket | ◑ gated | — |

For single commodities, pull the outright future or spot RIC rather than an index.

## 4. Equity benchmark levels

Equity index **levels** are available via `get_history` (a clean daily close, decades deep) — a
different route from the `TR.Index*` valuation/return/constituent data in
[benchmarks.md](benchmarks.md), which is `get_data`-only. **Use this file for the index level; use
benchmarks.md for P/E, dividend yield, total return, and constituents.**

The **US flagships and the Nikkei are gated on the reference account** — `.SPX` (S&P 500), `.DJI`
(Dow), `.N225` (Nikkei 225) need the S&P DJI / JPX index licence — so the ✅ substitutes there are
Nasdaq (`.NDX`/`.IXIC`) and Russell (`.RUT`) for the US, and TOPIX (`.TOPX`) for Japan.

| Region | Indices (RIC — status / live 2026-07-06) |
|---|---|
| **US** | S&P 500 `.SPX` ◑ (TR `.SPXT` ◑) · Dow `.DJI` ◑ · Nasdaq 100 `.NDX` ✅ 29698 · Nasdaq Composite `.IXIC` ✅ 26121 · Russell 2000 `.RUT` ✅ 3010 |
| **Europe** | STOXX Europe 600 `.STOXX` ✅ 650 · EURO STOXX 50 `.STOXX50E` ✅ 6398 · FTSE 100 `.FTSE` ✅ 10652 · DAX `.GDAXI` ✅ 25818 · CAC 40 `.FCHI` ✅ 8480 · IBEX 35 `.IBEX` ✅ 19684 · SMI `.SSMI` ✅ 14302 · AEX `.AEX` ✅ 1082 · BEL 20 `.BFX` ✅ 5732 · OMX Stockholm 30 `.OMXS30` ✅ 3236 · OMX Helsinki 25 `.OMXH25` ✅ 6202 · ATX `.ATX` ✅ 6566 · PSI 20 `.PSI20` ✅ 9217 · Oslo OBX `.OBX` ✅ 1872 |
| **Asia-Pacific** | Nikkei 225 `.N225` ◑ · TOPIX `.TOPX` ✅ 4102 · Hang Seng `.HSI` ✅ 23616 · HS China Enterprises `.HSCE` ✅ 7812 · HS Tech `.HSTECH` ✅ 4541 · Shanghai Composite `.SSEC` ✅ 4041 · CSI 300 `.CSI300` ✅ 4842 · KOSPI `.KS11` ✅ 8051 · Taiwan TAIEX `.TWII` ✅ 46556 · Jakarta Composite `.JKSE` ✅ 5916 · Straits Times `.STI` ✅ 5260 · ASX 200 `.AXJO` ✅ 8831 · All Ordinaries `.AORD` ✅ 9037 · Sensex `.BSESN` ✅ 78285 |
| **Americas (ex-US)** | S&P/TSX Composite `.GSPTSE` ✅ 35212 · Mexico S&P/BMV IPC `.MXX` ✅ 67466 · Bovespa `.BVSP` ✅ 172448 · Merval `.MERV` ✅ 3267481 |
| **Global (MSCI / Refinitiv)** | MSCI World (DM) `.MIWD00000PUS` ✅ 1128 · MSCI ACWI `.MIWO00000PUS` / `.MIWO00000GUS` ✅ (gross 23392) · MSCI Emerging Markets `.MIEF00000PUS` ✅ 1721 · MSCI AC Asia Pacific `.MIAP00000PUS` ✅ 276 · Refinitiv Global `.TRXFLDGLPU` ✅ 437 |

**Notes on codes.** `.STOXX50E` is the Refinitiv RIC for the EURO STOXX 50 (the common ticker "SX5E"
is not a resolvable RIC). Yahoo/Google-style tickers (`.GSPC`, `.INX`) and the Bloomberg `.NKY` are
**not** LSEG RICs — use `.SPX` and `.N225`.

**MSCI RIC decode:** `.MI{universe}00000{RT}{CUR}` — universe `WD`=World (developed), `WO`=ACWI (all
countries), `EF`=Emerging Free, `AP`=AC Asia Pacific; return type `P`=price, `G`=gross, `N`=net;
currency `US`=USD. So `.MIEF00000NUS` is MSCI EM net-return in USD. Confirm the exact price/net/gross
variant against the MSCI factsheet before using in a return study.

## 5. Credit / CDS indices

The tradable credit-index families (**iTraxx** Europe Main / Crossover, **CDX** NA IG / HY) live on
LSEG but require a **dedicated credit (CDS) entitlement** and are addressed through **chains** rather
than a single dot-RIC — generic guesses (`ITXEB5Y=R`, `CDXIG5Y=R`, …) did not resolve on the reference
account. Discover the live constituent RIC via `ld.discovery.search("iTraxx Europe 5Y", view="SearchAll")`
or the relevant CDS chain before pulling. For a **sovereign** credit-risk read without that entitlement,
the `=RR` benchmark page already carries a spread block (`AST_SWPSPD`, `ZSPREAD`, `INT_CDS`, bond-CDS
basis) — see [sovereign-yields.md](sovereign-yields.md).

> **Tip — the delayed (`.d`) variant.** Some real-time index RICs are gated while a **delayed feed** is
> not: `.dMIWO00000GUS` returned the same value as `.MIWO00000GUS`. If a headline code comes back null,
> a `.d`-prefixed or exchange-delayed variant is worth a probe before concluding the series is
> unavailable on your entitlement.

## History depth (by tier)

Deepest daily history of `TRDPRC_1` for the ✅ series, verified with a yearly-interval probe back to
1985:

| Tier | Indices | Level series starts | Notes |
|---|---|---|---|
| **Deepest (mid-1980s)** | `.DXY`, `.BADI`, `.FTSE`, `.HSI`, `.KS11`, `.RUT`, `.NDX` | **1985** | Multi-decade daily. |
| **Late 1980s** | `.STOXX` (1986), `.GDAXI` (1987), MSCI `.MIWD/.MIEF` (base 100 = **Dec 1987**) | **1986–87** | MSCI rebased to 100 at inception. |
| **1990s** | `.BCOM`/`.BCOMTR` (1991), `.TRCCRB` (1994), `.V2TX`/`.V6I1` (1999) | **1991–99** | VSTOXX from 1999. |
| **2000s** | `.VHSI` (2001), `.MOVE` (2002), `.NIFVIX` (2008) | **2001–08** | Vol indices are the shallowest. |

**Watch out:** `.BVSP` (Bovespa) prints from 1985 but pre-1994 values are near-zero artefacts of
Brazil's currency redenominations — treat it as usable from the **1994 Real plan** onward. **Frequency:**
daily (business days); `interval` also accepts `weekly` / `monthly` / `quarterly` / `yearly`.
**T-1 availability** — the latest close usually posts the next business day, so a query up to "today"
may miss the final bar.

## Access patterns

**1. One index, as a time series (default fields → read `TRDPRC_1`):**

```python
import lseg.data as ld
ld.open_session()
dxy = ld.get_history(universe=".DXY", start="1985-01-01", end="2026-07-06", interval="daily")
# columns: TRDPRC_1 (level), OPEN_PRC, HIGH_1, LOW_1
ld.close_session()
```

**2. A cross-section of indices — multi-RIC, ONE field → wide frame, one column per index:**

```python
gauges = ld.get_history(
    universe=".DXY, .MOVE, .V2TX, .VHSI, .BCOM",
    fields=["TRDPRC_1"],                 # ONE field -> wide, one column per RIC
    start="2026-06-22", end="2026-07-06",
)
# columns: Date, .DXY, .MOVE, .V2TX, .VHSI, .BCOM
# (harmless "Requested fields not found: ['TRDPRC_1']" warning — values ARE TRDPRC_1;
#  any unentitled RIC comes back as an all-null column, listed in a second warning)
```

**3. The VSTOXX term structure in one call:**

```python
vstoxx = ld.get_history(
    universe=", ".join(f".V6I{i}" for i in range(1, 9)),   # .V6I1 .. .V6I8
    fields=["TRDPRC_1"], start="2026-06-22", end="2026-07-06",
)
```

**4. Long histories:** the series are decades deep and daily — chunk by date range and persist
(`df.to_parquet(...)`) rather than holding a wide multi-decade frame in memory.

## Notes / gotchas

- **`TRDPRC_1` is the level.** A bare `get_history` returns it plus OHLC where published. In the
  multi-RIC wide form the values are still `TRDPRC_1` despite the "field not found" warning.
- **Entitlement, not existence.** `◑`-marked RICs (`.VIX`, `.SPX`, `.DJI`, `.N225`, S&P GSCI, the CBOE
  suite) are real, standard LSEG codes that were simply unentitled on the reference account — they
  resolve on a subscription that licenses the underlying index. An unentitled RIC returns an **all-null
  column, not an error**, so always inspect which columns populated before claiming a series exists.
- **Validate the RIC, not the concept**, and prefer the Refinitiv RIC over a Yahoo/Bloomberg ticker
  (`.SPX` not `.GSPC`/`.INX`; `.N225` not `.NKY`; `.STOXX50E` not `SX5E`).
- **`.d` delayed variants** sometimes bypass a real-time entitlement (worked for MSCI ACWI); worth a
  probe for a gated code.
- **T-1 availability** and **silent field/RIC drops** apply as everywhere in LSEG.
- **Related families:** equity/FI benchmark **valuation multiples, returns, and constituents** are in
  [benchmarks.md](benchmarks.md) (`TR.Index*`, `get_data`); **cash sovereign yield curves** in
  [sovereign-yields.md](sovereign-yields.md); **FX implied-vol surfaces** (currency-level vol, the FX
  analogue of these equity-vol indices) in [fx-options.md](fx-options.md); **FX spot** for building a
  custom dollar index in [fx-spot.md](fx-spot.md).
```
