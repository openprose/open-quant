# Reproduce the synthetic dependence calculations

This owned script constructs nine correlation candidates with fixed inputs and no random search or market data. It records joint/pairwise eigenvalues, factorization outcomes, missing-data observation memberships, two explicit adjustments and exposure-order calculations. All source records and adverse findings are retained in its output.

The development environment is Python 3.12.14 and NumPy 2.5.3. With those dependencies, run from the source repository root into a fresh output file:

```sh
mkdir -p results
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python examples/dependence-review/model/measure.py results/dependence-observations.json
```

The script refuses to overwrite a result. Its numerical tolerance is 1e-12; it exits nonzero on failure of a fixed analytic identity, preserving observations first. Cholesky rejection of a singular or indefinite candidate is an observation rather than a process failure. Tiny negative floating-point eigenvalues remain visible.

These are established mathematical constructions, not newly discovered numerical algorithms or statistical estimates from real markets. Matrices use variable order A,B,C unless explicitly permuted. Variance is in squared synthetic units for unit marginal scales, not money or a risk quantile. Clipping/rescaling is not generally a nearest-correlation algorithm; no adjustment is approved for production.

Reproduction is separate from the reporting invocation: the executor's selected packet determines its available evidence. This source embeds all constructions and is not an allowed substitute for records missing from that packet. The report does not authorize running this script.
