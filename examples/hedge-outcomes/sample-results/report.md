# Hedge review — authored reference

Case: `complete`. This report illustrates supplied synthetic records. It is not an agent execution, actual hedge or independently validated forecast. Both periods contain four hypothetical P&L observations; all selection timestamps are authored assertions.

## Positions and outcomes

| Candidate | Standard lots | Training SSE | Later SSE | Within original limit? |
|---|---:|---:|---:|---|
| C1 | 0 | 50 | 20 | Yes |
| C2 | 2 | 10 | 100 | No |
| C3 | 1 | 20 | 50 | Yes |
| C4 | -1 | 100 | 10 | Yes |
| C5 | 2 | 10 | 100 | No |
| C6 | 200 | 392050 | 404020 | No |

SSE units are `(thousand USD)^2`. Displayed positions are rounded; findings use underlying values and supplied allowances. C1 is the unhedged baseline. Relative training reductions for C1–C6 are 0%, 80%, 60%, -100%, 80% and -784000%; later reductions are 0%, -400%, -150%, 50%, -400% and -2020000%. Negative reduction means a larger squared residual sum, not a cash loss of that amount. Each comparison retains its same-period baseline and all four observations.

All residual means are zero here, so population variance is SSE/4. This does not establish a general identity between mean squared error and variance. Fees, funding, margin and actual trades are outside this construction.

Evidence: `inputs/complete.json`, C1–C6, both observation populations and their residual vectors; `inputs/brief.md`, signs and units; `inputs/requirements.md`, original limit and tolerances.

## Fit, bounds and units

S1 returns the training least-squares coefficient 2, while S2 returns -1 fitted to the later period. Their squared-error minima are both 10 on their respective fitting populations. All three NumPy fits S1–S3 have rank one and return coefficients, residual sums and singular values; they do not return a Boolean success field. The supplied positive-curvature quadratics support unique global optima for the represented unconstrained problems. S1's optimum nevertheless violates the original ±1 standard-lot limit.

S4 and S5 both terminate successfully after seven iterations. They represent the training problem with ±1 lot and ±0.01 basket constraints. Their native cost is 10, corresponding to SSE20; it is not the full SSE. The positive-curvature quadratic and endpoint derivative support the upper-bound optimum. C3 respects the original position limit but still worsens later SSE by 150%.

S3 returns approximately 0.02 of a 100-lot basket. C5 therefore represents the same two-standard-lot position as C2, with the same results and the same limit breach. C6 instead applies S1's coefficient of two as a number of baskets, representing 200 lots. Correlation remains approximately 0.894427 in training and -0.707107 later under positive scaling; that invariance does not make C5 and C6 equivalent. Replacing C6 with a converted or clipped position would assess a different candidate.

Evidence: `inputs/complete.json`, S1–S5, C2/C3/C5/C6, `quadratic_reference` and `correlations`. Arithmetic checks use retained values without rerunning a solver.

## Timing and conclusion

C2, C3, C5 and C6 have selection records after the training observations and before the first later observation. That supports their stated timing within this authored packet, not proof against undisclosed real-world tuning. C4 was selected after all later observations; its 50% later improvement is a retrospective comparison, not an advance decision. It does not replace C2's adverse subsequent result.

All six candidates, five fits and eight observations are accounted for; there are no producer claims in this case. The report can fulfill its content obligation while identifying position breaches and worse later results. Statistical significance, real-world effectiveness, savings and institutional acceptance are not established. No position was refitted, traded or approved. An actual invocation must also provide its result record and available execution evidence; the numerical receipt does not prove those requirements were fulfilled.

Evidence: `inputs/complete.json`, candidate selection timestamps, fit populations and observation times; `receipt.json`, numerical calculation identity and scope.

## Source identities

- `examples/hedge-outcomes/program.md` — SHA-256 `4f12c4d3a52c82c61f4b14f9052c25262da48659df81d442b55bc94ec5e47d1e`.
- `contracts/optimization-review.md` — SHA-256 `c0fdd4f6f8599bc7501c00bfecdc3490ce2ece113dd179341499a43ce1b05cf7`.
- `contracts/outcomes-analysis.md` — SHA-256 `feda0de65ffaa28fa57b78934dd30f706700ac0de7acc1f566a8d2595df86077`.
- `contracts/operating-report.md` — SHA-256 `e582e1c900f8f83d8a9c333e0e1900927e4e05bb5d63c66a3a4ca1007fd18e70`.
- `contracts/numerical-evidence.md` — SHA-256 `74dad32c15bea33cda09f0e3b6b97f60eee3b097705aeee5d860c7b363480183`.
- `contracts/claim-evidence.md` — SHA-256 `b023aeb88dc481b6cf31aff630a7adab28e52979827f5c6ecfda8861063d207c`.
- `contracts/institutional-facts.md` — SHA-256 `cfb18dc33211a4b511e8af40172596a4f9df592a3d99d41c93da877fd0b10ed1`.
- `examples/hedge-outcomes/inputs/brief.md` — SHA-256 `82ecc9b7e060279df0512e41366494eb2731c5cb5f193b96e6062821aa72ccae`.
- `examples/hedge-outcomes/inputs/requirements.md` — SHA-256 `07a5010d1a6a9437d821787c5bfa25f5346c4b8f1455fe139174aaf6e9dc8e26`.
- `examples/hedge-outcomes/inputs/complete.json` — SHA-256 `60b485ee9dc8404e3fb0a00de5b021be851c48cb04657dc0067e2574997a01a5`.
- `examples/hedge-outcomes/receipt.json` — SHA-256 `4013b091c93d107e534acc1d098413aaa61f976a99777daa27d1373bcda35e00`.
