# September monitoring review — authored reference

Case: `complete`. Review date: October 5, 2026. This is a hand-authored illustration using synthetic data, not a recorded agent run or an institutional review.

## Monitoring

| Expected record | Source observation | Observed value | Finding |
|---|---|---|---|
| E1: USD-CURVE r3 repricing | O1 | 1.0 bp | Within limit; equality passes. |
| E2: USD-CURVE r3 missing inputs | O2 | 0 count | Within limit. |
| E3: CREDIT-SPREAD r2 repricing | O3 | 1.2 bp | Breach; 0.2 bp above the 1.0 bp limit. |
| E4: CREDIT-SPREAD r2 missing inputs | O4 | 0 count | Within limit. |

All observations concern September 2026. Coverage is four of four expected observations: three within limit, one breached and none unresolved. No unmatched or duplicate observation is present in this case. Producer labels agree with the values. The overall control finding is **breach** under the house aggregation rule; complete coverage does not make this an all-clear result.

Evidence: `inputs/packet.json`, `expected_observations` E1–E4 and `cases.complete` O1–O4; `inputs/policy.md`, observation matching, thresholds and aggregation. The 0.2 bp excess is 1.2 minus 1.0 using those inputs.

## Open issue

I1 records an investigation of quote mapping for CREDIT-SPREAD r2, owned by Credit Analytics and due October 1. Although its producer status is closed and its action-complete date is September 30, both the closure observation and review record are absent. Closure is unsupported under the house rule. The issue is overdue at the October 5 review date. O3 is a breach and cannot substitute for the required passing post-action observation.

Credit Analytics needs to supply the required closure evidence or a disposition. This report does not change the issue or send a notification. Evidence: `inputs/packet.json`, `issues` I1 and `models`; `inputs/policy.md`, issue closure and response rules.

## Scope

The reference report accounts for every expected observation and supplied issue. The operating findings remain adverse even though the reporting content is complete. The packet does not establish broader model validity, future performance, risk acceptance or institutional approval. No execution trace accompanies this authored illustration, so it is not evidence of permissions being respected in an actual run.
