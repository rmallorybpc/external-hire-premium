# The Talent Premium, Two Markets: Comparison Panel

One question, asked in two markets that look nothing alike: **does the premium paid for
outside talent predict the return it delivers?** The business analysis leads; four prior
sports free-agency studies corroborate. The domains differ in every mechanical detail and
converge on one answer.

## Framing

Two markets price outside talent — the executive labor market and professional sports free
agency. They are structurally unrelated, yet both are asked to solve the same problem:
paying a premium for talent acquired from outside, in the hope of a better result than
promoting or retaining from within. This study tests, in the business market, whether that
premium predicts the return that follows, and sets the result beside four prior analyses of
the same bet in the NHL, NFL, and NBA. The answer converges: **the premium paid does not
reliably predict the return delivered, because in both markets buyers pay for recent
outcomes that tend not to persist.** Mean reversion and buyer-side error dominate.

## The comparison panel

| Domain | Market & sample | Premium measure | Return measure | Does the premium predict the return? | Key statistic |
|---|---|---|---|---|---|
| **CEO hires (business — headline)** | **S&P 500, 2010–2022; 611 transitions, 158 external** | **External pay premium over predecessor (TDC1-style total)** | **Post-hire market-adj TSR; ROA change** | **No** | **premium ≈ +9% (n.s.); premium→TSR p=0.14, premium→ROA p=0.45 — indistinguishable from zero** |
| NHL free agency | 9 seasons, 1,648 UFA signings, 284 team-seasons | Offseason UFA spend | Next-season point change | No | spend not predictive; prior-finish→next-change slope −0.42, p<0.001 (mean reversion) |
| NFL free agency | 10 seasons, 643 moves | Top-spender status | Win gain | No | top FA spender rarely the top win-gainer; roster construction outweighs dollars |
| NBA supermax | 8 seasons, rotation players | Supermax contract | Performance change | No | supermax penalty vanishes once age + prior performance controlled; movers decline more than stayers |
| NHL play-for-contract | same-team vs new-team signings | Cap share | Time on ice | (retention beats acquisition) | same-team +0.70 min/game-equiv per cap share, p<0.0001 — the loyalty discount |

## Interpretation: one mechanism, two markets

The common thread is **mean reversion in what buyers pay for**. In sports, teams and clubs
pay for a player's recent peak — a career year, a deep playoff run — and the next season
regresses (the NHL prior-finish slope of −0.42 is this directly). In the executive market,
boards pay a premium for an outside CEO at the moment of a visible problem, and the firm's
trajectory was already mean-reverting (which is why the raw "external underperformance"
was mostly the inherited decline, not the hire). In both, the premium is priced off the
recent past, and the recent past does not persist. The buy-side error is structurally the
same even though a CEO is not a free agent and TSR is not time on ice.

## What this panel does and does not claim

- **Claims**: across two unrelated markets, the premium paid for outside talent does not
  reliably predict the return delivered. This is the robust, replicated finding.
- **Does not claim**: a predictive model or a hiring decision tool. This is backward-looking
  analysis of a bet, not a method for picking the next hire.
- **KPIs are analogous, not identical.** A CEO is not a free agent; a pay premium is not a
  cap-share signing cost; TSR is not time on ice. The strength of the result is convergence
  *despite* structural difference, not a false claim of identical metrics.
- **Business leads.** The CEO analysis is the headline (top row, the study's own data); the
  four sports studies are a single corroborating panel, cited not re-run here.

## The honest hierarchy of claims (carried from the business analysis)

The flashy version — "outside talent costs more and delivers less" — does not hold up: the
cost premium is directional but imprecise, and the market-return shortfall is mostly
selection. The claim that survives every control in the business data **and** replicates in
four sports datasets is the quieter one: **what you pay for outside talent tells you little
about what you will get.** That is the thesis, and the two arms together are its evidence.

## Sources (sports arm)

The four sports studies are prior published TMG analyses, linked from the site and cited
here as corroborating evidence; their underlying data is not re-run in this artifact. The
business arm's data and code are in this repository and fully reproducible from public
sources.
