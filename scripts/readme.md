# Scripts

Run order and purpose. Full PM-friendly instructions are in the repo root: RUN_LOCALLY.md.

| Order | Script | Pulls | Source | Output |
|---|---|---|---|---|
| 1 | `sec_xbrl_roa.py` | ROA (net income / total assets) | SEC XBRL API (free, no key) | `roa_from_xbrl.csv` |
| 2 | `price_tsr.py` | TSR (-2yr/+3yr window, raw + market-adjusted) | yfinance / Stooq (free) | `tsr_from_prices.csv`, `tsr_unresolved_tickers.csv` |
| 3 | `edgar_comp_extraction.py` | CEO compensation (predecessor + successor) | SEC DEF 14A proxies (free) | `edgar_comp_matched.csv` |

`wrds_extraction.py` is the optional faster path for anyone with WRDS access; it pulls all
three layers in one query. Not required. See WRDS_EXTRACTION_README.md.

Field note for the methods page: proxy "Total" is grant-date fair value, not the academic
TDC1 measure. If WRDS and EDGAR figures are ever mixed, label the source per row.
