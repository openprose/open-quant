# Reproduce the synthetic credit-loss calculation

This developer calculation is separate from the reporting agent's permissions. The source uses Python 3.12.14 and QuantLib 1.43; its exponential controls use the Python standard library. Install and select dependencies separately. Do not change an occupied result or a retained source revision.

From the repository root, with that environment already available, use one bounded process and a fresh output path outside this checkout:

```python
import os
from pathlib import Path
import subprocess
import sys

output = Path("../credit-loss-observations.json").resolve()
if output.exists():
    raise SystemExit("Choose a fresh output path.")
subprocess.run(
    [sys.executable, "examples/credit-loss-review/model/measure.py", str(output)],
    check=True, timeout=120,
    env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"),
)
```

The source refuses to replace an existing observation. It records all six constructions, four intervals, QuantLib probability outputs and independent 50-digit Decimal references. One attempt is the reproduction scope; a failure is evidence to retain, not permission to retry. No network, provider call or financial operation is involved.

Times are exact year fractions rather than calendar anniversary dates. The flat hazard, exposure, severity and interval-end settlement assumptions are synthetic. Five constructions deliberately change selected bindings. This does not estimate real default probabilities, implement an accounting standard or establish model acceptance.

Probability definitions follow QuantLib 1.43's [default term structure](https://github.com/lballabio/QuantLib/blob/v1.43/ql/termstructures/defaulttermstructure.hpp) and [flat-hazard implementation](https://github.com/lballabio/QuantLib/blob/v1.43/ql/termstructures/credit/flathazardrate.hpp). The calculation source here is owned example code; no third-party source is copied. Numerical reproduction does not establish that an agent fulfills the reporting contract.
