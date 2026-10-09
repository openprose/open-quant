# Pricing probabilities and intended use

Authored reference for `complete`; not an agent execution or independent assessment. Reading and arithmetic checks on retained evidence are distinct from reproducing the calculation. Other selections need reports based on their own packets.

## Model and scope

TOY-STATE-PRICES r1 prices six payoffs in a frictionless, deterministic-rate, two-state market over one year. A USD1 terminal bond costs 20/21; a USD100 stock becomes either USD80 or USD130. There are no dividends, taxes, transaction costs or default, and unrestricted real holdings are assumed. This synthetic construction does not establish applicability to a real market or institution.

The bond and stock span both terminal states, so every listed payoff is replicated. State prices are 10/21 for down and up. Their sum is 20/21, the bond price. Normalization gives Q(down)=Q(up)=1/2. State prices are present prices of unit state-contingent payoffs; they are not already probabilities. The native results agree with exact rational references within the supplied 1e-10 arithmetic allowance, including replication in both states.

## Prices and expectations

All table entries are USD per stated instrument. Prices are at t=0; expectations concern terminal payoffs at T=1 year. The quantities are related, but they are not interchangeable.

| Instrument | Present price | Q expected payoff | A physical expected payoff | B physical expected payoff |
|---|---:|---:|---:|---:|
| bond | 0.952381 | 1 | 1 | 1 |
| stock | 100 | 105 | 110 | 120 |
| call-100 | 14.285714 | 15 | 18 | 24 |
| put-100 | 9.523810 | 10 | 8 | 4 |
| digital-up | 0.476190 | 0.5 | 0.6 | 0.8 |
| digital-down | 0.476190 | 0.5 | 0.4 | 0.2 |

Physical world A stipulates P(down)=2/5 and P(up)=3/5. World B stipulates 1/5 and 4/5. Their expected stock returns are therefore 10% and 20%. These are implications of assumptions, not empirically validated forecasts. Neither world is selected as true.

Both reproduce all six present prices using state-dependent discount factors. The down/up factors are (25/21, 50/63) in A and (50/21, 25/42) in B. In each state, physical probability times discount factor equals its state price. Thus price=E_P[m X] in either world, while price=(20/21)E_Q[X]. A stochastic discount factor need not be constant or at most one.

The put's price is approximately USD9.523810, its Q expected payoff is USD10, and its physical expected payoffs are USD8 and USD4. Dividing the price by the bond price recovers the Q expectation. Discounting either physical mean by the constant bond price does not produce this put price. These positive payoffs are not realized portfolio losses or regulatory expected credit losses.

## What the evidence supports

Pricing and replication are supported within the stipulated market. Complete payoff spanning does not select a physical probability model: the two worlds share prices while assigning different event probabilities. More generally, any positive physical probabilities can reproduce these state prices with factors m(s)=z(s)/P(s). That algebraic construction does not establish an empirical distribution.

The separate equality control has P=Q and constant m=20/21. The measures can coincide, but market-price consistency alone does not establish that equality. The supplied observations support conditional explanations of both worlds; selecting an empirical forecast would require additional evidence and a defined forecasting objective outside this reporting assignment.

The receipt reports one successful public CPU reproduction with 63 passing construction controls. This report checks retained quantities and identities; it does not claim to have rerun the calculation or inspected its source. There are no producer statements in this selected packet, and no selected organizational facts require completion. The reporting scope is covered, while empirical applicability and institutional acceptance remain unestablished. This authored reference does not establish actual executor fulfillment.

## Source identities

Locators below identify the report's selected evidence and adopted requirements. The calculation-source identity is reported by the receipt, separately from these inspected-file identities.

- `examples/pricing-probabilities/program.md` — `e6e033f682a735ff2516bb37a4a5b1161cccaeb5f6a0e25deb5cb86ce1018a93`
- `examples/pricing-probabilities/inputs/brief.md` — `9227557b782eb15c06256d4e3a3acd03b2200495df7c30883d95adf404edc9a8`
- `examples/pricing-probabilities/inputs/requirements.md` — `1a8f570281ae82ba4030812b7e582b400cd1cd0336d3438c469c85c2e0bbfcf4`
- `examples/pricing-probabilities/inputs/complete.json` — `768763ff97c5ea53977a11594d86a0174f72d1bc6a8ce8afd548cb06ec8e21f6`
- `examples/pricing-probabilities/receipt.json` — `f910417abb626079ce09167eb51f60d8ab615caaf7b84a7f5424ab776b862aee`
- `contracts/model-description.md` — `8a48a2f1ff8bea197026b3ba433ebb36cf9cfeb739cfd35b2eddfe992fe0c574`
- `contracts/numerical-evidence.md` — `74dad32c15bea33cda09f0e3b6b97f60eee3b097705aeee5d860c7b363480183`
- `contracts/claim-evidence.md` — `b023aeb88dc481b6cf31aff630a7adab28e52979827f5c6ecfda8861063d207c`
- `contracts/institutional-facts.md` — `cfb18dc33211a4b511e8af40172596a4f9df592a3d99d41c93da877fd0b10ed1`
