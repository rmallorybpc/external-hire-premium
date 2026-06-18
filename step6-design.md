# Refined Findings: Industry Controls + Post-Hire-Only Returns

Date: 2026-06-13. Status: the most defensible estimates this data supports. Adds 2-digit
SIC industry fixed effects and, critically, separates the return window into post-hire-only
(appointment to +3yr) versus the full straddling window, to break the selection confound.
Robust (HC1) errors throughout. This supersedes the return/selection reading in the prior
controlled findings.

## 1. The premium: unchanged by industry controls — still directional, still imprecise

log(successor/predecessor pay ratio) on external, with size, year, AND industry fixed
effects: **+8.8%**, p=0.54 (n=236). Adding industry controls barely moved it from the
+10.7% without them. The conclusion stands: the premium is directionally present and
Bidwell-sized, but not statistically distinguishable from zero on the parametric test in
this sample. Note the ticker fill did not help here — it widened TSR coverage, not
compensation, and the premium is limited by comp coverage (236 paired figures). Tightening
it requires filling the no-proxy compensation gaps, not more tickers.

## 2. The return result was mostly selection — this is the key refinement

The headline number from the prior pass — external hires associated with ~29–38 points
lower market-adjusted TSR — **largely disappears once we measure only the post-hire period**:

- FULL window (−2yr to +3yr, straddles the hire): external **−38.5 points**, p=0.0005
- POST-HIRE ONLY (appointment to +3yr): external **−11.9 points, p=0.14 (NOT significant)**

Both with industry, size, and year controls, same 431-firm sample. Reading this honestly:
roughly two-thirds of the apparent external underperformance was the **inherited decline**
— the slump that prompted the outside search in the first place, captured in the pre-hire
years of the window. Once we look only at what happened *after* the external CEO arrived,
the stock-return gap shrinks by more than two-thirds and is no longer statistically
significant. **We cannot claim external hires deliver worse stock returns.** The earlier
result was substantially a selection artifact, exactly as the confound warning predicted.

Operating performance is the exception that survives: ROA change (post − pre) on external is
**−2.5 points, p=0.009**, still significant with industry FE. So on accounting performance
around the transition there is a real, if modest, external shortfall; on market returns,
once de-confounded, there is not a significant one.

## 3. Headline holds: the premium does not predict the return

With industry fixed effects and the clean post-hire return:

- premium on post-hire market-adjusted TSR: +0.15, p=0.14 (n=189)
- premium on ROA change: −0.02, p=0.45 (n=204)

Both indistinguishable from zero. Paying a larger premium does not buy a better result,
and this survives every control we can apply. It is the most robust finding in the study,
and the cross-domain match to the sports free-agency arm.

## 4. Survival (unchanged): no significant tenure difference

From the prior pass, not re-run here: KM median tenure identical (~10.5yr), Cox external
hazard ratio 1.28, p=0.20 — directionally shorter, not significant, limited by window-end
censoring.

## The defensible bottom line

After the fullest controls this data allows:

1. **Premium**: directional (~9%), Bidwell-sized, not statistically significant — robust in
   medians, imprecise in means. Limited by compensation coverage.
2. **Stock returns**: the external underperformance was **mostly a selection artifact**;
   post-hire-only, it is not significant. This is a correction to the earlier reading, and
   the honest result.
3. **Operating returns (ROA)**: a small but significant external shortfall persists.
4. **The premium does not predict the return**: robust to industry FE and post-hire
   windows, in both the business data and the sports comparison arm. The study's anchor.
5. **Tenure**: no significant difference.

The one claim that survives every control, every de-confounding, and replicates across two
unrelated markets is the thesis the project was built on: **the premium paid for outside
talent does not predict the return it delivers.** The flashier claim — "external hires cost
more and deliver less" — does not hold up: the cost premium is imprecise, and the
delivery shortfall is mostly selection on the market-return side. Leading with the robust
claim rather than the flashy one is the difference between a defensible study and an
overclaim.

## Addendum: the selection mechanism, quantified (D-098)

The selection confound was tested directly, not inferred. Pre-hire performance, external vs
internal:

- Pre-hire market-adjusted TSR (two years to appointment): external median −18.2%, internal
  −1.7%. Mann-Whitney p < 0.0001. External hires concentrate in firms whose stock lagged the
  market.
- Pre-hire ROA: external 7.2%, internal 5.7%. No difference (p = 0.91). These were not firms
  in operating crisis.
- Spread: 70% of external hires followed below-market stock performance, 30% followed
  above-market. Not a universal rule.

Reading: the trigger for an outside hire is share-price disappointment, not operating
decline, and not in every case. This explains the straddling-window underperformance (the
pre-hire stock lag inflated it) and matches the glass-cliff literature, where Ryan and Haslam
(2005) found women appointed to boards after share-price declines, measured on stock price
rather than operating performance. The same selection signature appears here for external
CEO hires. Source for the glass cliff: Ryan and Haslam, British Journal of Management (2005);
popularized in Freakonomics Radio Episode 319 (2018).
