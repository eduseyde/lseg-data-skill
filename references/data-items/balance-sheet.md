# Balance Sheet (`TR.F.*`)

The **standardized balance sheet** — LSEG's mapping of every filer's statement of financial
position onto one common chart of accounts, so a line item means the same thing across companies,
countries and accounting regimes (IFRS and US GAAP alike). These are the `TR.F.*` fields (the
`.F` marks the *standardized* fundamentals family). The full set was enumerated live from the MCP
on **2026-07-02** via `TR.F.BalanceSheet.fieldname` + `TR.F.BalanceSheet.fielddescription` on
`AAPL.O`: **144 fields**, listed and grouped below. The list regenerates at any time —

```python
ld.get_data("AAPL.O",
            ["TR.F.BalanceSheet.fieldname", "TR.F.BalanceSheet.fielddescription"],
            {"Period": "FY0"})
```

returns a `Name` column (the field code) and a `Description` column (the authoritative LSEG
definition) for all 144. See [../usage/field-discovery.md](../usage/field-discovery.md) for the
meta-field method and the `TR.*` vs `TR.F.*` distinction.

**How to query.** Address a company by RIC in `universe` and pass the fields plus a `Period`:
`FY0`/`FY-1`/… for annual, `FQ0`/`FQ-1`/… for quarterly (or a range, `FY0:FY-4`). Values come in
the **reported currency** at raw magnitude unless you override with `currency="USD"` and a `scale`
(`6` = millions, `9` = billions). Every field accepts the companion suffixes **`.date`** (period-end
date), **`.fperiod`** (period label, e.g. `FY2024`) and **`.currency`** (reporting currency) — add
them to align or audit a multi-period pull.

> **Entitlement note.** Standardized company fundamentals are **broadly entitled** — verified live
> on `AAPL.O`, where all 144 fields resolve. Coverage still varies by *filer* (many items are flagged
> "Applicable to Industrial and Property companies" and return blank for banks/insurers, which use
> the non-differentiated aggregates further down), and an **invalid or unentitled field is silently
> dropped** from the result rather than raising. Always inspect the returned columns against what you
> requested.

Nearly every line item is typed **Money** (reporting-currency amount); the **share-count** fields
(`TR.F.ComShr*`) and the **allocation factor** are typed **Float**; `TR.F.CapLeaseMatIntrCosts` is a
signed Money value (always negative).

## Current Assets

