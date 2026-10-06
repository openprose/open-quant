# Reproduce the synthetic simulation

The owned [measure.py](measure.py) uses 64 fixed PCG64DXSM streams, two nested sample sizes and four deliberately labeled estimator views. It performs no network retrieval or model API call. The example packets select replicate 0 by index; the script retains all replicates and interval outcomes.

The retained run used Python 3.12.14, NumPy 2.5.3, SciPy 1.18.1 and QuantLib 1.43 on macOS ARM64. The script requires those versions, uses a POSIX 120-second alarm and refuses an existing output path. Dependency installation is a separate caller action; use an isolated environment. Other operating systems and numerical builds are not qualified. Dependencies retain their own licenses.

An explicitly requested reproduction from the source root is:

```sh
mkdir -p results
python examples/simulation-review/model/measure.py --output results/simulation-evidence-new.json
```

Use a fresh output path. Source/native hashes, exact inputs, stream construction, moments, intervals, algebraic discrepancies and timing are recorded. Exit zero means the selected algebraic relationships and closed-form/reference comparison pass; it does not mean every interval contains the requested target or every estimator meets the report's house policy. No intervals or seeds are selected after seeing outcomes.

The [receipt](../receipt.json) identifies the October 6 observations underlying the example. A subsequent reproduction is new evidence and must not silently replace those packets. The reporting program permits source inspection and arithmetic, not execution of this script.
