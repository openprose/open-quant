# Reproduce the synthetic optimization observations

This owned source solves seven prespecified two-variable problems with SciPy SLSQP and creates one separate rounded-weight artifact. All inputs and analytic reference calculations are explicit in [measure.py](measure.py). The inputs are synthetic assumptions, not financial forecasts or a proposed allocation. No network, model-provider call or financial action occurs.

The observed development environment is Python 3.12.14, SciPy 1.18.1 and NumPy 2.5.3. Reproduction requires an already provisioned environment; this source does not install dependencies. Select a nonexistent JSON output path in an existing directory outside the checkout. Use one attempt, one concurrent process and a 120-second external deadline, with BLAS/OMP threads limited to one. For example, from the repository root with the selected Python:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python -c 'import subprocess, sys; subprocess.run([sys.executable, "examples/optimization-review/model/measure.py", "/absolute/new-observations.json"], check=True, timeout=120)'
```

An existing output is refused. Retain failed output or stderr rather than retrying or changing the cases, settings or tolerances. The script records environment/source identity, native results, analytic references and implementation controls. Its process exit concerns those controls; individual solver failures remain in the output. Record the external execution state separately.

Timestamp and duration may differ between runs. Compare the specification, all seven solver records, derived candidate and controls with the selected receipt's observations. A changed result needs investigation; do not relabel it as agreement. Reference arithmetic and solver output do not establish agent-report fulfillment, economic suitability or institutional acceptance.

This developer reproduction permission is separate from any reporting program's scope. A report restricted to supplied evidence must not execute this source to reconstruct withheld observations.
