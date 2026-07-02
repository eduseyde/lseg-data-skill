# Funds & ETFs (`TR.Fund*`, Lipper)

Descriptive, holdings, allocation, flow, performance, ratings and ESG data for **mutual funds and ETFs**, sourced from **LSEG Lipper**. Every field below carries the `parent_category` **Lipper Funds** and was enumerated live from the MCP field catalogue (`search_fields`): **281 fields across 11 families**. A separate ETF-scores family is documented at the end.

> **Entitlement caveat (important).** The whole Lipper Funds family is a **separately licensed module**. On a login without the Lipper entitlement, *every* field here returns `access to field(s) denied` — even basic descriptors like `TR.FundName` — while the symbol itself still resolves normally. If you get blanket denials on a valid fund RIC, it is a licensing gap, not a bad query. As a fallback, a quarterly Lipper holdings panel also lives in BigQuery (`nexus-data-24.lipper`), from which allocations can be rebuilt.

## How to address a fund

Use the fund/ETF RIC as the `universe` (e.g. `"SPY"`), or the Lipper `LP########` code for open-end funds. `convert_symbols` maps an ISIN to the Lipper code (`asset_class="FUNDS"`).

## Three access patterns

1. **Single value (current):** Overview, Benchmark, Lipper Ratings, Responsible Investments — one row per fund.
2. **Multi-row breakdown (per snapshot):** Summary Holdings and Fund Holdings return many rows; pass `SDate` for a point-in-time snapshot and loop period-ends for history.
3. **Time series:** Price & Performance History, Asset Value flows and Corporate Action History accept `SDate`/`EDate` + `Frq` (`D`/`W`/`M`). Quantitative Analysis stats are computed to a reference point (last month end / yesterday / inception).

## Fund Overview (38)

Static descriptive and reference data for a fund or ETF: identity, legal form, domicile, base currency, launch date, people and companies behind it, stated objective, the fee schedule, minimum investments, dividend policy, and where it is registered for sale. Almost all are a **single value per fund** (the current state); `TR.FundTER` carries a companion `TR.FundTERDate`. This is where **countries registered for sale** live: `TR.FundRegisteredCountry` (one row per country of registration) and the `TR.FundRegisterCountryofSalesFlag` toggle.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.FundClassificationSectorName` | Classification Sector Name | String | Sector to which the fund belongs for comparative purposes. |
| `TR.FundClassificationSectorScheme` | Classification Sector Scheme | String | The Sector Scheme to which the fund belongs for comparative purposes. |
| `TR.FundCompany` | Fund Company | String | Fund Company. |
| `TR.FundCrossReferenceIdentifiers` | Cross Reference Identifiers | String | Third party codes allocated to funds by other associations, allowing the fund to be cross-referenced. |
| `TR.FundCrossReferenceIdentifiersType` | Identifier Type | String | The third party association code name used for the listed cross-reference code. |
| `TR.FundCurrAnnualCharge` | Current Annual Charge | Money | Current level of annual charge applicable at the expense of the Net Asset Value of a fund. |
| `TR.FundCurrInitialCharge` | Current Initial Charge | Money | Current fee that the fund charges the investors when they enter the fund. |
| `TR.FundCurrRedemptionCharge` | Current Redemption Charge | Money | Current level of commission charged by a mutual fund company when an investor redeems shares. |
| `TR.FundCurrency` | Currency | Currency | The currency in which the fund price data is published. |
| `TR.FundCustodian` | Custodian | String | The company responsible for the safekeeping of all the legal documents and financial assets. |
| `TR.FundDividendPayment` | Dividend Payment | Float | Dividend Payment. |
| `TR.FundDomicile` | Domicile | String | The jurisdiction in which a fund is legally incorporated. |
| `TR.FundDomicileCode` | Domicile Code | String | The jurisdiction under which the fund is legally incorporated. |
| `TR.FundExDividendDate` | Ex Dividend Date | Date | The date on which a fund's net asset value will fall by an amount equal to a dividend or capital gains distribution. |
| `TR.FundGeographicFocus` | Geographic Focus | String | Main Countries or regions areas where the fund invests. |
| `TR.FundIncDistributionIndicator` | Income Distribution Indicator | String | Indicates whether fund distributes or accumulates income. |
| `TR.FundLaunchDate` | Launch Date | String | The date that the subscription period for a fund ends. Not Earlier than IPO date. |
| `TR.FundLegalStructure` | Legal Structure | String | Legal structure may be, for example, Unit Trust, SICAV, UCITS, OEIC, Fondo de Inversion, Investmentfonds, Zbrige, Fonds etc. |
| `TR.FundMaxAnnualCharge` | Maximum Annual Charge | Money | Maximum level of annual recurring charge applicable at the expense of the Net Asset Value of a fund. |
| `TR.FundMaxInitialCharge` | Maximum Initial Charge | Money | Maximum fee that the fund charges the investors when they enter the fund. |
| `TR.FundMaxRedemptionCharge` | Maximum Redemption Charge | Money | Maximum level of commission charged by a mutual fund company when an investor redeems shares. |
| `TR.FundMinAccBalance` | Minimum Account Balance (Value) | Money | Minimum monetary value that the investor must maintain in the fund. |
| `TR.FundMinAnnualCharge` | Minimum Annual Charge | Money | Minimum level of annual recurring charge applicable at the expense of the Net Asset Value of a fund. |
| `TR.FundMinInitialCharge` | Minimum Initial Charge | Money | Minimum fee that the fund charges the investors when they enter the fund. |
| `TR.FundMinInitialInv` | Minimum Initial Investment | Money | Minimum number of shares or currency amount that investors must purchase. |
| `TR.FundMinIrregularInv` | Minimum Irregular Investment | Money | Minimum number of shares or currency amount that investors can subsequently invest (on an ad hoc basis) in the fund after initial shares are purchased. |
| `TR.FundMinRedemptionCharge` | Minimum Redemption Charge | Money | Minimum level of commission charged by a mutual fund company when an investor redeems shares. |
| `TR.FundMinRegularInv` | Minimum Regular Investment | Money | Minimum amount of investment accepted on a regular basis. |
| `TR.FundName` | Fund Name | String | Fund Name. |
| `TR.FundNumberOfDividendPaymentPerYear` | Number Of Dividend Payment Per Year | Integer | Number Of Dividend Payment Per Year. |
| `TR.FundObjective` | Objective | String | The published fund objective or investment guidelines and the date they were recorded. |
| `TR.FundPortfolioManager` | Portfolio Manager | String | Company responsible for actually managing the investment of the available funds. |
| `TR.FundProjectedYield` | Projected Yield | Float | Percentage of income earned as a proportion of the total return performance over a one year period as of the latest month end |
| `TR.FundRegisterCountryofSalesFlag` | Register Country of Sales Flag | String | The country in which a fund is sold, based on registration with a local regulatory body. |
| `TR.FundRegisteredCountry` | Country of Registration | String | The country in which a fund is sold, based on registration with a local regulatory body. |
| `TR.FundTER` | Total Expense Ratio | Float | Total expense ratio for the fund. |
| `TR.FundTERDate` | Total Expense Ratio Date | Date | Date when the total expense ratio is calculated for the fund. |
| `TR.FundType` | Fund Type | String | Fund Type. |

## Benchmark Details (4)

The fund's declared benchmark identity: its name, the RIC and internal code you can use to pull the benchmark's own series, and the benchmark type. One value each.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.FundBenchmarkInstrumentCode` | Benchmark Instrument Code | String | Benchmark Instrument Code. |
| `TR.FundBenchmarkInstrumentRIC` | Benchmark Instrument RIC | String | Benchmark instrument RIC. |
| `TR.FundBenchmarkName` | Benchmark Name | String | Benchmark Name. |
| `TR.FundBenchmarkType` | Benchmark Type | String | Benchmark Type, there are three different types of Benchmarch, Techinical Indicator, Risk Free and Asset Manager. |

