# A new winner is not confirmation of the old one

This report composes outcomes analysis and model data. It follows one candidate chosen from synthetic scores, evaluates that frozen candidate on a separate sample, and compares it with a new winner chosen on that evaluation sample. The numerical values are observed from a reproducible construction; the reporting program and reference are authored.

| Case | Distinction |
|---|---|
| complete | Selection maxima and frozen-candidate evaluation support different statistical comparisons. |
| missing-evaluation | The selection result remains available while both evaluation views are unresolved. |
| contradictory | A lower raw tail does not establish a genuine effect or independent confirmation after reselection. |

With an authenticated runtime from [the run guide](../../docs/running.md):

```sh
prose --harness claude --model haiku --native-profile claude-workspace-tools --permission-mode acceptEdits run examples/selection-review/program.md complete
```

Select missing-evaluation or contradictory for the other packets. Calls can incur usage; no agent has executed or assessed this report in this candidate. Use [the common evaluator](../assess-report.md) for an actual result under its original selection. This example is source-only; it adds no contract definition or package dependency.

[The receipt](receipt.json) identifies the calculation and selected projection. [Developer reproduction](model/README.md) is separate from reporting permissions. [The reference report](sample-results/report.md) illustrates the content. `node scripts/check_selection.mjs` checks fixed candidate/score bindings, selection rules, supplied probability arithmetic and adverse mutations; it does not assess prose or establish investment performance.
