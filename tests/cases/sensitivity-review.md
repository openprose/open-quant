# Distinguishing cases for sensitivity precision

These are authored interpretation cases for [the sensitivity/implementation composition](../../examples/sensitivity-review/README.md), not agent results.

- **Complete:** QuantLib prices and analytic derivatives agree with the supplied references, and all cent-rounding errors are within half a cent plus allowance. These implementation checks do not clear the finite-difference criteria. Preserve all 36 views and delta/gamma findings separately.
- **Quantization:** short-ATM at h=USD0.01 has rounded gamma −100 against analytic approximately +0.381. Zero rounded derivatives at smaller steps reflect unchanged represented prices, not proof of zero risk.
- **Step size:** the smallest unrounded step is worse than intermediate steps for gamma in all three cases. Large steps are also inaccurate near expiry. Do not infer a universal optimum or present a selected passing row as qualification of the whole grid.
- **Missing-unrounded:** analytic derivative references and rounded prices/views remain available. Unrounded views, observed price-rounding errors and actual rounded-minus-unrounded differences remain unresolved. The quantization envelope is conditional on a per-price assumption; a bound is not the missing observation.
- **Contradictory:** all four producer claims conflict with the evidence or units. Price tolerance does not guarantee derivative tolerance, minimum bump does not guarantee accuracy, zero rounded changes do not prove zero risk, and a derivative is not a finite dollar change for any shock.

The examples concern derivatives with respect to forward while discount, volatility, maturity and strike are held fixed. They do not establish spot sensitivities, recalibrated risk, stochastic convergence, a hedge or institutional acceptance.
