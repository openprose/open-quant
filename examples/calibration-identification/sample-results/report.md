# Calibration review — authored reference

Case: `complete`. This illustration uses synthetic observations and supplied calculation evidence. It is not an agent run, market calibration or institutional acceptance.

## Fit, admissibility and selection

| Record | q1 | q2 | q3 | Original-data fit | Six-month call, USD | Native success |
|---|---:|---:|---:|---|---:|---|
| C1 | 0.000 | 0.080 | 0.050 | Met | 0.000000 | Not a solve |
| C2 | 0.040 | 0.040 | 0.050 | Met | 5.637198 | Not a solve |
| C3 | 0.080 | 0.000 | 0.050 | Met | 7.965567 | Not a solve |
| C4 | -0.010 | 0.090 | 0.050 | Met | Undefined | Not a solve |
| S1 | 0.040 | 0.040 | 0.050 | Met | 5.637198 | Yes |
| S2 | 0.010 | 0.070 | 0.050 | Met | 2.820360 | Yes |
| S3 | 0.040 | 0.040 | 0.050 | Met | 5.637198 | Yes |
| S4 | 0.070 | 0.010 | 0.050 | Met | 7.452657 | Yes |
| S5 | 0.096 | 0.000 | 0.042 | Not met | 8.722938 | Yes |

Rates are variances per year, displayed to three decimals. Prices are rounded to six decimals. Findings use the underlying values and supplied tolerances. C4 fits both observed maturities but violates q>=0; its half-year variance is −0.005 and its call value is undefined under this model. Prices at its other maturities do not make the whole curve admissible. C1–C3 and S1–S5 have nonnegative supplied rates.

Evidence: `inputs/complete.json`, witnesses C1–C4, solves S1–S5, their `points` and original-data residuals; `inputs/requirements.md`, original-data tolerance; `inputs/brief.md`, variance and pricing conventions.

## What the observations identify

W(1)=0.04 and W(2)=0.09 imply q1+q2=0.08 and q3=0.05. Moving along [1,−1,0] preserves that fit. Nonnegativity permits q1 from 0 to 0.08, so half-year variance ranges from 0 to 0.04. C1 and C3 attain the endpoints, yielding call values USD0 and USD7.965567. These are sharp bounds within this stipulated exact-fit family, not market confidence intervals or forecasts.

For all admissible exact fits, W(1.5)=0.065 and the supplied eighteen-month call is USD10.143593. Nonunique parameters therefore leave this particular output identified. S5 is outside the exact-fit family and is not a counterexample to its bounds.

Evidence: `inputs/brief.md`, data equations; `inputs/complete.json`, `analytical_reference`, C1–C3 and their eighteen-month points. The sums and null-direction implications above are arithmetic checks of those inputs.

## Optimizer and preference

S1 successfully minimizes the original nonnegative least-squares objective, but one returned solution does not establish uniqueness. S2–S4 add allocation preferences −0.06, 0 and +0.06. Their full-rank augmented systems select different unique, zero-residual solutions. The preference supplies the additional restriction; original data rank remains two. The specified numerical penalty assumes rates expressed per year, not an arbitrary unit-invariant weight.

S5's preference +0.10 is incompatible with an exact fit and nonnegative rates. Its supplied candidate has original residuals approximately (0.008,0), so it fails the 1e-10 fit tolerance. Preference residual −0.004 gives augmented objective 0.00004. The gradient (0,0.008,0) satisfies the active lower-bound condition, and the augmented quadratic is strictly convex. Thus the evidence supports global optimality for that penalized problem, alongside failed original-data fit. The solver's successful termination after ten iterations concerns the former.

Evidence: `inputs/complete.json`, S1–S5 native outputs and preference fields; `inputs/brief.md`, the two objectives. Objective and gradient checks use the supplied residuals and matrix, without rerunning optimization.

## Scope and remaining work

All nine records are accounted for. This report can fulfill its content obligation while identifying C4's inadmissibility and S5's misfit. No producer statements appear in this case. Economic suitability, empirical uncertainty and institutional approval are not established. The receipt records numerical reproduction, not execution of this report or compliance with its permissions. An actual invocation must also supply its result record and available execution evidence.

In `missing-allocation`, C2's retained longer-maturity values and reported residuals do not determine its actual rates, six-month price or admissibility. Family-level identities remain available; another proposal or optimum cannot replace the missing actual vector. In `contradictory`, the same numerical records do not support the seven added producer claims.

## Source identities

- `examples/calibration-identification/program.md` — SHA-256 `d07570c098e3c30af3b16634e9688ae605487670d3b7132adf021791367526b6`.
- `contracts/calibration-review.md` — SHA-256 `a6bdefcc594f59ae18f30c9cbb838aebee4577c4f1aadc17505bfde3f11688cc`.
- `contracts/optimization-review.md` — SHA-256 `c0fdd4f6f8599bc7501c00bfecdc3490ce2ece113dd179341499a43ce1b05cf7`.
- `contracts/operating-report.md` — SHA-256 `e582e1c900f8f83d8a9c333e0e1900927e4e05bb5d63c66a3a4ca1007fd18e70`.
- `contracts/numerical-evidence.md` — SHA-256 `74dad32c15bea33cda09f0e3b6b97f60eee3b097705aeee5d860c7b363480183`.
- `contracts/claim-evidence.md` — SHA-256 `b023aeb88dc481b6cf31aff630a7adab28e52979827f5c6ecfda8861063d207c`.
- `contracts/institutional-facts.md` — SHA-256 `cfb18dc33211a4b511e8af40172596a4f9df592a3d99d41c93da877fd0b10ed1`.
- `examples/calibration-identification/inputs/brief.md` — SHA-256 `aa33c89cccb636c255302702fa4a3dc588da74f282776a562a895c36b189e710`.
- `examples/calibration-identification/inputs/requirements.md` — SHA-256 `88c1ba0231fe574c1e435da98b4885494312734791c8f484fedfa8e33176d0cd`.
- `examples/calibration-identification/inputs/complete.json` — SHA-256 `aea334641dce67e75ace14d1b6345eac8d0c221d5eb1c55451ab730ddb58f27c`.
- `examples/calibration-identification/receipt.json` — SHA-256 `52f6a0679ab5f6847c91ffb1af5854d93716826de06a1b080b07ea897b3bc5b6`.
