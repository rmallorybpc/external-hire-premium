# External Hire Premium

Do externally hired S&P 500 CEOs cost more and deliver less than internal promotions?
A backward-looking data study of CEO transitions, 2010–2022, with a sports free-agency
comparison arm. This repository holds the code, the frozen classification, the full
decision log, and (eventually) the published findings.

## Status

| Phase | State |
|---|---|
| Classification of CEO transitions (the sample) | **Frozen.** 611 transitions, 453 internal / 158 external (25.9%), 149 rule-excluded. |
| Decision log | Complete through D-088, every ruling dated and sourced. |
| Financial enrichment (compensation, ROA, TSR) | Pipeline built; data not yet collected. |
| Analysis (premium, return-on-premium, survival) | Not started; waits on enrichment. |
| Findings site | Held until findings exist and it is this project's turn to publish. |

## What this is, and is not

It is a backward-looking analysis of whether the premium paid for outside CEO talent
predicts the return delivered. It is **not** a predictive tool and makes no claim to pick
the next hire. The expected finding, consistent with prior work (Bidwell, Groysberg,
Boivie et al.), is that the premium does not reliably predict return, because mean
reversion and buyer-side error dominate.

## Reproducibility

Every input is public. Compensation comes from SEC DEF 14A proxy filings, accounting from
the SEC XBRL company-facts API, returns from public adjusted price data. **No licensed
database (WRDS, Bloomberg, FactSet) is required to reproduce these results.** A WRDS path
is included as a faster alternative for anyone who has access, but it is optional.

## Repository layout

```
external-hire-premium/
├── README.md              <- you are here
├── RUN_LOCALLY.md         <- step-by-step to collect the data on your own machine
├── requirements.txt       <- Python packages the scripts need
├── .gitignore
├── scripts/               <- the data-collection scripts + their READMEs
├── docs/                  <- decision log, methods, design docs (the paper trail)
├── data/
│   ├── source/            <- the working panel (input)
│   ├── classification/    <- the frozen sample (the headline dataset)
│   └── enrichment/        <- per-firm financial pulls land here
└── site/                  <- GitHub Pages content (built later, from findings)
```

## Where to start

- To understand the study: read `docs/phase-0-pre-commitments.md` (the rules) and
  `docs/methods-commitments.md` (what gets reported).
- To see every decision: `docs/decisions-log.md`.
- To collect the financial data: `RUN_LOCALLY.md`, then `scripts/`.
- The frozen sample is `data/classification/step5-classification-worksheet.csv`.
