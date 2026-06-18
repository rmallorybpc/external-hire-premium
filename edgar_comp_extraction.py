# WRDS-Free Pass Two: complete pipeline on free public data

With WRDS unavailable, the entire financial layer runs on free, public, reproducible
sources. Three fetchers, one per layer, all keyed on the panel you already have. No
subscription, no institution. For a public portfolio piece this is arguably better than
WRDS, because anyone can rerun it without access, which is a methods-page virtue.

## The three layers and their free sources

| Layer | Source | Script | Quality vs WRDS |
|---|---|---|---|
| Compensation | SEC DEF 14A proxy SCT | `edgar_comp_extraction.py` | Same data WRDS parses; proxy "Total" not TDC1 (label it). The grind. |
| ROA | SEC XBRL company-facts API | `sec_xbrl_roa.py` | Same data Compustat repackages, from the issuer. Effectively equal. |
| TSR | Free price feeds (yfinance/Stooq) + S&P 500 | `price_tsr.py` | Dividend-adjusted via yfinance = true TSR; near-CRSP for this purpose. |

## Run order

1. `sec_xbrl_roa.py` — fast, clean, do this first; it validates the panel's CIKs too.
2. `price_tsr.py` — resolves CIK->ticker, computes windows; acquired/renamed firms drop
   to `tsr_unresolved_tickers.csv` for a manual ticker, then rerun with overrides.
3. `edgar_comp_extraction.py` — the long one; run as a background batch (~1,000 filings).

Each writes its own CSV; a final merge on `transition_id` assembles the analysis dataset
alongside the already-built `step6-enrichment.csv` (which holds verified dates, tenure,
and censoring).

## Before running anything

- Edit the `CONTACT` line in each script with your real email. SEC and good practice
  require a descriptive User-Agent; the scripts refuse to run until you do.
- `pip install requests pandas lxml html5lib yfinance`.

## Honest quality notes for the methods page

- ROA from SEC XBRL uses NetIncomeLoss / Assets (year-end), the conventional ni/at, plus
  an operating-income variant for robustness. Pre-FY2009 years may be missing (XBRL became
  mandatory around then) and surface as flagged gaps; fill from the EDGAR 10-K if a
  predecessor's last full year predates XBRL.
- TSR via yfinance auto-adjusted close is split- and dividend-adjusted, i.e. true total
  return. If a ticker only resolves via Stooq, that figure is closer to price return; the
  source is recorded per row so the two are never silently mixed.
- Compensation stays the bottleneck and the one genuinely messy layer; see
  EDGAR_FALLBACK_README. Prefer the structured Pay-versus-Performance disclosures for
  FY2020+ where available, proxy SCT parsing for earlier years.
- Reproducibility statement for the site: "All inputs are public. Compensation from SEC
  DEF 14A filings, accounting from SEC XBRL company facts, returns from public adjusted
  price data. No licensed database is required to reproduce these results." That sentence
  is a credibility asset, not a consolation.

## If a WRDS login ever turns up

The WRDS package (wrds_extraction.py) remains the faster, TDC1-native path and stays
ready. These free fetchers then become the independent cross-check — agreement between a
free public pull and a WRDS pull is a robustness result worth stating.
