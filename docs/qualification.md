# Qualification status

The source-only [reproduction program](../examples/sofr-reproduction/README.md) adds a caller-bound request for fresh calculation evidence. Its helper now limits one calculation attempt, retains execution and comparison records separately, and refuses to accept matching partial output from failed or interrupted calculations. Twenty unit tests cover the existing controls and new local-process cases, including timeout, launch failure, missing or invalid results, changed inputs and numerical mismatch. These tests use tiny synthetic processes. A separately prespecified [SOFR calculation](../provenance/reproduction/2026-10-06-bounded.json) at source f07b037 completed in 2.62 seconds with unchanged source/input identities. Its result file is byte-identical to the retained reference and passes the unchanged numerical comparison. No provider call occurred; agent execution and assessment of the new program remain unperformed. The observed duration is not a performance comparison.

The library now has an [observed CLI-generated SOFR note](../examples/sofr-curve/observed-run/README.md) and separate assessment. The sample note remains an authored reference. Historical numerical results are imported calculations with explicit provenance. A separate October 6 numerical reproduction now matches them, conditional on the retained derived inputs; see the checkpoint below.

The offline checker verifies imported file identities, relative Markdown links, a fixed set of computed field correspondences and the scope of the included fixtures. Tests include missing fields, wrong values, swapped method meanings, unit mismatch and stale source identity. They exercise deterministic evidence checks, not general interpretation of natural-language contracts.

The development task records fresh-checkout and CLI preparation observations separately. A public first-run claim still requires the selected released executable, admitted/authenticated harness, observed kernel, actual model execution, inspected note and complete assessment. No comparison establishes superiority over equally informative plain instructions or another format.

Known deliberate limits: one model example with retained CLI execution; additional synthetic operating examples without model execution; finite authored evidence cases; individual run timings without a success-rate estimate; no independent financial review; no full-document acceptance; no institution-specific approval; no universal semantic validator. The SOFR brief preserves limitations in the supplied model comparison.

## October 5, 2026 preparation check

On macOS ARM64, an isolated npm installation of public CLI 0.15.0-rc.2 succeeded. The example's dry run resolved kernel-0.1.0-rc.1 (SHA-256 `6cd37fd568df61026688ca2e3f684dbf76e1a51fa8a67fbd832f6225bbb81cb7`). Without an installed admitted harness it reported HARNESS_UNAVAILABLE. Installing Claude Code 2.1.243 in a disposable prefix passed the executable version check; the subsequent dry run stopped at HARNESS_NEEDS_AUTH. No model started. No shared installation or credentials were changed. Runtime preparation therefore remains blocked on authentication for this route, and execution remains unqualified.

The repository checker and six offline tests pass, including seven labeled numerical evidence cases. These results concern deterministic checks only. The optional numerical reproduction helper correctly stopped at version preflight in the default Python 3.14.6 environment, which lacked the required numerical packages. It did not execute the model, install packages or create a result directory. The historical numerical results have not been newly reproduced in this task.

The component-first expansion adds model-description and numerical-evidence contracts, composed by the full-document contract. Six authored semantic cases illustrate their intended distinctions; no model has evaluated these cases in this task. The SOFR program and its retained inputs are unchanged. More reusable contracts do not establish more qualified model examples.

## October 6, 2026 bounded OpenAI development runs

Six sequential CLI invocations completed: two executions (ordinary and missing-evidence inputs) and four assessments (both results under original and clarified assessment requirements). They made 47 underlying SDK model requests. Requested model was `gpt-5.6-luna`; served snapshot and actual billed cost were not independently established. Reported token usage estimates total about USD0.066 at checked rates; this is not an invoice or a cost-per-success benchmark.

The released CLI remained 0.15.0-rc.2 with the same public kernel identity. Its generic Agents SDK 0.1.0 harness ran in an isolated research container, with provider transport retries disabled. The ordinary execution completed in 42.8 seconds and its content was accepted by both assessments. Evaluators correctly kept execution effects unresolved without a supplied trace. The coordinator separately retained unchanged source hashes and native events; no complete operating-system effect audit is claimed.