## Summary Holdings (7)

The **pre-computed allocation summaries** and the top-ten concentration figure. Each allocation field returns **one row per bucket** (one row per currency, per country, etc.) as a **percentage of Total Net Assets**, and is dated via `TR.FundAllocationDate` so it forms a historical series. See the deep dive immediately below this table for how to query them correctly.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.FundAllocationDate` | Allocation Date | Date | The date the allocation applies to. |
| `TR.FundAllocationName` | Allocation Name | String | The name of the entity that the allocation applies to. |
| `TR.FundAssetAllocation` | Asset Allocation % of TNA | Percentage | The Asset Allocation of the fund expressed as a percentage of Total Net Assets |
| `TR.FundCountryAllocation` | Country Allocation % of TNA | Percentage | The Country Allocation of assets in the fund expressed and a percentage of the total net assets. |
| `TR.FundCurrencyAllocation` | Currency Allocation % of TNA | Percentage | The Currency Allocation of assets in the fund expressed and a percentage of total net assets |
| `TR.FundIndustrySectorAllocation` | Industry Allocation % of TNA | Percentage | The Industry Sector Allocation of the fund expressed as a percentage of TNA |
| `TR.FundTopTenHoldings` | Top Ten Holdings % of TNA | Percentage | The top ten holders of the fund expressed as Total Net Assets |

### Asset allocation — how to query it

The four allocation dimensions are the heart of this family:

| Dimension | Field | Breaks the fund down by |
|---|---|---|
| Asset type | `TR.FundAssetAllocation` | equity / bond / cash / other |
| Currency | `TR.FundCurrencyAllocation` | currency of the underlying assets |
| Country | `TR.FundCountryAllocation` | country / geography of the underlying assets |
| Industry / sector | `TR.FundIndustrySectorAllocation` | industry sector |

Rules of the road:

- **One dimension per request.** Each allocation field returns one row per bucket, and the
  number of buckets differs across dimensions (a fund may span 30 countries but 3 currencies).
  Always pair the chosen dimension with `TR.FundAllocationName` (the bucket label) and
  `TR.FundAllocationDate` (the as-of date). Mixing two allocation fields in one call makes the
  Name column ambiguous.
- **Percentages sum to ~100%** within a single dimension, expressed as a share of Total Net Assets.
- **It is historical.** Pass an as-of date via `parameters={"SDate": "YYYY-MM-DD"}`, and loop over
  period-ends to assemble a time series. (The standalone script `lseg_spy_allocation.py` in
  `share/lseg-toolkit/standalone/` does exactly this.)
- **`TR.FundTopTenHoldings` is a lone percentage field** — it returns the ten largest weights but
  carries **no** name or RIC companion. To know *what* the top holdings are, use the Fund Holdings
  family below (pull the full portfolio and sort by weight); that gives names, identifiers and weights.

Example — SPY's currency allocation, one snapshot:

```python
import lseg.data as ld
ld.open_session()
df = ld.get_data(
    universe=["SPY"],
    fields=["TR.FundAllocationName", "TR.FundCurrencyAllocation", "TR.FundAllocationDate"],
    parameters={"SDate": "2023-12-31"},
)
print(df)
ld.close_session()
```


## Fund Holdings (7)

The **full portfolio, security by security** (one row per position). Requesting `TR.FundHoldingName` returns every holding; pair it with weight and identifier. Pass an as-of date (`SDate`) to get the portfolio as it stood on that date, and step through period-ends to build a historical panel. Note the detail is lean (name, identifier, shares, weight, share-change, country, filing date) — there is **no per-holding market value or asset-type field**; derive those by joining `TR.FundHoldingRIC` to security reference/pricing data.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.FundCountryOfDomicile` | Country of Domicile | String | Country of domicile. |
| `TR.FundHoldingName` | Holding Name | String | Holding Name. |
| `TR.FundHoldingRIC` | Holding RIC | String | Holding RIC. |
| `TR.FundLatestFilingDate` | Latest Filing Date | Date | Latest filing date. |
| `TR.FundNumberOfShares` | Number of Shares | Integer | Number of shares held. |
| `TR.FundNumberOfSharesChanged` | Number of Shares Changed | Integer | Number of shares changed, where "-" means decrease in number of shares held and positive value means increase in number of shares held. Third option is "No information". |
| `TR.FundPercentageOfFundAssets` | Percentage of Fund Assets | Percentage | Percentage of fund assets. |

