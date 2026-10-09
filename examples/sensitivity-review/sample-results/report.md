# Authored reference: sensitivity precision review

This is an authored illustration for the complete packet, not an agent execution or independent assessment. SENSITIVITY-2026-10-06 contains three separate synthetic calls, six forward bumps per call and unrounded/cent-rounded prices: 36 derivative views, with delta and gamma assessed separately. These are hypothetical calculations, not a portfolio or market observation.

The changed factor is forward in USD. Strike, volatility, maturity and discount remain fixed. Delta units are USD PV per USD forward; gamma units are USD PV per squared USD forward. Neither is directly a finite dollar premium change. No spot conversion or recalibration is performed.

## Implementation and reference

| Case | Base PV USD | Analytic forward delta | Analytic forward gamma |
|---|---:|---:|---:|
| ATM | 15.200904102678 | 0.528423229531 | 0.008319030935 |
| OTM | 1.629626312863 | 0.145338832018 | 0.008670643840 |
| short-ATM | 0.417572753937 | 0.502019375310 | 0.381031658208 |

Locators: `records[*].base`, `.reference`, `.quantlib_analytic` and `.perturbations`. Every supplied unrounded price and analytic QuantLib derivative matches its corresponding independent reference within 1e-10. Every cent-rounded price is within USD0.005 plus floating allowance. These checks compare implementations of the same assumed Black model; they do not establish economic suitability.

## All finite-difference findings

Each cell shows signed estimate-minus-reference error and its finding. M means met; N means not met under the absolute 1e-4 criterion in the metric's units. No step is omitted or selected as universally optimal.

| Case | h USD | Unrounded delta | Unrounded gamma | Rounded delta | Rounded gamma |
|---|---:|---:|---:|---:|---:|
| ATM | 1e-06 | -1.69007e-09 (M) | -0.00298996 (N) | -0.528423 (N) | -0.00831903 (N) |
| ATM | 0.0001 | 2.41169e-11 (M) | -5.29491e-07 (M) | -0.528423 (N) | -0.00831903 (N) |
| ATM | 0.01 | -2.0798e-09 (M) | -1.01446e-10 (M) | -0.0284232 (N) | 99.9917 (N) |
| ATM | 0.1 | -2.07976e-07 (M) | -1.25306e-09 (M) | -0.0284232 (N) | -0.00831903 (N) |
| ATM | 1 | -2.07956e-05 (M) | -1.25202e-07 (M) | -0.00342323 (N) | 0.00168097 (N) |
| ATM | 5 | -0.000518702 (N) | -3.14866e-06 (M) | -0.00142323 (N) | 8.09691e-05 (M) |
| OTM | 1e-06 | -1.38127e-09 (M) | -0.000899083 (N) | -0.145339 (N) | -0.00867064 (N) |
| OTM | 0.0001 | 9.61814e-13 (M) | 1.31369e-07 (M) | -0.145339 (N) | -0.00867064 (N) |
| OTM | 0.01 | 3.22255e-09 (M) | -7.44405e-11 (M) | -0.145339 (N) | -0.00867064 (N) |
| OTM | 0.1 | 3.22239e-07 (M) | -1.02429e-08 (M) | -0.0453388 (N) | -0.00867064 (N) |
| OTM | 1 | 3.2222e-05 (M) | -1.02411e-06 (M) | -0.000338832 (N) | 0.00132936 (N) |
| OTM | 5 | 0.000804347 (N) | -2.54847e-05 (M) | 0.000661168 (N) | 0.000129356 (N) |
| short-ATM | 1e-06 | -3.01522e-09 (M) | -0.0115494 (N) | -0.502019 (N) | -0.381032 (N) |
| short-ATM | 0.0001 | 1.70789e-11 (M) | -6.90319e-07 (M) | -0.502019 (N) | -0.381032 (N) |
| short-ATM | 0.01 | -9.52557e-08 (M) | -2.8962e-06 (M) | -0.00201938 (N) | -100.381 (N) |
| short-ATM | 0.1 | -9.5041e-06 (M) | -0.00028936 (N) | -0.00201938 (N) | -0.381032 (N) |
| short-ATM | 1 | -0.000764893 (N) | -0.0265235 (N) | 0.00298062 (N) | -0.0310317 (N) |
| short-ATM | 5 | -0.00208784 (N) | -0.214465 (N) | -0.00201938 (N) | -0.214632 (N) |

Locators: `records[*].perturbations[*].views`; all 72 metric findings are accounted for. Unrounded delta meets 14/18 comparisons and gamma 12/18. Rounded delta meets 0/18 and gamma 1/18; a successful gamma row does not clear its delta. These counts describe this fixed grid, not reliability estimates.

At h=USD0.01, short-ATM rounded gamma is −100 against analytic +0.381031658208. At the two smallest bumps, rounded delta and gamma are zero in every case. Small rounding errors can dominate subtraction and division, so accurate displayed prices do not establish accurate sensitivities.

Unrounded estimates also depend on step size. ATM gamma at h=USD1e-6 is 0.005329070518, while h=USD1e-4 gives 0.008318501443 against analytic 0.008319030935. Short-ATM gamma at h=USD5 is 0.166566801421. Small-step precision loss and large-step truncation are distinct; the grid establishes no universal best bump or accuracy under other inputs.

The observed rounded-minus-unrounded differences lie inside the supplied epsilon/h and 4*epsilon/h² envelopes with their arithmetic allowance. These envelopes concern quantization only. They are neither observed total errors nor evidence that the derivative criterion is met. Even an extremely loose envelope can be satisfied by an unusable estimate.

## Limits and reporting scope

The complete packet contains no producer assertions. No market calibration, smile dynamics, stochastic simulation, hedge execution or institutional approval is established. Known finite premium changes apply to the specified shocks; scaling a local derivative does not prove the actual change for any shock.

The reporting obligation is to account accurately for these supported successes and failures, not to make all derivatives pass. Actual execution must supply computed input/definition identities, checks and output locations in its separate result; this illustration supplies no execution receipt.
