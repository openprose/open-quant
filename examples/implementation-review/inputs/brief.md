# Synthetic Black pricing adapters

The subject is BLACK-ADAPTERS-2026-10-06: three adapters in the calculation source identified by the receipt. The intended use is a bounded implementation-evidence review for an AI-literate financial operations reader on October 6, 2026. No observed production deployment, institutional acceptance or approval record is supplied; those are the selected institutional facts to report as unresolved.

The documented method values European calls and puts using a lognormal terminal forward, positive forward F, nonnegative strike K, annual volatility sigma and time to expiry T. F and K are USD per underlying unit, sigma is a decimal annual volatility, T is years, and r is a continuously compounded annual rate. The discount factor is exp(-r*T). Output is present-value USD per underlying unit. Displacement is zero. Nonpositive forwards and negative strikes, volatilities or expiries are outside the selected domain. Negative rates are permitted in this example.

The QuantLib Black API receives total standard deviation sigma*sqrt(T), not annual volatility, and the discount factor as separate arguments. The reference independently integrates the discounted payoff under the same lognormal assumption, splitting at the payoff kink and truncating the normal variable to [-12, 12]. Its reported quadrature estimate and analytical tail bound qualify the reference under the policy; they are not a formal error guarantee. Zero volatility or expiry uses the deterministic discounted payoff. Put–call parity requires call minus put = exp(-r*T)*(F-K).

| Report name | Source variant | Input mapping |
|---|---|---|
| A | correct | sigma*sqrt(T), exp(-r*T) |
| B | wrong-time-scaling | sigma, exp(-r*T) |
| C | omitted-discount | sigma*sqrt(T), 1 |

B and C are deliberately constructed convention errors, not defects discovered in QuantLib. Their names and mappings are disclosed; this is not a blind evaluation. Baseline T=1 and r=0 masks both errors. Passing parity alone cannot detect all pricing errors, especially when both sides share a wrong volatility input.

The implementations share QuantLib, while the numerical reference uses SciPy quadrature. Both share the selected inputs, units and mathematical assumptions. Agreement tests numerical implementation under those assumptions; it does not establish market suitability, comprehensive test coverage, regulatory compliance or approval.

The owned script uses the API documented in [QuantLib 1.43's Black header](https://github.com/lballabio/QuantLib/blob/v1.43/ql/pricingengines/blackformula.hpp). This is a source citation for the supplied brief, not permission for this report to retrieve external material.
