# Reproduce the historical-selection observations

[measure.py](measure.py) contains thirteen synthetic feature records, ten decision requests, six SQLite queries and a separate Python selection reference. The fixed copy-the-feature prediction rule has deliberately planted later outcomes. It is a demonstration of evidence requirements, not a financial model or forecasting benchmark.

The observed environment is Python 3.12.14 with SQLite 3.53.1. Only the Python standard library is used; no dependencies are installed and no network, model-provider call or financial action occurs. Use an already provisioned environment and a nonexistent output path in an existing directory outside the source checkout. One attempt, one process and a 120-second deadline are sufficient for the declared reproduction scope. From the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python -c 'import subprocess, sys; subprocess.run([sys.executable, "examples/availability-review/model/measure.py", "/absolute/new-observations.json"], check=True, timeout=120)'
```

The script refuses an existing output and retains every requested selection. Compare its exact tables, scope, selected IDs, diagnostic reasons, numeric metrics and controls with the selected observation. Timestamp and duration may differ. Preserve failures; do not retune the data, queries or comparison population to obtain a preferred metric. Record external completion and environment separately.

All known timestamps use normalized UTC strings at second precision. This fixed construction does not test time-zone conversion, actual historical ingestion, production databases or a general duplicate-resolution policy. The only selected highest-version conflict contains different values.

Reproduction is a developer action with its own scope. An agent reviewing a supplied missing-history packet is not authorized to run this source or inspect other cases to reconstruct withheld observations.
