# Flat-hazard credit-loss methodology — authored reference

Mode: `public-methodology`. This is a public synthetic-methodology example with institutional records absent. It is an authored reference, not an observed agent result or regulatory submission.

## Scope

`CREDIT-LOSS-2026-10-06` illustrates expected discounted loss under a stipulated default distribution. It selects the `interval_mass` construction and compares five alternatives. It does not estimate borrower probabilities, calibrate market-implied probabilities, calculate an accounting reserve or establish an approved production model.

The reference date is January 1, 2026. The curve uses Actual/365 Fixed, but the calculation queries exact year fractions 0, 1, 2, 3 and 5, not calendar anniversary dates. The supplied method assumes a single absorbing default event, no cure or competing event, deterministic exposure and loss fraction conditional on the default interval, and settlement at the interval end.

Sources: model brief; packet `subject` and `selected_method.scope`; calculation source `TIMES` and `measure()`.

## Method and inputs

The fixed hazard of 0.12 per year is an intensity, not a one-year default probability of 12%. Survival is `S(t)=exp(-0.12*t)`; cumulative default is `1-S(t)`. For `(a,b]`, unconditional default probability is `S(a)-S(b)`. Conditional on having survived to `a`, the interval probability is `[S(a)-S(b)]/S(a)`. The latter uses a different population and cannot replace the unconditional weight in the selected time-zero expectation.

The selected interval loss is unconditional probability × exposure × loss fraction × `exp(-0.03*b)`. Loss fraction is the fraction lost on default, not the fraction recovered. The total sums four disjoint intervals. With no point masses in this stipulated continuous distribution, endpoint equality has zero probability; the interval definitions remain explicit.

| Interval | Years | Exposure, USD | Loss fraction | Unconditional probability | Conditional probability | Selected discounted loss, USD |
|---|---|---:|---:|---:|---:|---:|
| I1 | (0,1] | 1000000 | 0.45 | 0.113079563283 | 0.113079563283 | 49381.900706 |
| I2 | (1,2] | 800000 | 0.45 | 0.100292575651 | 0.113079563283 | 34002.716663 |
| I3 | (2,3] | 600000 | 0.50 | 0.088951534996 | 0.113079563283 | 24388.674543 |
| I4 | (3,5] | 400000 | 0.50 | 0.148864689977 | 0.213372138933 | 25625.805214 |

The total is USD133399.097125. The four interval probabilities telescope to `1-S(5)=0.451188363906`; five-year survival is 0.548811636094. The conditional probability is the same across the three equal-length first intervals, although their unconditional probabilities decrease because fewer paths survive to each start. The two-year final interval has a different conditional probability.

Sources: packet `selected_method.intervals`, `observed_probabilities` and `observed_constructions[interval_mass]`; model brief. Displayed values are rounded; original precision supports the checks.

## Implementation and choices

The owned Python source constructs QuantLib `FlatHazardRate` with the supplied reference date, quote and day counter. It queries survival, cumulative default, hazard and interval default probability, derives conditional probability by dividing by start survival, and applies the stated exponential discount factor and deterministic loss inputs. It uses `math.fsum` to aggregate amounts. Decimal calculations at 50-digit precision provide separate exponential reference values for the stipulated formulas.

The current brief selects unconditional interval mass because it corresponds to this expected-loss definition. It does not supply an empirical reason for a 0.12 hazard, 0.03 discount rate, exposure profile, severity profile or interval-end settlement. These are example assumptions. Interval-end settlement differs from settlement at the actual default time; that alternative was not evaluated. A more detailed model or different probability basis requires new inputs and requirements, not relabeling these results.

Sources: calculation source `measure()` and its constants; current model brief; receipt source/environment identities. This is local source inspection, not a full upstream QuantLib audit.

## Comparison evidence

| Construction | Total expected loss, USD | Difference from selected, USD |
|---|---:|---:|
| interval_mass | 133399.097125 | 0.000000 |
| cumulative_as_interval | 282281.768182 | 148882.671057 |
| conditional_as_unconditional | 155454.158864 | 22055.061738 |
| hazard_times_interval | 167303.792201 | 33904.695075 |
| recovery_as_loss | 151929.012096 | 18529.914971 |
| undiscounted | 143449.529206 | 10050.432080 |

All six constructions have individual probability weights between zero and one, yet five change the selected meaning. Cumulative probabilities repeatedly count earlier defaults; their weight sum is 1.079963740051. Conditional probabilities use survivors as their denominator. Hazard times interval length is not the exact unconditional mass. The recovery substitution changes the 0.45 loss fractions to 0.55; the 0.50 intervals happen to remain unchanged. Omitting discounting changes the timing/value convention. These alternatives are comparison evidence, not equally acceptable implementations of the selected method. A smaller number alone would not establish a better model.

Sources: all six packet construction records, selected method and calculation branches. Totals are numerical expectations under specified assumptions, not observed cash losses, profits or documentation savings.

## Evidence and limitations

The receipt records one earlier successful calculation using Python 3.12.14 and QuantLib 1.43, and reproduction agreement under its stated scope. Source controls use probability tolerance 1e-12 and amount tolerance USD1e-7. The reference display has fewer digits; comparisons use underlying values. The source separately checks each construction's arithmetic, so matching a Decimal calculation does not establish conformity with the selected method.

No fresh numerical reproduction was performed for this document. Evidence covers fixed synthetic inputs, not empirical calibration, parameter uncertainty, economic suitability, stochastic exposure/default dependence or a continuous-time settlement model. The receipt does not establish documentation fulfillment, a complete citation audit or permitted agent behavior.

Sources: receipt, packet `selected_method.scope`, calculation controls and current brief.

## Institutional gaps

- [INSTITUTION-SUPPLIED: accountable model owner and organization, effective scope and date].
- [INSTITUTION-SUPPLIED: actual deployed revision, approved use and restrictions].
- [INSTITUTION-SUPPLIED: reviewer, reviewed revision, scope, dated decision and outstanding conditions].

The registered institutional-facts file supplies none of these records. Their absence here does not prove the activities never occurred. This document discloses the selected gaps; it does not supply the underlying facts, approve use or constitute a complete institution-specific document.
