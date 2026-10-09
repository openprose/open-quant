# Illustrative dependence review policy

This is authored example policy, not a regulatory or institutional standard. Expected matrix identities are identity, singular, inconsistent, pairwise_complete, common_complete, clipped_rescaled, shrunk_half, alignment_original and alignment_permuted, from the calculation identified in the receipt. Preserve omissions, duplicates, incompatible identities and extra records.

For all nine candidates, report symmetry, unit diagonal, entry bounds and joint positive semidefiniteness using supplied diagnostics. Computational comparisons use absolute tolerance 1e-12; retain observed signed eigenvalue residuals. A singular matrix is permitted for this variance use. Cholesky success is not a universal acceptance condition and is not a substitute for other evidence. Report missing diagnostics as unavailable without concealing any independently supported violation.

For inconsistent and its two adjustment candidates, assess three criteria separately: correlation admissibility, minimum eigenvalue at least 0.05 (with the stated numerical tolerance), and unchanged AB=0.9. All three are required for a candidate to meet the selected replacement policy. Preserve original/adjusted identities and quantify changes; report the fixed-witness quadratic form for each. No authorization to implement an adjustment follows from this review.

For each pairwise estimate, identify the variable pair, correlation, count and available observation IDs. Reconcile supplied memberships to raw observations when available. Compare the common-complete population with the pairwise populations. Equal counts do not establish equal membership; missing IDs do not establish different membership. The missing-membership packet omits raw rows and membership lists while retaining counts and numerical diagnostics. Do not infer that the omitted records never existed or import them from another source.

For the exposure comparison, preserve matrix order and named exposure values. Explain both the correctly bound and positionally misbound quadratic forms. A favorable producer summary must be checked against the records it summarizes.

Apply conjunction explicitly where requirements are combined: a supported violation yields breached; otherwise a missing fact needed to decide yields unresolved; only sufficient support for all selected requirements yields met. Keep missing evidence visible even when another violation is decisive. Findings about candidates and data are separate from fulfillment of the reporting contract, empirical suitability and institutional approval.
