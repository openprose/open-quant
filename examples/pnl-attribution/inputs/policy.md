# Selected attribution requirements

The total is closing value V(111) minus opening value V(000). Require each available native position value to agree with its independent reference within absolute USD 1e-6, including equality at the boundary. Preserve the 10,000-unit scale, factor endpoints, currency and valuation conventions. Use exact rational arithmetic on retained represented decimal values for bridge identities; this precision does not make the original theoretical price exact.

Review all six sequential orders of changing forward, volatility and maturity. Each step must name its changed factor, prior corner, next corner and value difference. Check reconciliation separately from support for every intermediate valuation. Different orders may assign different amounts while closing to the same total.

The selected explanatory allocation averages each factor's increments over all six orders with equal weight, using three distinct factors. Retain standalone effects V(100)−V(000), V(010)−V(000), V(001)−V(000), and their interaction residual against the total. These are finite full-revaluation effects, not derivatives or first-order approximations. Do not distribute the residual to make the standalone explanation close.

Check the equivalent interaction allocation where inputs permit: d(A) is the sum over B⊆A of (−1)^(|A|−|B|)V(B), with each d(A) divided equally among its member factors. Compare the producer's two-group calculation, which combines forward and volatility before averaging the two group orders, with the selected three-factor result. The two-group result is a comparison, not a substitute for the selected method. Neither symmetric averaging nor closure identifies economic causality or a uniquely appropriate institutional policy.

When a corner's native and reference values are null, retain its identity, parameters, reported producer status and all downstream quantities. Mark affected source comparisons unresolved. Do not treat zero, an inferred value from a reported contribution, or a recomputed formula as the missing native observation. Known endpoint totals, supported paths, standalone effects and internally reconciled reported arithmetic remain reportable. Assess input support at the relevant level rather than making the entire report either an all-clear or wholly unknown.

Producer assertions are claims to review, not requirements or independent evidence. Reporting fulfillment is separate from source completeness, favorable model findings and authority to make an accounting or trading decision.