The short-term asset block — cash and near-cash, marketable short-term investments, the receivable
family, inventories and the current-asset catch-alls, closing on the current-assets subtotal.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.CashSTInvst` | Cash & Short Term Investments | Money | Combined cash, cash equivalents and short-term investments as reported (industrial/property presentation). |
| `TR.F.CashCashEquiv` | Cash & Cash Equivalents | Money | Cash plus highly liquid investments with original maturities of three months or less. |
| `TR.F.STInvstTot` | Short-Term Investments - Total | Money | Investments in debt/equity securities and derivatives maturing within one year. |
| `TR.F.LoansRcvblNetST` | Loans & Receivables - Net - Short-Term | Money | Current loans and receivables, net of provisions for doubtful accounts. |
| `TR.F.TradeAcctTradeNotesRcvblNet` | Trade Accounts & Trade Notes Receivable - Net | Money | Claims on customers for goods/services sold, net of doubtful-account provisions (excludes loans and other receivables). |
| `TR.F.RcvblOthTot` | Receivables - Other - Total | Money | Receivables not arising from sales, loans or notes, net of provisions, including short-term accrued income. |
| `TR.F.InvntTot` | Inventories - Total | Money | All stocks and inventories except any classified as fixed assets. |
| `TR.F.OthCurrAssetsTot` | Other Current Assets - Total | Money | Other current assets reported on the face of the balance sheet (aggregate of the sub-items). |
| `TR.F.OthCurrAssets` | Other Current Assets | Money | Current assets outside the named cash/investment/receivable/inventory/derivative buckets. |
| `TR.F.TotCurrAssets` | Total Current Assets | Money | Sum of all current assets — cash, short-term investments, receivables, inventories, prepaids and discontinued-operation assets. |

## Non-Current Assets, PP&E & Right-of-Use

Long-term assets: long-term and marketable investments, the full property-plant-and-equipment
ladder (net, gross, its components and accumulated depreciation), right-of-use tangible assets held
under leases, deferred tax assets and the non-current catch-alls, closing on the non-current
subtotal.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.InvstLT` | Investments - Long-Term | Money | Long-term investments held for sale or to maturity, including investment property and other non-current financial assets. |
| `TR.F.InvstAFSHTMLT` | Investments - Available for Sale/Held to Maturity - Long-Term | Money | Long-term marketable, term, equity and other investments (differentiated industrial/property). |
| `TR.F.MktSecLT` | Marketable Securities - Long-Term | Money | Long-term investments in very liquid, readily cash-convertible instruments. |
| `TR.F.PPENetTot` | Property, Plant & Equipment - Net - Total | Money | Net book value of all property, plant and equipment (all industries). |
| `TR.F.PPEExclAssetsLeasedOutNetTot` | Property, Plant & Equipment - excluding Assets Leased Out - Net - Total | Money | Net tangible fixed assets excluding assets leased out. |
| `TR.F.PPEGrossTot` | Property, Plant & Equipment - Gross - Total | Money | Gross value of fixed assets before accumulated depreciation (all industries). |
| `TR.F.PPEExclAssetsLeasedOutGross` | Property, Plant & Equipment - excluding Assets Leased Out - Gross | Money | Gross fixed assets excluding assets leased out, before depreciation and impairment. |
| `TR.F.LandBuildGross` | Land & Buildings - Gross | Money | Gross book value of freehold land and buildings (before depreciation). |
| `TR.F.LeasehImprovGross` | Leasehold Improvements - Gross | Money | Gross book value of improvements to leased/held real estate. |
| `TR.F.PlantMachEquipGross` | Plant, Machinery & Equipment - Gross | Money | Gross book value of plant, machinery and production equipment before depreciation/impairment. |
| `TR.F.ROUTangTotGross` | Right of Use Tangible Assets - Total - Gross | Money | Gross value of right-of-use tangible assets under any lease, before depreciation/impairment (also used when the lease type is indeterminate). |
| `TR.F.ROUTangOpLeaseGross` | Right of Use Tangible Assets - Operating Lease - Gross | Money | Gross value of right-of-use assets held under operating leases, before depreciation/impairment. |
| `TR.F.PPEAccumDeprTot` | Property, Plant & Equipment - Accumulated Depreciation & Impairment - Total | Money | Total accumulated depreciation and impairment on fixed assets still carried on the books. |
| `TR.F.PPEExclAssetsLeasedOutAccumDeprTot` | Property, Plant & Equipment - excluding Assets Leased Out - Accumulated Depreciation & Impairment - Total | Money | Accumulated depreciation/impairment on fixed assets other than assets leased out. |
| `TR.F.OthNonCurrAssetsTot` | Other Non-Current Assets - Total | Money | Aggregate of other non-current assets (industrial/property). |
| `TR.F.DefTaxAssetLT` | Deferred Tax - Asset - Long-Term | Money | Net long-term deferred tax assets (long-term deferred tax credits offset by long-term debits), plus the short-term portion carried in long-term assets. |
| `TR.F.OthNonCurrAssets` | Other Non-Current Assets | Money | Non-current assets not captured by the granular non-current codes. |
| `TR.F.TotNonCurrAssets` | Total Non-Current Assets | Money | Total long-term assets reported on the face of the balance sheet. |

## Total Assets

