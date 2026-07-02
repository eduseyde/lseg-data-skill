# Fundamentals (`TR.*`)

Headline, LSEG-calculated fundamental fields. These are convenient aggregates; for
precise, standardized statement line items see [balance-sheet.md](balance-sheet.md),
[income-statement.md](income-statement.md), and [cash-flow.md](cash-flow.md).

Use with `ld.get_data()` and the `Period` parameter (e.g. `FY0` for latest annual,
`FQ0` for latest quarterly). See [../usage/querying.md](../usage/querying.md).

| Field Code | Title |
|---|---|
| `TR.Revenue` | Revenue |
| `TR.GrossProfit` | Gross Profit |
| `TR.OperatingIncome` | Operating Income |
| `TR.EBITDA` | EBITDA |
| `TR.NetIncome` | Net Income Incl Extra Before Distributions |
| `TR.TotalAssets` | Total Assets |
| `TR.TotalDebt` | Total Debt |
| `TR.TotalEquity` | Total Equity |
| `TR.FreeCashFlow` | Free Cash Flow |
| `TR.CashFromOperatingAct` | Cash from Operating Activities, Cumulative |
| `TR.CashFromInvestingAct` | Cash from Investing Activities, Cumulative |
| `TR.CashFromFinancingAct` | Cash from Financing Activities, Cumulative |

## Notes

- `TR.FreeCashFlow` is one of several free cash flow definitions. If the exact
  methodology matters, compare against the standardized codes in
  [cash-flow.md](cash-flow.md) (`TR.F.LeveredFOCF`, `TR.F.FOCF`,
  `TR.F.FreeCashFlowToEq`).
- For a debt-to-equity ratio, compute `TR.TotalDebt / TR.TotalEquity`; there is no
  standalone `TR.*` field for it.
