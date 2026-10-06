# Supporting records for the authored reference

These records concern the accompanying authored document under the complete supplied-evidence case. They are coordinator authoring checks, not an evaluator invocation, institutional acceptance or proof that an executor followed the program's boundaries. Artifact and input identities are recorded below and in result.md.

## Section plan

| Requirement | Document location | Content finding and remaining scope |
|---|---|---|
| D1 | Purpose and scope | Model/date, use and exclusions are stated. Institutional deployment is not asserted. |
| D2 | Inputs and provenance | Input units, flags, fixing timing and upstream limitations are explicit. Raw acquisition is outside the declared scope. |
| D3 | Construction and conventions | Both implementations, instruments, time/accrual/schedule conventions and B's solve/interpolation are described. |
| D4 | Developer choice and observed comparisons; Construction and conventions; this choice register | B's reason and A's alternative are attributed; unsupplied rationales remain gaps rather than inventions. |
| D5 | Developer choice and observed comparisons | Repricing, daily/five-day moves and locality values are supplied with units and measured scope. |
| D6 | Variants, conventions and endpoint behavior | End rule, failed/configured variants and payment-lag sensitivity are identified. |
| D7 | Present-value interpretation | Monthly-grid date, discount-factor difference and one-payment USD interpretation are stated. |
| D8 | Limitations and unresolved institutional facts; comparison and variant sections | Finite evidence, sparse inputs, method tradeoffs, reproduction limits and unperformed broader checks remain visible. |
| D9 | Limitations and unresolved institutional facts | All three selected gap categories appear. Their disclosure does not supply the facts. |
| D10 | Source locators throughout; source-locator convention | Material claim groups have the checked source bindings below. No external paper contents are asserted from titles. |

## Choice register

Each row identifies a material choice described in the document. “Not supplied” means no developer rationale or alternative was found in the selected evidence; it does not mean none existed. Code can establish the implemented setting without establishing its author's economic reason.

| Choice | Supplied reason or absence | Alternative and limitation | Locator |
|---|---|---|---|
| Single-curve SOFR scope | Stated developer scope; further rationale not supplied. | Multi-curve and other-currency uses excluded, not assessed alternatives. | brief.md |
| One as-of snapshot | September 18, 2026 is supplied; selection rationale absent. | Other dates untested by this document. | brief.md; results.json.as_of |
| Use only selected derived-quote rows | Code follows used_in_bootstrap; admission rationale not reproduced here. | Unselected rows are not calibration inputs; upstream processing remains outside scope. | quotes.csv; bootstrap.py: load_inputs |
| Same last-known fixing for O/N and T/N | Setting is visible; economic rationale not supplied. | Different T/N input is a source parameter, not the selected build. | bootstrap.py: ql_helpers |
| Act/365 Fixed curve time | Implemented setting; rationale not supplied. | No selected alternative time-axis study is supplied. | bootstrap.py: DC, T |
| Act/360 accruals | Implemented setting; rationale not supplied. | A fixed-leg convention comparison is recorded, not a mandate to change. | bootstrap.py: ACT360; results.json.convention_sensitivities |
| SOFR calendar | Implemented setting; rationale not supplied. | Other calendars are not qualified by this example. | bootstrap.py: CAL |
| Two-business-day swap spot lag | Implemented setting; rationale not supplied. | Other starts are not evaluated here. | bootstrap.py: ql_helpers |
| Annual fixed-leg frequency | Implemented default; rationale not supplied. | Quarterly comparison exists; its result does not approve a convention. | bootstrap.py: ql_helpers; results.json.convention_sensitivities |
| Following adjustment | Implemented setting; rationale not supplied. | Other adjustments not evaluated in the selected account. | bootstrap.py: ql_helpers |
| Two-business-day payment lag | Implemented setting; rationale not supplied. | Zero-lag comparison has an observed effect. | bootstrap.py: PAYMENT_LAG; results.json.convention_sensitivities.payment_lag_0_vs_2 |
| B rather than A | Developer prefers observed forward shape. | A has stronger observed locality; no universal preference follows. | brief.md; results.json.forward_smoothness, locality_bump_5Y_plus_1bp |
| Unameliorated B with collar enabled | Method identity is supplied; economic reason for collar selection absent. | No-collar case has no measured effect here; other inputs may differ. | brief.md; results.json.interpolation_variants, hagan_west_collar_binding_nodes |
| Simultaneous B calibration | Source explains interpolation's neighbor dependence. | Source explicitly does not use a node-by-node solve; comparative runtime evidence absent. | hagan_west.py module description and bootstrap |
| Hybrid solver and numerical tolerances | Implemented values; selection rationale absent. | Other solvers/tolerances are not compared in this account. | hagan_west.py: bootstrap |
| Constant terminal forward | Implemented end rule; economic rationale absent. | Sparse long-end inputs and extrapolation remain limitations. | hagan_west.py: forward, integral; brief.md |
| Daily/five-day grids and one 5Y +1 bp locality test | Supplied comparison design; rationale for full test selection absent. | Finite grids and one perturbation do not establish all-regime behavior. | bootstrap.py: main; brief.md |
| USD100 million single-payment interpretation | Supplied notional and comparison meaning. | It is not a portfolio profit or savings estimate. | bootstrap.py: NOTIONAL; brief.md |

