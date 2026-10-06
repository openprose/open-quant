# Review a calibration's evidence

This example composes calibration review with model-data requirements. It uses the per-instrument output from a fresh reproduction of the retained SOFR comparison, then supplies two separately labeled authored alterations. It reviews evidence; it does not rerun the financial model.

| Case | Intended distinction |
|---|---|
| complete | 22 expected instruments for each method, two explicitly excluded source tenors, all reported residuals within the illustrative limit. |
| missing | 6M is absent for both methods. The old aggregate maximum cannot substitute for missing item-level evidence. |
| contradictory | A's altered 6M residual exceeds the limit and conflicts with displayed rates and the unchanged historical summary. Preserve the conflict; do not claim the actual model acquired that error. |

With the authenticated runtime described in [the run guide](../../docs/running.md):

```sh
prose --harness claude --model haiku --native-profile claude-workspace-tools --permission-mode acceptEdits run examples/calibration-review/program.md complete
```

Replace complete with missing or contradictory to select a different packet. These are proposed model invocations and can incur usage; none has been executed in this expansion. Assess an actual report with [the shared evaluator](../assess-report.md), preserving its original case selection.

[The reference report](sample-results/report.md) is authored. `node scripts/check_calibration.mjs` checks table identity, population accounting, precision and explicit numerical relationships; it does not evaluate the report's prose or contract fulfillment. [The numerical receipt](../../provenance/reproduction/2026-10-06.json) establishes the complete table's generation and the limits of reproduction. It does not cover the altered tables.
