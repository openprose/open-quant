# Quantitative operating contracts

These are reusable Markdown requirements, not a scheduler or a schema that the CLI interprets. The selected OpenProse kernel supplies language semantics. Each caller identifies the inputs, adopted requirements and permitted result location.

Use [model decision](model-decision.md) for a bounded note and [documentation](documentation.md) for a complete model document. Both compose [claim evidence](claim-evidence.md) and [institutional facts](institutional-facts.md). The full-document contract also composes [model description](model-description.md) and [numerical evidence](numerical-evidence.md); these can be used independently for smaller tasks. [Assessment](assessment.md) examines a supplied result against its selected requirements without rewriting the subject.

The [SOFR example](../examples/sofr-curve/program.md) is one binding of the decision-note contract. Model-specific facts and house conventions belong in the caller's inputs, not these definitions. Contracts need not map one-to-one to agents or files.

[Choosing and composing contracts](../docs/composition.md) shows the reusable parts and their caller bindings.

[Implementation review](implementation-review.md) examines evidence that a particular implementation follows its documented method and conventions. It distinguishes test execution, property checks, reference agreement and coverage. Compose it with calibration or change review when those questions are also in scope.

[Operating-work components](../docs/operating-work.md) cover model inventory, change impact, monitoring, limitations and remediation, model data, calibration evidence, valuation comparison, outcomes analysis, backtesting, sensitivities, scenarios, P&L explanation and vendor-model evidence. They compose shared [reporting requirements](operating-report.md). The [monitoring example](../examples/monitoring-review/README.md) illustrates adverse findings without confusing them with report failure.

[Simulation review](simulation-review.md) examines whether a supplied estimate targets the requested quantity and whether its reported uncertainty respects the sampling design. Compose it with implementation review when mapping conventions or numerical behavior are also in scope. The [worked simulation report](../examples/simulation-review/README.md) distinguishes precision from target correctness.

[Dependence review](dependence-review.md) examines joint admissibility, estimation populations, exposure alignment and adjustments. Compose it with data, implementation or simulation review when those outputs are needed. A valid matrix alone does not establish suitability for its intended use. The [worked data composition](../examples/dependence-review/README.md) separates known matrix violations from missing observation memberships.
