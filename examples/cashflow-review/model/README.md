# Reproduce the synthetic coupon-leg calculation

The owned source constructs three variants of a receiving USD1 million fixed-rate leg with four coupons and one principal flow. It compares QuantLib amounts and six aggregate present values with Python date and arithmetic references. Selected terms are 5% simple annual coupon, Actual/360 accrual and Following payments on a weekends-only calendar. Deliberate variants use Actual/365 Fixed accrual or unadjusted payments. Both settlement-flow inclusion choices are explicit.

The development environment is Python 3.12.14 and QuantLib 1.43. From the source root, use a fresh output file:

```sh
mkdir -p results
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python examples/cashflow-review/model/measure.py results/cashflow-observations.json
```

The source refuses overwrite. It retains all flows, valuations, comparisons, diagnostics and source/dependency identities. Arithmetic/date controls use USD1e-8 for coupon amounts and USD1e-7 for NPVs. It preserves observations before exiting nonzero for failed controls; it does not adjust tolerances or repair inputs.

The fixed boundaries are November 30, 2025; February 28, May 31, August 31 and November 30, 2026. Settlement and discount reference are March 2, 2026; the hypothetical discount function is continuous 4% with Actual/365 Fixed time. QuantLib evaluation date is February 27 inside SavedSettings. The illustrative USD10 comparison does not replace payment-date requirements or constitute a financial standard.

Per-flow inclusion and discounted contributions are independent reference records, not an internal QuantLib trace. The observed library outputs are coupon amounts, dates and aggregate NPVs. These are synthetic modeled obligations, not market data, actual payments, entitlement evidence or an approved security valuation. No floating fixings, real holiday calendar, fees, amortization, optionality, ex-coupon entitlement, tax or default is modeled.

This developer reproduction is outside the report's permissions. The report may read only its selected packet and stated context, not this all-case source to reconstruct withheld evidence.
