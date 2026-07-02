# Income Statement (`TR.F.*`)

LSEG's **standardized income statement** — the single-step and multi-step profit and
loss account rebuilt onto one common template so that a US filer, a European IFRS
filer and a Japanese filer line up field-for-field. Every code here carries the
`parent_category` **Company Fundamentals** / category **Standardized Fundamentals**, and
the whole family was enumerated live from the MCP on **2026-07-02** by requesting
`TR.F.IncomeStatement.fieldname` + `TR.F.IncomeStatement.fielddescription` on `AAPL.O`:
that call returns **102 rows / 101 distinct field codes** (the DPS-by-period-end code
`TR.F.DPSComGrossIssueByPrdEndDate` is returned twice). You can regenerate the exact
list at any time with that meta-field pair (see
[../usage/field-discovery.md](../usage/field-discovery.md)).

**How to query.** Pass one or more codes to `ld.get_data()` with a `Period` (`FY0` =
latest fiscal year, `FQ0` = latest quarter, ranges like `FY0:FY-4`), and optionally
`frequency` (`FY`/`FQ`), `currency` and `scale` (`6` = millions, `9` = billions). Every
value field accepts the **companion suffixes** `.date` (period-end), `.fperiod`
(period label such as `FY2024`) and `.currency` (reporting currency) to stamp each row.
Most items are money amounts in the reporting currency; per-share items (EPS, DPS) are
money **per share**; weighted-average share counts and earnings-allocation factors are
plain floats.

> **Entitlement note.** Standardized fundamentals are **broadly entitled** — verified
> live on `AAPL.O` on 2026-07-02, the full statement returns without a licence error.
> Invalid or unentitled fields are **silently dropped** from the result rather than
> raising, so always inspect the columns you actually get back. A handful of line items
> are industry-specific (e.g. loan-loss and utility items) and return blank for
> companies they do not apply to — that is expected, not an error.

## Revenue & Cost of Revenue

The top of the statement: total consolidated revenue and the several cost-of-revenue
cuts (as-reported, utility-inclusive, ex-depreciation). `TR.F.TotRevenue` is the
all-industry total line; the goods-and-services fields are the Industrial/Property
disaggregation.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.RevGoodsSrvc` | Revenue from Goods & Services | Money | Receipts from product and service sales, net of discounts, excise tax and returns (Industrial/Property). |
| `TR.F.SalesOfGoodsSrvcNetUnclassif` | Sales of Goods & Services - Net - Unclassified | Money | Net product and service receipts where the company does not delineate the revenue split. |
| `TR.F.TotRevenue` | Revenue from Business Activities - Total | Money | Total consolidated revenue of the company; applicable to all industries. |
| `TR.F.CostOfOpRev` | Cost of Operating Revenue | Money | Total cost of goods and services sold. |
| `TR.F.COGSTot` | Cost of Revenues - Total | Money | All as-reported costs of goods and services. |
| `TR.F.COGSInclOpMaintUtilTot` | Cost of Revenue including Operation & Maintenance (Utility) - Total | Money | Cost of revenue plus utility operation and maintenance costs. |
| `TR.F.COGSExclDepr` | Cost of Revenues excluding Depreciation | Money | Cost of goods and services with the depreciation/amortization embedded in COGS removed. |

## Gross Profit

The single standardized gross-margin line for Industrials and Property companies.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.GrossProfIndPropTot` | Gross Profit - Industrials/Property - Total | Money | Residual profit after deducting cost of production/sale from revenue (Industrial/Property). |

## Operating Expenses (SG&A, R&D)

