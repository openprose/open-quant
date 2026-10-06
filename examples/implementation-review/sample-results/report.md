# Pricing implementation evidence review

**Authored reference for the complete case; not an agent-generated result or assessment.** Reporting date: October 6, 2026. Subject: BLACK-ADAPTERS-2026-10-06, calculation source identified by the receipt.

The intended method values European call and put payoffs under a lognormal terminal forward. Inputs are forward and strike in USD per unit, decimal annual volatility, expiry in years and a continuously compounded annual rate. Output is discounted present-value USD per unit. It requires a positive forward and nonnegative strike, volatility and expiry. The API receives total standard deviation sigma*sqrt(T) and discount exp(-r*T). These are supplied conventions, not conclusions about market suitability. [Sources: inputs/brief.md; model/measure.py: domain, price, reference.]

All ten required valid-input cases are supplied once, with call and put prices for each adapter. The twelve invalid-input controls cover four selected conditions for each adapter; all record ValueError rejections. Both numerical references are usable under the illustrative policy in every case: no warnings, with reported quadrature estimate plus tail bound below 1e-9. These estimates are not rigorous error guarantees. [Source: inputs/complete.json: observations, invalid_input_controls.]

| Adapter | Mapping | Price agreement | Parity | Selected invalid inputs |
|---|---|---|---|---|
| A | Met | 10/10 cases met | 10/10 met | 4/4 rejected |
| B | Breached | 3/10 met; criterion breached | 10/10 met | 4/4 rejected |
| C | Breached | 2/10 met; criterion breached | 6/10 met; criterion breached | 4/4 rejected |

B passes annual volatility directly instead of scaling by sqrt(T). Its price comparisons pass only baseline, zero-volatility and zero-strike; its maximum absolute price discrepancy is about 26.040808 USD per unit. Every parity check passes because parity does not generally expose this common volatility error. C omits discounting; price comparisons pass only baseline and zero-expiry, with maximum discrepancy about 11.400143 USD per unit. Baseline T=1 and r=0 hides both incorrect mappings. A's largest discrepancy is about 1.42e-14 USD per unit. Counts require both call and put to pass; maxima cover both prices. [Sources: inputs/complete.json: observations[].variants; inputs/brief.md: mapping table; inputs/policy.md.]

For every case below, A meets both price and parity criteria and B meets parity. Entries show the maximum absolute call/put price discrepancy for B and C, and C’s absolute parity residual, in USD per unit. Each required bound is 1e-9; values are displayed to six significant digits.

| Case | B price error | C price error | C parity residual |
|---|---:|---:|---:|
| baseline | <1e-12 | <1e-12 | <1e-12 |
| short-expiry | 3.94808 | 0.0297963 | <1e-12 |
| long-expiry | 6.99459 | 1.79253 | <1e-12 |
| in-the-money | 2.52707 | 1.44602 | 1.16471 |
| out-of-the-money | 1.78627 | 1.34423 | 1.16471 |
| zero-volatility | <1e-12 | 1.16471 | 1.16471 |
| zero-expiry | 2.1473 | <1e-12 | <1e-12 |
| zero-strike | <1e-12 | 5.82355 | 5.82355 |
| negative-rate | 3.347 | 0.22719 | <1e-12 |
| higher-volatility | 26.0408 | 11.4001 | <1e-12 |

Zero-forward, negative-strike, negative-volatility and negative-expiry each have the required observed rejection for all three adapters. No required case is missing or duplicated in this selected packet. [Source: inputs/complete.json: named observations and invalid_input_controls.]

A meets the selected implementation criteria on this finite evidence. B and C breach them. Favorable parity and baseline results cannot replace the required price and mapping checks. All selected records are accounted for; that does not establish that this test design covers every intended use. The numerical reference uses a different calculation method but shares the inputs and lognormal assumptions. No deployment or institutional approval evidence is supplied; those facts remain unresolved. [Sources: inputs/brief.md; inputs/policy.md; receipt.json.]

This report provides the requested supported findings and explicit gaps. Its adverse adapter findings do not themselves prevent reporting fulfillment. It does not establish execution-boundary compliance or an independent assessment; a real invocation must provide its own result record and hashes.
