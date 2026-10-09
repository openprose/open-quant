# What does a tighter simulation interval establish?

This example composes simulation review and implementation review. It uses observed synthetic option calculations to distinguish sampling precision, dependence and the quantity being estimated. Repeating each observation twice reduces a naive standard error without improving the estimate. Omitting discounting estimates the wrong target, even with a small sampling error.

| Case | Question |
|---|---|
| complete | Which views meet the target, uncertainty-method and precision requirements separately? |
| missing-large-sample | What remains unresolved without the required larger-sample observation? |
| contradictory | Does a favorable producer claim follow from the reported small standard errors? |

With an authenticated runtime from [the run guide](../../docs/running.md):

```sh
prose --harness claude --model haiku --native-profile claude-workspace-tools --permission-mode acceptEdits run examples/simulation-review/program.md complete
```

Select missing-large-sample or contradictory for the other packets. Calls can incur usage; no agent has executed or assessed this report in this candidate. Use [the common evaluator](../assess-report.md) for an actual result under its original selection. This example is in the source checkout, not the reusable component package.

[The receipt](receipt.json) identifies the observed calculation and authored projections. [The numerical source](model/README.md) supports explicit reproduction. [The reference report](sample-results/report.md) is authored. `node scripts/check_simulation.mjs` checks retained-record arithmetic, selected policy bindings and distinguishing cases; it does not evaluate prose or establish empirical coverage, financial suitability or operational savings.
