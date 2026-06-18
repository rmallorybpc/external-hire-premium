# Two-Arm Design: Talent Premium Study (Business Arm + Sports Comparison Arm)

Date: 2026-06-13. Status: staged design. The framing and the panel spec are written now.
The panel is NOT assembled until the business arm produces its first real effect sizes
from the WRDS pull, so that when the arms sit side by side they carry comparable
statistical weight and "business leads" is true in the numbers, not only the layout.

## The thesis

One question, asked in two structurally different markets for talent: does the premium
paid for outside talent predict the return it delivers? Prior work in both domains points
the same way, weakly or not at all, because mean reversion and buyer-side error dominate.
The convergence is the contribution. The piece is a thesis with corroboration, not two
studies stapled together.

## Arm roles (do not let these invert)

- Business arm is the headline: S&P 500 CEO transitions 2010-2022, external versus
  internal. Premium from compensation (WRDS ExecuComp TDC1). Return from TSR and ROA
  (CRSP, Compustat). Survival on tenure. Anchored by Bidwell, Groysberg, Boivie et al.
- Sports arm is one corroborating panel: four published TMG free-agency studies. Cited
  and linked, not re-run inside this artifact. Supporting evidence, not the subject.

Enforcement, not intention: the sports numbers are already precise and published; the
business numbers are not computed yet. A reader's eye goes to the precise number, so the
artifact tips toward sports by default. The only real guard is sequence. The comparison
panel is assembled AFTER the business arm has comparable effect sizes, never before.

## The comparison panel (singular)

One snapshot table, one figure, one interpretation paragraph. Structure:

| Domain | Market | Premium measure | Return measure | Premium-to-return finding | Effect size |
|---|---|---|---|---|---|
| CEO (business, headline) | S&P 500 hires 2010-2022 | external pay premium (TDC1) | TSR / ROA / tenure | TBD from WRDS pull | TBD |
| NHL UFA | 9 seasons, 1,648 signings | offseason UFA spend | next-season change | spend does not predict change | prior-to-next slope -0.42, p<0.001 |
| NFL FA | 10 seasons, 643 moves | top-spender flag | win-gain | top spender rarely top gainer | roster construction > dollars |
| NBA supermax | 8 seasons, rotation players | supermax flag | performance change | penalty vanishes with controls | movers decline > stayers |
| NHL play-for-contract | same- vs new-team | cap share | time on ice | same-team delivers more per cap share | +0.70 min/game-equiv, p<0.0001 |

The CEO row is filled last and leads the table visually (top row, bold). The four sports
rows are corroboration beneath it.

## KPI definitions: analogous, not identical

State this explicitly. KPIs are operationalized appropriately in each domain, not
literally identical, because a CEO is not a free agent, TSR is not time on ice, and a
pay premium is not a cap-share signing cost. The claim is stronger this way: the same
question, operationalized for each market's structure, converges on the same answer
DESPITE the markets being different. This preempts the obvious referee objection that
"identical KPIs across sports and business" cannot be true.

- Premium paid: pay above the internal/stay baseline (business: external vs internal
  TDC1; sports: signing cost or cap share vs comparable retained talent).
- Return delivered: domain-appropriate outcome (business: TSR, ROA, tenure; sports:
  win/performance change, time on ice).
- Pay-to-performance gap: return regressed on premium, with controls. The shared finding
  is a flat or negative relationship after controls.

## Controls, by arm (analogous, disclosed)

- Business: prior firm performance, predecessor pay, CEO tenure/age proxy, year, industry,
  the 2020-21 cohort flag. Mean-reversion check: post-return regressed on pre-return.
- Sports: prior finish, age, tier, season. Mean-reversion is the headline mechanism
  (NHL slope -0.42).

The mean-reversion parallel is the spine of the cross-domain story: both markets pay for
recent outcomes that do not persist.

## The strategy-prevalence-over-time view (formerly "adoption")

Present the external-hire rate over time as the prevalence of a hiring strategy against
its returns. Do NOT call it product/user adoption. The series already exists from the
classification: 26.3% (2010), trough 14.3% (2016), peak 44.7% (2017), frozen-board 17.9%
(2021), 23.7% (2022). Plot the rate against the average return to external hires by cohort
year. If the label "adoption" is earned honestly as strategy-adoption, fine; if it has to
be stretched to hit a resume keyword, drop the word and keep the chart. The chart is the
asset, not the label.

## Guardrails carried from the audit (do not drop)

- No predictive or decision-tool claim. Backward-looking analysis. The finding is that the
  premium does not reliably predict return; this is not a tool that picks the next hire.
- Business leads, enforced by sequence (panel assembled after business effect sizes exist).
- Snapshot files with provenance notes and a refresh script for any cross-repo assembly.
  No live cross-repo fetching. Reliability over the appearance of sophistication.
- Length is attention. If the sports panel runs longer than the CEO results section, the
  artifact has betrayed the headline regardless of the prose. Hold the sports arm to one
  panel.

## Build sequence (staged)

1. Now: this design doc and the framing paragraph. Done.
2. Gate: WRDS pull produces business effect sizes (premium, return-on-premium, survival).
3. Then: assemble the snapshot table (fill the CEO row), build the one figure, write the
   interpretation paragraph.
4. Then: the prevalence-over-time chart from the already-frozen classification.
5. Publish within the business piece, sports as the corroborating panel.

## Cross-arm framing paragraph (draft, for the welcome/findings page)

> Two markets price outside talent: the executive labor market and professional sports
> free agency. They look nothing alike, yet they are asked to solve the same problem,
> paying a premium for talent hired from outside in the hope of a better result than
> promoting from within. This study tests, in the business market, whether that premium
> predicts the return that follows, and sets the result beside four prior analyses of the
> same bet in the NHL, NFL, and NBA. The domains differ in every detail and converge on
> one answer: the premium paid does not reliably predict the return delivered, because in
> both markets buyers pay for recent outcomes that tend not to persist. The business
> analysis leads; the sports work corroborates.
