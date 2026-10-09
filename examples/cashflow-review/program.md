# Review a coupon schedule and its valuation

**For agents.** Execute under the caller's selected OpenProse kernel. The working root is the source repository, two directories above this program.

Adopt [cash-flow review](../../contracts/cashflow-review.md) and [valuation comparison](../../contracts/valuation-comparison.md), including their adopted definitions, for one report. Apply [the brief](inputs/brief.md) and [review policy](inputs/policy.md). The caller selects `complete`, `missing-schedule` or `contradictory`; ask for an absent or unknown selection. Read only the corresponding [complete](inputs/complete.json), [missing-schedule](inputs/missing-schedule.json) or [contradictory](inputs/contradictory.json) packet and [receipt](receipt.json).

Produce a report under 900 words excluding locators for an AI-literate financial operations reader. Account for three constructions, five expected obligations in each, and both settlement-inclusion choices. Compare the evidence with the required accrual/payment conventions separately from arithmetic agreement and aggregate valuation tolerance. Explain known discrepancies, unavailable evidence and unsupported producer claims. Distinguish modeled cash flows from evidence of payment.

Write only `report.md` and `result.md` in a fresh directory under `results/cashflow-review/`. Identify the selected case, program, adopted definitions, brief, policy, packet and receipt by computed hash. Attribute calculation-source identity to the receipt rather than claim to have inspected or reproduced it. State checks performed, remaining work, reporting fulfillment and the actual output path.

Use only those sources and definitions. Arithmetic and identity checks are permitted. Do not inspect the reproduction source, other case packets, reference report or test answers to replace missing evidence. Do not generate missing observations, fetch data, change terms, book adjustments, transfer money or issue approvals. Reading restrictions are instructions, not enforced filesystem isolation.
