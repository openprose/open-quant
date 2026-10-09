# Dependence-input review — authored reference

**Subject:** DEPENDENCE-2026-10-06, complete case, reviewed October 6, 2026. This is an authored content reference, not an executor result. The inputs are synthetic Pearson correlations with unit marginal scales for variance aggregation; no production use or financial horizon is established. [Brief](../inputs/brief.md), “Synthetic dependence-input review.”

None of the original inconsistent input and its two adjustments meets all replacement requirements. The original fails joint validity and the eigenvalue floor. Clipping and rescaling restores validity but fails the floor and changes the locked AB entry. Shrinkage meets the floor but also changes AB. The combined finding is breached for all three. This does not mean every possible replacement would fail. [Policy](../inputs/policy.md), “For inconsistent and its two adjustment candidates”; [packet](../inputs/complete.json), matrices and adjustments.

## Matrix findings

All nine supplied matrices have unit diagonal, bounded entries and symmetry within the 1e-12 tolerance. Joint findings use the supplied spectra; small signed residuals remain visible. [Packet](../inputs/complete.json), matrices, each named record's matrix/eigenvalues/diagnostic fields.

| Matrix | Minimum eigenvalue | Correlation admissibility |
|---|---:|---|
| identity | 1 | met |
| singular | -3.33066907e-16 | met within tolerance |
| inconsistent | -0.8 | breached |
| pairwise_complete | -0.960784314 | breached |
| common_complete | 1 | met |
| clipped_rescaled | -1.05101113e-16 | met within tolerance |
| shrunk_half | 0.1 | met |
| alignment_original | 0.332212909 | met |
| alignment_permuted | 0.332212909 | met |

Every two-variable block of inconsistent has eigenvalues 0.1 and 1.9, yet its joint minimum is -0.8. The unit witness (-1,1,1)/sqrt(3) gives quadratic form -0.8, which cannot be a variance. Passing the pair checks does not establish joint validity. Singular has spectrum approximately 0,0,3; its failed Cholesky does not invalidate correlation for the permitted variance use. An inverse would require a different finding. [Packet](../inputs/complete.json), matrices.inconsistent.pair_blocks, negative_variance_witness, matrices.singular; [policy](../inputs/policy.md), “A singular matrix is permitted.”

## Observation populations

The ten raw rows have distinct IDs O01–O10. No dates or publication timestamps are supplied, so market alignment and freshness are not established. The common population O01–O04 has four observations and yields identity. Each pair uses those four plus different pair-only observations:

| Pair | Correlation | Count | Observation IDs |
|---|---:|---:|---|
| A,B | 0.980392157 | 6 | O01–O06 |
| A,C | 0.980392157 | 6 | O01–O04, O07, O08 |
| B,C | -0.980392157 | 6 | O01–O04, O09, O10 |

The memberships match the available values in the raw rows; missing entries are excluded for each pair. Equal counts conceal different samples. The resulting pairwise matrix is indefinite, while the common-sample matrix is valid. That does not establish which estimator represents any economic population. No missing value was filled or input repaired. [Packet](../inputs/complete.json), missing_data and matrices.common_complete/pairwise_complete.

## Adjustments and exposure binding

Clipping/rescaling changes the original signed correlations ±0.9 to ±0.5: maximum absolute entry change 0.4, Frobenius change 0.979795897. Its witness quadratic form is approximately zero. Shrinkage changes them to ±0.45: maximum change 0.45, Frobenius change 1.102270384; witness value 0.1. Both replace AB=0.9. Neither passing PSD nor the smaller adjustment establishes optimality or approval. [Packet](../inputs/complete.json), adjustments; [brief](../inputs/brief.md), adjustment constructions.

The original matrix order A,B,C binds exposures (1,2,-1), giving variance 8.4 squared synthetic units. Reordering to C,A,B requires exposures (-1,1,2), preserving 8.4. Retaining the old positions instead gives 4.6. Both matrices remain valid; the difference is the exposure binding. [Packet](../inputs/complete.json), alignment and matrices.alignment_original/alignment_permuted.

## Scope and remaining work

This reference accounts for all nine candidates, three pair populations and both adjustments using supplied observations and arithmetic checks. It does not rerun eigendecompositions or certify statistical representativeness, predictive performance, tail behavior or financial suitability. No institutional approval record is supplied; approval remains unestablished. The complete case supplies no producer claims to reconcile. [Packet](../inputs/complete.json), producer_claims; [brief](../inputs/brief.md), scope; [receipt](../receipt.json), calculation identity.

The content illustrates the required report. It does not claim runtime fulfillment: an actual executor must also produce the required result record, hashes and execution account. The supplied records support adverse findings, not authority to implement an adjustment.
