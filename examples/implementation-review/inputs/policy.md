# Illustrative implementation review policy

This is the caller's synthetic house policy, not an institutional or regulatory standard. Apply it to BLACK-ADAPTERS-2026-10-06 and the exact calculation source identified in the receipt, for all three adapters A, B and C. Prices and residuals must be present-value USD per underlying unit. Apply these requirements separately:

- Input mappings must implement the conventions in the model brief across the selected domain.
- Each adapter must have supplied call and put results for baseline, short-expiry, long-expiry, in-the-money, out-of-the-money, zero-volatility, zero-expiry, zero-strike, negative-rate and higher-volatility. The expected inputs are the named CASES in the calculation source. Record identity and input values must match; another case with the same label is not a substitute.
- For each case, each price must agree with a usable reference within absolute 1e-9 USD per underlying unit. A reference is usable here only when it has no recorded warning and its nonnegative estimated error plus tail bound is at most 1e-9. This criterion limits the comparison; it does not make the estimate a guaranteed bound.
- For each case, call minus put must agree with exp(-r*T)*(F-K) within absolute 1e-9 USD per underlying unit. Report price agreement and parity separately.
- Each adapter must have an observed rejection for each selected invalid-input case: zero-forward, negative-strike, negative-volatility and negative-expiry, with the exact supplied control inputs in the calculation source. Test code alone does not supply an execution record.

Account for missing, duplicate and unexpected records against these expected populations. A known violation makes its criterion breached even when other evidence is missing. Otherwise a criterion requiring unavailable evidence is unresolved; only support across its whole selected scope makes it met. For the conjunction of implementation criteria, a known violation remains decisive while individual evidence gaps remain visible. This is distinct from fulfillment of the reporting contract.

The baseline-only packet deliberately withholds other calculation records. Do not infer from their absence that those tests were never run, or use another packet to fill the gap. The contradictory packet adds an authored producer claim to unchanged numerical observations. Resolve that claim against the observations rather than treating it as an acceptance decision.