The missing-evidence executor disclosed absent locality measurements but claimed fulfillment. After a small clarification, the evaluator rejected that overall claim while preserving its positive findings on supported content. The baseline reassessment remained positive for content. This is a useful individual before/after observation, not a controlled estimate of improvement: the revised evaluator still emphasized missing field names in its remedy and omitted required subject-artifact hashes. Its assertion of complete assessment coverage was therefore too strong.

The separate contradiction case was prepared but not executed; the last two invocations tested the observed evaluator issue and baseline regression. No additional model calls remain in this campaign. The full-document and new component cases remain authored illustrations.

The preceding 47-file SOFR package passed an offline round trip through CLI source functions with a synthetic receipt. That result does not qualify subsequent expanded package bytes. A credential-free public registry listing returned HTTP503 during this campaign. No package was published or successfully fetched from production. Fresh attendee installation and the one-hour rehearsal remain outstanding.

## Operating-work expansion

| Example | Available evidence | What remains untested |
|---|---|---|
| SOFR decision note | Two CLI executions and four assessments in the bounded development campaign above. | Attendee route, broad reliability and full-document acceptance. |
| Monitoring and remediation | Authored report, three synthetic cases, explicit arithmetic and mutation checks. | Model execution and assessment of the composed report. |
| Valuation and model data | Authored report, four synthetic cases, price-scale and exception controls. | Model execution, source independence and actual valuation operations. |
| Backtesting review | Authored report, four synthetic cases, observed-versus-policy exception counts and timing controls. | Model execution, statistical adequacy and any complete regulatory test. |
| Cash-flow outcome comparison | Authored synthetic forecasts/outcomes, matched-population reversal and timing/coverage controls. | Agent execution, predictive performance, statistical significance and economic usefulness. |
| P&L and scenario report | Authored synthetic book, three cases, residual/interaction calculations and scope controls. | Agent execution, model valuation, causal attribution and operational use. |
| Vendor deployment and inventory review | Authored synthetic records, complete/missing/ambiguous cases, identity and local-check controls. | Agent execution, real vendor verification and institutional model validation. |
| SOFR calibration review | Fresh numerical reproduction, per-instrument table, authored missing/conflicting cases and precision controls. | Agent execution and assessment of the report, independent financial validation. |
| Simulation review | Actual fixed-stream calculations, selected replicate, authored missing/contradictory cases and reference report. | Agent execution, general interval coverage, other simulation designs and financial suitability. |
| Black implementation review | Fresh ten-case numerical comparison, twelve invalid-input controls, authored missing/contradictory packets and reference report. | Agent execution and assessment, broader implementation coverage and financial suitability. |
| SOFR change review | Existing historical model evidence, two authored requirement selections, reference report and exact metric/threshold checks. | Model-backed execution of the new composed report and any production-change readiness. |

The shared library definitions are candidates for reuse, not individually certified capabilities. Mechanical checks do not establish that an executor follows them or that an evaluator detects every violation. A complete report can properly find adverse results; its fulfillment depends on the selected reporting requirements. Package checks, source review, financial acceptance and model-backed trials remain separate forms of evidence.

## October 6, 2026 numerical reproduction

The existing helper at source `27e5594bb03751bdfe9272cfd58e4923e72d9d64` completed in 18.16 seconds using the exact documented Python and numerical-package versions in an isolated environment. All fields in results.json matched under the unchanged relative 1e-10 and absolute 1e-12 numeric tolerances, with exact structure and nonnumeric values. Input and script hashes were unchanged. The [public receipt](../provenance/reproduction/2026-10-06.json) records versions, hashes, command scope and comparison.

This is a deterministic calculation using the committed derived quotes and fixing, without new market-data retrieval or quote derivation. The generated run_info.json lists derive_quotes.py as original project metadata; that script was not executed in this invocation. The result does not validate raw-input selection, the financial model independently, agent documentation or contract fulfillment. The earlier default-environment preflight failure remains a separate historical observation.

## Implementation-review component

