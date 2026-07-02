# Valuation & Ratios (`TR.*`)

Valuation multiples and financial ratios, **LSEG-calculated**. This family splits into two
behaviours that matter for how you query it: a set of **daily time-series** fields (enterprise
value, market cap and the price-based multiples, which update every trading day) and a set of
**point-in-time** ratios tied to the latest fiscal period. Every code below was **validated
live against the MCP field catalogue on 2026-07-02**; two of them (`TR.PERatio`, `TR.EPS`) are
valid but sit behind a separate entitlement — see the caveat.

> **`TR.*` vs `TR.F.*` caveat.** These are *non-standardized*, LSEG-calculated fields, a
> different family from the standardized statement items (`TR.F.*`). A `TR.*` valuation field
> and a `TR.F.*` line item built on the "same" underlying (book value, EPS, sales) can return
> **different values** because the inputs are computed differently. Pick the one whose
> methodology matches your use case; see [../usage/field-discovery.md](../usage/field-discovery.md).

> **Entitlement caveat (important).** `TR.PERatio` (Price/Earnings, adjusted) and `TR.EPS` are
> **valid field names** but are gated behind a separate entitlement on some accounts and return
> `access-denied` (they come back as an all-`NULL` column with a warning, not an error — the
> query still succeeds). Documented fallbacks:
> - **P/E:** compute from `TR.CompanyMarketCap / TR.NetIncome`.
> - **EPS:** use `TR.F.EPSBasicExclExordItemsComTot` (standardized, see
>   [income-statement.md](income-statement.md)) or `TR.EPSMean` (consensus estimate, see
>   [estimates.md](estimates.md)).

## Daily time-series valuation fields

These carry a value **for every trading day** and are the ones you query with
`SDate` / `EDate` + `Frq` (`D` daily, `W` weekly, `M` monthly). They re-price as the share
price moves, so a monthly panel of valuation multiples comes straight out of these — no need to
join price to fundamentals yourself. See [../usage/querying.md](../usage/querying.md).

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.PriceClose` | Price Close | Money | Closing share price for the day; the price input underlying the multiples below. |
| `TR.CompanyMarketCap` | Company Market Cap | Money | Market capitalisation (share price times shares outstanding), re-priced daily. |
| `TR.EV` | Enterprise Value (Daily Time Series) | Money | Market cap plus net debt (and minorities/preferred); the takeover-value numerator, daily. |
| `TR.EVToEBITDA` | Enterprise Value To EBITDA (Daily Time Series Ratio) | Float | Enterprise value divided by EBITDA — the core cash-flow valuation multiple. |
| `TR.EVToSales` | Enterprise Value To Sales (Daily Time Series Ratio) | Float | Enterprise value divided by revenue; useful where earnings are thin or negative. |
| `TR.PriceToBVPerShare` | Price To Book Value Per Share (Daily Time Series Ratio) | Float | Share price divided by book value per share (price-to-book). |
| `TR.PriceToSalesPerShare` | Price To Sales Per Share (Daily Time Series Ratio) | Float | Share price divided by sales per share (price-to-sales). |
| `TR.DividendYield` | Dividend Yield | Percentage | Indicated annual dividend per share as a percentage of the share price. |

## Point-in-time ratios

These resolve to a single value tied to the **latest (or requested) fiscal period** — query
them with `Period` (`FY0`, `FQ0`, ranges), like any fundamental. They do not re-price daily.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.BookValuePerShare` | Book Value Per Share | Money | Common shareholders' equity divided by shares outstanding. |
| `TR.CurrentRatio` | Current Ratio | Float | Current assets divided by current liabilities (short-term liquidity). |
| `TR.PERatio` | Price/Earnings Ratio (Adjusted) | Float | Price/earnings on an adjusted-earnings basis. **Entitlement-gated** (see caveat). |
| `TR.EPS` | EPS | Money | Earnings per share (LSEG-calculated). **Entitlement-gated** (see caveat). |

## Access patterns

**1. A daily valuation time series** — enterprise value, market cap and EV/EBITDA over a
window, one row per trading day:

```python
import lseg.data as ld
ld.open_session()
df = ld.get_data(
    universe=["AAPL.O"],
    fields=["TR.PriceClose", "TR.CompanyMarketCap", "TR.EV",
            "TR.EVToEBITDA", "TR.EVToSales", "TR.EV.date"],
    parameters={"SDate": "2025-01-01", "EDate": "2025-06-30", "Frq": "D"},
)
print(df.head())
ld.close_session()
```

**2. A point-in-time valuation snapshot** — the multiples for the latest fiscal year, with a
computed P/E fallback in case the gated field is denied:

```python
df = ld.get_data(
    universe=["AAPL.O"],
    fields=["TR.CompanyMarketCap", "TR.NetIncome",   # -> P/E = MCap / NetIncome
            "TR.PriceToBVPerShare", "TR.DividendYield", "TR.BookValuePerShare"],
    parameters={"Period": "FY0", "Curn": "USD"},
)
```

## Notes / gotchas

- **`Frq` on daily fields, `Period` on point-in-time fields.** Passing `Frq="FQ"` with
  `SDate/EDate` on a *daily* field down-samples it; passing `Frq` alone (no `SDate/EDate`)
  is ignored and you get only the latest value. Never mix a `Period` range with an
  `SDate/EDate` range — it creates a confusing cross-product. See the gotchas in
  [../usage/querying.md](../usage/querying.md).
- **Entitlement drops are silent-ish.** A gated field (`TR.PERatio`, `TR.EPS`) returns an
  all-`NULL` column plus a warning rather than raising; the surrounding query still succeeds.
  Inspect the columns and fall back to the computed alternatives above.
- **Case-insensitive** field codes, and multiple valid names can exist for one concept
  (`TR.CompanyMarketCap` = `TR.CompanyMarketCapitalization`).
- **Silent drops** for any invalid/unentitled field — always inspect the returned columns.
