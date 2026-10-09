# Synthetic selection-history review

Review SELECTION-2026-10-06, replicate 0, candidate set M01–M64, on October 6, 2026. This is a constructed example of quantitative performance-evidence review. Scores are dimensionless standard-normal statistics, not asset returns, Sharpe ratios, money or an actual investment-strategy backtest. No financial horizon, production use, institutional acceptance or approval record is supplied.

All candidates have zero true effect in the specified mathematical model. Selection and evaluation score vectors are independent, with independent standard-normal entries. The observed pseudorandom vectors illustrate this assumption reproducibly; they do not prove empirical independence in financial data. Candidate order is M01 through M64. Every candidate has equal weight in the selection opportunity; a winner is the highest score, with the smallest candidate index breaking an exact tie.

The three requested views have different roles:

- `selection_winner` chooses a candidate using the selection scores and reports that selected score.
- `frozen_evaluation` reports the evaluation score of that same candidate. It does not choose using evaluation scores.
- `reselected_evaluation` chooses a winner using the evaluation scores. Those scores now serve selection, even though their dataset label says evaluation.

The nominal one-candidate one-sided null threshold is Phi^-1(0.95). For a maximum over K=64 independent all-null scores, the corresponding family threshold is Phi^-1(0.95^(1/64)). The supplied raw tail is 1-Phi(z); the independent-family tail for a maximum is 1-Phi(z)^64. These are sampling probabilities under the stated model, not posterior probabilities of no effect or success. The family formula is not a general remedy for dependent or adaptive financial searches and is not a probability-of-backtest-overfitting estimator.

The receipt identifies an actual CPU calculation and the authored projection. Replicate 0 and K=64 were selected by index before its result was inspected for this example. The report uses that one selected replicate, not all 256 replicates of the developer study. No frequency estimate or general reliability claim follows from this single reporting packet. Its scores and all-null construction must not be presented as observed investment performance.
