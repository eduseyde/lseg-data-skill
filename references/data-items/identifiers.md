# Identifiers & Classification (`TR.*`)

Company names, cross-market **security identifiers**, exchange/domicile reference
data, and the two **industry-classification schemes** (GICS and LSEG's own TRBC).
These are the descriptive fields you attach to any equity universe to label rows,
map to other datasets, and slice a cross-section by sector. Every field below carries
the `parent_category` **Reference & Identifiers** and was enumerated and validated
live from the MCP field catalogue (`search_fields`) and confirmed to resolve on
`AAPL.O` / `XOM.N` via `get_data` on **2026-07-02**.

These are **`get_data` snapshot fields** — one row per instrument, current state (no
`SDate`/`Frq` needed). For converting *between* identifier systems programmatically
(RIC ↔ ISIN ↔ CUSIP ↔ SEDOL ↔ Lipper), see
[../usage/symbology.md](../usage/symbology.md).

> **Entitlement caveat (important).** On the validation login, the raw
> `TR.ISIN` / `TR.CUSIP` / `TR.SEDOL` fields **resolved as columns but returned
> `null` values** (the API flags them as an all-NULL column, not an error). The same
> identifiers came back cleanly through **`convert_symbols`** (ISIN `US0378331005`,
> CUSIP `037833100` for Apple). If the identifier *fields* come back empty on a valid
> RIC, it is a reference-data licensing gap — **fall back to the symbol-conversion
> route**, which is separately entitled and is the more reliable path for a mapping
> table anyway.

## Company names

Three overlapping name fields. `TR.CommonName` is the everyday display name (and, for
funds, the primary share-class name); `TR.CompanyName` and `TR.OrganizationName` are
the fuller legal/registered forms. For a clean equity label, `TR.CommonName` is the
default.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.CommonName` | Company Common Name | String | Where available, the name of the organization most commonly used; provides the primary share-class name for funds. |
| `TR.CompanyName` | Company Name | String | The company's name. |
| `TR.OrganizationName` | Organization Name | String | The registered organization name. |
| `TR.CompanyLegalType` | Company Legal Type | String | The company's legal form (e.g. public company, private company). |

## Security identifiers

The cross-reference codes that link an LSEG instrument to the rest of the world. `RIC`
is LSEG's native instrument key; `ISIN`/`CUSIP`/`SEDOL` are the global/North-American/UK
standards; `Organization PermID` is LSEG's permanent, never-reused entity ID (the right
key for joining all securities of one company). Note the entitlement caveat above for
ISIN/CUSIP/SEDOL as raw fields.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.RIC` | RIC | String | Reuters Instrument Code — LSEG's native instrument identifier (e.g. `AAPL.O`). |
| `TR.PrimaryRIC` | Primary Issue RIC | String | The RIC of the company's primary listing/consolidated issue. |
| `TR.ISIN` | ISIN | String | International Securities Identification Number (12-char, consolidated with ISINCode). |
| `TR.CUSIP` | CUSIP | String | Committee on Uniform Securities Identification Procedures code (9-char North-American identifier). |
| `TR.SEDOL` | SEDOL | String | Stock Exchange Daily Official List code (7-char, consolidated with SEDOLCode). |
| `TR.OrganizationID` | Organization PermID | String | LSEG permanent organization identifier (PermID) — one code per company across all its securities. |

## Exchange & domicile

Where a security lists and where its issuer is based. `TR.ExchangeName`/`TR.ExchangeCountry`
describe the *listing venue*; `TR.HeadquartersCountry`/`TR.HQCountryCode`/`TR.RegistrationCountry`
describe the *issuer* (headquarters vs legal incorporation — these can differ, e.g. an
issuer incorporated in Ireland but headquartered in the US).

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.ExchangeName` | Exchange Name | String | Name of the exchange / consolidated issue on which the instrument trades. |
| `TR.ExchangeCountry` | Country of Exchange | String | Country of the listing exchange. |
| `TR.ExchangeTicker` | Exchange Ticker | String | The exchange ticker symbol (e.g. `AAPL`). |
| `TR.HeadquartersCountry` | Country of Headquarters | String | Country of headquarters, also known as country of domicile. |
| `TR.HQCountryCode` | Country ISO Code of Headquarters | String | ISO 3166 country code for the organization's headquarters. |
| `TR.RegistrationCountry` | Country of Incorporation | String | Country of legal incorporation / registration (may differ from headquarters). |

## Classification — GICS

The **Global Industry Classification Standard** (S&P / MSCI). A four-level hierarchy of
increasing granularity: **Sector → Industry Group → Industry → Sub-Industry**. Each level
comes as a name (`String`) and a numeric code (`Integer`, suffix `…Code`). GICS is the
market-standard scheme for equity-portfolio and cross-listing comparability.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.GICSSector` | GICS Sector Name | String | GICS Sector (broadest level, e.g. "Information Technology"). |
| `TR.GICSIndustryGroup` | GICS Industry Group Name | String | GICS Industry Group (2nd level). |
| `TR.GICSIndustry` | GICS Industry Name | String | GICS Industry (3rd level). |
| `TR.GICSSubIndustry` | GICS Sub-Industry Name | String | GICS Sub-Industry (finest level). |
| `TR.GICSSectorCode` | GICS Sector Code | Integer | Numeric code for the GICS Sector (companion codes exist at every level: `TR.GICSIndustryGroupCode`, `TR.GICSIndustryCode`, `TR.GICSSubIndustryCode`). |

## Classification — TRBC

**The Refinitiv Business Classification** — LSEG's own scheme and the **more granular** of
the two. A five-level hierarchy: **Economic Sector → Business Sector → Industry Group →
Industry → Activity**. Because it goes one level deeper than GICS (down to the specific
*Activity*), TRBC is the sharper tool for narrow peer sets. Each level has an `…All`
companion returning the numeric code (e.g. `TR.TRBCActivityAll`).

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.TRBCEconomicSector` | TRBC Economic Sector Name | String | TRBC Economic Sector (broadest level, e.g. "Technology"). |
| `TR.TRBCBusinessSector` | TRBC Business Sector Name | String | TRBC Business Sector (2nd level). |
| `TR.TRBCIndustryGroup` | TRBC Industry Group Name | String | TRBC Industry Group (3rd level). |
| `TR.TRBCIndustry` | TRBC Industry Name | String | TRBC Industry (4th level). |
| `TR.TRBCActivity` | TRBC Activity Name | String | TRBC Activity (finest level — the extra granularity over GICS). |

For reference, the two schemes side by side for Apple (validated live):

| Level | GICS | TRBC |
|---|---|---|
| Top | Information Technology | Technology |
| … | Technology Hardware & Equipment | Computers, Phones & Household Electronics |
| … | Technology Hardware, Storage & Peripherals | Phones & Handheld Devices |
| Finest | Technology Hardware, Storage & Peripherals | Phones & Smart Phones |

## Access patterns

**1. A one-shot identifier + classification pull** (snapshot, one row per instrument):

```python
import lseg.data as ld
ld.open_session()
df = ld.get_data(
    universe=["AAPL.O", "MSFT.O", "XOM.N"],
    fields=[
        "TR.CommonName", "TR.ISIN", "TR.CUSIP", "TR.OrganizationID",
        "TR.ExchangeName", "TR.HeadquartersCountry",
        "TR.GICSSector", "TR.TRBCEconomicSector", "TR.TRBCActivity",
    ],
)
print(df)
ld.close_session()
```

**2. Programmatic identifier mapping** — for building a RIC ↔ ISIN ↔ CUSIP ↔ SEDOL ↔
Lipper crosswalk (and the more reliable route when the raw identifier *fields* return
null), use `convert_symbols` rather than the `TR.*` fields:

```python
from lseg.data.content import symbol_conversion
r = symbol_conversion.Definition(
    symbols=["AAPL.O", "MSFT.O"],
    from_symbol_type="RIC",
    to_symbol_types=["ISIN", "CUSIP", "SEDOL"],
).get_data()
print(r.data.df)
```

See [../usage/symbology.md](../usage/symbology.md) for the full conversion recipe,
exchange-suffix table, bulk chunking, and the WRDS/CRSP linking workflow.

## Notes

- **Two classification schemes, different depth.** GICS (`TR.GICSSector` →
  `TR.GICSSubIndustry`) is the market standard; TRBC (`TR.TRBCEconomicSector` →
  `TR.TRBCActivity`) is LSEG's own and runs **one level deeper**. Pick one and stay
  consistent — do not mix a GICS sector with a TRBC industry in the same cross-section.
- **CUSIP is 9-character (with check digit).** CRSP/WRDS linking usually wants the
  8-character form — take the first 8 characters. (Some LSEG deal-side fields, e.g.
  `TR.NIIssuerCusip9` vs the 8-digit repo variants, expose both lengths explicitly.)
- **Headquarters ≠ incorporation.** `TR.HeadquartersCountry` (domicile) and
  `TR.RegistrationCountry` (legal incorporation) can diverge for cross-border issuers;
  choose deliberately when assigning a country.
- **Use `TR.OrganizationID` (PermID) to group cross-listings.** It links all securities
  of one company; an ISIN maps to a single line, but one company can trade on many venues.
- **Case-insensitive:** field codes resolve regardless of case (`TR.ISIN` == `TR.isin`).
- **Silent drops:** invalid or unentitled fields are omitted from the result rather than
  raising, and entitlement-gated identifiers can come back as an all-NULL column — always
  inspect the returned columns and values.