The implementation-review contract has authored distinguishing cases for bounded reference agreement, passing identities with convention errors, unexecuted tests, observer discrepancies and shared input-mapping errors. The [worked report](../examples/implementation-review/README.md) composes it with model description; that addition brought the operating examples to nine across fourteen domains. No agent has executed or assessed this composition. At source 6772948, package selection reached 128 files, the inspected file-count limit. Its package qualification concerns that exact all-in-one checkpoint.

## Component-package separation proposal

A separate candidate selects all 22 reusable definitions, a consumer entry document, license and manifest: 25 files. The separation itself leaves definitions and existing example programs unchanged. The subsequent implementation-review example adds source-only material; its numerical evidence does not change the reusable package. Runnable examples remain in the complete source repository; the delivery guide pins checkpoint 6772948 for the existing demonstration. Example exports are deliberately absent from the component package, so fetching it is not an install-and-run example flow.

The prior all-in-one candidate and its numerical/agent evidence remain historical records for their exact scope. Local-reference, byte and package checks cannot establish registry delivery, authentication or fresh attendee execution. This packaging change introduces no new model results or financial acceptance.

## October 6, 2026 Black adapter calculation

The owned calculation at source e14925e completed using Python 3.12.14, QuantLib 1.43 and SciPy 1.18.1. [The receipt](../examples/implementation-review/receipt.json) identifies the source, native dependency and packet projections. All ten selected cases have a usable numerical reference under the illustrative tolerance. Adapter A agrees in ten cases; the deliberately wrong time-scaling adapter agrees in three despite passing all ten parity checks. The omitted-discount adapter agrees in two and passes six parity checks. All twelve selected invalid-input controls reject their inputs. These are actual CPU calculations, not model API calls or agent outcomes.

The calculation reproduces an earlier research study exactly for numerical observations, invalid-input controls and summary counts. Agreement with a second calculation method is conditional on common inputs and assumptions. The complete packet preserves observed records; baseline-only withholds records and contradictory adds an explicitly authored producer claim. Their reference report and expected interpretations are authored. Neither this calculation nor its record checks establishes natural-language contract fulfillment, an advantage over plain instructions, regulatory compliance or production readiness.

## Simulation-review addition

The simulation-review component adds explicit target, sampling-unit, dependence, uncertainty-method and error-scope requirements. It composes existing reporting and numerical-evidence definitions. Its worked report composes implementation review, bringing the catalog to fifteen operating domains and ten report examples. These are authored compositions, not fifteen qualified capabilities.

The owned calculation at source c5648a2 reproduces all observations and summaries of a preceding prespecified research study: 64 fixed streams and two nested sample sizes. Duplicating each observation reduces the naive standard error by about 29.3% without changing the estimate; grouping the known pairs recovers the original. A deliberately omitted discount estimates a different expectation. The public packets select replicate 0 by index, not outcome; missing-large-sample withholds its larger observation and contradictory adds an authored producer claim. [The receipt](../examples/simulation-review/receipt.json) binds their observed numerical records.

No agent has executed or assessed this report. Its reference and method/policy interpretations are authored. Moment and interval checks do not establish general empirical coverage, financial suitability, superiority over plain instructions or operational savings. The new definition increases the reusable component package to 23 definitions and 26 selected files; preceding 25-file package observations remain historical evidence for their original bytes.

## Full methodology-document example

The [full SOFR example](../examples/sofr-documentation/README.md) binds the default documentation contract to an explicitly bounded public technical scope. It reuses existing code and historical numerical evidence; no new financial calculation or agent invocation was performed. The short decision-note demo remains unchanged.

Its complete-case document, supporting section/choice/citation/readiness records and identity record are authored references. The missing-locality case removes only the specified numerical results. D5 requires those results, so gap disclosure cannot establish document completeness. D9 deliberately requires disclosure of institutional gaps, which does not supply the missing facts or approval. The dedicated evaluator keeps document findings, report coverage and execution evidence separate.

Fixed checks cover projection identities, selected numerical table correspondences, D1–D10 section-plan markers and reference hashes. They do not evaluate arbitrary prose, determine citation support or certify the authored readiness conclusion. Historical full-document candidates in the predecessor and the earlier short-note runs are not qualification of this composition. All 23 reusable definitions and the existing 26-file component package remain unchanged.