## Citation audit

This audit checks support for the specific claim groups below. It does not establish the underlying model's suitability or independently verify the external data provider. Claim groups include their stated limitations; an inspected implementation is not treated as proof of every intended property.

| Document claim group | Checked support | Applicability and finding |
|---|---|---|
| Model purpose, date, methods and developer preference | brief.md; results.json.as_of/spot; bootstrap.py: CurveSet | Supported as supplied scope and attributed preference. No deployment claim. |
| Twenty OIS inputs, excluded 9M/25Y and two deposits | quotes.csv flags; results.json.instruments; bootstrap.py: load_inputs/ql_helpers | Supported selected population, not a complete market universe. |
| Fixing 3.85%, September 17 identity and no later-field use | sofr-fixing.json; bootstrap.py: load_inputs | Code reads sofr_percent only; post-as-of observations are not the selected anchor. |
| Percent conversion and source-data limits | quotes.csv; bootstrap.py: load_inputs; provenance/README.md | Transformation is supported; raw acquisition/quote derivation is not claimed reproduced. |
| Calendar, day counts, frequencies, adjustments and lags | bootstrap.py constants, ql_helpers, hw_instruments | Supported as implemented defaults, not institution-approved conventions. |
| A construction and B's shared dates/separate pricing | bootstrap.py: CurveSet, hw_instruments; hagan_west.py: ois_par_rate | Supported source description; shared dates limit comparison independence. |
| B's discrete/node forwards, collar, piecewise integration and discounting | hagan_west.py: MonotoneConvex, _sector, _g, _G | Supported implementation account; no unprovided paper theorem is asserted. |
| Simultaneous root solve and acceptance residual | hagan_west.py: bootstrap | Requested tolerance 1e-14 and residual guard 1e-11 are source values, not model-error bounds. |
| Four-row A/B comparison table | Selected results.json fields named in D5; bootstrap.py metric definitions | All displayed values match the original record at stated precision. Finite comparisons are not broad validation. |
| Locality date boundaries and last node | bootstrap.py: d4/d6; source-register boundary explanation; results.json.forward_smoothness | Uses actual pillar dates and inclusive inside bounds, not nominal year fractions. |
| Endpoint behavior and B forward value | hagan_west.py: forward/integral; results.json.forward_smoothness.B | Code end rule plus retained observed values; no market-extrapolation acceptance. |
| Collar and QuantLib variant outcomes | results.json.interpolation_variants, hagan_west_collar_binding_nodes | Failed (0,1) variant preserved; default variant is not called identical to B. |
| Payment-lag comparison and its USD interpretation | results.json.convention_sensitivities.payment_lag_0_vs_2.B; bootstrap.py: NOTIONAL | Conditional variant comparison; the worst-point date is not invented. |
| Monthly-grid A/B difference and USD100 million payment | results.json.df_difference_A_minus_B_monthly_grid; brief.md | Absolute valuation difference at stated date; no profit or documentation-savings claim. |
| Finite-snapshot and locality limitations | brief.md; selected results and source | Supported limits of the supplied observation design, not invented results for other regimes. |
| Earlier reproduction and unchanged-input scope | provenance/reproduction/2026-10-06.json | Receipt identifies successful conditional comparison; it does not establish this document's execution. |
| Selected institutional gaps | institutional-facts.md; requirements.md: D9 | Disclosure supported; actual ownership, review, approval and production use remain unknown. |

No material claim group in this authored document is intentionally left unchecked. Economic rationales marked absent remain absent; this audit does not supply them. Wider acquisition checks, external-paper verification and institutional review are outside the selected public account, not silently passed.

## Readiness

The authored document supplies D1–D10 under the declared public scope. The section plan covers all ten IDs; the choice register preserves known reasons and absences; the citation audit covers the document's material claim groups. These are manual authoring findings on these exact artifacts, not an independent evaluator result or broad assurance that any executor follows the contracts.

Institutional facts remain unresolved. D9 asks for disclosure, so that does not by itself make this public account incomplete. In contrast, the missing-locality case removes numerical evidence required by D5: a document can then report an honest gap but cannot be declared complete. This reference must not be reused unchanged for that case.

The program has not been executed in an authenticated CLI run. Tool permissions, source preservation and runtime behavior of a future invocation are untested. An overall fulfillment claim for such an invocation is therefore unavailable here. Its own result record and separate assessment remain required. Source/package checks and numeric correspondences do not substitute for that assessment.