Below-the-line running costs: selling, general and administrative expense (with and
without R&D folded in), research and development, and the various operating-expense
totals used by single-step statements.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.SGATot` | Selling, General & Administrative Expenses - Total | Money | All costs of running the business other than readying a product for sale. |
| `TR.F.SGAUnclassif` | Selling, General & Administrative Expenses - Unclassified | Money | SG&A where the company gives no further breakdown. |
| `TR.F.SGAExclRnD` | Selling, General & Administrative Expenses excluding Research & Development Expenses | Money | SG&A with R&D stripped out. |
| `TR.F.RnD` | Research & Development Expense | Money | R&D expensed during the year (excludes the portion capitalized to assets). |
| `TR.F.OpExpnTot` | Operating Expenses - Total | Money | Total operating expense as reported in a cost-by-nature / single-step statement. |
| `TR.F.OpExpn` | Operating Expenses | Money | Total operating expenses. |
| `TR.F.OpExpnExclNonCashChrgTot` | Operating Expenses excluding Non-Cash Charges - Total | Money | Operating expense less depreciation and amortization. |

## Operating Profit / EBIT / EBITDA

The operating-profit block. `TR.F.EBIT` is revenue minus total operating expense;
`TR.F.EBITDA` adds back depreciation and amortization; the operating-lease variant and
tax-adjusted operating income are analytic inputs layered on top.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.OpProfBefNonRecurIncExpn` | Operating Profit before Non-Recurring Income/(Expense) | Money | As-reported operating income from core operations, before non-recurring and non-operating items. |
| `TR.F.EBIT` | Earnings before Interest & Taxes (EBIT) | Money | Total revenue less total operating expense. |
| `TR.F.EBITDA` | Earnings before Interest, Taxes, Depreciation & Amortization (EBITDA) | Money | EBIT plus total depreciation and amortization for the period. |
| `TR.F.EBITDAOpLeasePaymt` | EBITDA and Operating Lease Payments | Money | EBITDA with operating lease payments added back. |
| `TR.F.TaxAdjOpInc` | Tax Adjusted Operating Income | Money | Income before discontinued/extraordinary items adjusted for after-tax net interest expense (analytic input). |

## Non-Operating & Pre-Tax

Other non-operating income/expense and the pre-tax income lines, including the
insurance-specific pre-provision variant.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.OthNonOpIncExpnTot` | Other Non-Operating Income/(Expense) - Total | Money | Net other non-operating income or expense. |
| `TR.F.IncBefTax` | Income before Taxes | Money | As-reported income after all operating and non-operating items, before income tax. |
| `TR.F.IncBefTaxProvForLoanLosses` | Income before Taxes & Provision for Loan Losses | Money | Pre-tax income adjusted for loan-loss provisions (Insurance/financials). |

## Taxes

The income-tax charge and its current/deferred and domestic/foreign decomposition
(mostly sourced from the tax footnotes).

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.IncTax` | Income Taxes | Money | Total income taxes for the period. |
| `TR.F.IncTaxForTheYrCurr` | Income Taxes for the Year - Current | Money | Total current tax where no jurisdiction breakdown is reported. |
| `TR.F.IncTaxDomCurr` | Income Taxes - Domestic - Current | Money | Current tax attributable to the domestic/local jurisdiction. |
| `TR.F.IncTaxFornCurr` | Income Taxes - Foreign - Current | Money | Current tax attributable to non-domestic jurisdictions. |
| `TR.F.IncTaxDef` | Income Taxes - Deferred | Money | Total deferred tax where no jurisdiction breakdown is reported. |
| `TR.F.IncTaxDomDef` | Income Taxes - Domestic - Deferred | Money | Deferred tax attributable to the domestic/local jurisdiction. |
| `TR.F.IncTaxFornDef` | Income Taxes - Foreign - Deferred | Money | Deferred tax attributable to non-domestic jurisdictions. |

## Net Income, Discontinued & Extraordinary Items, Minority Interest

