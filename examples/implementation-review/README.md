# When a passing property misses a pricing error

This example composes implementation review and model description. It supplies actual synthetic calculations from three pricing adapters, including two deliberately incorrect input mappings. One incorrect adapter passes parity in all ten selected cases but agrees with the intended prices in only three. The familiar baseline passes for all three adapters.

| Selected case | Reporting question |
|---|---|
| complete | What do price agreement, parity, mapping inspection and observed invalid-input controls establish separately? |
| baseline-only | What is supported when only one numerical case is supplied, even though source inspection exposes mapping errors? |
| contradictory | Does a favorable producer claim survive comparison with the unchanged calculation records? |

With an authenticated runtime from [the run guide](../../docs/running.md):

```sh
prose --harness claude --model haiku --native-profile claude-workspace-tools --permission-mode acceptEdits run examples/implementation-review/program.md complete
```

Use baseline-only or contradictory for the other packets. The command can incur usage. No agent has executed or assessed this report in this candidate. Assess an actual result with [the common evaluator](../assess-report.md) under its original case selection. These source examples are not included in the reusable component package.

[The receipt](receipt.json) identifies the observed numerical calculation and authored case projections. [The model source](model/README.md) supports explicit reproduction; the report program itself does not authorize running it. [The reference report](sample-results/report.md) is authored. `node scripts/check_implementation.mjs` checks finite evidence identities, arithmetic and distinguishing cases; it does not evaluate prose or establish financial suitability, agent reliability or institutional approval.
