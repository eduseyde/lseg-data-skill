# Pricing Fields (`get_history`)

Field codes for market pricing, retrieved with `ld.get_history()` (not
`ld.get_data()`). See [../usage/pricing.md](../usage/pricing.md).

## Historical OHLCV fields

These are the canonical column names returned by `get_history()`:

| Field Code | Meaning |
|---|---|
| `OPEN_PRC` | Open price |
| `HIGH_1` | High price |
| `LOW_1` | Low price |
| `TRDPRC_1` | Close / last trade price |
| `ACVOL_UNS` | Volume (unscaled) |
| `VWAP` | Volume-weighted average price |
| `BID` | Bid |
| `ASK` | Ask |
| `TRNOVR_UNS` | Turnover (unscaled) |
| `NUM_MOVES` | Number of price moves |
| `BLKCOUNT` | Block trade count |
| `BLKVOLUM` | Block trade volume |

When you call `get_history()` **without** specifying fields, it returns ~17 columns
including the above plus `TRD_STATUS`, `SALTIM`, `NAVALUE`, and `VWAP_VOL`. For clean
OHLCV, request the five core fields explicitly:
`["OPEN_PRC", "HIGH_1", "LOW_1", "TRDPRC_1", "ACVOL_UNS"]`.

> Friendly aliases (`OPEN`, `HIGH`, `LOW`, `CLOSE`, `VOLUME`) are also accepted by
> the library, but the codes above are what appear in the returned DataFrame.

## Real-time / snapshot fields (`CF_*`)

Composite real-time fields, retrieved via `ld.get_data()` for a live snapshot:

| Field Code | Meaning |
|---|---|
| `CF_LAST` | Last traded price |
| `CF_BID` | Best bid |
| `CF_ASK` | Best ask |
| `CF_VOLUME` | Today's volume |
| `CF_OPEN` | Today's open |
| `CF_HIGH` | Today's high |
| `CF_LOW` | Today's low |
| `CF_CLOSE` | Previous close |

## Notes

- **T-1 availability:** end-of-day pricing is typically available the next day.
  When querying up to "today", expect the latest bar to be missing until T+1.
- **Adjustments:** by default history is unadjusted; pass
  `adjustments=["split", "dividend"]` to `get_history()` for corporate-action
  adjusted prices.
- Real-time (`CF_*`) fields require a real-time entitlement; without it they return
  no value.
