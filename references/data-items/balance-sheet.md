# Balance Sheet (`TR.F.*`)

Standardized balance sheet line items (~144 fields). Use with `ld.get_data()` and
the `Period` parameter (e.g. `FY0` annual, `FQ0` quarterly). The full list can be
regenerated at any time via `TR.F.BalanceSheet.fieldname` (see
[../usage/field-discovery.md](../usage/field-discovery.md)).

| Field Code | Title |
|---|---|
| `TR.F.CashSTInvst` | Cash & Short Term Investments |
| `TR.F.CashCashEquiv` | Cash & Cash Equivalents |
| `TR.F.STInvstTot` | Short-Term Investments - Total |
| `TR.F.LoansRcvblNetST` | Loans & Receivables - Net - Short-Term |
| `TR.F.TradeAcctTradeNotesRcvblNet` | Trade Accounts & Trade Notes Receivable - Net |
| `TR.F.RcvblOthTot` | Receivables - Other - Total |
| `TR.F.InvntTot` | Inventories - Total |
| `TR.F.OthCurrAssetsTot` | Other Current Assets - Total |
| `TR.F.OthCurrAssets` | Other Current Assets |
| `TR.F.TotCurrAssets` | Total Current Assets |
| `TR.F.InvstLT` | Investments - Long-Term |
| `TR.F.InvstAFSHTMLT` | Investments - Available for Sale/Held to Maturity - Long-Term |
| `TR.F.MktSecLT` | Marketable Securities - Long-Term |
| `TR.F.PPENetTot` | Property, Plant & Equipment - Net - Total |
| `TR.F.PPEExclAssetsLeasedOutNetTot` | Property, Plant & Equipment - excluding Assets Leased Out - Net - Total |
| `TR.F.PPEGrossTot` | Property, Plant & Equipment - Gross - Total |
| `TR.F.PPEExclAssetsLeasedOutGross` | Property, Plant & Equipment - excluding Assets Leased Out - Gross |
| `TR.F.LandBuildGross` | Land & Buildings - Gross |
| `TR.F.LeasehImprovGross` | Leasehold Improvements - Gross |
| `TR.F.PlantMachEquipGross` | Plant, Machinery & Equipment - Gross |
| `TR.F.ROUTangTotGross` | Right of Use Tangible Assets - Total - Gross |
| `TR.F.ROUTangOpLeaseGross` | Right of Use Tangible Assets - Operating Lease - Gross |
| `TR.F.PPEAccumDeprTot` | Property, Plant & Equipment - Accumulated Depreciation & Impairment - Total |
| `TR.F.PPEExclAssetsLeasedOutAccumDeprTot` | Property, Plant & Equipment - excluding Assets Leased Out - Accumulated Depreciation & Impairment - Total |
| `TR.F.OthNonCurrAssetsTot` | Other Non-Current Assets - Total |
| `TR.F.DefTaxAssetLT` | Deferred Tax - Asset - Long-Term |
| `TR.F.OthNonCurrAssets` | Other Non-Current Assets |
| `TR.F.TotNonCurrAssets` | Total Non-Current Assets |
| `TR.F.TotAssets` | Total Assets |
| `TR.F.TradeAcctPbleAccrualsST` | Trade Accounts Payable & Accruals - Short-Term |
| `TR.F.TradeAcctTradeNotesPbleST` | Trade Accounts & Trade Notes Payable - Short-Term |
| `TR.F.AccrExpnST` | Accrued Expenses - Short-Term |
| `TR.F.STDebtCurrPortOfLTDebt` | Short-Term Debt & Current Portion of Long-Term Debt |
| `TR.F.STDebtNotesPble` | Short-Term Debt & Notes Payable |
| `TR.F.CurrPortOfLTDebtCapLeases` | Current Portion of Long-Term Debt including Capitalized Leases |
| `TR.F.CurrPortOfLTDebtExclCapLease` | Current Portion of Long-Term Debt excluding Capitalized Leases |
| `TR.F.CapLeaseCurrPort` | Capitalized Leases - Current Portion |
| `TR.F.IncTaxPbleST` | Income Taxes - Payable - Short-Term |
| `TR.F.OpLeaseLiabCurrPortST` | Operating Lease Liabilities - Current Portion/Short-Term |
| `TR.F.OthCurrLiabTot` | Other Current Liabilities - Total |
| `TR.F.DefIncST` | Deferred Income - Short-Term |
| `TR.F.OthCurrLiab` | Other Current Liabilities |
| `TR.F.TotCurrLiab` | Total Current Liabilities |
| `TR.F.DebtLTTot` | Debt - Long-Term - Total |
| `TR.F.LTDebtExclCapLease` | Long-Term Debt excluding Capitalized Leases |
| `TR.F.DebtNonConvertLT` | Debt - Non-Convertible - Long-Term |
| `TR.F.CapLeaseObligLT` | Capitalized Lease Obligations - Long-Term |
| `TR.F.OpLeaseLiabLT` | Operating Lease Liabilities - Long-Term |
| `TR.F.OthNonCurrLiabTot` | Other Non-Current Liabilities - Total |
| `TR.F.OthNonCurrLiab` | Other Non-Current Liabilities |
| `TR.F.TotNonCurrLiab` | Total Non-Current Liabilities |
| `TR.F.TotLiab` | Total Liabilities |
| `TR.F.ShHoldEqParentShHoldTot` | Shareholders' Equity - Attributable to Parent Shareholders - Total |
| `TR.F.ComEqParentShHold` | Common Equity Attributable to Parent Shareholders |
| `TR.F.ComEqContrib` | Common Equity - Contributed |
| `TR.F.ComStockIssuedPaid` | Common Stock - Issued & Paid |
| `TR.F.ComStockShrPremInclOptionRsrv` | Common Stock - Additional Paid in Capital including Option Reserve |
| `TR.F.EqNonContribRsrvRetainedEarn` | Equity - Non-Contributed - Reserves & Retained Earnings |
| `TR.F.RetainedEarnTot` | Retained Earnings - Total |
| `TR.F.ComprIncAccumTot` | Comprehensive Income - Accumulated - Total |
| `TR.F.ComEqTot` | Common Equity - Total |
| `TR.F.TotShHoldEq` | Total Shareholders' Equity - including Minority Interest & Hybrid Debt |
| `TR.F.TotLiabEq` | Total Liabilities & Equity |
| `TR.F.ComShrIssuedTot` | Common Shares - Issued - Total |
| `TR.F.ComShrOutsTot` | Common Shares - Outstanding - Total |
| `TR.F.ComShrTrezTot` | Common Shares - Treasury - Total |
| `TR.F.ComShrAuthIssue` | Common Shares - Authorized - Issue Specific |
| `TR.F.ComShrIssuedIssue` | Common Shares - Issued - Issue Specific |
| `TR.F.ComShrOutsIssue` | Common Shares - Outstanding - Issue Specific |
| `TR.F.ComShrTrezIssue` | Common Shares - Treasury - Issue Specific |
| `TR.F.AssetAllocFactorIssue` | Asset Allocation Factor - Issue Specific |
| `TR.F.ROUTangTotNetSuppl` | Right of Use Tangible Assets - Total - Net - Supplemental |
| `TR.F.ROUTangOpLeaseNetSuppl` | Right of Use Tangible Assets - Operating Lease - Net - Supplemental |
| `TR.F.ROUTangCapFinLeaseNetSuppl` | Right of Use Tangible Assets - Capital/Finance Lease - Net - Supplemental |
| `TR.F.PPEExclROUTangCapLeaseNetSuppl` | Property, Plant & Equipment - excluding Right of Use Tangible Assets & Capital Leases - Net - Supplemental |
| `TR.F.TotOpLeaseLiabSuppl` | Total Operating Lease Liabilities - Supplemental |
| `TR.F.OpLeaseLiabCurrPortSTSuppl` | Operating Lease Liabilities - Current Portion/Short-Term - Supplemental |
| `TR.F.OpLeaseLiabLTSuppl` | Operating Lease Liabilities - Long-Term - Supplemental |
| `TR.F.FinOpLeaseLiabTotSuppl` | Finance and Operating Lease Liabilities - Total - Supplemental |
| `TR.F.DebtInclFinOpLeaseLiabSuppl` | Debt including Finance and Operating Lease Liabilities - Supplemental |
| `TR.F.InvstTot` | Investments - Total |
| `TR.F.LoansRcvblTot` | Loans & Receivables - Total |
| `TR.F.OthAssetsTot` | Other Assets - Total |
| `TR.F.IncTaxPbleLTST` | Income Taxes - Payable - Long-Term & Short-Term |
| `TR.F.PbleAccrExpn` | Payables & Accrued Expenses |
| `TR.F.TradeAcctPbleTot` | Trade Account Payables - Total |
| `TR.F.AccrExpn` | Accrued Expenses |
| `TR.F.NetDebt` | Net Debt |
| `TR.F.DebtTot` | Debt - Total |
| `TR.F.DebtLTMatTot` | Debt - Long-Term - Maturities - Total |
| `TR.F.DebtLTMatIn1Yr` | Debt - Long-Term - Maturities - within 1 Year |
| `TR.F.DebtLTMatYr2` | Debt - Long-Term - Maturities - Year 2 |
| `TR.F.DebtLTMatYr3` | Debt - Long-Term - Maturities - Year 3 |
| `TR.F.DebtLTMatYr4` | Debt - Long-Term - Maturities - Year 4 |
| `TR.F.DebtLTMatYr5` | Debt - Long-Term - Maturities - Year 5 |
| `TR.F.DebtLTMatRemain` | Debt - Long-Term - Maturities - Remaining |
| `TR.F.DebtLTMat23Yr` | Debt - Long-Term - Maturities - 2-3 Years |
| `TR.F.DebtLTMat45Yr` | Debt - Long-Term - Maturities - 4-5 Years |
| `TR.F.DebtLTMatYr6Beyond` | Debt - Long-Term - Maturities - Year 6 & Beyond |
| `TR.F.CapLeaseMatTot` | Capital Lease Maturities - Total |
| `TR.F.CapLeaseMatDueIn1Yr` | Capital Lease Maturities - Due within 1 Year |
| `TR.F.CapLeaseMatDueInYr2` | Capital Lease Maturities - Due in Year 2 |
| `TR.F.CapLeaseMatDueInYr3` | Capital Lease Maturities - Due in Year 3 |
| `TR.F.CapLeaseMatDueInYr4` | Capital Lease Maturities - Due in Year 4 |
| `TR.F.CapLeaseMatDueInYr5` | Capital Lease Maturities - Due in Year 5 |
| `TR.F.CapLeaseMatRemainMat` | Capital Lease Maturities - Remaining Maturities |
| `TR.F.CapLeaseMatIntrCosts` | Capital Lease Maturities - Interest Costs |
| `TR.F.CapLeaseMatDueIn23Yr` | Capital Lease Maturities - Due in 2-3 Years |
| `TR.F.CapLeaseMatDueIn45Yr` | Capital Lease Maturities - Due in 4-5 Years |
| `TR.F.CapLeaseMatDueInYr6Beyond` | Capital Lease Maturities - Due in Year 6 & Beyond |
| `TR.F.AccrualsST` | Accruals - Short-Term |
| `TR.F.AssetAccruals` | Asset Accruals |
| `TR.F.CashCashEquivTot` | Cash & Cash Equivalents - Total |
| `TR.F.CashSTInvstTot` | Cash & Short Term Investments - Total |
| `TR.F.DebtInclPrefEqMinIntrTot` | Debt - including Preferred Equity & Minority Interest - Total |
| `TR.F.InvstPermanent` | Investments - Permanent |
| `TR.F.NetBookCap` | Net Book Capital |
| `TR.F.NetOpAssets` | Net Operating Assets |
| `TR.F.ShHoldEqCom` | Shareholders Equity - Common |
| `TR.F.CashSTInvstNetOfDebt` | Cash & Short Term Investments - Net of Debt |
| `TR.F.TangTotEq` | Tangible Total Equity |
| `TR.F.TangBV` | Tangible Book Value |
| `TR.F.CurrPortOfLTDebtCapLeasesHybrid` | Current Portion of Long-Term Debt including Capitalized Leases & Hybrid Financial Instruments |
| `TR.F.TotBookCap` | Total Book Capital |
| `TR.F.TotCap` | Total Capital |
| `TR.F.TotLTCap` | Total Long Term Capital |
| `TR.F.TotFixedAssetsNet` | Total Fixed Assets - Net |
| `TR.F.UnearnRevTot` | Unearned Revenue - Total |
| `TR.F.WkgCap` | Working Capital |
| `TR.F.IntrBearLiabTot` | Interest Bearing Liabilities - Total |
| `TR.F.WkgCapNonCash` | Working Capital - Non-Cash |
| `TR.F.WkgCapExclOthCurrAssetsLiab` | Working Capital excluding Other Current Assets & Liabilities |
| `TR.F.BVExclOthEq` | Book Value excluding Other Equity |
| `TR.F.NetDebtInclPrefEqMinIntr` | Net Debt Including Preferred Equity & Minority Interest |
| `TR.F.OthSTLTAssetsTot` | Other Short-Term & Long-Term Assets - Total |
| `TR.F.OthSTLTLiabTot` | Other Short-Term & Long-Term Liabilities - Total |
| `TR.F.TotCurrAssetsExclTotInvnt` | Total Current Assets excluding Total Inventories |
| `TR.F.TangBVExclOthEq` | Tangible Book Value excluding Other Equity |
| `TR.F.TotDebtExclIslamic` | Total Debt Excluding Islamic |
| `TR.F.TradeAcctTradeNotesRcvblNetTot` | Trade Accounts & Trade Notes Receivable - Net - Total |
| `TR.F.CurrLiabExclCurrDebtTot` | Current Liabilities excluding Current Debt - Total |
| `TR.F.CurrAssetsExclCashSTInvstTot` | Current Assets excluding Cash & Short Term Investments - Total |
| `TR.F.CashSTInvstAcctRcvblTot` | Cash, Short Term Investments & Accounts Receivable - Total |
| `TR.F.CashInHandWithBanksTot` | Cash in Hand & with Banks - Total |
