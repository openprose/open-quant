# Compare models on the same observations

This synthetic cash-flow review composes outcome analysis and model-data requirements. It shows how a missing difficult observation can reverse an apparent model comparison without changing any available forecast value.

| Case | Intended distinction |
|---|---|
| complete | On the same three mature observations, B has lower observed mean absolute error. The fourth observation is immature. |
| missing | B lacks F3. Comparing each model's own population falsely favors B; on their two common observations A has lower error. Neither subset comparison establishes the missing full-cohort result. |
| late-forecast | B's F3 value was issued after the window and observed outcome. It is unavailable for predictive evaluation, not a perfect eligible forecast. |

With an authenticated runtime from [the run guide](../../docs/running.md):

```sh
prose --harness claude --model haiku --native-profile claude-workspace-tools --permission-mode acceptEdits run examples/outcomes-review/program.md complete
```

Select missing or late-forecast for the other packets. These calls can incur usage; none has been run by an agent in this expansion. Assess an actual result with [the common evaluator](../assess-report.md) under the original case selection.

[The reference report](sample-results/report.md) is authored. `node scripts/check_outcomes.mjs` checks explicit pairing, timing, coverage and metric arithmetic. It does not evaluate prose, establish out-of-sample independence, validate financial forecasts or measure an OpenProse advantage over a baseline.