The bottom of the statement, walked down step by step: after-tax income, the
before/after extraordinary-item and discontinued-operations lines, the before/after
minority-interest cut, and the income figures made available to common shareholders
(the numerators of the EPS block).

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.NetIncAfterTax` | Net Income after Tax | Money | Income after all operating/non-operating items and tax, before equity earnings, minority interest and extraordinary items. |
| `TR.F.IncBefDiscOpsExordItems` | Income before Discontinued Operations & Extraordinary Items | Money | Net income after tax plus equity in affiliate earnings and other after-tax adjustments. |
| `TR.F.ExordActivAfterTaxGL` | Extraordinary Activities - after Tax - Gain/(Loss) | Money | All after-tax extraordinary items reported by the company. |
| `TR.F.ExordItems` | Extraordinary Items | Money | Unusual, infrequent, material items reported after income taxes. |
| `TR.F.NetIncBefMinIntr` | Net Income before Minority Interest | Money | Income before discontinued/extraordinary items plus after-tax extraordinary items. |
| `TR.F.NetIncAfterMinIntr` | Net Income after Minority Interest | Money | Total net income after tax, equity earnings, extraordinary items and minority interest. |
| `TR.F.IncAvailToComShr` | Income Available to Common Shares | Money | Net income attributable to common holders, before preferred dividends and other distributions. |
| `TR.F.IncAvailToComExclExordItems` | Income available to Common excluding Extraordinary Items | Money | Income to common before extraordinary items and dividends. |
| `TR.F.DilIncAvailToComExclExordItems` | Diluted Income available to Common excluding Extraordinary Items | Money | Diluted income to common after dilution adjustments but before after-tax extraordinary items. |
| `TR.F.IncAvailToComShrBefDeprAmort` | Income Available to Common Shares before Depreciation & Amortization | Money | Income available to common with depreciation and amortization added back. |

## Comprehensive Income (OCI)

The other-comprehensive-income section: the OCI starting line, its main components
(foreign currency, unrealized investment gains, hedging), the net-of-tax OCI total, and
total comprehensive income before and after minority interest. Note OCI is reported net
of the income statement, so `TR.F.OthComprIncNetOfTaxTot` is **not** total comprehensive
income — the comprehensive-income totals below add the P&L back in.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.OthComprIncStartingLine` | Other Comprehensive Income - Starting Line | Money | The net income used to open the OCI section (falls back to bottom-line net income if not restated). |
| `TR.F.OthComprIncFornCcy` | Other Comprehensive Income - Foreign Currency | Money | OCI from foreign currency translation differences. |
| `TR.F.OthComprIncUnrealInvstGL` | Other Comprehensive Income - Unrealized Investment Gain/(Loss) | Money | OCI from revaluation of investments. |
| `TR.F.OthComprIncHedgeGL` | Other Comprehensive Income - Hedging Gain/(Loss) | Money | Unrealized gains/losses from hedging and risk management, taken through OCI. |
| `TR.F.OthComprIncNetOfTaxTot` | Other Comprehensive Income - Net of Tax - Total | Money | Sum of all OCI items not run through the income statement (excludes P&L items). |
| `TR.F.ComprIncBefMinIntrTot` | Comprehensive Income before Minority Interest - Total | Money | Sum of all income statement and OCI items before excluding minority interests. |
| `TR.F.ComprIncParentTot` | Comprehensive Income - Attributable to Parent Company Equity Holders - Total | Money | Total comprehensive income less the minority-interest share. |

## Basic EPS (Total vs Issue-Specific)

Everything needed to reconstruct **basic** earnings per share. Two axes trip people up
and are worth reading carefully:

- **Total vs Issue-Specific.** `…Tot` fields are computed at **company level** (one
  weighted-average share count for the whole company); `…Issue` fields are computed
  **per share class / instrument**, using an *earnings allocation factor* to split
  company earnings across issues. Use `…Tot` unless you specifically need per-class EPS.
