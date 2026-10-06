# Full-revaluation P&L attribution and factor grouping

Prespecified October 6, 2026, under IMP-087. One CPU process, at most 120 seconds, no retry, network, provider call or financial action. Use Python 3.12.14 and QuantLib 1.43. Preserve all eight native outcomes and their independent references, including failures. Subsequent record verifiers use arithmetic only, without native pricing.

## Fixed valuation scope

Price a fixed long position in 10,000 European calls, strike 100, continuous discount rate 0.03, no displacement. The three independently supplied factors are forward F:100→110, annual volatility v:0.20→0.30, and remaining maturity T:1→0.75 years. At each corner use standard deviation v√T and discount exp(−0.03T). This is an explicitly defined counterfactual grid; forward is not a spot inferred from time or carry. Advancing remaining maturity changes discount and standard deviation together while preserving the chosen forward input. No trade, cash flow, fee, exercise or quantity change is included. Values and movements are in USD for the fixed position.

Enumerate all eight old/new factor corners. Independently calculate the Black call with an elementary normal CDF using math.erfc. Require native position values to agree within absolute USD 1e-6, including equality at the boundary. Do not relabel a factor or alter its endpoints after seeing the result. This is synthetic mark-to-market movement rather than an accounting posting or regulatory P&L attribution test.

## Attribution constructions

The total is V(111)−V(000), with bit order forward, volatility, maturity. Retain every intermediate state and contribution for all six possible orders of changing the factors. Every path telescopes to the same total, but its individual factor increments need not agree with those from another order.

Retain standalone changes V(100)−V(000), V(010)−V(000) and V(001)−V(000). Keep total minus their sum as the joint interaction residual. These are finite full-revaluation single-factor changes, not derivative or first-order approximations.

Average each factor's increments over all six orders. Separately derive the seven nonempty subset interactions by inclusion-exclusion: for a factor subset A, d(A)=Σ[B⊆A](−1)^(|A|−|B|)V(B). Reconstruct every corner from its subset interactions and the base. Allocate each d(A) equally among its |A| members and compare the resulting factor allocations with the average over orders. These are two calculations of a specified symmetric allocation; agreement does not establish economic causality or prove that it is the institution's required method.

Finally treat forward and volatility as one group G, retaining two group orders G→T and T→G. Average the grouped increments and compare G with the sum of separate forward/volatility average allocations. Compare maturity allocation under both partitions as well. Grouping before allocation need not agree with summing already allocated components. Preserve differences rather than choosing whichever explanation looks better.

Use Fraction on each native position value's retained decimal representation for subsequent bridge/interaction arithmetic. This makes reconciliation identities exact for the represented values; it does not convert native prices into exact theoretical prices. Compare native/reference prices using the prespecified USD tolerance. No rounding occurs before attribution.

## Evidence and limits

Retain source, plan and input hashes; Python, QuantLib and native-library identity; all eight corners; six path traces; standalone effects/residual; seven interactions; symmetric allocations; both group orders; partition comparisons; timing and controls. An adverse check should detect lost or mislabeled corners, wrong factor transitions, redistributed residual, altered order, double counting, grouped allocation substitution and unsupported causality claims.

The inspected [QuantLib v1.43 Black interface](https://github.com/lballabio/QuantLib/blob/v1.43/ql/pricingengines/blackformula.hpp) binds forward, standard deviation and discount. The path and subset identities are finite algebraic derivations in this study, not a claim of new attribution theory. Existing P&L explanation, sensitivity and numerical-evidence requirements can express the distinction when the caller supplies its method. No new contract, agent qualification, institutional acceptance or measured savings is presumed.

## Optional reproduction

This calculation is separate from the reporting program. In an environment with Python 3.12.14 and QuantLib 1.43, run `python3 examples/pnl-attribution/model/measure.py --output /tmp/open-quant-pnl-fresh.json` from the repository root, choosing an unused destination. Apply an external 120-second process deadline. The calculation makes eight native price calls and no market or provider request.

Public source and this plan are committed before the one authorized reproduction. Compare all fields with the preceding study except newly recorded timing and explicitly rebound source/plan hashes. A reproduced calculation does not qualify the reporting agent or establish economic causality.
