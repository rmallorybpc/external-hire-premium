# Phase 1 data pipeline: external hire premium study

Status as of June 11, 2026. Phase 0 rules are locked in phase-0-pre-commitments.md. This document is the working plan for panel construction.

## Step 1: Acquire the backbone (user action required)

Download from https://zenodo.org/records/17725939 the file "CEO Dismissal Database Posted to Web 10Oct24.xlsx" (3.4 MB) and upload it to the project chat. Also download "CEO Dismissal Database Documentation 10Oct24.docx" for the code definitions and change log.

## Step 2: Inspect and verify

- Confirm row counts, year coverage, and variable list against the documentation.
- Locate the departure reason code variable and quote the code definitions verbatim into the decisions log (D-004).
- Check whether the file carries an index membership variable or successor identity fields. Both affect Steps 3 and 5.

## Step 3: Filter

- Window: departure or appointment dates within January 1, 2010 to December 31, 2022.
- Scope: S&P 500 membership at the transition date, point in time, not current membership (D-002).

## Step 4: Map exit classifications

- Build the mapping table from Gentry codes to forced, voluntary, unclassified.
- Apply Phase 0 overrides on top of the mapping: government-exit (voluntary regardless of age), exogenous-exit (death or incapacity, excluded from forced vs voluntary), change-of-control (excluded).

## Step 5: Classify successors (the hand work)

The Gentry database codes departures. Internal vs external classification of each successor against the 12-month primary rule is this study's own contribution and is expected to remain manual:
- Successor identity from the database if present, otherwise from 8-K filings.
- Prior employment months from proxy statement biographies.
- Every judgment call logged with rule, flag, and date.

## Step 6: Enrich

- Compensation: DEF 14A summary compensation table, first full fiscal year (per Phase 0 section 5).
- TSR and ROA: windows from minus 2 to plus 3 years around appointment.
- Tenure and censoring at the fixed observation date, set on the day of the final pull.

## Revised effort estimate

The original estimate was 1 to 2 weeks of assembly, protected to 3. The backbone removes the transition-list construction. Remaining manual work concentrates in Step 5 (successor classification) and Step 6 (compensation pulls). New estimate: roughly 1 week of focused work, protected to 2. The estimate firms up after Step 2.

## Session boundary note

The analysis sandbox cannot reach Zenodo or SEC EDGAR directly. Bulk files must be uploaded to the chat by the user. SEC lookups run through web fetch one document at a time, which is workable for Step 6 at S&P 500 scale but should be batched by company.
