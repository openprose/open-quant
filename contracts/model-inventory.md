# Reconcile a model inventory

**For agents.** Adopt [operating report](operating-report.md).

The caller supplies the inventory snapshot, comparison population or discovery evidence, identity and inclusion rules, required inventory fields, and any model classification policy. An inventory snapshot alone cannot establish that every model in the organization is registered.

Produce a review identifying each in-scope model, its recorded revision, purpose and use, responsible roles, lifecycle state, and other caller-required attributes. Preserve the distinction between a model, an implementation, a deployment and a vendor version under the supplied identity rules; do not collapse these because their names match.

Account for records on both sides of the comparison. Identify omissions, ambiguous duplicates, stale or conflicting attributes and dependencies visible in the supplied evidence. Associate findings with exact source records. Apply supplied classification criteria only where the evidence supports them; distinguish an assigned classification from your proposed classification.

Report coverage and the specific facts needed to resolve discrepancies. This is an inventory review, not an update to the authoritative register or proof of a complete organization-wide discovery.
