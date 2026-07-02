# LSEG Data Skill

A portable [Claude](https://claude.com/claude-code) **skill** for querying LSEG
(London Stock Exchange Group, formerly Refinitiv) financial data through the
official [`lseg.data`](https://pypi.org/project/lseg-data/) Python library.

It gives an AI assistant (or a human) the domain knowledge to retrieve LSEG data
correctly: how to authenticate, how to find the right field codes, how the
period/date parameters actually behave, and a **validated catalog** of field codes
grouped by category.

## What you need

- An **entitled LSEG account** (LSEG Workspace / Refinitiv, or a Data Platform
  machine account). The `lseg.data` library is free; the underlying data is a paid
  subscription.
- Python 3.9+ and `pip install lseg-data`.

## What's inside

```
SKILL.md                      Entry point: query discipline, quick start, index
references/
  usage/                      HOW to query (task-based guides)
    getting-started.md        install, authenticate, first query
    field-discovery.md        how to find field codes (incl. Data Item Browser)
    querying.md               periods, date ranges, and the common pitfalls
    pricing.md                historical + real-time prices
    symbology.md              RIC / ISIN / CUSIP / SEDOL conversion
    screening.md              dynamic stock screening
    esg.md                    ESG scores and emissions
    troubleshooting.md        when something goes wrong
    wrds-comparison.md        a bridge for WRDS / CRSP / Compustat users
  data-items/                 WHAT fields exist (validated catalog, by category)
    README.md                 index + the two field families
    balance-sheet.md          income-statement.md   cash-flow.md
    fundamentals.md           estimates.md          valuation-ratios.md
    esg.md                    identifiers.md        pricing-fields.md
examples/                     runnable lseg.data scripts
scripts/test_connection.py    validate connectivity
```

## About the field catalog

Every field code in `references/data-items/` was **validated against the live LSEG
Data Library**, not guessed. Standardized statement fields (`TR.F.*`) were listed
programmatically; other fields (`TR.*`) were confirmed by submitting candidates to
the API and keeping only those that resolved.

LSEG data is **entitlement-based**, so a valid field can still return access-denied
depending on your subscription. Treat this catalog as a reliable floor, not the
complete universe of fields available to every account.

## Using it as a Claude skill

Place this folder where your Claude environment discovers skills (for example a
`skills/` directory), then ask things like "get 5 years of annual revenue for Apple
and Microsoft from LSEG" or "convert these ISINs to RICs". The assistant will load
the relevant guides and field lists on demand.

## A note on credentials

This skill contains **no credentials**. Provide your own via a
`lseg-data.config.json` (kept out of version control) or environment variables — see
`references/usage/getting-started.md`. Never commit secrets.

## Licence

[MIT](LICENSE). This project is an independent helper for the LSEG Data Library and
is not affiliated with or endorsed by LSEG. "LSEG", "Refinitiv", and related marks
belong to their respective owners.
