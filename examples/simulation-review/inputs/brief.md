# Synthetic European-call simulation

The reporting subject is BLACK-SIMULATION-2026-10-06, replicate 0 at 4,096 and 16,384 underlying draws, using the exact source and dependencies identified in the receipt. Review date is October 6, 2026. Intended reader: an AI-literate financial operations colleague. No production use, institutional acceptance or approval record is supplied; these are the selected institutional facts to report as unresolved.

The requested quantity is discounted expected European-call payoff under a lognormal terminal forward. Forward and strike are each 100 USD per underlying unit; annual volatility is 0.3, expiry is 2 years and the continuously compounded annual rate is 0.05. The discount factor is exp(-0.05*2). Terminal forward is 100*exp(-0.5*0.3^2*2 + 0.3*sqrt(2)*Z), with Z standard normal. Output is present-value USD per underlying unit. The closed-form reference is about 15.2009041; the expectation without discounting is about 16.7995971. The packet retains full precision.

The study generated 64 sequential PCG64DXSM streams with SeedSequence(2026100601).spawn(64). This report uses replicate 0 by index, not because of its outcomes. The two sizes are nested prefixes of the same stream. The design assumes independent normal draws within a stream; source identity and stream construction support reproducibility, not mathematical proof of independence. There is no adaptation, seed selection or stopping based on observed precision.

| View | Construction and uncertainty |
|---|---|
| independent_units | Discounted payoffs; mean and sample variance across N draws. Standard error is s/sqrt(N), with variance denominator N-1. |
| duplicated_naive | Each discounted payoff appears twice. The mean is preserved, but uncertainty incorrectly treats 2N rows as independent. |
| duplicated_grouped | The same duplicated records are averaged within each known pair. Uncertainty uses N group means, recovering the original sampling units. |
| omitted_discount | Payoffs omit discounting. Its sampling calculation describes the different, undiscounted expectation. |

Every view reports a nominal 95% interval using a t quantile and its declared uncertainty denominator. For this nonnormal payoff mean, the usual interval is an approximation; no exact finite-sample coverage is asserted. A realized interval need not contain a reference on every run. The four views share draws, and grouped duplicates are not independent corroboration of the original estimate.

This is exact terminal sampling, so the example introduces no time-discretization error. Reported sampling intervals exclude parameter uncertainty, data error and model misspecification. A tighter interval alone does not establish the correct target or financial suitability. The duplicate and discount errors are deliberate constructions, not defects found in a vendor system.

Background: [NIST on confidence limits for the mean](https://itl.nist.gov/div898/handbook/eda/section3/eda352.htm) and [NumPy on random streams](https://numpy.org/doc/stable/reference/random/parallel.html). These citations explain the supplied method; they do not authorize external retrieval for this report.
