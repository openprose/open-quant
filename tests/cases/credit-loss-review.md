# Distinguishing cases for credit-loss review

These authored cases describe [credit-loss review](../../contracts/credit-loss-review.md). They are interpretation references, not observed agent judgments or an automated prose benchmark.

| Supplied evidence | Required distinction |
|---|---|
| An absorbing-default model supplies consistent survival and interval masses, deterministic conditional exposure/severity, loss timing and matching calculated amounts. | Report the supported method and arithmetic conclusion for that exact scope. Do not promote it to empirical calibration, accounting acceptance or credit approval. |
| Cumulative default probabilities at successive horizons are individually bounded, then summed as interval masses. | Cumulative events overlap. Their validity as cumulative probabilities does not justify using them as disjoint interval probabilities. |
| Conditional interval default probabilities are multiplied by losses without the selected preceding-survival factor; their sum is below one. | Boundedness and a sum below one do not establish unconditional weighting. Preserve the omitted conditioning relationship. |
| Only the initial interval was checked, when survival is one and conditional/unconditional probabilities coincide. | Passing that baseline does not establish correct conditioning for later intervals. |
| An annual continuously compounded hazard is used directly as a default probability. | A rate, a time interval and a probability have different meanings. Identify the selected conversion or approximation and its evidence. |
| A loss uses one minus LGD; tests include only LGD 0.50. | Recovery and loss happen to coincide in that case. Those tests do not distinguish their roles for other severities. |
| The probability distribution is correct but a required discount factor or recovery delay is omitted. | Correct default probabilities do not establish the selected loss timing or present value. Preserve each binding separately. |
| A stochastic exposure and stochastic loss fraction are separately averaged and multiplied without dependence evidence. | Do not infer that their product equals the required conditional expected product. Identify the assumptions and missing support. |
| A market-implied curve is relabeled as an observed borrower default estimate without evidence. | Preserve the original probability basis. Numerical agreement cannot establish the new interpretation. |
| Some exposure or loss-severity records are absent, while the report gives a zero loss for them and a complete portfolio total. | Identify unresolved contributions and coverage. Missing evidence is not a zero observation or evidence of complete aggregation. |

The component reviews supplied evidence. Reproduction, model estimation and financial actions require their own caller scope. No worked credit-loss report or agent execution is qualified at this component checkpoint.
