# Review vendor evidence without losing deployment identity

This synthetic example composes model inventory and vendor-model review into one operating report. Two deployments share a model and display name but use different versions and configurations. Product-level statements and tests of an earlier configuration cannot silently qualify the current deployment.

The complete packet deliberately contains exceptions: a stale register entry, an unregistered deployment, an unmatched retired record, a mismatched local test and an observed threshold breach. Missing and contradictory packets separately remove a local test or add an ambiguous register match. The report must account for them; it does not repair them.

With an authenticated runtime from [the run guide](../../docs/running.md):

```sh
prose --harness claude --model haiku --native-profile claude-workspace-tools --permission-mode acceptEdits run examples/vendor-inventory-review/program.md complete
```

Select missing or contradictory for the other cases. These calls can incur provider usage; none has been run in this expansion. Use [the common evaluator](../assess-report.md) for an actual report, preserving its case selection.

[The reference report](sample-results/report.md) is authored. `node scripts/check_vendor_inventory.mjs` checks the fixture's explicit identities, coverage, dates and numerical limits; it does not assess prose, perform independent validation or verify real vendor claims. The fictional product names do not identify actual products or institutions.

## Case interpretation

These notes compare the authored cases; they are not part of the complete-case reference report or permitted evidence for a selected-case execution.

The contradictory packet adds R1b with version 2.3: D1's register match is now ambiguous, even though one of its two records agrees with the deployment. T1 still supports D1's exact-version local check; the register conflict does not erase that separate evidence.

In missing, T1 is unavailable and D1's local check is unresolved.

Complete and contradictory each yield one supported local check, one unresolved check and one adverse check across three deployments. Missing yields two unresolved and one adverse.
