# Valuation comparison — authored reference

Case: `complete`. Review time: September 30, 2026 at 20:00 UTC. All inputs are synthetic. This reference is hand-authored, not a recorded execution or actual price verification.

| Position | Internal clean value, USD | Comparison clean value, USD | Internal minus comparison, USD | Finding |
|---|---:|---:|---:|---|
| P1, USD-ZERO-2028 | 984,000 | 982,000 | +2,000 | Within the USD5,000 tolerance. |
| P2, USD-ZERO-2030 | 1,926,000 | 1,936,000 | −10,000 | Exception: absolute difference exceeds tolerance. |

Both comparisons use USD prices quoted as percent of par, the required clean basis, October 2 settlement and the required review time. Values are price × par ÷ 100. For example, P1 internal value is 98.4 × 1,000,000 ÷ 100. Evidence: `inputs/packet.json`, `positions` P1–P2 and `cases.complete` Q1–Q2; `inputs/policy.md`, matching and normalization rules.

Coverage is two of two positions with usable quotes; neither quote is duplicated or unused. Internal values total USD2,910,000 and comparison values total USD2,918,000. The signed difference is −USD8,000; the sum of absolute differences is USD12,000. These describe the same complete two-position population. Offsetting signs do not resolve P2's USD10,000 exception.

The source is SYNTHETIC-FEED, whose metadata explicitly does not verify independence. The packet does not establish executable prices, vendor reliability, fair value or a required accounting adjustment. Differences are comparison findings, not realized losses or operating-cost savings. Valuation Control needs evidence or a disposition for P2. No marks or records have been changed as part of this authored illustration.

The report's content accounts for the supplied scope. It does not establish that an actual executor respected permissions; no execution trace is provided. Evidence: `inputs/packet.json`, `source_metadata`; `inputs/policy.md`, tolerance, aggregation and source limitations.
