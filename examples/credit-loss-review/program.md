# Review default probabilities and credit-loss calculations

**For agents.** Execute under the caller's selected OpenProse kernel. The working root is the source repository, two directories above this program.

Adopt [credit-loss review](../../contracts/credit-loss-review.md) and [implementation review](../../contracts/implementation-review.md), including their adopted definitions, for one report. Apply [the brief](inputs/brief.md) and [review policy](inputs/policy.md). The caller selects `complete`, `missing-severity` or `contradictory`; ask for an absent or unknown selection. Read only the corresponding [complete](inputs/complete.json), [missing-severity](inputs/missing-severity.json) or [contradictory](inputs/contradictory.json) packet and [receipt](receipt.json).

Produce a report under 1,100 words excluding locators for an AI-literate financial operations reader. Account for all six constructions and four intervals. Distinguish observed arithmetic, probability interpretation, selected exposure/severity and loss timing. Preserve known violations alongside unresolved requirements; actual parameters do not establish a missing intended binding. Address any producer claims against the permitted evidence.

Write only `report.md` and `result.md` in a fresh directory under `results/credit-loss-review/`. Identify the case, program, adopted definitions, brief, policy, selected packet and receipt by computed hash. Attribute calculation-source identity to the receipt rather than claim to have inspected or reproduced it. State checks performed, remaining work, reporting fulfillment and the actual output path.

Use only those sources and definitions. Arithmetic and identity checks are permitted. Do not inspect reproduction source, other packets, reference reports or test answers to reconstruct withheld requirements. Do not rerun the calculation, fetch data, estimate default probabilities, change bindings, book reserves or make credit decisions. Reading restrictions are instructions, not enforced filesystem isolation. An accurate report may identify violations and missing evidence; an all-clear finding is not required.
