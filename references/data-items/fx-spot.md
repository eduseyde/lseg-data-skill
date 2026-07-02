# FX Spot Rates (RIC-addressed, `get_history`)

Spot exchange rates for every major and a wide range of emerging-market currencies, plus the
standard cross pairs. Coverage was enumerated live from the MCP (`search_instruments` +
`get_history`) on **2026-07-02**: **30+ currencies** confirmed resolving, **daily** history back to
**~1990** for majors (deeper/shallower per currency — see below), and clean session-level
(Asia/Europe/Americas) intraday breakdown on every quote.

> **This family does NOT use `TR.*` fields.** Like the swap-curve family, a spot rate is not a
> `get_data` field code — it is an **instrument addressed by RIC** and read as a **price time
> series with `get_history`**. There is one RIC per currency (vs. USD) or per cross pair. Pull
> `MID_PRICE` for the clean series.

## RIC anatomy — the single most important gotcha

FX spot RICs are a **bare 3-letter currency code + `=`**, not `CCY1CCY2=`. This trips up anyone
coming from a "ticker = pair" mental model:

| What you might guess | What actually works | Why |
|---|---|---|
| `USDJPY=` | ❌ fails (`The universe is not found`) | USD-vs-single-currency pairs are addressed by the **other currency's bare code alone** |
| `JPY=` | ✅ works — this **is** USD/JPY | |
| `USDCHF=` | ❌ fails | |
| `CHF=` | ✅ works — this **is** USD/CHF | |
| `AUDUSD=` | ❌ fails | |
| `AUD=` | ✅ works — this **is** AUD/USD | |
| `EURJPY=`, `EURGBP=`, `GBPJPY=`, `AUDJPY=` | ✅ all work | **Cross pairs** (neither leg is USD) *do* use the two-code concatenated form |

So: every USD pair is addressed by a single bare currency code. Only genuine crosses concatenate
two codes.

## Quoting convention — verified live by magnitude, not assumed

The bare code does **not** uniformly mean "USD per unit of currency" — it follows real interbank
quoting convention, which varies by currency. Confirmed live (2026-07-01 prints):

| RIC | Value | Convention |
|---|---|---|
| `EUR=` | 1.1377 | **USD per 1 unit of currency** |
| `GBP=` | 1.32755 | USD per 1 unit |
| `AUD=` | 0.68935 | USD per 1 unit |
| `NZD=` | 0.5672 | USD per 1 unit |
| `JPY=` | 162.575 | **units of currency per 1 USD** |
| `CHF=` | 0.8096 | units per 1 USD |
| `CAD=` | 1.42165 | units per 1 USD |

Only EUR, GBP, AUD, NZD are quoted currency-per-USD; every other currency (JPY, CHF, CAD, and all
EM below) is quoted units-per-USD. **Cross-check before treating a series as a "strengthens when
the number rises" or "falls" series** — it depends on which side of this split the currency is on.

Two independent sanity checks that confirm the data is right, not just plausible:
- **Pegged currencies print at their known peg**: `SAR=` = 3.7552–3.7572 (peg 3.75), `AED=` = 3.673
  (peg 3.6725), `HKD=` = 7.84375 (trading band ~7.75–7.85).
- **Cross-pair arithmetic is internally consistent**: on 2026-07-01, EUR/USD × USD/JPY =
  1.138 × 162.575 = 185.0 vs. observed `EURJPY=` = 184.97; GBP/USD × USD/JPY = 215.8 vs. observed
  `GBPJPY=` = 215.84; EUR/USD ÷ GBP/USD = 0.857 vs. observed `EURGBP=` = 0.857 — all match.

## Currency coverage (confirmed live via `get_history`)

| Tier | Currencies | RIC form |
|---|---|---|
| G10 | EUR, GBP, JPY, CHF, AUD, NZD, CAD | bare code |
| Asia EM | CNY (onshore), CNH (offshore), KRW, IDR, THB, PHP, MYR, SGD, HKD, TWD, VND, INR | bare code |
| LatAm EM | BRL, MXN, COP, PEN | bare code |
| EMEA EM | ZAR, TRY, RUB, PLN, HUF, CZK, ILS, EGP | bare code |
| GCC (pegged) | SAR, AED | bare code |
| Cross pairs | `EURJPY=`, `EURGBP=`, `GBPJPY=`, `AUDJPY=` (pattern generalizes) | two-code concatenation |

`RUB=` still resolves with a live, plausible price despite sanctions-era disruption to Russian FX
markets — not dropped from coverage.

To confirm the exact RIC for any currency rather than guessing:

```
search_instruments(
    query="<Currency> US Dollar",
    view="SearchAll",
    filter="RCSAssetCategoryLeaf eq 'FX Spot Rate'",
    select="RIC, DocumentTitle, RCSSourceTypeLeaf",
)
```

The broader `SearchAllCategory eq 'FX & Money'` filter also returns spot but is much noisier
(forwards, spot-week/spot-next outrights, futures chains all share that category) — prefer the
`RCSAssetCategoryLeaf eq 'FX Spot Rate'` filter for spot specifically.

## Composite vs contributor

Exactly like the swap-rate family: **bare `=` is the REFINITIV composite** and the broadly
entitled default. A search on EUR alone surfaced 30 contributor variants:

