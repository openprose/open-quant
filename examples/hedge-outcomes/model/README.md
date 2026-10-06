# Hedge fit and subsequent outcomes

Status: public reproduction plan, October 6, 2026. No agent or provider invocation. This investigates reporting distinctions using existing Open Quant optimization, outcomes and numerical-evidence requirements; it does not propose a new financial method.

## Fixed question and data

Can a successful historical hedge fit establish acceptable position size, later-period improvement or equivalence after changing lot units?

Let `x = [-2,-1,1,2]` be hypothetical hedge P&L in thousands of USD per standard lot and `e = [1,-2,2,-1]`. Training position P&L is `y = 2x + e`; later position P&L is `y = -x + e`. Each period has four distinct dated observations. The hedge position contributes `-h*x`, so the total is `y-h*x`, with `h` measured in standard lots. No actual trades, fees, funding, slippage, margin or institutional facts are modeled.

Training ends September 24, 2026 at 20:00 UTC; its candidate selection is dated 21:00 UTC. Later observations are September 25, 28, 29 and 30 at 20:00 UTC; their refit is dated September 30 at 21:00 UTC. These timestamps are authored fixtures, not historical execution evidence. The later refit uses the evaluation outcomes and is ineligible as an advance prediction.

Minimize the sum of squared residual P&L, with no intercept. Also solve the same training problem under `-1 <= h <= 1`. Report squared-error sums, mean residual and population variance with denominator four. All selected vectors are centered, so variance reduction and squared-error reduction coincide in this construction; that equality is not general. Reference reduction is `1 - hedged SSE / unhedged SSE` on the same four observations. A negative reduction means a larger squared-error sum, not an observed cash loss of that amount.

Compare six candidates: unhedged; unconstrained training fit; constrained training fit; later-period refit; training fit with hedge P&L expressed per 100-lot basket and correctly converted position; and the deliberately incorrect use of the standard-lot coefficient as a number of those baskets. For the basket representation, `x' = 100x`, `h' = h/100` and the original position bound is `|h'| <= 0.01`. Preserve actual and equivalent standard-lot positions. A numerical coefficient without its unit is insufficient.

## Calculation and independent checks

Run NumPy `lstsq` for unconstrained training, later-period and basket fits, and SciPy `lsq_linear` for the original and basket constrained problems (`method=trf`, `lsq_solver=exact`, `tol=1e-14`, `max_iter=100`). Retain returned coefficients, residual arrays, rank and singular values, or native status, cost, optimality and iterations as applicable. NumPy's return does not include a Boolean success field; do not invent one.

Independently derive exact rational quadratic coefficients and evaluate all candidate residuals. Training SSE is `10h^2-40h+50`, later SSE is `10h^2+20h+20`. Their unconstrained minima occur at 2 and -1; the original bounded training minimum is 1. The exact training minima are 10 unconstrained and 20 bounded. Check native values against these independently specified values, using absolute tolerance 1e-8 for sums and 1e-10 for coefficients. Preserve observations even if a check fails.

Retain full populations and units, baseline denominators, coefficient timing, fitted and subsequent performance, exact references, native diagnostics, source/plan hashes and environment. Check correlation invariance under positive lot scaling without treating correlation as proof of equivalent positions. No inference about real-world hedge efficacy, statistical significance, cost reduction or regulatory treatment follows from these eight constructed observations.

## Execution bound

Commit this plan and source before running one fresh-output CPU process, at most 120 seconds, one attempt, no automatic retry, network, dependency installation or provider request. Use the existing numerical environment. A failure is evidence to inspect, not permission for an unrecorded retry. Later verification may inspect retained output without rerunning either native solver.

## Source

[NumPy's least-squares interface](https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html), inspected October 6, 2026, describes the minimizing vector and returned residual, rank and singular-value fields. The financial interpretation and synthetic data above are authored, not claims from that documentation.

## Reproduce separately from reporting

The reporting program reads prepared evidence and does not authorize this calculation. In a separately authorized environment with Python, NumPy and SciPy installed, choose a fresh directory outside the source checkout:

```sh
python3 examples/hedge-outcomes/model/measure.py /tmp/open-quant-hedge-YOUR-RUN
```

The retained numerical environment uses Python 3.12.14, NumPy 2.5.3 and SciPy 1.18.1. The command refuses an existing destination or a destination inside the checkout. It writes observations and controls; it does not evaluate a report, execute a trade or establish financial suitability. No agent execution of the reporting program is implied by a normal numerical exit.
