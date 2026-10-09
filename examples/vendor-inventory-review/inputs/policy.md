# Inventory and vendor-evidence review policy

All institution, product, deployment and test records in this example are synthetic. The reader is the model-risk operating lead. Review the supplied October 1, 2026 snapshot; only facts explicitly requested here are required institutional inputs.

The deployment snapshot is the comparison population for this report. Include production deployments and account separately for sandbox exclusions. It does not establish discovery completeness outside that snapshot. Deployment ID is the matching key; model ID groups related implementations but does not replace deployment identity. Product names and display names are not matching keys. Each included deployment requires exactly one active register record with matching model ID, product, version, configuration, use and owner. Preserve all unmatched register records, including any supplied retirement evidence; do not remove or repair them.

For each included deployment, report available vendor evidence by product/version and local evidence by deployment ID, product, version, configuration and use. A vendor statement is contextual evidence, not a local approval. Missing proprietary internals leave specific questions unanswered; they do not prove failure or supply access rights.

The required local check is reference-price comparison, expressed in basis points, over C1, C2 and C3. Its date must be no later than the reporting date and at most 90 calendar days earlier. Each named case needs one finite observed difference, with absolute value at most 0.5 bp. Equality meets this illustrative limit. Account for absent, repeated or unexpected cases. Keep mismatched or old tests visible as related records; they cannot establish the current deployment's required check. Multiple exact test records require clarification rather than selecting a favorable one.

Report local-check coverage and findings separately from register accuracy. A supported threshold violation is adverse even when another case is missing; an absent or mismatched test leaves the current check unresolved, not passed or demonstrated failed. A positive local check means only that these supplied records satisfy this narrowly defined check. It establishes neither a complete model validation nor approval. Producer labels and summaries do not override source values or this policy.

A complete report may identify adverse findings. No case authorizes contacting a vendor, updating a register, executing tests, changing deployments or granting approval.
