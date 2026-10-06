# Hedge fit and later performance

A historical optimum, a permitted position and a useful subsequent result are different findings. This example composes [optimization review](../../contracts/optimization-review.md) and [outcomes analysis](../../contracts/outcomes-analysis.md) for one hypothetical hedge report. It also tests whether position units and selection timing survive the comparison.

From the source checkout, with an authenticated harness configured through [the running guide](../../docs/running.md):

```sh
prose run examples/hedge-outcomes/program.md complete
prose run examples/assess-report.md examples/hedge-outcomes/program.md results/hedge-outcomes/YOUR-RUN complete
```

Use the first invocation's actual result directory. The [program](program.md) accepts `complete`, `missing-selection-time` and `contradictory`. Missing selection time limits the advance-selection claim for C2 without removing its numerical evidence. The contradictory case adds producer claims without changing calculations. Each invocation has separate model usage.

The [reference report](sample-results/report.md) is authored; the reporting and assessment route remains agent-unqualified. [Numerical reproduction](model/README.md) is a separate operation. One bounded public CPU process reproduced all study observations and 106 controls, excluding only fresh timing and explicitly rebound source/plan identities. The [receipt](receipt.json) records that calculation and the packet projections. Offline checks verify fixed records, not arbitrary prose fulfillment.

Examples and numerical helpers are source-only. The component package remains unchanged. No actual hedge, forecast, institutional acceptance or savings is demonstrated.
