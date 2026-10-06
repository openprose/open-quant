# From a decision note to a methodology document

This example binds the library's default documentation contract to a methodology document plus section, choice, citation and readiness records. It reuses the existing SOFR source and numerical evidence. The [short decision-note example](../sofr-curve/program.md) remains the simpler workshop entry.

The public document scope covers purpose, inputs, implementation, choices, numerical comparisons, limitations and explicit institutional gaps. Its requirements are authored for this example, not a regulator-issued checklist. A complete account under this supplied public scope is not a complete institutional submission.

With an authenticated runtime from [the run guide](../../docs/running.md):

```sh
prose --harness claude --model haiku --native-profile claude-workspace-tools --permission-mode acceptEdits run examples/sofr-documentation/program.md complete
```

Select missing-locality to withhold one mandatory numerical result. An executor should retain useful partial work and identify nonfulfillment rather than claiming that a gap label supplied the missing result. A complete audit can support that negative finding; a correct negative finding alone does not establish a complete audit.

Assess an actual result with [the dedicated assessment entry](assess.md), supplying its directory and original case. The full artifact set differs from the operating reports' two-file interface. These commands can incur usage; no agent has executed or assessed this new composition. Historical full-document candidates and earlier decision-note runs do not qualify it.

[The reference document and records](sample-results/README.md) are authored illustrations. Source examples are not included in the reusable component package. No additional numerical calculation, source acquisition or institutional approval is supplied by this example.
