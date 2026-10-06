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
| Explain differences between valuations | [Valuation comparison](../contracts/valuation-comparison.md) | Positions, prices, source provenance, conventions and tolerance. |
| Compare predictions with observed outcomes | [Outcomes analysis](../contracts/outcomes-analysis.md) | Dated predictions/outcomes, pairing rules, metrics and evaluation scope. |
| Account for risk-model backtest exceptions | [Backtesting](../contracts/backtesting.md) | Forecasts, outcome series, timing, sign conventions and exception policy. |
| Explain response to input changes | [Sensitivity review](../contracts/sensitivity-review.md) | Base and perturbed results, shock definitions and normalization. |
| Interpret a scenario set | [Scenario review](../contracts/scenario-review.md) | Scenarios, base case, portfolio, horizons and assumed actions. |
| Reconcile an explained P&L movement | [P&L explanation](../contracts/pnl-explanation.md) | A defined total, explanatory components, exclusions and tolerance. |
| Assess available vendor-model evidence | [Vendor model review](../contracts/vendor-model-review.md) | Product/version, local configuration, vendor claims and local observations. |

For example, a periodic model review can compose monitoring with limitations and remediation. A change review can compose model change, model data and calibration review. Adopt only components relevant to the intended result and bind their inputs explicitly. A caller can require a report that identifies missing data, or a supported substantive conclusion that cannot be reached without that data; state which obligation is intended.

The [monitoring example](../examples/monitoring-review/README.md) provides a small, synthetic composition. It contains authored cases and mechanically checked reference arithmetic, not a recorded model execution. The existing [SOFR decision example](../examples/sofr-curve/program.md) is unchanged.

The [valuation example](../examples/valuation-review/README.md) composes valuation comparison with model data. It distinguishes position-level exceptions from offsetting totals and usable quotes from missing, stale or incompatible evidence. It is also synthetic and not model-executed.

The [backtesting example](../examples/backtesting-review/README.md) preserves observed exceedances separately from policy exceptions caused by unavailable data. Its separate case files also allow an experiment to stage one selected case without the alternatives. Five illustrative days do not establish an annual regulatory backtest.

The [SOFR change review](../examples/sofr-change-review/README.md) reuses the existing historical model evidence. It composes change and sensitivity review, then optionally adds a locality requirement. The numerical finding changes because the selected requirements change, while the model evidence remains fixed. The original short decision-note program is unaffected.

The [calibration review](../examples/calibration-review/README.md) uses freshly reproduced per-instrument SOFR evidence. It distinguishes selected and excluded instruments, missing item-level support, rounded displays and conflicting source records. The report itself remains unexecuted by an agent.

The [vendor/inventory example](../examples/vendor-inventory-review/README.md) preserves deployment identity across shared model names, versions and local configurations. It separates register accuracy, vendor assertions and the evidence for narrow local checks. These synthetic records are authored; the report has not been run by an agent.

## Public foundations and scope

Checked October 6, 2026. These are Open Quant's reusable reporting requirements, not regulator-issued templates. House thresholds, schedules, identifiers, materiality and approval rules remain caller inputs.

[SR 26-2](https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm) superseded SR 11-7 in April 2026. Its [guidance](https://www.federalreserve.gov/frrs/guidance/supervisory-guidance-on-model-risk-management.htm) provides relevant context: section IV addresses development and use; section V discusses validation and monitoring; section VI covers governance, inventory and documentation; section VII addresses vendor products. Applicability is risk-based, principally for banking organizations above $30 billion, with stated exceptions. It is supervisory guidance, not itself an enforceable documentation standard. Agentic AI is outside its model scope; our application here concerns the quantitative models being documented.

The components support preparing evidence for these activities. They do not establish regulatory compliance, independent validation, authorization to operate, or measured operating-cost savings. Domain interpretation, institution-specific acceptance and operational action remain distinct from report completion.

[Basel CAP50](https://www.bis.org/committees/bcbs/basel-framework/standard/cap/50/inforce/2019-12-15/published/2019-12-15), particularly 50.3 and 50.6–50.8, provides context for valuation controls, model review and independent price verification. The valuation component prepares a comparison report; it does not establish the organizational independence or complete verification process discussed there. [SRP36](https://www.bis.org/committees/bcbs/basel-framework/standard/srp/36/inforce/2019-12-15/published/2019-12-15) addresses risk-data aggregation and reporting for systemically important banks; it is relevant context for population coverage and data quality, not a source for our synthetic thresholds. Local adoption and applicability require separate determination.

[Basel MAR32](https://www.bis.org/committees/bcbs/basel-framework/standard/mar/32/inforce/2023-01-01/published/2020-03-27) defines specific backtesting and P&L attribution requirements for the internal models approach. The P&L explanation contract is a caller-defined analytical bridge, not implementation of that regulatory test. In particular, preserving a residual is useful reporting but does not establish compliance with the test's statistical requirements.
