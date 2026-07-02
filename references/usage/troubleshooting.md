# Troubleshooting

Common problems with the `lseg.data` library and how to fix them.

## Authentication

**"Session is not opened"** — call `ld.open_session()` before any data call.

**"Authentication failed / invalid credentials"**
- Use the **machine ID** (e.g. `GE-A-01234567-8-9012`), not your email.
- Check the app key is set: `import os; print(os.environ.get("RDP_APP_KEY"))`.
- If the password has expired, regenerate it in the LSEG Developer Portal.

**"Cannot connect to desktop session"** — either ensure LSEG Workspace/Eikon is
running and logged in, or switch to a platform session:
```python
ld.open_session(config_name="platform.ldp")
```

## Empty or missing data

**Empty / all-NaN DataFrame**
1. Wrong RIC — verify the exchange suffix (`AAPL.O`, not `AAPL`); convert from ISIN
   if unsure (see [symbology.md](symbology.md)).
2. Missing period for periodic data — add `parameters={"Period": "FY0"}`.
3. Field not available for that instrument or not entitled on your account.

**Some fields populated, others null** — a field may have no coverage for that
company (e.g. ESG for a small cap), require a separate entitlement, or update on a
different cadence.

**History gaps** — weekends/holidays are expected; other gaps usually mean a
corporate action or ticker change. Use `adjustments=["split", "dividend"]` for
adjusted history.

## Rate limits

Requests are throttled. If you hit a limit:

```python
import time

def get_data_with_retry(universe, fields, max_retries=3):
    for attempt in range(max_retries):
        try:
            return ld.get_data(universe, fields)
        except Exception as e:            # narrow to the library's error class if you know it
            if "rate limit" in str(e).lower():
                time.sleep(2 ** attempt * 30)   # back off: 30s, 60s, 120s
            else:
                raise
    raise RuntimeError("Max retries exceeded")
```

Also **batch** instruments into chunks rather than one request per symbol.

## Common code errors

**`'Response' object is not subscriptable`** — you forgot `.get_data()`:
```python
resp = fundamental_and_reference.Definition(universe, fields).get_data()
df = resp.data.df
```

**`module 'lseg.data' has no attribute ...`** — check the function name with
`dir(ld)`. The core functions are `get_data`, `get_history`, `open_session`,
`close_session`.

**KeyError on `df.loc["AAPL.O"]`** — the frame has a MultiIndex; use
`df.reset_index()` or `df.loc[df["Instrument"] == "AAPL.O"]`.

## Debugging aids

```python
import logging
logging.getLogger("lseg.data").setLevel(logging.DEBUG)   # verbose output

# Inspect the raw response
resp = fundamental_and_reference.Definition(["AAPL.O"], ["TR.Revenue"]).get_data()
print(resp.data.raw)     # raw JSON
print(resp.data.df)      # parsed frame
```

## If a query "succeeds" but the data looks wrong

Invalid fields are silently dropped and empty cells are returned instead of errors,
so a query can look successful and still be wrong. Always: verify field names
against the [field catalog](../data-items/README.md), check the returned columns,
null-check critical fields, and confirm the date range.

## Getting help

- LSEG Developer Community: https://community.developers.refinitiv.com/
- API documentation: https://developers.lseg.com/
- Data Item Browser (field lookup): see [field-discovery.md](field-discovery.md)
