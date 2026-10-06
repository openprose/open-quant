# Reverse-stress severity, feasibility and search evidence

Prespecified October 6, 2026. Public reproduction plan. Commit this plan and source before one CPU process: at most 120 seconds, one concurrent process, no retry, network, provider request or dependency installation. Use the existing Python 3.12.14 / SciPy 1.18.1 / NumPy 2.5.3 environment. Retain every native result and failed outcome. The eight solver invocations below are distinct prespecified observations within that single process, not adaptive retries.

## Selected question

For a synthetic fixed portfolio, let instantaneous incremental loss be L(x,y)=x²+4y²−2x in USD millions. The base has x=y=0 and loss zero. x is a rate change divided by 25 basis points; y is an equity-return change divided by 5 percentage points. These are chosen normalization scales, not estimated standard deviations. There is no distribution, data calibration, actual portfolio, management action or empirical likelihood claim. The quadratic is defined on all real x,y for this mathematical study; that does not establish validity of a real pricing approximation over arbitrary shocks.

Find a scenario with L>=3 that minimizes selected squared severity S=x²+y². Reaching the loss threshold, minimizing a stated severity and maximizing loss over a domain are different questions. Use loss-feasibility tolerance 1e-8 USD million and objective-gap tolerance 1e-8 in the dimensionless selected squared severity. These are illustrative numerical tolerances, not institution or regulatory policy.

## Independent global references

For metric F=a*x²+b*y² with a,b>0, use an elementary nonnegative-polynomial certificate, not another optimizer. If b<2a, set c=a−b/4, x0=−b/(4a−b), m=b*(3a−b)/(4a−b), lambda=b/4. Then F−lambda*(L−3)−m=c*(x−x0)². Its two minimizers have x=x0 and y=±sqrt((3−x0²+2x0)/4). If b>=2a, m=a and lambda=a/2; F−lambda*(L−3)−m=(a/2)*(x+1)²+(b−2a)*y², attained at (−1,0). Check coefficient identities in exact rational arithmetic and candidate attainment numerically. A feasible point therefore has F>=m within this stipulated problem; a successful solver result is not the source of that bound.

For selected a=b=1, m=2/3 and the two minimizers are (−1/3,±sqrt(5)/3). Axis boundary points (−1,0) and (3,0) have squared severities 1 and 9. Whether symmetric solver starts terminate at these non-global stationary points is an observation, not a required outcome. Retain analytic-gradient stationarity and tangent-curvature diagnostics without equating native QP multipliers with a global certificate.

## Eight fixed SLSQP invocations

All use analytic objective and loss-constraint gradients, constraint L−3>=0, no variable bounds, ftol=1e-12, maxiter=200 except the last selected-metric limited run. Preserve x, objective, success, status, message, iterations, evaluation counts, gradient and available QP multipliers.

| ID | Metric a,b | Start | maxiter |
|---|---|---|---|
| selected-negative-axis | 1,1 | −2,0 | 200 |
| selected-positive-axis | 1,1 | 4,0 | 200 |
| selected-upper | 1,1 | −0.2,0.8 | 200 |
| selected-lower | 1,1 | −0.2,−0.8 | 200 |
| selected-origin | 1,1 | 0,0 | 200 |
| selected-iteration-limit | 1,1 | 4,0.2 | 1 |
| raw-mixed-units | 1,1/25 | −0.2,0.8 | 200 |
| raw-common-basis-points | 1,400 | −2,0.1 | 200 |

The last two metrics deliberately differ from the selected requirement. Summing squared numerical rate-bp and equity-percentage-point changes and dividing by 625 yields x²+y²/25. Merely expressing equity changes in basis points before applying the same numerical recipe yields x²+400y². The common positive divisor affects neither minimizer. Neither recipe supplies the selected normalization; reporting both factors in basis points does not establish equal economic scale. In contrast, explicit normalization by 25 rate bp and 5 equity percentage points, or equivalently 500 equity bp, preserves selected S for the same physical shock.

For every observed candidate, retain loss and severity under all three metrics, selected feasibility and objective gap, physical units in both representations, and independent implemented-metric reference. Do not claim that selecting the best of these finite starts establishes global optimality; the polynomial reference establishes the bound only for this toy.

## Finite-catalog boundary

Retain four authored scenarios (−1,0), (3,0), (0,1), (0,−1), and a separately identified witness (0,2). They are direct evaluations, not solver attempts. Minimum catalog severity is not the global minimum. Maximum catalog loss is not the maximum over the specified all-real domain: L(0,y)=4y² is unbounded. A nearest scenario is not a probability estimate or necessarily a worst-loss scenario.

## Controls and report

Check exact certificate coefficient identities, reference threshold attainment, native objective/gradient consistency, independent loss expansion, severity-unit invariance and all retained input identities. Do not make solver success or convergence to the expected stationary point an integrity requirement. Unexpected outcomes remain results; no settings change or retry follows. Later fixed-record verification must use no solver, and a report must preserve failures and distinguish observed candidate support from analytical reference knowledge.

Existing scenario review and optimization review already require supplied scope, units, objective identity and honest global claims. This study tests a new composition use, not a presumed kernel or standard-library change. It is not a new optimization theory, regulatory implementation, calibrated stress model, agent benchmark or savings estimate.

Primary references inspected October 6: [SciPy SLSQP](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-slsqp.html) defines stopping options and identifies returned multipliers as belonging to a QP approximation. [BCBS Stress testing principles](https://www.bis.org/publications/201810-guidelines-stress-testing-principles) places objectives, methodology and documentation within stress-testing frameworks. Neither source supplies this toy loss function, distance metric or its acceptance policy; the certificates above are derived for this study.

## Optional reproduction

This numerical calculation is separate from the reporting program. With the exact environment specified above, run `python3 examples/reverse-stress/model/measure.py /tmp/open-quant-reverse-stress-fresh.json` from the source repository, using an unused destination and an external 120-second deadline. Do not execute it as part of the reporting-only invocation. Compare every observation/control with the retained study, excluding only new timestamp/duration and the explicitly rebound calculation-source/plan identities. Reproduction does not qualify agent interpretation of the contracts.