Example — SPY's full portfolio (current), sorted to the top holdings:

```python
import lseg.data as ld
ld.open_session()
df = ld.get_data(
    universe=["SPY"],
    fields=["TR.FundHoldingName", "TR.FundHoldingRIC",
            "TR.FundPercentageOfFundAssets", "TR.FundNumberOfShares"],
)
print(len(df), "holdings")
print(df.sort_values("Percentage of Fund Assets", ascending=False).head(10))
ld.close_session()
```


## Price & Performance History (9)

The fund's own **price and size time series**: NAV, bid, mid and offer prices, matching 'is estimated' flags, and Total Net Assets (the fund's size). Genuine time series — query with `SDate`/`EDate` and a frequency (`D`/`W`/`M`).

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.FundBid` | Bid | Money | Bid price. |
| `TR.FundIsBidEstFlag` | Is Bid Estimated Flag | Boolean | Confirms if Bid is an estimated value. |
| `TR.FundIsMidEstFlag` | Is Mid Estimated Flag | Boolean | Confirms if Mid is an estimated value. |
| `TR.FundIsNAVEstFlag` | Is NAV Estimated Flag | Boolean | Confirms if NAV is an estimated value. |
| `TR.FundIsOfferEstFlag` | Is Offer Estimated Flag | Boolean | Confirms if Offer is an estimated value. |
| `TR.FundMid` | Mid | Money | Represents price at which an asset was last traded. |
| `TR.FundNAV` | NAV | Money | The market worth of one share of a mutual fund. This figure is derived by taking a fund's total assets (securities, cash and any accrued earnings), deducting liabilities, and dividing by the number of shares outstanding. |
| `TR.FundOffer` | Offer | Money | Offer Price. |
| `TR.FundTotalNetAssets` | Total Net Assets | Money | Value of the underlying holdings within a portfolio net of expenses. |

## Asset Value (19)

**Flows, dealing and standardized performance.** This family carries subscription and redemption activity — daily inflows/outflows, gross sales, redemption amounts and their ratios — plus the number of investors, settlement periods, capital-guarantee percentage, US-SEC standardized performance, and a couple of German tax items (Zwist, EU-tax non-grandfathered share). The flow fields are the most useful here for capital-flow research.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.FundDailyOutflows` | Daily Outflows | Float | Daily net amount withdrawn from the fund through redemptions. |
| `TR.FundDailyinflows` | Daily Inflows | Float | Daily net amount received by the fund from new subscriptions. |
| `TR.FundEuTaxNonGfPct` | EU Tax Non-Grandfathered Percentage | Float | Percentage of fund's assets invested in debt claims with non-grandfathered status (value can be a percentage or N/A). |
| `TR.FundGrossSales` | Gross Sales | Float | The actual amount of new receipts into a fund as of the fund's fiscal year-end. This information is retrieved directly from the fund's audited annual report. Totals are reported in millions. |
| `TR.FundGrossSalesRat` | Gross Sales Ratio | Float | Annual gross sales of a fund expressed as a percentage of Average Net Assets (ANA). |
| `TR.FundNAVDisplUnit` | NAV Display Unit | Integer | It's the NAV unit value defining how many times NAV is priced and displayed. |
| `TR.FundNoOfInvestors` | Number of Investors | Float | Total number of individual or institutional investors holding shares (quotas) in the fund. |
| `TR.FundPctGuarantee` | % Guarantee | Float | The % the capital invested by the shareholder that is guaranteed to be returned to the investor when the fund matures. If the guarantee percentage above 100%, return on investment plus the percentage over the initial investment is protected on the expiry date. If the guarantee percentage below 100%, only that portion of initial investment is protected upon the expiry date of the fund. Please note that most funds apply the guarantee to investor's capital before fee and expenses. |
| `TR.FundRedemptAmount` | Redemption Amount | Float | The actual amount of withdrawals out of a fund as of fiscal year-end. This information is retrieved directly from the fund's audited annual report. Totals are reported in thousands. |
| `TR.FundRedemptRatio` | Redemption Ratio | Float | Annual redemptions from a fund expressed as a percentage of Average Net Assets (ANA). |
| `TR.FundRedemptSettlPerDays` | Redemption Settlement Period (days) | Float | Number of business days between the subscription request date and the date when the payment is processed (T+N). |
| `TR.FundSEC10YearPerf` | SEC 10 Year Performance | Float | SEC Return is the SEC standardized pre-tax total return net of maximum loads, fees and charges. SEC returns are required by SEC for 1-year, 5-year, and 10-year periods or since inception and are presented on an annualized basis. |
| `TR.FundSEC1YearPerf` | SEC 1 Year Performance | Float | SEC Return is the SEC standardized pre-tax total return net of maximum loads, fees and charges. SEC returns are required by SEC for 1-year, 5-year, and 10-year periods or since inception and are presented on an annualized basis. |
| `TR.FundSEC3YearPerf` | SEC 3 Year Performance | Float | SEC Return is the SEC standardized pre-tax total return net of maximum loads, fees and charges. SEC returns are required by SEC for 1-year, 5-year, and 10-year periods or since inception and are presented on an annualized basis. |
| `TR.FundSEC5YearPerf` | SEC 5 Year Performance | Float | SEC Return is the SEC standardized pre-tax total return net of maximum loads, fees and charges. SEC returns are required by SEC for 1-year, 5-year, and 10-year periods or since inception and are presented on an annualized basis. |
| `TR.FundSECSIncPerf` | SEC Since Inception Performance | Float | SEC Return is the SEC standardized pre-tax total return net of maximum loads, fees and charges. SEC returns are required by SEC for 1-year, 5-year, and 10-year periods or since inception and are presented on an annualized basis. |
| `TR.FundSubsSettlPerDays` | Subscription Settlement Period (days) | Float | Number of business days between the subscription request date and the date when the fund shares are issued (T+N). |
| `TR.FundZwist` | Zwist | Float | The Zwist value is the percentage of a fund's distributions refundable to investors as a result of corporate income and withholding taxes paid by the fund. Applicable to German funds. |
| `TR.FundZwistMaxDate` | Zwist Max Date | Date | The maximum date that the Zwist value is refunded to the investor. |