- **Including vs excluding Extraordinary Items, and Normalized.** `InclExordItems` is
  the as-reported bottom-line EPS; `ExclExordItems` strips extraordinary items;
  `…Norm` (Normalized) divides **normalized** net income (also net of non-recurring
  items) by the share count. The three answer different questions — headline, clean, and
  underlying — so pick deliberately.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.NetIncBasicInclExordItemsComTot` | Net Income - Basic - including Extraordinary Items Applicable to Common - Total | Money | The basic EPS numerator: income available to common shares (company level). |
| `TR.F.ShrUsedToCalcBasicEPSTot` | Shares used to calculate Basic EPS - Total | Float | Weighted-average common shares outstanding used for per-share items, company level. |
| `TR.F.EPSBasicInclExordItemsComTot` | EPS - Basic - including Extraordinary Items Applicable to Common - Total | Money | Bottom-line basic EPS to common, company level. |
| `TR.F.EPSBasicExclExordItemsComTot` | EPS - Basic - excluding Extraordinary Items Applicable to Common - Total | Money | Basic EPS to common excluding extraordinary items, company level. |
| `TR.F.EPSBasicExclExordItemsNormTot` | EPS - Basic - excluding Extraordinary Items - Normalized - Total | Money | Normalized net income divided by basic shares, company level. |
| `TR.F.AllocNetIncInclExordItemsComIssue` | Allocated Net Income including Extraordinary Items Applicable to Common - Issue Specific | Money | Basic net income allocated to a specific share issue. |
| `TR.F.EarnAllocFactorBasicIssue` | Earnings Allocation Factor - Basic - Issue Specific | Float | Factor that allocates company-level earnings to a specific share class (1.0 for single-issue companies). |
| `TR.F.ShrUsedToCalcBasicEPSIssue` | Shares used to calculate Basic EPS - Issue Specific | Float | Weighted-average shares for per-share items, per share issue. |
| `TR.F.EPSBasicInclExordItemsComIssue` | EPS - Basic - including Extraordinary Items Applicable to Common - Issue Specific | Money | As-reported bottom-line basic EPS, per share issue. |
| `TR.F.EPSBasicExclExordItemsComIssue` | EPS - Basic - excluding Extraordinary Items Applicable to Common - Issue Specific | Money | Basic EPS excluding extraordinary items, per share issue. |
| `TR.F.EPSBasicExclExordItemsNormIssue` | EPS - Basic - excluding Extraordinary Items - Normalized - Issue Specific | Money | Normalized net income divided by basic shares, per share issue. |
| `TR.F.EPSBasicDiscOpsExordItems` | EPS - Basic from Discontinued Operations & Extraordinary Items | Money | Basic per-share gain/loss from discontinued operations and extraordinary items. |
| `TR.F.ComprEPSBasicIssue` | Comprehensive Earnings Per Share - Basic - Issue Specific | Money | Comprehensive income (incl. OCI) per basic share, per share issue. |

## Diluted EPS

The diluted mirror of the basic block — same Total-vs-Issue and Incl/Excl/Normalized
axes, using diluted (fully-converted) weighted-average shares as the denominator.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.NetIncDilInclExordItemsComTot` | Net Income - Diluted - including Extraordinary Items Applicable to Common - Total | Money | Income available to common plus the diluted adjustment (company level). |
| `TR.F.ShrUsedToCalcDilEPSTot` | Shares used to calculate Diluted EPS - Total | Float | Diluted weighted-average shares for per-share items, company level. |
| `TR.F.EPSDilInclExordItemsComTot` | EPS - Diluted - including Extraordinary Items Applicable to Common - Total | Money | Bottom-line diluted EPS to common, company level. |
| `TR.F.EPSDilExclExordItemsComTot` | EPS - Diluted - excluding Extraordinary Items Applicable to Common - Total | Money | Diluted EPS to common excluding extraordinary items, company level. |
| `TR.F.EPSDilExclExordItemsNormTot` | EPS - Diluted - excluding Extraordinary Items - Normalized - Total | Money | Normalized net income divided by diluted shares, company level. |
| `TR.F.AllocDilNetIncInclExordItemsComIssue` | Allocated Diluted Net Income including Extraordinary Items Applicable to Common - Issue Specific | Money | Diluted net income allocated to a specific share issue. |
| `TR.F.EarnAllocFactorDilIssue` | Earnings Allocation Factor - Diluted - Issue Specific | Float | Proportion of each share issue used to allocate diluted earnings (1.0 for single-issue companies). |
| `TR.F.ShrUsedToCalcEPSDilIssue` | Shares used to calculate Diluted EPS - Issue Specific | Float | Diluted weighted-average shares for per-share items, per share issue. |
| `TR.F.EPSDilInclExordItemsComIssue` | EPS - Diluted - including Extraordinary Items Applicable to Common - Issue Specific | Money | As-reported bottom-line diluted EPS, per share issue. |
| `TR.F.EPSDilExclExordItemsComIssue` | EPS - Diluted - excluding Extraordinary Items Applicable to Common - Issue Specific | Money | Diluted EPS excluding extraordinary items, per share issue. |
| `TR.F.EPSDilExclExordItemsNormIssue` | EPS - Diluted - excluding Extraordinary Items - Normalized - Issue Specific | Money | Normalized net income divided by diluted shares, per share issue. |
| `TR.F.EPSDilDiscOpsExordItems` | EPS - Diluted from Discontinued Operations & Extraordinary Items | Money | Diluted per-share gain/loss from discontinued operations and extraordinary items. |
| `TR.F.ComprEPSDilIssue` | Comprehensive Earnings Per Share - Diluted - Issue Specific | Money | Comprehensive income (incl. OCI) per diluted share, per share issue. |

