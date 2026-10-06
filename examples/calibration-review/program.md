# Review SOFR input repricing

**For agents.** Execute under the caller's selected OpenProse kernel. The working root is the repository or extracted-package root, two directories above this program.

Adopt [calibration review](../../contracts/calibration-review.md) and [model data](../../contracts/model-data.md), including their adopted definitions, for one report. The caller selects `complete`, `missing` or `contradictory`; ask for an absent or unknown selection. Use only its corresponding table: [complete](inputs/repricing.csv), [missing](inputs/missing.csv) or [contradictory](inputs/contradictory.csv). Alternative case tables and reference reports are outside the execution's reading scope.

Apply [the review policy](inputs/policy.md). Supplied model context is the SOFR [brief](../sofr-curve/inputs/brief.md), [quote population](../sofr-curve/inputs/quotes.csv), [fixing](../sofr-curve/inputs/sofr-fixing.json), [historical result](../sofr-curve/inputs/results.json), and unchanged [bootstrap](../sofr-curve/model/bootstrap.py) and [Hagan–West implementation](../sofr-curve/model/hagan_west.py). The [reproduction receipt](../../provenance/reproduction/2026-10-06.json) identifies the complete table's calculation. The two altered tables are authored challenges, not outputs covered by that receipt.

Produce a report under 700 words excluding locators. Account for the expected calibration population and exclusions, explain the residual definition and numerical precision, and give supported, breached or unresolved fit findings for each method. Identify conflicts with summaries or displayed rates without repairing source records. Distinguish input fit from independent validation and solver settings from observed diagnostics. A report can fulfill this obligation by accurately reporting adverse or incomplete evidence.

Write only `report.md` and `result.md` to a fresh directory under `results/calibration-review/`. Identify the selected case, program, adopted definitions, policy and evidence by hash, checks performed, remaining evidence needs and reporting fulfillment. Return the actual output path.

Use only supplied sources. Basic arithmetic and source inspection are allowed. Preserve sources and prior outputs; do not run or recalibrate models, fetch data, supply missing values from another case, or claim institutional approval. Reading boundaries are instructions, not enforced filesystem isolation.
