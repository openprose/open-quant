# Synthetic house policy

This policy is authored solely for the example. It is not a regulatory requirement or a recommended model-risk policy.

The expected population is exactly the four records in `expected_observations`. Match an observation using model ID, revision, metric and period. Preserve observation IDs and report unmatched or duplicate records; do not choose one ambiguous duplicate. A value must be a finite, nonnegative number in the expected unit; counts must also be integers. Missing or invalid evidence is unresolved, not within limit. The producer's label is a claim to check, not an override of the measured value.

- Maximum repricing error is **within limit at or below 1.0 bp**; greater values breach the limit.
- Missing required inputs are **within limit only at 0 count**; a positive count breaches the limit.

Report how many expected observations are within limit, breached and unresolved, always using four as the denominator. A complete, valid observation for every expected item is required for a control-wide all-clear claim. Any known breach makes the overall control finding `breach`; otherwise unresolved observations make it `unresolved`; otherwise it is `within limit`. A separate contradiction in a producer label must remain visible even when the underlying value is usable.

Review every supplied issue. Dates are calendar dates. An issue with a due date before October 5 and without adequate closure evidence is overdue. Closure requires an identified post-action observation for the same model revision and metric that is valid and within limit, plus a supplied review record accepting that evidence. A producer's closed label, an action-complete date, or a proposed observation does not establish closure. No review record is supplied in this packet.

For breaches, missing observations or unsupported closure, report that the relevant recorded owner needs to provide evidence or a disposition. This requirement does not authorize contacting the owner or resolving the issue. Do not invent an organizational risk-acceptance decision.
