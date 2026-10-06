# Illustrative simulation review policy

This is authored caller policy for the example, not a regulatory or institutional standard. Apply it to the exact study/source and replicate 0 identified in the brief and receipt. Expected records cover both 4,096 and 16,384 underlying draws and all four named views. Preserve missing, duplicate and unexpected identities; source code is not a substitute for a missing observed result.

Review three criteria separately for each view:

1. **Target:** the estimator must target the discounted payoff specified in the brief. A narrow interval around a different expectation does not meet this requirement.
2. **Uncertainty method:** the reported uncertainty must respect the documented sampling units and dependence. Duplication does not add independent information. The method must state its approximation and excluded sources of error; no exact interval-coverage claim is required.
3. **Precision:** at 16,384 underlying draws, estimated standard error for the requested quantity must be at most 0.30 present-value USD per unit, using a supported uncertainty method. The 4,096-draw result is a comparison point, not a separate required precision gate. A numeric value below the threshold cannot clear an incompatible method or a different target.

Apply the conjunction explicitly: a supported violation yields a breached finding; otherwise unavailable evidence required to decide yields unresolved; only support for all selected requirements yields met. Preserve individual gaps even when another violation is decisive. An invalid reported uncertainty method does not imply that the true error is large; it means that report does not support the claimed precision under this policy. A different supplied view can be assessed separately, but must not silently replace the one under review.

The missing-large-sample case withholds its 16,384-draw records. Do not infer that they were never generated or extrapolate an observed result from 4,096 draws. The contradictory case adds an authored producer claim to unchanged observations. These changes concern the supplied reporting evidence, not a new simulation. Distinguish fulfillment of the reporting obligation from the underlying findings, and do not infer approval.
