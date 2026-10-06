# Distinguishing cases for counterparty-exposure review

These authored cases describe [counterparty-exposure review](../../contracts/counterparty-exposure.md). They are interpretation references, not observed agent judgments or an automated prose benchmark.

| Supplied evidence | Required distinction |
|---|---|
| A caller supplies an exposure definition, recognized netting sets, exclusive collateral allocations and matching component calculations. | Report the supported conclusion for those supplied facts and criteria. Arithmetic agreement does not independently establish their legal or institutional recognition. |
| Two separate sets belong to one counterparty; one has positive exposure and the other has a liability and excess collateral. | Common counterparty identity does not establish cross-set netting. Preserve the selected set boundaries and identify the effect of pooling. |
| Offsetting assets and liabilities across different counterparties produce a small signed portfolio total. | A signed total is not automatically aggregate positive counterparty exposure. Apply the caller's measure and grouping. |
| Positive-value collateral is pending settlement, or is settled but ineligible under the selected rules. | Balance, settlement and eligibility are distinct. Record the supplied value without automatically recognizing it as an exposure offset. |
| A haircut or the direction of an FX rate is changed while all resulting additions remain internally consistent. | Correct sums do not establish selected adjustment or conversion conventions. Preserve the binding and its effect. |
| Two trades and three collateral records are joined by netting set, producing six rows before aggregation. | Account for duplicated contributions on both sides. A balanced net result does not establish unique trade or collateral coverage. |
| A report floors each trade at zero before allowing offsets within a recognized set; the selected method floors after netting. | The operations are not interchangeable. A higher result is not automatic conformity to the requested measure. |
| Netting-set membership is missing, while aggregate trade and collateral amounts remain available. | Preserve known amounts and explicitly conditional calculations. Do not infer the missing grouping, report absent contributions as zero or certify the portfolio exposure. |
| Collateral balances are supplied without the recognition evidence required by the caller. | Distinguish a calculation conditional on recognition from an established recognized exposure. Missing evidence does not itself prove either eligibility or ineligibility. |
| A single allocation is credited to multiple sets, or surplus collateral is moved between them without supporting rules. | Retain allocation identity and restrictions; do not double count or infer transfer authority. |
| Received and posted collateral are given the same sign without the selected custody and recognition conventions. | Identify which obligations, rights and signs the selected method requires. Do not invent a universal treatment from the balance label. |
| Current exposure is zero and is reported as proof of zero potential future exposure or regulatory EAD. | Preserve measure and horizon distinctions. The current snapshot does not establish future, probability-weighted or regulatory quantities. |

The component reviews supplied evidence. Model execution, legal determinations and financial operations require their own scope and authority. These cases do not qualify an agent or implement a regulatory framework.

The [worked composition](../../examples/exposure-review/README.md) now supplies observed synthetic calculations, three evidence packets and an authored reference. It does not establish agent qualification.
