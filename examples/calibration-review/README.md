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

## Case interpretation

These notes compare the authored cases; they are not part of the complete-case reference report or permitted evidence for a selected-case execution.

**Missing case.** The 6M row is unavailable: 21 of 22 instruments, or 42 of 44 method/instrument comparisons, are present. Available residuals are within limit, but neither method has complete item-level support. The retained aggregate summary does not fill that gap. Obtain the identified missing evidence; do not recreate it from the complete case while assessing this packet.

**Contradictory case.** A's altered 6M residual is +0.002 bp, 2,000 times the limit. It also conflicts with both rounded percentage rates, whose equal displayed values permit at most approximately 0.0001 bp difference from rounding, and with the unchanged summary maximum. Report the recorded breach and conflict. The supplied packet cannot support an overall all-clear for A, and the altered row does not prove the actual model produced it. B's 22 comparisons retain their supported input-fit finding. Reconcile the disputed source against authentic calculation evidence before accepting A's reported fit.
