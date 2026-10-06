# Quantitative operating contracts

These are reusable Markdown requirements, not a scheduler or a schema that the CLI interprets. The selected OpenProse kernel supplies language semantics. Each caller identifies the inputs, adopted requirements and permitted result location.

Use [model decision](model-decision.md) for a bounded note and [documentation](documentation.md) for a complete model document. Both compose [claim evidence](claim-evidence.md) and [institutional facts](institutional-facts.md). The full-document contract also composes [model description](model-description.md) and [numerical evidence](numerical-evidence.md); these can be used independently for smaller tasks. [Assessment](assessment.md) examines a supplied result against its selected requirements without rewriting the subject.

The [SOFR example](../examples/sofr-curve/program.md) is one binding of the decision-note contract. Model-specific facts and house conventions belong in the caller's inputs, not these definitions. Contracts need not map one-to-one to agents or files.

[Choosing and composing contracts](../docs/composition.md) shows the reusable parts and their caller bindings.

[Operating-work components](../docs/operating-work.md) cover model inventory, change impact, monitoring, limitations and remediation, model data, calibration evidence, valuation comparison, outcomes analysis, sensitivities, scenarios, P&L explanation and vendor-model evidence. They compose shared [reporting requirements](operating-report.md). The [monitoring example](../examples/monitoring-review/README.md) illustrates adverse findings without confusing them with report failure.
