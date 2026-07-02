# ESG (`TR.*`)

Environmental, Social, and Governance scores, plus headline emissions. Scores are
on a 0-100 scale and are relative to industry peers.

ESG fields support annual time series via `SDate` / `EDate` with `Frq=FY`. See
[../usage/esg.md](../usage/esg.md).

| Field Code | Title |
|---|---|
| `TR.TRESGScore` | ESG Score |
| `TR.ESGScore` | LSEG ESG Score |
| `TR.TRESGCScore` | ESG Combined Score |
| `TR.EnvironmentPillarScore` | Environmental Pillar Score |
| `TR.SocialPillarScore` | Social Pillar Score |
| `TR.GovernancePillarScore` | Governance Pillar Score |
| `TR.ControversiesScore` | Controversies Score |
| `TR.ControvEnv` | Environmental Controversies Count |
| `TR.CO2EmissionTotal` | CO2 Equivalent Emissions Total |

## Notes

- **Two headline codes:** `TR.TRESGScore` (legacy naming) and `TR.ESGScore`
  (current LSEG naming) both return the overall ESG score; the examples in this
  skill use `TR.TRESGScore`. Confirm they agree for your data vintage before mixing
  them.
- **Combined vs headline score:** `TR.TRESGCScore` (Combined) adjusts the headline
  `TR.TRESGScore` downward for controversies. A large gap between the two signals
  material controversies.
- **Industry-relative:** scores compare a company to its industry peers, so a high
  score does not imply low absolute emissions. For absolute figures use
  `TR.CO2EmissionTotal`.
- LSEG publishes many finer-grained category and governance metrics (resource use,
  emissions, board composition, and so on). Only the headline codes above have been
  validated here; discover others via the methods in
  [../usage/field-discovery.md](../usage/field-discovery.md).
