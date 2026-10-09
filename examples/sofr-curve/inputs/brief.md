# USD SOFR curve: interpolation decision

This is a bounded adaptation of the OpenProse model developer's brief identified in [the import provenance](../../../provenance/README.md). It is evidence of the developer's choice and reasons, not a new instruction to change the library requirements.

The model produces discount factors for USD cash flows in a single-curve SOFR setting. This example concerns one as-of date, 2026-09-18. It does not cover other currencies, multi-curve construction, production deployment or an institution's actual approval process.

Method A uses log-linear interpolation of discount factors, implemented with QuantLib. Method B uses the unameliorated Hagan–West monotone-convex method for forward rates, including its positivity collar, implemented in the included model source. Method B is not QuantLib's default smoothed ConvexMonotone variant.

The developer chose **method B**, retaining method A as a comparison. The supplied reason is the shape of projected forward rates; the comparison does not establish that B is preferable for every use. Both methods reprice the selected input instruments closely in this snapshot.

The main evidence for that reason is the smaller largest day-to-day forward move under B on the measured date grid. This is a finite-grid observation, not a proof of smoothness everywhere. A five-business-day comparison is also supplied. B has flat stretches and short ramps, and long-end behavior depends on sparse inputs and the method's end rule.

The material trade-off is **locality**: a one-basis-point perturbation to the 5Y quote changes forwards outside the 4Y–6Y window more under B than A. A's more local sensitivity may be preferable for instrument-by-instrument hedging. This test uses one selected quote perturbation; it is not a norm over every input.

If discussing the present-value difference between the methods, identify the USD100 million payment, the particular worst-difference date on the monthly grid, and its scope. The difference is neither a trading profit nor a gain caused by OpenProse. No baseline study of documentation quality, cost or speed is supplied.

Numerical evidence and locators are in [the evidence guide](evidence.md) and [results.json](results.json). Missing institutional information is listed [separately](institutional-facts.md). Do not add external paper claims from titles or references alone.
