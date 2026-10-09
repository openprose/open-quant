# Public credit methodology requirements

These are authored technical-documentation requirements for the supplied synthetic credit-loss model. The reader understands AI and financial operations but need not know credit mathematics. The scope is the public model and its retained calculation evidence, not a borrower forecast, accounting implementation or regulatory submission.

| ID | Required content in the methodology document |
|---|---|
| D1 | Identify the model/revision, purpose, reference date, supplied uses and exclusions. Distinguish a stipulated synthetic distribution from empirically calibrated or market-implied probabilities. |
| D2 | Describe all input intervals, exposure and loss fractions, hazard and discount rates, units and time conventions. Keep loss fraction distinct from recovery. |
| D3 | Explain survival, cumulative default, unconditional interval default and conditional interval default in plain language and formulas. Explain the selected discounted interval-loss aggregation and its absorbing-default assumption. |
| D4 | Explain the actual source implementation and the material choices, supplied rationale, alternatives and limitations. Mark an absent original rationale rather than inventing it. |
| D5 | Supply supported interval probabilities, selected interval loss amounts and the selected total, with units and locators. Describe why the four disjoint probabilities sum to cumulative default by the horizon. A gap label cannot replace a required numerical result. |
| D6 | Account for all six retained constructions and their totals. Explain what differs from the selected method and why bounded probability weights alone do not establish conformity. Preserve inappropriate alternatives as comparison evidence, not equally acceptable methods. |
| D7 | State what source inspection and the retained numerical receipt establish, their tolerances and material limitations. Distinguish historical calculation evidence from a new reproduction or an agent's documentation result. |
| D8 | Disclose each of the three selected institutional fact categories as supplied or unresolved. In the public scope, disclosure is required; supplying the missing underlying facts is not. Preserve uncertainty about whether a decision or activity occurred. |

Apply the documentation contract to the whole artifact set. Its section plan, choice register, citation audit, readiness and result record are additional obligations. Public document completeness means D1–D8 are met; it does not establish completeness under an institution's other requirements.
