# Identifiers & Classification (`TR.*`)

Company names, security identifiers, and industry classification fields. For
converting between identifier systems programmatically, see
[../usage/symbology.md](../usage/symbology.md).

| Field Code | Title |
|---|---|
| `TR.CommonName` | Company Common Name |
| `TR.OrganizationName` | Organization Name |
| `TR.ISIN` | ISIN |
| `TR.CUSIP` | CUSIP |
| `TR.SEDOL` | SEDOL |
| `TR.ExchangeName` | Exchange Name |
| `TR.HeadquartersCountry` | Country of Headquarters |
| `TR.GICSSector` | GICS Sector Name |
| `TR.GICSIndustry` | GICS Industry Name |
| `TR.TRBCEconomicSector` | TRBC Economic Sector Name |
| `TR.TRBCBusinessSector` | TRBC Business Sector Name |
| `TR.TRBCIndustry` | TRBC Industry Name |
| `TR.TRBCActivity` | TRBC Activity Name |

## Notes

- **Two classification schemes:** GICS (`TR.GICSSector`, `TR.GICSIndustry`) and
  TRBC, LSEG's own scheme (`TR.TRBCEconomicSector` down to `TR.TRBCActivity`).
  TRBC is the more granular of the two.
- CUSIP is returned as the 9-character form (with check digit). CRSP/WRDS linking
  usually needs the 8-character form: take the first 8 characters.
