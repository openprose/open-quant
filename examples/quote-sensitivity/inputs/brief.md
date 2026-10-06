# Synthetic curve risk brief

Review `SYNTHETIC-PAR-CURVE r1` as of January 1, 2026. Payments occur exactly 365 and 730 calendar days later, at times one and two under Actual/365 Fixed. Currency is USD. This is an authored annual par-coupon construction, not a production SOFR curve, swap-convention template or market observation.

The initial annual par quotes are q1=3% and q2=4%. Intended calibration is D1=1/(1+q1), D2=(1-q2 D1)/(1+q2). The common fixed-cash-flow valuation relationship is V=a D1+b D2. Continuously compounded zero rates satisfy z(t)=-log(D(t))/t. The fixed 4% instrument pays USD40,000 and USD1,040,000; the fixed 6% instrument pays USD60,000 and USD1,060,000. Principal is USD1 million. Coupons and payment dates remain fixed under perturbations.

The expected scenario population is base and plus/minus for six factors: quote_1, quote_2, quote_parallel, zero_1, zero_2 and zero_parallel. Shock size is 0.0001 in decimal rate units. Quote shocks request algebraic recalibration while holding the other quote fixed for a single-factor shock. Zero shocks request changes to D(t) through exp(-t*shock), holding the other zero fixed for a single-factor shock. No iterative calibration solver is used.

Scenario coordinate, mask, direction and requested_par_quotes describe the requested construction; they do not substitute for its numerical support. discount_nodes, implied_par_quotes and values_usd are selected native-result records. Sensitivity summaries are calculations from those values. Receipt identities refer to the complete historical calculation; a projected case can withhold some of its fields. Withholding is not evidence that a calculation never occurred.

The selected values use the stated common discounting relationship. This supplies a basis for deriving numerical implications from available evidence; label such implications as derived. It does not create a missing native record or independently prove how execution occurred. No institutional facts, trade, hedge recommendation or approval are requested.
