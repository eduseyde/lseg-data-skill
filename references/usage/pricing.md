# Pricing Data

Historical and real-time market prices. For the field codes themselves, see
[../data-items/pricing-fields.md](../data-items/pricing-fields.md).

## Historical prices — `get_history()`

```python
import lseg.data as ld

ld.open_session()

# Daily OHLCV (request core fields explicitly for a clean frame)
df = ld.get_history(
    universe="AAPL.O",
    fields=["OPEN_PRC", "HIGH_1", "LOW_1", "TRDPRC_1", "ACVOL_UNS"],
    start="2024-01-01",
    end="2024-12-31",
    interval="daily",
)

# Intraday (1-minute bars)
bars = ld.get_history(
    universe="AAPL.O",
    start="2024-01-15 09:30",
    end="2024-01-15 16:00",
    interval="1min",
)

ld.close_session()
```

### Intervals

| Interval | Description |
|---|---|
| `tick` | Tick-by-tick |
| `1min`, `5min`, `15min`, `30min`, `60min` | Intraday bars |
| `daily` | Daily bars |
| `weekly` | Weekly bars (end-of-week) |
| `monthly` | Monthly bars |

Calling `get_history()` with no `fields` returns ~17 default columns. Specify the
five core OHLCV fields for a clean result.

## Multiple instruments

```python
df = ld.get_history(
    universe=["AAPL.O", "MSFT.O"],
    fields=["TRDPRC_1", "ACVOL_UNS"],
    start="2024-01-01",
    end="2024-12-31",
    interval="daily",
)
# Columns come back as a MultiIndex (instrument, field): df["AAPL.O"]
```

## Adjusted prices

History is **unadjusted by default**. For corporate-action adjusted prices:

```python
df = ld.get_history(
    universe="AAPL.O",
    fields=["TRDPRC_1"],
    start="2020-01-01",
    end="2023-12-31",
    adjustments=["split", "dividend"],
)
```

## Real-time / snapshot prices

```python
snap = ld.get_data(
    universe=["AAPL.O", "MSFT.O"],
    fields=["CF_LAST", "CF_BID", "CF_ASK", "CF_VOLUME"],
)
```

`CF_*` fields require a real-time entitlement.

## Streaming prices

```python
from lseg.data.content import pricing

stream = pricing.Definition(
    universe=["AAPL.O", "MSFT.O"],
    fields=["BID", "ASK", "LAST"],
).get_stream()

stream.open()
print(stream.get_snapshot())
stream.close()
```

## Large date ranges — chunk them

Each request is capped (roughly a few thousand rows). For long histories, request
in yearly chunks and concatenate:

```python
import pandas as pd
from datetime import datetime, timedelta

def get_history_chunked(universe, fields, start, end, chunk_days=365):
    frames, current = [], datetime.strptime(start, "%Y-%m-%d")
    end_dt = datetime.strptime(end, "%Y-%m-%d")
    while current < end_dt:
        chunk_end = min(current + timedelta(days=chunk_days), end_dt)
        frames.append(ld.get_history(
            universe=universe, fields=fields,
            start=current.strftime("%Y-%m-%d"),
            end=chunk_end.strftime("%Y-%m-%d"),
        ))
        current = chunk_end + timedelta(days=1)
    return pd.concat(frames)
```

## Common issues

- **T-1 availability:** the latest bar is usually missing until the next day.
- **Missing days:** weekends/holidays are expected; other gaps usually mean the
  instrument wasn't traded or had a corporate action / ticker change.
- **Timezone:** prices are in exchange local time by default.
- **Adjusted vs unadjusted:** default is unadjusted — pass `adjustments` explicitly.
