# Solver success is one finding

This example composes optimization review and implementation review into one report. It retains seven observed solver outcomes and a separate rounded export from a synthetic convex problem. The intended problem, candidate feasibility and supported optimality remain separate from the solver's termination status.

| Case | Distinction |
|---|---|
| complete | Successful termination can accompany a different problem or inadequate original-unit accuracy; a failed run can still return a feasible candidate. |
| missing-candidate | The analytical reference and success flag remain known while one actual candidate is unavailable. |
| contradictory | Producer claims cannot override the original constraints, units, variable identities or observed candidate. |

With an authenticated runtime from [the run guide](../../docs/running.md):

```sh
prose --harness claude --model haiku --native-profile claude-workspace-tools --permission-mode acceptEdits run examples/optimization-review/program.md complete
```

Select missing-candidate or contradictory for the other packets. Calls can incur usage; no agent has executed or assessed this report in this candidate. Use [the common evaluator](../assess-report.md) for an actual result under its original selection. This source-only example adds no definition or package dependency.

[The receipt](receipt.json) separates observed calculation from authored projections. [Developer reproduction](model/README.md) is outside reporting permissions. [The authored reference](sample-results/report.md) accounts for every candidate. `python3 scripts/check_optimization.py` checks fixed evidence, source identities, original-unit arithmetic and selected corruptions without running a solver or model; it does not assess prose or authorize an allocation.
