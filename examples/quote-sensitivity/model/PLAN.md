# Quote and parameter sensitivity: prespecified study

Use a synthetic two-node annual curve at January 1, 2026, with Actual/365 Fixed times exactly one and two years (365 and 730 calendar days). Annual par-coupon quotes are q1=0.03 and q2=0.04. Algebraic calibration gives D1=1/(1+q1), D2=(1-q2 D1)/(1+q2). The first instrument pays 1+q1 at year one; the second pays q2 at year one and 1+q2 at year two, per unit principal. These are synthetic conventions, not a supplied market or production swap curve.

Value two fixed cash-flow instruments of USD1,000,000 principal: coupon 4% (USD40,000 and USD1,040,000 at years one/two) and coupon 6% (USD60,000 and USD1,060,000). Cash flows stay fixed in every perturbation. The first is par at the base quotes; do not reset its coupon as quotes change.

Build thirteen QuantLib DiscountCurve instances: base, plus/minus h=0.0001 for quote q1, quote q2, both quotes, zero parameter z1, zero parameter z2 and both zeros. Quote changes recalculate both discount nodes algebraically. Zero changes use D(t)*exp(-t*shock) at the selected nodes, holding the other zero fixed; z(t)=-log(D(t))/t is continuously compounded. Calculate both fixed instruments with native CashFlows.npv for every curve. There are 26 native values; no numerical calibration solver is used.

Retain nodes, implied annual par quotes, native values, each positive-shock change and central derivative/change per basis point. Compute independent 50-digit decimal node/value references for each scenario and exact rational base calibration and Jacobians. Verify the chain rule linking zero-parameter and quote derivatives. The two-year par instrument must remain par for either q1-only bump with q2 fixed; its zero1-only response can differ. A correctly calculated parameter response is not a quote response.

Predeclared tolerances: discount nodes 1e-14 absolute; values USD1e-8 absolute; implied quote targets 1e-12; central finite derivatives against decimal finite references USD2e-5 per unit rate; central derivatives against infinitesimal analytic derivatives USD0.1 per unit rate. Preserve finite versus infinitesimal differences. Exact rational identities have zero symbolic tolerance. No threshold is an institutional policy.

Run one CPU process in the existing Python3.12/QuantLib1.43 environment, one attempt, outer timeout120seconds, one concurrent process, no network, dependency installation, retry or provider call. Commit this plan and measure.py before execution. Write observations before failing a numerical control; retain nonzero exits and partial logs. Do not alter source or tolerances to erase a failure.

This is established mathematics in a synthetic numerical reporting specimen. It tests risk-coordinate meaning and supplied-record controls, not agent fulfillment, real hedge effectiveness, financial suitability, comparative OpEx or novelty of the underlying mathematics. Existing sensitivity/calibration requirements appear sufficient; decide public-example scope only after inspecting evidence.

## Public reproduction

This public source reproduces the same fixed construction in one newly recorded process. Compare all numerical records and controls with the prior study before projecting reporting packets; fresh timing and source/plan identities are separate. The reporting program will not authorize calculation. In a separately authorized Python/QuantLib environment, select a fresh output file:

```sh
python3 examples/quote-sensitivity/model/measure.py --output /tmp/open-quant-quotes-YOUR-RUN.json
```

The retained environment is Python3.12.14 and QuantLib1.43. The command refuses an existing file. It constructs and values synthetic curves; it does not execute a financial transaction, assess a report or establish financial suitability. Dependencies are prerequisites, not installed by the script. [QuantLib's curve source](https://github.com/lballabio/QuantLib/blob/v1.43/ql/termstructures/yield/discountcurve.hpp) documents the native discount-curve representation; this study evaluates only node-dated payments.
