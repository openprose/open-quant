# A close valuation can conceal a cash-flow error

This report composes cash-flow review and valuation comparison. It reviews a synthetic receiving coupon leg under three constructions and two settlement-inclusion choices. The observed calculations are reproducible; the reporting program, policy and reference report are authored.

| Case | Distinction |
|---|---|
| complete | Correct arithmetic under different conventions does not establish compliance with selected terms. |
| missing-schedule | Known aggregate values and declared conventions do not supply omitted flow observations. |
| contradictory | Producer assertions cannot turn a close valuation into correct dates or generated obligations into paid flows. |

With an authenticated runtime from [the run guide](../../docs/running.md):

```sh
prose --harness claude --model haiku --native-profile claude-workspace-tools --permission-mode acceptEdits run examples/cashflow-review/program.md complete
```

Select missing-schedule or contradictory for the other packets. Calls can incur usage; no agent has executed or assessed this report in this candidate. Use [the common evaluator](../assess-report.md) for an actual result under its original selection. This example stays outside the component package.

[The receipt](receipt.json) identifies the calculation and authored projection. [Developer reproduction](model/README.md) is separate from reporting permissions. [The reference report](sample-results/report.md) illustrates the complete-case content. `node scripts/check_cashflow.mjs` checks fixed dates, amounts, inclusion, aggregate arithmetic, caller bindings and selected corruptions. It does not assess prose or establish an actual payment.
