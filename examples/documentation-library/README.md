# One library, two model documentation contracts

This example composes the existing [SOFR](../sofr-documentation/README.md) and [credit-loss](../credit-methodology/README.md) documentation programs. It requests two complete methodology documents with their supporting records and a collection index. It adds no component definition, scheduler or runtime feature.

Both models use the same documentation contract. Their inputs, requirements and findings remain separate. The collection demonstrates how a reusable contract can apply across a model inventory without requiring identical content or treating one model's evidence as support for another.

## Run and inspect

From the source repository with the [documented authenticated runtime](../../docs/running.md):

```sh
prose --harness claude --model haiku --native-profile claude-workspace-tools --permission-mode acceptEdits run examples/documentation-library/program.md complete
```

Select `missing-locality` instead to withhold the SOFR perturbation record. Credit remains in `public-methodology` mode in both cases. The selected evidence, restrictions and existing output locations come from each child program. This example does not copy model inputs or reexecute their calculations.

The executor returns an index and collection result under `results/documentation-library/`, pointing to fresh child outputs under `results/sofr-documentation/` and `results/credit-methodology/`. Inspect those actual files. No result directory exists until execution produces one; the authored child references are illustrations, not results to import.

For a separate assessment, replace YOUR-RUN with the actual collection directory and retain the original SOFR selection:

```sh
prose --harness claude --model haiku --native-profile claude-workspace-tools --permission-mode acceptEdits run examples/documentation-library/assess.md results/documentation-library/YOUR-RUN complete
```

Assessment is another model invocation with its own usage. The execution strategy is unspecified: two adopted programs do not require two processes or two agents. Supplying a larger scope may increase context, work and cost; none has been measured here.

## What to examine

Both entries must remain visible, with their own requirement and evidence identities. SOFR D5 and credit D5 are different requirements despite their shared local label. The missing-locality selection cannot supply the mandatory SOFR response through disclosure alone. Credit's public institutional-gap disclosure has a different obligation; no institutional-records mode is adopted by this collection.

An index can accurately describe incomplete documentation. That makes the index useful but does not fulfill this collection's requirement to produce both documents. A collection asking only to inventory existing results would be a different contract.

[Authored review cases](../../tests/cases/documentation-library.md) cover the relevant distinctions. No agent has executed or assessed this composition. Static source checks establish reference integrity and preservation, not document quality, complete semantic coverage, parallel safety, cost savings or a working attendee journey. The [qualification record](../../docs/qualification.md) maintains that boundary.
