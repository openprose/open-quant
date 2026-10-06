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
| Review implementation against its documented method | [Implementation review](../contracts/implementation-review.md) | Method conventions, exact implementation, required tests, observations and acceptance criteria. |
| Review dependence inputs and adjustments | [Dependence review](../contracts/dependence-review.md) | Variables and order, dependence inputs, estimation populations, joint diagnostics, intended use and adjustment criteria. |
| Review simulation precision and assumptions | [Simulation review](../contracts/simulation-review.md) | Target quantity, sampling design, uncertainty method, observations and precision criteria. |
| Explain differences between valuations | [Valuation comparison](../contracts/valuation-comparison.md) | Positions, prices, source provenance, conventions and tolerance. |
| Compare predictions with observed outcomes | [Outcomes analysis](../contracts/outcomes-analysis.md) | Dated predictions/outcomes, pairing rules, metrics and evaluation scope. |
| Account for risk-model backtest exceptions | [Backtesting](../contracts/backtesting.md) | Forecasts, outcome series, timing, sign conventions and exception policy. |
| Explain response to input changes | [Sensitivity review](../contracts/sensitivity-review.md) | Base and perturbed results, shock definitions and normalization. |
| Interpret a scenario set | [Scenario review](../contracts/scenario-review.md) | Scenarios, base case, portfolio, horizons and assumed actions. |
| Reconcile an explained P&L movement | [P&L explanation](../contracts/pnl-explanation.md) | A defined total, explanatory components, exclusions and tolerance. |
| Assess available vendor-model evidence | [Vendor model review](../contracts/vendor-model-review.md) | Product/version, local configuration, vendor claims and local observations. |

For example, a periodic model review can compose monitoring with limitations and remediation. A change review can compose model change, model data and calibration review. Adopt only components relevant to the intended result and bind their inputs explicitly. A caller can require a report that identifies missing data, or a supported substantive conclusion that cannot be reached without that data; state which obligation is intended.

## Worked compositions

These operating reports have authored references and deterministic fixture checks. They have not been executed by an agent in this expansion. The original [SOFR decision note](../examples/sofr-curve/program.md) has separately retained CLI evidence; that does not qualify these new compositions.

| Example | Composed requirements | Distinction to inspect |
|---|---|---|
| [Monitoring](../examples/monitoring-review/README.md) | Monitoring, limitations and remediation | An adverse finding can be the correct result of fulfilled reporting. |
| [Valuation](../examples/valuation-review/README.md) | Valuation comparison, model data | Offsetting differences do not remove position-level exceptions. |
| [Backtesting](../examples/backtesting-review/README.md) | Backtesting, outcomes analysis | Observed exceedances differ from policy treatment of missing data. |
| [SOFR change](../examples/sofr-change-review/README.md) | Model change, sensitivity review | Adding a locality requirement changes the finding without changing evidence. |
| [SOFR calibration](../examples/calibration-review/README.md) | Calibration review, model data | Rounded displays, missing instruments and conflicting records limit a fit conclusion. |
| [Vendor inventory](../examples/vendor-inventory-review/README.md) | Model inventory, vendor review | Register accuracy and local-test support are separate findings for an exact deployment. |
| [Risk report](../examples/risk-report/README.md) | P&L explanation, scenario review, sensitivity review | Residuals, joint effects and assumed actions remain distinct. |
| [Outcomes](../examples/outcomes-review/README.md) | Outcomes analysis, model data | A comparison can reverse when both models use the same observations. |
| [Implementation](../examples/implementation-review/README.md) | Implementation review, model description | Passing parity or one baseline does not establish correct price conventions. |
| [Selection history](../examples/selection-review/README.md) | Outcomes analysis, model data | A newly selected evaluation winner does not independently confirm the frozen original candidate. |
| [Dependence](../examples/dependence-review/README.md) | Dependence review, model data | Valid pairs, joint validity, observation populations and exposure identity are distinct. |
| [Simulation](../examples/simulation-review/README.md) | Simulation review, implementation review | A small standard error cannot clear dependent sampling or a different target. |

The SOFR examples use retained historical calculations; calibration also has a fresh numerical reproduction receipt. The implementation and simulation examples use freshly observed calculations on synthetic option inputs. Dependence review uses observed synthetic matrix calculations; selection review uses a fixed synthetic score replicate. Other inputs are authored synthetic records. Case selection, house policy and permissions are explicit in each program. Use [the common assessment entry point](../examples/assess-report.md) for an actual operating report, with its original program and selected case or mode.

Implementation review also has [authored distinguishing cases](../tests/cases/operating-reports.md#implementation-review). Its numerical observations establish finite adapter behavior, not agent qualification. Calibration fit, mathematical consistency and reference agreement remain separate findings.

## Public foundations and scope

Checked October 6, 2026. These are Open Quant's reusable reporting requirements, not regulator-issued templates. House thresholds, schedules, identifiers, materiality and approval rules remain caller inputs.

[SR 26-2](https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm) superseded SR 11-7 in April 2026. Its [guidance](https://www.federalreserve.gov/frrs/guidance/supervisory-guidance-on-model-risk-management.htm) provides relevant context: section IV addresses development and use; section V discusses validation and monitoring; section VI covers governance, inventory and documentation; section VII addresses vendor products. Applicability is risk-based, principally for banking organizations above $30 billion, with stated exceptions. It is supervisory guidance, not itself an enforceable documentation standard. Agentic AI is outside its model scope; our application here concerns the quantitative models being documented.

The components support preparing evidence for these activities. They do not establish regulatory compliance, independent validation, authorization to operate, or measured operating-cost savings. Domain interpretation, institution-specific acceptance and operational action remain distinct from report completion.

[Basel CAP50](https://www.bis.org/committees/bcbs/basel-framework/standard/cap/50/inforce/2019-12-15/published/2019-12-15), particularly 50.3 and 50.6–50.8, provides context for valuation controls, model review and independent price verification. The valuation component prepares a comparison report; it does not establish the organizational independence or complete verification process discussed there. [SRP36](https://www.bis.org/committees/bcbs/basel-framework/standard/srp/36/inforce/2019-12-15/published/2019-12-15) addresses risk-data aggregation and reporting for systemically important banks; it is relevant context for population coverage and data quality, not a source for our synthetic thresholds. Local adoption and applicability require separate determination.

[Basel MAR32](https://www.bis.org/committees/bcbs/basel-framework/standard/mar/32/inforce/2023-01-01/published/2020-03-27) defines specific backtesting and P&L attribution requirements for the internal models approach. The P&L explanation contract is a caller-defined analytical bridge, not implementation of that regulatory test. In particular, preserving a residual is useful reporting but does not establish compliance with the test's statistical requirements.

## Dependence review

[Dependence review](../contracts/dependence-review.md) has [authored distinguishing cases](../tests/cases/dependence-review.md) and a [worked data composition](../examples/dependence-review/README.md). This brings the catalog to sixteen operating domains and twelve worked operating reports; it does not establish agent qualification. Compose it with model data for lineage questions, implementation review for method conformance, or simulation review for how dependence enters simulated results.

[R's correlation documentation](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/cor.html), Details, explains why pairwise-complete estimates can be non-PSD. [Nick Higham's correlation-matrix overview](https://nhigham.com/2020/04/14/what-is-a-correlation-matrix/) explains joint admissibility and constrained adjustment problems. These primary sources support the component's mathematical distinctions, not institutional acceptance rules. The illustrative thresholds remain caller policy; mathematical validity alone does not establish economic suitability.
