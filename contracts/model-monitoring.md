# Review model monitoring

**For agents.** Adopt [operating report](operating-report.md).

The caller supplies the model revisions and uses, expected observations and reporting period, metric definitions, supplied observations, and the policy for thresholds, missing data and escalation. Thresholds and observation frequency are caller policy, not universal requirements of this contract.

Produce a monitoring report that maps every expected observation to its evidence or gap. Preserve metric direction, units, denominator, horizon and threshold boundary, including whether equality passes. Distinguish an observation outside the limit, an unavailable or invalid observation, and a valid observation within the limit. Do not count missing observations as passing or silently remove them from the denominator.

Compare reported statuses with the underlying evidence where available. Identify contradictions, stale observations, relevant changes in model use or inputs, and repeated exceptions within the supplied period. Describe trends only when the observations are comparable; a short or selected series does not establish continuing performance.

State required responses under the supplied policy and their evidenced status. Distinguish reporting a breach from resolving it. Within-limit observations do not by themselves establish model validity or fitness for every use.