The asset-side grand total — the anchor for asset-scaling and the top of the balance-sheet identity.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.TotAssets` | Total Assets | Money | Total assets reported by the company (or the sum of total current and total non-current assets where not reported directly). |

## Current Liabilities

Obligations due within a year: trade payables and accruals, the short-term/current-debt block, the
current portions of long-term debt and leases, income-tax payable, current operating-lease
liabilities, deferred income and the current catch-alls, closing on the current-liabilities subtotal.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.TradeAcctPbleAccrualsST` | Trade Accounts Payable & Accruals - Short-Term | Money | Amounts owed to suppliers/creditors for goods and services plus accrued expenses. |
| `TR.F.TradeAcctTradeNotesPbleST` | Trade Accounts & Trade Notes Payable - Short-Term | Money | Amounts owed to suppliers/creditors for goods and services acquired in normal operations. |
| `TR.F.AccrExpnST` | Accrued Expenses - Short-Term | Money | Expenses incurred but not yet paid, due within one year, including wages/compensation payable. |
| `TR.F.STDebtCurrPortOfLTDebt` | Short-Term Debt & Current Portion of Long-Term Debt | Money | All borrowings due within one year (all industries). |
| `TR.F.STDebtNotesPble` | Short-Term Debt & Notes Payable | Money | Short-term debt, notes payable, bills of exchange and other interest-bearing obligations due within a year. |
| `TR.F.CurrPortOfLTDebtCapLeases` | Current Portion of Long-Term Debt including Capitalized Leases | Money | Portion of long-term debt instruments (including capitalized leases) due within the next fiscal year. |
| `TR.F.CurrPortOfLTDebtExclCapLease` | Current Portion of Long-Term Debt excluding Capitalized Leases | Money | Current portion of long-term debt due next year, excluding capital leases. |
| `TR.F.CapLeaseCurrPort` | Capitalized Leases - Current Portion | Money | Portion of finance leases due within the next fiscal year. |
| `TR.F.IncTaxPbleST` | Income Taxes - Payable - Short-Term | Money | Income taxes payable to government on company profits (current). |
| `TR.F.OpLeaseLiabCurrPortST` | Operating Lease Liabilities - Current Portion/Short-Term | Money | Current operating-lease liabilities, including the current portion of long-term operating leases and short-term accrued lease costs. |
| `TR.F.OthCurrLiabTot` | Other Current Liabilities - Total | Money | Other short-term liabilities on the face — current liabilities other than debt and payables. |
| `TR.F.DefIncST` | Deferred Income - Short-Term | Money | Income received in advance of delivering goods/services, within current liabilities. |
| `TR.F.OthCurrLiab` | Other Current Liabilities | Money | Current liabilities other than debt, trade payables and provisions (includes accrued interest and sundry payables). |
| `TR.F.TotCurrLiab` | Total Current Liabilities | Money | Sum of the company's current liabilities (due within one year). |

## Long-Term Debt & Non-Current Liabilities

Obligations due beyond a year: total long-term debt and its convertible/non-convertible and
ex-lease splits, capitalized and operating lease obligations, and the non-current catch-alls,
closing on the non-current-liabilities subtotal.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.DebtLTTot` | Debt - Long-Term - Total | Money | Total non-current interest-bearing debt (convertible and non-convertible), including non-current lease obligations, hybrids and long-term FHLB advances. |
| `TR.F.LTDebtExclCapLease` | Long-Term Debt excluding Capitalized Leases | Money | Total non-current interest-bearing debt (convertible and non-convertible), excluding capitalized leases. |
| `TR.F.DebtNonConvertLT` | Debt - Non-Convertible - Long-Term | Money | Non-convertible interest-bearing debt where current and long-term portions cannot be separated. |
| `TR.F.CapLeaseObligLT` | Capitalized Lease Obligations - Long-Term | Money | Obligations outstanding under finance-lease and hire-purchase agreements (non-differentiated presentation). |
| `TR.F.OpLeaseLiabLT` | Operating Lease Liabilities - Long-Term | Money | Total long-term operating-lease liabilities. |
| `TR.F.OthNonCurrLiabTot` | Other Non-Current Liabilities - Total | Money | Non-current liabilities other than debt, trade payables and provisions (differentiated presentation). |
| `TR.F.OthNonCurrLiab` | Other Non-Current Liabilities | Money | Long-term liabilities not specified as trade creditors, payables, tax or grants, or a combination thereof. |
| `TR.F.TotNonCurrLiab` | Total Non-Current Liabilities | Money | Sum of the company's non-current liabilities. |

## Total Liabilities

The liability-side grand total — all current and non-current obligations, excluding equity.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.TotLiab` | Total Liabilities | Money | All current and non-current liabilities (including short- and long-term debt), excluding shareholders' equity. |

## Shareholders' Equity

