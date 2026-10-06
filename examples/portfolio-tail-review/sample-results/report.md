# Authored reference: complete portfolio-tail review

This is an authored reference, not an agent result. All six dependence proposals and sixteen confidence-level summaries are covered. Four joint distributions satisfy the selected marginal/default requirements; two do not, despite positive-definite correlation matrices. All native tail-allocation objectives agree with their exact references, but two native quantiles differ from the selected exact rule.

The synthetic one-year positive-loss portfolio has default probabilities A=0.10 and B=0.20, with deterministic losses on default USD 450,000 and 500,000. No discounting, mitigation or netting is included. State order 00/10/01/11 gives losses USD 0/450,000/500,000/950,000. The selected comparison base is independent defaults at q=1/50. [Evidence: complete.json/scope; brief.md; policy.md.]

| Proposal | Indicator correlation | State probabilities 00, 10, 01, 11 | Joint-distribution requirements |
|---|---|---|---|
| q_0 | -1/6 | 7/10, 1/10, 1/5, 0 | met |
| q_1_50 | 0 | 18/25, 2/25, 9/50, 1/50 | met |
| q_1_20 | 1/4 | 3/4, 1/20, 3/20, 1/20 | met |
| q_1_10 | 2/3 | 4/5, 0, 1/10, 1/10 | met |
| rho_negative_half | -1/2 | 33/50, 7/50, 6/25, -1/25 | breached |
| rho_positive_nine_tenths | 9/10 | 207/250, -7/250, 9/125, 16/125 | breached |

Each row is supported by candidates[id].states, joint_default_probability, indicator_correlation and correlation_eigenvalues. All six matrices are positive definite. For correlation −1/2 the joint-default probability is −0.04; for correlation 9/10, A-only probability is −0.028. Those tables cannot be probability distributions under the selected marginals. No risk summary is supplied for them; absence here does not mean zero risk. No clipping or alternative marginal assumption is applied.

Every valid distribution has expected loss USD 145,000: 0.10×450,000+0.20×500,000. This additive expectation does not require independent defaults. Equal marginals and mean therefore do not establish the same joint distribution or tail behavior.

VaR is the first loss whose cumulative probability reaches alpha. Expected shortfall (ES) averages the worst mass 1−alpha, splitting an atom if needed. Strict and inclusive conditional means use their own event probabilities. All amounts below are USD; the final two columns condition on the exact VaR.

| Proposal | Confidence | Exact VaR | Native VaR | Exact ES | Mean above VaR | Mean at or above VaR |
|---|---|---|---|---|---|---|
| q_0 | 80% | 450,000 | 500,000 | 500,000.00 | 500,000.00 | 483,333.33 |
| q_0 | 90% | 500,000 | 500,000 | 500,000.00 | undefined | 500,000.00 |
| q_0 | 95% | 500,000 | 500,000 | 500,000.00 | undefined | 500,000.00 |
| q_0 | 99% | 500,000 | 500,000 | 500,000.00 | undefined | 500,000.00 |
| q_1_50 | 80% | 450,000 | 500,000 | 545,000.00 | 545,000.00 | 517,857.14 |
| q_1_50 | 90% | 500,000 | 500,000 | 590,000.00 | 950,000.00 | 545,000.00 |
| q_1_50 | 95% | 500,000 | 500,000 | 680,000.00 | 950,000.00 | 545,000.00 |
| q_1_50 | 99% | 950,000 | 950,000 | 950,000.00 | undefined | 950,000.00 |
| q_1_20 | 80% | 450,000 | 450,000 | 612,500.00 | 612,500.00 | 580,000.00 |
| q_1_20 | 90% | 500,000 | 500,000 | 725,000.00 | 950,000.00 | 612,500.00 |
| q_1_20 | 95% | 500,000 | 500,000 | 950,000.00 | 950,000.00 | 612,500.00 |
| q_1_20 | 99% | 950,000 | 950,000 | 950,000.00 | undefined | 950,000.00 |
| q_1_10 | 80% | 0 | 0 | 725,000.00 | 725,000.00 | 145,000.00 |
| q_1_10 | 90% | 500,000 | 500,000 | 950,000.00 | 950,000.00 | 725,000.00 |
| q_1_10 | 95% | 950,000 | 950,000 | 950,000.00 | undefined | 950,000.00 |
| q_1_10 | 99% | 950,000 | 950,000 | 950,000.00 | undefined | 950,000.00 |

