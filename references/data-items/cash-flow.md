# Cash Flow Statement (`TR.F.*`)

LSEG's **standardized cash flow statement** — the three sections (operating, investing,
financing) rebuilt onto one common template so filers reporting under different regimes,
and under either the **indirect** or the **direct** method, line up field-for-field.
Every code here carries the `parent_category` **Company Fundamentals** / category
**Standardized Fundamentals**, and the whole family was enumerated live from the MCP on
**2026-07-02** by requesting `TR.F.CashFlowStatement.fieldname` +
`TR.F.CashFlowStatement.fielddescription` on `AAPL.O`: that call returns **49 field
codes**. You can regenerate the exact list at any time with that meta-field pair (see
[../usage/field-discovery.md](../usage/field-discovery.md)).

**How to query.** Pass one or more codes to `ld.get_data()` with a `Period` (`FY0` =
latest fiscal year, `FQ0` = latest quarter, ranges like `FY0:FY-4`), and optionally
`frequency` (`FY`/`FQ`), `currency` and `scale` (`6` = millions, `9` = billions). Every
value field accepts the **companion suffixes** `.date` (period-end), `.fperiod` (period
label such as `FY2024`) and `.currency` (reporting currency) to stamp each row. All
items in this statement are money amounts in the reporting currency. Note the sign
convention baked into the titles: `Decrease/(Increase)` items add to cash when the
underlying asset falls; `Increase/(Decrease)` items add to cash when the underlying
liability rises.

> **Entitlement note.** Standardized fundamentals are **broadly entitled** — verified
> live on `AAPL.O` on 2026-07-02, the full statement returns without a licence error.
> Invalid or unentitled fields are **silently dropped** from the result rather than
> raising, so always inspect the columns you actually get back. Many line items are
> industry-specific (banking, insurance, property) and return blank for companies they
> do not apply to — that is expected, not an error.

## Operating — Starting Line & Non-Cash Reconciliation

The top of the operating section under the **indirect method**: the starting-line profit
figure, the non-cash add-backs that reconcile it to cash (D&A, share-based payments,
other non-cash items), and the operating-cash-flow subtotals struck before working
capital. Note `TR.F.ProfLossStartingLineCF` is the cash-flow starting line, which is
usually income *before* extraordinary items and can differ from the income statement's
bottom line.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.ProfLossStartingLineCF` | Profit/(Loss) - Starting Line - Cash Flow | Money | The first line of the indirect-method operating section (net income, EBITDA or similar). |
| `TR.F.NonCashItemsReconcAdjCF` | Non-cash Items & Reconciliation Adjustments - Cash Flow | Money | Total non-cash reconciliation adjustments in the operating section. |
| `TR.F.OthNonCashItemsReconcAdjCF` | Other Non-Cash Items & Reconciliation Adjustments - Cash Flow - to Reconcile | Money | Provisions, other non-cash and unusual items grouped as other operating reconciliation. |
| `TR.F.DeprDeplAmortInclImpairCF` | Depreciation, Depletion & Amortization including Impairment - Cash Flow - to Reconcile | Money | Total D&A plus impairment of tangible and intangible fixed assets, added back. |
| `TR.F.DeprDeplPPECF` | Depreciation & Depletion - Property, Plant & Equipment - Cash Flow - to Reconcile | Money | Depreciation and depletion of PP&E (incl. investment property), added back. |
| `TR.F.DeprDeplAmortCF` | Depreciation, Depletion & Amortization - Cash Flow | Money | Combined PP&E depreciation/depletion and intangible amortization reconciled to cash. |
| `TR.F.ShrBasedPaymtCF` | Share Based Payments - Cash Flow - to Reconcile | Money | Reversal of the non-cash stock-based compensation expense. |
| `TR.F.CashFlowOpBefChgInWkgCap` | Cash Flow from Operating Activities before Changes in Working Capital | Money | Net operating cash flow before working-capital movements. |
| `TR.F.CashFlowOpBefChgInWkgCapAndInt` | CF from Operating Activities before Change in WC & Int Payments | Money | Operating cash flow before working-capital changes and interest paid. |

## Operating — Working Capital changes

The movements in operating assets and liabilities that convert accrual profit into cash:
receivables, inventories, payables, other assets/liabilities, and the working-capital
total.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.WkgCapCF` | Working Capital - Increase/(Decrease) - Cash Flow | Money | Total of all movements in operating assets and liabilities. |
| `TR.F.AcctRcvblCF` | Accounts Receivables - Decrease/(Increase) - Cash Flow | Money | Change in receivables (a rise in receivables reduces operating cash). |
| `TR.F.InvntCF` | Inventories - Decrease/(Increase) - Cash Flow | Money | Change in inventories (a rise in inventory reduces operating cash). |
| `TR.F.OthAssetsCF` | Other Assets - Decrease/(Increase) - Cash Flow | Money | Change in other operating assets not separately classified. |
| `TR.F.AcctPbleCF` | Accounts Payable - Increase/(Decrease) - Cash Flow | Money | Change in payables (a rise in payables adds to operating cash). |
| `TR.F.OthLiabTotCF` | Other Liabilities - Increase/(Decrease) - Total - Cash Flow | Money | Change in other operating liabilities not separately classified. |

