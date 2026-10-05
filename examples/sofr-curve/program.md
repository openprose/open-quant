# Document the SOFR interpolation decision

**For agents.** Requirements and bindings for execution under the caller's selected OpenProse kernel.

Run this program under the OpenProse kernel supplied by the caller's runtime. Resolve file links relative to their containing file. The repository root is two directories above this file.

Adopt [Document a model decision](../../contracts/model-decision.md). Bind its model brief to [brief.md](inputs/brief.md), evidence to [results.json](inputs/results.json) and [the evidence guide](inputs/evidence.md), house requirements to [requirements.md](house/requirements.md), and selected institutional facts to [institutional-facts.md](inputs/institutional-facts.md). Read the adopted contract and its nested definitions. Use the brief as the source of the developer's choice and rationale; numerical claims must point to the results field that supports them.

The requested result is a note about the interpolation decision, not the complete methodology document. The committed model source is available for inspection if necessary; do not execute it, fetch new sources or recompute financial results for this task. Do not read sample results or test reference labels to obtain an answer.

Create a new, uniquely named directory under `results/sofr-curve/` at the repository root. Do not reuse or overwrite an existing run directory. Write only `note.md` and `result.md` there. Return the actual paths. In result.md, identify the supplied kernel/runtime identity when available, SHA-256 identities of the adopted contract definitions, program, house requirements and bound inputs, checks performed and remaining work. Do not invent an unavailable runtime identity.

Preserve every source, contract, house file, sample, test and previous result. No network acquisition, repository integration, publication or institutional action is requested. If execution cannot finish within the caller's limits, retain partial work and report what remains.
