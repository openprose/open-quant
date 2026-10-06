# Joint exposure and default evidence

Authored reference for `complete`; not an agent execution or independent assessment. This report checks retained evidence and arithmetic. It does not claim to have rerun native calculations or inspected their source.

## Scope and quantities

TOY-EXPOSURE-DEFAULT r1 has potential exposure X of 10, 50 or 100 USD million at T=1 year, with probabilities 1/2, 3/10 and 1/5. Default indicator I has probability 1/10. Loss is (3/5)XI, paid at T and discounted by 20/21. The probabilities are stipulated under one measure, not empirically estimated or calibrated to market data. The convention excludes closeout, collateral, netting, earlier settlement, own default and recovery dynamics.

The common mean exposure is USD40 million. Multiplying that mean by PD, loss fraction and discount yields 16/7 million, approximately 2.285714. The actual joint calculation instead uses sum(x_i*d_i), where d_i is the probability of exposure state i together with default. Nondefault cells are p_i−d_i. Both sets of cells must be nonnegative and preserve the stated marginals.

## Proposal findings

All amounts below are USD million. The last column for J6 is formal arithmetic on an invalid table, not an expected loss.

| Proposal | Valid joint law | Independent | Exposure on default | Discounted loss or formal sum |
|---|---|---|---:|---:|
| J1 | yes | yes | 40 | 2.285714 |
| J2 | yes | no | 10 | 0.571429 |
| J3 | yes | no | 50 | 2.857143 |
| J4 | yes | no | 100 | 5.714286 |
| J5 | yes | no | 40 | 2.285714 |
| J6 | no | not applicable | unavailable | 3.085714 |

J1–J5 preserve nonnegative joint cells and the selected marginals. Their native quantities agree with exact references under the supplied 1e-10 arithmetic allowance. J2 and J4 demonstrate that the same marginals can produce different joint losses. The product of means is therefore not determined to be the joint expected loss by those marginals alone.

J5 also shows why the converse matters. Its conditional default probabilities given exposure are 12%, 4% and 14%, rather than the common 10% probability required for independence. Yet its default-weighted exposure is 4 and its covariance Cov(X,I) is zero. Hence E[XI]=E[X]E[I] for this quantity despite dependence. A matching product does not prove independence; dependence does not necessarily make this particular product incorrect.

J6 has default cells −1/100, 11/100 and 0. Its negative cell prevents interpretation as a probability law, even though marginal totals match and its formal loss sum lies between the valid bounds below. A plausible scalar does not establish valid joint inputs. Its ratio of weighted exposure to PD is arithmetic, not a supported conditional expectation; statistical independence is not applicable to this invalid table.

## Bound calculations

For nonnegative default allocations of total mass 1/10 and exposure between 10 and 100, the weighted exposure sum lies between 1 and 10. The corresponding discounted loss bounds are 4/7 and 40/7 million. The minimum witness allocates default mass [1/10,0,0]; the maximum uses [0,0,1/10]. Both respect exposure-state capacities, so these bounds are sharp for this finite problem.

Both native LPs report success, with candidates attaining those references. The minimizing objective is 1; the maximization is implemented by minimizing its negative, returning −10. The exact inequalities and feasible witnesses provide global support independent of the success labels. These attainable bounds are not an empirical confidence interval or a calibrated stress range for an actual counterparty.

## Reporting conclusion

The selected packet supports all five valid-table findings and the J6 violation. It contains no producer statements. No selected joint input is missing in this case. The receipt reports one public reproduction with 126 passing controls; inspecting these retained quantities is distinct from reproducing them.

This authored report covers the selected numerical questions while preserving the invalid proposal. It does not establish actual executor fulfillment, empirical validity, institutional acceptance or permission to book an adjustment. A real use would require its own probability basis, exposure/default construction, loss timing and applicable criteria. No organizational facts are selected for completion here.

## Source identities

These computed locators identify the selected report evidence and requirements. The calculation-source identity is reported separately in the receipt.

- `examples/exposure-default/program.md` — `5bef7cab336991d89ec57d0df2725913a609937f9932ce909d1a238bc1e1633e`
- `examples/exposure-default/inputs/brief.md` — `36fda93b707bbefa356cb6e192c5bc22f7804b63d7ba3e353dea15fee4bce526`
- `examples/exposure-default/inputs/requirements.md` — `2c6eaf59fcb6e62a4be70f941c8981058d3565ef652889f9194c95687a7f8baf`
- `examples/exposure-default/inputs/complete.json` — `232655a7759c2208b3fdd1d247748153bdf13bff974cfb778fdc309bf7df9c13`
- `examples/exposure-default/receipt.json` — `6b2e6437040c485615d02cb5e06c0796d2dd347b64e70ee28d6f909fd425105a`
- `contracts/credit-loss-review.md` — `7f2e9d6f65dafcf80b36369eb9d44f98aa71c2bf398af3022dbb6d8916a176f5`
- `contracts/dependence-review.md` — `3d262b85a34f0e0604650a462956028049314318552bcdfbedce475985a22b74`
- `contracts/operating-report.md` — `e582e1c900f8f83d8a9c333e0e1900927e4e05bb5d63c66a3a4ca1007fd18e70`
- `contracts/numerical-evidence.md` — `74dad32c15bea33cda09f0e3b6b97f60eee3b097705aeee5d860c7b363480183`
- `contracts/claim-evidence.md` — `b023aeb88dc481b6cf31aff630a7adab28e52979827f5c6ecfda8861063d207c`
- `contracts/institutional-facts.md` — `cfb18dc33211a4b511e8af40172596a4f9df592a3d99d41c93da877fd0b10ed1`
