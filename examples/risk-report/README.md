# Explain a day's movement and its stress exposure

This synthetic risk report composes P&L explanation, scenario review and sensitivity interpretation. The daily book gains USD5,000, but the approximate components explain USD8,000; the USD−3,000 residual stays visible. Separate stress scenarios show why an assumed hedge and a sum of single-factor responses cannot replace the requested unmitigated joint result.

| Case | Distinction |
|---|---|
| complete | Full evidence supports an adverse P&L reconciliation and two unmitigated scenario breaches. |
| missing | Missing carry and a missing joint-scenario position leave those full results unresolved, while a separately supported scenario breach remains adverse. |
| contradictory | Producer statements disagree with the components, unmitigated scenarios and assumed-only hedge record. |

With an authenticated runtime from [the run guide](../../docs/running.md):

```sh
prose --harness claude --model haiku --native-profile claude-workspace-tools --permission-mode acceptEdits run examples/risk-report/program.md complete
```

Other case names select their corresponding packet. These calls can incur provider usage; no case has been executed by an agent in this expansion. Use [the common report evaluator](../assess-report.md) with an actual output and its original case.

[The reference report](sample-results/report.md) is authored. `node scripts/check_risk_report.mjs` checks the fixture's explicit arithmetic, identities, coverage and policy limits; it does not assess prose, validate a pricing model or establish causal factor attribution. No fixture is a trading recommendation or an actual bank result.

## Case interpretation

These notes compare the authored cases; they are not part of the complete-case reference report or permitted evidence for a selected-case execution.

In missing, P2 carry is unavailable. Known components subtotal +USD7,600, but a −USD2,600 difference against that subtotal is not the complete unexplained residual. The complete explanation remains unresolved; do not fill the carry gap with zero or borrow another packet's observation.

In missing, joint lacks P2. The available P1 subset loses USD45,000, but the full joint result, its interaction comparison and its after-hedge result are unresolved. Do not infer P2 or a full-book limit finding from that subset. Rates still has complete evidence of a breach, so missing joint evidence does not support an overall all-clear.

In contradictory, the producer's USD5,000 explanation conflicts with the +USD8,000 component calculation. Its all-clear scenario statement conflicts with rates and joint, and its hedge-executed statement conflicts with H1's assumed-only record. Preserve both the statements and contradictory evidence. They are not permissions or replacement observations.