The equity block: total shareholders' funds and the parent-attributable slice, contributed capital
(par value and share premium/APIC), reserves and retained earnings, accumulated other comprehensive
income, common-equity totals, and the two grand equity totals — closing on Total Liabilities &
Equity, which balances back to Total Assets.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.ShHoldEqParentShHoldTot` | Shareholders' Equity - Attributable to Parent Shareholders - Total | Money | Total shareholders' funds attributable to the parent, including reserves and preferred shareholders. |
| `TR.F.ComEqParentShHold` | Common Equity Attributable to Parent Shareholders | Money | Par value of issued common shares plus capital surpluses and option reserves, adjusted for treasury stock, attributable to the parent. |
| `TR.F.ComEqContrib` | Common Equity - Contributed | Money | Par/stated value of issued common shares plus all capital surpluses and share-option reserves. |
| `TR.F.ComStockIssuedPaid` | Common Stock - Issued & Paid | Money | Par or stated value of the company's issued common shares (includes limited-partner capital and all multiple share classes). |
| `TR.F.ComStockShrPremInclOptionRsrv` | Common Stock - Additional Paid in Capital including Option Reserve | Money | Capital surplus on common stock (share premium/APIC) plus reported share-option reserves. |
| `TR.F.EqNonContribRsrvRetainedEarn` | Equity - Non-Contributed - Reserves & Retained Earnings | Money | Combined reported retained earnings/reserves and comprehensive income. |
| `TR.F.RetainedEarnTot` | Retained Earnings - Total | Money | Combined reported retained earnings/reserves and comprehensive income. |
| `TR.F.ComprIncAccumTot` | Comprehensive Income - Accumulated - Total | Money | Accumulated other comprehensive income, net of tax (generally US filers only). |
| `TR.F.ComEqTot` | Common Equity - Total | Money | Total common equity including general-partner holdings, deferred shares and other shareholder funds. |
| `TR.F.TotShHoldEq` | Total Shareholders' Equity - including Minority Interest & Hybrid Debt | Money | Total equity after minority interest, including equity-classified hybrids, non-controlling interest and parent-attributable equity. |
| `TR.F.TotLiabEq` | Total Liabilities & Equity | Money | Sum of all liabilities and shareholders' equity (balances back to Total Assets). |

## Shares Outstanding, Issued & Treasury

Share **counts** (not currency), at the company level and per specific issue: issued, outstanding
and treasury shares, authorized shares, and the asset-allocation factor used to split company-level
figures across multiple share classes. Typed **Float** (share quantities).

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.ComShrIssuedTot` | Common Shares - Issued - Total | Float | Number of common shares issued at company level (outstanding plus treasury). |
| `TR.F.ComShrOutsTot` | Common Shares - Outstanding - Total | Float | Number of common shares outstanding at company level (excludes treasury). |
| `TR.F.ComShrTrezTot` | Common Shares - Treasury - Total | Float | Number of common treasury shares at company level. |
| `TR.F.ComShrAuthIssue` | Common Shares - Authorized - Issue Specific | Float | Number of common shares authorized for issuance, per specific share issue. |
| `TR.F.ComShrIssuedIssue` | Common Shares - Issued - Issue Specific | Float | Number of common shares issued per specific share issue (outstanding plus treasury). |
| `TR.F.ComShrOutsIssue` | Common Shares - Outstanding - Issue Specific | Float | Number of common shares outstanding per specific share issue (excludes treasury). |
| `TR.F.ComShrTrezIssue` | Common Shares - Treasury - Issue Specific | Float | Number of common treasury shares per specific share issue. |
| `TR.F.AssetAllocFactorIssue` | Asset Allocation Factor - Issue Specific | Float | Proportion of net assets attributable to a given issue (an issue's outstanding shares over all issues' combined outstanding shares). |

## Lease Accounting Supplemental (IFRS 16 / ASC 842)

