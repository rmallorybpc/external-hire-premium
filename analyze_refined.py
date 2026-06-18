# WRDS Extraction Package: External Hire Premium

Purpose: collect the entire pass-two financial layer for the classified panel in one
WRDS session, instead of 600 individual proxy fetches. Built before access is in hand,
so the moment a WRDS login is available this runs start to finish.

## Files

- `wrds_panel_gvkeys.csv` — the 611-transition panel keyed on GVKEY, with each
  transition's two target fiscal years already computed (predecessor's last full
  fiscal year, successor's first full fiscal year). 437 unique firms.
- `wrds_extraction.py` — the extraction and merge script.

## What it pulls

1. ExecuComp `comp_execucomp.anncomp`: every CEO-year for the panel firms, 2007-2024,
   with TDC1 (the headline academic total-compensation measure) and its components.
2. Compustat `comp.funda`: net income and total assets for ROA, plus operating ROA and
   revenue, over the same band.
3. CRSP `crsp.msf` monthly returns (linked via `crsp.ccmxpf_linktable`) plus the
   value-weighted market index, for the -2yr / +3yr TSR windows, raw and market-adjusted.

It then merges into `enrichment_from_wrds.csv`: one row per transition with predecessor
TDC1, successor TDC1, their ratio, ROA pre and post, and the TSR windows.

## How to run

Any one of these (all behind the same WRDS login):

- WRDS JupyterHub: upload both files, open a notebook, `%run wrds_extraction.py`.
- WRDS Cloud (SSH) or local Python: `pip install wrds`, then `python wrds_extraction.py`.
  First run prompts for WRDS username and password and offers to create a `.pgpass`.

The GVKEY filter keeps every query small; the whole pull is minutes, not hours.

## Access routes still worth checking (no purchase required)

- University alumni access (often via the business school or library).
- Large public or state library systems that carry WRDS.
- A Network/Client contact at a subscribing institution who can run it or sponsor a guest account.
- A coauthor or academic affiliate, which also strengthens the paper.

## Methods-page notes (so the writeup stays clean)

- Headline compensation is ExecuComp TDC1, not the proxy "Total" line. State this
  explicitly. Any figure recorded earlier from trade press (e.g. Campanelli) gets
  replaced by the TDC1 value for consistency.
- WRDS terms forbid redistributing raw rows. The published site reports derived
  results (premiums, ratios, window returns) and never republishes ExecuComp,
  Compustat, or CRSP tables. Cite as: compensation from ExecuComp, accounting from
  Compustat, returns from CRSP, all via WRDS.
- Rows where ExecuComp has no CEO flag for a target year (small-cap coverage gaps,
  unusual fiscal-year ends) come back as NaN and get a short manual name-to-execid
  check. Expect a modest number; they are flagged, not silently dropped.
- ExecuComp covers S&P 1500, so coverage of an S&P 500 panel is near-complete, but
  the predecessor's last full year occasionally predates a firm's ExecuComp entry;
  those also surface as NaN for a manual check.
