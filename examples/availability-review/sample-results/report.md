# Authored reference: complete historical-input review

This is an authored reference for the complete packet, not an agent result. All six selectors and ten decisions are covered below. The exercise retrospectively selects synthetic features; it is not a log of actual forecasting or ingestion. Later corrected values intentionally equal the supplied outcomes. No error score establishes economic usefulness or operational readiness.

The selected policy requires exact entity/observation-date identity, publication and known local availability at or before cutoff, and the highest eligible revision. Conflicting records cannot be resolved by record ID. All known times are UTC; equality is allowed. The table reports independently supported selection evidence, not whether a query ran successfully. “Unavailable” means no eligible record in the supplied history; “unresolved” preserves missing availability. [Evidence: policy.md; complete.json/features and decisions.]

| Selector | Supported decisions | Breached decisions | Other requested decisions |
|---|---|---|---|
| point_in_time | D02, D04, D05, D06, D07, D10 | none | unavailable: D01, D03; ambiguous: D09; unresolved: D08 |
| latest_revision | D10 | D01, D02, D03, D04, D05, D06, D07, D09 | unresolved: D08 |
| published_only | D04, D05, D06, D07, D10 | D01, D02, D03, D09 | unresolved: D08 |
| latest_arrival | D02, D04, D05, D06, D07 | D09, D10 | unavailable: D01, D03; unresolved: D08 |
| unscoped_arrival | D02, D04, D05, D06 | D07, D09, D10 | unavailable: D01, D03; unresolved: D08 |
| observation_date_asof | none | D01, D02, D03, D04, D05, D06, D07, D09, D10 | unresolved: D08 |

Each row covers all ten requested decisions once. The evidence for each cell is its selector's observed selected_record_ids, the linked feature records and that decision's entity, date and cutoff. A recorded selection is an observation to assess; its label does not certify eligibility.

The fixed common population is D02, D04, D05, D06, D07 and D10. Every method has six numeric predictions on those IDs, but that does not establish historical validity. Own-population error uses only each method's uniquely selected values. Missing or ambiguous predictions are retained as exclusions, not zero errors. All quantities below are dimensionless absolute errors. [Evidence: complete.json/selectors/*/rows, own_population and common_population.]

| Selector | Numeric coverage | Own error sum | Own MAE | Common-six error sum | Common-six MAE |
|---|---|---|---|---|---|
| point_in_time | 6/10 | 0.300000000 | 0.050000000 | 0.300000000 | 0.050000000 |
| latest_revision | 10/10 | 0.000000000 | 0.000000000 | 0.000000000 | 0.000000000 |
| published_only | 10/10 | 0.410000000 | 0.041000000 | 0.300000000 | 0.050000000 |
| latest_arrival | 7/10 | 0.360000000 | 0.051428571 | 0.360000000 | 0.060000000 |
| unscoped_arrival | 7/10 | 1.320000000 | 0.188571429 | 1.320000000 | 0.220000000 |
| observation_date_asof | 10/10 | 0.460000000 | 0.046000000 | 0.280000000 | 0.046666667 |

**Corrections and apparent performance.** latest_revision has zero numeric error, including on the common six. Five common selections use revisions published and available after their cutoffs; only D10's choice is eligible. This planted retrospective advantage cannot support a historical forecasting claim. Comparing its ten observations with point_in_time's six without retaining the population difference would also be misleading.

**Publication and receipt identity.** D03's B value was public at 09:00 but locally available at 10:00, after its 09:30 cutoff. D04 at exactly 10:00 is eligible. At D02, published_only chooses R13, a January 6 arrival, while R01 was eligible at the January 2 09:05 cutoff. R13 and R01 contain the same value. That explains how published_only can match the common-six MAE of 0.05 while citing an unsupported historical receipt. It does not show that the numerical value was unavailable through R01. [Evidence: R01, R03, R13; D02–D04 and the corresponding selection rows.]

**Version and period scope.** At D10, latest_arrival chooses revision 1 R13 even though revision 2 R02 is eligible. At D07, unscoped_arrival chooses R09, a November observation, for a January observation-date request. observation_date_asof likewise drops the required period and ignores publication/availability; it breaches nine selections and leaves C unresolved. These findings concern the selected requirements, not a general defect in temporal joins. [Evidence: R02, R09, R13; D07/D10; the six observed selector populations.]

**Missing and conflicting evidence.** D01/D03 have no eligible local input at their cutoffs. C's publication time cannot establish its unknown local availability at D08. D09 has two eligible highest-revision records, R11/R12, with conflicting values. point_in_time retains that conflict; choosing the greater ID imposes a precedence absent from the policy. No source history should be filled, backdated or repaired to make these findings favorable.

No producer claims are present in this complete packet. The review can account for all sixty selections and all metric denominators while preserving the remaining evidence gaps. The receipt identifies the developer calculation; this reference did not rerun it. The findings do not establish production history, statistically reliable forecasting, institutional approval or fulfillment by an agent.
