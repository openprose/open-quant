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

## Case interpretation

These notes compare the authored cases; they are not part of the complete-case reference report or permitted evidence for a selected-case execution.

**Missing.** B3 is absent. A's three-observation descriptive mean remains USD33,333.33; B's two-observation descriptive mean is USD10,000. Comparing those unequal populations would favor B while omitting the observation on which A has its largest error. The common population is F1/F2: A's mean is zero and B's USD10,000, so B minus A is +USD10,000. A has lower error on this two-item subset. A relative reduction against A is undefined because its mean error is zero. Neither this result nor an invented B3 establishes a full three-item comparison. The producer's blanket claim is unsupported by a comparable full-cohort result.

**Late forecast.** B3 is issued September 30 at 17:06 UTC, after F3's 09:00–17:00 window and the 17:05 outcome availability. Its matching USD100,000 value is not eligible predictive evidence. Coverage and metrics therefore match the two-item comparison above, but the reason is timing incompatibility rather than an absent record. Preserve that distinction.

All cases retain four expected cohort observations, three mature outcomes and one immature item. Complete has three paired eligible observations; missing and late-forecast have two.

Accurate reporting may be fulfilled despite incomplete paired coverage. Obtain the actual admissible missing forecast or report its absence; do not backdate a forecast or borrow another case's value. No model was trained, tuned, run or approved.
