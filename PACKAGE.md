# Open Quant contracts

Contract authoring is expressing intent by composing requirements. Open Quant provides reusable requirements for quantitative model documentation and operating work. Supply the model evidence, applicable house requirements, permitted tools and output scope in your own program, and adopt the components relevant to its result.

This package contains contract definitions, its manifest and the license. It does not contain example inputs, financial model code, development tests, a kernel or an agent harness. The selected OpenProse runtime supplies the kernel and execution capabilities.

| Purpose | Contracts |
|---|---|
| Describe and document | [Model description](contracts/model-description.md), [decision note](contracts/model-decision.md), [full documentation](contracts/documentation.md) |
| Ground a report | [Claim evidence](contracts/claim-evidence.md), [numerical evidence](contracts/numerical-evidence.md), [institutional facts](contracts/institutional-facts.md), [operating report](contracts/operating-report.md) |
| Assess a result | [Assessment](contracts/assessment.md) |
| Review implementation and use | [Implementation](contracts/implementation-review.md), [simulation](contracts/simulation-review.md), [inventory](contracts/model-inventory.md), [vendor evidence](contracts/vendor-model-review.md) |
| Review inputs and changes | [Model data](contracts/model-data.md), [calibration](contracts/calibration-review.md), [change impact](contracts/model-change.md) |
| Monitor and follow up | [Monitoring](contracts/model-monitoring.md), [limitations and remediation](contracts/limitations-and-remediation.md) |
| Explain values and results | [Valuation comparison](contracts/valuation-comparison.md), [P&L explanation](contracts/pnl-explanation.md), [outcomes](contracts/outcomes-analysis.md) |
| Examine risk evidence | [Backtesting](contracts/backtesting.md), [sensitivities](contracts/sensitivity-review.md), [scenarios](contracts/scenario-review.md) |

The default export is the full-documentation contract. Named exports locate individual definitions; importing a package does not execute them. A report may satisfy several contracts without requiring a separate agent or file for each. A fulfilled report can identify adverse findings or missing evidence; it does not thereby approve a model or establish regulatory compliance.

## Run an example

Runnable examples and their inputs live in the [complete source repository](https://github.com/openprose/open-quant), separately from this component package. The [SOFR example checkpoint](https://github.com/openprose/open-quant/tree/6772948763b736e87d4661fd4d1565ce8e841751) contains its own contracts, evidence and instructions. Clone that revision and follow its README for the demonstration. It uses the definitions in that checkout; a package fetched elsewhere does not silently replace them.

That checkpoint retains one bounded CLI development campaign. The complete attendee setup, broader report examples and reliability claims remain unqualified; see its [evidence and limits](https://github.com/openprose/open-quant/blob/6772948763b736e87d4661fd4d1565ce8e841751/docs/qualification.md). Selecting a newer source checkpoint or package creates a new version to inspect and qualify.

Owned definitions are provided under the included [MIT license](LICENSE). Preserve the exact package identity from its publication receipt when adopting it in your own program.
