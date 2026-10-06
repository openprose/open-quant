# Contracts for quantitative operating work

The operating contracts turn supplied model records and house policy into reviewable reports. Their common [reporting requirements](../contracts/operating-report.md) handle scope, source support, coverage and execution boundaries. Specialized contracts add the domain question. One report may satisfy several contracts; composition does not require one agent or file per component.

| Use | Component | Caller supplies |
|---|---|---|
| Identify gaps in the model register | [Model inventory](../contracts/model-inventory.md) | Inventory, comparison population, identity rules and required fields. |
| Explain what a proposed revision affects | [Model change](../contracts/model-change.md) | Two revisions, comparison evidence, affected uses and materiality policy. |
| Account for performance checks and exceptions | [Model monitoring](../contracts/model-monitoring.md) | Expected observations, metrics, values, limits and response policy. |
| Determine what remains open | [Limitations and remediation](../contracts/limitations-and-remediation.md) | Issues, actions, use restrictions and closure criteria. |
| Identify input-quality and lineage gaps | [Model data](../contracts/model-data.md) | Source/input snapshots, transformations and quality criteria. |
| Explain the evidence for a calibration | [Calibration review](../contracts/calibration-review.md) | Targets, fitted values, conventions, diagnostics and tolerance. |

For example, a periodic model review can compose monitoring with limitations and remediation. A change review can compose model change, model data and calibration review. Adopt only components relevant to the intended result and bind their inputs explicitly. A caller can require a report that identifies missing data, or a supported substantive conclusion that cannot be reached without that data; state which obligation is intended.

The [monitoring example](../examples/monitoring-review/README.md) provides a small, synthetic composition. It contains authored cases and mechanically checked reference arithmetic, not a recorded model execution. The existing [SOFR decision example](../examples/sofr-curve/program.md) is unchanged.

## Public foundations and scope

Checked October 6, 2026. These are Open Quant's reusable reporting requirements, not regulator-issued templates. House thresholds, schedules, identifiers, materiality and approval rules remain caller inputs.

[SR 26-2](https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm) superseded SR 11-7 in April 2026. Its [guidance](https://www.federalreserve.gov/frrs/guidance/supervisory-guidance-on-model-risk-management.htm) provides relevant context: section IV addresses development and use; section V discusses validation and monitoring; section VI covers governance, inventory and documentation; section VII addresses vendor products. Applicability is risk-based, principally for banking organizations above $30 billion, with stated exceptions. It is supervisory guidance, not itself an enforceable documentation standard. Agentic AI is outside its model scope; our application here concerns the quantitative models being documented.

The components support preparing evidence for these activities. They do not establish regulatory compliance, independent validation, authorization to operate, or measured operating-cost savings. Domain interpretation, institution-specific acceptance and operational action remain distinct from report completion.
