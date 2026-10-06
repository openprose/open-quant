# Document a synthetic credit-loss model

This second full-methodology example uses the same [documentation contract](../../contracts/documentation.md) as the [SOFR document](../sofr-documentation/README.md), with different model inputs and public requirements. It reuses existing code, observed calculations and a numerical receipt; it introduces no financial calculation or library definition.

From the source checkout, with an authenticated harness configured through [the running guide](../../docs/running.md):

```sh
prose run examples/credit-methodology/program.md public-methodology
prose run examples/credit-methodology/assess.md results/credit-methodology/YOUR-RUN public-methodology
```

Use the first invocation's actual result directory. Each invocation has separate model usage. The program produces document.md, reviews.md and result.md; the generic two-file operating-report assessment is not its interface. The [authored reference](sample-results/document.md) illustrates public-methodology content and has [supporting records](sample-results/reviews.md) and an [identity/result record](sample-results/result.md). This execution and assessment route remains agent-unqualified.

## Change the required outcome

`public-methodology` requires a complete account of the supplied model and disclosure of missing institutional facts. `institutional-records` additionally adopts [three factual-entry requirements](institutional.md). The evidence is unchanged and supplies none of those records. Gap disclosure can therefore satisfy D8 while the additional I1–I3 content remains unmet. Useful partial documentation must not be reported as fulfillment of the larger agreement. This comparison is part of the guide, not a reference output for the second mode.

The underlying real-world facts remain unknown; the missing entries are known limitations of the document. Neither mode approves the model or establishes a complete institutional or regulatory submission. A negative subject finding can be correct while an assessment is incomplete, so inspect its coverage too.

The [source register](inputs/sources.md) scopes the existing calculation evidence. Reporting does not authorize numerical reproduction; optional reproduction belongs to the [separate calculation guide](../credit-loss-review/model/README.md). Examples remain source-only and the component package is unchanged. Offline checks verify specific identities, numerical cells and authored mappings, not arbitrary prose fulfillment.