## Dependence-review proposal

The dependence-review component adds joint admissibility, estimation-population, exposure-binding and adjustment-provenance requirements. Eight authored cases distinguish supported, missing and contradictory evidence. No agent has executed this component, and it has no worked report yet. Existing definitions and examples remain unchanged.

The component package now contains 24 definitions and 27 selected files. Earlier package observations above retain their historical scope; they do not qualify the new bytes. Repository/reference closure checks are distinct from interpreting these requirements or assessing financial suitability.

The subsequent [worked dependence report](../examples/dependence-review/README.md) composes model-data requirements with this component. Its public calculation source reproduces every matrix, membership, adjustment and exposure observation from the separately retained deterministic study. Three packets preserve complete evidence, omit membership lists/raw rows, or add contradictory producer claims. The latter two changes are authored evidence selections, not new model calculations.

The reference report is authored and the execution route remains unqualified. Fixed controls cover numerical relationships and twelve adverse mutations; they do not establish arbitrary contract fulfillment or institutional suitability. The 24 definitions and 27-file component package are unchanged by this source-only example.

## Selection-history composition

The [selection review](../examples/selection-review/README.md) reuses outcomes analysis and model data, adding no definition. Its owned numerical source reproduces the separately retained fixed-score study exactly. The public packet selects replicate 0 at K=64 by index, not favorable outcome; every other study replicate remains outside the report scope. Missing-evaluation and contradictory packets are authored modifications of the supplied evidence, not new score calculations.

The reference is authored, and no agent has executed or assessed the program. Controls establish fixed identities, score comparisons, family-tail arithmetic and selected adverse cases; they do not establish performance of an investment strategy or arbitrary contract fulfillment. All 24 definitions, earlier examples and the 27-file component package remain unchanged.

## Cash-flow review proposal

The cash-flow component adds instrument terms, accrual/payment distinctions, flow identity and settlement-inclusion requirements. Eight authored cases distinguish supported findings, missing evidence and contradictions. It has no worked report or agent execution yet. A close aggregate valuation cannot establish payment-date correctness, and modeled obligations do not establish actual payment.

The candidate now contains 25 definitions and 28 selected package files. Existing definitions and examples are unchanged. Previous package and runtime observations retain their exact historical scope; source/package checks do not establish semantic fulfillment or financial suitability.

The subsequent [cash-flow/valuation composition](../examples/cashflow-review/README.md) uses a public-source calculation that reproduces every term, flow, valuation, comparison and control from a prespecified synthetic study. Three packets preserve complete evidence, withhold schedules while retaining aggregates, or add unsupported producer claims. Per-flow valuation rows are independent reference calculations, not an internal library trace.

The reference is authored and no agent has executed or assessed the report. Fixed controls cover date/amount arithmetic, inclusion populations, aggregate comparisons and twelve adverse mutations. They do not establish actual payment, institutional acceptance or arbitrary report fulfillment. The 25 definitions and 28-file package remain unchanged by this example.

## Sensitivity precision composition

The [sensitivity/implementation report](../examples/sensitivity-review/README.md) accounts for all three synthetic calls, six forward bumps and two price representations. A public-source reproduction matches every observation, reference and control in the prespecified study. Complete, missing-unrounded and contradictory packets separate derivative findings from price precision and supplied uncertainty bounds.

The reference report is authored and remains agent-unqualified. Fixed controls cover arithmetic, input/metric identities, missing observations, equality at the illustrative tolerance and twelve adverse mutations. They do not establish an optimal step, spot sensitivity, hedge or arbitrary report fulfillment. All 25 definitions, earlier examples and the 28-file package remain unchanged.


## Optimization-review component

The [optimization-review contract](../contracts/optimization-review.md) adds authored cases distinguishing native termination, original problem identity, feasibility, objective accuracy and actual candidate revisions. It composes existing reporting/numerical requirements; preceding definitions and examples are unchanged. Its private development study retains seven fixed synthetic solver results and one rounded export, with independent two-variable convex references. Those calculations motivate the distinctions; they do not qualify agent execution of the contract.