A **supplemental lease block** disclosed under IFRS 16 / ASC 842: net right-of-use tangible assets
(total, and split by operating vs finance lease), PP&E stated excluding those ROU assets, and the
operating/finance lease liability ladder with a "debt including leases" aggregate. Use these to make
pre- and post-standard balance sheets comparable and to size the on-balance-sheet lease footprint.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.ROUTangTotNetSuppl` | Right of Use Tangible Assets - Total - Net - Supplemental | Money | Gross right-of-use assets less accumulated depreciation (IFRS 16 / ASC 842). |
| `TR.F.ROUTangOpLeaseNetSuppl` | Right of Use Tangible Assets - Operating Lease - Net - Supplemental | Money | Net operating-lease right-of-use assets (gross less accumulated depreciation). |
| `TR.F.ROUTangCapFinLeaseNetSuppl` | Right of Use Tangible Assets - Capital/Finance Lease - Net - Supplemental | Money | Net finance/capital-lease right-of-use assets (gross less accumulated depreciation). |
| `TR.F.PPEExclROUTangCapLeaseNetSuppl` | Property, Plant & Equipment - excluding Right of Use Tangible Assets & Capital Leases - Net - Supplemental | Money | Net PP&E excluding right-of-use assets and capital leases. |
| `TR.F.TotOpLeaseLiabSuppl` | Total Operating Lease Liabilities - Supplemental | Money | Total accrued rental liabilities arising from operating-lease contracts. |
| `TR.F.OpLeaseLiabCurrPortSTSuppl` | Operating Lease Liabilities - Current Portion/Short-Term - Supplemental | Money | Current/short-term operating-lease liabilities (IFRS 16 / ASC 842). |
| `TR.F.OpLeaseLiabLTSuppl` | Operating Lease Liabilities - Long-Term - Supplemental | Money | Long-term operating-lease liabilities (IFRS 16 / ASC 842). |
| `TR.F.FinOpLeaseLiabTotSuppl` | Finance and Operating Lease Liabilities - Total - Supplemental | Money | Sum of operating-lease liabilities and capital leases arising on IFRS 16 adoption. |
| `TR.F.DebtInclFinOpLeaseLiabSuppl` | Debt including Finance and Operating Lease Liabilities - Supplemental | Money | Debt plus operating leases arising on IFRS 16 adoption. |

## Debt Maturity Schedule

A **maturity ladder** for long-term debt and capital leases: the amount coming due in each of the
next five years, the 2-3 and 4-5 year bands, the year-6-and-beyond and post-year-10 remainders, and
the totals — plus a capital-lease interest-cost reconciliation line. Values are **non-cumulative**
(each bucket is a standalone year, not a running sum), so this block reads directly as a
refinancing/rollover profile. Where a filer reports ranges rather than single years, the value is
placed at the highest year in the range.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.DebtLTMatTot` | Debt - Long-Term - Maturities - Total | Money | Total scheduled long-term debt repayments across the maturity ladder. |
| `TR.F.DebtLTMatIn1Yr` | Debt - Long-Term - Maturities - within 1 Year | Money | Long-term debt maturing within year 1 of the period-end date (non-cumulative). |
| `TR.F.DebtLTMatYr2` | Debt - Long-Term - Maturities - Year 2 | Money | Long-term debt maturing in year 2 (non-cumulative). |
| `TR.F.DebtLTMatYr3` | Debt - Long-Term - Maturities - Year 3 | Money | Long-term debt maturing in year 3 (non-cumulative). |
| `TR.F.DebtLTMatYr4` | Debt - Long-Term - Maturities - Year 4 | Money | Long-term debt maturing in year 4 (non-cumulative). |
| `TR.F.DebtLTMatYr5` | Debt - Long-Term - Maturities - Year 5 | Money | Long-term debt maturing in year 5 (non-cumulative). |
| `TR.F.DebtLTMatRemain` | Debt - Long-Term - Maturities - Remaining | Money | Long-term debt maturing after year 10. |
| `TR.F.DebtLTMat23Yr` | Debt - Long-Term - Maturities - 2-3 Years | Money | Long-term debt maturing in years 2 and 3 combined. |
| `TR.F.DebtLTMat45Yr` | Debt - Long-Term - Maturities - 4-5 Years | Money | Long-term debt maturing in years 4 and 5 combined. |
| `TR.F.DebtLTMatYr6Beyond` | Debt - Long-Term - Maturities - Year 6 & Beyond | Money | Long-term debt maturing after year 5 (non-cumulative). |
| `TR.F.CapLeaseMatTot` | Capital Lease Maturities - Total | Money | Sum of capital-lease maturities across years 1-10 plus executory costs. |
| `TR.F.CapLeaseMatDueIn1Yr` | Capital Lease Maturities - Due within 1 Year | Money | Capital-lease payments due within year 1 (non-cumulative). |
| `TR.F.CapLeaseMatDueInYr2` | Capital Lease Maturities - Due in Year 2 | Money | Capital-lease payments due in year 2 (non-cumulative). |
| `TR.F.CapLeaseMatDueInYr3` | Capital Lease Maturities - Due in Year 3 | Money | Capital-lease payments due in year 3 (non-cumulative). |
| `TR.F.CapLeaseMatDueInYr4` | Capital Lease Maturities - Due in Year 4 | Money | Capital-lease payments due in year 4 (non-cumulative). |
| `TR.F.CapLeaseMatDueInYr5` | Capital Lease Maturities - Due in Year 5 | Money | Capital-lease payments due in year 5 (non-cumulative). |
| `TR.F.CapLeaseMatRemainMat` | Capital Lease Maturities - Remaining Maturities | Money | Capital-lease payments maturing after year 10. |
| `TR.F.CapLeaseMatIntrCosts` | Capital Lease Maturities - Interest Costs | Money | Interest discounted from gross future lease payments to reconcile them to present value (always negative). |
| `TR.F.CapLeaseMatDueIn23Yr` | Capital Lease Maturities - Due in 2-3 Years | Money | Capital-lease payments due in years 2 and 3 combined. |
| `TR.F.CapLeaseMatDueIn45Yr` | Capital Lease Maturities - Due in 4-5 Years | Money | Capital-lease payments due in years 4 and 5 combined. |
| `TR.F.CapLeaseMatDueInYr6Beyond` | Capital Lease Maturities - Due in Year 6 & Beyond | Money | Capital-lease payments due after year 5 (non-cumulative). |

