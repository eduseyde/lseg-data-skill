# Estimates (`TR.*`, Refinitiv I/B/E/S)

Analyst **consensus estimate** fields, sourced from **Refinitiv I/B/E/S** (parent category
*Refinitiv I/B/E/S Estimates*). Each field is a summary statistic across the pool of
contributing brokers' forecasts for a given metric and forward fiscal period. Every code below
was **validated live against the MCP field catalogue on 2026-07-02** (each resolves and returns
a value for `AAPL.O` on a forward period).

## The suffix system (read this first)

You build an estimate field by appending a **statistic suffix** to a base metric. The same six
suffixes work across every metric family below:

| Suffix | Builds | What it returns (I/B/E/S definition) |
|---|---|---|
| `Mean` | `TR.RevenueMean` | Statistical average of all broker estimates on the majority accounting basis. |
| `High` | `TR.RevenueHigh` | Highest broker estimate included in the summary. |
| `Low` | `TR.RevenueLow` | Lowest broker estimate included in the summary. |
| `Median` | `TR.RevenueMedian` | Statistical median of all broker estimates on the majority accounting basis. |
| `NumOfEst` | `TR.RevenueNumOfEst` | Count of broker estimates associated with the summary. |
| `StdDev` | `TR.EPSStdDev` | Standard deviation of the estimates — the **dispersion / disagreement** gauge. |

So `Mean`/`Median` are the central consensus, `High`/`Low` bracket the range, `NumOfEst` tells
you how many analysts stand behind it (a thin-coverage warning), and `StdDev` measures how much
they disagree. Not every base metric exposes all six suffixes — the tables below list the ones
verified live — but the pattern is consistent, so an unlisted combination is worth trying.

> **Forward periods.** Estimates live in the **future**: query them with forward periods
> (`FY1`, `FY2`, `FQ1:FQ4`), where the corresponding *actual* fields return `<NA>`. Mixing
> actuals and estimates over a range like `FY-1:FY2` gives you reported history and consensus
> future side by side. See the forward-period pattern in
> [../usage/querying.md](../usage/querying.md).

> **`TR.*` (I/B/E/S) vs `TR.F.*` (reported).** These are *non-standardized* estimate fields —
> a different family from the standardized reported statements (`TR.F.*`). Do not expect a
> consensus `Mean` to equal the eventual reported figure; it is a forecast, on the brokers'
> majority accounting basis, which may differ from the standardized definition.

## Revenue

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.RevenueMean` | Revenue - Mean | Money | Average of all broker revenue estimates for the period. |
| `TR.RevenueHigh` | Revenue - High | Money | Highest broker revenue estimate. |
| `TR.RevenueLow` | Revenue - Low | Money | Lowest broker revenue estimate. |
| `TR.RevenueMedian` | Revenue - Median | Money | Median of all broker revenue estimates. |
| `TR.RevenueNumOfEst` | Revenue - Number of Estimates | Integer | Number of brokers contributing a revenue estimate. |

## EPS (earnings per share)

The most heavily-covered metric, and the one where dispersion (`StdDev`) is most worth pulling.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.EPSMean` | Earnings Per Share - Mean | Money | Average broker EPS estimate (analyst-basis EPS, may include/exclude items per model). |
| `TR.EPSHigh` | Earnings Per Share - High | Money | Highest broker EPS estimate. |
| `TR.EPSLow` | Earnings Per Share - Low | Money | Lowest broker EPS estimate. |
| `TR.EPSMedian` | Earnings Per Share - Median | Money | Median broker EPS estimate. |
| `TR.EPSNumOfEst` | EPS Number of Estimates | Integer | Number of brokers contributing an EPS estimate. |
| `TR.EPSStdDev` | Earnings Per Share - Standard Deviation | Money | Standard deviation of the EPS estimates (consensus disagreement). |

