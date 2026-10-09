# Review quantitative model implementation evidence

**For agents.** Adopt [operating report](operating-report.md) and [numerical evidence](numerical-evidence.md).

The caller supplies the documented method and conventions, implementation and dependency identities, intended use, required test scope, observed test results and acceptance criteria. This contract reviews supplied evidence; it does not authorize executing or changing an implementation.

Explain how the implementation's inputs and outputs map to the documented quantities. Preserve units, scaling, dates, time conventions, discounting and any transformations relevant to the selected scope. Agreement between records does not establish that their common convention is the required one.

Account for each required behavior or test condition, its expected result, the observed implementation result and the evidence supporting comparison. Distinguish a proposed test, available test code and an observed execution. Identify missing coverage of selected input regimes, boundary conditions and invalid-input behavior; do not imply that unperformed tests passed.

Explain what each check can establish. Passing a mathematical identity or matching one reference case does not establish every required behavior. Identify shared code, input preparation, assumptions or other dependencies that limit a benchmark's ability to expose errors. A disputed measurement requires evidence before attributing the discrepancy to the implementation rather than the reference, inputs or observer.

Report met, breached and unresolved criteria with their exact scope and remaining evidence needs. Implementation agreement with a documented method does not establish that the method is suitable for every use, that the test scope is sufficient, or that deployment is approved. Preserve source defects and conflicting records in the report; do not repair them or infer institutional acceptance.
