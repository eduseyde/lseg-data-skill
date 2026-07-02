# Market Pricing (OHLCV via `get_history`, snapshots via `CF_*`)

Open/high/low/close/volume time series and real-time price snapshots for any tradable
instrument (equities, ETFs, indices, FX, futures). Field titles and descriptions below were
enumerated live from the MCP field catalogue (`search_fields`, `namespace="real-time"`) on
**2026-07-02**. This family has two distinct access routes that must not be confused.

> **Pricing is not a `TR.*` `get_data` field.** Historical prices are read as a **column
> time series with `get_history`** (like the swap curves in
> [swap-rates.md](swap-rates.md), but with a real OHLCV tape). Live snapshots are read with
> `get_data` using **composite `CF_*` fields**. You do not query "TR.Price" — you pick
> `get_history` for history and `CF_*` for the current tick. See
> [../usage/pricing.md](../usage/pricing.md) for the full workflow (intervals, streaming,
> chunking).

## Historical OHLCV columns (`get_history`)

These are the canonical column names `get_history` returns for a trade tape. The five
core OHLCV fields are the ones you request explicitly for a clean frame; the rest arrive
on a no-`fields` call as extras.

| Field Code | Meaning |
|---|---|
| `OPEN_PRC` | **Open** — today's/session opening price. |
| `HIGH_1` | **High** — session high. |
| `LOW_1` | **Low** — session low. |
| `TRDPRC_1` | **Close / last** — last trade price or value. |
| `ACVOL_UNS` | **Volume (unscaled)** — total trading volume, raw units. |
| `VWAP` | Volume-weighted average price. |
| `BID` | Latest/closing bid. |
| `ASK` | Latest/closing ask. |
| `TRNOVR_UNS` | Turnover (unscaled) — traded value. |
| `NUM_MOVES` | Number of price moves (trades) in the bar. |
| `BLKCOUNT` | Block-trade count. |
| `BLKVOLUM` | Block-trade volume — total block volume for the day. |

- **For clean OHLCV, request the five core fields explicitly:**
  `["OPEN_PRC", "HIGH_1", "LOW_1", "TRDPRC_1", "ACVOL_UNS"]`. This is the standard bar.
- **No `fields` = ~17 columns.** Calling `get_history` with no `fields` returns the table
  above **plus** housekeeping columns like `TRD_STATUS`, `SALTIM`, `NAVALUE` and `VWAP_VOL`.
  Convenient for exploration, noisy for a panel — name the five core fields to trim it.
- **Friendly aliases** (`OPEN`, `HIGH`, `LOW`, `CLOSE`, `VOLUME`) are accepted by the
  library on input, but the **codes above are what appear in the returned DataFrame** — key
  your downstream code off the codes, not the aliases.
- **Multi-instrument calls** return a `MultiIndex` `(instrument, field)` — slice with
  `df["AAPL.O"]`.

## Real-time / snapshot columns (`CF_*`, via `get_data`)

The `CF_*` family are LSEG **composite** (cross-asset) real-time fields — the current tick,
pulled with `get_data` rather than `get_history`. They give you the live top-of-book and
today's running OHLC without opening a stream.

| Field Code | Title | Meaning |
|---|---|---|
| `CF_LAST` | Last | Last traded price. |
| `CF_BID` | Bid | Latest best bid price. |
| `CF_ASK` | Ask | Latest best ask price. |
| `CF_VOLUME` | Volume | Today's accumulated trading volume. |
| `CF_OPEN` | Open | Today's opening price. |
| `CF_HIGH` | High | Highest bid/transaction value of the day. |
| `CF_LOW` | Low | Lowest bid/transaction value of the day. |
| `CF_CLOSE` | Close | Last trade price, settlement value or closing value. |

> **Real-time entitlement caveat (important).** The `CF_*` fields require a **real-time
> entitlement**. Without it they resolve as columns but return **no value** (an empty
> snapshot) — the same silent-drop behaviour seen elsewhere. If a `CF_*` snapshot comes
> back blank on a valid, actively-trading RIC, it is a licensing gap, not a bad query. Fall
> back to `get_history` (end-of-day, T-1) for values you can rely on without the live feed.

## Access patterns

**1. Daily OHLCV history** — request the five core fields for a clean bar (mirrors the
single-series `get_history` call for swaps):

```python
import lseg.data as ld
ld.open_session()
df = ld.get_history(
    universe="AAPL.O",
    fields=["OPEN_PRC", "HIGH_1", "LOW_1", "TRDPRC_1", "ACVOL_UNS"],
    start="2024-01-01", end="2024-12-31",
    interval="daily",
)
ld.close_session()
```

`interval` also accepts `tick`, `1min`/`5min`/`15min`/`30min`/`60min` (intraday),
`weekly`, `monthly`. Intraday depth is shallow — minute bars only reach back a recent
window (see [../usage/pricing.md](../usage/pricing.md)).

**2. Live snapshot** — the current tick and today's running figures via `CF_*`:

```python
snap = ld.get_data(
    universe=["AAPL.O", "MSFT.O"],
    fields=["CF_LAST", "CF_BID", "CF_ASK", "CF_VOLUME", "CF_OPEN", "CF_HIGH", "CF_LOW"],
)
print(snap)   # empty values ⇒ no real-time entitlement
```

## Notes

- **T-1 availability.** End-of-day pricing is usually there the next day; a query up to
  "today" may miss the final bar until T+1. For anything you need to trust without the live
  feed, use `get_history`.
- **Adjustments.** History is **unadjusted by default** — pass
  `adjustments=["split", "dividend"]` to `get_history` for corporate-action-adjusted prices.
  Unadjusted series show jumps at splits/large dividends; that is expected, not a data error.
- **Real-time entitlement.** `CF_*` snapshots need the live feed (see caveat above);
  `get_history` end-of-day does not.
- **Missing days.** Weekends/holidays are expected gaps; other gaps usually mean the
  instrument did not trade or had a corporate action / ticker change.
- **Timezone.** Prices are in exchange local time by default.
- **Silent field drops.** Invalid or unentitled fields are omitted from the result rather
  than raising — inspect the returned columns.
- **Related families.** For **interest-rate / OIS / swap-curve** series (rates, not an OHLCV
  tape) use [swap-rates.md](swap-rates.md); for the full pricing workflow — intervals,
  multi-instrument frames, streaming, and long-history chunking — see
  [../usage/pricing.md](../usage/pricing.md).