## Dividends Per Share (DPS)

Common dividends per share, disclosed **per share issue**, gross (pre-tax) or net
(post-tax). The variants differ only in **which date the DPS is dated to** — by
announcement, ex-date, payable date or period-end — which matters when aligning
dividends to a price series or an accrual calendar. `TR.F.TotComSpecialDPSGrossIssue`
adds special dividends to the ordinary figure.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.DPSComGrossIssue` | DPS - Common - Gross - Issue - By Announcement Date | Money | Gross common DPS dated to the dividend announcement date. |
| `TR.F.DPSComNetIssue` | DPS - Common - Net - Issue - By Announcement Date | Money | Net (post-tax) common DPS dated to the announcement date. |
| `TR.F.DPSComGrossIssueByExDate` | DPS - Common - Gross - Issue - By Ex Date | Money | Gross common DPS dated to the ex-dividend date. |
| `TR.F.DPSComGrossIssueByPbleDate` | DPS - Common - Gross - Issue - By Payable Date | Money | Gross common DPS dated to the payable date. |
| `TR.F.DPSComGrossIssueByPrdEndDate` | DPS - Common - Gross - Issue - By Period End Date | Money | Gross common DPS dated to the fiscal period-end date. |
| `TR.F.TotComSpecialDPSGrossIssue` | Total Common & Special DPS - Gross - Issue - By Announcement Date | Money | Gross ordinary plus special common DPS, dated to the announcement date. |

## Depreciation & Amortization

The income statement D&A lines (as distinct from the cash-flow reconciliation D&A). The
`…Tot` fields take the maximum D&A reported across the income statement, cash flow or
notes.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.DeprAmortSuppl` | Depreciation & Amortization - Supplemental | Money | Combined depreciation of tangible assets and amortization of intangibles for the period. |
| `TR.F.DeprExpnTotSuppl` | Depreciation Expense - Total - Supplemental | Money | Allocation of tangible fixed-asset cost to expense over the period. |
| `TR.F.DeprDeplAmortTot` | Depreciation, Depletion & Amortization - Total | Money | Maximum combined D&A reported across statement, cash flow or notes. |
| `TR.F.DeprTot` | Depreciation - Total | Money | Maximum depreciation reported across statement, cash flow or notes. |

## Stock-Based Compensation

The stock-based compensation charge, disclosed in the footnotes on a pre-tax and
net-of-tax basis together with its tax benefit.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.StockBasedCompExpnPretaxSuppl` | Stock-Based Compensation Expense - Pre-tax - Supplemental | Money | Footnoted stock-option/share-based compensation charge, before tax. |
| `TR.F.StockBasedCompExpnNetOfTaxSuppl` | Stock-Based Compensation Expense - Net of Tax - Supplemental | Money | Footnoted stock-based compensation charge, after tax. |
| `TR.F.StockBasedCompTaxBenefSuppl` | Stock-Based Compensation - Tax Benefit - Supplemental | Money | Tax benefit relating to stock-based compensation. |

## Normalized figures

The **normalized** profit ladder — pre-tax, after-tax, continuing-operations and
bottom-line income, plus normalized EBIT and EBITDA — with non-recurring and unusual
items removed to give an underlying earnings picture.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.NormPretaxProf` | Normalized Pre-tax Profit | Money | Pre-tax profit stripped of unusual and extraordinary income/expense. |
| `TR.F.NormAfterTaxProf` | Normalized after Tax Profit | Money | Net income after tax less total non-recurring income/expense. |
| `TR.F.NormNetIncContOps` | Normalized Net Income from Continuing Operations | Money | Income before discontinued/extraordinary items less non-recurring items. |
| `TR.F.NormNetIncBottomLine` | Normalized Net Income - Bottom Line | Money | Income available to common adjusted for non-recurring and after-tax extraordinary items. |
| `TR.F.EBITNorm` | Earnings before Interest & Taxes (EBIT) - Normalized | Money | Pre-tax profit excluding unusual/extraordinary items and interest expense. |
| `TR.F.EBITDANorm` | Earnings before Interest, Taxes, Depreciation & Amortization (EBITDA) - Normalized | Money | Pre-tax profit excluding unusual items, interest and D&A. |

## Supplemental: R&D, Leases & Auditor Fees

