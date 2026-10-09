# Option consistency review — complete

Authored reference for the `complete` packet; no reporting agent or evaluator produced this result. All ten inversions meet the selected fit tolerance, but that does not establish joint price consistency. One authored strike-aware position has negative cost and nonnegative payoff under the stipulated terms and narrow spreads.

## Individual quote fit

The two synthetic single-expiry slices use European calls, forward 100, discount 1 and one-year maturity. All selected instrument terms stipulate underlying U1, expiry T1, USD unit notional and common cash settlement. These are caller stipulations, not actual market records. Standard deviation and annual volatility coincide numerically at one year.

| Slice | Strike | Call input USD | Native implied standard deviation | Repricing residual USD |
|---|---:|---:|---:|---:|
| constant_volatility | 80 | 21.185929513210 | 0.200000000000 | 0 |
| constant_volatility | 90 | 13.589108116055 | 0.200000000000 | -1.06581410364e-14 |
| constant_volatility | 105 | 5.905593471555 | 0.200000000000 | 0 |
| constant_volatility | 110 | 4.292010941410 | 0.200000000000 | 0 |
| constant_volatility | 130 | 1.008871615969 | 0.200000000000 | 1.55431223448e-15 |
| authored_quotes | 80 | 21.000000000000 | 0.189918271026 | 9.96891458271e-12 |
| authored_quotes | 90 | 14.000000000000 | 0.212437586417 | 1.93765004042e-11 |
| authored_quotes | 105 | 9.000000000000 | 0.277893025294 | -3.5527136788e-15 |
| authored_quotes | 110 | 8.000000000000 | 0.296413588731 | 1.7763568394e-15 |
| authored_quotes | 130 | 3.000000000000 | 0.280813969512 | 2.22044604925e-15 |

All native solves succeed. Root differences satisfy 1e-9 and the largest repricing residual is about USD 1.94e-11, below USD 1e-8. Intrinsic/forward bounds, parity and adjacent slopes in [-1,0] pass. Constructed parity puts are not independent observed quotes. These checks establish individual fit and identities, not a common distribution across strikes. [Evidence: slices[].quotes, adjacent_slopes; selected_instrument_terms; policy.]

## Joint payoff and cost

Strike-aware wings are (upper − middle)/(upper − lower) and its complement; equal wings are one half each. Both sell one middle call. Costs buy wings at ask and sell the middle at bid, so each is mid-cost plus twice the half-spread h.

| Slice | Weighting / middle strike | Mid cost USD | Cost at h=0.05 USD | Cost at h=0.20 USD | Minimum payoff USD |
|---|---|---:|---:|---:|---:|
| constant_volatility | strike_aware_90 | 1.484686980494 | 1.584686980494 | 1.884686980494 | 0.000000000000 |
| constant_volatility | equal_wings_90 | -0.043346623672 | 0.056653376328 | 0.356653376328 | -2.500000000000 |
| constant_volatility | strike_aware_105 | 0.710691763516 | 0.810691763516 | 1.110691763516 | 0.000000000000 |
| constant_volatility | equal_wings_105 | 3.034966057177 | 3.134966057177 | 3.434966057177 | 0.000000000000 |
| constant_volatility | strike_aware_110 | 0.634238159028 | 0.734238159028 | 1.034238159028 | 0.000000000000 |
| constant_volatility | equal_wings_110 | -0.834778397648 | -0.734778397648 | -0.434778397648 | -7.500000000000 |
| authored_quotes | strike_aware_90 | 2.200000000000 | 2.300000000000 | 2.600000000000 | 0.000000000000 |
| authored_quotes | equal_wings_90 | 1.000000000000 | 1.100000000000 | 1.400000000000 | -2.500000000000 |
| authored_quotes | strike_aware_105 | 0.500000000000 | 0.600000000000 | 0.900000000000 | 0.000000000000 |
| authored_quotes | equal_wings_105 | 2.000000000000 | 2.100000000000 | 2.400000000000 | 0.000000000000 |
| authored_quotes | strike_aware_110 | -0.200000000000 | -0.100000000000 | 0.200000000000 | 0.000000000000 |
| authored_quotes | equal_wings_110 | -2.000000000000 | -1.900000000000 | -1.600000000000 | -7.500000000000 |

