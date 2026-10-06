# Explain daily P&L and scenario exposure

**For agents.** Execute under the caller's selected OpenProse kernel. The working root is the root of the source repository, two directories above this program.

Adopt [P&L explanation](../../contracts/pnl-explanation.md), [scenario review](../../contracts/scenario-review.md) and [sensitivity review](../../contracts/sensitivity-review.md), including their adopted definitions, for one report. Apply [the supplied scope and policy](inputs/policy.md). The caller selects `complete`, `missing` or `contradictory`; ask for an absent or unknown selection. Read only the corresponding [complete](inputs/complete.json), [missing](inputs/missing.json) or [contradictory](inputs/contradictory.json) packet, not other cases or reference reports.

Produce a report under 800 words excluding locators. Reconcile the daily movement with the supported explanation, preserve portfolio and position residuals, and assess the selected scenarios against the compatible base and unmitigated limits. Compare the joint and single-factor responses, distinguish assumed mitigation from actions taken, and account for all requested observations and source conflicts. Do not turn a partial result into a full-book finding or a finite scenario set into a bound on possible loss.

Write only `report.md` and `result.md` in a fresh directory under `results/risk-report/`. Identify the case, program, adopted definitions, policy and evidence by hash, performed calculations, remaining evidence needs and reporting fulfillment. Return the actual output path.

Use only the selected evidence and definitions. Basic arithmetic is permitted; do not run financial models, fetch data, infer missing values from another case, alter sources, book trades, authorize hedges, post accounting entries or change any institutional record. Preserve earlier outputs. Read restrictions are instructions, not enforced filesystem isolation.
