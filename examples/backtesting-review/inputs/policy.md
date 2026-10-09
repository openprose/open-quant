# Synthetic backtesting policy

Use the exact five-date population and model/portfolio definitions in population.md. Values are USD. VaR must be finite and nonnegative; P&L must be finite, with negative values denoting losses. A numerical exceedance occurs when loss is **strictly greater** than VaR, equivalently when P&L is less than negative VaR. Equality is not an exceedance.

A comparison is unavailable if its P&L or VaR is absent or invalid, its identity/unit is wrong, or the forecast was not available before that date's 09:00 UTC start. Identify the reason instead of inventing a number. Count each unavailable comparison as one policy exception for the affected series. An unavailable common VaR or a late forecast affects both series; missing APL alone does not make HPL unavailable.

For each series, policy exception count is observed numerical exceedances plus unavailable comparisons. Keep these components separate. The reported combined count is the **greater of the APL and HPL exception counts**, not their sum or the number of distinct exception dates. Every series retains five expected comparisons. No exclusions or waivers are supplied.

Check any supplied producer summary. Do not classify this five-day exercise into a regulatory zone, estimate an annual rate, assign a capital multiplier, conclude statistically validated performance or declare model approval. No overall pass/fail threshold is supplied; report the counts and their scope.

The separation of APL/HPL counts, their maximum, and adverse treatment of unavailable values is informed by [Basel MAR32.5 and 32.18](https://www.bis.org/committees/bcbs/basel-framework/standard/mar/32/inforce/2023-01-01/published/2020-03-27). This toy population, time window and treatment of forecast-timing defects are authored house conventions. The complete regulatory test and local applicability are outside this example. The reference is provenance, not permission to fetch or adopt additional requirements during execution.
