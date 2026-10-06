# September periodic model review — authored reference

Case: `complete`; review date October 5, 2026. This report uses authored synthetic records. It is not an observed agent execution or institutional review.

## Inventory and use

| Deployment | Current scope | Register finding |
|---|---|---|
| D1 | RATE-CURVE r3, pricing | Unique R1 matches model, revision, use, owner and lifecycle. |
| D2 | RATE-CURVE r3, stress | R2 records pricing use; current-use conflict. |
| D3 | CREDIT-PD r2, origination | R3 records r1; revision conflict. |
| D4 | CREDIT-PD r3, pilot | Sandbox; excluded from the production population. |

The production population is three deployments. One has a valid register match and two have conflicting attributes. R4 is unmatched: it records D5 as production despite supplied retirement event L1, effective September 1. The snapshot supports this reconciliation, not organization-wide discovery. D1 and D2 share a model revision but are distinct deployment/use identities.

Evidence: `inputs/complete.json`, deployments D1–D4, register R1–R4 and lifecycle L1; `inputs/policy.md`, Inventory.

## Monitoring and issues

| Expected observation | Evidence | Finding |
|---|---|---|
| E1: D1 pricing | O1, 0.8 bp | Within the 1.0 bp upper limit. |
| E2: D2 stress | No matching observation | Unresolved. O2 concerns pricing use, despite its D2/model/revision labels. |
| E3: D3 origination | O3, 0.03 probability | Breaches the 0.02 upper limit. |

Coverage retains all three expected observations: one within limit, one breach and one unresolved. O2 remains unmatched; its value of USD4 million and favorable producer label do not satisfy E2. The overall monitoring finding is **breach** because E3 is known adverse; E2's gap remains visible. Registry conflicts do not erase independently supplied monitoring evidence for E3.

I1 concerns D2 stress, owned by Market Risk and due September 30. Its producer labels it closed and records action completion September 29. O2 and accepting review V1 both concern pricing use, so neither establishes closure for the stress issue. I1 remains unsupported as closed and is overdue. Their existence, favorable value and later dates do not fix the scope mismatch.

I2 concerns D3 origination, owned by Credit Analytics, due October 10. Closure evidence is absent and the issue is open; it is not yet overdue. Market Risk needs to supply evidence or a disposition for E2/I1, and Credit Analytics for the E3 breach. These follow-ups are proposed responses, not recorded actions.

Evidence: `inputs/complete.json`, E1–E3, O1–O3, I1–I2 and V1; `inputs/policy.md`, Monitoring and Issues and closure. The three-way count preserves the expected population.

## Changes and follow-up

H1 changes D2 from pricing to stress while retaining RATE-CURVE r3. A changed use requires further review under the supplied policy; unchanged code revision is insufficient to waive it. H2 changes D3 from CREDIT-PD r1 to r2 for the same origination use and also requires further review. Both after states match the current deployment snapshot. No numerical impact comparison is supplied, so the magnitude of financial effects is unestablished. The review requirement itself is neither approval nor a declaration that the deployment is prohibited.

Evidence: `inputs/complete.json`, H1–H2 and current deployments; `inputs/policy.md`, Changes and Reporting outcome.

## Reporting scope

All supplied records are accounted for in their applicable areas. Supported reporting content can be complete despite operating gaps and adverse findings. Institutional approval and execution-boundary compliance are not established by this authored artifact; an actual invocation must supply its own result record and available execution evidence.

## Source identities

- `examples/periodic-review/program.md` — SHA-256 `57a45c79e7c6f55ec0e3115dbf379822650813992d8b1f8415f647610c38863d`.
- `contracts/model-inventory.md` — SHA-256 `530219e9e4f1c4cf27d75685cacbe1f0c10580da9f52b510744a9bcffe37c236`.
- `contracts/model-monitoring.md` — SHA-256 `b03b2f3ed6fa06c57a198bae94fd9aa37f6620b491d629f2079fd0ffe0b4c197`.
- `contracts/limitations-and-remediation.md` — SHA-256 `cd5bef8a31877c138da596797104e21d35959ad721e387c0f8a8ead9a1b4e895`.
- `contracts/model-change.md` — SHA-256 `4aa02029f7cd8d9c9e8fb7277cf86968d08011f17c813ce52e96181c269380f8`.
- `contracts/operating-report.md` — SHA-256 `e582e1c900f8f83d8a9c333e0e1900927e4e05bb5d63c66a3a4ca1007fd18e70`.
- `contracts/numerical-evidence.md` — SHA-256 `74dad32c15bea33cda09f0e3b6b97f60eee3b097705aeee5d860c7b363480183`.
- `contracts/claim-evidence.md` — SHA-256 `b023aeb88dc481b6cf31aff630a7adab28e52979827f5c6ecfda8861063d207c`.
- `contracts/institutional-facts.md` — SHA-256 `cfb18dc33211a4b511e8af40172596a4f9df592a3d99d41c93da877fd0b10ed1`.
- `examples/periodic-review/inputs/policy.md` — SHA-256 `e590c51a6c2f795ec57a0cfd5a657f87fe63e1d831721f0c67992652a4fc05a0`.
- `examples/periodic-review/inputs/complete.json` — SHA-256 `f15d93d0c9450392d21037d912974c7e56a9d211e240dbefb26e19ab30aea696`.