## Supplemental & Derived Items

The remaining fields are **not new lines on the face of the statement** — they are alternative
aggregates and analyst-facing recombinations of the items above. Two clusters follow.

**Alternative (non-differentiated) aggregates.** Combined totals used when a filer does not split
current from non-current — the presentation banks, insurers and other financials typically use, plus
whole-balance-sheet cash/receivable/payable rollups.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.InvstTot` | Investments - Total | Money | Total trading, term, property and other investments plus loans (non-differentiated). |
| `TR.F.LoansRcvblTot` | Loans & Receivables - Total | Money | Trade, accounts and loans receivable, net of doubtful-account provisions (all sectors). |
| `TR.F.OthAssetsTot` | Other Assets - Total | Money | Total other assets of the company. |
| `TR.F.IncTaxPbleLTST` | Income Taxes - Payable - Long-Term & Short-Term | Money | Total income taxes payable on company profits (current plus non-current). |
| `TR.F.PbleAccrExpn` | Payables & Accrued Expenses | Money | Combined payables and accrued expenses. |
| `TR.F.TradeAcctPbleTot` | Trade Account Payables - Total | Money | Total trade payables owed to suppliers/creditors, current plus non-current, including combined payables/accruals. |
| `TR.F.AccrExpn` | Accrued Expenses | Money | Total expenses accrued but not yet paid, current and non-current, including accrued interest and compensation payable. |
| `TR.F.AccrualsST` | Accruals - Short-Term | Money | Total current assets less cash and cash equivalents, minus total current liabilities. |
| `TR.F.AssetAccruals` | Asset Accruals | Money | All current assets plus total fixed assets, less cash and highly liquid short-term investments. |
| `TR.F.CashCashEquivTot` | Cash & Cash Equivalents - Total | Money | Cash plus highly liquid three-month-or-less investments (all industries). |
| `TR.F.CashSTInvstTot` | Cash & Short Term Investments - Total | Money | Total cash on hand and short-term deposits due from banks (all industries). |
| `TR.F.InvstPermanent` | Investments - Permanent | Money | Long-term investments held to maturity/for sale, including investment property, non-current financial assets and equity-method holdings. |
| `TR.F.TotFixedAssetsNet` | Total Fixed Assets - Net | Money | Total assets less all current assets (differentiated industrial/property). |
| `TR.F.UnearnRevTot` | Unearned Revenue - Total | Money | Current plus non-current deferred income (advance receipts for undelivered goods/services). |
| `TR.F.OthSTLTAssetsTot` | Other Short-Term & Long-Term Assets - Total | Money | Combined other current and non-current assets. |
| `TR.F.OthSTLTLiabTot` | Other Short-Term & Long-Term Liabilities - Total | Money | Combined other current and non-current liabilities. |
| `TR.F.TradeAcctTradeNotesRcvblNetTot` | Trade Accounts & Trade Notes Receivable - Net - Total | Money | Total customer claims for goods/services sold, net (industrial/property). |
| `TR.F.CashSTInvstAcctRcvblTot` | Cash, Short Term Investments & Accounts Receivable - Total | Money | Cash and short-term deposits combined with accounts receivable. |
| `TR.F.CashInHandWithBanksTot` | Cash in Hand & with Banks - Total | Money | Unrestricted cash on hand, demand deposits and near-term savings/time deposits. |

**Derived capital, leverage & working-capital measures.** Recombinations LSEG computes for analysis
— net debt, total-debt and capital aggregates, tangible book value, working-capital variants and the
ex-cash/ex-inventory/ex-Islamic cuts.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.F.NetDebt` | Net Debt | Money | Long-term debt less cash and short-term investments. |
| `TR.F.DebtTot` | Debt - Total | Money | Total of all borrowings, short-term plus long-term. |
| `TR.F.DebtInclPrefEqMinIntrTot` | Debt - including Preferred Equity & Minority Interest - Total | Money | Total debt plus minority interest and preferred stock. |
| `TR.F.IntrBearLiabTot` | Interest Bearing Liabilities - Total | Money | Sum of all interest-bearing borrowings reported. |
| `TR.F.TotDebtExclIslamic` | Total Debt Excluding Islamic | Money | Total debt less liabilities arising from Islamic debt-financing agreements. |
| `TR.F.NetDebtInclPrefEqMinIntr` | Net Debt Including Preferred Equity & Minority Interest | Money | Total debt including redeemable preferred and non-equity minority interest, less cash and short-term investments. |
| `TR.F.CurrPortOfLTDebtCapLeasesHybrid` | Current Portion of Long-Term Debt including Capitalized Leases & Hybrid Financial Instruments | Money | Current portion of long-term debt due next year, including capital leases and hybrid/mandatorily-redeemable instruments. |
| `TR.F.CashSTInvstNetOfDebt` | Cash & Short Term Investments - Net of Debt | Money | Total cash and short-term investments less total debt. |
| `TR.F.NetBookCap` | Net Book Capital | Money | Total shareholders' equity plus net debt. |
| `TR.F.TotBookCap` | Total Book Capital | Money | Total equity after minority interest plus total borrowings, less preferred equity. |
| `TR.F.TotCap` | Total Capital | Money | Total equity after minority interest, non-controlling interests in liabilities, plus total borrowings. |
| `TR.F.TotLTCap` | Total Long Term Capital | Money | Total shareholders' equity plus non-current liabilities, less minority interest. |
| `TR.F.NetOpAssets` | Net Operating Assets | Money | Operating assets less operating liabilities. |
| `TR.F.ShHoldEqCom` | Shareholders Equity - Common | Money | Parent-attributable equity less minority interest, hybrid equity portion and preferred shareholders' equity. |
| `TR.F.TangTotEq` | Tangible Total Equity | Money | Total equity after minority interest less net total intangible assets (including goodwill). |
| `TR.F.TangBV` | Tangible Book Value | Money | Total equity after minority interest less preferred equity and net total intangibles (including goodwill). |
| `TR.F.BVExclOthEq` | Book Value excluding Other Equity | Money | Common shareholders' equity less other reserves/equity. |
| `TR.F.TangBVExclOthEq` | Tangible Book Value excluding Other Equity | Money | Book value excluding other equity, further less net total intangible assets. |
| `TR.F.WkgCap` | Working Capital | Money | Total current assets less total current liabilities. |
| `TR.F.WkgCapNonCash` | Working Capital - Non-Cash | Money | Current assets net of cash, less current liabilities. |
| `TR.F.WkgCapExclOthCurrAssetsLiab` | Working Capital excluding Other Current Assets & Liabilities | Money | Working capital less other current assets and other current liabilities. |
| `TR.F.TotCurrAssetsExclTotInvnt` | Total Current Assets excluding Total Inventories | Money | Total current assets less total inventories (a quick-asset base). |
| `TR.F.CurrAssetsExclCashSTInvstTot` | Current Assets excluding Cash & Short Term Investments - Total | Money | Total current assets less cash and short-term investments. |
| `TR.F.CurrLiabExclCurrDebtTot` | Current Liabilities excluding Current Debt - Total | Money | Total current liabilities less short-term debt and current portion of long-term debt. |

