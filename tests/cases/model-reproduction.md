# Distinguishing cases for model reproduction

These are authored interpretations for [model reproduction](../../contracts/model-reproduction.md), not agent observations.

| Supplied situation | Required distinction |
|---|---|
| Selected implementation and inputs run within scope; outputs meet the caller's numeric and structural comparison. | Report the supported reproduction with exact scope and evidence. It does not establish model suitability or institutional acceptance. |
| Process exits zero, but no required result is written. | Execution settled successfully; required calculation evidence and comparison are unavailable. Reproduction is not established. |
| Process writes a matching result and later exits nonzero or times out. | Preserve the partial artifact and failure. A matching file does not override incomplete execution. Do not silently retry. |
| Process exits zero and produces a complete result outside tolerance. | Distinguish observed numerical mismatch from missing evidence and from process failure. Retain the result; do not relax tolerance or change the selected inputs. |
| A result contains malformed, nonfinite or ambiguous duplicate-key data. | Preserve the original bytes and report unusable comparison evidence. Do not silently choose a duplicate or interpret nonfinite data as equality. |
| Required versions or selected inputs are absent. | Report the unmet prerequisite without claiming a launch or reproduction. Installation or fetching needs its own authority. |
| A new run matches after changing a seed, dependency or input without authorization. | The requested selection was not reproduced under its agreement. A favorable later result does not erase the change or qualify the original attempt. |
| Source hashes match before and after execution, but no trace of intermediate behavior exists. | Report the matching identities within their scope. They do not prove every source-preservation or permission claim. |
| An honest report fully explains a failed attempt. | The report may fulfill a reporting-only obligation; it does not fulfill a separate requirement to reproduce the result. |

The bounded SOFR helper tests these process/evidence distinctions using small local fixtures. Those tests do not assess whether an agent follows the contract, validate an economic model or establish production isolation.
