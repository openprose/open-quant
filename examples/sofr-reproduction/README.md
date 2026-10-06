# Produce fresh reproduction evidence

This program demonstrates evidence production rather than review of a prepared packet. It uses the [model-reproduction contract](../../contracts/model-reproduction.md) to request one bounded calculation and a report distinguishing execution, numerical agreement and remaining limitations.

The financial implementation and retained derived inputs are unchanged. The helper requires the exact versions and POSIX environment described in [the reproduction guide](../sofr-curve/model/README.md). Missing dependencies are a reportable prerequisite, not permission to install them or use a different calculation. No raw-data acquisition or model-provider call is part of the helper.

With an authenticated, suitably permitted runtime, supply a fresh absolute output path outside the checkout:

```sh
prose --harness claude --model haiku --native-profile claude-workspace-tools --permission-mode acceptEdits run examples/sofr-reproduction/program.md /absolute/new/reproduction
```

The agent and its native harness must be permitted to execute the helper and write to the selected external path. Model usage can incur charges. The program has not been executed or assessed by an agent; an authenticated runtime and filesystem permission must be qualified for this route. Do not change permissions or billing routes silently if the launch is blocked.

For a direct developer calculation without a model call, use the helper command in the reproduction guide. That establishes only the helper's observed calculation and comparison, not execution of the OpenProse reporting program. Its process tests use tiny local fixtures to distinguish a zero exit from a usable result, a numeric mismatch from missing evidence, and a matching partial file from completed work.

Assess the actual result with [the reproduction assessment](assess.md), replacing the path below with the subject directory returned by the execution. It checks the report, result and calculation artifacts without rerunning the model:

```sh
prose --harness claude --model haiku --native-profile claude-workspace-tools --permission-mode acceptEdits run examples/sofr-reproduction/assess.md /absolute/actual/reproduction
```

This is a separate model invocation. Supply any execution evidence needed to assess effects that final artifacts cannot establish. The [authored assessment cases](../../tests/cases/reproduction-assessment.md) are review expectations, not observed performance; this assessment route remains agent-unqualified.

The source-only program and helper remain outside the component package. No financial approval, publication or operational action is implied by reproduction.
