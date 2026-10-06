# Review what exception statistics establish

This source-only example composes [backtesting](../../contracts/backtesting.md) with its adopted outcomes, numerical-evidence and reporting requirements. Six observed calculations on constructed binary sequences show why counts, timing, uncertainty and model approval must remain separate.

With an authenticated runtime from [the run guide](../../docs/running.md):

```sh
prose --harness claude --model haiku --native-profile claude-workspace-tools --permission-mode acceptEdits run examples/backtest-statistics/program.md complete
```

Other cases are `missing-order` and `contradictory`. Provider usage may be incurred. No agent has executed or assessed this example; the [reference report](sample-results/report.md) is authored. For a separate assessment, use [the operating-report evaluator](../assess-report.md) with the actual result directory, original program and selected case.

The missing case keeps aggregate counts and reported statistics while withholding one series' ordered indicators and positions. Frequency calculations remain available from the aggregate, but reported timing cannot replace its missing support. The contradictory case adds producer claims without changing numerical evidence. Case restrictions are instructions, not filesystem isolation.

The [optional calculation](model/README.md) produced the evidence before report authoring. Its public source was committed before one bounded reproduction; all numerical observations and 61 controls match the preceding study. Timestamp, duration and explicitly rebound source/plan identities are separate. The [receipt](receipt.json) identifies source and packet bytes. The reporting program permits arithmetic but does not rerun that calculation.

`python3 scripts/check_backtest_statistics.py` verifies fixed records and adverse mutations without SciPy, provider calls or arbitrary prose assessment. This is a statistical-evidence example, not actual forecasts, a regulatory backtest, a new statistical method or evidence of model reliability. The existing five-day [backtesting example](../backtesting-review/README.md) separately addresses forecast availability, P&L series and house-policy exception counting.
