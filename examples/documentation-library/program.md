# Build a two-model documentation library

**For agents.** Execute under the caller's selected OpenProse kernel. The working root is the source repository, two directories above this program.

Produce methodology documentation for both entries below by adopting their programs, including adopted definitions. Each row is a separate application with its own requirements, evidence and output scope. Reusing a definition does not merge those applications.

| Entry | Adopted program | Selection |
|---|---|---|
| SOFR curve | [SOFR documentation](../sofr-documentation/program.md) | Caller supplies `complete` or `missing-locality` |
| Credit loss | [Credit methodology](../credit-methodology/program.md) | `public-methodology` |

Ask for an absent or unknown SOFR selection. Preserve both programs' source restrictions and permitted effects within their respective scopes. Material available for one entry does not become evidence for another. Preserve sources and earlier results; use each program's required fresh result directory. No particular order, agent count or execution strategy is required.

Also produce `index.md` and `result.md` in a fresh directory under `results/documentation-library/`. The index accounts for both entries with model/revision, selected case or mode, actual document/support/result paths and hashes, requirement and input identities, supported fulfillment finding and remaining work. Identify absent artifacts instead of omitting an entry. Distinguish an executor's reported finding from what has been checked; do not present an index as an independent assessment.

The collection result identifies this program, kernel/runtime identities when available, selected bindings, index path/hash, work performed, checks, remaining work and overall fulfillment. It need not contain its own hash. Fulfillment requires both adopted programs and these collection requirements to be satisfied. A known unmet requirement prevents an overall fulfilled finding; unresolved support remains visible. An accurate index of unfinished work does not complete that work. Return the actual collection result path.

The collection permits reading its selected child requirements, evidence and actual outputs, and writing its index/result. It adds no authority to run financial code, retrieve sources, change requirements or data, publish or create institutional facts. Do not read authored references or test answers to produce the result.
