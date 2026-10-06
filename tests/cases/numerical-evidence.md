# Numerical evidence: distinguishing cases

These are authored illustrations for [numerical evidence](../../contracts/numerical-evidence.md), using invented inputs. They are not model executions, independent judgments or empirical financial results. Expected findings apply to the stated requirement, not to every requirement of a complete document.

## Supported comparison

**Inputs:** A retained report identifies methods A1 and B1, input revision D1, a shared 100-case evaluation sample and the same calculation environment. It reports mean absolute prediction error of 10 and 8 basis points respectively. Its measure definition says lower error is preferable for this comparison. A supplied comparison table records a reduction of 2 basis points, or 20% relative to A1's 10 basis points. No out-of-sample or production evidence is supplied.

**Result:** “B1 has lower error on the supplied sample: 2 basis points, or 20% relative to A1. This describes the retained comparison; I did not reproduce the calculations. Performance on other samples remains unestablished.” The surrounding discussion identifies the report, revisions and common conditions.

**Expected:** The comparison and its interpretation are supported within this scope. This establishes neither general model superiority nor institutional acceptance.

## Missing comparison conditions

**Inputs:** Two tables report error of 10 and 8 basis points but omit sample identity and calculation revisions. No evidence establishes shared conditions.

**Result:** “The reported errors differ by 2 basis points. Whether the difference is attributable to the methods is unresolved because the comparison conditions are unavailable.”

**Expected:** Disclosure meets the requirement to identify the limitation; the underlying method comparison remains unresolved. “B improves accuracy by 20%” would exceed the available support. Filling in plausible common conditions would violate the contract.

## Contradictory interpretation

**Inputs:** A report explicitly assigns A's error to sample D1 and B's error to a different sample D2. The executor only reads that report; no calculation is run.

**Result:** “On identical inputs, our reproduction proves B is 20% more accurate.”

**Expected:** Not met. Identical inputs contradict the report; method attribution is unsupported; reproduction contradicts the stated execution. Matching the reported numbers does not cure these failures. A corrected discussion can report both observations and their differing samples without claiming an attributable improvement or reproduction.

## Rounded equality and acceptance limits

An instrument's target and implied rates both display 3.850000 percent, while its residual is reported at finer precision as a small nonzero basis-point value. Treating the difference as exactly zero erases supplied evidence. Use the residual's precision, identify its units and retain the distinction between calibration fit and predictive quality. If a rounded residual lies on a required threshold and could fall on either side before rounding, exact equality is not established; the finding remains unresolved until sufficient precision is available. These are authored expectations, not model-evaluation results.