## Quantitative Analysis (72)

**Computed performance and risk statistics**, mostly measured over rolling 1/3/5/10-year windows 'to Last Month End' (a few also 'to Yesterday'). Returns (1M through 10Y, YTD, since inception), performance relative to the benchmark, and the full risk/return toolkit: alpha, beta, correlation, R-squared, tracking error, information ratio, Sharpe, Treynor, standard deviation, max drawdown, return/risk ratio, and best/worst 3-month figures. Each is a point-in-time computed value.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.Fund10YearPerf` | 10 Year Performance to Last Month End | Percentage | Takes into account not only the capital gains of an investment but also the income yield from dividends or interest payments. The calculation of total return is based on the assumption that interest payments or dividends are immediately reinvested. Value is measured for last 10 years. |
| `TR.Fund10YearPerftoYesterday` | 10 Year Performance to Yesterday | Percentage | Takes into account not only the capital gains of an investment but also the income yield from dividends or interest payments. The calculation of total return is based on the assumption that interest payments or dividends are immediately reinvested. Value is measured on a 10 year period ending yesterday. |
| `TR.Fund1MnthPerf` | 1 Month Performance to Last Month End | Percentage | Takes into account not only the capital gains of an investment but also the income yield from dividends or interest payments. The calculation of total return is based on the assumption that interest payments or dividends are immediately reinvested. Value is measured for the last month. |
| `TR.Fund1MnthPerftoYesterday` | 1 Month Performance to Yesterday | Percentage | Takes into account not only the capital gains of an investment but also the income yield from dividends or interest payments. The calculation of total return is based on the assumption that interest payments or dividends are immediately reinvested. Value is measured on a 1 month period ending yesterday. |
| `TR.Fund1YearPerf` | 1 Year Performance to Last Month End | Percentage | Takes into account not only the capital gains of an investment but also the income yield from dividends or interest payments. The calculation of total return is based on the assumption that interest payments or dividends are immediately reinvested. Value is measured for last year. |
| `TR.Fund1YearPerftoYesterday` | 1 Year Performance to Yesterday | Percentage | Takes into account not only the capital gains of an investment but also the income yield from dividends or interest payments. The calculation of total return is based on the assumption that interest payments or dividends are immediately reinvested. Value is measured on a 1 year period ending yesterday. |
| `TR.Fund3MnthPerf` | 3 Month Performance to Last Month End | Percentage | Takes into account not only the capital gains of an investment but also the income yield from dividends or interest payments. The calculation of total return is based on the assumption that interest payments or dividends are immediately reinvested. Value is measured for last 3 months. |
| `TR.Fund3MnthPerftoYesterday` | 3 Month Performance to Yesterday | Percentage | Takes into account not only the capital gains of an investment but also the income yield from dividends or interest payments. The calculation of total return is based on the assumption that interest payments or dividends are immediately reinvested. Value is measured on a 3 month period ending yesterday. |
| `TR.Fund3YearPerf` | 3 Year Performance to Last Month End | Percentage | Takes into account not only the capital gains of an investment but also the income yield from dividends or interest payments. The calculation of total return is based on the assumption that interest payments or dividends are immediately reinvested. Value is measured for last 3 years. |
| `TR.Fund3YearPerftoYesterday` | 3 Year Performance to Yesterday | Percentage | Takes into account not only the capital gains of an investment but also the income yield from dividends or interest payments. The calculation of total return is based on the assumption that interest payments or dividends are immediately reinvested. Value is measured on a 3 year period ending yesterday. |
| `TR.Fund5YearPerf` | 5 Year Performance to Last Month End | Percentage | Takes into account not only the capital gains of an investment but also the income yield from dividends or interest payments. The calculation of total return is based on the assumption that interest payments or dividends are immediately reinvested. Value is measured for last 5 years. |
| `TR.Fund5YearPerftoYesterday` | 5 Year Performance to Yesterday | Percentage | Takes into account not only the capital gains of an investment but also the income yield from dividends or interest payments. The calculation of total return is based on the assumption that interest payments or dividends are immediately reinvested. Value is measured on a 5 year period ending yesterday. |
| `TR.Fund6MnthPerf` | 6 Month Performance to Last Month End | Percentage | Takes into account not only the capital gains of an investment but also the income yield from dividends or interest payments. The calculation of total return is based on the assumption that interest payments or dividends are immediately reinvested. Value is measured for last 6 months. |
| `TR.Fund6MnthPerftoYesterday` | 6 Month Performance to Yesterday | Percentage | Takes into account not only the capital gains of an investment but also the income yield from dividends or interest payments. The calculation of total return is based on the assumption that interest payments or dividends are immediately reinvested. Value is measured on a 6 month period ending yesterday. |
| `TR.FundAlpha10Year` | Alpha for 10 Years to Last Month End | Float | 10 years measure of selection risk of a mutual fund in relation to the market. |
| `TR.FundAlpha1Year` | Alpha for 1 Year to Last Month End | Float | 1 year measure of selection risk of a mutual fund in relation to the market. |
| `TR.FundAlpha3Year` | Alpha for 3 Years to Last Month End | Float | 3 years measure of selection risk of a mutual fund in relation to the market. |
| `TR.FundAlpha5Year` | Alpha for 5 Years to Last Month End | Float | 5 years measure of selection risk of a mutual fund in relation to the market. |
| `TR.FundBest3Mnth` | Best 3 Months within the Last 3 Years to Last Month End | Percentage | Best three-month return over the last three years to the prior month end. |
| `TR.FundBeta10Year` | Beta for 10 Years to Last Month End | Float | 10 years market risk measure employed primarily in the equity markets. It measures the systematic risk of a single instrument or an entire portfolio. |
| `TR.FundBeta1Year` | Beta for 1 Year to Last Month End | Float | 1 year market risk measure employed primarily in the equity markets. It measures the systematic risk of a single instrument or an entire portfolio. |
| `TR.FundBeta3Year` | Beta for 3 Years to Last Month End | Float | 3 years market risk measure employed primarily in the equity markets. It measures the systematic risk of a single instrument or an entire portfolio. |
| `TR.FundBeta5Year` | Beta for 5 Years to Last Month End | Float | 5 years market risk measure employed primarily in the equity markets. It measures the systematic risk of a single instrument or an entire portfolio. |
| `TR.FundCorrelation10Year` | Correlation for 10 Years to Last Month End | Float | 10 years measure of the strength of the linear relationship between fund performance and benchmark performance. |
| `TR.FundCorrelation1Year` | Correlation for 1 Year to Last Month End | Float | 1 year measure of the strength of the linear relationship between fund performance and benchmark performance. |
| `TR.FundCorrelation3Year` | Correlation for 3 Years to Last Month End | Float | 3 years measure of the strength of the linear relationship between fund performance and benchmark performance. |
| `TR.FundCorrelation5Year` | Correlation for 5 Years to Last Month End | Float | 5 years measure of the strength of the linear relationship between fund performance and benchmark performance. |
| `TR.FundInfoRatio10Year` | Information Ratio for 10 Years to Last Month End | Float | 10 years ratio of annualized expected Residual Return to residual risk. |
| `TR.FundInfoRatio1Year` | Information Ratio for 1 Year to Last Month End | Float | 1 year ratio of annualized expected Residual Return to residual risk. |
| `TR.FundInfoRatio3Year` | Information Ratio for 3 Years to Last Month End | Float | 3 years ratio of annualized expected Residual Return to residual risk. |
| `TR.FundInfoRatio5Year` | Information Ratio for 5 Years to Last Month End | Float | 5 years ratio of annualized expected Residual Return to residual risk. |
| `TR.FundMaxDrawDown10Year` | Max Drawdown for 10 Years to Last Month End | Float | Represents the most negative cumulative return within last 10 years. |
| `TR.FundMaxDrawDown1Year` | Max Drawdown for 1 Year to Last Month End | Float | Represents the most negative cumulative return within last year. |
| `TR.FundMaxDrawDown3Year` | Max Drawdown for 3 Years to Last Month End | Float | Represents the most negative cumulative return within last 3 years. |
| `TR.FundMaxDrawDown5Year` | Max Drawdown for 5 Years to Last Month End | Float | Represents the most negative cumulative return within last 5 years. |
| `TR.FundPerfSinceIncepttoYesterday` | Performance From Inception to Yesterday | Percentage | Takes into account not only the capital gains of an investment but also the income yield from dividends or interest payments. The calculation of total return is based on the assumption that interest payments or dividends are immediately reinvested. Value is measured since inception up until yesterday. |
| `TR.FundRSq10Year` | R-Squared for 10 Years to Last Month End | Float | 10 years measurement of how closely a portfolio's performance correlates with the performance of a benchmark index, such as the S&P 500, and thus a measurement of what portion of its performance can be explained by the performance of the overall market or index. |
| `TR.FundRSq1Year` | R-Squared for 1 Year to Last Month End | Float | 1 year measurement of how closely a portfolio's performance correlates with the performance of a benchmark index, such as the S&P 500, and thus a measurement of what portion of its performance can be explained by the performance of the overall market or index. |
| `TR.FundRSq3Year` | R-Squared for 3 Years to Last Month End | Float | 3 years measurement of how closely a portfolio's performance correlates with the performance of a benchmark index, such as the S&P 500, and thus a measurement of what portion of its performance can be explained by the performance of the overall market or index. |
| `TR.FundRSq5Year` | R-Squared for 5 Years to Last Month End | Float | 5 years measurement of how closely a portfolio's performance correlates with the performance of a benchmark index, such as the S&P 500, and thus a measurement of what portion of its performance can be explained by the performance of the overall market or index. |
| `TR.FundRelPerf10Year` | Relative Performance for 10 Years to Last Month End, (%) | Percentage | The difference (in percentage format) between the total return of the fund and the total return of its reference index (Out or under performance) measured in last 10 years. |
| `TR.FundRelPerf1Year` | Relative Performance for 1 Year to Last Month End, (%) | Percentage | The difference (in percentage format) between the total return of the fund and the total return of its reference index (Out or under performance) measured in last year. |
| `TR.FundRelPerf3Year` | Relative Performance for 3 Years to Last Month End, (%) | Percentage | The difference (in percentage format) between the total return of the fund and the total return of its reference index (Out or under performance) measured in last 3 years. |
| `TR.FundRelPerf5Year` | Relative Performance for 5 Years to Last Month End, (%) | Percentage | The difference (in percentage format) between the total return of the fund and the total return of its reference index (Out or under performance) measured in last 5 years. |
| `TR.FundRelPerf6Mnth` | Relative Performance for 6 Months to Last Month End, (%) | Percentage | The difference (in percentage format) between the total return of the fund and the total return of its reference index (Out or under performance) measured in last 6 months. |
| `TR.FundRelativePerf1Mnths` | Relative Performance for 1 Month to Last Month End, (%) | Percentage | The difference (in percentage format) between the total return of the fund and the total return of its reference index (Out or under performance) measured in last month. |
| `TR.FundRelativePerf1Year` | Relative Performance Year to Month End, (%) | Percentage | The difference (in percentage format) between the total return of the fund and the total return of its reference index (Out or under performance) measured in last year. |
| `TR.FundRelativePerf3Mnths` | Relative Performance for 3 Months to Last Month End, (%) | Percentage | The difference (in percentage format) between the total return of the fund and the total return of its reference index (Out or under performance) measured in last 3 months. |
| `TR.FundRelativePerfSinceIncept` | Performance From Inception to Last Month End | Percentage | Takes into account not only the capital gains of an investment but also the income yield from dividends or interest payments. The calculation of total return is based on the assumption that interest payments or dividends are immediately reinvested. Value is measured for lifetime of the fund. |
| `TR.FundRiskToReturnRatio10Year` | Return/Risk Ratio for 10 Years to Last Month End | Float | 10 years ratio of relationship of substantial reward corresponding to the amount of risk taken. |
| `TR.FundRiskToReturnRatio1Year` | Return/Risk Ratio for 1 Year to Last Month End | Float | 1 year ratio of relationship of substantial reward corresponding to the amount of risk taken. |
| `TR.FundRiskToReturnRatio3Year` | Return/Risk Ratio for 3 Years to Last Month End | Float | 3 years ratio of relationship of substantial reward corresponding to the amount of risk taken. |
| `TR.FundRiskToReturnRatio5Year` | Return/Risk Ratio for 5 Years to Last Month End | Float | 5 years ratio of relationship of substantial reward corresponding to the amount of risk taken. |
| `TR.FundSharpe10Year` | Sharpe Ratio for 10 Years to Last Month End | Float | 10 years measure of a portfolio's excess return relative to the total variability of the portfolio. |
| `TR.FundSharpe1Year` | Sharpe Ratio for 1 Year to Last Month End | Float | 1 year measure of a portfolio's excess return relative to the total variability of the portfolio. |
| `TR.FundSharpe3Year` | Sharpe Ratio for 3 Years to Last Month End | Float | 3 years measure of a portfolio's excess return relative to the total variability of the portfolio. |
| `TR.FundSharpe5Year` | Sharpe Ratio for 5 Years to Last Month End | Float | 5 years measure of a portfolio's excess return relative to the total variability of the portfolio. |
| `TR.FundStdDev10Year` | Standard Deviation for 10 Years to Last Month End | Float | 10 years measure of how a fund's percentage changes over the period have varied from the mean. |
| `TR.FundStdDev1Year` | Standard Deviation for 1 Year to Last Month End | Float | 1 year measure of how a fund's percentage changes over the period have varied from the mean. |
| `TR.FundStdDev3Year` | Standard Deviation for 3 Years to Last Month End | Float | 3 years measure of how a fund's percentage changes over the period have varied from the mean. |
| `TR.FundStdDev5Year` | Standard Deviation for 5 Years to Last Month End | Float | 5 years measure of how a fund's percentage changes over the period have varied from the mean. |
| `TR.FundTrackingError10Year` | Tracking Error for 10 Years to Last Month End | Float | When using an indexing or any other benchmarking strategy, the amount by which the performance of the portfolio differed from that of the benchmark measured within last 10 years. |
| `TR.FundTrackingError1Year` | Tracking Error for 1 Year to Last Month End | Float | When using an indexing or any other benchmarking strategy, the amount by which the performance of the portfolio differed from that of the benchmark measured within last year. |
| `TR.FundTrackingError3Year` | Tracking Error for 3 Years to Last Month End | Float | When using an indexing or any other benchmarking strategy, the amount by which the performance of the portfolio differed from that of the benchmark measured within last 3 years. |
| `TR.FundTrackingError5Year` | Tracking Error for 5 Years to Last Month End | Float | When using an indexing or any other benchmarking strategy, the amount by which the performance of the portfolio differed from that of the benchmark measured within last 5 years. |
| `TR.FundTreynor10Year` | Treynor Ratio for 10 Years to Last Month End | Float | 10 years measure of the excess return per unit of risk, where excess return is defined as the difference between the portfolios return and the risk-free rate of return over the same evaluation period and where the unit of risk is the portfolios beta. |
| `TR.FundTreynor1Year` | Treynor Ratio for 1 Year to Last Month End | Float | 1 year measure of the excess return per unit of risk, where excess return is defined as the difference between the portfolios return and the risk-free rate of return over the same evaluation period and where the unit of risk is the portfolios beta. |
| `TR.FundTreynor3Year` | Treynor Ratio for 3 Years to Last Month End | Float | 3 years measure of the excess return per unit of risk, where excess return is defined as the difference between the portfolios return and the risk-free rate of return over the same evaluation period and where the unit of risk is the portfolios beta. |
| `TR.FundTreynor5Year` | Treynor Ratio for 5 Years to Last Month End | Float | 5 years measure of the excess return per unit of risk, where excess return is defined as the difference between the portfolios return and the risk-free rate of return over the same evaluation period and where the unit of risk is the portfolios beta. |
| `TR.FundWorst3Mnth` | Worst 3 Months within the Last 3 Years to Last Month End | Percentage | Worst three-month return over the last three years to the prior month end. |
| `TR.FundYeartoMnthEnd` | Year-to-Month End Performance | Percentage | Takes into account not only the capital gains of an investment but also the income yield from dividends or interest payments. The calculation of total return is based on the assumption that interest payments or dividends are immediately reinvested. Value is measured on a year to month basis. |
| `TR.FundYeartoYesterday` | Year-to-Date Performance | Percentage | Takes into account not only the capital gains of an investment but also the income yield from dividends or interest payments. The calculation of total return is based on the assumption that interest payments or dividends are immediately reinvested. Value is measured from January 1st of the current year up until yesterday. |

## Lipper Ratings (8)

The **Lipper Leader** ratings — Lipper's own 1-to-5 scorecard (5 best) across Total Return, Consistent Return, Preservation, Expense and Tax Efficiency — plus the rating's country, time frame and reported date. Ratings are relative to a peer universe within a country.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.FundConsistentReturnLipperRating` | Consistent Return Lipper Rating | Integer | The Lipper Rating for Consistent Return identifies a fund that has provided relatively superior consistency and risk-adjusted returns when compared to a group of similar funds. 5 is the highest and 1 is the lowest. |
| `TR.FundExpenseLipperRating` | Expense Lipper Rating | Integer | The Lipper Rating for Expense identifies a fund that has successfully managed to keep its expenses low relative to its peers and within its load structure. 5 is the highest and 1 is the lowest. |
| `TR.FundPreservationLipperRating` | Preservation Lipper Rating | Integer | The Lipper Rating for Preservation is a fund that has demonstrated a superior ability to preserve capital in a variety of markets when compared with other funds in its asset class. 5 is the highest and 1 is the lowest. |
| `TR.FundRatingCountry` | Rating Country | String | Rating Country. |
| `TR.FundRatingTimeFrame` | Rating Time Frame | String | Rating Time Frame. |
| `TR.FundReportedDateLipperRating` | Reported Date | Date | As-of-date for the Lipper ratings. |
| `TR.FundTaxEfficiencyLipperRating` | Tax Efficiency Lipper Rating | Integer | The Lipper Ratings for Tax Efficiency identifies a fund that has been successful at deferring taxes over the measurement period relative to similar funds. 5 is the highest and 1 is the lowest. |
| `TR.FundTotalReturnLipperRating` | Total Return Lipper Rating | Integer | The Lipper Rating for Total Return denotes a fund that has provided superior total returns (income from dividends and interest as well as capital appreciation) when compared to a group of similar funds. 5 is the highest and 1 is the lowest. |

