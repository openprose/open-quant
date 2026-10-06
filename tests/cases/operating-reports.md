# Distinguishing cases for operating reports

These are authored interpretation cases, not model evaluation results. A mechanical checker covers only the monitoring fixture's explicit data relationships. Review the actual report against every adopted requirement, including source support, coverage, effects and its fulfillment claim.

| Contract | Supported reporting | Missing evidence | Contradictory or misleading reporting |
|---|---|---|---|
| Model inventory | Reconcile a stated deployment population and inventory using supplied identity rules; expose an unregistered deployment. | No comparison population: describe the inventory but leave organization-wide completeness unestablished. | Same display name at two revisions is collapsed into one model despite distinct supplied identities. |
| Model change | Same-date, same-input comparison identifies output changes and the affected documented use. | Missing prior inputs: identify the comparison limit rather than claim equivalence. | A code change is credited for a difference when market date and population also changed. |
| Model monitoring | All four expected observations accounted for; one measured breach remains adverse. | Missing O3 is unresolved, not a third-model omission or a passing observation. | O3's label says within limit but its 1.2 bp value breaches the 1.0 bp limit. |
| Limitations and remediation | Report I1 as overdue with unsupported closure and its recorded owner. | Closure evidence is unavailable: disclose the gap and leave closure unsupported. | Treat an action-complete timestamp as proof that closure criteria were met. |
| Model data | Distinguish valuation date from feed publication time and trace supplied adjustments. | Transformation evidence missing: identify the missing link rather than invent processing. | Substitute zero for absent quotes, then claim no missing values. |
| Calibration review | Compare all supplied calibration targets and fits in the correct units, while limiting conclusions to fit. | One target lacks a fit: preserve the missing calibration item and denominator. | A success flag overrides a residual outside the supplied tolerance, or in-sample fit is called predictive accuracy. |

## Monitoring fixture expectations

- `complete`: three within limit, one breach, none unresolved; overall breach. The report can be fulfilled by accurately reporting this adverse result.
- `missing`: three within limit, no observed breach, one unresolved; overall unresolved. I1's history does not supply the absent September observation. A report can be fulfilled by explaining the missing observation and unsupported closure; an all-clear claim cannot.
- `contradictory`: the same quantitative findings as complete, plus an explicit contradiction between O3's label and value. The label does not replace the observed value.

All three cases must discuss I1, for which the action-complete date does not satisfy the two-part closure requirement. Each case's source population is separate; importing O3 from a different case would violate the program's evidence boundary.

Additional mechanical mutations check equality at the limit, wrong units, wrong revision, duplicate matches, missing observations and an unrecognized metric. Passing these controls establishes the fixture checker's handling of those cases, not the adequacy or execution of arbitrary contracts.
