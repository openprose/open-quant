# Simulation evidence review

**Authored reference for the complete case; not an agent-generated report or assessment.** Subject: BLACK-SIMULATION-2026-10-06, replicate 0, October 6, 2026. Source and numerical identities are recorded in the receipt.

The requested quantity is the discounted expected European-call payoff under the supplied lognormal terminal-forward model. Forward and strike are 100 USD per unit, annual volatility 0.3, expiry two years and continuous rate 0.05. The reference present value is about 15.2009041 USD per unit; omitting discounting changes the target to about 16.7995971. No production-use or approval record is supplied, so those institutional facts remain unresolved. [Sources: inputs/brief.md; inputs/complete.json: inputs, target prices.]

Both selected sample sizes and all four views are supplied once. The sizes are nested prefixes of stream 0, and all four views share draws. They are not independent corroborating estimates. The duplicate views contain 2N records from N original units. Known-pair grouping recovers those N units; treating all rows as independent does not. [Sources: inputs/complete.json: observations; model/measure.py: main.]

| Underlying draws | View | Recorded rows | Units used for uncertainty | Estimate | Standard error |
|---:|---|---:|---:|---:|---:|
| 4,096 | independent_units | 4,096 | 4,096 | 15.004107 | 0.454262 |
| 4,096 | duplicated_naive | 8,192 | 8,192 | 15.004107 | 0.321192 |
| 4,096 | duplicated_grouped | 8,192 | 4,096 | 15.004107 | 0.454262 |
| 4,096 | omitted_discount | 4,096 | 4,096 | 16.582103 | 0.502037 |
| 16,384 | independent_units | 16,384 | 16,384 | 15.194391 | 0.223995 |
| 16,384 | duplicated_naive | 32,768 | 32,768 | 15.194391 | 0.158386 |
| 16,384 | duplicated_grouped | 32,768 | 16,384 | 15.194391 | 0.223995 |
| 16,384 | omitted_discount | 16,384 | 16,384 | 16.792399 | 0.247553 |

Values are USD per unit under each view’s stated convention; omitted_discount is undiscounted. Display values are rounded to six decimals. Exact packet values determine the 0.30 precision comparison. Duplication preserves the estimate but reduces the naive standard error by sqrt((N-1)/(2N-1)), about 29.3%. Grouping restores the original standard error. [Source: inputs/complete.json: observations[].views.]

| View | Requested target | Uncertainty method | Precision requirement at 16,384 draws |
|---|---|---|---|
| independent_units | Met | Met within stated approximation | Met |
| duplicated_naive | Met | Breached: dependent rows treated as independent | Breached: unsupported method |
| duplicated_grouped | Met | Met within stated approximation | Met |
| omitted_discount | Breached: different expectation | Met for its actual expectation | Breached: different target |

All four large-sample standard errors are numerically below 0.30. That alone cannot clear the naive or undiscounted view: the policy also requires compatible uncertainty and the requested quantity. Correct grouping is a separate reported view, not permission to relabel the naive report. The larger observed sample has smaller reported sampling error than the smaller one; the omitted-discount estimate remains an estimate of a different quantity. [Sources: inputs/policy.md; inputs/brief.md; inputs/complete.json.]

The nominal 95% t intervals are approximations for nonnormal payoff means. They concern sampling variability under the supplied model, not parameter, data or model uncertainty. Stream construction and hashes support reproducibility without proving independence. Terminal values are sampled directly, with no time-discretization approximation. Sizes and seeds were fixed, with no precision-based stopping or favorable-seed selection. Two prefixes of one stream cannot establish general confidence-interval coverage or financial suitability. [Sources: inputs/brief.md; model/measure.py; receipt.json.]

All required records are accounted for in this case. The supported adverse findings do not prevent fulfillment of the reporting obligation. This reference does not establish actual execution-boundary compliance; a real invocation must provide its own result record, hashes and assessment.