## Corporate Action History (18)

**Distribution and corporate-action history**: income dividends and capital-gains distributions (payment values, currencies, and the full set of ex/record/payment/reinvestment dates and tax status), plus fund splits (factor, old/new holdings, valuation date). A dated history, not a single value.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.FundCGCurrency` | Capital Gains Currency Code. | String | The currency of the capital gain paid. |
| `TR.FundCGExDate` | Valuation Date | Date | Date on which the fund reviews the share register to determine who is entitled to receive the capital gain payment. |
| `TR.FundCGIncomeOperation` | Income Operation | String | Indicates if the payment was Paid or Retained. |
| `TR.FundCGPayment` | Capital Gains Payment Value | Float | A capital payment (or accounting of) capital gain generated by a fund to the investor. |
| `TR.FundCGPaymentDate` | Payment Date | Date | The date when the capital gain is payable to the shareholder of the fund. |
| `TR.FundCGReinvestDate` | Reinvestment Date | Date | The date when the capital gain is reinvested into the fund. |
| `TR.FundCGTaxStatus` | Tax Status | String | Indicates if the payment is Gross or Net for taxes. |
| `TR.FundCGValueType` | Capital Gains Value Type | String | The type of capital gain being paid or reinvested. |
| `TR.FundDiv` | Dividend Payment | Money | The value of the dividend payment proposed or paid. |
| `TR.FundDivCurr` | Dividend Currency Code | Currency | The code representing currency of the Dividend Paid. |
| `TR.FundExDate` | Ex Dividend Date | Date | The date of the distribution event or the day the share price is reduced by the amount of the distribution. Often referred to as the 'ex-date' or 'ex dividend date'. |
| `TR.FundIncDistribution` | Income Distribution | String | A distribution (or accounting of) of income generated by a fund to the investor. Income can be either paid or distributed to the investor OR retained by the fund share class to accrue further income in the future. |
| `TR.FundPayDate` | Payment Date | Date | The day distributions are posted to the shareholder's account. |
| `TR.FundRecordDate` | Record Date | Date | Date on which the fund reviews the share register to determine who is entitled to receive the dividend payment. |
| `TR.FundSFFactor` | Split Factor | Float | Adjustment factor due to a fund split. |
| `TR.FundSFNewHolding` | New Holdings | Float | Number of shares held following the split. |
| `TR.FundSFOldHolding` | Old Holdings | Float | Number of shares held before the split. |
| `TR.FundSFValuationDate` | Valuation Date | Date | The effective date of the Split Adjustment or Factor Adjustment to the Fund. |

## Responsible Investments (19)

**ESG / SRI classification flags** describing the fund's responsible-investment posture: headline ESG (environmental/social/governance) and SRI flags, impact-investing themes (microfinance, SDGs, sustainable bonds), negative-screening exclusions (tobacco, weapons, fossil energy, nuclear, GMO, alcohol/drugs, adult entertainment, other) and positive-screening approaches (best-in-class, positive tilt, thematic). Mostly Yes/No indicators.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.FundRIESGEnviron` | ESG-Environmental | String | Environmental identifies funds that include Environmental criteria in their overall screening process. |
| `TR.FundRIESGGov` | ESG-Governance | String | Governance identifies funds that include Governance criteria in their overall screening process. |
| `TR.FundRIESGSoc` | ESG-Social | String | Social identifies funds that include Social criteria in their overall screening process. |
| `TR.FundRIImpInvMicFi` | Impact Investing-Microfinance | String | Microfinance identifies funds that invest exclusively in microfinance projects. Must be used in conjunction with the attribute SDG, as Microfinance is supposed to fight poverty (one of the main SDGs). |
| `TR.FundRIImpInvSDG` | Impact Investing-Sustainable Development Goals (SDGs) | String | Sustainable Development Goals identifies funds that invest in companies that strive to have a positive contribution to the achievement of the UN sustainable development goals as part of the agenda 2030. |
| `TR.FundRIImpInvSuBnd` | Impact Investing-Sustainable Bonds | String | Sustainable Bonds identifies funds that invest exclusively in so-called green bonds, social bonds, sustainable bonds, blue bonds, impact bonds, transition bonds et cetera. |
| `TR.FundRINegScnXAdEt` | Negative Screening-ex Adult Entertainment | String | Ex Alcohol & Drugs identifies funds that exclude companies who are involved in the production and/or distribution of alcohol or drugs like cannabis from their investment universe. |
| `TR.FundRINegScnXAlDg` | Negative Screening ex Alcohol or Drugs | String | Ex Alcohol & Drugs identifies funds that exclude companies who are involved in the production and/or distribution of alcohol or drugs like cannabis from their investment universe. |
| `TR.FundRINegScnXFsEn` | Negative Screening-ex Fossil Energy | String | Ex Fossil Energy identifies funds that exclude companies who are involved in the production and/or distribution of fossil energy from their investment universe. Fossil energy includes brown coal, stone coal, natural gas, mineral oil, thermal coal, oil sands et cetera. This may also include the producers of drilling equipment or equipment for refineries and plants. |
| `TR.FundRINegScnXGMO` | Negative Screening-ex GMO | String | x GMO identifies funds that exclude companies who are involved in the production and/or distribution and/or use of genetically modified organisms from their investment universe. |
| `TR.FundRINegScnXNuc` | Negative Screening-ex Nuclear | String | Ex Nuclear identifies funds that exclude companies who are involved in the production of nuclear power and/or nuclear power plants and/or uranium mining from their investment universe. This may also include the producers of parts for nuclear plants or other activities related to nuclear power. |
| `TR.FundRINegScnXOth` | Negative Screening-ex Other | String | Ex Other identifies funds that excludes companies who are involved in the production and/or distribution of a segment which is currently not available as single exclusion segment. |
| `TR.FundRINegScnXTbc` | Negative Screening-ex Tobacco | String | Ex Tobacco identifies funds that exclude companies who are involved in the production and/or distribution of tobacco from their investment universe. |
| `TR.FundRINegScnXWep` | Negative Screening-ex Weapons | String | Ex Weapons identifies funds that exclude companies who are involved in the production of civilian and military weapons and firearms from their investment universe. |
| `TR.FundRIPosScnBIC` | Positive Screening-Best in Class | String | An approach which identifies leading sustainable companies in a certain peer group which is not necessarily noted as sustainable. So one might choose the least polluting oil company etc. |
| `TR.FundRIPosScnPsTlt` | Positive Screening-Positive Tilt | String | An approach which overweights leading companies compared to the benchmark. |
| `TR.FundRIPosScnTheme` | Positive Screening-Thematic | String | An approach which invests in sustainable themes such as clean water, climate change, low carbon, low pollution innovations etc. |
| `TR.FundRIRespInvest` | Responsible Investments | String | Responsible Investment identifies funds that include ESG, SRI, Positive-/Negative Screening, Impact Investing and or Religious criteria in their overall screening process. |
| `TR.FundRISRI` | SRI | String | Fund has a socially responsible investment strategy. |