| RIC pattern | Meaning |
|---|---|
| `EUR=` | REFINITIV composite (default, use this) |
| `EUR=TRB` | REFINITIV blended composite |
| `EUR=S`, `EUR=X` | REFINITIV snapshot variants |
| `EUR=EBS` | EBS trading-platform feed |
| `EUR=D3` / `EUR=D4` | Dealing 3000 traded / derived |
| `EUR=BARL`, `EUR=COBA`, `EUR=DDBK`, `EUR=ABSA`, `EUR=ZKBZ` | Individual bank/broker pages (Barclays, Commerzbank, Danske, ABSA, ZKB, …) |
| `EUR=ICAP`, `EUR=TTKL`, `EUR=TKFX` | Interdealer broker pages |
| `EUR=CFXS`/`=CFXM`/`=CFXB` | China Foreign Exchange Trade System (onshore CNY reference variants) |

**Entitlement caveat, confirmed live**: `EUR=EBS` and `EUR=D3` both denied
(`UserNotPermission`) on the account tested. A denial on a contributor page is a licensing gap —
fall back to the bare composite `EUR=`.

## Fields returned by `get_history`

Calling `get_history` with no `fields` on `EUR=` returns **22 columns**. Like the swap-rate pages,
there is **no OHLCV trade tape** — this is a quoted bid/ask composite, not an exchange feed:

| Field Code | Meaning |
|---|---|
| `MID_PRICE` | **The clean spot series to use** — (BID+ASK)/2 |
| `BID` / `ASK` | Two-way quote |
| `OPEN_BID` / `OPEN_ASK` | Session-open bid/ask |
| `BID_HIGH_1` / `BID_LOW_1` | Intraday high/low of the bid |
| `ASK_HIGH_1` / `ASK_LOW_1` | Intraday high/low of the ask |
| `NUM_BIDS` | Number of bid ticks contributed that day |
| `ASIAOP_BID` / `ASIAHI_BID` / `ASIALO_BID` / `ASIACL_BID` | Asia-session open/high/low/close of the bid |
| `EUROP_BID` / `EURHI_BID` / `EURLO_BID` / `EURCL_BID` | Europe-session open/high/low/close of the bid |
| `AMEROP_BID` / `AMERHI_BID` / `AMERLO_BID` / `AMERCL_BID` | Americas-session open/high/low/close of the bid |

**Requesting equity-style trade fields raises an explicit error, not a silent drop**:
`fields=["TRDPRC_1"]` on `EUR=` returns `The universe does not support the following fields:
[TRDPRC_1]`. Use `MID_PRICE`/`BID`/`ASK`, not OHLCV field names.

## Historical depth (verified live)

| Currency | Earliest data found | Notes |
|---|---|---|
| EUR=, JPY=, GBP=, CHF=, ZAR= | **1990-01-02** | Empty at 1985/1987 — majors + ZAR bottom out ~1990. EUR is a pre-euro synthetic/stitched series, same pattern as the swap-curve doc's D-mark note. |
| TRY= | **≥1990-05-30** | Genuinely deep pre-redenomination lira-era data. |
| CNY= | **~1992-02-06** | Captures China's January 1994 official/swap-rate unification exactly (rate jumps 5.80 → 8.70 across that date) — a strong internal data-integrity marker. |
| BRL= | **1995-01-02** | Consistent with the July 1994 Plano Real currency launch. |
| MXN= | **1995-01-02** | Captures the Dec 1994/Jan 1995 "Tequila Crisis" peso collapse live in the series. |
| INR= | **1995-01-02** | Empty at 1990, consistent with India's pre-1993 capital-account controls. |

**Frequency:** daily (business days); `interval` also accepts `weekly`/`monthly`. Weekly bars are
Friday-dated and can be labeled by calendar week-end rather than last trading day (watch this near
period boundaries). Monthly bars are one end-of-month row.

**Intraday:** `1min` bars work for recent dates (confirmed clean for a same-week date). `60min`
depth was present ~9 months back from "today" and empty further back — intraday is shallow, same
guidance as the swap-curve/pricing docs.

## Access patterns

**One currency, as a time series:**

```python
import lseg.data as ld
ld.open_session()
df = ld.get_history(
    universe="EUR=",                 # EUR/USD, REFINITIV composite
    fields=["MID_PRICE"],
    start="1990-01-01", end="2026-07-01",
    interval="daily",
)
ld.close_session()
```

**A panel of currencies — one RIC per call:**

```python
currencies = {"EUR": "EUR=", "GBP": "GBP=", "JPY": "JPY=", "CHF": "CHF=",
              "AUD": "AUD=", "CNY": "CNY=", "BRL": "BRL=", "ZAR": "ZAR="}
panel = {name: ld.get_history(ric, fields=["MID_PRICE"],
                               start="2000-01-01", end="2026-07-01")
         for name, ric in currencies.items()}
```

> **Multi-RIC bug (same as swap curves).** Passing several FX spot RICs in one `get_history`
> `universe` list errors with `keys must be str, int, float, bool or None, not tuple`. Query one
> RIC at a time.

## Notes / gotchas

- **RIC form.** `USDJPY=`, `USDCHF=`, `AUDUSD=` all fail. The data lives at the bare code (`JPY=`,
  `CHF=`, `AUD=`) for USD pairs; only genuine crosses concatenate two codes.
- **Quoting direction is not uniform** — check per currency (see table above) before assuming
  "rising number = currency strengthening."
- **T-1 availability**, as with every other LSEG time series — the latest close may not post until
  the next day.
- **Multi-day ranges can occasionally return a single trailing row** rather than the full window —
  pad date ranges generously and don't assume every business day will appear.
- **Silent field drops** on genuinely invalid fields, but an **explicit error** on
  structurally-wrong fields (`TRDPRC_1`) — inspect returned columns either way.
- **Related family:** forward points and outright forwards are a *different* RIC family (tenor
  suffix, no plain spot equivalent) — see [fx-forwards.md](fx-forwards.md). FX implied volatility
  is documented in [fx-options.md](fx-options.md).
