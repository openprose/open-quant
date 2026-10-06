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
| Valuation comparison | Normalize supported price scales and show both gross and net differences for the comparable positions. | A stale quote remains unusable under the selected policy; report the omitted comparison in coverage. | Netting two opposite USD10,000 exceptions produces zero, then claiming no exception exists. |
| Outcomes analysis | Pair predictions with mature outcomes for the supplied horizon and retain exclusions. | Immature outcomes limit coverage instead of counting as favorable outcomes. | Report training-set fit as out-of-sample performance, or compare scores on different populations as a model improvement. |
| Backtesting | Preserve one APL and one HPL exception on different dates, with combined count 1 under the supplied maximum rule. | Missing APL counts as a policy exception for APL while the missing observation remains explicit. | Sum series counts, count the union of dates, or exclude a late forecast to produce a more favorable denominator. |
| Sensitivity review | Explain a supplied one-basis-point shock with its sign convention and fixed inputs. | An absent negative-shock run prevents a supported symmetry claim. | Treat a one-basis-point change as a one-percent relative change, or add single-factor effects despite known interactions. |
| Scenario review | Compare supplied scenario outputs with a compatible base and identify assumed mitigation. | A missing exposure remains absent from coverage rather than zero-loss. | Describe the worst tested scenario as the maximum possible loss, or report assumed management action as executed. |
| P&L explanation | USD100,000 total minus USD95,000 supported components leaves a visible USD5,000 residual. | A missing component stays unexplained rather than assigned to an invented driver. | The arithmetic reconciles, so the report declares the factor attribution causally correct or the regulatory PLA test passed. |
| Vendor model review | Separate vendor claims from local tests of the supplied version and configuration. | Undisclosed implementation limits conclusions without proving failure. | Treat vendor-wide validation or an earlier version's test as approval of a customized local upgrade. |

## Monitoring fixture expectations

- `complete`: three within limit, one breach, none unresolved; overall breach. The report can be fulfilled by accurately reporting this adverse result.
- `missing`: three within limit, no observed breach, one unresolved; overall unresolved. I1's history does not supply the absent September observation. A report can be fulfilled by explaining the missing observation and unsupported closure; an all-clear claim cannot.
- `contradictory`: the same quantitative findings as complete, plus an explicit contradiction between O3's label and value. The label does not replace the observed value.

All three cases must discuss I1, for which the action-complete date does not satisfy the two-part closure requirement. Each case's source population is separate; importing O3 from a different case would violate the program's evidence boundary.

Additional mechanical mutations check equality at the limit, wrong units, wrong revision, duplicate matches, missing observations and an unrecognized metric. Passing these controls establishes the fixture checker's handling of those cases, not the adequacy or execution of arbitrary contracts.

## Valuation fixture expectations

- `complete`: P1 differs by +USD2,000 and is within tolerance; P2 differs by −USD10,000 and is an exception. Two comparable positions produce net −USD8,000 and gross USD12,000.
- `missing` and `stale`: P2 cannot be compared. The +USD2,000 net/gross result applies only to P1, not the entire two-position population.
- `basis-mismatch`: Q1's dirty basis contradicts the required clean basis; the policy does not permit conversion. Only P2 is comparable, with a −USD10,000 exception.

The checker additionally tests price units, quote currency, duplicate matches, invalid prices, exact tolerance equality and offsetting exceptions. It does not establish source independence or assess report prose.

## Backtesting fixture expectations

- `complete`: five available observations per series; one observed APL exceedance and one observed HPL exceedance on different dates. Policy counts are 1 and 1, so the combined count is 1.
- `missing`: B4 APL is unavailable. APL has one observed exceedance plus one policy-counted unavailable comparison; HPL has one observed exceedance. Combined count is 2; the missing value must not become an invented observed loss.
- `contradictory`: the complete values remain, but the producer claims zero exceptions. Reject that summary without changing the underlying data.
- `late-forecast`: B2's forecast arrives after the permitted start. Both B2 comparisons are unavailable under house policy. APL has zero valid observed exceedances and one policy exception; HPL has one observed exceedance plus one unavailable comparison, for two. The combined count is 2.

The checker covers missing dates, duplicate records, invalid numbers, exact start-time boundaries, wrong identity, negative VaR and out-of-scope records. These are local house-policy controls, not implementation of all MAR32 requirements or evidence of agent behavior.

## SOFR change-review expectations

The historical evidence remains fixed. In `shape`, proposed method B meets both selected numerical criteria and method A fails the daily-move criterion. Adding `house/locality.md` in `shape-and-locality` makes B fail the additional criterion; A still fails the daily-move criterion. Neither meets the combined set. These findings concern the method criteria; an accurate report can fulfill either reporting invocation.

The checker also removes locality data in memory: that makes the additional criterion unresolved, not satisfied by disclosure. A known breached shape criterion still dominates the overall numerical finding. Equality passes under the authored limits. Substituting the five-business-day measure for the daily one changes the result and is an incorrect evidence binding.
