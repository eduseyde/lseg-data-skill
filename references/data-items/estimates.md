# Estimates (`TR.*`)

Analyst consensus estimate fields. Build them by appending a suffix to a base
metric: `Mean`, `High`, `Low`, `Median`, or `NumOfEst` (number of estimates).

Estimates work with **forward** periods (`FY1`, `FY2`, `FQ1:FQ4`), where actuals
return `<NA>`. See [../usage/querying.md](../usage/querying.md) for the forward
period pattern.

| Field Code | Title |
|---|---|
| `TR.RevenueMean` | Revenue - Mean |
| `TR.RevenueHigh` | Revenue - High |
| `TR.RevenueLow` | Revenue - Low |
| `TR.RevenueMedian` | Revenue - Median |
| `TR.RevenueNumOfEst` | Revenue - Number of Estimates |
| `TR.EBITDAMean` | EBITDA - Mean |
| `TR.EPSMean` | Earnings Per Share - Mean |
| `TR.EPSHigh` | Earnings Per Share - High |
| `TR.EPSLow` | Earnings Per Share - Low |
| `TR.EPSMedian` | Earnings Per Share - Median |
| `TR.EPSNumOfEst` | EPS Number of Estimates |
| `TR.NetIncomeMean` | Net Income - Mean |
| `TR.FCFMean` | Free Cash Flow - Mean |
| `TR.FCFPSMean` | Free Cash Flow Per Share - Mean |
| `TR.ROEMean` | Return On Equity - Mean |
| `TR.ROAMean` | Return On Assets - Mean |

## Notes

- Estimate fields often use **abbreviations**: `TR.FCFMean` (not
  `TR.FreeCashFlowMean`), `TR.EPSMean` (not `TR.EarningsPerShareMean`).
- For estimate fields the `.date` suffix returns the date the estimate was
  retrieved, not the fiscal period end date. Use `.fperiod` to identify the period.
