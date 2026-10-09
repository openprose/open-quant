# Authored reference: coupon schedule and valuation review

This is an authored illustration for the complete packet, not an agent execution or independent assessment. Subject CASHFLOW-2026-10-06 is a synthetic USD1 million receiving leg. Five obligations per construction remain in scope: four coupons and separate principal, with positive amounts. No payment or approval evidence is supplied.

## Flow evidence

Accrual boundaries remain November 30, 2025; February 28, May 31, August 31 and November 30, 2026. Coupon periods contain 90, 92, 92 and 91 days. Following adjustments on the supplied weekends-only calendar change payment dates, not accrual endpoints. This calendar does not represent real market holidays.

| Flow | Selected payment | Unadjusted payment | Selected/Unadjusted amount USD | Act/365 Fixed amount USD |
|---|---|---|---:|---:|
| C1 | 2026-03-02 | 2026-02-28 | 12500.000000 | 12328.767123 |
| C2 | 2026-06-01 | 2026-05-31 | 12777.777778 | 12602.739726 |
| C3 | 2026-08-31 | 2026-08-31 | 12777.777778 | 12602.739726 |
| C4 | 2026-11-30 | 2026-11-30 | 12638.888889 | 12465.753425 |
| P1 | 2026-11-30 | 2026-11-30 | 1000000.000000 | 1000000.000000 |

Locators: `variants.{selected,wrong_day_count,unadjusted_payment}.flows`. Both Following constructions share payment dates. Selected and Unadjusted use Act/360; Wrong day count uses Act/365 Fixed. Amounts match independent date/arithmetic references within USD1e-8 for their own terms. The latter still breaches the required accrual convention. Unadjusted payments breach Following for C1 and C2. C4 and P1 share a date but are distinct obligations; removing either loses required coverage.

## Valuation evidence

Both valuations use March 2, 2026 for settlement and discount reference, with hypothetical continuous 4% discounting on Actual/365 Fixed time. Values are absolute USD NPVs. February 27 is the library evaluation date; it does not replace settlement.

| Construction | Inclusion | Observed NPV USD | Difference from selected USD | Within USD10 |
|---|---|---:|---:|---|
| selected | exclude_settlement | 1007968.091392 | 0.000000 | Yes |
| selected | include_settlement | 1020468.091392 | 0.000000 | Yes |
| wrong_day_count | exclude_settlement | 1007455.176434 | -512.914958 | No |
| wrong_day_count | include_settlement | 1019783.943557 | -684.147835 | No |
| unadjusted_payment | exclude_settlement | 1007969.477877 | 1.386485 | Yes |
| unadjusted_payment | include_settlement | 1007969.477877 | -12498.613515 | No |

Locators: `variants.*.valuations` and `comparisons`. All six observed NPVs match independent references within USD1e-7. Reference populations include C2,C3,C4,P1 under exclusion for all constructions. Under inclusion, Following constructions add C1 on settlement; Unadjusted does not, because its C1 precedes settlement. Include-minus-exclude is USD12,500 for Selected, USD12,328.767123 for Wrong day count, and zero for Unadjusted.

The USD1.386485 Unadjusted difference under exclusion passes aggregate tolerance but cannot clear its incorrect payment dates. Under inclusion its difference is USD−12,498.613515. Both the inclusion policy and flow-level convention must remain explicit; a close total is insufficient evidence of compliance. Independent per-flow contributions are reference calculations, not an internal QuantLib trace.

## Conclusions and limits

Selected is supported within this fixed review scope. Wrong day count and Unadjusted each breach a required convention despite correct arithmetic for their stated terms. No producer assertions appear in the complete packet.

Absence of payment confirmation supports neither paid nor unpaid. The complete numerical packet establishes only the modeled calculations described above.

This review does not establish market value, entitlement, actual settlement, ledger agreement or institutional acceptance. An accurate report can fulfill its reporting requirements while identifying breaches and evidence gaps. Actual execution must supply computed input/definition identities, checks and output locations in its separate result; this illustration supplies no execution receipt.
