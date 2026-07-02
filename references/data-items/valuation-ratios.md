# Valuation & Ratios (`TR.*`)

Valuation multiples and financial ratios. Several of these are **daily time-series**
fields: they support `SDate` / `EDate` with `Frq=D/W/M`. See
[../usage/querying.md](../usage/querying.md).

| Field Code | Title |
|---|---|
| `TR.EV` | Enterprise Value (Daily Time Series) |
| `TR.EVToEBITDA` | Enterprise Value To EBITDA (Daily Time Series Ratio) |
| `TR.CompanyMarketCap` | Company Market Cap |
| `TR.PriceToBVPerShare` | Price To Book Value Per Share (Daily Time Series Ratio) |
| `TR.PriceToSalesPerShare` | Price To Sales Per Share (Daily Time Series Ratio) |
| `TR.DividendYield` | Dividend Yield |
| `TR.BookValuePerShare` | Book Value Per Share |
| `TR.CurrentRatio` | Current Ratio |
| `TR.PERatio` | Price/Earnings Ratio (Adjusted) |
| `TR.EPS` | EPS |

## Notes

- **Entitlement caveat:** `TR.PERatio` and `TR.EPS` are valid field names but are
  gated behind a separate entitlement on some accounts and may return access-denied.
  If so, use alternatives:
  - **P/E:** compute from `TR.CompanyMarketCap / TR.NetIncome`.
  - **EPS:** use `TR.F.EPSBasicExclExordItemsComTot` (standardized, in
    [income-statement.md](income-statement.md)) or `TR.EPSMean` (consensus estimate,
    in [estimates.md](estimates.md)).
- Daily fields (`TR.EV`, `TR.EVToEBITDA`, `TR.CompanyMarketCap`,
  `TR.PriceToBVPerShare`, `TR.PriceToSalesPerShare`, `TR.DividendYield`,
  `TR.BookValuePerShare`, `TR.CurrentRatio`) return a value per trading day when
  queried with `SDate/EDate` + `Frq`.
