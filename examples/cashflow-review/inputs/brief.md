# Synthetic coupon-leg review

Review CASHFLOW-2026-10-06, a synthetic receiving USD1 million fixed-rate leg with 5% simple annual coupons. This is documentation and evidence review, not a traded security, a market valuation or an instruction to pay. The expected population is C1–C4 coupons plus P1 principal in each construction. Principal is USD1 million at the final payment date, separate from the last coupon.

Unadjusted accrual boundaries are November 30, 2025; February 28, May 31, August 31 and November 30, 2026. Required accrual is Actual/360. Required payments roll Following on a weekends-only calendar; this is not a real holiday calendar. Payment adjustment does not change accrual endpoints. No floating fixings, fees, principal amortization, optionality, ex-coupon period, tax or default is in scope.

Settlement and discount reference date are March 2, 2026. The supplied hypothetical discount function is continuous 4%, Actual/365 Fixed time from that date. Values are absolute USD present values, not prices per 100 or clean/dirty price quotes. The calculation's QuantLib global evaluation date is February 27, distinct from settlement. Review both explicit settlement-flow inclusion choices; past flows are excluded under either.

The selected construction follows the required conventions. Two deliberate variants use Actual/365 Fixed accrual or unadjusted payments. Their arithmetic can be correct for their own terms without meeting the required terms. Review observed evidence before concluding that a declared construction has been implemented correctly.

The receipt identifies a CPU calculation and the authored packet projection. Observed QuantLib outputs comprise dates, coupon amounts and aggregate NPVs. Per-flow inclusion and discounted contributions in valuation records are independent Python references, not an internal library trace. No payment confirmation, ledger reconciliation, entitlement record, institutional acceptance or approval is supplied.
