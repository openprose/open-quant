# Reproduce the synthetic selection study

The owned source generates 256 fixed replicates of 64 independent standard-normal selection/evaluation score pairs, then examines nested candidate counts 1,4,16,64. Every candidate has zero true effect in the specified model. These are dimensionless synthetic statistics, not financial returns, Sharpe ratios or a real strategy backtest.

The development environment is Python 3.12.14 and NumPy 2.5.3. From the source root, use a fresh output file:

```sh
mkdir -p results
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python examples/selection-review/model/measure.py results/selection-observations.json
```

The source refuses overwrite. It preserves every score vector, selected identity and outcome, with seed/spawn keys and byte hashes. It exits nonzero only for failed deterministic checks, preserving observations first. Observed frequencies are never required to equal theoretical expectations; no seed filtering or adaptive stopping occurs.

The three views are the selection maximum, independent evaluation of that same frozen candidate, and reselection of a winner on evaluation data. The latter is another selection exercise. Exact family probabilities assume independent standard-normal all-null scores; they are not a universal correction for dependent or adaptive financial searches, a posterior probability of economic success, or a probability-of-backtest-overfitting estimator.

This developer reproduction is outside the report's permissions. The program may read only its selected packet, brief, policy and receipt, not this all-case source as a replacement for missing evidence.