The component checkpoint at 66721cf contains 27 definitions across nineteen operating domains, with authored cases but no worked optimization report. Seventeen offline commands and actual CLI-source preparation/extraction of its 30-file package pass. Earlier package results retain their original scope.


## Worked optimization composition

The [optimization/implementation report](../examples/optimization-review/README.md) preserves seven native outcomes and one actual rounded export. Public source 0f8b3c8 reproduces every numerical observation, reference and control from the prespecified synthetic study. Complete, missing-candidate and contradictory packets distinguish expected analytical results from actual candidate observations, and native success from original feasibility and optimality.

The authored complete-case reference accounts for all eight candidates. Fixed checks use standard-library arithmetic and twelve adverse mutations; they do not run a solver, assess arbitrary prose, estimate solver reliability or authorize an allocation. All 27 definitions and the 30-file component package remain unchanged. Agent execution and assessment of the worked report remain unperformed.


## Historical-availability composition

The [model-data/outcomes report](../examples/availability-review/README.md) reviews six selectors over thirteen synthetic records and ten requested decision cutoffs. Public source dd53d67 reproduces all sixty selections, diagnostic reasons, metrics and seventy-two controls in the prespecified study. Later corrected values deliberately equal the synthetic outcomes; perfect error is a planted illustration, not a forecast result.

The complete, missing-history and contradictory packets preserve observed selections and numeric errors while separating independent timing support. Withheld availability does not prove late data or non-execution. The authored complete-case reference accounts for all sixty selections; fixed checks cover timestamp/identity relationships, denominators, exact boundaries and twelve adverse mutations. These checks do not run a query, assess prose or verify a production feed. Existing definitions, earlier examples and component-package bytes are unchanged; the reporting program remains agent-unqualified.


## Credit-loss component

[Credit-loss review](../contracts/credit-loss-review.md) adds authored requirements and ten distinguishing cases for probability conditioning, exposure/severity, loss timing and evidence gaps. It composes existing reporting and numerical requirements. All previous definitions and examples remain unchanged. The component checkpoint has 28 definitions across twenty operating domains; existing worked reports retain their prior qualification limits.

At component checkpoint a2e62da, no agent had executed or assessed this new component and no worked credit-loss report was supplied. The requirements do not implement a regulatory or accounting standard, estimate loss-model reliability or authorize a financial action. Source checks and package preparation establish only their stated mechanical properties.


## Worked credit-loss composition

The [credit-loss/implementation report](../examples/credit-loss-review/README.md) retains all six observed constructions and four intervals. Public source d717a0d reproduces the preceding study's source identity, scope, inputs, probabilities, amounts and 58 controls exactly. Only observation timestamp and duration are excluded from that comparison. Complete, missing-severity and contradictory packets distinguish actual parameters from selected requirements; withholding an intended loss fraction leaves calculation observations intact.

The 725-word complete-case reference is authored. Fixed controls inspect all four bindings per interval, observed arithmetic, source identities, exact tolerance boundaries and fourteen adverse mutations. They do not run QuantLib, assess arbitrary prose or establish accounting acceptance. All definitions, preceding examples and component-package bytes remain unchanged. Agent execution and assessment of this report remain unperformed.


## Portfolio-tail composition

The [portfolio-tail report](../examples/portfolio-tail-review/README.md) composes existing credit-loss, dependence and scenario requirements. Public source 77818d9 reproduces all fixed inputs, native/exact quantities and 120 controls from the preceding study, including two native/exact quantile differences at 80%. Only observation timestamp and duration differ. All six proposed tables and sixteen risk summaries remain visible; the two incompatible probability proposals are retained without a risk calculation.

The 931-word complete-case reference is authored. Fixed checks preserve the one missing native allocation without erasing the independently supported risk result; sixteen adverse mutations and exact tolerance-boundary controls exercise selected corruptions. These checks make no solver or provider call and do not assess arbitrary prose. All 28 definitions, previous examples and component-package bytes remain unchanged. Agent reporting and financial acceptance remain unqualified.
