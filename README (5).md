# Data

Snapshot files with provenance, not live feeds.

- `source/` the working panel built from the CEO dismissal database
- `classification/` the frozen sample: every transition classified internal or external
- `enrichment/` collected financial data (ROA, TSR, SIC, compensation), the keyed inputs,
  and the merged analysis files

The large raw compensation dump (`edgar_comp_raw.csv`) is excluded by `.gitignore`. Rebuild
it by running the compensation script.
