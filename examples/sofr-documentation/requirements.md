# Public methodology-document requirements

These are authored technical-documentation requirements for this example. The requested scope is a public account of the supplied USD SOFR model, conditional on retained derived inputs. It does not include a complete institution-specific model document, raw-data acquisition audit or regulatory submission. The selected institutional facts must remain visible as gaps; their factual completion is outside this invocation.

| ID | Required content in the methodology document |
|---|---|
| D1 | Identify the model, as-of date, purpose, intended public scope and excluded uses. Distinguish intended use from observed institutional deployment. |
| D2 | Describe supplied inputs, their dates, units, selection flags and source limitations. Explain the boundary between derived inputs and the upstream acquisition/quote-derivation process that is not reproduced here. |
| D3 | Explain how the two implementations turn inputs into discount factors and forward measures. Identify curve time, accrual, scheduling, payment and rate conventions; describe the simultaneous solve and the actual interpolation implementation. |
| D4 | Preserve the developer's selected method, supplied reason, alternative and material tradeoffs. Describe additional material implementation choices and label reasons that the supplied evidence does not establish. |
| D5 | Supply supported A/B repricing maxima, largest daily and five-business-day forward moves, and outside-window response to the selected +1 bp 5Y quote perturbation. Give units, dates, comparison population and interval definitions; explain what each measure does and does not establish. A gap label does not replace a required result. |
| D6 | Describe implementation-variant evidence, the endpoint/extrapolation rule, and convention sensitivity with at least one supported numerical example. Preserve failed variants and distinguish an API's configured method from a similarly named alternative. |
| D7 | Explain the monthly-grid discount-factor difference and its USD100 million single-payment interpretation, with the selected date. Do not present it as trading profit, a documentation benefit or a savings estimate. |
| D8 | State material limitations of the supplied model, inputs, numerical comparison and developer preference. Distinguish observed results, source inspection, reproduction evidence and unperformed broader checks. |
| D9 | Identify every selected institutional fact as supplied or unresolved. No institutional facts are supplied in this example; disclosing those gaps fulfills this content requirement but does not establish the facts, approval or an institution-ready document. |
| D10 | Provide traceable source locators for material factual claims and distinguish the developer's rationale from an independently established fact. No source outside the selected register may supply a claim. |

Apply the [documentation contract](../../contracts/documentation.md) to the whole artifact set. Its section plan, choice register, citation audit, readiness report and result record are additional obligations. A correct negative readiness finding does not excuse an incomplete audit or missing report. Document completeness means every D1–D10 requirement is met under this declared public scope; it says nothing about requirements outside that scope.
