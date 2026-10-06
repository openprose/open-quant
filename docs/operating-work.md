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
| Reproduce selected quantitative results | [Model reproduction](../contracts/model-reproduction.md) | Exact source/input selection, environment, reference outputs, comparison policy and execution limits. |
| Review counterparty exposure | [Option consistency](../examples/option-consistency/README.md) | Calibration review, implementation review | Individual quote fit does not establish joint consistency; calculation assumptions cannot fill missing instrument terms. |
| [Counterparty exposure](../contracts/counterparty-exposure.md) | Exposure definition, horizons, netting-set mappings, recognition evidence, collateral allocations and calculation criteria. |
| Review credit-loss calculations | [Credit-loss review](../contracts/credit-loss-review.md) | Default probabilities, exposure/severity assumptions, loss timing, calculation evidence and criteria. |
| Review optimization results | [Optimization review](../contracts/optimization-review.md) | Exact problem and variable identities, candidate, constraints, native diagnostics and acceptance criteria. |
| Review implementation against its documented method | [Implementation review](../contracts/implementation-review.md) | Method conventions, exact implementation, required tests, observations and acceptance criteria. |
| Review dependence inputs and adjustments | [Dependence review](../contracts/dependence-review.md) | Variables and order, dependence inputs, estimation populations, joint diagnostics, intended use and adjustment criteria. |
| Review simulation precision and assumptions | [Simulation review](../contracts/simulation-review.md) | Target quantity, sampling design, uncertainty method, observations and precision criteria. |
| Review instrument cash-flow evidence | [Cash-flow review](../contracts/cashflow-review.md) | Selected terms, flow population, schedules, dates, conventions and review criteria. |
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
| [Backtesting statistics](../examples/backtest-statistics/README.md) | Backtesting, outcomes analysis | Equal exception counts do not establish equal timing; missing order limits verification without erasing aggregate calculations. |
| [Backtesting](../examples/backtesting-review/README.md) | Backtesting, outcomes analysis | Observed exceedances differ from policy treatment of missing data. |
| [SOFR change](../examples/sofr-change-review/README.md) | Model change, sensitivity review | Adding a locality requirement changes the finding without changing evidence. |
| [SOFR calibration](../examples/calibration-review/README.md) | Calibration review, model data | Rounded displays, missing instruments and conflicting records limit a fit conclusion. |
| [Vendor inventory](../examples/vendor-inventory-review/README.md) | Model inventory, vendor review | Register accuracy and local-test support are separate findings for an exact deployment. |
| [Risk report](../examples/risk-report/README.md) | P&L explanation, scenario review, sensitivity review | Residuals, joint effects and assumed actions remain distinct. |
| [Outcomes](../examples/outcomes-review/README.md) | Outcomes analysis, model data | A comparison can reverse when both models use the same observations. |
| [Historical availability](../examples/availability-review/README.md) | Model data, outcomes analysis | Equal errors do not establish available historical inputs; recorded selections and independently supported timing remain distinct. |
| [Implementation](../examples/implementation-review/README.md) | Implementation review, model description | Passing parity or one baseline does not establish correct price conventions. |
| [Cash flows](../examples/cashflow-review/README.md) | Cash-flow review, valuation comparison | Close aggregate values do not clear a required payment-date convention. |
| [Sensitivity precision](../examples/sensitivity-review/README.md) | Sensitivity review, implementation review | Small price errors can amplify into large derivative errors; missing unrounded observations remain missing. |
| [Counterparty exposure](../examples/exposure-review/README.md) | Counterparty exposure, implementation review | Correct arithmetic does not establish selected netting or collateral recognition; an actual eligibility choice does not supply a missing intended binding. |
| [Portfolio tail](../examples/portfolio-tail-review/README.md) | Credit-loss review, dependence review, scenario review | Equal expected loss does not establish equal tail loss; supported risk results and actual solver-allocation evidence remain separate. |
| [Credit loss](../examples/credit-loss-review/README.md) | Credit-loss review, implementation review | Bounded probabilities do not establish correct conditioning or loss timing; actual parameters do not supply missing intended requirements. |
| [Optimization](../examples/optimization-review/README.md) | Optimization review, implementation review | Native success, original feasibility and supported optimality are separate; missing candidates remain unknown. |
| [Selection history](../examples/selection-review/README.md) | Outcomes analysis, model data | A newly selected evaluation winner does not independently confirm the frozen original candidate. |
| [Dependence](../examples/dependence-review/README.md) | Dependence review, model data | Valid pairs, joint validity, observation populations and exposure identity are distinct. |
| [Simulation](../examples/simulation-review/README.md) | Simulation review, implementation review | A small standard error cannot clear dependent sampling or a different target. |

