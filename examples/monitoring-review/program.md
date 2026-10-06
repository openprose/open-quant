# Report on a monthly model monitoring packet

**For agents.** Execute under the caller's selected OpenProse kernel. The working root is the repository or extracted-package root, two directories above this program; output paths below are relative to that root.

## Agreement

Produce a concise monitoring and open-issue report for the selected synthetic case. Adopt [model monitoring](../../contracts/model-monitoring.md) and [limitations and remediation](../../contracts/limitations-and-remediation.md), including their adopted reporting requirements. These contracts apply together to one report.

The caller supplies exactly one case name: `complete`, `missing` or `contradictory`. Use that case in [the evidence packet](inputs/packet.json), together with its shared model, expected-observation and issue records, and [the house policy](inputs/policy.md). If the case is absent or unknown, request it; do not silently choose an easier case. Other cases, authored reference outputs and test material are not evidence for the selected case.

The reporting period is September 2026 and the review date is October 5, 2026. The intended reader is an operating manager. Required institutional facts are the supplied synthetic owner and issue fields; missing facts remain unresolved. No claim of actual institutional approval is requested.

## Result

Write `report.md` and `result.md` in a fresh directory under `results/monitoring-review/`. The report must identify the case, account for all expected observations and supplied issue records, apply the exact house rules, explain contradictions and gaps, and state what response remains. Keep it under 650 words, excluding source locators. The report may fulfill this obligation while finding a breach, an overdue issue or missing observation; honest supported reporting is the requested outcome, not an all-clear finding.

In `result.md`, identify the chosen program, adopted definitions, policy and packet with file hashes, the output directory, checks performed and unfinished reporting work. State whether this reporting obligation was fulfilled separately from the control findings. File hashes identify inspected bytes; they do not prove content correctness.

## Permissions

Read only the selected case and shared inputs, the program and adopted definitions. Basic arithmetic on those inputs is permitted. Preserve all source files and previous results. Do not access the network, run financial model code, read sample-results or tests, alter issues or monitoring values, or send notifications. Repository-based read restrictions are instructions to the executor, not a filesystem isolation guarantee.
