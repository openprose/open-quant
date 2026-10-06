# Distinguishing cases for optimization review

These authored cases describe [optimization review](../../contracts/optimization-review.md). They are not model assessments or observed agent outputs.

| Supplied evidence | Required distinction |
|---|---|
| Candidate satisfies the selected constraints; a valid analytical reference supports the requested global objective tolerance. | Report the supported conclusion for that exact problem, input and candidate. This does not establish economic suitability or approval to implement it. |
| Solver reports success after a required return constraint was omitted. | Assess the original constraint separately. A lower objective cannot compensate for its violation. |
| Expected returns are expressed in percentages but compared with a fractional threshold. | Identify the unit mismatch and its effect on the implemented problem. Preserve original-unit findings. |
| A covariance matrix is valid but its rows/columns refer to a different variable order. | Matrix validity does not establish correct objective binding or optimality for the selected problem. |
| A positively rescaled objective triggers successful termination at a feasible candidate with an excessive original-unit objective gap. | Mathematical equivalence of minimizers does not establish equivalent numerical stopping accuracy. |
| Solver hits an iteration limit but its candidate satisfies all original constraints. | Report unsuccessful termination and observed feasibility separately. Optimality still requires its own evidence. |
| Full investment is required but nonnegative position caps sum to less than one. | The stated constraints establish infeasibility in this construction. A solver's failure status is not itself that certificate. |
| Actual exported weights were rounded and breach a required constraint; the unrounded solution passed. | Assess the revised artifact separately. Do not use the earlier candidate's success to clear it, or confuse an actual export with a rounded display. |
| A stationary point is supplied for a nonconvex problem without a global bound or other supporting argument. | Do not infer global optimality from stationarity or local solver success. |
| Constraint residuals or variable identities are missing while the producer labels a candidate optimal. | Preserve supported findings and identify the unavailable checks. The label does not supply the missing evidence. |

The [worked report](../../examples/optimization-review/README.md) supplies constructed numerical evidence, a public reproduction source and three reporting cases. It remains agent-unqualified. This component reviews supplied evidence; no solver invocation is implied by adopting it.
