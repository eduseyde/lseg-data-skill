# ESG & Emissions (`TR.*`)

LSEG's **Environmental, Social and Governance** scores, their pillar and category
breakdowns, controversy overlays, and absolute **carbon-emissions** figures. Scores run
on a **0–100 scale and are industry-relative** — a company is graded against its peer
group, not on an absolute basis. All scores are an **annual time series**: pull history
with `SDate`/`EDate` + `Frq="FY"` (or `period="FY0"` for the latest). Every field below
carries the `parent_category` **Environmental, Social and Governance** and was enumerated
via `search_fields` and confirmed to resolve on `AAPL.O` (with real FY2019–FY2023 values)
via `get_data` on **2026-07-02**. For the query recipe and score-interpretation bands,
see [../usage/esg.md](../usage/esg.md).

## Headline & Combined scores

The top-line company score comes under **two interchangeable field codes** — `TR.TRESGScore`
(legacy "TR" naming) and `TR.ESGScore` (current "LSEG" naming) — both returning the overall
score built up from the three pillars. The **Combined** score (`TR.TRESGCScore`) takes that
headline and **discounts it downward for controversies**: the gap between headline and
combined is a direct read on how much negative media exposure is dragging the company down.
Letter-grade companions (`…Grade`) map the number onto an A+ … D– band.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.TRESGScore` | ESG Score | Float | Overall ESG score from the reported information across the three pillars (legacy code). |
| `TR.ESGScore` | LSEG ESG Score | Float | Overall ESG score across environmental, social and governance factors (current LSEG code; equivalent to `TR.TRESGScore`). |
| `TR.TRESGCScore` | ESG Combined Score | Float | The headline ESG score with an ESG-controversies overlay applied (adjusted downward for controversies). |
| `TR.TRESGScoreGrade` | ESG Score Grade | String | Letter-grade band of the headline ESG score (e.g. `B+`). |
| `TR.TRESGCScoreGrade` | ESG Combined Score Grade | String | Letter-grade band of the Combined score (e.g. `C`). |

## Pillar scores

The headline decomposes into **three pillars** — Environmental, Social, Governance — each
itself a 0–100, industry-relative score. These are the workhorses for most ESG research.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.EnvironmentPillarScore` | Environmental Pillar Score | Float | Impact on natural systems (air, land, water, ecosystems) via resource use, emissions and innovation. |
| `TR.SocialPillarScore` | Social Pillar Score | Float | Capacity to build trust and loyalty with workforce, customers and society ("license to operate"). |
| `TR.GovernancePillarScore` | Governance Pillar Score | Float | Systems and processes ensuring board and executives act in long-term shareholders' interests. |

> The pillars also exist under the current "LSEG" naming — `TR.EnvironmentalPillarESGScore`,
> `TR.SocialPillarESGScore`, `TR.GovernancePillarESGScore` — mirroring the
> `TR.TRESGScore` / `TR.ESGScore` duplication above. Either family resolves; the examples
> here use the shorter legacy codes.

## Category scores

