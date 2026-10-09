# Selection-history review — authored reference

**Subject:** SELECTION-2026-10-06, replicate 0, complete case, October 6, 2026. This is an authored content reference, not an executor result. All 64 candidates have zero true effect in the synthetic model; the scores are not observed investment returns. No economic performance or institutional approval is established. [Brief](../inputs/brief.md), “Synthetic selection-history review.”

M34 is the selection winner. Its score exceeds the ordinary one-candidate threshold but does not exceed the applicable threshold for a maximum among 64 candidates. Independently evaluating M34 yields a lower score that does not exceed the ordinary threshold. M24 wins when the evaluation sample is searched again; that is another selection, not confirmation of M34. [Packet](../inputs/complete.json), observation.views and score vectors.

| View | Candidate | Score | Raw one-candidate tail | Applicable tail | Required exceedance |
|---|---|---:|---:|---:|---|
| selection_winner | M34 | 2.161527485 | 0.015327308 | 0.627881554 | not met |
| frozen_evaluation | M34 | -0.266037669 | 0.604894901 | 0.604894901 | not met |
| reselected_evaluation | M24 | 2.510286421 | 0.006031664 | 0.321041560 | not met |

The ordinary threshold is 1.644853627; the independent-family threshold is 3.155492604. The policy applies the latter to the two selected maxima and the former to the frozen candidate's independent evaluation. Equality does not count as an exceedance. None of the three observed comparisons meets its applicable exceedance condition. These labels do not mean the report failed or prove any result about a real strategy. [Policy](../inputs/policy.md), “For selected maxima”; [packet](../inputs/complete.json), theory and observation.views.

## Candidate and data lineage

The packet supplies 64 selection and 64 evaluation scores in M01–M64 order, with separate vector hashes and spawn keys [0,0] and [0,1]. The maximum selection score is at index 33, M34. Its evaluation score uses the same index. The maximum evaluation score is at index 23, M24. Candidate identity changes because evaluation data are used to select again; the dataset's name does not make that operation independent confirmation. The declared construction assumes independent standard-normal score vectors, not empirical independence established from market data. [Packet](../inputs/complete.json), candidate_ids, rng and observation; [receipt](../receipt.json), source identity and projection.

All three requested views and both score populations are present. This report uses only replicate 0 with 64 candidates. It does not turn the parent study's 256-replicate design into an observed success-rate estimate from this packet. No candidate was dropped or substituted in the comparison. The complete case contains no producer claim to reconcile. [Packet](../inputs/complete.json), observation.replicate/candidate_count and producer_claims.

## Interpretation and limits

Under the stated independent all-null model, at least one of 64 scores crosses the ordinary 5% threshold with probability 1-0.95^64, approximately 96.25%. The family comparison accounts for that fixed search. A raw tail of 0.006031664 for the newly selected M24 is therefore not the probability that it lacks a genuine effect, nor independent evidence confirming the original M34 selection. [Packet](../inputs/complete.json), theory; [brief](../inputs/brief.md), probability definitions.

This construction does not determine a correction for correlated candidates, temporal dependence, adaptive searches, undisclosed trials or changing market regimes. It supplies no implementation costs, financial horizon, production evidence or approval. Missing real-world history cannot be replaced with an invented effective trial count. [Brief](../inputs/brief.md) and [policy](../inputs/policy.md), stated scope and final paragraph.

The content reference covers the supplied reporting questions and numerical comparisons. No score generation or strategy change is performed as part of this report. Runtime fulfillment is not claimed: an actual executor must also provide the required result record, computed hashes and execution account. A complete account of these non-exceedances is a legitimate reporting outcome; it is not permission to use a candidate.
