# Review exposure, netting and collateral evidence

This source-only example composes [counterparty-exposure review](../../contracts/counterparty-exposure.md) and [implementation review](../../contracts/implementation-review.md). Nine observed SQL constructions share six synthetic trades and six collateral records. Their arithmetic can be correct under their own conventions while violating the selected netting, recognition or aggregation rules.

With an authenticated runtime from [the run guide](../../docs/running.md):

```sh
prose --harness claude --model haiku --native-profile claude-workspace-tools --permission-mode acceptEdits run examples/exposure-review/program.md complete
```

Other cases are `missing-eligibility` and `contradictory`. Provider usage may be incurred. No agent has executed or assessed this program; the [reference report](sample-results/report.md) is authored. For a separate assessment, use [the operating-report evaluator](../assess-report.md) with the actual result directory, original program and selected case.

The missing case withholds only the selected C2 eligibility binding while retaining the actual calculation's eligible flag and all observed results. The actual choice cannot supply the missing intended requirement. Known breaches elsewhere remain visible. The contradictory case adds producer assertions without changing the numerical evidence. Declared reading restrictions are not enforced filesystem isolation.

The [optional source calculation](model/README.md) was committed before a bounded public-source reproduction. Every numerical input, query, native row, reference and all 142 controls match the preceding study. New timing and explicitly rebound source/plan identities are recorded separately. The [receipt](receipt.json) identifies calculation and packet bytes; the reporting program permits arithmetic but does not rerun SQL.

`python3 scripts/check_exposure.py` checks fixed records, missing-binding behavior and adverse mutations without SQL or provider execution. This is an illustrative current-exposure review, not a full SA-CCR/EAD implementation or evidence of actual enforceability, settlement, collateral eligibility or operational savings.