## Net Cash from Operations

The operating-section total, after tax and finance-servicing outflows.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.NetCashFlowOp` | Net Cash Flow from Operating Activities | Money | Total operating cash flow after tax and finance-servicing outflows (all rounding adjustments applied). |

## Investing — CapEx & PP&E

Capital expenditure and property/plant/equipment flows. Mind the overlap:
`TR.F.CAPEXNetCF` nets PP&E against intangibles; `TR.F.CAPEXTot` is the gross
capitalized total (PP&E + intangibles + software); `TR.F.PPENetCF` /
`TR.F.PPEPurchCF` isolate the tangible leg.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.CAPEXNetCF` | Capital Expenditures - Net - Cash Flow | Money | Net cash from sale/purchase of tangible and intangible fixed assets. |
| `TR.F.PPENetCF` | Property, Plant & Equipment - Purchased/(Sold) - Net - Cash Flow | Money | Net cash from sale/purchase of tangible fixed assets. |
| `TR.F.PPEPurchCF` | Property, Plant & Equipment - Purchased - Cash Flow | Money | Cash outflow on the purchase of PP&E (capitalized capex). |
| `TR.F.CAPEXTot` | Capital Expenditures - Total | Money | All capitalized expenditure on PP&E, software and intangibles with useful life over one year. |

## Investing — Securities & Other

Investment-security flows (purchases, sales/maturities, and the net) plus the
catch-all other-investing line.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.InvstExclLoansCF` | Investments excluding Loans - Decrease/(Increase) - Cash Flow | Money | Net change in investments including investment-property flows, excluding loans. |
| `TR.F.InvstSecSoldPurchNetTotCF` | Investment Securities - Unclassified - Sold/(Purchased) - Net - Total - Cash Flow | Money | Net change in investment securities (sales/maturities less purchases). |
| `TR.F.InvstSecSoldMaturedCF` | Investment Securities - Sold/Matured - Unclassified - Cash Flow | Money | Cash inflow from selling securities or securities maturing. |
| `TR.F.InvstSecPurchCF` | Investment Securities - Purchased - Unclassified - Cash Flow | Money | Cash outflow on purchases of investment securities. |
| `TR.F.OthInvstCashFlow` | Other Investing Cash Flow - Decrease/(Increase) | Money | Loan originations, deferred charges and other items classified as other investing. |

## Net Cash from Investing

The investing-section total.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.NetCashFlowInvst` | Net Cash Flow from Investing Activities | Money | Sum of all inflows and outflows from investing transactions. |

## Financing — Dividends

