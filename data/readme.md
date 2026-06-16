# Data

Snapshot files with provenance, not live feeds. The classification is frozen; the
enrichment fills in as the scripts run.

- `source/` — the working panel built from the Gentry CEO Dismissal Database, filtered to
  point-in-time S&P 500 constituents.
- `classification/` — the frozen sample. `step5-classification-worksheet.csv` is the
  headline dataset: every transition classified internal or external, with flags, sources,
  and the decision reference. `sp500-panel-confirmed.csv` is the confirmed membership panel.
- `enrichment/` — financial data lands here. `step6-enrichment.csv` holds verified dates,
  tenure, and censoring. `wrds_panel_gvkeys.csv` and `edgar_comp_panel.csv` are the keyed
  inputs the scripts read.

Provenance rule (from the audit): any cross-source assembly is a committed snapshot with a
note and a refresh script. No live cross-repo fetching.
