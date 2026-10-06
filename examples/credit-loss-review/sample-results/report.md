# Authored reference: complete credit-loss review

This is an authored reference for the complete packet, not an agent result. All six constructions and four intervals are covered. Observed arithmetic is internally consistent in all six; only `interval_mass` follows all selected method bindings. The other five deliberately change probability weighting, severity or discounting. Their observed differences are not measures of production model quality.

The selected distribution is synthetic, with absorbing default and constant annual hazard 0.12. There is no empirical or market-calibration evidence. Times are exact Actual/365 Fixed year fractions from 2026-01-01, not calendar anniversaries. Exposure and loss severity are deterministic conditional on default in each interval. Loss settles at interval end, discounted at 3% continuously compounded. [Evidence: complete.json/selected_method; policy.md.]

Survival is S(t)=exp(−0.12t). An unconditional interval mass counts defaults in that interval from the original population: S(start)−S(end). The conditional probability divides by survival to the interval start, answering a different question about the remaining population. The selected loss uses unconditional mass × exposure × loss fraction × discount factor.

| Interval | Years | Unconditional mass | Conditional probability | Exposure USD | Loss fraction | Discount factor | Selected loss USD |
|---|---|---|---|---|---|---|---|
| I1 | 0–1 | 0.113079563283 | 0.113079563283 | 1,000,000 | 0.45 | 0.970445533549 | 49,381.900706 |
| I2 | 1–2 | 0.100292575651 | 0.113079563283 | 800,000 | 0.45 | 0.941764533584 | 34,002.716663 |
| I3 | 2–3 | 0.088951534996 | 0.113079563283 | 600,000 | 0.50 | 0.913931185271 | 24,388.674543 |
| I4 | 3–5 | 0.148864689977 | 0.213372138933 | 400,000 | 0.50 | 0.860707976425 | 25,625.805214 |

Each row is supported by selected_method.intervals[id], observed_probabilities.intervals[id] and observed_constructions[interval_mass].rows[interval_id]. Selected loss is USD 133,399.097125. The four masses sum to 0.451188363906, equal to cumulative default by year 5. Checks use unrounded packet values with absolute probability/severity/discount tolerance 1e-12 and USD arithmetic tolerance 1e-7; displayed rounding is not the acceptance test.

| Construction | Weight sum | Observed loss USD | Difference from observed interval_mass USD | Selected bindings |
|---|---|---|---|---|
| interval_mass | 0.451188363906 | 133,399.097125 | +0.000000 | met: I1–I4 |
| cumulative_as_interval | 1.079963740051 | 282,281.768182 | +148,882.671057 | breached: probability I2–I4 |
| conditional_as_unconditional | 0.552610828782 | 155,454.158864 | +22,055.061738 | breached: probability I2–I4 |
| hazard_times_interval | 0.600000000000 | 167,303.792201 | +33,904.695075 | breached: probability I1–I4 |
| recovery_as_loss | 0.451188363906 | 151,929.012096 | +18,529.914971 | breached: severity I1–I2 |
| undiscounted | 0.451188363906 | 143,449.529206 | +10,050.432080 | breached: discount I1–I4 |

The table covers observed_constructions[id], including all four component amounts. Exposure bindings match throughout. Unlisted probability, severity and discount bindings are met in this complete case. The comparison column uses an observed construction; its conformity has been established separately here, not inferred from its name.

**Probability interpretation.** All individual weights are between zero and one. Cumulative probabilities remain valid cumulative probabilities, but successive cumulative events overlap; summing them as disjoint interval masses repeats earlier defaults. Conditional probabilities have a sum below one yet omit survival to each interval start when used directly as unconditional weights. For I3, conditional default is 0.113079563283 versus unconditional mass 0.088951534996. Hazard multiplied by interval length omits exponential conversion and preceding survival. No such approximation is selected. First-interval agreement cannot expose later conditioning errors because initial survival equals one. [Evidence: observed_probabilities and the first four constructions.]

**Severity and timing.** Recovery substituted for LGD changes 0.45 to 0.55 in I1/I2. The two coincide at 0.50 in I3/I4, so those latter intervals alone would not test the distinction. The undiscounted construction preserves all probability and severity bindings but changes all four selected discount factors to one. Correct probabilities therefore do not establish correct discounted loss. [Evidence: recovery_as_loss and undiscounted rows.]

This scoped review checks the supplied records and arithmetic; it does not inspect or rerun calculation source. The receipt identifies source revision, hash, environment and one completed developer calculation. Source execution, reporting fulfillment and financial acceptance are distinct. There are no missing selected bindings or producer assertions in this packet. No borrower performance, accounting treatment, stochastic exposure/severity dependence or institutional approval is established. Those require separate evidence and scope. This authored report illustrates the reporting outcome; it does not establish an agent's fulfillment or execution effects.

Source identity locators (SHA-256, computed while authoring):

```text
examples/credit-loss-review/program.md  54b9b89c7b44d822b1d704a516793f4ceb7b97dc0ee4cb8afdaecbe31c113d49
examples/credit-loss-review/inputs/brief.md  7f0b41eb36a2248fd6c33b0d229dfce38d8e1ac082e815865cd2fe9933503f22
examples/credit-loss-review/inputs/policy.md  e627241df75b5d356bd05757b52ff0cf8a399d7d1d942fbe51dee3ac25626f40
examples/credit-loss-review/inputs/complete.json  810a88259b3e961ff58269d8a97ee846465cdeabdd55590df9c6b486707fa687
examples/credit-loss-review/receipt.json  28fad7d2bbabe91ace75e9d4e08e06578d32f1a7493acde0ab8d7e38ace79266
contracts/claim-evidence.md  b023aeb88dc481b6cf31aff630a7adab28e52979827f5c6ecfda8861063d207c
contracts/credit-loss-review.md  7f2e9d6f65dafcf80b36369eb9d44f98aa71c2bf398af3022dbb6d8916a176f5
contracts/implementation-review.md  f110ecc95fd9228ddefc78388553898e26570aefc70363a00dd84315e3e7b6cb
contracts/institutional-facts.md  cfb18dc33211a4b511e8af40172596a4f9df592a3d99d41c93da877fd0b10ed1
contracts/numerical-evidence.md  74dad32c15bea33cda09f0e3b6b97f60eee3b097705aeee5d860c7b363480183
contracts/operating-report.md  e582e1c900f8f83d8a9c333e0e1900927e4e05bb5d63c66a3a4ca1007fd18e70
```
