# The same expected loss can conceal a different tail

This example composes credit-loss, dependence and scenario requirements into one report. Four synthetic joint distributions share the same mean loss but have different tail measures; two other proposals have valid correlation matrices but incompatible probabilities. All native/reference quantile differences remain visible.

| Case | Distinction |
|---|---|
| complete | Matrix definiteness, joint-distribution validity, mean loss and tail behavior answer different questions. |
| missing-allocation | An exact risk result and native objective remain known while one actual solver allocation cannot be checked. |
| contradictory | Assertions cannot redefine expected shortfall, erase quantile differences or approve invalid probability tables. |

With an authenticated runtime from [the run guide](../../docs/running.md):

```sh
prose --harness claude --model haiku --native-profile claude-workspace-tools --permission-mode acceptEdits run examples/portfolio-tail-review/program.md complete
```

Select missing-allocation or contradictory for the other packets. Calls can incur usage; no agent has executed or assessed this report in this candidate. Use [the common evaluator](../assess-report.md) for an actual result under its original selection. No new definition or package dependency is needed for this source-only example.

[The receipt](receipt.json) distinguishes observed calculations from authored projections. [Developer reproduction](model/README.md) is outside reporting permissions. [The authored reference](sample-results/report.md) accounts for every proposal and risk summary. `python3 scripts/check_portfolio_tail.py` checks the fixed records and selected corruptions without a solver or model call; it does not assess arbitrary prose or establish financial acceptance.
