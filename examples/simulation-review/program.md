# Review simulation precision and the estimated quantity

**For agents.** Execute under the caller's selected OpenProse kernel. The working root is the source repository, two directories above this program.

Adopt [simulation review](../../contracts/simulation-review.md) and [implementation review](../../contracts/implementation-review.md), including their adopted definitions, for one report. Apply [the review policy](inputs/policy.md) and [simulation brief](inputs/brief.md). The caller selects `complete`, `missing-large-sample` or `contradictory`; ask for an absent or unknown selection. Read only the corresponding [complete](inputs/complete.json), [missing-large-sample](inputs/missing-large-sample.json) or [contradictory](inputs/contradictory.json) packet. The [receipt](receipt.json) identifies its calculation and projection; the [calculation source](model/measure.py) may be inspected for construction and method, not executed. Do not read other cases, reference reports or test answers.

Produce a report under 800 words excluding locators for an AI-literate financial operations reader. Account for all selected sample sizes and views. Distinguish the target quantity, sampling units, uncertainty assumptions, observed precision and producer claims. Explain which selected criteria are met, breached or unresolved and what the available evidence cannot establish. A report can fulfill this obligation while finding an invalid method or unavailable result.

Write only `report.md` and `result.md` in a fresh directory under `results/simulation-review/`. Identify the selected case, program, adopted definitions, policy, brief, numerical packet, receipt and calculation source by hash. State calculations performed, remaining work and reporting fulfillment; return the actual output path.

Use only the selected sources and definitions. Basic arithmetic and identity checks are permitted. Preserve sources and earlier outputs. Do not generate samples, run pricing code, fetch data, repair records or issue approvals. Reading restrictions are instructions, not enforced filesystem isolation.
