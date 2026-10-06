# Exposure/default dependence and expected loss

Public reproduction plan, prespecified October 6, 2026. Test a finite synthetic expectation, not a calibrated CVA model, regulatory EAD, accounting allowance or financial action. All probabilities refer to one stipulated measure; no empirical or market-implied estimation is supplied.

## Fixed question

At T=1 year, potential positive exposure X takes values 10, 50 and 100 in USD millions, with probabilities 1/2, 3/10 and 1/5. Default by T is indicator I with probability 1/10. Under an explicitly simplified convention, loss is paid at T and equals (3/5)XI. Apply deterministic discount 20/21. There is no collateral, netting, closeout simulation, earlier default payment, own default or recovery timing model. Compare discounted joint loss with the product of the supplied marginal mean exposure, default probability, loss fraction and discount.

A joint allocation d_i=P(X=x_i,I=1) must satisfy 0<=d_i<=p_i and sum(d_i)=1/10. Nondefault cells are p_i-d_i. Retain these six fixed proposals, without clipping or renormalizing:

| ID | Default allocations for X=10,50,100 |
|---|---|
| independent | 1/20, 3/100, 1/50 |
| low-exposure-default | 1/10, 0, 0 |
| middle-exposure-default | 0, 1/10, 0 |
| high-exposure-default | 0, 0, 1/10 |
| dependent-zero-covariance | 3/50, 3/250, 7/250 |
| invalid-negative-cell | -1/100, 11/100, 0 |

The zero-covariance construction tests the converse: equality of the product and joint expectation need not imply independence. The invalid construction preserves marginal totals and produces a scalar inside the valid loss range, while containing a negative joint cell. Interpret its outputs as formal arithmetic, not expectations under a probability distribution.

## Native calculations and references

Use NumPy to compute all joint cells, marginal checks, mean exposure, default-weighted exposure, the ratio of default-weighted exposure to PD, conditional default probabilities by exposure, covariance, discounted loss and the product-of-marginals value. Independently derive references with exact Fraction arithmetic. Fixed absolute numerical allowance is 1e-10 in each stated unit. Retain the invalid table as an adverse observation, not a failed launch.

Run two SciPy linprog calls with method=highs, maxiter=100, time_limit=10 seconds each: minimize and maximize sum(x_i*d_i), with the fixed equality and bounds above. Preserve success/status/message, candidate, objective, iterations and available constraint/bound diagnostics. No alternate algorithm, adaptive starts or retry. If a solve fails, retain it; the exact bounds remain separate mathematical evidence.

The exact inequalities 10*PD <= sum(x_i*d_i) <= 100*PD hold for nonnegative d and are attained because both the lowest and highest exposure states have at least PD mass. Explicit feasible witnesses are [1/10,0,0] and [0,0,1/10]. This establishes sharp bounds for this stipulated finite marginal problem, independently of native termination. It does not establish plausible stress probabilities, forecast confidence intervals or a bound for a real portfolio.

## Execution and follow-up

Commit plan and source before one CPU process, at most 120 seconds, one attempt, one concurrent process, no retry, network/provider call or dependency installation. Use the existing numerical environment with one thread. Retain source/plan hashes, environment, full output, exit status and elapsed time. Numerical failures must remain visible rather than trigger changed tolerances.

Afterward verify retained arithmetic and adverse mutations without rerunning native optimization. A concise report should distinguish admissibility, factorization, dependence, bounds and supplied evidence. Existing credit-loss and dependence contracts already express those distinctions; a new reusable definition is not presumed. Any public composition is separately claimed.

## Primary context

[Basel Framework CRE50](https://www.bis.org/committees/bcbs/basel-framework/standard/cre/50/inforce/2019-12-15/published/2024-07-05), paragraphs 50.35–50.36, inspected October 6, identifies exposure/default association as relevant to wrong-way risk. This motivates the reporting question; it does not supply these toy inputs, formula, tolerances or institutional requirements. Positive association here is a synthetic dependence property, not proof of a transaction-specific regulatory classification.

## Optional reproduction

With Python 3.12.14, NumPy 2.5.3 and SciPy 1.18.1, run `python3 examples/exposure-default/model/measure.py /tmp/open-quant-exposure-default-fresh.json` from the source repository, with a fresh destination and external 120-second deadline. This is separate from the reporting program. Compare all numerical observations/controls, excluding only new timestamp/duration and explicitly rebound source/plan hashes. The reporting packet projects source proposals by their fixed order into neutral IDs J1–J6; source labels and observer classification flags are not reporting evidence. Reproduction does not qualify agent interpretation.