## Rolling Performance (1)

A single parameterized field returning rolling performance over a chosen window.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.FundRollingPerformance` | Rolling Performance | Percentage | Takes into account not only the capital gains of an investment but also the income yield from dividends or interest payments. The calculation of total return is based on the assumption that interest payments or dividends are immediately reinvested. Value is measured on a rolling period basis. |

## Bonus: ETF ReportsPlus scores (ETF-specific)

These sit under a **separate parent** (`ETF Reports Plus`, a distinct entitlement from Lipper Funds)
but are directly relevant to ETFs such as SPY. They are Lipper-produced quantitative scores on a
**1-to-10 scale (10 most favourable)**, recalculated weekly. The Overall Score blends up to seven
components; each component is also exposed on its own, and the Overall Score has historical variants
(one week / one / three / six months / one / three years ago) for trend analysis.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.ETFOverallScore` | ETF Reports Plus Overall Score | Integer | Weighted blend of up to seven components (Performance, Risk, Cost, Fundamental, Valuation, Technical, Sentiment), normalised by asset type/region. 8-10 positive, 4-7 neutral, 1-3 negative. |
| `TR.ETFOverallScoreOneWeekAgo` | Overall Score - 1 Week | Integer | Overall Score as of the previous week. |
| `TR.ETFOverallScoreOneMonthAgo` | Overall Score - 1 Month | Integer | Overall Score as of the previous month. |
| `TR.ETFOverallScoreThreeMonthsAgo` | Overall Score - 3 Months | Integer | Overall Score three months ago. |
| `TR.ETFOverallScoreSixMonthsAgo` | Overall Score - 6 Months | Integer | Overall Score six months ago. |
| `TR.ETFOverallScoreOneYearAgo` | Overall Score - 1 Year | Integer | Overall Score one year ago. |
| `TR.ETFOverallScoreThreeYearsAgo` | Overall Score - 3 Years | Integer | Overall Score three years ago. |
| `TR.ETFPerformanceScore` | Performance Score | Integer | Return, return-to-risk, up/down capture, capital preservation. |
| `TR.ETFRiskScore` | Risk Score | Integer | Volatility, liquidity, value-at-risk, holdings risk. |
| `TR.ETFCostScore` | Cost Score | Integer | Expense ratio, trading volume, bid-ask spread. |
| `TR.ETFFundamentalScore` | Fundamental Score | Integer | Holdings-weighted earnings surprises, estimate revisions, debt, earnings quality (equity ETFs only). |
| `TR.ETFValuationScore` | Valuation Score | Integer | Equity ETFs: P/E, PEG, P/S, P/B. Bond ETFs: dividend yield, yield-to-quality/maturity/median. |
| `TR.ETFTechnicalScore` | Technical Score | Integer | Long-term relative strength, medium-term moving average, short-term overbought/oversold. |
| `TR.ETFSentimentScore` | Sentiment Score | Integer | Short interest, institutional buying/selling, net flows. |


## Notes

- **Case-insensitive:** field codes resolve regardless of case (`TR.FundNAV` == `TR.FUNDNAV`). One code is stored lowercase in the catalogue (`TR.FundDailyinflows`) but resolves either way.
- **Companion fields:** allocation fields need `TR.FundAllocationName` + `TR.FundAllocationDate`; many price/flow fields accept `.date`.
- **Silent drops:** invalid or unentitled fields are omitted from the result rather than raising; always inspect the returned columns.
- **Related standalone tests:** `share/lseg-toolkit/standalone/lseg_spy_allocation.py` (allocation history) and `lseg_spy_holdings.py` (full holdings panel).
- **Not available as fund summaries:** there is no ready-made *maturity ladder* or *credit-quality* breakdown at fund level — derive those from the holdings.