The SOFR examples use retained historical calculations; calibration also has a fresh numerical reproduction receipt. The implementation and simulation examples use freshly observed calculations on synthetic option inputs. Dependence review uses observed synthetic matrix calculations; selection review uses a fixed synthetic score replicate. Cash-flow, sensitivity, optimization and credit-loss examples also use observed synthetic calculations. The historical-availability example uses observed SQLite selections over fixed synthetic input histories. Other inputs are authored synthetic records. Case selection, house policy and permissions are explicit in each program. Use [the common assessment entry point](../examples/assess-report.md) for an actual operating report, with its original program and selected case or mode.

Implementation review also has [authored distinguishing cases](../tests/cases/operating-reports.md#implementation-review). Its numerical observations establish finite adapter behavior, not agent qualification. Calibration fit, mathematical consistency and reference agreement remain separate findings.

## Public foundations and scope

Checked October 6, 2026. These are Open Quant's reusable reporting requirements, not regulator-issued templates. House thresholds, schedules, identifiers, materiality and approval rules remain caller inputs.

[SR 26-2](https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm) superseded SR 11-7 in April 2026. Its [guidance](https://www.federalreserve.gov/frrs/guidance/supervisory-guidance-on-model-risk-management.htm) provides relevant context: section IV addresses development and use; section V discusses validation and monitoring; section VI covers governance, inventory and documentation; section VII addresses vendor products. Applicability is risk-based, principally for banking organizations above $30 billion, with stated exceptions. It is supervisory guidance, not itself an enforceable documentation standard. Agentic AI is outside its model scope; our application here concerns the quantitative models being documented.

The components support preparing evidence for these activities. They do not establish regulatory compliance, independent validation, authorization to operate, or measured operating-cost savings. Domain interpretation, institution-specific acceptance and operational action remain distinct from report completion.

[Basel CAP50](https://www.bis.org/committees/bcbs/basel-framework/standard/cap/50/inforce/2019-12-15/published/2019-12-15), particularly 50.3 and 50.6–50.8, provides context for valuation controls, model review and independent price verification. The valuation component prepares a comparison report; it does not establish the organizational independence or complete verification process discussed there. [SRP36](https://www.bis.org/committees/bcbs/basel-framework/standard/srp/36/inforce/2019-12-15/published/2019-12-15) addresses risk-data aggregation and reporting for systemically important banks; it is relevant context for population coverage and data quality, not a source for our synthetic thresholds. Local adoption and applicability require separate determination.

[Basel MAR32](https://www.bis.org/committees/bcbs/basel-framework/standard/mar/32/inforce/2023-01-01/published/2020-03-27) defines specific backtesting and P&L attribution requirements for the internal models approach. The P&L explanation contract is a caller-defined analytical bridge, not implementation of that regulatory test. In particular, preserving a residual is useful reporting but does not establish compliance with the test's statistical requirements.

## Dependence review

[Dependence review](../contracts/dependence-review.md) has [authored distinguishing cases](../tests/cases/dependence-review.md) and a [worked data composition](../examples/dependence-review/README.md). The current catalog has twenty operating domains and eighteen worked operating reports; these describe authored coverage, not agent qualification. Compose it with model data for lineage questions, implementation review for method conformance, or simulation review for how dependence enters simulated results.

[R's correlation documentation](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/cor.html), Details, explains why pairwise-complete estimates can be non-PSD. [Nick Higham's correlation-matrix overview](https://nhigham.com/2020/04/14/what-is-a-correlation-matrix/) explains joint admissibility and constrained adjustment problems. These primary sources support the component's mathematical distinctions, not institutional acceptance rules. The illustrative thresholds remain caller policy; mathematical validity alone does not establish economic suitability.

## Cash-flow review

[Cash-flow review](../contracts/cashflow-review.md) has [authored distinguishing cases](../tests/cases/cashflow-review.md). It preserves accrual terms, payment dates, flow identity, valuation inclusion and actual-payment evidence as separate questions. Compose it with valuation comparison for a valuation report or model data for lineage questions. A generated schedule is not a payment confirmation or a ledger reconciliation. The [worked valuation composition](../examples/cashflow-review/README.md) has complete, missing-schedule and contradictory packets; it remains agent-unqualified.

## Produce evidence before reviewing it

The [bounded SOFR reproduction program](../examples/sofr-reproduction/README.md) applies model-reproduction requirements to one explicitly authorized calculation. It is separate from the eighteen prepared-evidence report compositions above. A normal exit, complete evidence, numerical agreement and fulfillment of the reproduction/reporting program are distinct findings. Dependency setup and agent execution remain separately qualified; reproduction does not establish economic suitability or institutional acceptance.


## Optimization review

[Optimization review](../contracts/optimization-review.md) has [authored distinguishing cases](../tests/cases/optimization-review.md) for original constraint satisfaction, objective binding, numerical scaling, local/global conclusions and revised candidate artifacts. It composes existing reporting and numerical-evidence requirements. Pair it with model data for input lineage, dependence review for covariance diagnostics or implementation review for the numerical method. Reviewing a candidate does not authorize implementing it.

[The SLSQP reference](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-slsqp.html) documents stopping tolerance and returned multipliers; [OptimizeResult](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.OptimizeResult.html) describes native termination fields. These interface documents do not certify satisfaction of a caller's original problem or provide institution-specific approval rules. The [worked composition](../examples/optimization-review/README.md) retains all seven native outcomes and the rounded export in complete, missing-candidate and contradictory packets. The component and report remain agent-unqualified.


## Historical input review

The [historical-availability composition](../examples/availability-review/README.md) uses existing model-data and outcomes-analysis requirements. It preserves observation date, publication, local availability, revision order and metric population as caller bindings. Complete, missing-history and contradictory packets distinguish an observed selected record from evidence that it was eligible at a past decision cutoff. No additional definition or runtime capability is required; agent execution remains unqualified.


## Credit-loss review

[Credit-loss review](../contracts/credit-loss-review.md) adds explicit probability conditioning, horizon, exposure/severity and loss-timing requirements, with [authored distinguishing cases](../tests/cases/credit-loss-review.md). Compose it with model description for a method explanation, model data for lineage, implementation review for formula conformance, or outcomes analysis for empirical evaluation. A numerical loss calculation alone does not establish borrower performance or an accounting reserve.

QuantLib's [default-probability interface](https://github.com/lballabio/QuantLib/blob/v1.43/ql/termstructures/defaulttermstructure.hpp) and [flat-hazard implementation](https://github.com/lballabio/QuantLib/blob/v1.43/ql/termstructures/credit/flathazardrate.hpp) illustrate the distinction between survival, cumulative default probability and hazard. Those definitions do not select a probability basis, institutional loss method or acceptance policy. The [worked composition](../examples/credit-loss-review/README.md) retains all six observed constructions and four intervals in complete, missing-severity and contradictory packets. It remains agent-unqualified.


## Portfolio loss distributions

The [portfolio-tail composition](../examples/portfolio-tail-review/README.md) combines existing credit-loss, dependence and scenario requirements. Six proposed joint tables distinguish correlation-matrix definiteness from compatibility with specified default probabilities. Sixteen risk summaries preserve mean loss, exact and native quantiles, expected shortfall and alternative conditional-tail means. Complete, missing-allocation and contradictory packets retain supported mathematical results separately from evidence about an actual solver candidate. No additional definition or package change is needed; agent execution remains unqualified.

## Exception frequency and timing

The [statistical-evidence composition](../examples/backtest-statistics/README.md) reuses backtesting and its adopted reporting requirements. Six constructed sequences retain separate excess-frequency tests, probability intervals and conditional clustering calculations. Complete, missing-order and contradictory packets distinguish a reported statistic from evidence supporting its sequence. The example supplements the earlier P&L/availability case; no new definition or package change is needed. It remains agent-unqualified.

## Counterparty exposure

[Counterparty-exposure review](../contracts/counterparty-exposure.md) binds the measure, recognized groups and collateral offsets, with [authored distinguishing cases](../tests/cases/counterparty-exposure.md). It preserves the difference between stipulated assumptions, supported institutional recognition and missing facts. Current exposure is not automatically future exposure or regulatory EAD. The definition composes existing reporting and numerical-evidence requirements; it does not supply a financial formula, legal opinion or permission to move collateral.

The [Basel Framework CRE52 version in force January 1, 2023](https://www.bis.org/committees/bcbs/basel-framework/standard/cre/52/inforce/2023-01-01/published/2020-06-05), paragraphs 52.1 and 52.6–52.12, illustrates why netting-set scope and collateral recognition matter. This contract does not implement that standard or establish its jurisdictional applicability. The caller supplies the method and governing requirements.

The [worked exposure composition](../examples/exposure-review/README.md) retains nine SQL constructions over six trades and six collateral records. Its three cases separate actual choices from selected requirements, including one unavailable eligibility binding. A report can retain known breaches and conditional calculations without inventing recognition evidence. The reference is authored and agent execution remains unqualified.

## Option quote consistency

The [option reporting composition](../examples/option-consistency/README.md) reuses calibration, implementation and numerical-evidence requirements. It preserves ten quote inversions, twelve strategy payoffs and 36 spread-dependent costs. A close fit can coexist with a joint-price violation; a negative portfolio cost can coexist with a possible terminal loss. The missing-underlying packet preserves calculations while limiting their applicability to selected instruments. No new definition is required, and agent execution remains unqualified.
