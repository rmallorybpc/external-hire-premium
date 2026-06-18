# EDGAR Comp-Extraction Fallback

The documented fallback for the compensation layer, to be used if WRDS access does not
land, or to fill the gaps the WRDS ExecuComp pull leaves behind. Free, authoritative,
slower and messier than ExecuComp.

## Files

- `edgar_comp_panel.csv` — 561 transitions carrying CIK (406 unique firms), with each
  transition's predecessor and successor target fiscal years AND the proxy-filing year
  that reports them (a DEF 14A filed in year T+1 discloses year-T pay).
- `edgar_comp_extraction.py` — the engine.

50 transitions lack a CIK and need a ticker/name -> CIK lookup before they can run
(EDGAR company search, or the SEC's company_tickers.json mapping).

## How it works

For each transition it pulls the firm's DEF 14A filed in the successor's target proxy
year and in the predecessor's target proxy year, fetches each filing's primary HTML,
locates the Summary Compensation Table, extracts the named-executive rows, flags the
CEO row, and records salary and total with the source accession number. Outputs a raw
per-NEO file and a matched one-row-per-transition file.

## Before running

1. Edit the `CONTACT` line with your real email. EDGAR's fair-access policy REQUIRES a
   descriptive User-Agent; requests without one get blocked. The script refuses to run
   until you do this.
2. `pip install requests pandas lxml html5lib`.
3. `python edgar_comp_extraction.py`. Throttled to ~7 requests/sec, under EDGAR's cap.

## Honest limitations (these are why WRDS is still the plan, not this)

- **Volume.** 561 transitions x two proxy years each = ~1,000+ filings to fetch and
  parse. Run it as a background batch, not interactively.
- **Parsing is heuristic.** SCTs are free-form HTML tables with no fixed schema across
  600 firms. The extractor uses signature-column matching and will get most large, clean
  proxies right, but it WILL mis-parse a meaningful minority (multi-column year headers,
  footnoted totals, image-based tables). Every row carries a status; anything not "ok"
  needs a manual look at the named accession. Treat parsed numbers as provisional until
  spot-checked.
- **The "Total" column is not TDC1.** The proxy SCT total uses grant-date fair value
  under post-2006 rules and is not identical to ExecuComp's TDC1, the academic standard.
  If you mix these with any WRDS figures, label the source per row. Prefer TDC1 as the
  headline measure and use EDGAR totals for gaps/validation only.
- **Transition-year ambiguity.** In a handover year the SCT may list a partial-year CEO,
  an interim, and the incoming CEO together. The script picks the CEO row matching the
  target fiscal year, falling back to the highest-paid CEO row; verify these by hand for
  any transition flagged interim-bridged or co-ceo in the worksheet.
- **Comp only.** This does not touch ROA (needs the 10-K) or TSR (needs a price series).
  A WRDS-free pass two would still need a separate 10-K ROA fetcher and a price-source
  TSR fetcher; those are not built yet and would be the next fallback components.

## Decision rule

Run WRDS if access lands; it gives TDC1, ROA, and TSR clean from one login. Run this only
to fill WRDS NaN gaps, or build it out into a full WRDS-free pass two (adding ROA and TSR
fetchers) if access never comes. Do not start the ~1,000-filing grind while WRDS is still
in reach.
