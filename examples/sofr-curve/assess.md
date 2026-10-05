# Assess a SOFR decision note

**For agents.** Requirements and bindings for execution under the caller's selected OpenProse kernel.

The caller supplies a result-directory path as the argument after this file. It must contain note.md and result.md from the selected invocation. If the path is absent, ambiguous or unreadable, request it rather than choosing a sample or another run.

Adopt [Documentation assessment](../../contracts/assessment.md). The subject agreement is [the decision program](program.md) and its adopted definitions; permitted evidence is the program's bound inputs. Read all applicable definitions. Compare the subject's recorded requirement and input hashes with the available files. If they changed and the original bytes are unavailable, report that the original agreement cannot be reconstructed; do not silently assess the old note under new requirements.

Assess all applicable content and result-record requirements. Include the developer's selected method and rationale, evidence for the forward-shape benefit and locality limitation, correct units/scope, house requirements and all selected institutional gaps. File-write or other execution-effect claims require execution evidence; a correct final note alone cannot establish them. State when that evidence is unavailable.

Use met, not met and unresolved for individual findings. The note's content is acceptable under this example only if all selected content requirements are met. Overall invocation fulfillment is unresolved if required execution-effect evidence is unavailable, even when the content meets its requirements. A disclosed institutional gap is not itself a content violation when the requirement is to disclose that gap. Report assessment coverage separately.

Create a fresh directory under `results/sofr-curve-assessments/` at the repository root and write assessment.md there. Record the subject directory and hashes, selected requirement/input identities, per-contract findings, coverage and overall conclusions. Do not edit the subject or any input. Return the assessment path; report unfinished checks faithfully.
