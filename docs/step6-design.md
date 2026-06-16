# Step 6 Design: Verification and Enrichment

Date: 2026-06-13. Status: design for owner review. Execution does not start until the owner approves the order of operations.

## Purpose

Step 5 produced a classified panel. Step 6 converts it into an analysis dataset. It does two jobs at once. It attaches primary sources to every preliminary classification. It collects the outcome variables the study measures. The design principle is one workflow per firm: a single pass per company gathers verification evidence and outcome data together, because both live in the same filings.

## Inventory at the start of Step 6

- 589 classified transitions: 432 internal, 157 external (26.7 percent external).
- 146 rule-excluded rows, each with a named exclusion flag.
- 22 VERIFIED rows. 567 PRELIMINARY rows. This is the verification debt.
- 23 PARSED-UNVERIFIED rows carrying candidate successor names from source notes. These still need classification.
- 22 verify-priority rows (list saved separately). These are threshold-zone or continuity cases where exact dates matter.
- 27 review-flag rows (list saved separately). These are sample-affecting questions: 3 exit-mapping conflicts, the spinoff family, 2 short-stint bridges, 2 source artifacts, 1 succession-structure question, 1 constituent-date problem, plus the deal-term documentation set.
- 15 flag-check firms from the re-match (D-051) where constituent membership at the anchor date is unconfirmed. These can add or remove sample rows.

## Order of operations

Sequence matters because some steps change denominators.

1. **Workstream 0: classify the 23 parsed rows.** Same protocol as the lookup batches. One session.
2. **Workstream 1: resolve everything that changes the sample.** The 15 flag-check firms, the 3 exit-mapping conflicts, the constituent-date problem, the 2 source artifacts, and the Fastenal succession-structure question. No analysis denominator is computed before this closes. Output: a frozen sample with a logged decision per change.
3. **Workstream 2: resolve the 22 verify-priority rows.** Exact hire dates from proxy bios and 8-Ks. These can move hired-heir flags and, rarely, classifications. The three continuity cases (Templeton, Breen, Mehrabian) close on Summary Compensation Table salary continuity.
4. **Workstream 3: the per-firm enrichment pull.** This is the bulk of Step 6 and runs firm by firm, not variable by variable.
5. **Workstream 4: the classification freeze.** After workstreams 1 through 3, classifications change only through a dated decision-log entry. Analysis begins after the freeze.

## What the per-firm pull collects

One packet per transition row, drawn from EDGAR filings (8-K, DEF 14A, 10-K) and price data:

1. **Verification fields.** Successor hire date, appointment effective date, and the citation. This upgrades PRELIMINARY to VERIFIED. One source per row, named in the worksheet.
2. **Compensation.** Successor total compensation for the first full fiscal year as CEO, from the Summary Compensation Table. Predecessor total compensation for the last full fiscal year. These two numbers carry the headline premium estimate.
3. **Performance windows.** TSR for the 2 years before and 3 years after the transition, with an index-adjusted version. ROA for the same windows from the 10-K. Window anchors on the appointment effective date.
4. **Tenure and censoring.** Successor end date if departed, or the fixed observation date if still serving. Successor exit type where known. This feeds the Kaplan-Meier and Cox work.
5. **Flag resolution evidence.** Whatever the row's open flags require, gathered in the same pass.

## Tooling and batching

EDGAR is reachable through web fetch. Price data needs a decision: owner upload of a price file, or a public source per ticker. Batching at roughly 20 firms per session keeps the per-session search and fetch volume near the levels the classification batches sustained. At that pace the pull is roughly 30 sessions of mechanical work. The owner should expect this to be the longest phase of the project by elapsed time and the least decision-dense.

## Quality gates

These carry forward from Step 5 because each one earned its place by catching a real error.

- All writes key on row ID. Name matching caused two over-writes; both are logged.
- Counts are computed, never recalled. Five log entries needed sed corrections because a remembered total disagreed with the computed one.
- Recovery sketches and pre-search expectations never enter the worksheet. The Starwood sketch and the Halverson expectation were both wrong; batch review caught both.
- Verification searches fire on conditions, not cadence. Five of the last nine batches were threshold-free and spent nothing.
- The verification ledger stays honest: VERIFIED means a primary or corporate source was checked in session, and nothing else does.

## What Step 6 does not do

It does not revisit ratified rules. It does not add sample rows outside workstream 1. It does not begin analysis. The analysis plan is locked in Phase 0, and the first computed result comes after the freeze.

## Open items for the owner

1. Approve this order of operations or amend it.
2. Decide the price-data source.
3. Decide whether the methods page commitments (merger-of-equals count, deal-term count, manual-row listing, chain-error statistics, the sensitivity ladder) get drafted now from the decisions log or after the freeze. Drafting now is cheap because the log already contains every number.
