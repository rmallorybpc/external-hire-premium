# Preliminary Findings (First Pass)

Date: 2026-06-13. Status: PRELIMINARY and UNADJUSTED. These are unconditional comparisons
on the free-data enrichment, before regression controls. Directional, not final. The
numbers will move with controls, fuller comp coverage, and the WRDS/EDGAR reconciliation.

## Sample

From the frozen 611-transition panel: 343 successor pay figures, 326 predecessor, 240 with
both (the premium sample); 461 ROA pairs; 434 TSR windows. Compensation parsed from EDGAR
proxy Summary Compensation Tables, outlier-screened to plausible CEO totals ($100k–$200M),
matched to each transition's target fiscal year (exact where available, nearest year as
fallback). ROA from SEC XBRL, TSR from public adjusted prices.

## Finding 1: the premium exists, measured the right way

Raw successor pay levels barely differ — external $10.4M median, internal $9.75M (+6%),
not significant (Mann-Whitney p=0.82). The premium is not in the level; it is in the
**change relative to the predecessor replaced**:

- Internal promotes: 0.907x predecessor pay (median), i.e. **−9.3%** — homegrown
  successors start below the departing veteran.
- External hires: 1.119x predecessor pay (median), i.e. **+11.9%** — outsiders command a
  raise over the person they replaced.

The spread is **21.2 percentage points**, external over internal, and it is significant on
the non-parametric test (Mann-Whitney, external > internal, p=0.0074). It is not
significant on a t-test of log means (p=0.34), because the mean is distorted by a few large
packages; the premium is a robust **median/distributional** phenomenon, not a mean one.
This is reported honestly both ways. The magnitude sits squarely in Bidwell's (~18%) range.

## Finding 2: external hires deliver worse, unadjusted

- Market-adjusted TSR (−2/+3yr): internal median −0.04, **external median −0.33**.
- ROA change (post − pre): internal ~0.00, **external −0.013**.

Strong causal caveat: external hires disproportionately go to already-troubled firms, and
the TSR window includes two pre-hire years, so part of this gap is selection (bad firms
hire outsiders), not the hire's effect. This comparison needs controls and an event-time
split before any causal reading. Directionally it matches the literature; causally it is
not yet established.

## Finding 3 (the headline): the premium does not predict the return

Among external hires, the size of the pay premium is **uncorrelated** with the return that
follows:

- premium vs market-adjusted TSR: rho = +0.11, p = 0.51 (n=38)
- premium vs ROA change: rho = −0.04, p = 0.82 (n=39)

Across all hires the relationship is likewise weak and not significant (rho +0.12, p=0.11
for TSR; −0.11, p=0.14 for ROA change). Paying more does not buy more. This is the central
thesis, and it is the same answer the sports free-agency arm reached in a structurally
different market: the premium paid for outside talent does not reliably predict the return
delivered, because mean reversion and buyer-side error dominate. Unlike Finding 2, this
within-group correlation is not driven by the troubled-firm selection effect, so it is the
more robust of the two return results.

## What this is not, yet

Unadjusted. No controls for firm size, industry, year, or the 2020–21 cohort. Comp covers
240 of 611 on the premium ratio, with year-distance fallback noise. Subsamples for the
premium-return correlation are small (n≈38). The next step is the regression layer:
premium and return on classification with controls, survival analysis on tenure, and the
ExecuComp/WRDS reconciliation if access appears. Treat every number here as a first
directional read that the controlled analysis will refine.

## Why it still matters now

After many sessions of infrastructure, the pipeline produced a coherent, literature-
consistent first result on free public data: a real and significant external pay premium,
worse unadjusted outcomes, and — the point of the whole study — no reliable link between
what you pay for outside talent and what you get. The headline the project pre-committed to
("I tested it") now has a tested answer to stand behind, pending the controls.
