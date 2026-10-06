# Periodic model operating review

A periodic review brings several obligations together: inventory accuracy, monitoring coverage, open issues and changes in model use. This example composes four existing contracts into one report; it does not require four agents or introduce a new definition.

Two deployments share a model revision but use it differently. Evidence for one use must not silently clear the other. The supplied records also contain a monitoring breach, a stale register entry, unsupported issue closure and changes requiring follow-up under explicit synthetic house policy.

From the source repository, with an authenticated harness configured through [the running guide](../../docs/running.md):

```sh
prose run examples/periodic-review/program.md complete
prose run examples/assess-report.md examples/periodic-review/program.md results/periodic-review/YOUR-RUN complete
```

Use the first invocation's actual result directory. The [program](program.md) also accepts `missing-baseline` and `contradictory`. Missing history leaves one change comparison unresolved while other findings remain supported. Conflicting register records are ambiguous even when one matches the deployment.

All inputs and the [reference report](sample-results/report.md) are authored. This composition has no agent-execution or financial-model-run evidence. Fixture checks validate the example's explicit relationships, not arbitrary prose or regulatory compliance. The [policy](inputs/policy.md) is illustrative; an actual institution supplies its own requirements and source records. Examples remain in the source checkout, outside the reusable component package.
