# Counterparty-exposure review

**Authored reference for `complete`; not an agent-produced result.** This report covers EXPOSURE-2026-10-06 at 2026-10-06T00:00:00Z, all nine constructions, six trades and six collateral records. The selected measure is current positive exposure in USD after recognized collateral, floored separately within each stipulated netting set. No record is excluded from the reviewed population. Settlement, eligibility and netting recognition are supplied synthetic assumptions, not independently established institutional facts. [Evidence: selected_method; observed_calculation_inputs; brief.]

| Selected set | Signed trade value USD | Recognized collateral USD | Current exposure USD | Trade rows | Collateral rows |
|---|---:|---:|---:|---:|---:|
| NS-A1 | 340,000 | 199,000 | 141,000 | 2 | 3 |
| NS-A2 | −300,000 | 200,000 | 0 | 2 | 1 |
| NS-B1 | 720,000 | 237,500 | 482,500 | 2 | 2 |

The selected total is USD 623,500. USD-per-EUR is 11/10. T1/T2 yield USD 340,000 in NS-A1; T3/T4 yield −300,000 in NS-A2; T5/T6 yield USD 720,000 in NS-B1. Received C1 contributes USD 100,000; C2 contributes 100,000 EUR × 1.10 × 0.90 = USD 99,000. Pending C3 contributes zero recognized value. C4 contributes USD 200,000 within NS-A2 only. C5 contributes USD 237,500 after its 5% haircut, while ineligible C6 contributes zero. Zero recognition is a selected treatment of known records, not a missing record. [Evidence: selected inputs; selected_sets native_rows and exact_reference_rows.]

| Construction | Reported total USD | Difference from selected_sets USD |
|---|---:|---:|
| selected_sets | 623,500.000000 | 0.000000 |
| counterparty_pool | 482,500.000000 | −141,000.000000 |
| global_pool | 123,500.000000 | −500,000.000000 |
| omit_haircuts | 600,000.000000 | −23,500.000000 |
| include_pending | 543,500.000000 | −80,000.000000 |
| include_ineligible | 323,500.000000 | −300,000.000000 |
| invert_fx | 717,045.454545 | 93,545.454545 |
| join_before_aggregation | 1,587,000.000000 | 963,500.000000 |
| floor_trades_first | 1,283,500.000000 | 660,000.000000 |

Rows map to constructions[id], including native rows, exact references, totals and observed differences. Native values match their own arithmetic references within USD 1e-6. The selected_sets construction also follows the selected bindings in this complete case; all eight alternatives breach them. Internal numerical correspondence does not clear a different grouping, recognition assumption or operation order. [Evidence: policy; all constructions and selected_method.]

**Grouping breaches.** The two CP-A sets remain separate under the selected method. Pooling them lets NS-A2's negative value and surplus collateral erase NS-A1's USD 141,000 exposure. Pooling all counterparties further changes the total. Neither common counterparty identity nor offsetting values establish cross-set recognition. [Evidence: netting_sets; counterparty_pool/global_pool native group identities and rows.]

**Recognition and conversion breaches.** Omitting haircuts overstates collateral by USD 11,000 in NS-A1 and USD 12,500 in NS-B1. Counting pending C3 lowers exposure by USD 80,000; counting ineligible C6 lowers it by USD 300,000. Inverting the EUR conversion changes both trade and collateral values and increases total exposure by approximately USD 93,545.45. Its larger answer does not establish conformity. [Evidence: C2/C3/C5/C6; omit_haircuts, include_pending, include_ineligible and invert_fx records.]

**Join and flooring breaches.** Joining each trade to each collateral record duplicates contributions. NS-A1's two trades and three collateral records become six joined rows, with USD 1,020,000 trade value and USD 398,000 recognized collateral; exposure becomes USD 622,000. NS-B1 becomes USD 965,000 exposed; NS-A2 remains zero. The construction counts twelve joined trade rows and twelve joined collateral rows across six original records on each side. Flooring trades first instead discards permitted offsets before aggregation. [Evidence: join_before_aggregation and floor_trades_first native rows; source record identities.]

The signed trade total USD 760,000, positive individual-trade total USD 1,820,000 and positive unsecured net-set total USD 1,060,000 are different measures. None substitutes for collateralized current exposure. No future-exposure process, probability weighting or regulatory EAD calculation is supplied. [Evidence: scope_measures; selected scope.]

This authored reference covers the requested reporting population and distinguishes each construction's arithmetic from method conformity. No selected binding is missing and no producer assertion is supplied in this case. Calculation identity and observed environment are attributed to receipt.json; this report does not claim a SQL rerun. Broader institutional acceptance would require actual recognition and legal evidence. No model approval, regulatory eligibility or permission to trade, call margin or move collateral follows from this report.

## Identity locators

SHA-256 values identify the selected source files. Calculation-source identity is attributed to receipt.json.

```text
examples/exposure-review/program.md  df63e16f0bc2a8ea409c48a06741c59ef9921a9897c45621e5b6cdf1daffb9fa
examples/exposure-review/inputs/brief.md  95a663c431742f7037e939de1917a7bea63f94cb0af48580532a3edc99f02cea
examples/exposure-review/inputs/policy.md  2aad5b5f43bbd2dfe4d87d007ac6f976a19624f8fd8973a216b66d93753ad5bd
examples/exposure-review/inputs/complete.json  1745b87eb64c15abddf8cf21e3b17c5e1ba93546f3ee52f8e9190910c5c0039b
examples/exposure-review/receipt.json  93cff75932d73ce23ae58cd1359be887b3434bf704f6e1e461a1fa8383a5f343
contracts/counterparty-exposure.md  5341b49ee62373104d0f95f954bfc955c4ba65c76baff1212e44170f295a9cb1
contracts/implementation-review.md  f110ecc95fd9228ddefc78388553898e26570aefc70363a00dd84315e3e7b6cb
contracts/operating-report.md  e582e1c900f8f83d8a9c333e0e1900927e4e05bb5d63c66a3a4ca1007fd18e70
contracts/numerical-evidence.md  74dad32c15bea33cda09f0e3b6b97f60eee3b097705aeee5d860c7b363480183
contracts/claim-evidence.md  b023aeb88dc481b6cf31aff630a7adab28e52979827f5c6ecfda8861063d207c
contracts/institutional-facts.md  cfb18dc33211a4b511e8af40172596a4f9df592a3d99d41c93da877fd0b10ed1
```
