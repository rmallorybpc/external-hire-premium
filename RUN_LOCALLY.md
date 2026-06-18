# Run locally

A plain guide. No prior Python needed. Free data, no API key.

## 1. Install Python
Install Python 3.11+ from python.org. On Windows, check "Add Python to PATH".

## 2. Install packages (once)
In a terminal, from the repo root:
```
pip install -r requirements.txt
```
If you see "externally managed environment", add `--break-system-packages`.

## 3. Collect the data (from the scripts folder)
Each script reads an input CSV that lives in `data/enrichment`. Copy the input into
`scripts` first, then run. Run order:
```
cd scripts
copy ..\data\enrichment\wrds_panel_gvkeys.csv .
copy ..\data\enrichment\ticker_overrides.csv .
copy ..\data\enrichment\edgar_comp_panel.csv .
python sec_xbrl_roa.py     # ROA, ~10 min
python price_tsr.py        # TSR with post-hire windows, ~20 min
python sec_sic.py          # industry codes, ~5 min
python edgar_comp_extraction.py   # compensation, runs a few hours
```
Each prints a progress counter and a summary line.

## 4. Analyze
With the collected CSVs in `data/enrichment`, run:
```
python analyze_refined.py
```
This prints the premium, return, and headline models and writes
`merged-enrichment-refined.csv`.

## Notes
- Contact email is already set in the scripts.
- Some tickers and proxies will not resolve. That is expected and documented.
- Reliable habit: `cd scripts`, then `dir filename` to confirm an input is present, then run.
