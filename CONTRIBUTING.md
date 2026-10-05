# Contributing

Keep reusable documentation requirements in contracts/, model evidence and caller-owned house conventions in examples/, and verification fixtures in tests/. Conference logistics and facilitator notes belong in private company coordination, not this repository. Do not add a kernel, evaluator provider shim or private workspace dependency here.

Use ordinary Markdown and Standard Technical English. State what is required, who supplies inputs, what the executor may change, and what evidence supports assessment. A contract need not prescribe a procedure or map to one subagent. Preserve the distinction between execution completion, subject fulfillment and assessment coverage.

Changes use labeled pull requests. Explain the concrete behavior, inspect adopted dependencies and run the offline checks in the README. For requirement changes, include distinguishing cases: a supported result, missing evidence and a contradiction where appropriate. Expected fixture labels are authored references, not independent model judgments.

New agent runs need explicit finite limits, selected runtime/model identities and permission for the chosen billing route. Retain actual inputs, outputs and failed attempts separately. Never call a dry run a successful model execution or relabel an authored illustration as generated evidence.

Preserve import hashes and historical records. A changed input is a new revision; update current provenance while retaining the preceding identity in Git. Do not weaken the integrity checker to make an unexplained mismatch pass. Third-party material needs its own provenance and permitted use; the repository's MIT license does not relicense external works.
