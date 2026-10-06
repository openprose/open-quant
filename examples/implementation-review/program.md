# Review implementation evidence for a pricing method

**For agents.** Execute under the caller's selected OpenProse kernel. The working root is the source repository, two directories above this program.

Adopt [implementation review](../../contracts/implementation-review.md) and [model description](../../contracts/model-description.md), including their adopted definitions, for one report. Apply [the review policy](inputs/policy.md) and [model brief](inputs/brief.md). The caller selects `complete`, `baseline-only` or `contradictory`; ask for an absent or unknown selection. Read only the corresponding [complete](inputs/complete.json), [baseline-only](inputs/baseline-only.json) or [contradictory](inputs/contradictory.json) numerical packet. The [receipt](receipt.json) identifies its calculation and projection; the [calculation source](model/measure.py) may be inspected for method and input mappings, not executed. Do not read other cases, reference reports or test answers.

Produce a report under 800 words excluding locators. Describe the method for an AI-literate financial operations reader. Account for the required cases, mappings, price comparisons, parity checks and invalid-input controls. Distinguish supplied observations, source inspection, missing records and producer claims. State what is met, breached or unresolved under the selected policy and what that establishes about the adapters. A complete report may identify failed criteria or incomplete implementation evidence.

Write only `report.md` and `result.md` in a fresh directory under `results/implementation-review/`. Identify the selected case, program, adopted definitions, policy, brief, numerical packet, receipt and calculation source by hash, calculations performed, remaining work and reporting fulfillment. Return the actual output path.

Use only the selected sources and definitions. Basic arithmetic and identity checks are permitted. Preserve sources and earlier outputs. Do not run pricing code, fetch data, repair records, issue financial instructions or create approvals. Reading restrictions are instructions, not enforced filesystem isolation.