Cash dividends paid. `TR.F.DivPaidCashTotCF` is the common-plus-preferred total;
`TR.F.DivComCashPaid` isolates the common leg.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.DivPaidCashTotCF` | Dividends Paid - Cash - Total - Cash Flow | Money | All cash dividends paid to common and preferred stockholders. |
| `TR.F.DivComCashPaid` | Dividends - Common - Cash Paid | Money | Cash dividends paid to common stockholders. |

## Financing — Stock Issuance / Buyback

Equity issuance and repurchase flows, from the all-in net line down to the isolated
common-buyback leg, plus the combined dividends-and-buyback shareholder-return line.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.StockTotIssuanceRetNetCF` | Stock - Total - Issuance/(Retirement) - Net - Cash Flow | Money | Net cash from issuance/repurchase of common and preferred stock, incl. options and warrants. |
| `TR.F.StockIssuanceRetNetExclOptWarrCF` | Stock - Issuance/(Retirement) - Net - Excluding Options/Warrants - Cash Flow | Money | Net stock issuance/repurchase excluding option-exercise and warrant flows. |
| `TR.F.StockComNetCF` | Stock - Common - Issuance/(Retirement) - Net - Cash Flow | Money | Net change in common stock (issuance less repurchase). |
| `TR.F.StockComRepurchRetiredCF` | Stock - Common - Repurchased/Retired - Cash Flow | Money | Cash outflow on repurchasing/retiring common stock. |
| `TR.F.ComStockBuybackNet` | Common Stock Buyback - Net | Money | Net common-stock buyback (repurchases less issuance). |
| `TR.F.CashDivPaidComStockBuybackNet` | Cash Dividends Paid & Common Stock Buyback - Net | Money | Combined common dividends paid and net common buyback (total shareholder cash return). |

## Financing — Debt Issuance / Reduction

Changes in the debt stack: the short-plus-long total, the short-term and long-term nets,
the long-term issuance and reduction legs, and the catch-all other-financing line.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.DebtLTSTIssuanceRetTotCF` | Debt - Long-Term & Short-Term - Issuance/(Retirement) - Total - Cash Flow | Money | Net cash from all changes in the company's debt level. |
| `TR.F.DebtIssuedReducedSTTotCF` | Debt - Issued/(Reduced) - Short-Term - Total - Cash Flow | Money | Net change in short-term debt. |
| `TR.F.DebtIssuedReducedLTCF` | Debt - Issued/Reduced - Long-Term - Cash Flow | Money | Net change in long-term debt (incl. lease liabilities). |
| `TR.F.DebtIssuedLTCF` | Debt - Issued - Long-Term - Cash Flow | Money | Cash inflow from issuing long-term debt (bank borrowings, bonds, etc.). |
| `TR.F.DebtReducedLTCF` | Debt - Reduced - Long-Term - Cash Flow | Money | Cash outflow on repaying long-term debt. |
| `TR.F.OthFinCashFlow` | Other Financing Cash Flow - Increase/(Decrease) | Money | Other financing items, incl. dividends paid to minority interests. |

## Net Cash from Financing

The financing-section total.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.NetCashFlowFin` | Net Cash Flow from Financing Activities | Money | Sum of all inflows and outflows from financing activities. |

## Net Change / Beginning / Ending balances

The reconciliation that ties the three sections back to the cash on the balance sheet:
the net change (including FX effects), the continuing-operations subtotal, and the
opening and closing cash balances.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.NetChgInCashTot` | Net Change in Cash - Total | Money | Net increase/decrease in cash incl. foreign-exchange effects, as reported. |
| `TR.F.NetCashContOps` | Net Cash from Continuing Operations | Money | Change in cash allocable to continuing operations across all three sections. |
| `TR.F.NetCashBegBal` | Net Cash - Beginning Balance | Money | Opening balance of cash and cash equivalents for the period. |
| `TR.F.NetCashEndBal` | Net Cash - Ending Balance | Money | Closing balance of cash and cash equivalents (beginning balance plus net change). |

## Free Cash Flow definitions & supplemental

LSEG carries **three** standardized free-cash-flow codes, and they return **different
values** — read the contrast before choosing:

- **`TR.F.LeveredFOCF` (title: "Free Cash Flow")** — operating cash flow **minus total
  capex**. The plain, most-cited FCF.
- **`TR.F.FOCF` (title: "Free Cash Flow Net of Dividends")** — operating cash flow
  **minus total capex minus all cash dividends paid**. The narrowest, i.e. FCF after
  returning cash to shareholders.
- **`TR.F.FreeCashFlowToEq`** — operating cash flow **minus net capex plus net debt
  issuance/retirement**. FCF available to equity holders after debt financing (an
  equity-capital-usage measure, not an ex-capex residual).

So `LeveredFOCF` > `FOCF` (dividends deducted), while `FreeCashFlowToEq` moves with the
debt flow and is a conceptually different construct. Pick the one that matches your
question and never assume they are interchangeable.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.LeveredFOCF` | Free Cash Flow | Money | Net operating cash flow less total capital expenditures. |
| `TR.F.FOCF` | Free Cash Flow Net of Dividends | Money | Operating cash flow less total capex and all cash dividends paid. |
| `TR.F.FreeCashFlowToEq` | Free Cash Flow to Equity | Money | Operating cash flow less net capex plus net debt issuance/retirement (cash to equity holders). |
| `TR.F.IncTaxPaidReimbCFSuppl` | Income Taxes - Paid/(Reimbursed) - Cash Flow - Supplemental | Money | Taxes actually paid in cash, net of refunds received (supplemental disclosure). |

