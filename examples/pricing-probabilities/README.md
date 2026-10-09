# Pricing evidence and physical probabilities

Correct prices can coexist with different physical probabilities. This example composes [model description](../../contracts/model-description.md) and [numerical evidence](../../contracts/numerical-evidence.md) to explain a small complete two-state market and two intended uses. It adds no new contract definition or pricing theory.

From the source repository, with an authenticated harness configured as described in [the running guide](../../docs/running.md):

```sh
prose run examples/pricing-probabilities/program.md complete
prose run examples/assess-report.md examples/pricing-probabilities/program.md results/pricing-probabilities/YOUR-RUN complete
```

Use the actual fresh result directory from the first invocation. The [program](program.md) accepts `complete`, `missing-world` or `contradictory`. The missing case removes world B's probability inputs, discount factors and all derived physical quantities together, preserving market prices and world A. The contradictory case adds producer statements without changing numerical observations.

The [reference report](sample-results/report.md) is authored, not an observed agent result. This reporting program remains agent-unqualified. Its checks verify fixed arithmetic, projections and identities; they do not evaluate arbitrary prose. Reading restrictions are instructions, not filesystem isolation.

The [optional reproduction](model/README.md) is separate from the reporting invocation. One public calculation reproduces all six payoff records, both worlds and 63 controls from the fixed study, excluding only fresh timing and rebound source/plan identities. The [receipt](receipt.json) records the reproduction and case projections. The component package contains reusable contracts; examples and development checks remain in this source repository.
