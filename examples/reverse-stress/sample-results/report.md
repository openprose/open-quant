# Reverse-stress review — complete case

Authored reference, not an observed agent result. Subject: TOY-REVERSE-STRESS r1, instantaneous synthetic losses from the zero-shock base. All eight runs, three metrics, four catalog scenarios and the separate witness are accounted for. No probability model, actual portfolio, management action or institutional acceptance evidence is supplied or required by this reporting scope.

## Candidate findings

Loss is x²+4y²−2x in USD millions; selected squared severity is S=x²+y². x divides a rate change by 25 bp and y divides an equity-return change by 5 percentage points. The loss threshold is USD3 million with USD0.01 allowance. The selected minimum is 2/3 with squared-severity tolerance 1e-8. Findings below use retained precision; they are numerical criteria rather than judgments of reporting fulfillment.

| Run | Native status | Loss, USD million | Selected S | Threshold | Selected minimum |
|---|---|---:|---:|---|---|
| selected-negative-axis | success | 3.000000000000 | 1.000000000000 | met | not met |
| selected-positive-axis | failure 8 | 2.999999938458 | 8.999999907687 | not met | not met |
| selected-upper | success | 3.000000000001 | 0.666666666667 | met | met |
| selected-lower | success | 3.000000000001 | 0.666666666667 | met | met |
| selected-origin | success | 3.000000000000 | 1.000000000000 | met | not met |
| selected-iteration-limit | failure 9 | 12.410383602212 | 10.221618257262 | met | not met |
| raw-mixed-units | success | 3.000000000000 | 0.745026017753 | met | not met |
| raw-common-basis-points | success | 3.000000000000 | 1.000000000000 | met | not met |

Evidence: `inputs/complete.json`, `solver_results`, named native candidates and quantities; `inputs/policy.md`, selected criteria. Negative-axis and origin successes produce S≈1, 50% above 2/3. Their zero recomputed stationarity residual does not establish a minimum: tangent curvature is approximately −2. Upper and lower starts produce distinct signs of y while both meet the selected minimum criterion. A requirement for the minimum does not select only one of those signs.

The positive-axis run fails (status 8); its loss falls about USD0.061542 below the threshold, beyond the USD0.01 allowance. A rounded “3.00 million” display would hide this failure. The one-iteration run fails (status 9) but its supplied candidate does reach the threshold; failure does not mean every finding is unavailable. All actual candidate, gradient and physical-shock records are supplied in this case. Derived correspondence checks do not transform a native success flag into a global certificate.

## Global references and metric identity

| Metric | Weights a,b | Own minimum | Minimizer x | Minimizer y² |
|---|---|---|---|---|
| selected | 1, 1 | 2/3 | -1/3 | 5/9 |
| raw-mixed-units | 1, 1/25 | 74/2475 | -1/99 | 7301/9801 |
| raw-common-basis-points | 1, 400 | 1 | -1 | 0 |

Evidence: `inputs/complete.json`, `global_references`. For each metric, the supplied identity F−lambda*(L−3)−m=cx*(x−x0)²+cy*y² has matching rational coefficients and nonnegative lambda, cx and cy. Its reference points attain loss 3 and objective m. This establishes the global bound for the stated all-real domain. For the selected metric it reduces to S−(L−3)/4−2/3=3(x+1/3)²/4. Native QP multipliers and the best of a finite number of starts do not establish that bound.

The raw-mixed and raw-common-basis-point runs meet their own metric minima, but neither meets the selected minimum. Their selected S values are approximately 0.745026 and 1. Summing squared numerical rate-bp and equity-percentage-point changes, divided by 625, gives x²+y²/25. Recoding equity in basis points before that same numerical recipe gives x²+400y². That changes the objective. Dividing equity changes by 5 percentage points or the equivalent 500 bp preserves the selected S for the same physical shock. Chosen scales are not estimated volatilities, and nearest distance does not establish likelihood.

## Finite catalog and scope

| Scenario | x,y | Loss, USD million | Selected S |
|---|---|---:|---:|
| C1 | -1, 0 | 3 | 1 |
| C2 | 3, 0 | 3 | 9 |
| C3 | 0, 1 | 4 | 1 |
| C4 | 0, -1 | 4 | 1 |
| outside-catalog | 0, 2 | 16 | 4 |

Evidence: `inputs/complete.json`, `catalog` and `outside_catalog_witness`. The four catalog scenarios all reach the threshold, but their minimum S=1 exceeds 2/3. Their maximum loss is USD4 million; the separately identified witness has loss USD16 million. In the stipulated mathematical domain L(0,y)=4y² is unbounded. This neither establishes a finite worst possible loss nor says a real pricing approximation remains valid for arbitrarily large shocks.

This complete-case reference covers the selected reporting questions while retaining adverse native outcomes, failed selected criteria and alternative objectives. It does not authorize rerunning searches, altering thresholds, assigning probabilities or taking financial action. The numerical reproduction identity is attributed to `receipt.json`; the reporting scope does not inspect or execute its source. No execution trace accompanies this authored report, so permitted behavior and a runtime fulfillment claim are unverified. Reporting success, a solver's success flag and financial-model acceptance remain separate questions.

## Identity locators

These hashes identify the selected source bytes; they do not certify this authored report or show a model used them.

```text
examples/reverse-stress/program.md  e8387a5f56b732f3578226b52a858b324ff20145dd1d8d3b749de4e285b912bb
contracts/scenario-review.md  2ecfbae91425a159b0670a6142517ad3e27808ebbba415a3a5075aeb818d267c
contracts/optimization-review.md  c0fdd4f6f8599bc7501c00bfecdc3490ce2ece113dd179341499a43ce1b05cf7
contracts/operating-report.md  e582e1c900f8f83d8a9c333e0e1900927e4e05bb5d63c66a3a4ca1007fd18e70
contracts/numerical-evidence.md  74dad32c15bea33cda09f0e3b6b97f60eee3b097705aeee5d860c7b363480183
contracts/claim-evidence.md  b023aeb88dc481b6cf31aff630a7adab28e52979827f5c6ecfda8861063d207c
contracts/institutional-facts.md  cfb18dc33211a4b511e8af40172596a4f9df592a3d99d41c93da877fd0b10ed1
examples/reverse-stress/inputs/brief.md  89979798cf2889e611268ae399b32d4a266650a798f98b5ed3dfbd5fe9e557cd
examples/reverse-stress/inputs/policy.md  e61492d92b3224860cc2eade2d6ca0c70812a9200d7fac797c63e7aa35a291d7
examples/reverse-stress/inputs/complete.json  955b8e88e75921f67001227dcaeacf7843203d2f77494ce7d4464c92d4f1b186
examples/reverse-stress/receipt.json  18e3c6d7fc9c591d6ed36925679f4246c5caac88864c0bad2c7ffd2737039be4
```
