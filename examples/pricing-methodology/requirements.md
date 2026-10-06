# Public pricing-methodology requirements

Document the supplied synthetic European-option model for an AI-literate financial operations reader. This is an authored technical scope, not a regulatory submission, real market calibration or institution-ready model document.

| ID | Required content in document.md |
|---|---|
| D1 | Identify model/revision, selected pricing method, public purpose, uses and exclusions. Distinguish a stipulated pricing distribution from an empirical forecast or actual deployment. |
| D2 | Define forward, strike, annual volatility, expiry, continuous rate, discount factor and total standard deviation, with units and selected input domain. Explain zero-volatility, zero-expiry and zero-strike behavior and the permitted negative rate. |
| D3 | Explain the selected discounted payoff expectation and actual native input mapping. Distinguish the forward from a spot price, annual volatility from total standard deviation, and pricing-model assumptions from implementation agreement. |
| D4 | Explain the reference integration, deterministic branch, truncation, error estimate and tail allowance. State how the supplied comparison policy uses them and the limits of a numerical estimate. Preserve material choices, supplied rationale, alternatives and absent rationale. |
| D5 | Supply the actual retained inputs and adapter A call/put values for all ten named cases, with units and traceable locators. Account for reference usability and the selected invalid-input observations. Theoretical values or source code do not replace required native observations. |
| D6 | Explain all three adapter mappings and their observed price/parity agreement counts under the supplied policy. Show why the baseline and parity alone can miss convention errors. Preserve known source-level deviations separately from missing execution evidence. |
| D7 | Identify what the source inspection, retained receipt and numerical comparisons establish. Keep original calculation evidence distinct from a fresh reproduction, agent documentation, model suitability or operating savings. |
| D8 | Disclose accountable ownership, production deployment/acceptance and independent review as supplied or unresolved within the registered evidence. Disclosure is required; supplying absent institutional facts is outside this public scope. |

Keep document.md under 1,500 words excluding source locators. Define specialist terms and use ordinary Markdown; no section sequence is prescribed. Identify the artifact as a public synthetic-methodology example. Use `[INSTITUTION-SUPPLIED: description]` for missing institutional facts; do not use those placeholders for required mathematical or numerical content.

Keep the section plan, choice register, citation audit and readiness together in reviews.md, with each distinguishable. Map D1–D8 to document locations or gaps. For material choices, preserve selected settings, supplied reasons or their absence, alternatives, limitations and evidence. Audit the support and applicability of material factual claims or identified claim groups; listing citations alone does not complete that work.

Separate document content, supporting-record coverage and execution evidence. For mandatory requirements, a supported violation yields not met; otherwise missing support needed to decide yields unresolved; only support for all mandatory requirements yields met. A known missing D5 observation is missing required content even when the method can be explained correctly. A negative readiness finding does not excuse incomplete supporting records. This selected policy does not establish institutional approval or the assessment's own fulfillment.
