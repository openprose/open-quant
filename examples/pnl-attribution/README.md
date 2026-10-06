# Review P&L attribution and factor grouping

This source-only example composes [P&L explanation](../../contracts/pnl-explanation.md) and [sensitivity review](../../contracts/sensitivity-review.md). Six full-revaluation paths close to the same total but produce different factor contributions. Grouping factors before allocation also changes the answer.

With an authenticated runtime from [the run guide](../../docs/running.md):

```sh
prose --harness claude --model haiku --native-profile claude-workspace-tools --permission-mode acceptEdits run examples/pnl-attribution/program.md complete
```

Other cases are `missing-corner` and `contradictory`. Provider usage may be incurred. No agent has executed or assessed this program; the [reference report](sample-results/report.md) is authored. For separate assessment use [the operating-report evaluator](../assess-report.md), with the actual result directory, original program and selected case.

The missing case withholds corner 110's native and independent-reference values while retaining reported allocations and producer status. The total and four sequential paths remain independently supported; the selected mean allocation requires additional input evidence. Deriving a missing number from a downstream total does not recover its native record. Reading restrictions are instructions, not enforced filesystem isolation.

The [optional calculation and current guide](model/README.md) were committed before a bounded reproduction. All eight valuations, six paths, interactions, grouped results and 31 controls match the preceding study; timing and explicitly rebound source/plan identities are recorded separately. The [receipt](receipt.json) identifies source and packet bytes. Reporting permits arithmetic without rerunning QuantLib.

`python3 scripts/check_pnl_attribution.py` checks fixed evidence and adverse mutations without native pricing or provider calls. This is not an arbitrary prose evaluator, causal identification or proof of operational savings.
