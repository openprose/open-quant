# Vendor deployment review — authored reference

Case: `complete`. This is an illustration, not an agent output or independent validation. The reporting date is October 1, 2026; all records are synthetic.

The supplied snapshot contains three production deployments, D1–D3, and one excluded sandbox deployment, D4. D1 and D2 share model M-CURVE and a display name; they remain distinct deployments. This review cannot establish organization-wide discovery completeness beyond the supplied snapshot.

**Register findings.** D1 has a unique matching record R1. D2's R2 records CurveBox 2.4/base, while the deployment is 2.5/local-overlay; its version and configuration are stale or conflicting. D3 has no register record. R3 refers to D5, absent from the deployment snapshot, and remains active despite retirement record X1 effective September 20. That discrepancy is visible rather than silently deleting R3.

**Vendor and local evidence.** V1 addresses standard CurveBox 2.4, V2 reports a 2.5 interpolation change and generic vendor checks, and V3 asserts CreditBox pricing accuracy while withholding underlying records and internals. None approves the local use. Unavailable internals limit review; they do not prove the product is unsound.

D1's exact local record T1 is dated September 25 and covers C1–C3. Its maximum absolute difference is 0.4 bp against a 0.5 bp limit, so the supplied local-check criterion is met.

T2 names D2 but tests version 2.4/base, not deployed 2.5/local-overlay. Its favorable values cannot qualify the current configuration. D2 therefore has no qualifying local check. Obtain evidence for the actual version, configuration and use rather than adding a citation to T2.

D3's exact local record T3 covers all three required test cases C1–C3, but C3 is 0.8 bp and breaches the 0.5 bp limit. Its producer label of within limit conflicts with the observation. The missing register entry does not hide the adverse local evidence, and V3's generic statement does not override it. The packet-wide claim that every production deployment is registered and locally validated is unsupported by the selected packet.

The selected packet yields one supported local check, one unresolved check and one adverse check across three deployments. These are narrow reference-price checks, not complete validations or approvals. Accurate reporting can be fulfilled despite these findings; no register update, remediation, vendor contact or approval was performed.

Locators: `inputs/complete.json`, deployments D1–D4, register R1/R2/R3, retirement X1, vendor records V1–V3, local records T1–T3 and their case observations; supplied policy. An actual execution must retain its own artifact identities and result.
