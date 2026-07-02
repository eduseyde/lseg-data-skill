# Finding Field Names

LSEG has **no programmatic full-text field search**. You cannot search "free cash
flow" and get back `TR.FreeCashFlow`. Use the methods below, in order.

## Start with the catalog

Most common fields are already listed, validated, in
[../data-items/README.md](../data-items/README.md). Check there first.

## Method 1: list standardized statement fields (`TR.F.*`)

The three financial statements support **meta-field suffixes** that return every
available field code and its description:

```python
import lseg.data as ld

ld.open_session()

df = ld.get_data(
    "AAPL.O",
    ["TR.F.CashFlowStatement.fieldname", "TR.F.CashFlowStatement.fielddescription"],
    {"Period": "FY0"},
)
ld.close_session()
```

| Category | Meta-field | Approx. fields |
|---|---|---|
| Balance Sheet | `TR.F.BalanceSheet.fieldname` | 144 |
| Income Statement | `TR.F.IncomeStatement.fieldname` | 96 |
| Cash Flow Statement | `TR.F.CashFlowStatement.fieldname` | 49 |

This returns a `Name` column (the field code, e.g. `TR.F.LeveredFOCF`) and a
`Description` column (what it represents).

## Method 2: bulk-validate candidate names (`TR.*`)

Non-standardized fields cannot be listed, so submit a batch of candidate names and
keep the ones that resolve. Invalid names are silently dropped:

```python
import lseg.data as ld
from lseg.data.content import fundamental_and_reference

ld.open_session()

candidates = ["TR.FreeCashFlow", "TR.FCF", "TR.CashFlowOps", "TR.OperatingCashFlow"]

resp = fundamental_and_reference.Definition(
    universe=["AAPL.O"],
    fields=candidates,
).get_data()

for h in resp.data.raw["headers"]:
    if h["name"].startswith("TR."):
        print(f"{h['name']:40s} -> {h['title']}")

ld.close_session()
```

Only the valid fields appear in the response headers, each with its human-readable
title (and often a description).

## Method 3: the Data Item Browser (DIB) — browser fallback

When Methods 1 and 2 don't turn up the field you need, LSEG's **Data Item Browser**
is the most comprehensive reference. It is a web app inside LSEG Workspace.

1. Open the DIB in your browser:
   `https://workspace.refinitiv.com/web/Apps/DataItemBrowser/`
2. Sign in with **your own** LSEG Workspace account if prompted.
3. In the "Find Data Item" search box, type a concept (e.g. "cash flow", "EBITDA").
4. Read the results table:
   - **Data Item Name** — the human-readable name.
   - **Data Item Code** — the field code to use in `get_data()`.
5. Click a row to see its full definition, parameters, and FieldID in the right
   panel. Multiple fields can share a similar name but differ in methodology, so
   confirm the definition before using it.

Tips: search broadly ("cash flow" rather than an exact code); use the left-sidebar
filters (asset class, content classification, data type) to narrow; add an
instrument in the top-left box to preview real values for a company.

## Field naming conventions

- **Case-insensitive:** `TR.EPS` and `TR.EARNINGSPERSHARE` both resolve.
- **Multiple valid names** can exist for one concept
  (`TR.CompanyMarketCap` = `TR.CompanyMarketCapitalization`).
- **Estimates use suffixes:** `Mean`, `High`, `Low`, `Median`, `NumOfEst`
  (`TR.RevenueMean`, `TR.EPSNumOfEst`), and abbreviations (`TR.FCFMean`, not
  `TR.FreeCashFlowMean`).
- **Companion suffixes** add per-row context to any field: `.date` (period end
  date), `.fperiod` (period label like `FY2024Q3`), `.currency` (reporting
  currency).

## The two field families

`TR.*` and `TR.F.*` can return **different values** for the same concept. Example,
"free cash flow" for one company and period:

| Field | Definition |
|---|---|
| `TR.FreeCashFlow` | LSEG calculated |
| `TR.F.LeveredFOCF` | Standardized: Free Cash Flow |
| `TR.F.FOCF` | Free Cash Flow Net of Dividends |
| `TR.F.FreeCashFlowToEq` | Free Cash Flow to Equity |

Always verify which definition matches your use case. See
[../data-items/README.md](../data-items/README.md) for the full picture.