Each pillar breaks down further into **category scores** (LSEG's ten ESG categories). These
let you see *which* dimension is driving a pillar — for instance, an environmental pillar
carried by strong Resource Use and Emissions management but weaker elsewhere. A curated,
validated selection across all three pillars:

| Field Code | Title | Type | Pillar | Description |
|---|---|---|---|---|
| `TR.TRESGResourceUseScore` | Resource Use Score | Float | E | Performance in reducing materials, energy and water use and improving supply-chain eco-efficiency. |
| `TR.TRESGEmissionsScore` | Emissions Score | Float | E | Commitment and effectiveness at reducing environmental emissions in production and operations. |
| `TR.TRESGWorkforceScore` | Workforce Score | Float | S | Job satisfaction, health and safety, diversity, equal opportunity and workforce development. |
| `TR.TRESGHumanRightsScore` | Human Rights Score | Float | S | Effectiveness at respecting the fundamental human-rights conventions. |
| `TR.TRESGCommunityScore` | Community Score | Float | S | Commitment to good citizenship, public health and business ethics. |
| `TR.TRESGProductResponsibilityScore` | Product Responsibility Score | Float | S | Quality goods and services integrating customer health, safety, integrity and data privacy. |
| `TR.TRESGCSRStrategyScore` | CSR Strategy Score | Float | G | Practices integrating financial, social and environmental dimensions into day-to-day decisions. |

## Controversies

The **controversy overlay** measures negative media exposure. `TR.ControversiesScore` (and
its combined-score sibling `TR.TRESGCControversiesScore`) is a 0–100 category score — a
**low** score means *more* controversy — while `TR.ControvEnv` is a raw **count** of
environmental controversy events. This overlay is what pulls the Combined score below the
headline.

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.ControversiesScore` | Controversies Score | Float | Exposure to and involvement in ESG-related controversies based on news data (lower = more controversy). |
| `TR.TRESGCControversiesScore` | ESG Controversies Score | Float | The controversies category score feeding the ESG Combined overlay. |
| `TR.ControvEnv` | Environmental Controversies Count | Integer | Number of controversies tied to the environmental impact of the company's operations (oil spills, toxic waste, etc.). |

## Emissions (absolute figures)

Unlike the scores above, these are **absolute carbon quantities in tonnes of CO₂-equivalent**
— not industry-relative. Use them when you need the physical footprint rather than a peer
ranking. `TR.CO2EmissionTotal` is Scope 1 + Scope 2; the Scope-1/Scope-3 legs and the full
1+2+3 total are separate fields. (Scope 2 is additionally carried split market-based vs
location-based, e.g. `TR.CO2EquivalentEmissionIndirectScope2Marketbased`.)

| Field Code | Title | Type | Description |
|---|---|---|---|
| `TR.CO2EmissionTotal` | CO2 Equivalent Emissions Total | Float | Total CO₂-equivalent emissions in tonnes (direct Scope 1 + indirect Scope 2). |
| `TR.CO2DirectScope1` | CO2 Equivalent Emissions Direct, Scope 1 | Float | Direct emissions from sources owned or controlled by the company (tonnes CO₂e). |
| `TR.CO2IndirectScope3` | CO2 Equivalent Emissions Indirect, Scope 3 | Float | Value-chain (Scope 3) emissions — supply chain, business travel, product use, etc. (tonnes CO₂e). |
| `TR.TotalCO2EquivalentEmissionsScope1and2and3` | Total CO2 Equivalent Emissions Scope 1 and Scope 2 and Scope 3 | Float | Full footprint across all three scopes (tonnes CO₂e). |

## Access patterns

**ESG score history (annual time series)** — the standard shape for panel work. Pass
`SDate`/`EDate` and `Frq="FY"`, and add `.date` to any field to stamp the reporting date:

```python
import lseg.data as ld
ld.open_session()
df = ld.get_data(
    universe="AAPL.O",
    fields=[
        "TR.TRESGScore",              # headline
        "TR.TRESGCScore",             # combined (controversy-adjusted)
        "TR.EnvironmentPillarScore", "TR.SocialPillarScore", "TR.GovernancePillarScore",
        "TR.CO2EmissionTotal",        # absolute Scope 1+2 (tonnes)
        "TR.TRESGScore.date",
    ],
    parameters={"SDate": "2019-01-01", "EDate": "2024-01-01", "Frq": "FY"},
)
print(df)
ld.close_session()
```

The controversy gap falls straight out of the headline vs combined columns:

```python
df["controversy_impact"] = df["ESG Score"] - df["ESG Combined Score"]
```

## Notes

- **Industry-relative, not absolute.** A high score ranks a company *against its peers*.
  An energy company scoring 80 on Emissions can still emit far more in absolute tonnes than
  a tech company scoring 50 — for the physical footprint use the emissions fields, not the
  scores.
- **Headline code duplication.** `TR.TRESGScore` (legacy) and `TR.ESGScore` (current) both
  return the overall score; the pillars duplicate the same way (`…PillarScore` vs
  `…PillarESGScore`). Confirm they agree for your data vintage before mixing them.
- **Combined-vs-headline gap = controversies.** A wide gap between `TR.TRESGScore` and
  `TR.TRESGCScore` signals a material controversy drag (Apple's ~68 headline vs ~36 combined
  in FY2019 is exactly this). Read the two together, not in isolation.
- **Coverage gaps and cadence.** Not every company has ESG coverage — drop nulls before
  aggregating. Scores refresh roughly weekly; carbon data is annual; controversies update as
  events occur. LSEG has revised its methodology over the years, so very long historical
  comparisons should be read with care.
- **Silent drops:** invalid or unentitled fields are omitted from the result rather than
  raising — always inspect the returned columns.
- **Discover more.** LSEG publishes hundreds of finer category, boolean-flag and CDP-sourced
  metrics beyond this curated set (`…Grade` variants, `…YoY` changes, Scope-2 market/location
  splits, board-structure booleans). Enumerate them with the methods in
  [../usage/field-discovery.md](../usage/field-discovery.md).
