# Reproduce the synthetic calculation

The owned [measure.py](measure.py) constructs ten synthetic European-option cases, compares three QuantLib input mappings with numerical payoff integration, and records twelve invalid-input controls. It performs no market-data retrieval or model API call. Two mappings are deliberately incorrect; findings concern these adapters, not QuantLib defects.

The retained run used Python 3.12.14, QuantLib 1.43 and SciPy 1.18.1 on macOS ARM64. The script requires those versions, uses a POSIX 120-second alarm and refuses an existing output file. It has not been qualified on Windows or across numerical-library builds. Dependency installation is a separate caller action; use an isolated environment with these versions. QuantLib and SciPy retain their own licenses.

From the source repository root, an explicitly requested reproduction is:

```sh
mkdir -p results
python examples/implementation-review/model/measure.py --output results/implementation-evidence-new.json
```

Use a fresh output path. The script records its own and QuantLib's native-extension hashes, exact inputs, prices, numerical-reference diagnostics, comparisons and timing. Exit zero means its selected reference, correct-adapter and rejection checks passed; deliberately incorrect adapters may still fail. It is not an all-adapters acceptance signal. The [receipt](../receipt.json) binds the committed example packets to the October 6 observed calculation. A subsequent reproduction is new evidence and must not overwrite that receipt or silently replace the supplied packets.
