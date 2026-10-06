# Review a model monitoring packet

This small example composes [model monitoring](../../contracts/model-monitoring.md) with [limitations and remediation](../../contracts/limitations-and-remediation.md). It asks for one report: which expected observations are supported, which limits were breached, and what remains unresolved?

All institutions, model identifiers, observations and house policies here are synthetic. Values illustrate reporting distinctions; they are not recommended risk limits or financial-model validation results. The example requires no knowledge of yield-curve construction.

The cases share one packet. Its file hash covers all cases, while only the selected case and shared records may support the report. This is an evidence-use restriction, not a blind trial with alternative cases hidden from the executor.

## Run

Use the authenticated runtime setup in [the run guide](../../docs/running.md). From the repository root, pass one case name, `complete`, `missing` or `contradictory`:

```sh
prose --harness claude --model haiku --native-profile claude-workspace-tools --permission-mode acceptEdits run examples/monitoring-review/program.md complete
```

This command can incur provider usage. The new example has not been run with a model. Inspect the reported result directory, then use [the operating-report assessment entry point](../assess-report.md) with this program, that directory and the selected case. The [run guide](../../docs/running.md#assess-an-operating-report) shows the command. An automatic evaluator can itself miss requirements; inspect its findings.

## Inspect before spending

Read [the program](program.md), [house policy](inputs/policy.md), [evidence packet](inputs/packet.json), and the [authored reference report](sample-results/report.md). The sample covers the complete case and is not agent-generated. [Distinguishing cases](../../tests/cases/operating-reports.md) explain the negative controls and the difference between a complete report and a passing control.

The fixture checker verifies selected arithmetic, classification and row coverage:

```sh
node scripts/check_monitoring.mjs
```

It does not interpret the contracts, evaluate arbitrary report prose or establish model performance. It is a transparent reference calculation for these synthetic inputs. It is not part of the executor's program and does not generate the requested report.