## Access patterns

**1. A multi-period balance sheet for one company** — five annual snapshots, currency-normalised to
USD millions, with period labels attached:

```python
import lseg.data as ld
ld.open_session()
df = ld.get_data(
    universe=["AAPL.O"],
    fields=[
        "TR.F.TotAssets", "TR.F.TotCurrAssets", "TR.F.TotLiab",
        "TR.F.DebtLTTot", "TR.F.NetDebt", "TR.F.TotShHoldEq",
        "TR.F.TotAssets.fperiod",           # companion: period label
    ],
    parameters={"Period": "FY0:FY-4", "Curn": "USD", "Scale": "6"},
)
print(df)
ld.close_session()
```

**2. A cross-section across companies** — one field, one period, many names (the standard panel
build); add `.date` to pin each firm's fiscal period-end:

```python
import lseg.data as ld
ld.open_session()
df = ld.get_data(
    universe=["AAPL.O", "MSFT.O", "005930.KS", "7203.T"],
    fields=["TR.F.NetDebt", "TR.F.TotAssets",
            "TR.F.NetDebt.date", "TR.F.NetDebt.currency"],
    parameters={"Period": "FY0"},
)
print(df)
ld.close_session()
```

**3. A refinancing profile** — pull the long-term-debt maturity ladder as a standalone series (each
bucket is non-cumulative, so this reads directly as a rollover schedule):