Footnote-sourced supplemental items: the fuller R&D picture (including the capitalized
portion), rental and operating-lease expense (incl. the US-GAAP variable-lease cut), and
the external-auditor fee breakdown.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.RnDExpnCapTotSuppl` | Research & Development Expense - Expensed & Capitalized - Total - Supplemental | Money | Total R&D including the portion capitalized to intangible/tangible assets. |
| `TR.F.RnDSuppl` | Research & Development Expense - Supplemental | Money | Footnoted R&D expense (excl. the capitalized portion) where placement is unspecified. |
| `TR.F.OpRentalExpnSuppl` | Operating/Rental Expense - Supplemental | Money | Footnoted rental expense for offices, factories, machinery and equipment. |
| `TR.F.VarOpLeaseExpnUSGAAPSuppl` | Variable Operating Lease Expenses - US GAAP | Money | Variable operating-lease cost tied to an index or rate, recognized under US GAAP. |
| `TR.F.RentalOpLeaseExpn` | Rental/Operating Lease Expense | Money | Rental expense for offices, factories, machinery and equipment. |
| `TR.F.AuditorFees` | Auditor Fees | Money | Total external-auditor fees (audit, audit-related, tax and other). |
| `TR.F.AuditRelFees` | Audit-Related Fees | Money | Fees for services reasonably related to the audit or review of the financial statements. |
| `TR.F.TaxFees` | Tax Fees | Money | Fees for the auditor's tax/legal counseling services. |
| `TR.F.FeesOth` | Fees - Other | Money | All other external-auditor and non-audit fees. |

## Access patterns

**1. Multi-period pull — five years of the core P&L for one company:**

```python
import lseg.data as ld
ld.open_session()
df = ld.get_data(
    universe="AAPL.O",
    fields=[
        "TR.F.TotRevenue", "TR.F.GrossProfIndPropTot", "TR.F.EBITDA",
        "TR.F.EBIT", "TR.F.NetIncAfterMinIntr",
        "TR.F.EPSDilExclExordItemsComTot", "TR.F.TotRevenue.date",
    ],
    parameters={"Period": "FY0:FY-4", "Frq": "FY", "Scale": "6", "Curn": "USD"},
)
print(df)
ld.close_session()
```

**2. Targeted cross-section — one line item across several companies, latest year:**

```python
import lseg.data as ld
ld.open_session()
df = ld.get_data(
    universe=["AAPL.O", "MSFT.O", "GOOGL.O"],
    fields=["TR.F.EBITDA", "TR.F.EBITDA.fperiod", "TR.F.EBITDA.currency"],
    parameters={"Period": "FY0", "Scale": "9"},
)
print(df)
ld.close_session()
```

## Notes / gotchas

- **Case-insensitive.** Field codes resolve regardless of case (`TR.F.EBITDA` ==
  `TR.F.ebitda`).
- **Companion suffixes.** Any value field accepts `.date`, `.fperiod` and `.currency`
  to stamp the period and reporting currency onto each row — essential when pulling
  multi-period panels.
- **Total vs Issue-Specific EPS.** `…Tot` = one company-level share count; `…Issue` =
  per share class, split by an earnings-allocation factor. Do not mix them in one panel.
- **Incl / Excl / Normalized EPS.** `InclExordItems` (headline), `ExclExordItems`
  (clean of extraordinary items) and `…Norm` (also net of non-recurring items) are three
  different numbers — choose the one that matches your question.
- **Silent drops.** Invalid or unentitled fields are omitted from the result, not
  raised — always inspect the returned columns. Industry-specific lines (loan-loss,
  utility) return blank for companies they do not apply to.
- **`TR.*` vs `TR.F.*` divergence.** The non-standardized `TR.*` family can return a
  *different value* for the same concept (e.g. `TR.Revenue`, `TR.EPSMean` estimates)
  because of different methodology, restatement handling or estimate vs actual. The
  `TR.F.*` codes here are the **standardized as-reported** statement; verify which
  definition you need before mixing families. See
  [../usage/field-discovery.md](../usage/field-discovery.md).
- **Regenerate the list.** `TR.F.IncomeStatement.fieldname` +
  `TR.F.IncomeStatement.fielddescription` re-enumerates every code and its authoritative
  definition (do not append `.fieldtype` — it nulls the call).
