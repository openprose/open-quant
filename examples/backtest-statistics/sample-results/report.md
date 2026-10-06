# Exception-statistics review

**Authored reference for `complete`; not an agent-produced result.** This review covers BACKTEST-STATISTICS-2026-10-06, all six supplied series, each with 250 synthetic binary observations. The aggregate counts agree with recounts of the ordered indicators, and their one-based exception positions agree. No observations are excluded. This is a review of statistical evidence; actual forecasts, losses, forecast availability and forecast/outcome pairing are not supplied. [Evidence: complete.json, sequences BT01–BT06; brief.]

| Series | Exceptions | Blocks of ones | Excess-frequency p | Two-sided 95% probability interval | Conditional clustering p |
|---|---:|---:|---:|---|---:|
| BT01 | 5 | 5 | 0.107812373096 | [0.006525070002, 0.046053577154] | 1 |
| BT02 | 5 | 1 | 0.107812373096 | [0.006525070002, 0.046053577154] | 3.146974734513e-08 |
| BT03 | 5 | 1 | 0.107812373096 | [0.006525070002, 0.046053577154] | 3.146974734513e-08 |
| BT04 | 0 | 0 | 1 | [0, 0.014647188636] | 1 |
| BT05 | 10 | 10 | 0.000250190069 | [0.019345498505, 0.072329355490] | 1 |
| BT06 | 10 | 1 | 0.000250190069 | [0.019345498505, 0.072329355490] | 1.100429908762e-15 |

Probabilities and endpoints are fractions. Rows map to each sequence's frequency_test, probability_interval and clustering_test. At the separately specified strict 5% thresholds, excess frequency is rejected for BT05 and BT06; it is not rejected for BT01–BT04. Clustering is identified for BT02, BT03 and BT06. The other clustering calculations do not reject their selected null. There is no combined acceptance rule or familywise error guarantee. [Evidence: policy; table fields and exception positions.]

**Matching counts do not establish matching timing.** BT01, BT02 and BT03 each have observed frequency 2% and excess-frequency p≈0.108. BT01 has five separated exceptions; BT02 has one consecutive block at positions 123–127; BT03 has one block at positions 1–5. The last case confirms that a block starting at the first observation counts. Their frequency summaries agree, while their timing findings differ. The corresponding conditional probability for the one-block pattern is about 3.15×10⁻⁸. [Evidence: BT01–BT03 indicators, positions and one_runs.]

**Non-rejection has limited meaning.** BT01 and BT05 are deliberately regularly spaced. A lower-tail block-count p-value of one does not establish random timing, independence or absence of every form of dependence. BT04 has no exceptions and no information about exception timing; its degenerate conditional probability of one cannot establish independence either. The selected clustering test addresses too few blocks given the count. [Evidence: BT01/BT05 position gaps; BT04 count; policy.]

**Zero exceptions retain uncertainty.** BT04's exact two-sided 95% interval reaches approximately 1.46%, despite observing zero exceptions in 250 trials. It does not establish zero exception probability. This interval concerns repeated-sample coverage under independent trials with constant probability, not a posterior probability for the parameter. The two-sided interval is a different question from the one-sided excess-frequency test. [Evidence: BT04 probability_interval; policy.]

**Statistical assumptions remain material.** Native excess-frequency probabilities agree with exact binomial sums within 1e-12; native interval endpoints agree with supplied finite-sum references within 1e-10. Recounted block counts support the conditional probabilities. Clustering in BT02, BT03 and BT06 challenges the independence assumption behind binomial inference, so the associated frequency quantities and intervals remain calculations under that null, not unconditional confidence guarantees. [Evidence: all frequency_test, probability_interval and clustering_test fields.]

All requested series and statistical questions are covered by this authored reference. The packet contains no producer assertions. No ordered evidence is missing in this case. Source identity and observed environment are attributed to the receipt; this report does not claim to have reproduced the measurement source. The calculations do not establish VaR calibration, regulatory eligibility, model approval, performance on unobserved data or operational savings. Reporting coverage and financial-model acceptance remain separate; actual forecast records and institutional criteria would be needed for a broader review.

## Identity locators

SHA-256 values below identify this reference's selected source files; the optional calculation source identity is recorded in receipt.json.

```text
examples/backtest-statistics/program.md  3ce4b0c993bd968ddc0f3f654a118176700b25e3f7979e888877c0a556112340
examples/backtest-statistics/inputs/brief.md  56781e8b5c9df7014442dc2a937c98d7c73ad3d02e90462b74286fd01cc7e597
examples/backtest-statistics/inputs/policy.md  2bd5cd3ab7f36fc33bdbb63a8eb824896cb9b9c3e0967ec1af0b4ed5082e2928
examples/backtest-statistics/inputs/complete.json  e34bb1836bb32714e0abfa135f7584700e287b186255d67d54578e8607e1d9a4
examples/backtest-statistics/receipt.json  5e5f3300b4f75cab8dc45d8f1c3b60f8ece1bf23cafca5100d034ff86a3dfc46
contracts/backtesting.md  0ae5a63aa9226968b75409b8b23d7f613a354c8947c5e7792278da793ae30ecc
contracts/outcomes-analysis.md  feda0de65ffaa28fa57b78934dd30f706700ac0de7acc1f566a8d2595df86077
contracts/operating-report.md  e582e1c900f8f83d8a9c333e0e1900927e4e05bb5d63c66a3a4ca1007fd18e70
contracts/numerical-evidence.md  74dad32c15bea33cda09f0e3b6b97f60eee3b097705aeee5d860c7b363480183
contracts/claim-evidence.md  b023aeb88dc481b6cf31aff630a7adab28e52979827f5c6ecfda8861063d207c
contracts/institutional-facts.md  cfb18dc33211a4b511e8af40172596a4f9df592a3d99d41c93da877fd0b10ed1
```
