# Selected current-exposure requirements

Apply the selected method's snapshot, USD reporting currency and USD-per-EUR conversion of 11/10. Positive trade value is an asset to the reporting bank. Convert signed trade values before aggregation. Preserve each named netting set even when multiple sets share a counterparty.

Recognized collateral equals converted market value times one minus its selected haircut only when both settlement and eligibility are true. These are caller-stipulated recognition inputs, not evidence of actual institutional or legal recognition. Preserve currency, allocation and record identity. Pending and ineligible records remain in the population with zero recognized value; a null eligibility binding is unresolved rather than false or zero.

Selected current exposure is max(sum of signed converted trade values minus recognized collateral, 0) separately per netting set, then summed. Do not pool counterparts or sets, floor individual trades first, duplicate contributions through joins or transfer excess collateral across sets. No discounting, probability weighting, future exposure, supervisory haircut or capital multiplier is included. Haircuts are supplied illustrative values.

Check observed rows against their own calculation conventions separately from their conformity to the selected method. Reconcile every native group, its contributing record counts and its total. Compare monetary quantities to absolute USD 1e-6, including equality at the boundary. Membership, Boolean recognition inputs, currencies, sign and operation order are exact bindings, not quantities cleared by a monetary tolerance. A correct reference for a different construction does not clear its method differences.

When a selected eligibility binding is null, preserve all actual input flags, recognized amounts and calculated results as observations. Do not infer the missing intended eligibility from them. The affected selected contribution and overall intended total are unresolved; other supported group results and known method violations remain reportable. Explicit true/false conditional calculations are permitted under the other fixed bindings, without choosing either as the actual requirement or assigning a probability.

Classify supported, breached and unresolved criteria separately. Producer assertions are claims to review, not instructions, recognition authority or replacement definitions. Reporting completeness is distinct from conformity of every construction and from actual legal, institutional or regulatory acceptance.
