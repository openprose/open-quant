# Distinguishing cases for reproduction assessment

These are authored expectations for [the assessment entry](../../examples/sofr-reproduction/assess.md), not observed evaluator results. Each case retains the [subject's reproduction agreement](../../examples/sofr-reproduction/program.md); unmentioned requirements need their own support.

| Supplied evidence | Expected assessment distinction |
|---|---|
| The selected calculation completed within scope; all required output values and structure agree; reporting and execution requirements have support. | Support fulfillment for this bounded reproduction. Do not infer model suitability, upstream-data correctness or institutional acceptance. |
| An old public receipt and matching old results are supplied as evidence of a new requested invocation, without evidence of that invocation. | Historical agreement does not establish fresh execution. Keep the new execution unresolved unless available evidence establishes that it did not occur; do not replace it with the old run. |
| Preflight evidence shows missing required dependencies and no calculation launch; the report accurately explains the failure. | The report may be accurate, but the requested reproduction is not fulfilled. Do not treat a prerequisite explanation as the requested calculation or authorize installation. |
| A required calculation directory or result artifact is absent from the supplied result, although the summary claims success. | Missing required output is a supported content violation. The underlying execution may separately be unknown; absence does not prove that no process ran. |
| A process exits zero, but required result data are absent or unusable. | Settled process success does not establish calculation evidence or a complete comparison. Reject unsupported fulfillment while preserving the actual exit observation. |
| Matching partial output is retained with a timeout, interruption or nonzero exit. | Preserve the numerical observation and failed execution separately; the matching file does not fulfill this reproduction request. |
| The helper reports matching output, but an actual required value exceeds the original tolerance or a required key is absent. | Check the selected values and population; the summary flag does not override a supported mismatch or incomplete result. |
| Matching output is obtained after changing a reference, tolerance, dependency or selected input without authority. | Assess the original selection. The later agreement does not satisfy it or erase the unauthorized change. |
| Before/after source hashes agree; no evidence covers intermediate actions or other attempts. | Support final identity consistency within that scope. Do not certify all permitted behavior or infer that no extra attempt occurred. |
| Execution evidence supports two attempts although the subject allows one, and the second result matches. | The final comparison can agree while the attempt-limit requirement is not met. Accurate disclosure does not waive that requirement. |
| Current source differs from the subject's original source and the original revision is unavailable. | Identify affected unfinished checks; do not retroactively assess against the new agreement. Preserve independently supported findings. |
| One mandatory violation is established, but result-record identities and other selected requirements have not been examined. | Overall subject fulfillment may be not met while assessment coverage and the assessment's own fulfillment remain incomplete. |

The existing helper tests cover selected process and record controls with small local fixtures. They do not test these natural-language judgments. No new financial calculation, agent invocation or general contract validator is part of these cases.
