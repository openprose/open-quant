# Assessment: SOFR interpolation decision

## Subject and identities

- **Subject directory:** `results/sofr-curve/run-20261006T014249Z-28/`
- **Subject artifacts assessed:** `note.md` (SHA-256 `e71402da97709694ae67a3334ce751c3665e8025271fb53ae40e4cdfde682041`); `result.md` (SHA-256 `62372cec4eb9a6241696912957ef6ec82c508678cd2a69c6e9d6ddc924ecd511`).
- **Assessment contract:** `contracts/assessment.md`, SHA-256 `ceba9ce7b1f2f06bb6104842db74687b210bd5291ff7aeedf7830d980201d7c1`.
- **Subject program:** `examples/sofr-curve/program.md`, SHA-256 `d95bdb78ed9aab5f99d95cbb991af64a933532af522a0f97d065ecc7407e7d79`.
- **Selected definitions:** `contracts/model-decision.md`, SHA-256 `bdb41752fb275da6d8fc8fbf669db4d5632da09805463064e9adaf3a39d05e4f`; `contracts/claim-evidence.md`, `b023aeb88dc481b6cf31aff630a7adab28e52979827f5c6ecfda8861063d207c`; `contracts/institutional-facts.md`, `cfb18dc33211a4b511e8af40172596a4f9df592a3d99d41c93da877fd0b10ed1`.
- **House requirements:** `examples/sofr-curve/house/requirements.md`, SHA-256 `accca09492247e3a09835fe4bf4ae0ee1404d78dd0fbc5e12fdb551d656ff9a9`.
- **Bound inputs:** brief `a35d830008dca73f6430ef4bf3829947153b2b09d58c4dc64761304c928f1f57`; evidence guide `26c70e862132e5f230fbfef93962e982f12bf56f43da79cc86394d496dec2496`; numerical evidence `1b42c6b824fae587d31b9d4c17de8867690e4e1f4eda6b3c31ce82ef96730494`; institutional facts `0229a1a1211b2494622e4b0a5f89aa386772a8c314200f1493e3d30e7d953b60`.

The hashes recorded in `result.md` match these selected files. No changed requirement or input revision was found, so the recorded agreement is reconstructable.

## Content findings

### Model-decision contract — **met**

- `note.md`, **Purpose**, states the USD single-curve SOFR discount-factor purpose, 2026-09-18 as-of date, and bounded scope.
- **Decision and reasons** identifies A as log-linear discount-factor interpolation and B as the unameliorated Hagan–West monotone-convex forward-rate method with positivity collar, and attributes the choice of B and its forward-shape rationale to the developer brief. It does not claim universal superiority.
- It identifies A as an alternative and reports the supplied repricing observations. The values match `results.json` fields `repricing_max_abs_error_bp.A` and `.B` (bp; selected input instruments), and the forward-jump comparison matches `forward_smoothness.A.max_jump_bp` and `.B.max_jump_bp` (bp; measured grid through the last node). The finite-grid qualification is retained.
- **Limitations** reports the locality trade-off and exact matching values from `locality_bump_5Y_plus_1bp.A.max_change_outside_4Y_6Y_bp` and `.B.max_change_outside_4Y_6Y_bp`, including the +1 bp 5Y perturbation and 4Y–6Y window. It states this is one perturbation and notes A may be preferable for hedging.
- Scope and units are preserved; the note does not turn the evidence into a certification, current-market claim, or full methodology document.

### Claim-evidence contract — **met**

Material factual claims have accessible locators to the brief, evidence guide, or named `results.json` fields. The numerical values, methods, date, grid scope, perturbation, units, and qualifications agree with the bound evidence. The brief's rationale is explicitly attributed rather than inferred from the numbers. No unsupported external-paper claim or PV claim requiring the brief's additional payment/date qualification was introduced.

### Institutional-facts contract — **met for disclosure; facts remain unresolved**

Under **Institutional information**, all three selected gaps are visibly marked with the required convention: accountable model owner; independent reviewer and actual review/approval status; permitted production use and implementation conventions. The note explicitly says no approval, certification, or completed review is established. This satisfies disclosure, not the underlying institutional facts or approval.

### House requirements — **met**

The required opening sentence is exact; all five required headings are present; A and B are defined before use; forward differences use bp with distinguishing precision; the developer is credited; benefit and limitation include exact field locators and the as-of date; and the note is approximately 414 words under the stated counting convention (well below 700, excluding title/source list). Required institution placeholders are used and prohibited approval language is absent.

### Result-record requirements — **met for recorded content; execution claims unresolved**

`result.md` records status, actual artifact paths, unavailable runtime identity without invention, selected definition/input hashes, checks performed, and remaining institutional/boundary work. It correctly states that the task did not execute the model or recompute results. Its hash statements were independently checked. The bounded-scope status is supported for content, subject to the execution findings below.

## Execution-effect findings (separate from content)

- **Artifacts exist at the recorded paths — met.** Both expected files are present in the subject directory, and their hashes are recorded above.
- **Fresh uniquely named directory, no reuse/overwrite, and only the two files were written — unresolved.** The final directory listing shows only `note.md` and `result.md`, but the available artifacts provide no execution log, creation history, or write trace establishing freshness, uniqueness at creation, absence of overwrite, or that no other effects occurred. A correct final note/result cannot prove those claims.
- **No source/input mutation — unresolved as an execution-effect claim.** The selected source files were readable and their current hashes match the identities used, but no before/after snapshot or execution evidence proves that the invocation did not alter them.
- **No network, publication, repository integration, or institutional action — unresolved from execution evidence.** These are asserted in `result.md`, but no runtime trace establishes them. No such effect is observed in the inspected subject artifacts.

## Coverage and overall conclusion

**Content coverage:** complete for the selected model-decision, claim-evidence, institutional-facts, house, and result-record requirements. Numerical claims were checked against the retained `results.json`; model source was not executed, consistent with scope. **Execution-effect coverage:** checked against observable final state but incomplete for historical/runtime effects because execution evidence is unavailable.

**Overall invocation fulfillment: unresolved.** No mandatory content violation was found, and the note's required institutional-gap disclosure is met; however, required evidence for several execution-effect claims is unavailable. The assessment itself is complete as to the available evidence, with the execution trace/write-history limitation remaining.

No subject or input was edited by this assessment.
