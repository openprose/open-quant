# Authored reference: complete optimization review

This is an authored reference for the complete packet, not an agent result. The scope includes seven native solver outcomes and one actual rounded export. The supplied expected returns and covariance are synthetic assumptions, without forecast-validation evidence. No allocation or institutional approval is recommended.

The original problem requires nonnegative A/B weights summing to one, caps 0.7/0.8 and expected return at least 0.04 in annualized fractions. With full investment, the positive-definite covariance gives a strictly convex one-variable quadratic over [1/3,0.7]. The analytical global minimum is A=1/3, B=2/3, variance 0.009777777778. Its scope is this exact problem and variable binding. The feasibility tolerance is 1e-10 in the declared fractions; objective tolerance is 1e-8 in variance units, conditional on feasibility. [Evidence: complete.json, scope/reference; policy.md.]

| Candidate | Native termination | Actual weights A, B | Original feasibility | Original variance | Original optimum tolerance |
|---|---|---|---|---|---|
| selected | success | 0.333333, 0.666667 | met | 0.009777777778 | met |
| omitted_return_constraint | success | 0.200000, 0.800000 | breached | 0.008640000000 | not met |
| percent_fraction_mismatch | success | 0.200000, 0.800000 | breached | 0.008640000000 | not met |
| covariance_order_mismatch | success | 0.700000, 0.300000 | met | 0.021340000000 | not met |
| scaled_objective | success | 0.500000, 0.500000 | met | 0.013500000000 | not met |
| infeasible_caps | failure | 0.400000, 0.400000 | breached | 0.008639999997 | not met |
| iteration_limit | failure | 0.485000, 0.515000 | met | 0.013060350000 | not met |
| rounded_export | not a solver run | 0.333000, 0.667000 | breached | 0.009772894000 | not met |

The table displays weights to six decimals; checks use the packet's unrounded values. Each row's evidence is complete.json/records[id]/solver and selected_problem_diagnostics, except the export at derived_candidates[id]. The selected solution meets every original constraint and the objective criterion.

**Problem identity.** The omitted-return and percent/fraction variants satisfy their implemented problems but yield original expected return 0.032, below 0.04. Their lower variance cannot improve the constrained original solution because they are infeasible. The covariance-order variant keeps a positive-definite matrix but assigns its entries to the wrong original variables. Its candidate is originally feasible; original variance 0.02134 exceeds the selected minimum by 0.011562222222. Native success does not repair that binding. [Evidence: the three implemented_problem records and their analytical references.]

**Numerical accuracy.** Scaling the objective and gradient by 1e-8 preserves the mathematical minimizer. With unchanged absolute stopping tolerance, this observed run returns its starting candidate [0.5,0.5] after one iteration and reports success. Original variance 0.0135 exceeds the minimum by 0.003722222222, failing the selected accuracy criterion. A small scaled objective does not answer the original-unit question. The record supports this constructed observation, not a general failure rate or a proposed replacement tolerance. [Evidence: scaled_objective solver/options and diagnostics.]

**Unsuccessful runs.** The changed caps [0.4,0.4] cannot permit weights summing to one: their sum is only 0.8. This establishes infeasibility of that revised system independently of the solver's failure. Its returned candidate also breaches original full investment; all other original constraints fall within the stated tolerance. The one-iteration native failure instead returns [0.485,0.515], which is originally feasible but exceeds the minimum variance by 0.003282572222. Failure therefore does not establish candidate infeasibility. [Evidence: infeasible_caps and iteration_limit records.]

**Export identity.** The actual rounded export [0.333,0.667] retains full investment and both caps, but expected return is 0.03998: a shortfall of 0.00002, or 0.2 basis points in annualized expected return. The unrounded solution's assessment does not clear this different artifact. A display rounded for this report is a separate matter. [Evidence: rounded_export weights and diagnostics.]

All eight required candidates and their original constraints are accounted for. Four candidates are originally feasible; only the selected solution also meets the requested objective tolerance. Four candidates breach original constraints, including the actual export and revised-cap result. No producer claims are supplied in this complete case. No solver was rerun for this reference, and the receipt attributes source/environment identity to the observed developer calculation. Financial suitability, implementation authority and agent reporting fulfillment remain unestablished.
