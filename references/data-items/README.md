# LSEG Field Catalog (Data Items)

A catalog of LSEG field codes, grouped by category. Each file lists the field
code and its human readable title. Use these codes with `ld.get_data()` (and, for
pricing, with `ld.get_history()`).

## How this catalog was built

Every field code here was **validated against the live LSEG Data Library**, not
guessed:

- **Standardized financial fields (`TR.F.*`)** were listed programmatically using
  the `TR.F.<Category>.fieldname` meta-field suffix (see
  [../usage/field-discovery.md](../usage/field-discovery.md)).
- **Non-standardized fields (`TR.*`)** were confirmed by submitting each candidate
  to the API and keeping only the ones that resolved.

This means the codes below are known to be *real* field names. It does **not**
guarantee every field is available on *your* account: LSEG data is entitlement
based, so a valid field may still return access-denied depending on your
subscription. Treat this as a reliable floor, not the full universe.

## The two field families

LSEG exposes two parallel field systems that can return **different values** for
the same concept:

| Family | What it is | Listable? |
|---|---|---|
| `TR.F.*` | Line items from LSEG's standardized financial statements | Yes, via `.fieldname` meta-suffix |
| `TR.*` | LSEG-calculated values, estimates, ratios, ESG, metadata | No, must be validated by trial |

Example: "Free cash flow" for the same company and period resolves to several
different values depending on which code you pick (`TR.FreeCashFlow`,
`TR.F.LeveredFOCF`, `TR.F.FOCF`, `TR.F.FreeCashFlowToEq`). Always confirm which
definition matches your use case.

## Catalog

| File | Family | Contents |
|---|---|---|
| [balance-sheet.md](balance-sheet.md) | `TR.F.*` | Balance sheet line items (~144) |
| [income-statement.md](income-statement.md) | `TR.F.*` | Income statement line items (~101) |
| [cash-flow.md](cash-flow.md) | `TR.F.*` | Cash flow statement line items (~49) |
| [fundamentals.md](fundamentals.md) | `TR.*` | Headline calculated fundamentals |
| [estimates.md](estimates.md) | `TR.*` | Analyst consensus estimates |
| [valuation-ratios.md](valuation-ratios.md) | `TR.*` | Valuation ratios and multiples |
| [esg.md](esg.md) | `TR.*` | ESG scores and emissions |
| [identifiers.md](identifiers.md) | `TR.*` | Identifiers and classification |
| [pricing-fields.md](pricing-fields.md) | pricing | `get_history()` OHLCV and real-time fields |
| [funds.md](funds.md) | `TR.Fund*` | Lipper fund/ETF data — overview, allocation, holdings, flows, performance, ratings, ESG (281) |
| [swap-rates.md](swap-rates.md) | RIC / `get_history` | Interest-rate-swap & OIS curves — par swap rates by currency × tenor for discount/yield curves (40+ currencies) |

## Universal notes

- **Case-insensitive:** `TR.EPS` and `TR.EARNINGSPERSHARE` both resolve.
- **Companion suffixes:** append `.date`, `.fperiod`, or `.currency` to any field
  for per-row context (period end date, fiscal period label, reporting currency).
- **Silent drops:** an invalid field is silently omitted from the result rather
  than raising an error. Always inspect the returned columns.
- **No standalone debt-to-equity `TR.*` field** exists; compute it from
  `TR.TotalDebt / TR.TotalEquity`.
