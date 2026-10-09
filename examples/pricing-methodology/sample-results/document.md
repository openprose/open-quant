# Black European-option pricing methodology — authored reference

This is a public synthetic-methodology example for `complete`, not an observed agent result or a regulatory submission. The subject is `BLACK-ADAPTERS-2026-10-06`; result.md records the exact calculation-source and evidence identities.

## Purpose and scope

The selected method, adapter A, prices European call and put payoffs under a stipulated lognormal terminal-forward distribution. The purpose is to explain that method and its implementation evidence. The example supplies no real market calibration, forecast of physical outcomes, observed deployment or institution-approved use. B and C are deliberately altered input mappings, not defects discovered in QuantLib. [Sources: model brief; calculation source: VARIANTS, price; packet study.]

## Method and parameter conventions

F is a forward price and K a strike, both in USD per underlying unit. F is not supplied as a spot price. Sigma is decimal annual volatility, T is expiry in years, and r is a continuously compounded annual discount rate. Total standard deviation is s=sigma*sqrt(T), and the discount factor is D=exp(-r*T). The output is present-value USD per underlying unit; displacement is zero.

The reference constructs terminal value `X=F*exp(-s²/2+s*Z)` for standard-normal Z. Call and put values are respectively the discounted expectations of `max(X-K,0)` and `max(K-X,0)` under that stipulated distribution. The native A mapping supplies K, F, s and D to QuantLib's Black formula. Agreement checks the implementation under these assumptions; it does not establish an empirical probability law.

The selected domain requires finite numeric inputs, F>0 and K, sigma, T≥0. Negative r is permitted, producing D>1 for T>0. At sigma=0 or T=0, the payoff is deterministic: D times the appropriate positive part of F-K or K-F. At K=0, call value is D*F and put value is zero under this positive-forward model. No broader negative-forward or displaced model is selected. [Sources: brief; source: domain, price, reference.]

## Reference and comparison design

For nonzero s, the reference integrates the discounted payoff against a standard-normal density on [-12,12], splitting at the payoff kink when it lies inside that interval. SciPy quadrature requests absolute and relative tolerance 1e-11 with subdivision limit 200. The code retains estimated integration error, warnings and a tail allowance. At zero s it uses the deterministic payoff directly.

The illustrative policy accepts a reference for comparison only if there are no recorded warnings and its nonnegative estimated error plus tail allowance is at most 1e-9 USD per unit. It compares each native price to that reference within the same absolute amount, and checks put–call parity separately: call minus put equals D*(F-K). The error estimate is not a proven total numerical bound. Both methods share input conventions and the same pricing assumptions; numerical agreement is not evidence that those assumptions fit a market. [Sources: source: reference, main; comparison policy.]

## Retained numerical evidence

The complete packet supplies ten cases. The table gives actual native A values; prices are rounded to nine decimals, while checks use retained precision. Input units and conventions are those above. All twenty call/put references meet the supplied usability criterion. [Source: packet observations, inputs, reference and variants.correct.prices.]

| Case | F | K | Sigma | T | r | A call, USD/unit | A put, USD/unit |
|---|---:|---:|---:|---:|---:|---:|---:|
| baseline | 100.0 | 100.0 | 0.2 | 1.0 | 0.0 | 7.965567455 | 7.965567455 |
| short-expiry | 100.0 | 100.0 | 0.2 | 0.25 | 0.03 | 3.957964835 | 3.957964835 |
| long-expiry | 100.0 | 100.0 | 0.2 | 4.0 | 0.03 | 14.059411222 | 14.059411222 |
| in-the-money | 120.0 | 100.0 | 0.2 | 2.0 | 0.03 | 23.384611746 | 4.549321074 |
| out-of-the-money | 80.0 | 100.0 | 0.2 | 2.0 | 0.03 | 2.903132607 | 21.738423279 |
| zero-volatility | 120.0 | 100.0 | 0.0 | 2.0 | 0.03 | 18.835290672 | 0.000000000 |
| zero-expiry | 120.0 | 100.0 | 0.2 | 0.0 | 0.03 | 20.000000000 | 0.000000000 |
| zero-strike | 100.0 | 0.0 | 0.2 | 2.0 | 0.03 | 94.176453358 | 0.000000000 |
| negative-rate | 100.0 | 100.0 | 0.2 | 2.0 | -0.01 | 11.473481763 | 11.473481763 |
| higher-volatility | 100.0 | 100.0 | 0.8 | 5.0 | 0.04 | 51.490519919 | 51.490519919 |

All twelve selected invalid-input calls were rejected: each adapter was exercised with zero forward, negative strike, negative volatility and negative expiry. The source also rejects nonfinite and nonnumeric inputs, but those conditions are not part of the retained twelve-call population. These checks are finite input evidence, not exhaustive domain testing. [Sources: packet invalid_input_controls; source: domain, main.]

## Adapter differences and limits of simple checks

| Adapter | Total deviation supplied | Discount supplied | Price agreement, cases/10 | Parity agreement, cases/10 | Largest absolute price difference, USD/unit |
|---|---|---|---:|---:|---:|
| A | sigma*sqrt(T) | exp(-r*T) | 10 | 10 | 1.42108547152e-14 |
| B | sigma | exp(-r*T) | 3 | 10 | 26.040808008 |
| C | sigma*sqrt(T) | 1 | 2 | 6 | 11.400143129 |

Price agreement here requires both call and put to meet the selected reference criterion in a case. At the baseline T=1 and r=0, all three mappings coincide. B preserves parity while using the wrong total deviation outside special cases. C's missing discount can pass a zero-valued parity right-hand side when F=K. Passing that identity alone therefore misses convention errors. These mappings are visible in source; their observed counts concern only the retained ten cases. [Sources: packet observations; source: price; comparison policy.]

## Choices, provenance and remaining gaps

The selected lognormal model, positive-forward domain, constant parameters, zero displacement, quadrature window and checking tolerances are supplied settings. No original economic rationale or comprehensive alternative-model comparison is supplied. The choice register preserves those absences. Negative rates are represented, but negative forwards, early exercise, volatility surfaces, calibration uncertainty and production pricing controls are outside this example. [Sources: brief; source constants, domain, reference; reviews.md.]

The receipt identifies an earlier Python 3.12.14 / QuantLib 1.43 / SciPy 1.18.1 calculation and the packet projections. This document performs no new calculation and claims no execution of an agent program. The retained synthetic cases establish neither financial suitability, operational savings nor the independence of an institutional review. [Source: numerical receipt.]

- [INSTITUTION-SUPPLIED: accountable model owner and organization]
- [INSTITUTION-SUPPLIED: actual production deployment, acceptance and permitted use]
- [INSTITUTION-SUPPLIED: independent reviewer, review scope and decision]

No such records are supplied. Their disclosure meets the selected public gap requirement; it does not establish what an institution actually did. Source names above resolve through [the register](../inputs/sources.md); result.md records their exact identities.
