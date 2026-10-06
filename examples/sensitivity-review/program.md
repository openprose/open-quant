# Review numerical sensitivity evidence

**For agents.** Execute under the caller's selected OpenProse kernel. The working root is the source repository, two directories above this program.

Adopt [sensitivity review](../../contracts/sensitivity-review.md) and [implementation review](../../contracts/implementation-review.md), including their adopted definitions, for one report. Apply [the brief](inputs/brief.md) and [review policy](inputs/policy.md). The caller selects `complete`, `missing-unrounded` or `contradictory`; ask for an absent or unknown selection. Read only the corresponding [complete](inputs/complete.json), [missing-unrounded](inputs/missing-unrounded.json) or [contradictory](inputs/contradictory.json) packet and [receipt](receipt.json).

Produce a report under 1,000 words excluding locators for an AI-literate financial operations reader. Account for all three cases, six bumps and two representations, preserving unavailable observations. Report delta and gamma findings separately. Distinguish price accuracy, derivative error, rounding-only bounds and finite premium changes. Explain how precision and perturbation scope affect the conclusion without selecting only favorable rows or inventing an optimal bump.

Write only `report.md` and `result.md` in a fresh directory under `results/sensitivity-review/`. Identify the case, program, adopted definitions, brief, policy, packet and receipt by computed hash. Attribute calculation-source identity to the receipt rather than claim to have inspected or reproduced it. State checks performed, remaining work, reporting fulfillment and the actual output path.

Use only those sources and definitions. Arithmetic and identity checks are permitted. Do not inspect the reproduction source, other packets, reference report or test answers to replace missing evidence. Do not generate new prices or sensitivities, fetch data, change source records, select hedges or issue approvals. Reading restrictions are instructions, not enforced filesystem isolation.
