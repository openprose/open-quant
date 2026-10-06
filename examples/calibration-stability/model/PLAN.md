# Calibration stability: prespecified study

Status: plan and source to be committed before the sole native calculation. This is a synthetic reporting specimen, not a market calibration or a contract-execution experiment.

## Question and construction

Can a unique, accurately solved calibration remain sensitive to stipulated input uncertainty? Does changing parameter coordinates remove that uncertainty?

Use constant variance rates `a` over `[0,1]` and `b` over `(1,1+epsilon]`, with times in years. Observed total variances are `q1=a` and `q2=a+epsilon*b`. Set baseline `a=0.04`, `b=0.09`. Test exactly four rational spacings: `epsilon=1, 1/12, 1/365, 1/3650` years. These are synthetic durations, not date/day-count conventions. Total variance and integrated variance are dimensionless; rates are variance per year.

Stipulate an independent input box with half-width `eta=0.00004` in each total variance. This is an assumed uncertainty set, not an estimated confidence region or distribution. At each spacing retain baseline, common-up `(+eta,+eta)`, common-down `(-eta,-eta)`, steepen `(-eta,+eta)` and flatten `(+eta,-eta)`: twenty cases. Add one shortest-spacing boundary witness `q1=q2=0.04`, yielding `b=0`, for twenty-one cases total.

The exact inverse is `a=q1`, `b=(q2-q1)/epsilon`. The raw b interval is `[0.09-2*eta/epsilon, 0.09+2*eta/epsilon]`; the admissible interval intersects this with `[0,infinity)`. All a values are positive. Bounds are sharp: opposite corners attain the raw extrema, and the additional witness attains the admissible zero boundary when the raw lower bound is negative. Negative variance rates are retained and labeled inadmissible, not silently clipped or refitted.

## Native measurements and controls

One process uses existing Python 3.12.14 and NumPy 2.5.3. For each case call `numpy.linalg.solve` in both physical coordinates `(a,b)` with matrix `[[1,0],[1,epsilon]]`, and integrated coordinates `(a,u)` with `u=epsilon*b` and matrix `[[1,0],[1,1]]`. Map the latter solution back to `(a,b)`. Retain all forty-two calls, original floating inputs, solutions, repriced values, residuals and exceptions.

For each spacing measure both matrix infinity-norm condition numbers using `numpy.linalg.cond(..., p=np.inf)`: eight calls. Exact references are `2*(1+epsilon)/epsilon` for the physical matrix and `4` for the integrated matrix. These are coordinate-dependent matrix norm measures; they are not direct confidence bounds on physical b. Record binary64 input representation error separately from the intended exact rational targets.

Before the run fix these checks: native physical parameters versus rational targets within absolute `1e-10` variance/year; original repricing residual at most `1e-12` total variance; coordinate reconstructions within absolute `1e-10`; condition numbers within relative `1e-12`. Check the exact uncertainty membership, rational interval extrema, admissible lower-bound witnesses and the expected counts. All controls and failures must be retained, not just aggregate success. Tolerances are synthetic study criteria, not institutionally accepted limits.

One attempt, one process, at most 120 seconds plus termination observation. No provider call, network, installation, retry or alteration of retained observations. An outer supervisor may terminate after 125 seconds. Set BLAS thread counts to one. Write a fresh output directory, with plan/source/package-binary hashes and environment identities. Commit raw observations before interpretation. A failed or partial process remains evidence and is not rerun under this allocation.

## Interpretation boundary

Compare exact solvability, native residual, interval width, variance admissibility and coordinate condition number separately. Do not infer probabilities from the uncertainty box, empirical model validity, production suitability, financial acceptance, agent reliability or operating savings. Existing calibration and sensitivity contracts may already cover these obligations; do not add a reusable definition without a distinct need.

## Sources

- [NumPy solve](https://numpy.org/doc/stable/reference/generated/numpy.linalg.solve.html): square-system solver API and singularity errors.
- [NumPy condition number](https://numpy.org/doc/stable/reference/generated/numpy.linalg.cond.html): infinity-norm option and matrix/inverse norm definition.
- Exact two-equation construction and bounds above are derived for this study; they are established linear algebra, not a novel numerical method.
