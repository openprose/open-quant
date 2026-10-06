# Exposure and default dependence

The same exposure distribution and default probability can produce different expected losses. This example composes [credit-loss review](../../contracts/credit-loss-review.md) and [dependence review](../../contracts/dependence-review.md) to examine six joint proposals and two bound calculations. It adds no contract definition or financial theory.

From the source repository, with an authenticated harness configured through [the running guide](../../docs/running.md):

```sh
prose run examples/exposure-default/program.md complete
prose run examples/assess-report.md examples/exposure-default/program.md results/exposure-default/<actual-run> complete
```

Use the actual result directory from the first invocation. The [program](program.md) accepts `complete`, `missing-joint` or `contradictory`. The missing case withholds one proposal's joint cells, conditional probabilities and exact references while retaining its reported aggregates. The other five proposals and bound evidence remain supplied. The contradictory case adds producer claims without changing numerical records.

The [reference report](sample-results/report.md) is authored, not an observed agent result. This reporting program remains agent-unqualified. Fixed arithmetic and projection checks do not assess arbitrary prose. Reading restrictions are instructions, not filesystem isolation.

The [optional numerical reproduction](model/README.md) is a separate operation. One public CPU process reproduces all six study proposals, both native LPs and 126 controls, excluding only fresh timing and explicitly rebound source/plan identities. The [receipt](receipt.json) records that calculation and authored projections. The component package contains reusable contracts; this example and its development checks remain source-only.
