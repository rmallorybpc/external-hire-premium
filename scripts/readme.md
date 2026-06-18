# Scripts

Run order and purpose. Full guide in the repo root: RUN_LOCALLY.md.

| Order | Script | Pulls | Output |
|---|---|---|---|
| 1 | `sec_xbrl_roa.py` | ROA from SEC XBRL | `roa_from_xbrl.csv` |
| 2 | `price_tsr.py` | TSR, pre/post-hire windows; reads `ticker_overrides.csv` | `tsr_from_prices.csv` |
| 3 | `sec_sic.py` | 2-digit SIC industry | `sic_from_sec.csv` |
| 4 | `edgar_comp_extraction.py` | CEO pay from proxy SCT | `edgar_comp_matched.csv`, `edgar_comp_raw.csv` |
| - | `analyze_refined.py` | runs the regressions and survival models | `merged-enrichment-refined.csv` |
| - | `wrds_extraction.py` | optional faster path if you have WRDS | one combined file |

Inputs live in `data/enrichment`. Copy the needed input into this folder before running.
