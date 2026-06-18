# Enrichment

Keyed inputs:
- `wrds_panel_gvkeys.csv` transitions with identifiers and target fiscal years
- `edgar_comp_panel.csv` keys for the compensation pull
- `ticker_overrides.csv` resolved historical tickers for acquired/renamed firms

Collected snapshots (from the scripts):
- `roa_from_xbrl.csv`, `tsr_from_prices.csv`, `sic_from_sec.csv`, `edgar_comp_matched.csv`

Merged for analysis:
- `step6-enrichment.csv`, `merged-enrichment.csv`, `merged-enrichment-refined.csv`
