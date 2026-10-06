# Model implementation and optional reproduction

bootstrap.py and hagan_west.py are unchanged OpenProse-owned model source from the predecessor revision in [the import manifest](../../../provenance/import.json). The first implements the two curve builds and reported comparisons; the second implements the Hagan–West monotone-convex method with retained attribution. They are supplied for inspection and optional numerical reproduction, not run by the documentation program.

The original scripts expect inputs in an out/ directory beside the source and generate numerical files and figures there. Use the reproduction helper so they operate in a fresh directory rather than changing the retained evidence:

```sh
python3 scripts/reproduce_sofr.py --output /absolute/new/sofr-reproduction
```

Run that command from the repository root using Python 3.12.14 with QuantLib 1.43, SciPy 1.18.1, NumPy 2.5.3 and Matplotlib 3.11.2 installed in an isolated environment. The helper checks dependency versions, copies the two original scripts and the committed derived quote/fixing inputs, and invokes the unchanged bootstrap. It then compares the numeric/structural result to the retained results.json, allowing relative tolerance 1e-10 and absolute tolerance 1e-12 per numeric leaf; keys, list lengths and nonnumeric values must match. It does not install dependencies, fetch market data, call an agent or change the source evidence. A failed reproduction remains in its requested output directory for diagnosis.

This reproduces the curve comparison conditional on those derived inputs. It does not rerun raw trade filtering/quote estimation or establish an institutional model review. Versioned packages may be unavailable in another environment; report that mismatch instead of silently substituting versions. [Source notices](../../../provenance/README.md#external-sources) describe the inputs and dependencies.

A fresh October 6, 2026 invocation matched the retained results under these tolerances; see [qualification and scope](../../../docs/qualification.md#october-6-2026-numerical-reproduction) and [the receipt](../../../provenance/reproduction/2026-10-06.json). Generated run_info.json retains original-project script names, including derive_quotes.py, which this helper does not execute.