All stated weights, exact payoffs and costs agree with their respective constructions. Each portfolio is piecewise linear between strikes and has zero final slope. Exact values at zero, all knots and the tail therefore establish the stated minimum for every nonnegative shared underlying value. This conclusion requires those legs to share that terminal underlying; it is not established solely by a grid of samples.

For authored 105/110/130 quotes, weights 4/5,−1,1/5 give cost −0.20 at zero spread and −0.10 at h=0.05, with minimum payoff zero. Both are conditional witnesses. Cost +0.20 at h=0.20 removes this particular witness; it does not establish global consistency. All other retained strategies lack this witness. [Evidence: slices[].strategies, exact payoff and costs; policy.]

Equal wings at middle strike 110 on the constant-volatility slice cost about −0.834778 at mid but can lose 7.50 at maturity. At middle strike 90 the corresponding values are −0.043347 and −2.50. Negative cost alone therefore gives a false alarm. Equal wings at middle strike 105 have nonnegative payoff but positive cost: equal weighting is not uniformly invalid.

## Findings and limits

Individual fit, parity, vertical bounds and faithful calculation are met. Joint consistency is breached for the authored slice under the narrower spread assumptions. The complete selected terms support applying the common-underlying payoff calculation to these synthetic instruments. Fractional positions and simultaneous quotes are stipulated, and no other fee, funding, margin, credit, tax or trading restriction is modeled. Nothing here establishes a tradeable real-market opportunity or permission to trade. [Evidence: calculation_assumptions; selected_instrument_terms; brief.]

If a selected underlying identity were missing, the calculation would remain an observation under its assumptions. Affected joint payoff applicability would be unresolved; unaffected triplets and fit/cost arithmetic would remain reportable. Nonnegative cost still rules out that specific negative-cost witness. Neither missing evidence nor a wider spread justifies an all-clear conclusion.

This authored report accounts for ten inversions, twelve strategies and 36 costs. It reviews supplied records and performs arithmetic, without reproducing native calculations or inspecting their source. Source identity is attributed to the receipt. Report fulfillment, underlying price findings and actual institutional acceptance are separate. No runtime fulfillment or independent assessment is claimed.

## Identity locators

Computed SHA-256 identities for the complete case:

```text
examples/option-consistency/program.md  1363d4642f1a6d45172eaa6b48f64d24affc4ca8eae72c96698b2931ef5055f9
contracts/calibration-review.md  a6bdefcc594f59ae18f30c9cbb838aebee4577c4f1aadc17505bfde3f11688cc
contracts/implementation-review.md  f110ecc95fd9228ddefc78388553898e26570aefc70363a00dd84315e3e7b6cb
contracts/operating-report.md  e582e1c900f8f83d8a9c333e0e1900927e4e05bb5d63c66a3a4ca1007fd18e70
contracts/numerical-evidence.md  74dad32c15bea33cda09f0e3b6b97f60eee3b097705aeee5d860c7b363480183
examples/option-consistency/inputs/brief.md  4a03c329efe41a2a5313fe0b07d45fe8d7e42e8cb379d1e6deabedde71d93538
examples/option-consistency/inputs/policy.md  3d6fd9f24faa6427c31598da1ec6d8f5a4a490a90a0f440946211e801768c843
examples/option-consistency/inputs/complete.json  f744803bf399c159d2fc5763cb8df0ed43e849cb78117e3521238f9a500b64ec
examples/option-consistency/receipt.json  8c2a831c7c9f8349c2caba2bc037e994586fc5caabc47226ad46ad6174c4e951
contracts/claim-evidence.md  b023aeb88dc481b6cf31aff630a7adab28e52979827f5c6ecfda8861063d207c
contracts/institutional-facts.md  cfb18dc33211a4b511e8af40172596a4f9df592a3d99d41c93da877fd0b10ed1
```
