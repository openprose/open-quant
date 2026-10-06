# Reverse-stress reporting example

A solver can find a loss-triggering scenario without finding the least severe one. This example composes [scenario review](../../contracts/scenario-review.md) and [optimization review](../../contracts/optimization-review.md) to examine eight native outcomes, three severity metrics and a finite scenario catalog. It adds no new contract definition.

From the source repository, with an authenticated harness configured as described in [the running guide](../../docs/running.md):

```sh
prose run examples/reverse-stress/program.md complete
prose run examples/assess-report.md examples/reverse-stress/program.md results/reverse-stress/<actual-run> complete
```

Use the actual fresh result directory returned by the first invocation. The [program](program.md) accepts `complete`, `missing-candidate` or `contradictory`. The missing case withholds one actual vector, gradient, physical-shock mapping and corresponding diagnostics while retaining its reported success, objective, loss and severity. The analytical bound and seven other observed candidates remain supplied. The contradictory case adds unsupported producer assertions without changing numerical evidence.

The [reference report](sample-results/report.md) is authored, not an observed agent result. No agent has executed or assessed this program. Source checks inspect fixed numerical records and selected mutations rather than arbitrary prose. Reading restrictions are instructions, not filesystem isolation.

The [optional numerical reproduction](model/README.md) is separate from the reporting invocation. Its public source reproduces the fixed study exactly except new timing and explicitly rebound source/plan identities. The [receipt](receipt.json) identifies that observation and the authored case projections. The component package contains reusable contracts; this example and its development tools are source-only.
