# Review a change using the retained SOFR evidence

This example reuses the original SOFR comparison without rerunning the model or changing its documentation program. It asks whether a hypothetical switch from method A to method B meets selected numerical requirements.

The two modes differ by one additional requirement:

- `shape` applies [repricing and forward-movement requirements](house/shape.md).
- `shape-and-locality` also applies [a locality requirement](house/locality.md).

The evidence stays the same. Under the first set, B meets the selected numerical criteria. Under the second, B fails the locality criterion. That is a change in the agreement, not a change in the model or proof that one model is universally better. Both reports can fulfill their reporting contract by explaining the result correctly.

With an authenticated runtime from [the run guide](../../docs/running.md):

```sh
prose --harness claude --model haiku --native-profile claude-workspace-tools --permission-mode acceptEdits run examples/sofr-change-review/program.md shape
prose --harness claude --model haiku --native-profile claude-workspace-tools --permission-mode acceptEdits run examples/sofr-change-review/program.md shape-and-locality
```

These calls can incur provider usage. Neither mode has been executed with a model in this expansion. [The authored reference](sample-results/report.md) illustrates the intended distinction; `node scripts/check_sofr_change.mjs` checks the explicitly bound numerical comparisons only.

The source is retained historical calculation evidence with [provenance and notices](../../provenance/README.md), not current market data. The house limits and proposed change are synthetic. This is not a production migration, model validation or approval.
