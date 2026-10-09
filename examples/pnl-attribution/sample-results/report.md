# P&L attribution review — complete

Authored reference for `complete`; no reporting agent or evaluator produced this result. The observed movement is USD 84,711.689941. All six bridges reconcile, but their allocations differ. The selected method averages three separate factors across all six orders; merging factors before allocation is a different method.

## Valuation evidence

The fixed position contains 10,000 long European calls, strike 100. Forward changes 100→110, annual volatility 0.20→0.30 and maturity 1→0.75 years, with rate 0.03 fixed. Discount and standard deviation change with maturity; forward is independently supplied. There are no trades, cash flows or fees. These are counterfactual corners, not a history of observed market interventions. Bit order is forward, volatility, maturity. [Evidence: inputs; scope; brief.]

| Corner | Forward | Annual volatility | Maturity years | Native position USD | Native minus reference USD |
|---|---:|---:|---:|---:|---:|
| 000 | 100 | 0.20 | 1.00 | 77,301.493593 | -4.37e-11 |
| 001 | 100 | 0.20 | 0.75 | 67,477.109508 | -1.46e-11 |
| 010 | 100 | 0.30 | 1.00 | 115,711.446562 | 0 |
| 011 | 100 | 0.30 | 0.75 | 101,057.894713 | 1.31e-10 |
| 100 | 110 | 0.20 | 1.00 | 138,696.181835 | 8.73e-11 |
| 101 | 110 | 0.20 | 0.75 | 130,166.730022 | 1.16e-10 |
| 110 | 110 | 0.30 | 1.00 | 176,048.641170 | 1.46e-10 |
| 111 | 110 | 0.30 | 0.75 | 162,013.183534 | 2.91e-11 |

All eight native outcomes succeed and agree with the independent references within USD 1e-6. Total movement is V(111)−V(000), under one unchanged formula and position. Subsequent exact fractions represent retained decimal outputs rather than exact theoretical prices. [Evidence: corners; reported_attribution.total_usd; policy.]

## Reconciliation and selected allocation

Each contribution equals the difference across its named adjacent corners. All six paths are supported in this complete packet and close exactly for the represented values. Their different amounts demonstrate that closure cannot select an order or validate a causal label.

| Factor order | Forward USD | Volatility USD | Maturity USD | Total USD |
|---|---:|---:|---:|---:|
| forward → volatility → maturity | 61,394.688242 | 37,352.459334 | -14,035.457636 | 84,711.689941 |
| forward → maturity → volatility | 61,394.688242 | 31,846.453512 | -8,529.451813 | 84,711.689941 |
| volatility → forward → maturity | 60,337.194607 | 38,409.952970 | -14,035.457636 | 84,711.689941 |
| volatility → maturity → forward | 60,955.288821 | 38,409.952970 | -14,653.551850 | 84,711.689941 |
| maturity → forward → volatility | 62,689.620514 | 31,846.453512 | -9,824.384085 | 84,711.689941 |
| maturity → volatility → forward | 60,955.288821 | 33,580.785204 | -9,824.384085 | 84,711.689941 |

Standalone finite revaluations sum to USD 89,980.257127, leaving a joint interaction residual of −USD 5,268.567186. They are not derivatives or first-order approximations. The residual remains visible even though the selected mean allocation distributes interactions across factors. [Evidence: sequential_paths; standalone_usd; interaction_residual_usd.]

| Factor | Standalone USD | Mean over six orders USD | Minimum across orders USD | Maximum across orders USD |
|---|---:|---:|---:|---:|
| forward | 61,394.688242 | 61,287.794875 | 60,337.194607 | 62,689.620514 |
| volatility | 38,409.952970 | 35,241.009584 | 31,846.453512 | 38,409.952970 |
| maturity | -9,824.384085 | -11,817.114517 | -14,653.551850 | -8,529.451813 |

The selected average allocation is fully supported here. Seven subset interactions reconstruct the corners; splitting each equally among its member factors yields the same allocation as averaging orders. This is an identity for the chosen factors and endpoints, not a proof of economic causality. All required factor contributions are covered; no input or path is excluded. [Evidence: subset_interactions_usd; equal_interaction_allocation_usd; average_over_orders_usd.]

## Factor grouping

The comparison combines forward and volatility, then averages group→maturity and maturity→group. Both grouped paths close, but the resulting allocation differs from summing already allocated components:

| Factor/group | Sum from three-factor allocation USD | Two-group allocation USD | Difference USD |
|---|---:|---:|---:|
| forward_volatility | 96,528.804458 | 96,641.610801 | 112.806343 |
| maturity | -11,817.114517 | -11,929.920860 | -112.806343 |

The maturity difference is one sixth of the three-factor interaction: its share changes from one third to one half under the new partition. The equal-and-opposite group difference preserves total P&L. The grouped result cannot replace the selected three-factor method merely because both reconcile. [Evidence: grouped_paths; group_average_usd; partition_difference_maturity_usd; policy.]

## Findings and limits

For the complete case, native/reference comparisons, path arithmetic, full input support and the selected three-factor calculation are met. The spread across orders is a property of the chosen construction, not a valuation error. No producer assertions or missing records are supplied. The evidence does not establish a uniquely appropriate factor partition, actual market causality, regulatory attribution compliance or permission to post accounts.

If an intermediate valuation were absent, internally reconciled reported increments would not independently confirm that missing source value. Known endpoints could still support the total, and paths avoiding that corner would retain support. This reporting obligation allows those distinctions; it does not require inventing evidence to obtain a favorable conclusion.

This authored report accounts for eight corners, six orders, standalone effects, interactions and both factor partitions. It checks supplied records and arithmetic without reproducing native pricing or inspecting its source. Source identity is attributed to the receipt. Report fulfillment, numerical findings and institutional acceptance remain separate. No runtime fulfillment or independent assessment is claimed.

## Identity locators

Computed SHA-256 identities for the complete case:

```text
examples/pnl-attribution/program.md  3d68b0c0ecb611d9055bb3ab47322863c395047974eca572f3073f2c6a13cfe2
contracts/pnl-explanation.md  b204bdd0e2ebcf6c572d741756868a63dd8c02301fb23dc59ee58b4e66dc9e01
contracts/sensitivity-review.md  5aebec871ee15a86cd9f659cb4337dd35e581bd58860b61e5728766575fbdf0a
contracts/operating-report.md  e582e1c900f8f83d8a9c333e0e1900927e4e05bb5d63c66a3a4ca1007fd18e70
contracts/numerical-evidence.md  74dad32c15bea33cda09f0e3b6b97f60eee3b097705aeee5d860c7b363480183
contracts/claim-evidence.md  b023aeb88dc481b6cf31aff630a7adab28e52979827f5c6ecfda8861063d207c
contracts/institutional-facts.md  cfb18dc33211a4b511e8af40172596a4f9df592a3d99d41c93da877fd0b10ed1
examples/pnl-attribution/inputs/brief.md  ff9ebed496225e168b79b5efebd42f53adcfc335f19f5d2154aa44f6bcbf35bd
examples/pnl-attribution/inputs/policy.md  407fde556cefc6d5f8f742245bf2d23b28d0334ee5bf5fdfc32b1334bcebc7be
examples/pnl-attribution/inputs/complete.json  120391c1b0a089aa8fe59ce0e31ff2a406882225bc42fd31e9cdb5f4604d1b85
examples/pnl-attribution/receipt.json  58c204ac6320fa2b164043ff71e7d386903cdf640b2a0693b352c5d1b0e29b61
```
