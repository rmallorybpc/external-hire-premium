# Option B: let GitHub Copilot scaffold the repo

If you create the repo with the Copilot setup prompt instead of uploading the folder, paste
this. It describes the same structure this scaffold contains, so either path lands in the
same place.

---

Create a research project repository named `external-hire-premium` for a backward-looking
data study of S&P 500 CEO transitions (2010–2022), testing whether the pay premium for
externally hired CEOs predicts the return they deliver. Set it up as follows:

- A root `README.md` describing the study, its status, and that all data sources are public
  (SEC proxy filings, SEC XBRL API, free price data) so no licensed database is required.
- A `RUN_LOCALLY.md` with plain step-by-step instructions for a non-developer to install
  Python, install dependencies from `requirements.txt`, and run three data-collection
  scripts in order.
- A `requirements.txt` listing: requests, pandas, lxml, html5lib, yfinance.
- A `.gitignore` for Python (`__pycache__`, `.venv`), editor files, and large regenerated
  raw data dumps, plus `.env` and `*.key` as secret guards.
- A `scripts/` folder for Python data-collection scripts with its own README giving run
  order: (1) SEC XBRL ROA fetcher, (2) free-price TSR fetcher, (3) EDGAR proxy compensation
  extractor, plus an optional WRDS extraction script.
- A `docs/` folder for the methods, the pre-committed rules, and a dated decision log.
- A `data/` folder with subfolders `source/`, `classification/`, and `enrichment/`, and a
  README stating that data are committed snapshots with provenance, not live feeds.
- A `site/` folder containing the GitHub Pages findings site. Primary entry page is `site/index.html`.

Do not add any GitHub Actions workflow for data collection; data collection runs locally.

---

After Copilot creates the skeleton, you still add the actual content files (the scripts,
the decision log, the data CSVs) from this scaffold — Copilot makes the empty structure;
the files in `repo-scaffold/` are the contents.
