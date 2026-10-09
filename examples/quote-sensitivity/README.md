# Quote risk and parameter risk

This example composes sensitivity and calibration review. One quote bump recalibrates a curve; one zero-rate bump holds the other parameter fixed. Both calculations can be correct while answering different questions. The report also distinguishes a missing field from missing substantive support.

The [program](program.md) reads one prepared evidence packet, produces report.md and result.md, and permits arithmetic/derivation within the supplied valuation relationship. It does not authorize curve calculation or require a particular workflow.

| Selection | Supplied difference |
|---|---|
| `complete` | Thirteen curve scenarios, twenty-six native values and twelve sensitivity summaries. |
| `missing-node-records` | Only quote_1_plus's explicit nodes and implied quotes are withheld; both fixed-instrument values remain. |
| `missing-independent-value` | The preceding fields plus that scenario's six-percent value and its quote_1 sensitivity summary are withheld. |
| `contradictory` | Complete numerical records plus five producer claims to assess. |

From the source root with the [documented authenticated runtime](../../docs/running.md):

```sh
prose --harness claude --model haiku --native-profile claude-workspace-tools --permission-mode acceptEdits run examples/quote-sensitivity/program.md complete
```

Replace complete with one selected case. For a separate assessment, use the [common entry](../assess-report.md) with the actual result and original selection:

```sh
prose --harness claude --model haiku --native-profile claude-workspace-tools --permission-mode acceptEdits run examples/assess-report.md examples/quote-sensitivity/program.md results/quote-sensitivity/YOUR-RUN complete
```

The [authored reference](sample-results/report.md) concerns complete only. In missing-node-records, the two fixed cash-flow values provide independent linear equations for both nodes under the supplied relationship. They are not independent data sources. With only the par value, q2 can remain identified while q1 is underdetermined. A second copy of the same value does not supply another equation. The reviewer must preserve error propagation and distinguish derived support from direct observations; these case explanations are not execution evidence.

[Public calculation source and plan](model/PLAN.md) describe a separately authorized numerical reproduction. One process retained thirteen native curves, twenty-six values and 110 controls. Reporting packets omit observer checks and analytical reference answers; the [receipt](receipt.json) records exact identities and projections. Neither native process success nor fixed-record tests establishes reporting or assessment fulfillment.

Offline inspection is `python3 scripts/check_quote_sensitivity.py`. It checks exact projections, fixed numerical relationships, recoverable and underdetermined cases, targeted corruptions and the authored table. [Interpretation cases](../../tests/cases/quote-sensitivity.md) remain unexecuted by a model. Agent behavior, fresh attendee execution, hedge performance and operating savings are unqualified.
