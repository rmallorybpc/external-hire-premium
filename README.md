# External hire premium

**Live site:** https://rmallorybpc.github.io/external-hire-premium/

Do externally hired S&P 500 CEOs cost more and deliver less than internal promotions? A backward-looking study of 611 CEO transitions, 2010 to 2022, with a sports free-agency comparison arm. All data is public. The study reproduces with no licensed database.

## Headline finding

What a company pays for an external hire does not predict the return that follows. The premium is directional (about 9 percent over the predecessor) but imprecise. The apparent worse-returns result is mostly selection: external CEOs are hired after the stock has lagged the market. The robust claim, which holds under every control and replicates in four sports datasets: the premium paid for external talent does not predict the return delivered.

## What it tracks

Internal vs external hire; pay (the premium); stock performance (Total Shareholder Return, TSR); operating performance (Return on Assets, ROA); tenure; and pre-hire performance.

## Layout

- `scripts/` data-collection and analysis code, with run notes
- `docs/` decision log, methods, design, and the findings write-ups
- `data/source` the working panel; `data/classification` the frozen sample; `data/enrichment` the collected financial snapshots and merged data
- `site/` static findings site for GitHub Pages (`index.html`, `findings.html`, `methods.html`, `audit.html`)

## Site publishing

The site is live at the link above. Pages deploys the `site/` folder through a GitHub Actions workflow (`.github/workflows/deploy-pages.yml`) with the upload path set to `./site`, and serves `site/index.html` as the entry page.

Brand stylesheet rule: published pages in `site/` must load TMG styles using either the CDN URL from `TMG-BRAND-GUIDE.md` or a stylesheet copied into `site/`. Do not use parent-relative stylesheet paths for published pages.

## Reproduce

See `RUN_LOCALLY.md`. Collect the data locally once, commit the snapshot CSVs, then the analysis runs from `scripts/analyze_refined.py`. The findings are in `docs/refined-findings.md`.
