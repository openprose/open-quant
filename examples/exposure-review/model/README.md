# Netting, collateral and current exposure

Fixed constructed study, October 6, 2026. One CPU process, at most 120 seconds, no retry, network or provider call. The retained environment is Python 3.12.14 with SQLite 3.53.1. No actual trading, collateral movement, legal decision, calibration or regulatory calculation is undertaken. Retain all constructions, including deliberately wrong mappings and failed controls.

## Fixed synthetic inputs

The valuation snapshot is 2026-10-06T00:00:00Z. Positive trade values are assets to the reporting bank; negative values are liabilities. Reporting currency is USD; conversion is USD 1 per USD and USD 11/10 per EUR. NS-A1 and NS-A2 belong to CP-A; NS-B1 belongs to CP-B. Separate netting-set membership and recognition are stipulated for this illustration. A common counterparty does not grant cross-set netting. These labels do not establish an actual legal agreement.

| Trade | Netting set | Currency | Signed value |
|---|---|---|---:|
| T1 | NS-A1 | USD | 1,000,000 |
| T2 | NS-A1 | EUR | −600,000 |
| T3 | NS-A2 | USD | −400,000 |
| T4 | NS-A2 | USD | 100,000 |
| T5 | NS-B1 | USD | 500,000 |
| T6 | NS-B1 | EUR | 200,000 |

All collateral values are positive received values, allocated exclusively to their named set. No posted collateral, reuse, cross-set allocation, currency mismatch add-on or dynamic margin calculation is included. Haircuts below are authored inputs, not supervisory parameters. Eligibility and settlement are distinct fields.

| Collateral | Netting set | Currency | Market value | Haircut | Settled | Eligible |
|---|---|---|---:|---:|---|---|
| C1 | NS-A1 | USD | 100,000 | 0 | Yes | Yes |
| C2 | NS-A1 | EUR | 100,000 | 1/10 | Yes | Yes |
| C3 | NS-A1 | USD | 80,000 | 0 | No | Yes |
| C4 | NS-A2 | USD | 200,000 | 0 | Yes | Yes |
| C5 | NS-B1 | USD | 250,000 | 1/20 | Yes | Yes |
| C6 | NS-B1 | USD | 300,000 | 0 | Yes | No |

Selected recognized collateral is converted market value × (1−haircut) only for settled eligible records. Selected current exposure is max(sum signed converted trade values − recognized collateral, 0) independently per stipulated set, then summed. Excess collateral or negative net value in one set cannot offset exposure in another. No probability, future exposure, EPE, CVA, discounting, capital multiplier or loss severity is implied.

## Nine fixed constructions

1. `selected_sets`: aggregate each input table independently by netting set, then combine and floor.
2. `counterparty_pool`: use the correct conversions and recognized collateral, but pool sets within each counterparty before flooring.
3. `global_pool`: pool all trades and recognized collateral before flooring.
4. `omit_haircuts`: preserve set boundaries, settlement and eligibility, but use zero haircut on recognized collateral.
5. `include_pending`: preserve set boundaries and haircuts, but count eligible pending collateral as settled.
6. `include_ineligible`: preserve set boundaries and haircuts, but count settled ineligible collateral.
7. `invert_fx`: preserve other rules, but divide EUR amounts by 11/10 for both trades and collateral.
8. `join_before_aggregation`: join every trade to every collateral record in its set, including records with recognized value zero, then sum both sides and floor. Retain joined row counts to expose duplicated source amounts.
9. `floor_trades_first`: replace each converted trade value with its positive part before set aggregation, then subtract selected recognized collateral and floor again.

The calculations deliberately differ. Agreement with an independent implementation of a variant does not establish compliance with the selected construction. A higher or lower reported exposure is not itself a reason to accept that variant. Preserve group identities, component values, row counts and totals so correct aggregate arithmetic cannot hide wrong membership or duplication.

## Independent checks

Execute each construction once through an in-memory SQLite query; retain the exact query and native rows. Independently build exact Fraction references from source records using ordinary Python grouping. For the join construction, derive multiplicities algebraically as each trade value times the number of collateral records and each recognized collateral value times the number of trades, rather than reproducing the SQL join. Compare every group value, recognized collateral, exposure and total to absolute USD 1e-6; row counts and group identities match exactly.

Also retain signed total trade value, the sum of positive individual values and the selected unsecured sum of positive net-set values. They are different scopes, not interchangeable exposure labels. Check the selected total against hand-derived USD 623,500 and report each alternative's exact difference from it. All amounts remain unrounded in observations; display rounding is separate.

Subsequent verification reads retained evidence and uses arithmetic, not new SQL measurements. Adverse cases will change mappings, sign, FX, eligibility, settlement, haircut, join multiplicity and aggregate rows. No recalculation of the native study is authorized by a failed verifier.

## Sources and interpretation

The inspected [Basel Framework CRE52, version in force January 1, 2023](https://www.bis.org/committees/bcbs/basel-framework/standard/cre/52/inforce/2023-01-01/published/2020-06-05), paragraphs 52.1, 52.6–52.12, distinguishes recognized netting sets and haircut collateral in counterparty exposure calculations. It motivates reporting distinctions only. The selected simplified formula does not implement SA-CCR, its legal conditions, margined replacement-cost formula, potential future exposure, NICA methodology or exposure-at-default rules. No claim about current jurisdictional implementation is made.

Inspect overlap with existing credit-loss, model-data, scenario and finance reconciliation contracts before adding a public specialist definition. A reporting component should bind exposure meaning, membership and collateral recognition without deciding legal enforceability or authorizing a financial action.

## Optional reproduction

This owned source is an optional calculation, separate from the reporting-agent program. Run `python measure.py --output /path/to/fresh-observation.json` from this directory with a finite 120-second process limit. The output must not already exist. It uses Python and SQLite, with no market data or provider credentials. Preserve failed observations without retuning inputs or silently replacing an attempt.
