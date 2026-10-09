# Equal error does not establish historical lineage

This source-only example composes model data and outcomes analysis. Six selectors review thirteen synthetic records across ten requested decision cutoffs. Current corrections can produce planted perfect errors, and two methods can have equal errors while citing different historical receipts. Numerical scoring and supported input history are separate findings.

| Case | Distinction |
|---|---|
| complete | Known publication, availability, revision and observation-date evidence permits an independent review of every selection. |
| missing-history | One local availability timestamp is withheld while actual selected IDs and arithmetic metrics remain known. |
| contradictory | Six producer claims conflict with supplied identity, timing, revision or ambiguity requirements. |

With an authenticated runtime from [the run guide](../../docs/running.md):

```sh
prose --harness claude --model haiku --native-profile claude-workspace-tools --permission-mode acceptEdits run examples/availability-review/program.md complete
```

Select missing-history or contradictory for the other packets. Calls can incur usage; this report has not been executed or assessed by an agent. Use [the common evaluator](../assess-report.md) for an actual result under its original selection. No new definition or component-package dependency is added.

[The receipt](receipt.json) separates observed selections from authored projections. [Developer reproduction](model/README.md) is outside the reporting program's permission scope. [The authored reference](sample-results/report.md) covers all six selectors and ten decisions. `python3 scripts/check_availability.py` checks fixed packet properties, timestamp relationships and metric arithmetic without running a query or model. It does not assess arbitrary prose, verify a production ingestion history or establish forecast performance.
