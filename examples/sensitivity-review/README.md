# Small price errors can become large sensitivity errors

This report composes sensitivity review and implementation review. It accounts for three synthetic calls, six forward bumps and two price representations. Prices within half a cent can yield misleading derivatives, and the smallest unrounded bump need not be the most accurate. The numerical records are observed; the reporting program, policy and reference are authored.

| Case | Distinction |
|---|---|
| complete | Price accuracy, derivative accuracy and finite premium changes are separate findings. |
| missing-unrounded | Rounded derivative findings remain available, but missing underlying observations cannot be reconstructed from their displays. |
| contradictory | Neither a small price error, the smallest bump nor zero rounded changes guarantees useful sensitivities. |

With an authenticated runtime from [the run guide](../../docs/running.md):

```sh
prose --harness claude --model haiku --native-profile claude-workspace-tools --permission-mode acceptEdits run examples/sensitivity-review/program.md complete
```

Select missing-unrounded or contradictory for the other packets. Calls can incur usage; no agent has executed or assessed this report in this candidate. Use [the common evaluator](../assess-report.md) for an actual result under its original selection. This source-only example adds no definition or package dependency.

[The receipt](receipt.json) identifies the calculation and authored projection. [Developer reproduction](model/README.md) is separate from reporting permissions. [The reference report](sample-results/report.md) covers all 36 views and 72 metric findings. `python3 scripts/check_sensitivity.py` checks fixed arithmetic, units, missing observations and selected corruptions without importing QuantLib. It does not assess prose or establish a hedge or institutional acceptance.