Rows map to candidates[id].risk_summaries[alpha], including reference and native observations. All sixteen native ES objectives match the exact references within absolute USD 1e-6. Every supplied native allocation has four masses within its state bounds, sums to 1−alpha within 1e-10, and yields the recorded objective. These candidate checks are separate from successful solver termination and from the mathematical reference.

**Tail interpretation.** At 95%, q=0 and q=0.02 share VaR USD 500,000 but have ES USD 500,000 and 680,000. At q=0.05, VaR remains USD 500,000 while ES reaches USD 950,000. For independent defaults, the worst 5% comprises 2% at USD 950,000 and 3% of the USD 500,000 atom. Its mean is USD 680,000. The strict conditional mean instead uses 2% and is USD 950,000; the inclusive mean uses 20% and is USD 545,000. An empty strict tail has an undefined conditional mean, not zero. [Evidence: q_1_50, alpha=19/20, reference allocation/probabilities; all other reference summaries.]

**Quantile boundary.** At 80%, q=0 and q=0.02 have exact CDF 0.8 at USD 450,000 but native CDF 0.7999999999999999. The native inverse returns USD 500,000, consistent with its represented CDF but different from exact VaR USD 450,000. The CDF error satisfies 1e-14 tolerance; the selected quantile rule still has two breaches. An acceptable CDF approximation cannot substitute for that distinct requirement. The other fourteen quantiles match. [Evidence: native_cdf_at_losses and alpha=4/5 summaries.]

No required allocation is missing in this complete packet and no producer assertions are supplied. The review uses permitted arithmetic and records, without rerunning a solver or inspecting source. The receipt identifies a developer calculation and its environment; it does not establish agent fulfillment or institutional acceptance. These stipulated distributions are not calibrated borrower forecasts or a regulatory capital calculation. A complete adverse report is compatible with fulfilled reporting; this authored reference itself is not execution evidence.

Source identity locators (SHA-256, computed while authoring):

```text
examples/portfolio-tail-review/program.md  dd2080580d682e05fb222b7d802f13553a6cc53491eeebebf6e029e5dcc04f14
examples/portfolio-tail-review/inputs/brief.md  80d4f0cb5ec27528b9d6449d5cf82c8b310ec3d6aa87e9f50f3a1c6bd1eff509
examples/portfolio-tail-review/inputs/policy.md  2a4e0a6db215c77abdfbdd3b5a9dd21e40291a0dbe513538be9a4dbeb828a00b
examples/portfolio-tail-review/inputs/complete.json  010b144775ca983b4798321cbb4852a21d80a04bc9676059fbd7471d86892679
examples/portfolio-tail-review/receipt.json  f06d45f4a314eff3bd5c62c2704cd5e0915ae260e1239cd16787df2242ea1743
contracts/claim-evidence.md  b023aeb88dc481b6cf31aff630a7adab28e52979827f5c6ecfda8861063d207c
contracts/credit-loss-review.md  7f2e9d6f65dafcf80b36369eb9d44f98aa71c2bf398af3022dbb6d8916a176f5
contracts/dependence-review.md  3d262b85a34f0e0604650a462956028049314318552bcdfbedce475985a22b74
contracts/institutional-facts.md  cfb18dc33211a4b511e8af40172596a4f9df592a3d99d41c93da877fd0b10ed1
contracts/numerical-evidence.md  74dad32c15bea33cda09f0e3b6b97f60eee3b097705aeee5d860c7b363480183
contracts/operating-report.md  e582e1c900f8f83d8a9c333e0e1900927e4e05bb5d63c66a3a4ca1007fd18e70
contracts/scenario-review.md  2ecfbae91425a159b0670a6142517ad3e27808ebbba415a3a5075aeb818d267c
```