## Access patterns

**1. Multi-period pull — five years of the cash-flow skeleton for one company:**

```python
import lseg.data as ld
ld.open_session()
df = ld.get_data(
    universe="AAPL.O",
    fields=[
        "TR.F.NetCashFlowOp", "TR.F.CAPEXTot", "TR.F.NetCashFlowInvst",
        "TR.F.NetCashFlowFin", "TR.F.LeveredFOCF", "TR.F.NetChgInCashTot",
        "TR.F.NetCashFlowOp.date",
    ],
    parameters={"Period": "FY0:FY-4", "Frq": "FY", "Scale": "6", "Curn": "USD"},
)
print(df)
ld.close_session()
```

**2. Targeted cross-section — compare the three FCF definitions across companies:**

```python
import lseg.data as ld
ld.open_session()
df = ld.get_data(
    universe=["AAPL.O", "MSFT.O", "GOOGL.O"],
    fields=["TR.F.LeveredFOCF", "TR.F.FOCF", "TR.F.FreeCashFlowToEq"],
    parameters={"Period": "FY0", "Scale": "9"},
)
print(df)   # the three columns differ — by dividends and by debt flow
ld.close_session()
```

## Notes / gotchas

- **Case-insensitive.** Field codes resolve regardless of case (`TR.F.LeveredFOCF` ==
  `TR.F.leveredfocf`).
- **Companion suffixes.** Any value field accepts `.date`, `.fperiod` and `.currency`
  to stamp the period and reporting currency onto each row — essential for multi-period
  panels.
- **Three Free Cash Flow codes, three values.** `TR.F.LeveredFOCF` (op cash − capex),
  `TR.F.FOCF` (also − dividends) and `TR.F.FreeCashFlowToEq` (op cash − net capex + net
  debt) are **not** interchangeable. Verify which you need.
- **Sign conventions.** `Decrease/(Increase)` asset lines add to cash as the asset
  falls; `Increase/(Decrease)` liability lines add to cash as the liability rises. Read
  the title, not just the sign.
- **Indirect vs direct method.** The starting-line and reconciliation fields assume the
  indirect method (the norm); direct-method filers populate a different set of
  underlying items that roll up into the same standardized subtotals.
- **Silent drops.** Invalid or unentitled fields are omitted from the result, not
  raised — always inspect the returned columns. Industry-specific lines (banking,
  insurance, property) return blank for companies they do not apply to.
- **`TR.*` vs `TR.F.*` divergence.** The non-standardized `TR.*` family can return a
  *different value* for the same concept — most sharply for free cash flow, where
  `TR.FreeCashFlow` is an LSEG-calculated figure distinct from all three standardized
  codes above. Verify which definition matches your use case before mixing families.
  See [../usage/field-discovery.md](../usage/field-discovery.md).
- **Regenerate the list.** `TR.F.CashFlowStatement.fieldname` +
  `TR.F.CashFlowStatement.fielddescription` re-enumerates every code and its
  authoritative definition (do not append `.fieldtype` — it nulls the call).
