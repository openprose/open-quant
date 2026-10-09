# Reproduce finite portfolio-loss calculations

This developer calculation is outside the reporting agent's permissions. It uses Python 3.12.14, NumPy 2.5.3 and SciPy 1.18.1. Dependency installation and environment selection are separate prerequisites. Select a fresh observation file outside this checkout and preserve the exact source revision.

From the repository root, in that existing environment:

```python
import os
from pathlib import Path
import subprocess
import sys

output = Path("../portfolio-tail-observations.json").resolve()
if output.exists():
    raise SystemExit("Choose a fresh output path.")
subprocess.run(
    [sys.executable, "examples/portfolio-tail-review/model/measure.py", str(output)],
    check=True, timeout=120,
    env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1", OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1"),
)
```

The source refuses an occupied observation file. One process evaluates six fixed dependence proposals and sixteen confidence-level summaries; each native tail-allocation program has a five-second limit. No failed attempt is replaced. Two incompatible proposals retain negative state probabilities and receive no risk calculation. No simulation, market retrieval, provider call or financial operation occurs.

Exact Fraction references, observed native CDFs and native quantiles are separate records. A native/exact quantile disagreement is retained even when the implementation controls pass. Do not silently replace native values with exact references or retune the confidence level. Floating environments and dependency revisions are part of the result identity.

[The SciPy quantile interface](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.rv_discrete.ppf.html) and Rockafellar and Uryasev's [general-distribution treatment](https://sites.math.washington.edu/~rtr/papers/rtr187-CVaR2.pdf) explain the relevant definitions. The source is owned example code with constructed inputs, not copied paper code or a third-party dataset. Exact enumeration does not establish that the synthetic distribution represents a real portfolio or that an agent fulfills the reporting contract.
