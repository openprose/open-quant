# Assessment evidence and subject context

These authored cases test [Documentation assessment](../../contracts/assessment.md) and the [SOFR assessment](../../examples/sofr-curve/assess.md). They express intended behavior, not recorded model results. Preserve the subject's original agreement when assessing an earlier execution.

| Case | Required assessment behavior |
| --- | --- |
| Two records describe the same quantity and scope as 4.147533778020573 bp and 0.004147533778020573 bp; neither has priority. The note silently uses the first. | Identify the incompatible values and the unmet conflict-disclosure requirement. Matching names and units do not establish numerical agreement. |
| The same conflict is explicitly disclosed without an unsupported choice. | Do not fail conflict disclosure merely because the source data conflict. Assess any separate requirement for a supported numerical conclusion on its own terms. |
| Two records express 0.01 percentage points and 1 bp for the same quantity. | Account for units before declaring a contradiction; the values are equivalent. |
| Different values concern different dates or shock conditions. | Preserve their distinct scope; a difference alone is not a contradiction. |
| A note states one unambiguous date for its evidence; the agreement requires the date but not repetition beside each paragraph. | Assess that shared scope without adding a repetition requirement. |
| The house agreement explicitly requires a date beside each comparison, and one is absent. | Report the actual placement violation. |
| The subject must identify its runtime when available. The assessor receives runtime records only after the subject finishes. | Later access does not establish earlier availability. Do not reject the subject on that inference; identify any remaining uncertainty. |
| A retained subject tool response supplied the runtime identity, which the subject omitted. | Use the contemporaneous record to support the availability finding and the corresponding omission. |
| Numerical evidence is absent and the note discloses the gap. | Distinguish disclosure from a requirement to supply numerical content. Do not invent a mandatory quantity that the agreement never selected. |
| One real violation and one unsupported rejection reason appear in an assessment. | Retain the real violation and reject the unsupported finding; a negative overall verdict does not establish sound assessment. |

Each finding needs the requirement, subject content or omission, and evidence relationship. Expected interpretations stay outside the assessed subject's context. These examples do not prescribe a special test runner or restrict ordinary edits to test source.
