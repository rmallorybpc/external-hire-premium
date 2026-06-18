# Controlled Findings: Regression and Survival

Date: 2026-06-13. Status: the controlled layer. Estimates with firm-size and year controls,
robust (HC1) standard errors, plus survival analysis on CEO tenure. Still subject to two
known limits: no industry fixed effects (SIC not collected), and the return comparisons
carry a selection confound described below. These are defensible first estimates, reported
with their uncertainty, not headline-ready point claims.

## 1. The premium: directionally Bidwell-sized, but imprecise

Controlling for predecessor pay, firm size, and year:

- log(successor pay) on external: **+6.3%**, p=0.59 (n=236)
- log(successor/predecessor pay ratio) on external: **+10.7%**, p=0.43 (n=236)

The point estimate (~11% over the predecessor, vs internal) sits in Bidwell's ~18%
neighborhood and points the same way. But on the parametric (mean) test it is **not
statistically significant** — the confidence interval comfortably includes zero. This is
the honest tension in the data: the premium is significant on the non-parametric median
test (Mann-Whitney p=0.0074) but not on the mean, because executive pay is heavy-tailed and
the sample (236 with both pay figures) is modest. Read plainly: **the premium is
directionally present and the right size, but this sample cannot reject "no premium" on the
mean.** A larger compensation sample (filling more transitions, resolving the unmatched
tickers and the no-proxy gaps) is the path to tightening it.

## 2. External hires are associated with worse outcomes — but selection confounds it

Controlling for size and year:

- Market-adjusted TSR (−2/+3yr) on external: **−29 percentage points**, p=0.004 (n=423)
- ROA change (post − pre) on external: **−2.3 points**, p=0.017 (n=461)

Both are statistically significant and survive the basic controls. But the confound is
serious and must lead the interpretation: **external CEOs are disproportionately hired by
already-struggling firms**, and the return window opens two years *before* the hire, so it
captures the decline that prompted the outside search. Size and year controls do not remove
this. So the correct statement is associational — external-hire situations have worse
returns — not causal. Establishing whether external *hiring* worsens returns needs an
event-time design (returns measured only after the hire) and ideally a matched-firm or
instrumented comparison. Flagged as the priority refinement.

## 3. Headline: the premium does not predict the return (robust null)

Does paying a bigger premium buy a better result? No, and this survives controls:

- premium (log pay ratio) on market-adjusted TSR: +0.21, p=0.19 (n=189)
- premium x external interaction: −0.06, p=0.85
- premium on ROA change: −0.04, p=0.25 (n=204)

Every estimate is statistically indistinguishable from zero. The amount paid over the
predecessor carries no reliable signal about the return that follows. This is the study's
central thesis, and it is the **most robust** of the results here, because — unlike Finding
2 — it is a within-relationship slope, not a level comparison, so the troubled-firm
selection effect does not drive it. It is also the same answer the sports free-agency arm
reached in a structurally unrelated market: the premium paid for outside talent does not
predict the return delivered, because mean reversion and buyer-side error dominate.

## 4. Survival: no significant tenure difference

CEO tenure derived from the transition chain (each successor served from appointment to the
next transition at that firm, or censored at the 2022 window end). 608 spells, 171 observed
departures, 437 censored.

- Kaplan-Meier median tenure: internal 10.5 yrs, external 10.5 yrs — essentially identical.
- Log-rank test: p=0.34 (no difference).
- Cox proportional hazards (external + size + year): external hazard ratio **1.28**, p=0.20
  — external CEOs depart somewhat faster, but not significantly.

Direction matches the intuition that outside hires are shorter-lived, but the effect is not
significant. Heavy censoring (72%, because the window ends in 2022 and recent appointees
have short observed spells) inflates the KM medians and limits power; this is the result
most constrained by the window length.

## The honest synthesis

1. The external pay premium is **directionally present and Bidwell-sized (~11%)** but not
   precisely estimated — robust in medians, not in means.
2. External-hire situations show **significantly worse returns**, but **selection into
   troubled firms confounds** this; it is associational, not causal, pending an event-time
   design.
3. The premium **does not predict the return** — the most robust finding, controls and all,
   and the cross-domain echo of the sports arm.
4. **No significant tenure difference**, external directionally shorter.

## What strengthens these next

- More compensation coverage (ticker fill, no-proxy gap-filling) to tighten the premium CI.
- Industry fixed effects (collect SIC from SEC submissions) — the one missing control.
- An event-time return design (post-hire-only windows) to address the selection confound on
  Finding 2.
- ExecuComp/WRDS reconciliation if access appears, as an independent check on the free-data
  compensation figures.

These are real, defensible estimates a reader can interrogate — including where they fall
short of significance, which is stated rather than hidden.
