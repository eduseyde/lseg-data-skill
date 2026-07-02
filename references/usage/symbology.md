# Symbology: Converting Identifiers

Map between RIC, ISIN, CUSIP, SEDOL, Ticker, and LSEG organization IDs. Essential
for linking LSEG to other datasets. For the identifier *fields*, see
[../data-items/identifiers.md](../data-items/identifiers.md).

## Supported identifier types

| Type | Description | Example |
|---|---|---|
| RIC | Reuters Instrument Code | `AAPL.O` |
| ISIN | International Securities ID | `US0378331005` |
| CUSIP | Committee on Uniform Security ID | `037833100` |
| SEDOL | Stock Exchange Daily Official List | `2046251` |
| Ticker | Exchange ticker | `AAPL` |
| OrgId | LSEG Organization ID | `4295905573` |
| LEI | Legal Entity Identifier | `HWUPKR0MPOU8FGXBT394` |

## RIC exchange suffixes

Always include the exchange suffix — a bare ticker is ambiguous.

| Exchange | Suffix | Exchange | Suffix |
|---|---|---|---|
| NASDAQ | `.O` | London | `.L` |
| NYSE | `.N` | Frankfurt | `.DE` |
| NYSE Arca | `.P` | Paris | `.PA` |
| OTC | `.PK` | Tokyo | `.T` |
| | | Hong Kong | `.HK` |
| | | Toronto | `.TO` |
| | | Sydney | `.AX` |

Special patterns: `0#.SPX` (index constituent chain), `=EUR` (FX rate),
`^SPX` (index level).

## Convert with `symbol_conversion`

```python
import lseg.data as ld
from lseg.data.content import symbol_conversion

ld.open_session()

# RIC -> ISIN / CUSIP / SEDOL
result = symbol_conversion.Definition(
    symbols=["AAPL.O", "MSFT.O"],
    from_symbol_type="RIC",
    to_symbol_types=["ISIN", "CUSIP", "SEDOL"],
).get_data()
print(result.data.df)

# ISIN -> RIC
result = symbol_conversion.Definition(
    symbols=["US0378331005", "US5949181045"],
    from_symbol_type="ISIN",
    to_symbol_types=["RIC", "Ticker"],
).get_data()

ld.close_session()
```

## Or pull identifiers as fields

```python
df = ld.get_data(
    universe=["AAPL.O", "MSFT.O"],
    fields=["TR.CommonName", "TR.ISIN", "TR.CUSIP", "TR.SEDOL"],
)
```

## Bulk conversion (chunk large lists)

```python
import pandas as pd

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

frames = []
for chunk in chunks(isins, 100):
    r = symbol_conversion.Definition(
        symbols=chunk, from_symbol_type="ISIN", to_symbol_types=["RIC", "CUSIP"],
    ).get_data()
    frames.append(r.data.df)
mapping = pd.concat(frames, ignore_index=True)
```

## Gotchas

- **CUSIP length:** LSEG returns the 9-character CUSIP (with check digit). CRSP/WRDS
  usually want the 8-character form — take the first 8 characters.
- **One ISIN, many RICs:** a security can trade on several venues; an ISIN may map
  to `VOD.L`, `VOD.N` (ADR), etc.
- **Symbols change over time:** mergers and ticker changes (e.g. `FB.O` -> `META.O`).
- **OrgId vs instrument IDs:** OrgId links all securities of one company; use it to
  find cross-listings.

See [wrds-comparison.md](wrds-comparison.md) for building a WRDS/CRSP linking table.
