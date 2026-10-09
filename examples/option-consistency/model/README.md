# Reproduce option quote and strategy evidence

Prespecified October 6, 2026, under IMP-087. One CPU process, at most 120 seconds, no retry, network, provider call or financial action. Use Python 3.12.14 and QuantLib 1.43. Each implied-standard-deviation solve has accuracy 1e-12, initial guess 0.20 and at most 100 iterations. Preserve native errors rather than replacing an unsuccessful solve.

## Two fixed one-expiry slices

All options are European calls on the same nonnegative terminal underlying, forward 100, discount factor 1, displacement zero, time to maturity one year, unit notional and prices in USD per option. Strikes are 80, 90, 105, 110 and 130. This is a synthetic snapshot, not actual market data or a multi-expiry volatility surface.

The `constant_volatility` slice uses QuantLib Black prices at standard deviation 0.20. The `authored_quotes` slice has exact call prices 21, 14, 9, 8 and 3 at those strikes. For each quote, retain native implied standard deviation and repriced call/put values. Compare the inversion with an independent 100-step bisection on [0,4] using the elementary Black formula and math.erfc. Compare standard deviations to absolute 1e-9 and price/parity residuals to absolute USD 1e-8. Record all failures. Because maturity is one year, the implied annual volatility and standard deviation have equal numerical values here; their concepts remain distinct.

Keep each call's intrinsic/forward bounds, adjacent-strike slopes and call-put parity visible. Puts are constructed by parity and then compared with native puts at the fitted standard deviation. Neither those identities nor a successful per-quote inversion establish that all quotes admit one common pricing distribution.

## Payoff and cost scope

Use all three adjacent strike triplets in both slices. For K_L<K_M<K_R, the selected butterfly holds w_L=(K_R−K_M)/(K_R−K_L) lower-strike calls, minus one middle-strike call, plus w_R=(K_M−K_L)/(K_R−K_L) upper-strike calls. Also retain the deliberately naive equal-wing construction w_L=w_R=1/2 on each triplet. Unequal strike spacing can give that construction a negative terminal payoff even when its purchase cost is negative.

Calculate exact rational terminal payoffs at S=0, all five strikes and S=230. A call spread portfolio is piecewise linear with knots only at its strikes. Both weight constructions have zero total call coefficient, so their final slope is zero; the last payoff is constant beyond the largest strike. Thus checking all knots, S=0 and the tail slope establishes the minimum on the entire nonnegative underlying domain for these specific portfolios, not merely a sampled grid. Retain weights, nodes, payoffs, tail slope and minimum separately from their initial cost.

For every strategy retain purchase costs at common quote half-spreads h=0,1/20,1/5: long wings are bought at mid+h and the short middle is sold at mid−h. Quantities can be fractional, all legs have the same underlying, maturity and settlement, and the constructed quotes are assumed simultaneously available for those quantities. No other fee, funding, margin, credit, tax or trading restriction is modeled. The constant discount of one avoids reinvestment adjustments.

A negative cost with nonnegative payoff everywhere gives a witness only under those assumptions. A negative cost from a portfolio with negative possible payoff does not. A nonnegative cost at a wider spread removes that specific witness; it does not establish global absence of arbitrage. For exact authored prices, use Fraction costs. For generated prices, use their retained decimal strings as the exact inputs to the subsequent cost accounting; the resulting witness is conditional on those represented quotes. Keep this distinction explicit.

There are ten implied-standard-deviation solves, twelve strategies and 36 cost views. Retain every quote, slope, root, repricing, payoff and cost. Do not retune the authored quotes, select successful strikes, repair the slice or claim an economic implementation from these finite calculations.

## Intended evidence

Retain source/plan/input identities, environment and native-library identity, command, timing, controls and all observations. Subsequent verifiers read records and perform arithmetic without new QuantLib solves. Adverse controls should distinguish altered quote identity, wrong strike weights, changed spread side, missing records, parity mismatch, false payoff positivity and unsupported global conclusions.

The inspected [QuantLib v1.43 Black interface](https://github.com/lballabio/QuantLib/blob/v1.43/ql/pricingengines/blackformula.hpp) specifies standard deviation and the inversion arguments. Strike-aware convexity is derived from the stated portfolio's exact piecewise payoff here; no external theorem or third-party market dataset is copied. Existing calibration, implementation and numerical-evidence contracts may support a worked reporting composition without a new definition. No agent qualification, novel pricing theory or investment recommendation is claimed.

## Optional reproduction

This calculation is separate from the reporting program. Python 3.12.14 and QuantLib 1.43 produced the retained observation. In an environment with those dependencies, run `python3 examples/option-consistency/model/measure.py --output /tmp/open-quant-options-fresh.json` from the repository root, choosing an unused destination. Apply an external 120-second process deadline; the source also limits every native inversion to 100 iterations. No market lookup or provider call is used.

The public source and this plan are committed before the one authorized reproduction. Timing and source/plan hashes will differ from the preceding study; all other fields must match before describing it as reproduced. A completed calculation does not qualify the reporting agent or establish institutional approval.
