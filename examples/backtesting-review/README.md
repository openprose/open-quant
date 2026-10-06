# Review five days of risk forecasts

This synthetic example demonstrates [backtesting](../../contracts/backtesting.md), which composes outcomes-analysis, numerical-evidence and operating-report requirements. It separates three things that are easy to conflate: observed losses, unavailable evidence and exceptions required by house policy.

The five-day packet is intentionally small enough to inspect. It is not a Basel annual backtest or a source of regulatory capital conclusions. The [house policy](inputs/policy.md) explains which ideas it borrows and which conventions are authored for the example.

With an authenticated runtime from [the run guide](../../docs/running.md):

```sh
prose --harness claude --model haiku --native-profile claude-workspace-tools --permission-mode acceptEdits run examples/backtesting-review/program.md complete
```

Other cases are `missing`, `contradictory` and `late-forecast`. Each has a separate input file so an experiment can stage only its selected case. These commands can incur provider usage; no model-backed execution of this example has occurred.

Read [the program](program.md) and [authored reference report](sample-results/report.md). `node scripts/check_backtesting.mjs` verifies the explicit fixture arithmetic and mutation controls, not arbitrary prose, statistical adequacy or regulatory eligibility.