```python
ladder = ["TR.F.DebtLTMatIn1Yr", "TR.F.DebtLTMatYr2", "TR.F.DebtLTMatYr3",
          "TR.F.DebtLTMatYr4", "TR.F.DebtLTMatYr5", "TR.F.DebtLTMatYr6Beyond"]
df = ld.get_data("XOM", ladder, {"Period": "FY0", "Curn": "USD", "Scale": "6"})
```

## Notes / gotchas

- **Case-insensitive.** Field codes resolve regardless of case (`TR.F.TotAssets` == `TR.F.TOTASSETS`).
- **Companion suffixes.** Any field takes `.date` (period-end date), `.fperiod` (period label such
  as `FY2024`) and `.currency` (reporting currency) — essential for aligning a multi-period or
  multi-company pull, since fiscal calendars and reporting currencies differ across filers.
- **Silent field drops.** An invalid or unentitled field is omitted from the result rather than
  raising — always inspect the returned columns against what you requested.
- **`TR.*` vs `TR.F.*` diverge.** The standardized `TR.F.*` figures can differ from same-named
  non-standardized `TR.*` fields (different methodology and vendor mapping). Pick the family
  deliberately — see [../usage/field-discovery.md](../usage/field-discovery.md).
- **Sector applicability.** Many line items are built for the *industrial/property* presentation and
  come back blank for banks and insurers; for financials, lean on the non-differentiated aggregates
  (`TR.F.InvstTot`, `TR.F.LoansRcvblTot`, `TR.F.OthAssetsTot`, `TR.F.CashInHandWithBanksTot`, …).
- **The maturity ladder is non-cumulative.** Each `DebtLTMat*` / `CapLeaseMat*` bucket is a
  standalone year (not a running total); range-reported maturities are placed at the top year of the
  range, and `TR.F.CapLeaseMatIntrCosts` is a negative reconciliation line, not a cash outflow.
- **Point-in-time reported values.** These are the figures as reported for each fiscal period;
  subsequent **restatements are not reflected** in the historical points. For a specific as-reported
  vintage, confirm with the filing rather than assuming the series is restatement-adjusted.
```
