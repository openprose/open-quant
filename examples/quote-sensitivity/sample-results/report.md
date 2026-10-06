# Quote and parameter sensitivity review

Authored complete-case reference; not an observed agent result. Subject: SYNTHETIC-PAR-CURVE r1, January 1, 2026. The two fixed USD1 million instruments pay at exact one- and two-year times. Both use the same discount curve; their coupons remain fixed under shocks. [inputs/brief.md; inputs/complete.json: cashflows_usd, times_years]

The base discount factors are 0.970873786407767 and 0.924197162061240. The 4% instrument is worth USD1,000,000; the 6% instrument is worth USD1,037,901.418969. They have different cash-flow profiles, not different curves. [inputs/complete.json: scenarios[id=base]]

## Risk coordinate matters

Quote shocks change annual par-coupon inputs and recalculate both discount nodes. Zero shocks change continuously compounded zero parameters, holding the other zero fixed for a single-factor change. The same decimal bump therefore does not specify the same economic perturbation. The quote_1-plus curve has a higher D2 than the base curve; its movement offsets the D1 change for the par instrument. [inputs/brief.md; inputs/complete.json: scenarios[id=quote_1_plus], scenarios[id=zero_1_plus]]

The following signed central changes equal `[V(+0.0001)-V(-0.0001)]/2`, in USD. They are central responses scaled to one basis point, not necessarily the exact positive-shock changes. Display values are rounded to six decimals. [inputs/complete.json: sensitivities]

| Factor | 4% instrument | 6% instrument |
|---|---:|---:|
| quote_1 | 0.000000 | -1.812684 |
| quote_2 | -189.507097 | -193.151464 |
| quote_parallel | -189.507098 | -194.964150 |
| zero_1 | -3.883495 | -5.825243 |
| zero_2 | -192.233011 | -195.929800 |
| zero_parallel | -196.116506 | -201.755042 |

The exact quote_1 derivative for the 4% instrument is zero under the calibration relationship: `0.04 D1 + 1.04 D2 = 1` while q2 stays 4%. The retained central response is about USD5.8e-11, within numerical tolerance. The positive zero_1 bump instead changes its value by USD-3.883301 and changes implied q2 to approximately 4.000204926%. That is a different scenario, not a failed computation of the same scenario. The 6% instrument's quote_1 response is nonzero. [inputs/brief.md; inputs/complete.json: scenarios, sensitivities]

For the 4% instrument, the actual positive quote_2 change is USD-189.488875, distinct from its central scaled response USD-189.507097. Finite joint quote changes also need not equal sums of finite single-factor changes. A local derivative relationship does not remove finite nonlinear effects. [inputs/complete.json: sensitivities[factor=quote_2], sensitivities[factor=quote_parallel]]

## Calibration support and coverage

All thirteen selected scenarios retain both native node values, implied par quotes and both instrument values. Quote scenarios' implied quotes match the requested targets within the supplied checking tolerance. Zero scenarios are supported by their parameter perturbation relationship; preserving the other zero does not preserve the other par quote. The reported values satisfy the supplied fixed-cash-flow relationships. These conclusions concern the supplied records, not an independently observed new run. [inputs/complete.json: scenarios; inputs/requirements.md]

Thirteen scenario records provide twenty-six values and twelve two-sided sensitivity summaries. No selected fields or producer claims are withheld in complete. The numerical receipt identifies one historical calculation; this report does not reproduce it. Intended construction, numerical support and execution provenance remain separate. [receipt.json; inputs/complete.json: withheld, producer_claims]

The example omits real market conventions, settlement effects, multi-curve projection, hedging costs and actual hedge performance. It does not establish a trading recommendation, model approval, operating savings or independent institutional validation. Available evidence supports the stated synthetic coordinate comparison. Reporting and assessment by an agent remain unqualified.
