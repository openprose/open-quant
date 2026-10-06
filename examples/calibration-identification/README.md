# Calibration fit and identified outputs

A curve can fit every supplied observation while leaving some outputs undetermined. This example composes [calibration review](../../contracts/calibration-review.md) and [optimization review](../../contracts/optimization-review.md) to distinguish fit, admissibility, optimizer success and regularization. It adds no definition or financial theory.

From the source checkout, with an authenticated harness configured through [the running guide](../../docs/running.md):

```sh
prose run examples/calibration-identification/program.md complete
prose run examples/assess-report.md examples/calibration-identification/program.md results/calibration-identification/YOUR-RUN complete
```

Use the first invocation's actual result directory. The [program](program.md) accepts `complete`, `missing-allocation` and `contradictory`. The missing case withholds C2's rate vector and half-year results while retaining reported longer-maturity quantities; those do not identify its allocation. The contradictory case adds claims without altering numerical records. Each invocation has separate model usage.

The [reference report](sample-results/report.md) is authored; this reporting and assessment route remains agent-unqualified. [The numerical reproduction](model/README.md) is a separate operation. One bounded public CPU process reproduced all study observations and 90 controls, apart from fresh timing and explicitly rebound source/plan identities. The [receipt](receipt.json) identifies that calculation and the authored packet projections. Offline checks verify fixed data relationships, not arbitrary prose fulfillment.

Examples and calculation helpers are source-only; the component package contains reusable contracts. Reading restrictions are instructions, not enforced filesystem isolation.

## Case interpretation

These notes compare the authored cases; they are not part of the complete-case reference report or permitted evidence for a selected-case execution.

In `missing-allocation`, C2's retained longer-maturity values and reported residuals do not determine its actual rates, six-month price or admissibility. Family-level identities remain available; another proposal or optimum cannot replace the missing actual vector. In `contradictory`, the same numerical records do not support the seven added producer claims.