## EBITDA

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.EBITDAMean` | EBITDA - Mean | Money | Average broker EBITDA estimate for the period. |
| `TR.EBITDAHigh` | EBITDA - High | Money | Highest broker EBITDA estimate. |
| `TR.EBITDALow` | EBITDA - Low | Money | Lowest broker EBITDA estimate. |
| `TR.EBITDANumOfEst` | EBITDA - Number of Estimates | Integer | Number of brokers contributing an EBITDA estimate. |

## Net income

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.NetIncomeMean` | Net Income - Mean | Money | Average broker net-income estimate for the period. |

## Cash flow (FCF, FCFPS, CFPS)

Free cash flow is estimated at both the **total** and **per-share** level; `TR.CFPSMean` is the
broader cash-flow-per-share consensus.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.FCFMean` | Free Cash Flow - Mean | Money | Average broker free-cash-flow estimate for the period. |
| `TR.FCFPSMean` | Free Cash Flow Per Share - Mean | Money | Average broker free-cash-flow-per-share estimate. |
| `TR.CFPSMean` | Cash Flow Per Share - Mean | Money | Average broker cash-flow-per-share estimate. |

## Per-share payouts and returns (DPS, ROE, ROA)

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.DPSMean` | Dividend Per Share - Mean | Money | Average broker dividend-per-share estimate for the period. |
| `TR.ROEMean` | Return On Equity - Mean | Percentage | Average broker return-on-equity estimate (net income / common equity). |
| `TR.ROAMean` | Return On Assets - Mean | Percentage | Average broker return-on-assets estimate (net income / total assets). |

## Access patterns

**1. Forward consensus with the full suffix system** — mean, range, count and dispersion for
next year's EPS, plus the fiscal-period label:

```python
import lseg.data as ld
ld.open_session()
df = ld.get_data(
    universe=["AAPL.O"],
    fields=["TR.EPSMean", "TR.EPSHigh", "TR.EPSLow",
            "TR.EPSNumOfEst", "TR.EPSStdDev", "TR.EPSMean.fperiod"],
    parameters={"Period": "FY1"},
)
print(df)
ld.close_session()
```

**2. Actuals-then-consensus, one row per period** — reported revenue for the past two years,
consensus for the next two:

```python
df = ld.get_data(
    universe=["AAPL.O"],
    fields=["TR.Revenue.fperiod", "TR.Revenue", "TR.RevenueMean", "TR.EPSMean"],
    parameters={"Period": "FY-1:FY2", "Scale": "6"},
)
# TR.Revenue is <NA> for FY1/FY2 (forward); TR.RevenueMean populates them.
```

## Notes / gotchas

- **Estimate codes use abbreviations, not the spelled-out metric.** It is `TR.FCFMean`
  (not `TR.FreeCashFlowMean`), `TR.EPSMean` (not `TR.EarningsPerShareMean`), `TR.DPSMean`,
  `TR.CFPSMean`, `TR.ROEMean`. When a spelled-out name silently drops, try the abbreviation.
- **`.date` returns the retrieval date, not the period end.** For estimate fields the `.date`
  companion gives the date the consensus was pulled; use **`.fperiod`** to identify which
  fiscal period each row belongs to.
- **Forward periods only for the estimate itself.** On `FY1`/`FY2`/`FQ1…` the matching *actual*
  field (`TR.Revenue`, `TR.EPS`) returns `<NA>`; only the `*Mean`/`*High`/… estimate populates.
- **`NumOfEst` is your coverage check.** A `Mean` backed by 2 estimates is not the same object
  as one backed by 40 — pull `NumOfEst` (and `StdDev`) alongside any consensus you rely on.
- **Not every suffix exists for every metric.** The tables list combinations verified live; some
  bases (e.g. net income) expose fewer suffixes than others. Unlisted combinations may still
  resolve — invalid ones are silently dropped, so inspect the returned columns.
- **Case-insensitive** field codes, as everywhere in the `TR.*` family.
