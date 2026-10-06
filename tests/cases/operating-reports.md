# Distinguishing cases for operating reports

These are authored interpretation cases, not model evaluation results. The fixture scripts check explicitly bound data relationships; none is a general report evaluator. Review the actual report against every adopted requirement, including source support, coverage, effects and its fulfillment claim.

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

## Vendor inventory expectations

- `complete`: D1 has a matching register record and a supported narrow local check. D2 has conflicting version/configuration fields and no exact local test for its deployed configuration. D3 is unregistered and has a local threshold breach. D4 is excluded as sandbox. R3 remains unmatched and conflicts with the supplied retirement event for D5.
- `missing`: T1 is unavailable, so D1's local check becomes unresolved while its register match remains supported. D2 is still unresolved and D3 still adverse; the population is still three production deployments.
- `contradictory`: a second D1 record creates an ambiguous register match. Do not choose R1 merely because it agrees with deployment evidence. T1 still supports D1's narrow local check; the inventory conflict does not erase independent source support for that finding.

Every case must reject the producer's blanket statement that the population is registered and locally validated. Generic vendor testing and an earlier local version are not substitutes for the exact current implementation and use. The checker also exercises evidence-age boundaries, future/invalid dates, missing observations alongside a known breach, duplicate cases/tests, incorrect configuration, unexpected cases and duplicate deployment identities. These remain authored fixture controls, not assessments by a decision model.

## P&L and scenario expectations

- `complete`: daily movement +USD5,000, explained components +USD8,000, residual −USD3,000; the portfolio reconciliation criterion is not met. P1/P2 residuals +USD6,400/−USD9,400 remain visible. Unmitigated rates and joint scenario losses breach the selected limit; spreads does not. Joint loses USD15,000 more than the sum of single-factor effects.
- `missing`: absent P2 carry leaves full explanation and residual unresolved despite a known-component subtotal of +USD7,600. Absent P2 in joint leaves the full joint, its interaction and its conditional hedge result unresolved. The observed P1 subset is not a full-book loss. A separate complete rates scenario still breaches, preventing an overall all-clear.
- `contradictory`: producer summaries disagree with the component sum, unmitigated scenarios and assumed-only hedge record. Neither a producer label nor a conditional hedge calculation overrides the selected unmitigated limit or supplies execution evidence.

The checker covers equality, duplicate rows/scenarios, wrong input types, incompatible base/currency/basis/horizon/revision/shock, unsupported cash-flow changes and extra records. Expected prose findings are authored; passing arithmetic controls does not establish that an agent preserves these distinctions.

## Outcome-comparison expectations

- `complete`: F1–F3 are mature and eligible for both models; F4 is immature. A's mean absolute error is USD100,000/3 and B's USD20,000/3. B has 80% lower error against A on this common three-item population; no broader performance or economic claim follows.
- `missing`: B3 is absent. A's descriptive three-item metric exceeds B's descriptive two-item metric, but that is not a matched comparison. On common F1/F2, A has zero mean error and B USD10,000. A relative comparison against zero is undefined. The full mature-cohort comparison remains unresolved.
- `late-forecast`: B3 exists but was issued after both its target window and observed outcome. Its correct value does not qualify it as predictive evidence. Eligibility and common-population metrics match missing, with a different recorded cause.

Every case must disclose unavailable training/selection history. Chronologically eligible predictions do not alone establish a pristine holdout. Controls cover exact timing boundaries, missing/duplicate observations, unmatched identities, invalid dates, wrong currency, nonnumeric values, empty metric populations and duplicate cohort identities. These authored cases do not establish model accuracy or evaluator reliability.

## Implementation review

These are authored interpretation cases for [implementation review](../../contracts/implementation-review.md), not outputs of agent execution or financial approval.

**Supported, bounded agreement.** A supplied packet identifies a pricing implementation, its annual-volatility and expiry conventions, numerical-reference method, ten required cases, observed prices and tolerances. All required comparisons are supported within their tolerances. A report identifies the tested scope, maps the conventions, accounts for each case and limits its conclusion to that evidence. This can fulfill the review without asserting universal correctness, adequate coverage for every use or deployment approval.

**A passing identity is insufficient.** A packet reports that a Black pricing adapter satisfies put–call parity, but off-one-year tests disagree with the required prices because annual volatility was passed where total standard deviation was required. Calling the implementation correct because parity passes is not supported. Report the convention mismatch and price failures separately from the passing identity. These expectations concern this stated packet; no observed defect in QuantLib is implied.

**Missing execution or coverage.** A packet contains test code for several expiries but observed results only for a one-year, at-the-money, zero-rate case. That result does not establish execution of the remaining tests. An accurate review can identify the gap; claiming the full implementation test scope passed cannot be supported by the code alone.

**Disputed observer result.** A numerical cross-check initially disagrees with an implementation's analytical integral. Retained refinement changes the numerical measurement while the subject source and inputs stay fixed, bringing the values into agreement. A report must account for that evidence before declaring a subject defect or proposing a repair. The refined check supports its observed scope, not a blanket conclusion that the observer or implementation is always correct.

**Shared convention error.** Two implementations agree after receiving inputs from the same adapter, but the adapter maps the documented quantities incorrectly. Their price agreement does not establish the required convention. Distinguish comparison independence from separate function or provider names, and identify the unsupported mapping.
