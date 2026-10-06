# Review two valuation comparisons

This synthetic example composes [valuation comparison](../../contracts/valuation-comparison.md) and [model data](../../contracts/model-data.md). It produces a short exception report from two positions, their internal prices and supplied comparison quotes. It illustrates why matching instrument IDs and subtracting numbers are insufficient: units, valuation basis, timing and coverage also matter.

From an authenticated runtime configured as described in [the run guide](../../docs/running.md):

```sh
prose --harness claude --model haiku --native-profile claude-workspace-tools --permission-mode acceptEdits run examples/valuation-review/program.md complete
```

Other case names are `missing`, `stale` and `basis-mismatch`. Calls can incur provider usage. These cases have not been executed by a model. Read [the program](program.md), [house policy](inputs/policy.md), [packet](inputs/packet.json) and [authored reference](sample-results/report.md) before running.

`node scripts/check_valuation.mjs` checks only explicit synthetic price conversions, differences and case distinctions. The results are not market observations, a certified valuation, an independent price-verification operation or measured savings. No trading or accounting action is requested.
