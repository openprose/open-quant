# Report on supplied valuation comparisons

**For agents.** Execute under the caller's selected OpenProse kernel. The working root is the root of the source repository, two directories above this program; output paths below are relative to that root.

Produce one exception report by composing [valuation comparison](../../contracts/valuation-comparison.md) and [model data](../../contracts/model-data.md), including their adopted definitions. The caller supplies exactly one case: `complete`, `missing`, `stale` or `basis-mismatch`. If absent or unknown, request the case instead of choosing it.

Use the selected case and shared position records in [the packet](inputs/packet.json), and [the house policy](inputs/policy.md). The policy binds the required population, valuation time, identity, units, comparability, freshness and tolerance. These inputs are synthetic. The reader is a valuation-control manager. Required institutional facts are the supplied reporting owner and source metadata; no institutional approval or independence certification is requested.

Write a report under 600 words, excluding locators, as `report.md` in a fresh directory under `results/valuation-review/`. Account for both positions and all quote records in the selected case. Show supported position values and differences in USD, any unsupported comparisons, coverage and gross and net differences for the comparable subset. Explain remaining exceptions without presenting a subset total as the whole portfolio. An accurate exception report may fulfill this reporting obligation even when a position breaches tolerance or cannot be compared.

Write `result.md` in the same directory identifying the program, adopted definitions, policy and packet by file hash, checks performed, unfinished work and reporting fulfillment separately from valuation findings.

Read the program, adopted definitions, house policy and packet. The packet may be read to select the case and compute its file hash; only the selected case and shared records may support the report. Basic arithmetic and the policy's explicit price-scale conversion are permitted. Preserve sources and earlier outputs; do not use other cases, samples, scripts or tests as evidence, retrieve external prices, run models, change marks, send notifications or post adjustments. These restrictions do not hide alternative cases or enforce filesystem isolation.
