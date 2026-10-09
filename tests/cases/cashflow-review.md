# Distinguishing cases for cash-flow review

These are authored interpretation cases for the [component](../../contracts/cashflow-review.md), not agent execution results. Synthetic arithmetic illustrates the requirements; it is not a market convention or a compliance determination.

| Supplied case | Required distinction |
|---|---|
| USD1 million receiving leg, 5% annual coupon, 90-day period, Act/360. Accrual ends Saturday February 28, 2026; Following on a weekends-only calendar gives payment March 2. Amount USD12,500. | Explain the supported amount and payment date under the supplied conventions. Payment adjustment does not extend the accrual period. A weekends-only calendar is not evidence of a real market holiday calendar. |
| The same required terms, but the producer uses Act/365 Fixed and obtains USD12,328.767123. Its implementation agrees with an independent calculation under that convention. | Preserve the successful arithmetic comparison and the breach of the selected Act/360 convention. Neither finding cancels the other. |
| Settlement is March 2. The selected first coupon pays on that date; one valuation includes it and another excludes it. Their difference is USD12,500 with settlement also the discount reference date. | Identify the two inclusion policies and populations. Do not infer a price error from the difference alone or substitute the global evaluation date for settlement. |
| An unadjusted-payment variant differs from the required Following variant by less than the caller's aggregate tolerance, but has incorrect payment dates. | Report the close valuation and the known convention breach separately. The aggregate comparison cannot establish flow-level compliance. |
| Final coupon C4 and principal P1 have the same date; a schedule retains only C4 after deduplicating by date. | Identify the missing principal obligation. Preserve distinct flow identities even when dates match; do not infer that the principal was paid elsewhere. |
| Amounts and totals are supplied without required fixing observations, calendar identity or schedule terms. | Report the supplied values and identify which conclusions lack evidence. A complete report about gaps is not evidence that the underlying cash flows meet every requirement. Missing evidence is not proof that calculations or fixings never existed. |
| A producer labels all generated flows paid, with no confirmation or settlement record. | Reject the payment claim as unsupported. Do not classify them as unpaid merely because confirmation is absent. |
| A valuation record is labeled clean price per 100, but its comparison is an absolute USD present value, with no accrued-interest or scale reconciliation. | Leave that comparison unresolved; matching digits or instrument IDs do not establish a common price basis. Do not invent normalization. |

These cases test the intended distinctions for review. Whether an agent preserves them requires execution and assessment against the selected agreement. No such qualification is claimed here.

## Worked report expectations

The [cash-flow/valuation composition](../../examples/cashflow-review/README.md) retains three constructions and six observed aggregate valuations.

- `complete`: Selected meets supplied conventions within this fixed scope. Wrong day count breaches Act/360; Unadjusted breaches Following payments even though its exclude-settlement comparison is within USD10. C4 and P1 remain distinct.
- `missing-schedule`: declared convention differences and aggregate values remain available. Actual flow dates/amounts and population reconciliation remain unresolved. Expected terms are not observations of withheld records.
- `contradictory`: all four producer claims are unsupported or contradicted. Close valuation does not clear dates; modeled obligations do not establish paid status; adjusted payment does not extend accrual; shared dates do not remove principal.

No case supplies payment confirmation. Paid and unpaid are both unsupported conclusions. An accurately supported adverse report can fulfill the reporting agreement.
