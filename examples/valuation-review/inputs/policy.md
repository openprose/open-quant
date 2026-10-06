# Synthetic valuation-review policy

The expected population is exactly the two positions in the packet. Review time is `2026-09-30T20:00:00Z`. The report owner is the synthetic Valuation Control team. All listed instruments are synthetic zero-coupon positions; no general bond-pricing rule is supplied or requested.

Match quotes to positions by instrument, currency, settlement date and selected comparison-source ID. Preserve quote IDs and report unused or ambiguous records. Require both internal and comparison valuation times to equal the review time exactly in this small example; this is a house rule, not a recommended market-data freshness interval. Both internal and comparison price must use the `clean` basis. A dirty or unspecified basis is not convertible under this policy, even if a reader believes accrued interest should be zero.

Prices use `percent_of_par`: multiply the quoted number by the position's positive par amount and divide by 100 to obtain the position's clean value in USD. Both values must be finite and nonnegative; par must be finite and positive. Do not treat a price of 98.4 as USD98.40 for the entire position. No FX conversion, accrued-interest adjustment or price interpolation is authorized.

For a comparable position, signed difference is internal value minus comparison value. An absolute difference at or below USD5,000 is within tolerance; a larger difference is an exception. Report both the sum of signed differences and the sum of absolute differences for the comparable subset. Offsetting signs do not erase position-level exceptions. No missing or unusable quote is zero-valued.

Source metadata establishes only the supplied origin and timestamp. It does not independently establish vendor reliability, executable prices or organizational independence. Report needed evidence or disposition for exceptions and unavailable comparisons; do not infer approval or authorization for an adjustment.
