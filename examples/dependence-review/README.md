# Can the parts pass while the combination fails?

This report composes dependence review and model data. It examines synthetic correlation inputs, observation populations, proposed adjustments and exposure alignment. The purpose is to make a useful review distinction: numerical validity, data support and compatibility with the intended use are separate requirements.

| Case | Distinction |
|---|---|
| complete | Individually valid pairs can be jointly invalid; singularity and adjustment constraints need separate findings. |
| missing-membership | Joint invalidity remains known while observation-population alignment is unresolved. |
| contradictory | Favorable producer claims conflict with the matrices, populations, policy and exposure binding. |

With an authenticated runtime from [the run guide](../../docs/running.md):

```sh
prose --harness claude --model haiku --native-profile claude-workspace-tools --permission-mode acceptEdits run examples/dependence-review/program.md complete
```

Select missing-membership or contradictory for the other packets. Calls can incur usage; this report has not been executed or assessed by an agent in this candidate. Use [the common evaluator](../assess-report.md) with the original program and selected case for an actual result. This source example is not included in the component package.

[The receipt](receipt.json) identifies one observed CPU calculation and its authored projections. [Numerical reproduction](model/README.md) is a separate developer action, outside the report's permissions. [The reference report](sample-results/report.md) is authored. `node scripts/check_dependence.mjs` checks fixed matrix relationships, population records, policy bindings and mutations; it does not assess prose, empirical suitability or financial approval.
