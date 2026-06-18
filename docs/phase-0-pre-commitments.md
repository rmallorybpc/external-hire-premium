# Phase 0 pre-commitments: external hire premium study

**Status:** Pre-committed before data assembly. Drafted June 10, 2026.
**Amendment rule:** Any change after data assembly begins is logged as a dated amendment with a stated reason. Silent edits are not allowed. The amendment log publishes with the audit page.

---

## 1. Study boundaries

- **Scope.** CEOs of S&P 500 firms. Index membership is measured at the transition date.
- **Appointment window.** Transitions from January 1, 2010 through December 31, 2022. Rationale: every cohort, including the latest, gets a full 3-year post-appointment performance window with reportable data. Appointments after 2022 are outside the study by design, not by oversight.
- **Observation date.** Fixed on the day the final data pull completes. The date is recorded on the methods page. All tenure and performance are measured through that date. Events after it, newsworthy or not, are outside the study.
- **Censoring.** CEOs still serving on the observation date are right-censored. They count as "lasted at least X months." They are not counted as successes or failures.

## 2. Primary classification rule

**Internal:** employed by the firm or a consolidated subsidiary, as an employee, for 12 or more continuous months at the CEO appointment date.

**External:** everyone else.

Non-executive board service does not count as employment.

## 3. Edge case rules

Each edge case gets a rule, a subgroup flag, and a planned sensitivity check. Flags are recorded in the panel so any reader can rebuild the sample under different rules.

| Case | Rule | Flag | Sensitivity check |
|---|---|---|---|
| Interim CEO | Interim appointments are excluded from the main sample. If the interim becomes permanent, the transition enters at the permanent appointment date. Interim service counts toward employment months. The tenure-in-role clock starts at the permanent appointment. | interim-to-permanent | Exclude these entirely |
| Board member steps in | External unless they meet the primary rule through actual employment. | board-insider | Reclassify as internal |
| Boomerang (amended 2026-06-13) | A former employee with any employment gap at appointment is external; the prior 12-month gap qualifier is removed. Returns with continuous employment (e.g. salaried executive chairman) remain governed by the primary rule. | boomerang; returning-former-ceo | Returning-former-CEO subgroup reported separately |
| Founder return | A boomerang special case. External by the primary rule. | founder | Exclude founders entirely |
| Hired to be promoted | Executive hired from outside into a senior role, then promoted to CEO. The primary rule applies: 12 or more months employed means internal. Flag if promoted within 24 months of joining the firm. | hired-heir | Reclassify as external |
| Co-CEOs | Excluded. | co-ceo | None |
| Predecessor death or sudden incapacity | Successor is included. The predecessor exit is excluded from forced vs voluntary analysis. | exogenous-exit | Exclude successors |
| Merger, acquisition, or buyout (friendly or hostile) | Transitions caused by a change of control are excluded, including hostile takeovers and take-private deals. A sitting CEO's tenure is censored on the date the firm ceases independent existence or leaves public markets. The incumbent's exit is excluded from forced vs voluntary analysis. | change-of-control | None |
| Activist pressure without change of control | If the firm stays independent and the board replaces the CEO under investor pressure, the transition is a real board hiring decision and stays in the sample. The exit is presumed forced. | activist-exit | Exclude these |
| Firm later exits the S&P 500 | The CEO stays in the sample. Cohort membership is fixed at the transition date. | index-exit | None |
| Spinoff or corporate split (ratified amendment, 2026-06-12) | When the index entity continues under a new identity and a unit head is promoted to CEO, classify by the primary rule using tenure at the pre-split parent. | review-spinoff | Exclude spinoff transitions |
| Merger of equals with continued CEO (ratified amendment, 2026-06-12) | When the surviving index entity's CEO was specified in the merger agreement itself, the transition is excluded: the post-close board inherited the CEO and made no succession choice, and leadership continued from a predecessor entity, so no hiring event occurred. The predecessor CEO's exit is excluded from forced vs voluntary analysis as a deal term. | merger-of-equals-continued-ceo | Count and report occurrences on the methods page |
| Acquirer installs the acquired company's CEO (ratified amendment, 2026-06-13) | When the index entity is the acquirer and its board installs the acquired company's CEO, the transition stays in the sample as an external hire: the board chose not to retain its own CEO and recruited leadership from outside, a hiring decision negotiated through a deal. The flag preserves these cases for a methods page count. | review-deal-term-ceo | Count and report occurrences on the methods page |
| Manual row for confirmed source gaps (ratified amendment, 2026-06-13) | A transition at a confirmed point-in-time constituent that is absent from the source database may be added manually, subject to all of: primary-document provenance (8-K or equivalent) for the departure, the successor, and the dates; a synthetic row ID outside the source's range; departure coding assigned by this project and marked as such; and a methods page count of manual rows. Anchor dating follows the source's own convention for comparable rows. Expected use is rare. | manual-row | Manual rows counted and listed on the methods page |

## 4. Exit classification

Exits are classified as forced, voluntary, or unclassified.

- Departures at age 60 or older with an announced retirement are voluntary, following the convention in Parrino (1997).
- Departures to a senior government appointment (cabinet post, ambassadorship, agency leadership, or elected office) are voluntary regardless of age. The move is treated as an exit to a role of equal stature. Flag: government-exit.
- Departures before 60, or without an announced retirement, health reason, or move to a comparable role, are presumed forced unless contemporaneous press coverage indicates otherwise.
- Unclassified is an allowed outcome. No exit is forced into a label to make the data cleaner.

## 5. Measurement definitions

- **Compensation:** total compensation from the DEF 14A summary compensation table, first full fiscal year in the role.
- **TSR:** stock price change plus dividends, measured over windows from 2 years before to 3 years after appointment.
- **ROA:** net income divided by total assets, same windows.
- **Tenure:** months from appointment to exit, or to the observation date if censored.
- **Predecessor comparison:** difference and ratio of the new CEO's tenure against the predecessor's completed tenure. Predecessor tenures are complete by construction.
- **Survival analysis:** Kaplan-Meier curves by hire type. Cox proportional hazards model with firm size, industry, and year controls.

## 6. Pre-committed robustness checks

1. Replace the 12-month employment threshold with 6 months, then 24 months.
2. Exclude interim-to-permanent transitions.
3. Exclude founders.
4. Exclude 2020 and 2021 appointments as a COVID sensitivity check.
5. Reclassify board-insider and hired-heir subgroups per the table above.

No robustness checks are added after results are known unless logged as a dated amendment.

## 7. Outcome framing

The headline is "I tested it," not "I confirmed it." Both outcomes are publishable. There is no third option.

- **If the premium appears:** External CEO hires in the 2010 to 2022 S&P 500 cost more and delivered less, consistent with Bidwell (2011).
- **If the premium does not appear:** The external hire premium documented by Bidwell (2011) does not replicate in 2010 to 2022 S&P 500 CEO data, and the gap between the two findings is the story.

## 8. Decisions log

Every classification judgment call is recorded at the time it is made: company, transition date, rule applied, decision, flags assigned, and date decided. The log publishes with the audit page. A reader should be able to disagree with a call and trace exactly where it changed the sample.
