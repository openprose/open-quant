# Exposure-ledger review

Review one synthetic valuation snapshot, 2026-10-06T00:00:00Z, in USD. The caller's `selected_method` specifies intended group membership, amounts, recognition inputs and measure. `observed_calculation_inputs` records what the calculation actually used. These roles remain separate even where their values agree.

The source population is six trades and six received-collateral records in three sets. NS-A1 and NS-A2 share counterparty CP-A; NS-B1 belongs to CP-B. Netting recognition is stipulated for this example rather than established by an actual legal agreement. Do not infer permission to net across sets or counterparties. The selected collateral allocations are exclusive; there is no posted collateral, reuse or dynamic margin calculation.

Native SQL rows and exact references describe nine deliberately different constructions. Their identifiers, including `selected_sets`, are implementation labels, not proof that a construction conforms to the supplied requirements. A difference from the `selected_sets` construction is an observed comparison, not an independently established difference from the caller's intended result when a selected binding is missing.

The task is an evidence review. It does not establish actual settlement, enforceability, institutional recognition, future exposure, EAD, CVA, regulatory capital or operational savings. Identify missing facts that limit a conclusion without inventing them or treating them as zero.
