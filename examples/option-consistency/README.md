# Review option fit and consistency

This source-only example composes [calibration review](../../contracts/calibration-review.md) and [implementation review](../../contracts/implementation-review.md). Every individual quote fits closely, yet the joint prices can admit a negative-cost position with nonnegative payoff. Uneven strikes also make a naive equal-wing alarm misleading.

With an authenticated runtime from [the run guide](../../docs/running.md):

```sh
prose --harness claude --model haiku --native-profile claude-workspace-tools --permission-mode acceptEdits run examples/option-consistency/program.md complete
```

Other cases are `missing-underlying` and `contradictory`. Provider usage may be incurred. No agent has executed or assessed this program; the [reference report](sample-results/report.md) is authored. Use [the operating-report evaluator](../assess-report.md) for a separate assessment with the actual result directory, original program and selected case.

The missing case withholds only one selected instrument's underlying identity. It retains all prices, native fits, strategy weights, mathematical payoffs and costs. An assumption inside a calculation cannot fill the missing instrument fact. The contradictory case adds unsupported producer assertions without changing observations. Reading restrictions are instructions, not enforced filesystem isolation.

The [optional source calculation](model/README.md) was committed before a bounded reproduction. All numerical observations and 111 controls match the preceding study; new timing and explicitly rebound source/plan identities are retained separately. The [receipt](receipt.json) identifies source and packet bytes. The reporting program permits arithmetic without rerunning QuantLib.

`python3 scripts/check_option_consistency.py` checks fixed records and adverse mutations without native inversion or provider calls. This is not an arbitrary prose evaluator, a market-arbitrage detector or evidence of operational savings.
