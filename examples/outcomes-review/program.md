# Compare cash-flow predictions with observed outcomes

**For agents.** Execute under the caller's selected OpenProse kernel. The working root is the root of the source repository, two directories above this program.

Adopt [outcomes analysis](../../contracts/outcomes-analysis.md) and [model data](../../contracts/model-data.md), including their adopted definitions, for one report. Apply [the comparison policy](inputs/policy.md). The caller selects `complete`, `missing` or `late-forecast`; ask for an absent or unknown selection. Read only the corresponding [complete](inputs/complete.json), [missing](inputs/missing.json) or [late-forecast](inputs/late-forecast.json) packet, not alternative cases or reference reports.

Produce a report under 700 words excluding locators. Account for every expected observation and both models' evidence, maturity, timing and pairing eligibility. Show each model's descriptive metric and a matched-population comparison with explicit denominators. Explain whether the producer's comparative claim is supported, the scope of the finding, and remaining uncertainty. An accurate report can fulfill this obligation while leaving a full-cohort comparison unresolved.

Write only `report.md` and `result.md` in a fresh directory under `results/outcomes-review/`. Identify the case, program, adopted definitions, policy and evidence by hash, performed calculations, remaining work and reporting fulfillment. Return the actual output path.

Use only the selected sources and definitions. Basic arithmetic and timestamp checks are permitted. Preserve sources and earlier outputs. Do not train, tune or run models, fetch observations, fill missing outcomes, issue financial instructions or change operational approvals. Reading restrictions are instructions, not enforced filesystem isolation.
