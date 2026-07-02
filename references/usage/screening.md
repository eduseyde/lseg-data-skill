# Screening

The `Screener` object filters the instrument universe by market cap, exchange,
sector, performance, and valuation, returning a list of RICs you can feed straight
into `get_data()`.

## Basic usage

```python
import lseg.data as ld
from lseg.data.discovery import Screener

ld.open_session()

rics = Screener(
    "U(IN(Equity(active,public,primary))), "
    "TR.CompanyMarketCap(Scale=6)>=5000, "         # market cap >= $5B
    'IN(TR.ExchangeMarketIdCode,"XNYS"), '         # NYSE
    'IN(TR.TRBCBusinessSectorCode,"5010","5020"), '
    "TR.TotalReturn3Mo>=15, "
    "CURN=USD"
)

print(list(rics))   # Screener is iterable -> list of RICs

df = ld.get_data(
    rics,
    ["TR.CommonName", "TR.CompanyMarketCap(Scale=6)", "TR.ExchangeName"],
)
ld.close_session()
```

## Expression building blocks

Filters are comma-separated inside one string.

**Universe**

| Expression | Meaning |
|---|---|
| `U(IN(Equity(active,public,primary)))` | Active, public, primary equities |
| `U(IN(Equity(active,public)))` | All active public equities |

**Market cap** — `TR.CompanyMarketCap(Scale=6)>=1000` (values in millions).

**Exchange** — `IN(TR.ExchangeMarketIdCode,"XNYS","XNAS")` (MIC codes: `XNYS` NYSE,
`XNAS` NASDAQ, `XLON` London, `XTKS` Tokyo).

**Sector** — `IN(TR.TRBCBusinessSectorCode,"5010","5020","5030")` (TRBC codes;
`5010` Energy-Fossil, `5110` Basic Materials, `5210` Industrials, `5310` Consumer
Cyclicals, ...).

**Performance** — `TR.TotalReturn3Mo>=15`, `TR.TotalReturn1Yr>=20`,
`TR.PricePercentChg52W>=10`.

**Valuation** — `TR.PriceToBVPerShare<=3`, `TR.DividendYield>=2` (P/E filters
depend on your entitlement).

**Currency** — `CURN=USD`.

## Example patterns

```python
# Large-cap value
Screener(
    "U(IN(Equity(active,public,primary))), "
    "TR.CompanyMarketCap(Scale=6)>=10000, "
    "TR.PriceToBVPerShare<=2, "
    "CURN=USD"
)

# High dividend on NYSE
Screener(
    "U(IN(Equity(active,public,primary))), "
    "TR.CompanyMarketCap(Scale=6)>=1000, "
    "TR.DividendYield>=4, "
    'IN(TR.ExchangeMarketIdCode,"XNYS"), '
    "CURN=USD"
)
```

## Notes

- Screener results obey the same request limits as `get_data()`; very large result
  sets may be truncated — add stricter filters.
- To build complex expressions visually, use the **Screener app in LSEG Workspace**,
  configure filters, and copy the generated expression into your code.
- Filter fields are subject to entitlement; if a screen returns nothing, verify each
  filter field resolves for your account (see [field-discovery.md](field-discovery.md)).
