# ESG Data

LSEG ESG scores rate companies 0-100, relative to industry peers, across three
pillars. For the field codes, see [../data-items/esg.md](../data-items/esg.md).

## Score structure

```
ESG Score (0-100)
├── Environmental Pillar   (resource use, emissions, innovation)
├── Social Pillar          (workforce, human rights, community, product resp.)
└── Governance Pillar      (management, shareholders, CSR strategy)

ESG Combined Score = ESG Score adjusted downward for controversies
```

## Snapshot

```python
import lseg.data as ld

ld.open_session()

df = ld.get_data(
    universe=["AAPL.O", "MSFT.O", "XOM.N"],
    fields=[
        "TR.CommonName",
        "TR.TRESGScore",              # headline ESG
        "TR.TRESGCScore",             # combined (controversy-adjusted)
        "TR.EnvironmentPillarScore",
        "TR.SocialPillarScore",
        "TR.GovernancePillarScore",
    ],
)
ld.close_session()
print(df)
```

## Score history (annual time series)

ESG fields support `SDate/EDate` with `Frq=FY`:

```python
df = ld.get_data(
    universe="AAPL.O",
    fields=["TR.TRESGScore", "TR.EnvironmentPillarScore", "TR.TRESGScore.date"],
    parameters={"SDate": "2018-01-01", "EDate": "2025-01-01", "Frq": "FY"},
)
```

## Controversy impact

```python
# A large gap = material controversies dragging the headline score down
df["controversy_impact"] = df["TR.TRESGScore"] - df["TR.TRESGCScore"]
```

## Interpreting scores

| Range | Reading |
|---|---|
| 75-100 | Top quartile |
| 50-75 | Above average |
| 25-50 | Average |
| 0-25 | Below average |

## Notes

- **Industry-relative:** an energy company scoring 60 may still emit far more in
  absolute terms than a tech company scoring 40. For absolute emissions use
  `TR.CO2EmissionTotal`.
- **Coverage gaps:** not every company has ESG coverage — drop nulls before
  aggregating (`df.dropna(subset=["TR.TRESGScore"])`).
- **Update cadence:** scores refresh roughly weekly; carbon data is often annual;
  controversies update as events occur.
- **Methodology changes:** LSEG has revised its ESG methodology over the years, so
  very long historical comparisons should be read with care.
- LSEG publishes many finer category and governance metrics beyond the headline
  codes above; discover them via [field-discovery.md](field-discovery.md).
