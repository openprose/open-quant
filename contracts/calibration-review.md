# Review quantitative model calibration evidence

**For agents.** Adopt [operating report](operating-report.md) and [numerical evidence](numerical-evidence.md).

The caller supplies the model and implementation revision, calibration instruments or observations, market date, parameters and conventions, calibration outputs, and acceptance criteria. This contract reviews supplied evidence; it does not itself authorize running or recalibrating the model.

Explain the calibration objective, selected inputs and parameter constraints. Compare fitted outputs with their identified targets using the supplied residual definition, units, weighting and tolerance. Account for every expected calibration item, including rejected or unavailable observations, and distinguish the calibration set from independent evaluation data.

Report convergence claims with their supporting diagnostics and limitations. A solver's success flag alone does not establish an acceptable fit; a close fit does not establish parameter stability, economic plausibility or predictive accuracy. Preserve evidence of boundary solutions, multiple solutions and sensitivity where supplied, without inventing unperformed tests.

State which supplied criteria are met, breached or unresolved, and any further evidence needed. Do not declare calibration acceptable under an invented tolerance or infer institution-wide approval from a local numerical check.
