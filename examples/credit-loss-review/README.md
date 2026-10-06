# Valid probabilities can still produce the wrong loss

This example composes credit-loss review and implementation review into one report. Six observed synthetic calculations use four default intervals. Every individual probability weight is between zero and one, but only one complete-case construction follows all selected requirements.

| Case | Distinction |
|---|---|
| complete | Correct probability meaning, exposure/severity and loss timing are separate from arithmetic consistency. |
| missing-severity | Actual calculations remain known, while one intended loss fraction is unavailable. The actual choice cannot supply the missing requirement. |
| contradictory | Favorable producer claims cannot override conditioning, timing or the synthetic probability basis. |

With an authenticated runtime from [the run guide](../../docs/running.md):

```sh
prose --harness claude --model haiku --native-profile claude-workspace-tools --permission-mode acceptEdits run examples/credit-loss-review/program.md complete
```

Select missing-severity or contradictory for the other packets. Calls can incur usage; no agent has executed or assessed this report in this candidate. Use [the common evaluator](../assess-report.md) for an actual result under its original selection. This source-only example leaves the reusable component package unchanged.

[The receipt](receipt.json) separates observed calculation from authored projections. [Developer reproduction](model/README.md) is outside reporting permissions. [The authored reference](sample-results/report.md) covers all six constructions. `python3 scripts/check_credit_loss.py` checks fixed input identities, arithmetic, binding classifications and selected corruptions without invoking QuantLib or a model. It does not assess arbitrary prose or establish accounting acceptance.
