# Public Black pricing-methodology example

The same [documentation contract](../../contracts/documentation.md) used for the SOFR and credit documents applies to a different model family. This example explains a synthetic European-option pricing method, its native mappings and the limits of numerical agreement. It reuses the retained implementation-review source and observations without another financial calculation.

From the source checkout, with an authenticated harness configured through [the running guide](../../docs/running.md):

```sh
prose run examples/pricing-methodology/program.md complete
prose run examples/pricing-methodology/assess.md results/pricing-methodology/YOUR-RUN complete
```

Replace `YOUR-RUN` with the actual returned result directory. Each command is a separate model invocation. `baseline-only` selects the same method and requirements with nine native case observations and the invalid-input observations withheld. Known source mappings remain available; neither source code nor theoretically correct values establish those missing historical observations. The authored reference covers `complete` only.

The [requirements](requirements.md) request a full document and supporting section plan, choices, citation audit, readiness and result record. [Reference artifacts](sample-results/result.md) are author-prepared, not an observed executor result. [Review cases](../../tests/cases/pricing-methodology.md) state intended distinctions; fixed numeric/identity checks do not qualify agent execution or assessment.

No new contract definition, financial model, registry publication or institutional approval is introduced. The source example remains outside the component package. This third methodology document does not change the separately scoped [two-model collection](../documentation-library/README.md).
